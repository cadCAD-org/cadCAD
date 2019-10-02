from distroduce.spark.session import sc


def distributed_produce(
        simulation_execs,
        var_dict_list,
        states_lists,
        configs_structs,
        env_processes_list,
        Ts,
        Ns,
        userIDs,
        sessionIDs,
        simulationIDs,
        runIDs,
        spark_context=sc,
        kafka_config=None
    ):
    func_params_zipped = list(
        zip(userIDs, sessionIDs, simulationIDs, runIDs, simulation_execs, configs_structs, env_processes_list)
    )
    func_params_kv = [((t[0], t[1], t[2], t[3]), (t[4], t[5], t[6])) for t in func_params_zipped]
    def simulate(k, v):
        from kafka import KafkaProducer
        prod_config = kafka_config['producer_config']
        kafka_config['producer'] = KafkaProducer(**prod_config)
        (sim_exec, config, env_procs) = [f[1] for f in func_params_kv if f[0] == k][0]
        results = sim_exec(
            v['var_dict'], v['states_lists'], config, env_procs, v['Ts'], v['Ns'],
            k[0], k[1], k[2], k[3], kafka_config
        )

        return results

    val_params = list(zip(userIDs, sessionIDs, simulationIDs, runIDs, var_dict_list, states_lists, Ts, Ns))
    val_params_kv = [
        (
            (t[0], t[1], t[2], t[3]),
            {'var_dict': t[4], 'states_lists': t[5], 'Ts': t[6], 'Ns': t[7]}
        ) for t in val_params
    ]
    results_rdd = spark_context.parallelize(val_params_kv).coalesce(1)

    return list(results_rdd.map(lambda x: simulate(*x)).collect())
