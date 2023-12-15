import unittest
from copy import deepcopy

from testing.models import exp
from testing.models.param_sweep import sim_config as sim_config_a
from testing.models.param_sweep import genesis_states as genesis_states_a
from testing.models.param_sweep import env_process as env_process_a
from testing.models.param_sweep import partial_state_update_blocks as psubs_a

def append_model_id(model_ids, sim_config, genesis_states, env_process, psubs):
    exp_copy = deepcopy(exp)
    for mod_id in model_ids:
        exp_copy.append_model(
            model_id=mod_id,
            sim_configs=sim_config,
            initial_state=genesis_states,
            env_processes=env_process,
            partial_state_update_blocks=psubs,
            policy_ops=[lambda a, b: a + b]
        )
    return exp_copy


class AppendModelTest(unittest.TestCase):
    def test_index_model_ids(self):
        no_id_exp = append_model_id(
            model_ids=[None] * 10,
            sim_config=sim_config_a,
            genesis_states=genesis_states_a,
            env_process=env_process_a,
            psubs=psubs_a
        )
        expected = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.assertEqual(no_id_exp.model_ids == expected, True, "Incorrect Indexing of System Model IDs")

    def test_same_model_ids(self):
        same_id_exp = append_model_id(
            model_ids=['sys_model'] * 10,
            sim_config=sim_config_a,
            genesis_states=genesis_states_a,
            env_process=env_process_a,
            psubs=psubs_a
        )
        expected = [
            'sys_model', 'sys_model@1', 'sys_model@2', 'sys_model@3', 'sys_model@4', 'sys_model@5',
            'sys_model@6', 'sys_model@7', 'sys_model@8', 'sys_model@9'
        ]
        self.assertEqual(same_id_exp.model_ids == expected, True, "Incorrect Duplicate Indexing of System Model IDs")

    def test_different_model_ids(self):
        diff_id_exp = append_model_id(
            model_ids=[f'sys_model_{i}' for i in list(range(10))],
            sim_config=sim_config_a,
            genesis_states=genesis_states_a,
            env_process=env_process_a,
            psubs=psubs_a
        )
        expected = [
            'sys_model_0', 'sys_model_1', 'sys_model_2', 'sys_model_3', 'sys_model_4', 'sys_model_5',
            'sys_model_6', 'sys_model_7', 'sys_model_8', 'sys_model_9'
        ]
        self.assertEqual(diff_id_exp.model_ids == expected, True, "Incorrect Unique System Model IDs")

    def test_mix_model_ids(self):
        mix_exp = append_model_id(
            model_ids=[None, 'sys_model_A', None, 'sys_model_B', 'model@3', 'model@3'],
            sim_config=sim_config_a,
            genesis_states=genesis_states_a,
            env_process=env_process_a,
            psubs=psubs_a
        )
        expected = ['0', 'sys_model_A', '2', 'sys_model_B', 'model@3', 'model@3@5']
        self.assertEqual(mix_exp.model_ids == expected, True, "Incorrect System Model ID Mix")


if __name__ == '__main__':
    unittest.main()