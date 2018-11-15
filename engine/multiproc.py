from pathos.multiprocessing import ProcessingPool as Pool


def parallelize_simulations(fs, states_list, configs, env_processes, T, N):
    l = list(zip(fs, states_list, configs, env_processes))
    with Pool(len(configs)) as p:
        results = p.map(lambda x: x[0](x[1], x[2], x[3], T, N), l)
    return results