import random
from copy import deepcopy
from datetime import timedelta, datetime

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import bound_norm_random, config_sim, time_step, env_trigger
from cadCAD.utils.sys_config import update_timestamp


def choose_rnd(x: list, choices):
    def choose(x, choices):
        for n in list(range(choices)):
            elem = random.choice(x)
            x.remove(elem)
            yield elem

    copied_list = deepcopy(x)
    results = list(choose(copied_list, choices))
    del copied_list
    return results


def message(sender, receiver, _input):
    return {'sender': sender, 'receiver': receiver, 'input': _input, 'sent_time': datetime.now()}

def enter_room_msgs(room, users):
    return [message(user, room, f"{user} enters chat-room") for user in users]

def exit_room_msgs(room, users):
    return [message(user, room, f"{user} exited chat-room") for user in users]

rooms = ['room_1', 'room_2']
user_group_1 = ['A', 'B', 'C', 'D']
user_group_2 = ['E', 'F', 'G', 'H']
room_1_messages = enter_room_msgs('room_1', random.shuffle(user_group_1))
room_2_messages = enter_room_msgs('room_2', random.shuffle(user_group_2))
def intitialize_conditions():
    users = user_group_1 + user_group_2
    messages = sorted(room_1_messages + room_2_messages, key=lambda i: i['time'])
    room_1_session = {'room': 'room_1', 'users': user_group_1, 'messages': room_1_messages}
    return {
        'client_a': room_1_session,
        'client_b': room_1_session,
        'server': {'rooms': rooms, 'users': users, 'messages': messages},
        'record_creation': datetime.now()
    }


def send_message(room, sender, receiver, _input):
    return lambda _g, step, sL, s: {
        'types': ['send'],
        'events': [
            {
                'type': 'send',
                'room': room,
                'user': sender,
                'sent': [message(sender, receiver, _input)]
            }
        ]
    }


def exit_room(room, sender):
    return lambda _g, step, sL, s: {
        'types': ['exit'],
        'events': [
            {
                'type': 'exit',
                'room': room,
                'user': sender,
                'sent': exit_room_msgs(sender, room)
            }
        ]
    }

# Policies per Mechanism
# ToDo Randomize client choices in runtime
[alpha, omega] = choose_rnd(user_group_1, 2)
a_msg1 = send_message('room_1', alpha, omega, f'Hello {omega}')
b_msg1 = send_message('room_1', omega, alpha, f'Hello {alpha}')

a_msg2 = send_message('room_1', alpha, omega, f'Bye {omega}')
b_msg2 = send_message('room_1', omega, alpha, f'Bye {alpha}')

a_msg3 = exit_room('room_1', alpha)
b_msg3 = exit_room('room_1', omega)

def remove_exited_users(users, actions):
    users = deepcopy(users)
    if 'exit' in actions['types']:
        for event in actions['events']:
            if event['type'] == 'exit':
                for user in event['user']:
                    users.remove(user)
    return users

# State Updates

# {'room': 'room_1', 'users': user_group_1, 'messages': room_1_messages}
def process_messages(_g, step, sL, s, actions):

    return 'client', {'room': s['room'], 'users': users, 'messages': actions['sent']}

def process_exits(_g, step, sL, s, actions):
    users = remove_exited_users(s['users'], actions)
    return 'server', {'rooms': s['room'], 'users': users, 'messages': actions['sent']}



update_record_creation = update_timestamp(
    'record_creation',
    timedelta(days=0, minutes=0, seconds=30),
    '%Y-%m-%d %H:%M:%S'
)

# partial_state_update_block = [
#     {
#         "policies": {
#             "b1": a_msg1,
#             "b2": b_msg1
#         },
#         "variables": {
#             "client_a": client_a_m1,
#             "client_b": client_b_m1,
#             "received": update_timestamp
#         }
#     },
#     {
#         "policies": {
#             "b1": a_msg2,
#             "b2": b_msg2
#         },
#         "variables": {
#             "s1": s1m2,
#             "s2": s2m2
#         }
#     },
#     {
#         "policies": {
#             "b1": a_msg3,
#             "b2": b_msg3
#         },
#         "variables": {
#             "s1": s1m3,
#             "s2": s2m3
#         }
#     }
# ]


sim_config = config_sim(
    {
        "N": 1,
        "T": range(5),
    }
)

# append_configs(
#     user_id='user_a',
#     sim_configs=sim_config,
#     initial_state=genesis_states,
#     env_processes=env_processes,
#     partial_state_update_blocks=partial_state_update_block,
#     policy_ops=[lambda a, b: a + b]
# )