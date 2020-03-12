from ..location import nearby_agents
import random

def p_feed_prey(params, substep, state_history, prev_state):
    """
    Feeds the hungry prey with all food located on its site.
    """
    agents = prev_state['agents']
    sites = prev_state['sites']
    preys = {k: v for k, v in agents.items() if v['type'] == 'prey'}
    hungry_preys = {label: properties for label, properties in preys.items()
                    if properties['food'] < params['hunger_threshold']}

    agent_delta_food = {}
    site_delta_food = {}
    for label, properties in hungry_preys.items():
        location = properties['location']
        available_food = sites[location]
        agent_delta_food[label] = available_food
        site_delta_food[location] = -available_food

    return {'agent_delta_food': agent_delta_food,
            'site_delta_food': site_delta_food}


def s_agent_food(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta_food in policy_input['agent_delta_food'].items():
        updated_agents[label]['food'] += delta_food
    return ('agents', updated_agents)


def s_site_food(params, substep, state_history, prev_state, policy_input):
    updated_sites = prev_state['sites'].copy()
    for label, delta_food in policy_input['site_delta_food'].items():
        updated_sites[label] += delta_food
    return ('sites', updated_sites)

def p_hunt_prey(params, substep, state_history, prev_state):
    """
    Feeds the hungry predators with an random nearby prey.
    """
    agents = prev_state['agents']
    sites = prev_state['sites']
    hungry_threshold = params['hunger_threshold']
    preys = {k: v for k, v in agents.items()
             if v['type'] == 'prey'}
    predators = {k: v for k, v in agents.items()
                 if v['type'] == 'predator'}
    hungry_predators = {k: v for k, v in predators.items()
                        if v['food'] < hungry_threshold}
    agent_delta_food = {}
    for predator_label, predator_properties in hungry_predators.items():
        location = predator_properties['location']
        nearby_preys = nearby_agents(location, preys)
        if len(nearby_preys) > 0:
            eaten_prey_label = random.choice(list(nearby_preys.keys()))
            delta_food = preys.pop(eaten_prey_label)['food']
            agent_delta_food[predator_label] = delta_food
            agent_delta_food[eaten_prey_label] = -1 * delta_food
        else:
            continue

    return {'agent_delta_food': agent_delta_food}
