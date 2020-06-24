from copy import deepcopy


def sanitize_config(config):
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
    def rename_keys(d):
        if 'behaviors' in d:
            d['policies'] = d.pop('behaviors')

        if 'states' in d:
            d['variables'] = d.pop('states')

    if isinstance(new_partial_state_updates, list):
        for v in new_partial_state_updates:
            rename_keys(v)
    elif isinstance(new_partial_state_updates, dict):
        for k, v in new_partial_state_updates.items():
            rename_keys(v)

    del partial_state_updates
    return new_partial_state_updates
