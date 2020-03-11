import random
import uuid
import numpy as np

N = 20
M = 20
sites = np.ones((N, M)) * 5
locations = [(n, m) for n in range(N) for m in range(M)]

n_predators = 20
n_preys = 100

initial_agents = {}

for i in range(n_preys):
  location = random.choice(locations)
  locations.remove(location)
  agent = {'type': 'prey',
           'location': location,
           'food': 10,
           'age': 0}
  initial_agents[uuid.uuid4()] = agent

for i in range(n_predators):
  location = random.choice(locations)
  locations.remove(location)
  agent = {'type': 'predator',
           'location': location,
           'food': 10,
           'age': 0}
  initial_agents[uuid.uuid4()] = agent


SITES = np.ones((N, M)) * 5
INITIAL_AGENTS = initial_agents


genesis_states = {
    'agents': INITIAL_AGENTS,
    'sites': SITES,
}
