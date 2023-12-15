# %% [markdown]
#  # cadCAD Easy Run for the Minimal Prey & Predator model

# %%
import plotly.express as px
import numpy as np
import sys
import seaborn as sns
from tqdm.auto import tqdm

import sys
sys.path.append("/Users/danlessa/repos/cadcad-org/cadCAD/")
# %% [markdown]
#  ## Minimal Prey and Predator Model

# %%
TIMESTEPS = 100
SAMPLES = 10

initial_conditions = {
    'prey_population': 100,
    'predator_population': 15
}

params = {
    "prey_birth_rate": [1.0],
    "predator_birth_rate": [0.01],
    "predator_death_const": [1.0],
    "prey_death_const": [0.03],
    # Precision of the simulation. Lower is more accurate / slower
    "dt": [0.01, 0.1, 0.05]
}


def p_predator_births(params, step, sL, s):
    dt = params['dt']
    predator_population = s['predator_population']
    prey_population = s['prey_population']
    birth_fraction = params['predator_birth_rate'] + \
        np.random.random() * 0.0002
    births = birth_fraction * prey_population * predator_population * dt
    return {'add_to_predator_population': births}


def p_prey_births(params, step, sL, s):
    dt = params['dt']
    population = s['prey_population']
    birth_fraction = params['prey_birth_rate'] + np.random.random() * 0.1
    births = birth_fraction * population * dt
    return {'add_to_prey_population': births}


def p_predator_deaths(params, step, sL, s):
    dt = params['dt']
    population = s['predator_population']
    death_rate = params['predator_death_const'] + np.random.random() * 0.005
    deaths = death_rate * population * dt
    return {'add_to_predator_population': -1.0 * deaths}


def p_prey_deaths(params, step, sL, s):
    dt = params['dt']
    death_rate = params['prey_death_const'] + np.random.random() * 0.1
    prey_population = s['prey_population']
    predator_population = s['predator_population']
    deaths = death_rate * prey_population * predator_population * dt
    return {'add_to_prey_population': -1.0 * deaths}


def s_prey_population(params, step, sL, s, _input):
    y = 'prey_population'
    x = s['prey_population'] + _input['add_to_prey_population']
    return (y, x)


def s_predator_population(params, step, sL, s, _input):
    y = 'predator_population'
    x = s['predator_population'] + _input['add_to_predator_population']
    return (y, x)


partial_state_update_blocks = [
    {
        'label': 'Lotka-Volterra Equations',
        'policies': {
            'predator_births': p_predator_births,
            'prey_births': p_prey_births,
            'predator_deaths': p_predator_deaths,
            'prey_deaths': p_prey_deaths,
        },
        'variables': {
            'prey_population': s_prey_population,
            'predator_population': s_predator_population
        }
    },
    {
        'label': 'Do Nothing',
        'policies': {
            
        },
        'variables': {
            
        }
    }
]


# %%


# %%
from cadCAD.tools import easy_run

df = easy_run(initial_conditions,
              params,
              partial_state_update_blocks,
              TIMESTEPS,
              SAMPLES,
              assign_params=True,
              drop_substeps=False)

# %%
from cadCAD_tools import profile_run

fig = px.line(df.query('dt == 0.1'),
              x=df.prey_population,
              y=df.predator_population,
              color=df.run.astype(str))

fig.show()

# %%
df = profile_run(initial_conditions,
              params,
              partial_state_update_blocks,
              20,
              10,
              use_label=True)

# %%
df.head(8).substep_label

# %%
from cadCAD_tools.profiling.visualizations import visualize_elapsed_time_per_ts

visualize_elapsed_time_per_ts(df, relative=False)

# %%
visualize_elapsed_time_per_ts(df, relative=True)

# %%
from cadCAD_tools.profiling.visualizations import visualize_substep_impact

visualize_substep_impact(df, relative=True)

# %%
visualize_substep_impact(df, relative=False)

# %%



