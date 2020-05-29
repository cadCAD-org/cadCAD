"""
Model logic structure.
"""


from .parts.environment.food_regeneration import *
from .parts.agents.feeding import *
from .parts.agents.reproduction import *
from .parts.agents.movement import *
from .parts.agents.ageing import *
from .parts.agents.natural_death import *


partial_state_update_block = [
    {
        'policies': {
            'grow_food': p_grow_food
        },
        'variables': {
            'sites': s_update_food
        }
    },
    {
        'policies': {
            'increase_agent_age': p_digest_and_olden
        },
        'variables': {
            'agents': s_agent_food_age

        }
    },
    {
        'policies': {
            'move_agent': p_move_agents
        },
        'variables': {
            'agents': s_agent_location

        }
    },
    {
        'policies': {
            'reproduce_agents': p_reproduce_agents

        },
        'variables': {
            'agents': s_agent_create,

        }
    },
    {
        'policies': {
            'feed_prey': p_feed_prey
        },
        'variables': {
            'agents': s_agent_food,
            'sites': s_site_food
        }
    },
    {
        'policies': {
            'hunt_prey': p_hunt_prey
        },
        'variables': {
            'agents': s_agent_food
        }
    },
    {
        'policies': {
            'natural_death': p_natural_death
        },
        'variables': {
            'agents': s_agent_remove
        }
    }
]
