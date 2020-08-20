from pprint import pprint
import sys
import pandas as pd
from tabulate import tabulate

from cadCAD.utils import arrange_cols

from simulations.regression_tests.poc.action_policies import enter_action, message_actions, exit_action
from simulations.regression_tests.poc.state_updates import send_message, count_messages, add_send_time, current_time

# State Updates
from simulations.regression_tests.experiments import poc

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
    poc.append_configs(
        user_id='Joshua',
        sim_configs=sim_config,
        initial_state=intitial_conditions,
        partial_state_update_blocks=sim_composition,
        policy_ops=[lambda a, b: a + b],
        _exo_update_per_ts=False
    )
    pprint(sim_composition)

    rdd, tensor_fields, sessions = executor.execute()
    rdd_result = rdd.collect()
    result = pd.DataFrame(rdd_result)
    print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
    pprint(sessions)
    print(tabulate(result.head(100), headers='keys', tablefmt='psql'))

    # i = 0
    # lasts = []
    # mem_size = 0
    # result_count = 0
    # for raw_result, tensor_field, session in executor.execute():
    #     result = pd.DataFrame(raw_result)
    #     # sesh = result[['user_id', 'session_id', 'simulation_id', 'run_id', 'run', 'timestep', 'substep']]
    #     # print(tabulate(sesh, headers='keys', tablefmt='psql'))
    #     # exit()
    #     metrics_result = result[
    #         [
    #             'timestep', 'substep',
    #             'record_creation', 'total_msg_count', 'total_send_time'
    #         ]
    #     ]
    #     msgs_result = result[
    #         [
    #             'timestep', 'substep',
    #             'record_creation',
    #             #'client_a', 'client_b'
    #         ]
    #     ]
    #     print()
    #     result_len = len(result.index)
    #     if i == 0:
    #         print()
    #         print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    #         # print(session)
    #         # print(f'result_len: {result_len}')
    #         # print(tabulate(msgs_result.tail(5), headers='keys', tablefmt='psql'))
    #         print()
    #
    #     # print(session)
    #     # print(tabulate(sesh.head(5), headers='keys', tablefmt='psql'))
    #     print(session)
    #     # result_len = len(result.index)
    #     # print(result_len)
    #     # mem_size += sys.getsizeof(result)
    #     result_count += result_len
    #     print(tabulate(msgs_result.head(5), headers='keys', tablefmt='psql'))
    #     # print()
    #     i += 1
    # # print(mem_size / 1073741824)
    # print("df total result: " + str(result_count))
