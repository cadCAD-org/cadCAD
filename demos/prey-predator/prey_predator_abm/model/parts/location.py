"""
Helper functions associated with location
"""


import numpy as np
import random
from typing import *


def check_location(position: tuple,
                   all_sites: np.matrix,
                   busy_locations: List[tuple]) -> List[tuple]:
    """
    Returns an list of available location tuples neighboring an given
    position location.
    """
    N, M = all_sites.shape
    potential_sites = [(position[0], position[1] + 1),
                       (position[0], position[1] - 1),
                       (position[0] + 1, position[1]),
                       (position[0] - 1, position[1])]
    potential_sites = [(site[0] % N, site[1] % M) for site in potential_sites]
    valid_sites = [site for site in potential_sites if site not in busy_locations]
    return valid_sites


def get_free_location(position: tuple,
                      all_sites: np.matrix,
                      used_sites: List[tuple]) -> tuple:
    """
    Gets an random free location neighboring an position. Returns False if
    there aren't any location available.
    """
    available_locations = check_location(position, all_sites, used_sites)
    if len(available_locations) > 0:
        return random.choice(available_locations)
    else:
        return False


def nearby_agents(location: tuple, agents: Dict[str, dict]) -> Dict[str, dict]:
    """
    Filter the non-nearby agents.
    """
    neighbors = {label: agent for label, agent in agents.items()
                 if is_neighbor(agent['location'], location)}
    return neighbors


def is_neighbor(location_1: tuple, location_2: tuple) -> bool:
    dx = np.abs(location_1[0] - location_2[0])
    dy = (location_1[1] - location_2[0])
    distance = dx + dy
    if distance == 1:
        return True
    else:
        return False
