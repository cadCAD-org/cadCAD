def p_digest_and_olden(params, step, sL, s):
  agents = s['agents']
  delta_food = {agent: -1 for agent in agents.keys()}
  delta_age = {agent: +1 for agent in agents.keys()}
  return {'agent_delta_food': delta_food,
          'agent_delta_age': delta_age}


def s_agent_food_age(params, step, sL, s, policy_input):
    delta_food_by_agent = policy_input['agent_delta_food']
    delta_age_by_agent = policy_input['agent_delta_age']
    updated_agents = s['agents'].copy()

    for agent, delta_food in delta_food_by_agent.items():
        updated_agents[agent]['food'] += delta_food
    for agent, delta_age in delta_age_by_agent.items():
        updated_agents[agent]['age'] += delta_age
    return ('agents', updated_agents)
