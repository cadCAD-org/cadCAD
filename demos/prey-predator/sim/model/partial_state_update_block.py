from .parts.environment.food_regeneration import *
from .parts.agents.feeding import *
from .parts.agents.reproduction import *
from .parts.agents.movement import *
from .parts.agents.ageing import *
from .parts.agents.natural_death import *


partial_state_update_block = [
    {
        'label': 'Grow food',
        'description': 'Grow food at every site',
        'ignore': False,
        'policies': {
            'grow_food': p_grow_food
        },
        'variables': {
            'sites': s_update_food
        }
    },
    {
        'label': 'Digest and olden agents',
        'description': '',
        'ignore': False,
        'policies': {
            'increase_agent_age': p_digest_and_olden
        },
        'variables': {
            'agents': s_agent_food_age

        }
    },
    {
        'label': 'Move agents',
        'description': '',
        'ignore': False,
        'policies': {
            'move_agent': p_move_agents
        },
        'variables': {
            'agents': s_agent_location

        }
    },
    {
        'label': 'Reproduce agents',
        'description': '',
        'ignore': False,
        'policies': {
            'reproduce_agents': p_reproduce_agents

        },
        'variables': {
            'agents': s_agent_create,

        }
    },
    {
        'label': 'Feed preys',
        'description': '',
        'ignore': False,
        'policies': {
            'feed_prey': p_feed_prey
        },
        'variables': {
            'agents': s_agent_food,
            'sites': s_site_food
        }
    },
    {
        'label': 'Feed predators',
        'description': '',
        'ignore': False,
        'policies': {
            'hunt_prey': p_hunt_prey
        },
        'variables': {
            'agents': s_agent_food
        }
    },
    {
        'label': 'Natural agent death',
        'description': '',
        'ignore': False,
        'policies': {
            'natural_death': p_natural_death
        },
        'variables': {
            'agents': s_agent_remove
        }
    }
]

partial_state_update_block = [block for block in partial_state_update_block
                              if block.get('ignore', False) is False]
