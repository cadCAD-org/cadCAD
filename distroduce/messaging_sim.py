import pandas as pd
from datetime import datetime
from tabulate import tabulate

from cadCAD import configs
from cadCAD.utils import arrange_cols
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

from distroduce.spark.session import sc
from distroduce.executor.spark import distributed_produce
from distroduce.action_policies import enter_action, message_actions, exit_action
from distroduce.state_updates import send_message, count_messages, add_send_time, current_time

# State Updates
variables = {
    'client_a': send_message('client_a'),
    'client_b': send_message('client_b'),
    'total_msg_count': count_messages,
    'total_send_time': add_send_time,
    'record_creation': current_time('record_creation')
}

# Action Policies
policy_group_1 = {
    "action_1": enter_action('server', 'room_1', 'A'),
    "action_2": enter_action('server', 'room_1', 'B')
}

policy_group_2 = {
    "action_1": message_actions('client_A', 'room_1', "Hi B", 'A', 'B'),
    "action_2": message_actions('client_B', 'room_1', "Hi A", 'B', 'A')
}

policy_group_3 = {
    "action_1": message_actions('client_A', 'room_1', "Bye B", 'A', 'B'),
    "action_2": message_actions('client_B', 'room_1', "Bye A", 'B', 'A')
}

policy_group_4 = {
    "action_1": exit_action('server', 'room_1', 'A'),
    "action_2": exit_action('server', 'room_1', 'B')
}

policy_groups = [policy_group_1, policy_group_2, policy_group_3, policy_group_4]
sim_composition = [{'policies': policy_group, 'variables': variables} for policy_group in policy_groups]

if __name__ == "__main__":
    print("Distributed Simulation: Chat Clients")
    intitial_conditions = {
        'record_creation': datetime.now(),
        'client_a': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
        'client_b': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
        'total_msg_count': 0,
        'total_send_time': 0.000000
    }
    exec_mode = ExecutionMode()


    # N = 5 = 10000 / (500 x 4)
    # T = 500
    sim_config = config_sim(
        {
            "N": 1,
            "T": range(10),
            # "T": range(5000),
        }
    )

    append_configs(
        user_id='Joshua',
        sim_configs=sim_config,
        initial_state=intitial_conditions,
        partial_state_update_blocks=sim_composition,
        policy_ops=[lambda a, b: a + b]
    )

    # parmeterize localhost, PRIVATE_IP=`hostname -I | xargs`
    kafkaConfig = {'send_topic': 'test', 'producer_config': {'bootstrap_servers': '10.0.0.7:9092', 'acks': 'all'}}
    dist_proc_ctx = ExecutionContext(context=exec_mode.dist_proc, method=distributed_produce, kafka_config=kafkaConfig)
    run = Executor(exec_context=dist_proc_ctx, configs=configs, spark_context=sc)

    i = 0
    for raw_result, tensor_field in run.execute():
        result = arrange_cols(pd.DataFrame(raw_result), False)[
            [
                'run_id', 'timestep', 'substep',
                'record_creation', 'total_msg_count', 'total_send_time'
            ]
        ]
        print()
        if i == 0:
            print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
        last = result.tail(1)
        last['msg_per_sec'] = last['total_msg_count']/last['total_send_time']
        print("Output: Head")
        print(tabulate(result.head(5), headers='keys', tablefmt='psql'))
        print("Output: Tail")
        print(tabulate(result.tail(5), headers='keys', tablefmt='psql'))
        print(tabulate(last, headers='keys', tablefmt='psql'))
        print()
        i += 1
