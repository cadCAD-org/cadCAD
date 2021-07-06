from pprint import pprint

from cadCAD import logo, version
from cadCAD.utils import flatten


def print_exec_info(exec_context, configs):
    print(logo)
    print(f'cadCAD Version: {version}')
    print(f'Execution Mode: {exec_context}')
    models = len(configs)
    sim_strs, run_vals, timestep_vals, params, sub_states = [], [], [], [], set()
    for i, config in enumerate(configs):
        sim_config = config.sim_config
        run_vals.append(sim_config['N'])
        for timestep in [*sim_config['T']]:
            timestep_vals.append(timestep)
        if type(sim_config['M']) is dict:
            params.append(len(sim_config['M']))
        for state_key in list(config.initial_state.keys()):
            sub_states.add(state_key)

        n_t = len(sim_config['T'])
        n_m = len(sim_config['M'])
        n_n = sim_config['N']
        n_s = len(config.initial_state)
        sim_strs.append(f'     Simulation {i}: (Timesteps, Params, Runs, Sub-States) = ({n_t}, {n_m}, {n_n}, {n_s})')

    timesteps = len(timestep_vals)
    if sum(params) != 0:
        param_count = sum(params)
    else:
        param_count = 1
    runs = sum(run_vals)
    init_states = len(sub_states)

    print("Simulation Dimensions:")
    print(
        f'Entire Simulation: (Models, Unique Timesteps, Params, Total Runs, Sub-States) = ({models}, {timesteps}, {param_count}, {runs}, {init_states})'
    )
    for sim_str in sim_strs:
        print(sim_str)
