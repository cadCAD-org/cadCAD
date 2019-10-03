from datetime import datetime

from cadCAD import configs
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

from distroduce.simulation import main, sim_composition
from distroduce.spark.session import sc
from distroduce.executor.spark import distributed_produce

if __name__ == "__main__":
    intitial_conditions = {
        'record_creation': datetime.now(),
        'client_a': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
        'client_b': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
        'total_msg_count': 0,
        'total_send_time': 0.000000
    }

    # N = 5 = 10000 / (500 x 4)
    # T = 500
    sim_config = config_sim(
        {
            "N": 1,
            "T": range(10),
            # "T": range(5000),
        }
    )

    exec_mode = ExecutionMode()
    kafkaConfig = {'send_topic': 'test', 'producer_config': {'bootstrap_servers': f'localhost:9092', 'acks': 'all'}}
    # kafkaConfig = {'send_topic': 'test', 'producer_config': {'bootstrap_servers': f'{sys.argv[1]}:9092', 'acks': 'all'}}
    dist_proc_ctx = ExecutionContext(context=exec_mode.dist_proc, method=distributed_produce, kafka_config=kafkaConfig)
    run = Executor(exec_context=dist_proc_ctx, configs=configs, spark_context=sc)

    main(run, sim_config, intitial_conditions, sim_composition)
