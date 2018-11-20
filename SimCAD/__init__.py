from fn.op import foldr
from SimCAD.utils.configuration import dict_elemwise_sum


configs = []


class Configuration:
    def __init__(self, sim_config, state_dict, seed, exogenous_states, env_processes, mechanisms, behavior_ops=[foldr(dict_elemwise_sum())]):
        self.sim_config = sim_config
        self.state_dict = state_dict
        self.seed = seed
        self.exogenous_states = exogenous_states
        self.env_processes = env_processes
        self.behavior_ops = behavior_ops
        self.mechanisms = mechanisms