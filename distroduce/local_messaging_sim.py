import sys
from datetime import datetime

from cadCAD import configs
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

from distroduce.simulation import main, sim_composition
from distroduce.spark.session import sc
from distroduce.executor.spark import distributed_produce

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
    sim_config = config_sim(
        {
            "N": 1,
            "T": range(10),
        }
    )

    # Configuration for Kafka Producer
    kafkaConfig = {
        'send_topic': 'test',
        'producer_config': {
            'bootstrap_servers': f'{sys.argv[1]}:9092',
            'acks': 'all'
        }
    }
    exec_mode = ExecutionMode()
    dist_proc_ctx = ExecutionContext(context=exec_mode.dist_proc, method=distributed_produce, kafka_config=kafkaConfig)
    run = Executor(exec_context=dist_proc_ctx, configs=configs, spark_context=sc)

    main(run, sim_config, initial_conditions, sim_composition)
