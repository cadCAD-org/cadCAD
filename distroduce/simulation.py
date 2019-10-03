import sys
from pprint import pprint

import pandas as pd
from tabulate import tabulate

from cadCAD.utils import arrange_cols
from cadCAD.configuration import append_configs

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
# Partial State update Block
sim_composition = [{'policies': policy_group, 'variables': variables} for policy_group in policy_groups]


def main(executor, sim_config, intitial_conditions, sim_composition):
    append_configs(
        user_id='Joshua',
        sim_configs=sim_config,
        initial_state=intitial_conditions,
        partial_state_update_blocks=sim_composition,
        policy_ops=[lambda a, b: a + b]
    )
    pprint(sim_composition)

    i = 0
    for raw_result, tensor_field in executor.execute():
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
        last['msg_per_sec'] = last['total_msg_count'] / last['total_send_time']
        print("Output: Head")
        print(tabulate(result.head(5), headers='keys', tablefmt='psql'))
        print("Output: Tail")
        print(tabulate(result.tail(5), headers='keys', tablefmt='psql'))
        print(tabulate(last, headers='keys', tablefmt='psql'))
        print()
        i += 1
