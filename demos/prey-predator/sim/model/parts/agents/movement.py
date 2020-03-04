from ..location import get_free_location


def p_move_agents(params, step, sL, s):
    """
    Move agents.
    """
    sites = s['sites']
    agents = s['agents']
    busy_locations = [agent['location'] for agent in agents.values()]
    new_locations = {}
    for label, properties in agents.items():
        new_location = get_free_location(properties['location'], sites, busy_locations)
        if new_location is not False:
            new_locations[label] = new_location
            busy_locations.append(new_location)
        else:
            continue
    return {'update_agent_location': new_locations}


def s_agent_location(params, step, sL, s, policy_input):
    updated_agents = s['agents'].copy()
    for label, location in policy_input['update_agent_location'].items():
        updated_agents[label]['location'] = location
    return ('agents', updated_agents)
