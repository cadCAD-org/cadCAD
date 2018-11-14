from pathos.multiprocessing import ProcessingPool as Pool


def parallelize_simulations(f, states_list, configs, env_processes, T, N):
    def process(config):
        return f(states_list, config, env_processes, T, N)

    with Pool(len(configs)) as p:
        results = p.map(process, configs)

    return results