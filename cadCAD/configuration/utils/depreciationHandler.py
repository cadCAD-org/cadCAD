from copy import deepcopy


def sanitize_config(config):
    # for backwards compatibility, we accept old arguments via **kwargs
    # TODO: raise specific deprecation warnings for key == 'state_dict', key == 'seed', key == 'mechanisms'
    for key, value in config.kwargs.items():
        if key == 'state_dict':
            config.initial_state = value
        elif key == 'seed':
            config.seeds = value
        elif key == 'mechanisms':
            config.partial_state_updates = value

    if config.initial_state == {}:
        raise Exception('The initial conditions of the system have not been set')


def sanitize_partial_state_updates(partial_state_updates):
    new_partial_state_updates = deepcopy(partial_state_updates)
    # for backwards compatibility we accept the old keys
    # ('behaviors' and 'states') and rename them
    def rename_keys(d):
        if 'behaviors' in d:
            d['policies'] = d.pop('behaviors')

        if 'states' in d:
            d['variables'] = d.pop('states')


    # Also for backwards compatibility, we accept partial state update blocks both as list or dict
    # No need for a deprecation warning as it's already raised by cadCAD.utils.key_filter
    if isinstance(new_partial_state_updates, list):
        for v in new_partial_state_updates:
            rename_keys(v)
    elif isinstance(new_partial_state_updates, dict):
        for k, v in new_partial_state_updates.items():
            rename_keys(v)

    del partial_state_updates
    return new_partial_state_updates
