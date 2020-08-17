from cadCAD.configuration.utils import config_sim, access_block
from simulations.regression_tests.experiments import hist_exp

policies, variables = {}, {}
exclusion_list = ['nonexsistant', 'last_x', '2nd_to_last_x', '3rd_to_last_x', '4th_to_last_x']

# Policies per Mechanism

# WARNING: DO NOT delete elements from sH
# state_history, target_field, psu_block_offset, exculsion_list
def last_update(_g, substep, sH, s, **kwargs):
    return {"last_x": access_block(
            state_history=sH,
            target_field="last_x",
            psu_block_offset=-1,
            exculsion_list=exclusion_list
        )
    }
policies["last_x"] = last_update

def second2last_update(_g, substep, sH, s, **kwargs):
    return {"2nd_to_last_x": access_block(sH, "2nd_to_last_x", -2, exclusion_list)}
policies["2nd_to_last_x"] = second2last_update


# Internal States per Mechanism

# WARNING: DO NOT delete elements from sH
def add(y, x):
    return lambda _g, substep, sH, s, _input, **kwargs: (y, s[y] + x)
variables['x'] = add('x', 1)

# last_partial_state_update_block
def nonexsistant(_g, substep, sH, s, _input, **kwargs):
    return 'nonexsistant', access_block(sH, "nonexsistant", 0, exclusion_list)
variables['nonexsistant'] = nonexsistant

# last_partial_state_update_block
def last_x(_g, substep, sH, s, _input, **kwargs):
    return 'last_x', _input["last_x"]
variables['last_x'] = last_x

# 2nd to last partial state update block
def second_to_last_x(_g, substep, sH, s, _input, **kwargs):
    return '2nd_to_last_x', _input["2nd_to_last_x"]
variables['2nd_to_last_x'] = second_to_last_x

# 3rd to last partial state update block
def third_to_last_x(_g, substep, sH, s, _input, **kwargs):
    return '3rd_to_last_x', access_block(sH, "3rd_to_last_x", -3, exclusion_list)
variables['3rd_to_last_x'] = third_to_last_x

# 4th to last partial state update block
def fourth_to_last_x(_g, substep, sH, s, _input, **kwargs):
    return '4th_to_last_x', access_block(sH, "4th_to_last_x", -4, exclusion_list)
variables['4th_to_last_x'] = fourth_to_last_x


genesis_states = {
    'x': 0,
    'nonexsistant': [],
    'last_x': [],
    '2nd_to_last_x': [],
    '3rd_to_last_x': [],
    '4th_to_last_x': []
}

PSUB = {
    "policies": policies,
    "variables": variables
}

partial_state_update_block = {
    "PSUB1": PSUB,
    "PSUB2": PSUB,
    "PSUB3": PSUB
}

sim_config = config_sim(
    {
        "N": 2,
        "T": range(3),
    }
)


hist_exp.append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    partial_state_update_blocks=partial_state_update_block
)
