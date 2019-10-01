from datetime import datetime
from kafka import KafkaProducer

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