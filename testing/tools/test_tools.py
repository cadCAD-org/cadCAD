from cadCAD.tools.execution import easy_run

# def test_empty_easy_run():
#     state_variables = {
#     }
#
#     params = {
#     }
#
#     psubs = [
#         {
#             'policies': {},
#             'variables': {},
#         },
#     ]
#
#     N_timesteps = 2
#
#     N_samples = 1
#
#     results = easy_run(
#         state_variables,
#         params,
#         psubs,
#         N_timesteps,
#         N_samples,
#     )
#     print(results)



def test_easy_run():
    state_variables = {
        'a':0.5,
    }

    params = {
        'c':[1, 2],
        'd':[1, 2],
    }

    def p(params, substep, state_history, previous_state):
        a_delta = 1 - params['c'] * previous_state['a']
        return {'a_delta': a_delta}

    def s(params, substep, state_history, previous_state, policy_input):
        return 'a', previous_state['a'] + policy_input['a_delta']

    psubs = [
        {
            'policies': {'p': p},
            'variables': {'a': s},
        },
    ]

    N_timesteps = 2

    N_samples = 1

    results = easy_run(
        state_variables,
        params,
        psubs,
        N_timesteps,
        N_samples,
    )
