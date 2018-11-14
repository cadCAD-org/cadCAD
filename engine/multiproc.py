from pathos.multiprocessing import ProcessingPool as Pool


def parallelize_simulations(f, states_list, configs, env_processes, T, N):
    with Pool(len(configs)) as p:
        results = p.map(lambda x: f(states_list, x[0], x[1], T, N), list(zip(configs, env_processes)))

    return results