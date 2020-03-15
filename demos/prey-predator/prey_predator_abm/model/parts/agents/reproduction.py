import random
from uuid import uuid4
from ..location import nearby_agents, get_free_location

def p_reproduce_agents(params, substep, state_history, prev_state):
  """
  Generates an new agent through an nearby agent pair, subject to rules.
  Not done.
  """
  agents = prev_state['agents']
  sites = prev_state['sites']
  food_threshold = params['reproduction_food_threshold']
  reproduction_food = params['reproduction_food']
  reproduction_probability = params['reproduction_probability']
  busy_locations = [agent['location'] for agent in agents.values()]
  already_reproduced = []
  new_agents = {}
  agent_delta_food = {}
  for agent_type in set(agent['type'] for agent in agents.values()):
      # Only reproduce agents of the same type
    specific_agents = {label: agent for label, agent in agents.items()
                       if agent['type'] == agent_type}
    for agent_label, agent_properties in specific_agents.items():
        location = agent_properties['location']
        if (agent_properties['food'] < food_threshold or agent_label in already_reproduced):
            continue
        kind_neighbors = nearby_agents(location, specific_agents)
        available_partners = [label for label, agent in kind_neighbors.items()
                              if agent['food'] >= food_threshold
                              and label not in already_reproduced]

        reproduction_location = get_free_location(location, sites, busy_locations)

        if reproduction_location is not False and len(available_partners) > 0:
            reproduction_partner_label = random.choice(available_partners)
            reproduction_partner = agents[reproduction_partner_label]
            already_reproduced += [agent_label, reproduction_partner_label]

            agent_delta_food[agent_label] = -1.0 * reproduction_food
            agent_delta_food[reproduction_partner_label] = -1.0 * reproduction_food
            new_agent_properties = {'type': agent_type,
                                    'location': reproduction_location,
                                    'food': 2.0 * reproduction_food,
                                    'age': 0}
            new_agents[uuid4()] = new_agent_properties
            busy_locations.append(reproduction_location)

  return {'agent_delta_food': agent_delta_food,
          'agent_create': new_agents}

def s_agent_create(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, food in policy_input['agent_delta_food'].items():
        updated_agents[label]['food'] += food
    for label, properties in policy_input['agent_create'].items():
        updated_agents[label] = properties
    return ('agents', updated_agents)
