from datetime import datetime

from cadCAD import configs
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

from simulations.regression_tests.poc.simulation import main, sim_composition

from distroduce.engine.execution import transform, distributed_simulations
from distroduce.session import sc_alt as sc

if __name__ == "__main__":
    # Initial States
    initial_conditions = {
        'record_creation': datetime.now(),
        'client_a': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
        'client_b': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
        'total_msg_count': 0,
        'total_send_time': 0.000000
    }

    '''
        Simulation Configuration:
        N = Simulation Runs
        T = Timesteps for each Partial State Update Block
    '''

    sim_config_dict = {
        "N":  3,
        "T": range(5),
    }
    # sim_config_dict = {
    #     "N": 1000,
    #     "T": range(5000),
    # }
    sim_config = config_sim(sim_config_dict)

    bootstrap_servers = ['localhost:9092']
    # bootstrap_servers = ['10.0.0.9:9092']

    # Configuration for Kafka Producer
    kafkaConfig = {
        'send_topic': 'test',
        'producer_config': {
            'bootstrap_servers': bootstrap_servers,
            'acks': 'all'
        }
    }

    parts = sim_config_dict['N']
    exec_mode = ExecutionMode()

    distributed_sims = distributed_simulations(transform(publish=False))
    distributed_ctx = ExecutionContext(context=exec_mode.distributed, method=distributed_sims, additional_objs=kafkaConfig)
    run = Executor(exec_context=distributed_ctx, configs=configs, spark_context=sc)

    main(run, sim_config, initial_conditions, sim_composition)

    # make default behind scenes
    # def rdd_trans_action(dist_obj_config, func_params_kv, rdd):
    #     # dist_obj_config: Object Injection in a good way
    #     # Sink for comparison / access
    #     simulate = dist_simulation(dist_obj_config, func_params_kv)
    #     spark_trans_action = rdd.map(simulate).collect()
    #     return list(spark_trans_action)

    # 10 executors: 10 - m4.2xlarge
    # spark.dynamicAllocation.enabled - true

    # new spark version
    # 10 M in 1.1 / 4.0 min - application_1576607651341_0002
    # .config("spark.executor.memory", "20g") \
    # spark.executor.memory - 13.3GB (total 147GB [executors included])
    # spark.executor.cores - 16 (total 16 x 10 = 160)

    # new spark version
    # 12 M in 1.6 / 4.9 min - application_1576693884747_0002
    # .config("spark.executor.memory", "25g") \
    # spark.executor.memory - 13.3GB (total 147GB [executors included])
    # spark.executor.cores - 16 (total 16 x 10 = 160)

    # new spark version
    # 14 M in 1.6 / 5.3 min - application_1576696344918_0002
    # .config("spark.executor.memory", "30g") \
    # spark.executor.memory - 13.3GB (total 147GB [executors included])
    # spark.executor.cores - 16 (total 16 x 10 = 160)

    # new spark version
    # 16 M in 1.9 / 6.3 min - application_1576696344918_0003
    # .config("spark.executor.memory", "30g") \
    # spark.executor.memory - 13.3GB (total 147GB [executors included])
    # spark.executor.cores - 16 (total 16 x 10 = 160)

    # new spark version
    # 18 M in 2 / 6.8 min - application_1576696344918_0004
    # .config("spark.executor.memory", "30g") \
    # spark.executor.memory - 13.3GB (total 147GB [executors included])
    # spark.executor.cores - 16 (total 16 x 10 = 160)

    # new spark version
    # 20 M in 2.1 / 7.6 min - application_1576696344918_0005
    # .config("spark.executor.memory", "30g") \
    # spark.executor.memory - 13.3GB (total 147GB [executors included])
    # spark.executor.cores - 16 (total 16 x 10 = 160)
    # ---------------------------------------------------------------------
    # 10 M in 2.1 / 4.1 min - application_???
    # .config("spark.executor.memory", "20g") \
    # spark.executor.memory - 13.5GB
    # spark.executor.cores - 16

    # 10 M in 2.1 / 5.3 min - application_1574186919629_0002
    # .config("spark.executor.memory", "20g") \
    # spark.executor.memory - 13.3GB
    # spark.executor.cores - 16



    # 2 M in 2.0 / 4.9 min - application_1574177687848_0008
    # .config("spark.executor.memory", "20g") \
    # spark.executor.memory - 12.7 GB
    # spark.executor.cores - 16
    # 2 M in 1.8 / 4.9 min - application_1574177687848_0006
    # spark.executor.memory - 13.3GB
    # spark.executor.cores - 16

    # 169 executors: 10 - m4.2xlarge
    # spark.dynamicAllocation.enabled - true
    # spark.executor.memory - 435MB
    # spark.executor.cores - 1

    # 8 M in 2.3 / 4.9 min - application_1574177687848_0004
    #     .config("spark.executor.memory", "2g") \
    #     .config("spark.executor.cores", "2") \
    # 8 M in 2.3 / 4.9 min - application_1574177687848_0003
    #     .config("spark.executor.memory", "2g") \
    #     .config("spark.executor.cores", "1") \
    # 8 M in 2.4 / 4.9 min - application_1574177687848_0002
    #     .config("spark.executor.memory", "1g") \
    #     .config("spark.executor.cores", "1") \

    # 34 executors: 5 - m4.2xlarge
    # 8 M in 3.7 / 6.3 min - application_1574122229644_0008
    #     .config("spark.executor.memory", "1g") \
    #     .config("spark.executor.cores", "1") \
    # 8 M in 3.6 / 6.1 min - application_1574122229644_0008
    #     .config("spark.executor.memory", "2g") \
    #     .config("spark.executor.cores", "1") \
    # 8 M in 3.7 / 6.2 min - application_1574122229644_0003
    #     .config("spark.executor.memory", "5g") \
    #     .config("spark.executor.cores", "5") \
    # 8 M in 3.7 / 6.2 min - application_1574122229644_0003
    #     .config("spark.executor.memory", "3g") \
    #     .config("spark.executor.cores", "4") \
    # 8 M in 3.7 / 6.3 min - application_1574122229644_0005
    #     .config("spark.executor.memory", "2g") \
    #     .config("spark.executor.cores", "5") \
    # 6 M in 2.9 / 4.8 min - application_1574122229644_0002
    #     .config("spark.executor.memory", "3g") \
    #     .config("spark.executor.cores", "4") \

    # ? executors: 5 - m4.xlarge
    # 6 M in 4.1 / 5.7 min - application_1574117954818_0003

    # 169 executors: 10 - m4.2xlarge
    # spark.dynamicAllocation.enabled - true
