from pathos.multiprocessing import ProcessingPool as Pool


def parallelize_simulations(fs, states_list, configs, env_processes, Ts, Ns):
    l = list(zip(fs, states_list, configs, env_processes, Ts, Ns))
    with Pool(len(configs)) as p:
        results = p.map(lambda t: t[0](t[1], t[2], t[3], t[4], t[5]), l)

    return results