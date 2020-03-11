"""
Model initial state.
"""

# Dependences

import random
import uuid
import numpy as np
from typing import Tuple, List, Dict

## Input parameters

### World size & initial food
N = 20
M = 20
INITIAL_SITE_FOOD = 5

### Initial agent count
PREDATOR_COUNT = 20
PREY_COUNT = 100

## Helper functions

def new_agent(agent_type: str, location: Tuple[int, int],
              food: int=10, age: int=0) -> dict:
    agent = {'type': agent_type,
             'location': location,
             'food': food,
             'age':age}
    return agent


def generate_agents(available_locations: List[Tuple[int, int]],
                    n_predators: int,
                    n_prey: int) -> Dict[str, dict]:
    initial_agents = {}
    type_queue = ['prey'] * n_prey
    type_queue += ['predator'] * n_predators
    random.shuffle(type_queue)
    for agent_type in type_queue:
        location = random.choice(available_locations)
        available_locations.remove(location)
        created_agent = new_agent(agent_type, location)
        initial_agents[uuid.uuid4()] = created_agent
    return initial_agents

## Generate initial state

sites = np.ones((N, M)) * INITIAL_SITE_FOOD
locations = [(n, m) for n in range(N) for m in range(M)]
initial_agents = generate_agents(locations, PREDATOR_COUNT, PREY_COUNT)

## Initial state object

genesis_states = {
    'agents': initial_agents,
    'sites': sites,
}
