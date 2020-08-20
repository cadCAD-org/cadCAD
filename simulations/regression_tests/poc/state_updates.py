from copy import deepcopy
from datetime import datetime
from functools import reduce

add = lambda a, b: a + b


'''
Function that maintains the state of users in a chat room
'''
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


'''
State Update used to counts sent messages
'''
def count_messages(_g, step, sL, s, actions, **kwargs):
    return 'total_msg_count', s['total_msg_count'] + reduce(add, actions['msg_counts'])


'''
State Update used to create to log message events
'''
def send_message(state):
    return lambda _g, step, sL, s, actions, **kwargs: (
        state,
        {
            'users': update_users(s[state]['users'], actions),
            'messages': actions['messages'],
            'msg_counts': reduce(add, actions['msg_counts']),
            'send_times': reduce(add, actions['send_times'])
        }
    )


'''
State Update used to sum the time taken for the Kafka Producer to send messages between users
'''
def add_send_time(_g, step, sL, s, actions, **kwargs):
    return 'total_send_time', s['total_send_time'] + reduce(add, actions['send_times'])


'''
State Update used to record the event record creation time
'''
def current_time(state):
    return lambda _g, step, sL, s, actions, **kwargs: (state, datetime.now())