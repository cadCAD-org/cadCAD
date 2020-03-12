import numpy as np

@np.vectorize
def calculate_increment(value, growth_rate, max_value):
    new_value = (value + growth_rate
                 if value + growth_rate < max_value
                 else max_value)
    return new_value


def p_grow_food(params, substep, state_history, prev_state):
  """
  Increases the food supply in all sites, subject to an maximum.
  """
  regenerated_sites = calculate_increment(prev_state['sites'],
                                          params['food_growth_rate'],
                                          params['maximum_food_per_site'])
  return {'update_food': regenerated_sites}


def s_update_food(params, substep, state_history, prev_state, policy_input):
    key = 'sites'
    value = policy_input['update_food']
    return (key, value)
