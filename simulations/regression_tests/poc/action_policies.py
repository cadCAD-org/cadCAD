from datetime import datetime
from kafka import KafkaProducer

def adjust_substep(substep):
    if substep == 0:
        new_substep = substep
    else:
        new_substep = substep - 1
    return new_substep

'''
Function that produces a single actions taken by a user and its accompanying message.

The results will be combined with a user-defined aggregation function (UDAF) 
given to the `policy_ops` argument of `cadCAD.configuration.append_configs`.
Current UDAF: `policy_ops=[lambda a, b: a + b]`
'''
def messages(client_id, room, action, _input, sender, receiver=None):
    return {
        'types': [action],
        'messages': [
            {
                'client': client_id, 'room': room, 'action': action,
                'sender': sender, 'receiver': receiver,
                'input': _input,
                'created': datetime.now()
            }
        ]
    }


'''
Policy representing a user entering a chat room and its accompanying message
'''
def enter_action(state, room, user):
    def f(_g, step, sL, s, **kwargs):
        msgs = messages(state, room, 'enter', f"{user} enters {room}", user)
        msgs['send_times'] = [0.000000]
        msgs['msg_counts'] = [len(msgs['messages'])]
        return msgs
    return f


'''
Policy representing a user sending a message to a receiver within a chat room
and its accompanying message

A Kafka Producer is used to send messages to a Kafka cluster. 
The configuration of the Kafka Producer via `cadCAD.engine.ExecutionContext`
'''
def message_actions(state, room, message_input, sender, receiver):
    msgs = messages(state, room, 'send', message_input, sender, receiver)
    msgs_list = msgs['messages']
    def send_action(_g, step, sL, s, kwargs_1):
        kafkaConfig = kwargs_1
        start_time = datetime.now()
        for msg in msgs_list:
            producer: KafkaProducer = kafkaConfig['producer']
            topic: str = kafkaConfig['send_topic']
            encoded_msg = str(msg).encode('utf-8')
            # part = adjust_substep(s['substep'])
            # print(f'PARTITION ------ {part}')
            # producer.send(topic=topic, value=encoded_msg, partition=part)
            producer.send(topic=topic, value=encoded_msg)
        msgs['send_times'] = [(datetime.now() - start_time).total_seconds()]
        msgs['msg_counts'] = [len(msgs_list)]
        return msgs

    return send_action


'''
Policy representing a user exiting a chat room and its accompanying message
'''
def exit_action(state, room, user):
    def f(_g, step, sL, s, **kwargs):
        msgs = messages(state, room, 'exit', f"{user} exited {room}", user)
        msgs_list = msgs['messages']
        msgs['send_times'] = [0.000000]
        msgs['msg_counts'] = [len(msgs_list)]
        return msgs
    return f
