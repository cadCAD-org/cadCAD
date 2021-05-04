from cadCAD import logo, version


def print_exec_info(exec_context, configs):
    print(logo)
    print(f'cadCAD Version: {version}')
    print(f'Execution Mode: {exec_context}')
    models = len(configs)
    first_sim = configs[0].sim_config
    n_t = len(first_sim['T'])
    n_m = len(first_sim['M'])
    n_n = first_sim['N']
    n_s = len(configs[0].initial_state)
    print(
        f'Dimensions of the first simulation: (Models, Timesteps, Params, Runs, Vars) = ({models}, {n_t}, {n_m}, {n_n}, {n_s})'
    )
