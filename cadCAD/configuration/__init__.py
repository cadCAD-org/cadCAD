from typing import Dict, Callable, List, Tuple
from pandas.core.frame import DataFrame
from collections import deque
from copy import deepcopy
import pandas as pd

from cadCAD import configs
from cadCAD.utils import key_filter
from cadCAD.configuration.utils import exo_update_per_ts
from cadCAD.configuration.utils.depreciationHandler import sanitize_partial_state_updates, sanitize_config


class Configuration(object):
    def __init__(self, user_id, subset_id, subset_window, sim_config={}, initial_state={}, seeds={}, env_processes={},
                 exogenous_states={}, partial_state_update_blocks={}, policy_ops=[lambda a, b: a + b],
                 session_id=0, simulation_id=0, run_id=1, experiment_id=0, exp_window=deque([0, None], 2), **kwargs
    ) -> None:
        self.sim_config = sim_config
        self.initial_state = initial_state
        self.seeds = seeds
        self.env_processes = env_processes
        self.exogenous_states = exogenous_states
        self.partial_state_updates = partial_state_update_blocks
        self.policy_ops = policy_ops
        self.kwargs = kwargs

        self.user_id = user_id
        self.session_id = session_id # essentially config id
        self.simulation_id = simulation_id
        self.run_id = run_id
        self.experiment_id = experiment_id
        self.exp_window = exp_window
        self.subset_id = subset_id
        self.subset_window = subset_window

        sanitize_config(self)


class Experiment:
    def __init__(self):
        self.exp_id = 0
        self.subset_id = 0
        self.exp_window = deque([self.exp_id, None], 2)
        self.subset_window = deque([self.subset_id, None], 2)

    def append_configs(
            self,
            user_id='cadCAD_user',
            sim_configs={}, initial_state={}, seeds={}, raw_exogenous_states={}, env_processes={},
            partial_state_update_blocks={}, policy_ops=[lambda a, b: a + b], _exo_update_per_ts: bool = True,
            config_list=configs
    ) -> None:

        try:
            max_runs = sim_configs[0]['N']
        except KeyError:
            max_runs = sim_configs['N']

        if _exo_update_per_ts is True:
            exogenous_states = exo_update_per_ts(raw_exogenous_states)
        else:
            exogenous_states = raw_exogenous_states

        if isinstance(sim_configs, dict):
            sim_configs = [sim_configs]

        simulation_id = 0
        if len(config_list) > 0:
            last_config = config_list[-1]
            simulation_id = last_config.simulation_id + 1

        sim_cnt = 0
        new_sim_configs = []
        for subset_id, t in enumerate(list(zip(sim_configs, list(range(len(sim_configs)))))):
            sim_config = t[0]
            sim_config['subset_id'] = subset_id
            sim_config['subset_window'] = self.subset_window
            N = sim_config['N']
            if N > 1:
                for n in range(N):
                    sim_config['simulation_id'] = simulation_id + sim_cnt
                    sim_config['run_id'] = n
                    sim_config['N'] = 1
                    # sim_config['N'] = n + 1
                    new_sim_configs.append(deepcopy(sim_config))
                del sim_config
            else:
                sim_config['simulation_id'] = simulation_id
                sim_config['run_id'] = 0
                new_sim_configs.append(deepcopy(sim_config))
                # del sim_config

            sim_cnt += 1

        run_id = 0
        for sim_config in new_sim_configs:
            subset_id = sim_config['subset_id']
            sim_config['N'] = run_id + 1
            if max_runs == 1:
                sim_config['run_id'] = run_id
            elif max_runs >= 1:
                if run_id >= max_runs:
                    sim_config['N'] = run_id - (max_runs - 1)

            self.exp_window = deepcopy(self.exp_window)
            config = Configuration(
                sim_config=sim_config,
                initial_state=initial_state,
                seeds=seeds,
                exogenous_states=exogenous_states,
                env_processes=env_processes,
                partial_state_update_blocks=partial_state_update_blocks,
                policy_ops=policy_ops,

                # session_id=session_id,
                user_id=user_id,
                session_id=f"{user_id}={sim_config['simulation_id']}_{sim_config['run_id']}",
                simulation_id=sim_config['simulation_id'],
                run_id=sim_config['run_id'],

                experiment_id=self.exp_id,
                exp_window=self.exp_window,
                subset_id=subset_id,
                subset_window=self.subset_window
            )
            configs.append(config)
            run_id += 1
        self.exp_id += 1
        self.exp_window.appendleft(self.exp_id)


class Identity:
    def __init__(self, policy_id: Dict[str, int] = {'identity': 0}) -> None:
        self.beh_id_return_val = policy_id

    def p_identity(self, var_dict, sub_step, sL, s, **kwargs):
        return self.beh_id_return_val

    def policy_identity(self, k: str) -> Callable:
        return self.p_identity

    def no_state_identity(self, var_dict, sub_step, sL, s, _input, **kwargs):
        return None

    def state_identity(self, k: str) -> Callable:
        return lambda var_dict, sub_step, sL, s, _input, **kwargs: (k, s[k])

    # state_identity = cloudpickle.dumps(state_identity)

    def apply_identity_funcs(self,
                             identity: Callable,
                             df: DataFrame,
                             cols: List[str]) -> DataFrame:
        """
        Apply the identity on each df column, using its self value as the
        argument.
        """
        fill_values = {col: identity(col) for col in cols}
        filled_df = df.fillna(fill_values)
        return filled_df


class Processor:
    def __init__(self, id: Identity = Identity()) -> None:
        self.id = id
        self.p_identity = id.p_identity
        self.policy_identity = id.policy_identity
        self.no_state_identity = id.no_state_identity
        self.state_identity = id.state_identity
        self.apply_identity_funcs = id.apply_identity_funcs

    def create_matrix_field(self, partial_state_updates, key: str) -> DataFrame:
        if key == 'variables':
            identity = self.state_identity
        elif key == 'policies':
            identity = self.policy_identity

        df = pd.DataFrame(key_filter(partial_state_updates, key))
        filled_df = self.apply_identity_funcs(identity, df, list(df.columns))
        if len(filled_df) > 0:
            return filled_df
        else:
            return pd.DataFrame({'empty': []})

    def generate_config(self, initial_state, partial_state_updates, exo_proc
                       ) -> List[Tuple[List[Callable], List[Callable]]]:

        def no_update_handler(bdf, sdf):
            if (bdf.empty == False) and (sdf.empty == True):
                bdf_values = bdf.values.tolist()
                sdf_values = [[self.no_state_identity] * len(bdf_values) for m in range(len(partial_state_updates))]
                return sdf_values, bdf_values
            elif (bdf.empty == True) and (sdf.empty == False):
                sdf_values = sdf.values.tolist()
                bdf_values = [[self.p_identity] * len(sdf_values) for m in range(len(partial_state_updates))]
                return sdf_values, bdf_values
            else:
                sdf_values = sdf.values.tolist()
                bdf_values = bdf.values.tolist()
                return sdf_values, bdf_values

        def only_ep_handler(state_dict):
            sdf_functions = [
                lambda var_dict, sub_step, sL, s, _input, **kwargs: (k, v) for k, v in zip(state_dict.keys(), state_dict.values())
            ]
            sdf_values = [sdf_functions]
            bdf_values = [[self.p_identity] * len(sdf_values)]
            return sdf_values, bdf_values

        if len(partial_state_updates) != 0:
            # backwards compatibility
            partial_state_updates = sanitize_partial_state_updates(partial_state_updates)

            bdf = self.create_matrix_field(partial_state_updates, 'policies')
            sdf = self.create_matrix_field(partial_state_updates, 'variables')
            sdf_values, bdf_values = no_update_handler(bdf, sdf)
            zipped_list = list(zip(sdf_values, bdf_values))
        else:
            sdf_values, bdf_values = only_ep_handler(initial_state)
            zipped_list = list(zip(sdf_values, bdf_values))

        return list(map(lambda x: (x[0] + exo_proc, x[1]), zipped_list))
