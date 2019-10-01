from copy import deepcopy
from datetime import timedelta, datetime
import time

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim

# session = enters('room_1', ['A', 'B'])
intitial_conditions = {
    'record_creation': datetime.now(),
    'client_a': {'users': [], 'messages': [], 'avg_send_time': 1},
    'client_b': {'users': [], 'messages': [], 'avg_send_time': 1}
}


# Actions
def message(client_id, room, action, _input, sender, receiver=None):
    # start_time = datetime.now()
    result = {
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
    # datetime.now() - start_time
    return result

def enter_action(state, room, user):
    return lambda _g, step, sL, s: message(state, room, 'enter', f"{user} enters {room}", user)

def message_action(state, room, _input, sender, receiver):
    return lambda _g, step, sL, s: message(state, room, 'send', _input, sender, receiver)

def exit_action(state, room, user):
    return lambda _g, step, sL, s: message(state, room, 'exit', f"{user} exited {room}", user)

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


def send_message(state):
    return lambda _g, step, sL, s, actions: (
        state,
        {
            'users': update_users(s[state]['users'], actions),
            'messages': actions['messages'], 'avg_send_time': 1
        }
    )

def current_time(state):
    return lambda _g, step, sL, s, actions: (state, datetime.now())

sim_composition = [
    {
        "policies": {
            "b1": enter_action('server', 'room_1', 'A'),
            "b2": enter_action('server', 'room_1', 'B')
        },
        "variables": {
            'client_a': send_message('client_a'),
            'client_b': send_message('client_b'),
            'record_creation': current_time('record_creation')
        }
    },
    {
        "policies": {
            "b1": message_action('client_A', 'room_1', "Hi B", 'A', 'B'),
            "b2": message_action('client_B', 'room_1', "Hi A", 'B', 'A')
        },
        "variables": {
            'client_a': send_message('client_a'),
            'client_b': send_message('client_b'),
            'record_creation': current_time('record_creation')
        }
    },
    {
        "policies": {
            "b1": message_action('client_A', 'room_1', "Bye B", 'A', 'B'),
            "b2": message_action('client_B', 'room_1', "Bye A", 'B', 'A')
        },
        "variables": {
            'client_a': send_message('client_a'),
            'client_b': send_message('client_b'),
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
            'record_creation': current_time('record_creation')
        }
    }
]

# 5 = 10000 / (500 x 4)
sim_config = config_sim(
    {
        "N": 5,
        "T": range(500),
    }
)

append_configs(
    user_id='user_a',
    sim_configs=sim_config,
    initial_state=intitial_conditions,
    partial_state_update_blocks=sim_composition,
    policy_ops=[lambda a, b: a + b]
)