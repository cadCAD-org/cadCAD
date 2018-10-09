# if beh list empty, repeat 0 x n_states in list
def generate_config(mechanisms, exogenous_states):
    es_funcs = [exogenous_states[state] for state in list(exogenous_states.keys())]
    config = list(
        map(
            lambda m: (
                list(mechanisms[m]["states"].values()) + es_funcs,
                list(mechanisms[m]["behaviors"].values())
            ),
            list(mechanisms.keys())
        )
    )
    return config