from functools import reduce

import pandas as pd
from copy import deepcopy
from datetime import datetime

from tabulate import tabulate

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD.utils import arrange_cols
from cadCAD import configs

from pyspark.sql import SparkSession
from pyspark.context import SparkContext

from kafka import KafkaProducer

from simulations.distributed.executor.spark.jobs import distributed_simulations
from simulations.distributed.spark.session import sc


def count(start, step):
    while True:
        yield start
        start += step

# session = enters('room_1', ['A', 'B'])
intitial_conditions = {
    'record_creation': datetime.now(),
    'client_a': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
    'client_b': {'users': [], 'messages': [], 'msg_count': 0, 'send_time': 0.0},
    'total_msg_count': 0,
    'total_send_time': 0.000000
}


# Actions
def messages(client_id, room, action, _input, sender, receiver=None):
    return {
        'types': [action],
        'messages': [
            {
                'client': client_id, 'room': room, 'action': action,
                'sender': sender, 'receiver': receiver,
                'input': _input,
                'creatred': datetime.now()
            }
        ]
    }


def enter_action(state, room, user):
    def f(_g, step, sL, s, kafkaConfig):
        msgs = messages(state, room, 'enter', f"{user} enters {room}", user)
        msgs['send_times'] = [0.000000]
        msgs['msg_counts'] = [len(msgs['messages'])]
        return msgs
    return f

def message_actions(state, room, _input, sender, receiver):
    msgs = messages(state, room, 'send', _input, sender, receiver)
    msgs_list = msgs['messages']
    def send_action(_g, step, sL, s, kafkaConfig):
        start_time = datetime.now()
        for msg in msgs_list:
            producer: KafkaProducer = kafkaConfig['producer']
            topic: str = kafkaConfig['send_topic']
            encoded_msg = str(msg).encode('utf-8')
            producer.send(topic, encoded_msg)
        msgs['send_times'] = [(datetime.now() - start_time).total_seconds()]
        msgs['msg_counts'] = [len(msgs_list)]
        return msgs

    return send_action

def exit_action(state, room, user):
    def f(_g, step, sL, s, kafkaConfig):
        msgs = messages(state, room, 'exit', f"{user} exited {room}", user)
        msgs_list = msgs['messages']
        msgs['send_times'] = [0.000000]
        msgs['msg_counts'] = [len(msgs_list)]
        return msgs
    return f

# State Updates
def update_users(users, actions, action_types=['send','enter','exit']):
    users = deepcopy(users)
    for action_type in action_types:
        if action_type in actions['types']:
            for msg in actions['messages']:
                if msg['action'] == 'send' and action_type == 'send':
                    continue
                elif msg['action'] == 'enter' and action_type == 'enter':
                    for user in msg['sender']:
                        users.append(user) # register_entered
                elif msg['action'] == 'exit' and action_type == 'exit':
                    for user in msg['sender']:
                        users.remove(user) # remove_exited
    return users

add = lambda a, b: a + b
def count_messages(_g, step, sL, s, actions, kafkaConfig):
    return 'total_msg_count', s['total_msg_count'] + reduce(add, actions['msg_counts'])

def add_send_time(_g, step, sL, s, actions, kafkaConfig):
    return 'total_send_time', s['total_send_time'] + reduce(add, actions['send_times'])

def send_message(state):
    return lambda _g, step, sL, s, actions, kafkaConfig: (
        state,
        {
            'users': update_users(s[state]['users'], actions),
            'messages': actions['messages'],
            'msg_counts': reduce(add, actions['msg_counts']),
            'send_times': reduce(add, actions['send_times'])
        }
    )

def current_time(state):
    return lambda _g, step, sL, s, actions, kafkaConfig: (state, datetime.now())

sim_composition = [
    {
        "policies": {
            "b1": enter_action('server', 'room_1', 'A'),
            "b2": enter_action('server', 'room_1', 'B')
        },
        "variables": {
            'client_a': send_message('client_a'),
            'client_b': send_message('client_b'),
            'total_msg_count': count_messages,
            'total_send_time': add_send_time,
            'record_creation': current_time('record_creation')
        }
    },
    {
        "policies": {
            "b1": message_actions('client_A', 'room_1', "Hi B", 'A', 'B'),
            "b2": message_actions('client_B', 'room_1', "Hi A", 'B', 'A')
        },
        "variables": {
            'client_a': send_message('client_a'),
            'client_b': send_message('client_b'),
            'total_msg_count': count_messages,
            'total_send_time': add_send_time,
            'record_creation': current_time('record_creation')
        }
    },
    {
        "policies": {
            "b1": message_actions('client_A', 'room_1', "Bye B", 'A', 'B'),
            "b2": message_actions('client_B', 'room_1', "Bye A", 'B', 'A')
        },
        "variables": {
            'client_a': send_message('client_a'),
            'client_b': send_message('client_b'),
            'total_msg_count': count_messages,
            'total_send_time': add_send_time,
            'record_creation': current_time('record_creation')
        }
    },
    {
        "policies": {
            "b1": exit_action('server', 'room_1', 'A'),
            "b2": exit_action('server', 'room_1', 'B')
        },
        "variables": {
            'client_a': send_message('client_a'),
            'client_b': send_message('client_b'),
            'total_msg_count': count_messages,
            'total_send_time': add_send_time,
            'record_creation': current_time('record_creation')
        }
    }
]

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
    user_id='user_a',
    sim_configs=sim_config,
    initial_state=intitial_conditions,
    partial_state_update_blocks=sim_composition,
    policy_ops=[lambda a, b: a + b]
)

exec_mode = ExecutionMode()

print("Simulation Execution: Distributed Execution")


dist_proc_ctx = ExecutionContext(
    context=exec_mode.dist_proc, method=distributed_simulations
)
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
    print("Output:")
    print(tabulate(result.head(5), headers='keys', tablefmt='psql'))
    print(tabulate(result.tail(5), headers='keys', tablefmt='psql'))
    print(tabulate(last, headers='keys', tablefmt='psql'))
    print()
    i += 1