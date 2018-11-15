configs = []

class Config(object):
    def __init__(self, sim_config, state_dict, seed, exogenous_states, env_processes, behavior_ops, mechanisms):
        self.sim_config = sim_config
        self.state_dict = state_dict
        self.seed = seed
        self.exogenous_states = exogenous_states
        self.env_processes = env_processes
        self.behavior_ops = behavior_ops
        self.mechanisms = mechanisms
