from typing import Dict, Callable, List, Tuple
from pandas.core.frame import DataFrame
from datetime import datetime
from collections import deque
from copy import deepcopy
import pandas as pd

from cadCAD.utils import key_filter
from cadCAD.configuration.utils import exo_update_per_ts, configs_as_objs
from cadCAD.configuration.utils.depreciationHandler import sanitize_partial_state_updates, sanitize_config


class Configuration():
    def __init__(self, user_id, model_id, subset_id, subset_window, sim_config={}, initial_state={}, seeds={}, env_processes={},
                 exogenous_states={}, partial_state_update_blocks={}, policy_ops=[lambda a, b: a + b],
                 session_id=0, simulation_id=0, run_id=1, experiment_id=0, exp_window=deque([0, None], 2),
                 exp_creation_ts=None, **kwargs
    ) -> None:
        self.sim_config = sim_config
        self.initial_state = initial_state
        self.seeds = seeds
        self.env_processes = env_processes
        self.exogenous_states = exogenous_states
        self.partial_state_update_blocks = partial_state_update_blocks
        self.policy_ops = policy_ops
        self.kwargs = kwargs

        self.session_id = session_id  # essentially config id

        self.experiment_id = experiment_id
        self.user_id = user_id
        self.model_id = model_id
        self.exp_creation_ts = exp_creation_ts

        self.labeled_jobs = {}
        self.simulation_id = simulation_id
        self.subset_id = subset_id
        self.run_id = run_id

        self.exp_window = exp_window
        self.subset_window = subset_window

        sanitize_config(self)


class Experiment(object):
    def __init__(self):
        self.exp_creation_ts = str(datetime.utcnow())
        self.configs = []
        self.sys_configs = []

        self.model_job_map, self.model_job_counts = {}, {}
        self.model_ids = list(self.model_job_map.keys())
        self.model_id_queue = []

        self.exp_id = 0
        self.simulation_id = -1
        self.subset_id = 0
        self.exp_window = deque([self.exp_id, None], 2)
        self.subset_window = deque([self.subset_id, None], 2)


    def append_model(
            self,
            user_id='cadCAD_user',
            model_id='sys_model_#',
            sim_configs={}, initial_state={}, seeds={}, raw_exogenous_states={}, env_processes={},
            partial_state_update_blocks={}, policy_ops=[lambda a, b: a + b], _exo_update_per_ts: bool = True, **kwargs
            # config_list=deepcopy(global_configs)
    ) -> None:
        _sim_configs = deepcopy(sim_configs)
        # self.configs = config_list
        self.simulation_id += 1

        try:
            max_runs = _sim_configs[0]['N']
        except KeyError:
            max_runs = _sim_configs['N']

        if _exo_update_per_ts is True:
            exogenous_states = exo_update_per_ts(raw_exogenous_states)
        else:
            exogenous_states = raw_exogenous_states

        if isinstance(_sim_configs, dict):
            _sim_configs = [_sim_configs]

        sim_cnt_local = 0
        new_sim_configs = []
        for subset_id, t in enumerate(list(zip(_sim_configs, list(range(len(_sim_configs)))))):
            sim_config = t[0]
            sim_config['subset_id'] = subset_id
            sim_config['subset_window'] = self.subset_window
            N = sim_config['N']
            if N > 1:
                for n in range(N):
                    sim_config['simulation_id'] = self.simulation_id
                    sim_config['run_id'] = n
                    sim_config['N'] = 1
                    new_sim_configs.append(deepcopy(sim_config))
                del sim_config
            else:
                sim_config['simulation_id'] = self.simulation_id
                sim_config['run_id'] = 0
                new_sim_configs.append(deepcopy(sim_config))

            sim_cnt_local += 1

        run_id = 0
        new_model_ids, new_configs = [], []
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
                exp_creation_ts=self.exp_creation_ts,

                sim_config=sim_config,
                initial_state=initial_state,
                seeds=seeds,
                exogenous_states=exogenous_states,
                env_processes=env_processes,
                partial_state_update_blocks=partial_state_update_blocks,
                policy_ops=policy_ops,

                # session_id=session_id,
                user_id=user_id,
                model_id=model_id,
                session_id=f"{user_id}={sim_config['simulation_id']}_{sim_config['run_id']}",

                experiment_id=self.exp_id,
                simulation_id=self.simulation_id,
                subset_id=subset_id,
                run_id=sim_config['run_id'],

                exp_window=self.exp_window,
                subset_window=self.subset_window
            )

            # self.configs.append(config)
            new_configs.append(config)
            new_model_ids.append(model_id)
            run_id += 1
        self.configs += new_configs
        self.model_id_queue += new_model_ids
        self.exp_id += 1
        self.exp_window.appendleft(self.exp_id)
        self.sys_configs += configs_as_objs(new_configs)

        unique_new_model_ids = list(set(new_model_ids))
        new_model_job_list = [(model_id, []) for model_id in unique_new_model_ids]
        for model_id, v in new_model_job_list:
            if model_id not in self.model_ids:
                self.model_job_map[model_id] = v
                self.model_ids.append(model_id)
            else:
                except_str = f"""
                    Error: Duplicate model_id in Experiment - \'{model_id}\' in {self.model_ids} 
                    -- Specify unique model_id for each use of `.append_config` per `Experiment()`
                """
                raise Exception(except_str)

        for model_id, job in list(zip(new_model_ids, new_configs)):
            self.model_job_map[model_id].append(job)

        self.model_job_counts = dict([(k, len(v)) for k, v in self.model_job_map.items()])

    append_configs = append_model


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
