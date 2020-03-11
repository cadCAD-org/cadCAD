from .parts.lotka_volterra import *


partial_state_update_block = [
    {
        'policies': {
            'reproduce_prey': p_reproduce_prey,
            'reproduce_predators': p_reproduce_predators,
            'eliminate_prey': p_eliminate_prey,
            'eliminate_predators': p_eliminate_predators
        },
        'variables': {
            'prey_population': s_prey_population,
            'predator_population': s_predator_population            
        }
    }

]