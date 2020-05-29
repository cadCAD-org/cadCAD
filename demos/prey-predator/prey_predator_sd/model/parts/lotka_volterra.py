import numpy as np

## Policies

def p_reproduce_prey(params, substep, state_history, prev_state):
    born_population = prev_state['prey_population']
    born_population *= params['prey_reproduction_rate']
    born_population *= params['dt']
    return {'add_prey': born_population}


def p_reproduce_predators(params, substep, state_history, prev_state):
    born_population = prev_state['predator_population']
    born_population *= prev_state['prey_population']  
    born_population *= params['predator_interaction_factor']
    born_population *= params['dt']
    return {'add_predators': born_population}


def p_eliminate_prey(params, substep, state_history, prev_state):
    population = prev_state['prey_population']
    natural_elimination = population * params['prey_death_rate']
    
    interaction_elimination = population * prev_state['predator_population']
    interaction_elimination *= params['prey_interaction_factor']
    
    eliminated_population = natural_elimination + interaction_elimination
    eliminated_population *= params['dt']
    return {'add_prey': -1.0 * eliminated_population}


def p_eliminate_predators(params, substep, state_history, prev_state):
    population = prev_state['predator_population']
    eliminated_population = population * params['predator_death_rate']
    eliminated_population *= params['dt']
    return {'add_predators': -1.0 * eliminated_population}


## SUFs

def s_prey_population(params, substep, state_history, prev_state, policy_input):
    updated_prey_population = np.ceil(prev_state['prey_population'] + policy_input['add_prey'])
    return ('prey_population', max(updated_prey_population, 0))


def s_predator_population(params, substep, state_history, prev_state, policy_input):
    updated_predator_population = np.ceil(prev_state['predator_population'] + policy_input['add_predators'])
    return ('predator_population', max(updated_predator_population, 0))