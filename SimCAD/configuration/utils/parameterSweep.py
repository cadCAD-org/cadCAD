import inspect
from copy import deepcopy
from funcy import curry

from SimCAD.utils import rename
from SimCAD.configuration.utils import exo_update_per_ts


class ParamSweep:
    def __init__(self, sweep_list, mechs=None, raw_exogenous_states=None, _exo_update_per_ts=True):
        self.sweep_list = sweep_list
        self.mechs = mechs
        self.raw_exogenous_states = raw_exogenous_states
        self._exo_update_per_ts = _exo_update_per_ts

    def mechanisms(self):
        swept_mechanisms = mech_sweep_identifier(self.sweep_list, self.mechs)
        return parameterize_mechanism(swept_mechanisms)

    def exogenous_states(self):
        swept_raw_exogenous_states = exo_sweep_identifier(self.sweep_list, self.raw_exogenous_states)
        return parameterize_states(swept_raw_exogenous_states, self._exo_update_per_ts)


def sweep(params, sweep_f):
    return [
        rename("sweep_"+sweep_f.__name__+"_"+str(i), curry(sweep_f)(param))
        for param, i in zip(params, range(len(params)))
    ]


def mech_sweep_identifier(sweep_list, mechanisms):
    new_mechanisms = deepcopy(mechanisms)
    for mech, update_types in new_mechanisms.items():
        for update_type, fkv in update_types.items():
            for sk, current_f in fkv.items():
                current_f_arg_len = len(inspect.getfullargspec(current_f).args)
                if update_type == 'behaviors' and current_f_arg_len == 4:
                    new_mechanisms[mech][update_type][sk] = sweep(sweep_list, current_f)
                elif update_type == 'states' and current_f_arg_len == 5:
                    new_mechanisms[mech][update_type][sk] = sweep(sweep_list, current_f)

    del mechanisms
    return new_mechanisms


def exo_sweep_identifier(sweep_list, exo_states):
    new_exo_states = deepcopy(exo_states)
    for sk, current_f in exo_states.items():
        current_f_arg_len = len(inspect.getfullargspec(current_f).args)
        if current_f_arg_len == 5:
            new_exo_states[sk] = sweep(sweep_list, current_f)

    del exo_states
    return new_exo_states


def zip_sweep_functions(sweep_lists):
    zipped_sweep_lists = []
    it = iter(sweep_lists)
    the_len = len(next(it))
    same_len_ind = all(len(l) == the_len for l in it)
    count_ind = len(sweep_lists) >= 2
    if same_len_ind is True and count_ind is True:
        return list(map(lambda x: list(x), list(zip(*sweep_lists))))
    elif same_len_ind is False or count_ind is False:
        return sweep_lists
    else:
        raise ValueError('lists have different lengths!')


# ToDo: Not producing multiple dicts.
def create_sweep_config_list(zipped_sweep_lists, states_dict, state_type_ind='mechs'):
    configs = []
    for f_lists in zipped_sweep_lists:
        new_states_dict = deepcopy(states_dict)
        for f_dict in f_lists:
            if state_type_ind == 'mechs':
                updates = list(f_dict.values()).pop()
                functs = list(updates.values()).pop()

                mech = list(f_dict.keys()).pop()
                update_type = list(updates.keys()).pop()
                sk = list(functs.keys()).pop()
                vf = list(functs.values()).pop()

                new_states_dict[mech][update_type][sk] = vf
            elif state_type_ind == 'exo_proc':
                sk = list(f_dict.keys()).pop()
                vf = list(f_dict.values()).pop()

                new_states_dict[sk] = vf
            else:
                raise ValueError("Incorrect \'state_type_ind\'")

        configs.append(new_states_dict)
        del new_states_dict

    return configs


def parameterize_states(exo_states, _exo_update_per_ts):
    sweep_lists = []
    for sk, vfs in exo_states.items():
        id_sweep_lists = []
        if isinstance(vfs, list):
            for vf in vfs:
                id_sweep_lists.append({sk: vf})
        if len(id_sweep_lists) != 0:
            sweep_lists.append(id_sweep_lists)

    def comp_exo_update(states_configs):
        return [exo_update_per_ts(x) if _exo_update_per_ts is True else x for x in states_configs]

    sweep_lists_len = len(sweep_lists)
    if sweep_lists_len != 0:
        zipped_sweep_lists = zip_sweep_functions(sweep_lists)
        states_configs = create_sweep_config_list(zipped_sweep_lists, exo_states, "exo_proc")
        return comp_exo_update(states_configs)
    elif sweep_lists_len == 0:
        return comp_exo_update([exo_states])


def parameterize_mechanism(mechanisms):
    sweep_lists = []
    for mech, update_types in mechanisms.items():
        for update_type, fkv in update_types.items():
            for sk, vfs in fkv.items():
                id_sweep_lists = []
                if isinstance(vfs, list):
                    for vf in vfs:
                        id_sweep_lists.append({mech: {update_type: {sk: vf}}})
                if len(id_sweep_lists) != 0:
                    sweep_lists.append(id_sweep_lists)

    if len(sweep_lists) == 0:
        return [mechanisms]

    zipped_sweep_lists = zip_sweep_functions(sweep_lists)
    mechanisms_configs = create_sweep_config_list(zipped_sweep_lists, mechanisms, "mechs")

    return mechanisms_configs
