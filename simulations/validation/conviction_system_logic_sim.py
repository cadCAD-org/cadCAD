from pprint import pprint

import numpy as np
from tabulate import tabulate

from cadCAD.configuration.utils import config_sim
from simulations.validation.conviction_helpers import *
#import networkx as nx
from scipy.stats import expon, gamma


#functions for partial state update block 1

#Driving processes: arrival of participants, proposals and funds
##-----------------------------------------


def gen_new_participant(network, new_participant_holdings):
    
    i = len([node for node in network.nodes])
    
    network.add_node(i)
    network.nodes[i]['type']="participant"
    
    s_rv = np.random.rand() 
    network.nodes[i]['sentiment'] = s_rv
    network.nodes[i]['holdings']=new_participant_holdings
    
    for j in get_nodes_by_type(network, 'proposal'):
        network.add_edge(i, j)
        
        rv = np.random.rand()
        a_rv = 1-4*(1-rv)*rv #polarized distribution
        network.edges[(i, j)]['affinity'] = a_rv
        network.edges[(i,j)]['tokens'] = a_rv*network.nodes[i]['holdings']
        network.edges[(i, j)]['conviction'] = 0
    
    return network
    

scale_factor = 1000

def gen_new_proposal(network, funds, supply, trigger_func):
    j = len([node for node in network.nodes])
    network.add_node(j)
    network.nodes[j]['type']="proposal"
    
    network.nodes[j]['conviction']=0
    network.nodes[j]['status']='candidate'
    network.nodes[j]['age']=0
    
    rescale = scale_factor*funds
    r_rv = gamma.rvs(3,loc=0.001, scale=rescale)
    network.node[j]['funds_requested'] = r_rv
    
    network.nodes[j]['trigger']= trigger_func(r_rv, funds, supply)
    
    participants = get_nodes_by_type(network, 'participant')
    proposing_participant = np.random.choice(participants)
    
    for i in participants:
        network.add_edge(i, j)
        if i==proposing_participant:
            network.edges[(i, j)]['affinity']=1
        else:
            rv = np.random.rand()
            a_rv = 1-4*(1-rv)*rv #polarized distribution
            network.edges[(i, j)]['affinity'] = a_rv
            
        network.edges[(i, j)]['conviction'] = 0
        network.edges[(i,j)]['tokens'] = 0
    return network
        
        

def driving_process(params, step, sL, s):
    
    #placeholder plumbing for random processes
    arrival_rate = 10/s['sentiment']
    rv1 = np.random.rand()
    new_participant = bool(rv1<1/arrival_rate)
    if new_participant:
        h_rv = expon.rvs(loc=0.0, scale=1000)
        new_participant_holdings = h_rv
    else:
        new_participant_holdings = 0
    
    network = s['network']
    affinities = [network.edges[e]['affinity'] for e in network.edges ]
    median_affinity = np.median(affinities)
    
    proposals = get_nodes_by_type(network, 'proposal')
    fund_requests = [network.nodes[j]['funds_requested'] for j in proposals if network.nodes[j]['status']=='candidate' ]
    
    funds = s['funds']
    total_funds_requested = np.sum(fund_requests)
    
    proposal_rate = 10/median_affinity * total_funds_requested/funds
    rv2 = np.random.rand()
    new_proposal = bool(rv2<1/proposal_rate)
    
    sentiment = s['sentiment']
    funds = s['funds']
    scale_factor = 1+4000*sentiment**2
    
    #this shouldn't happen but expon is throwing domain errors
    if scale_factor > 1: 
        funds_arrival = expon.rvs(loc = 0, scale = scale_factor )
    else:
        funds_arrival = 0
    
    return({'new_participant':new_participant,
            'new_participant_holdings':new_participant_holdings,
            'new_proposal':new_proposal, 
            'funds_arrival':funds_arrival})

    
#Mechanisms for updating the state based on driving processes
##---
def update_network(params, step, sL, s, _input):

    network = s['network']
    funds = s['funds']
    supply = s['supply']
    trigger_func = params['trigger_func']

    new_participant = _input['new_participant'] #T/F
    new_proposal = _input['new_proposal'] #T/F

    if new_participant:
        new_participant_holdings = _input['new_participant_holdings']
        network = gen_new_participant(network, new_participant_holdings)
    
    if new_proposal:
        network= gen_new_proposal(network,funds,supply,trigger_func )
    
    #update age of the existing proposals
    proposals = get_nodes_by_type(network, 'proposal')
    
    for j in proposals:
        network.nodes[j]['age'] =  network.nodes[j]['age']+1
        if network.nodes[j]['status'] == 'candidate':
            requested = network.nodes[j]['funds_requested']
            network.nodes[j]['trigger'] = trigger_func(requested, funds, supply)
        else:
            network.nodes[j]['trigger'] = np.nan
            
    key = 'network'
    value = network
    
    return (key, value)

def increment_funds(params, step, sL, s, _input):
    
    funds = s['funds']
    funds_arrival = _input['funds_arrival']

    #increment funds
    funds = funds + funds_arrival
    
    key = 'funds'
    value = funds
    
    return (key, value)

def increment_supply(params, step, sL, s, _input):
    
    supply = s['supply']
    supply_arrival = _input['new_participant_holdings']

    #increment funds
    supply = supply + supply_arrival
    
    key = 'supply'
    value = supply
    
    return (key, value)

#functions for partial state update block 2

#Driving processes: completion of previously funded proposals
##-----------------------------------------

def check_progress(params, step, sL, s):
    
    network = s['network']
    proposals = get_nodes_by_type(network, 'proposal')
    
    completed = []
    for j in proposals:
        if network.nodes[j]['status'] == 'active':
            grant_size = network.nodes[j]['funds_requested']
            base_completion_rate=params['base_completion_rate']
            likelihood = 1.0/(base_completion_rate+np.log(grant_size))
            if np.random.rand() < likelihood:
                completed.append(j)
    
    return({'completed':completed})


#Mechanisms for updating the state based on check progress
##---
def complete_proposal(params, step, sL, s, _input):
    
    network = s['network']
    participants = get_nodes_by_type(network, 'participant')
    
    completed = _input['completed']
    for j in completed:
        network.nodes[j]['status']='completed'
        for i in participants:
            force = network.edges[(i,j)]['affinity']
            sentiment = network.node[i]['sentiment']
            network.node[i]['sentiment'] = get_sentimental(sentiment, force, decay=0)
    
    key = 'network'
    value = network
    
    return (key, value)

def update_sentiment_on_completion(params, step, sL, s, _input):
    
    network = s['network']
    proposals = get_nodes_by_type(network, 'proposal')
    completed = _input['completed']
    
    grants_outstanding = np.sum([network.nodes[j]['funds_requested'] for j in proposals if network.nodes[j]['status']=='active'])
    
    grants_completed = np.sum([network.nodes[j]['funds_requested'] for j in completed])
    
    sentiment = s['sentiment']
    
    force = grants_completed/grants_outstanding
    mu = params['sentiment_decay']
    if (force >=0) and (force <=1):
        sentiment = get_sentimental(sentiment, force, mu)
    else:
        sentiment = get_sentimental(sentiment, 0, mu)
    
    
    key = 'sentiment'
    value = sentiment
    
    return (key, value)

def get_sentimental(sentiment, force, decay=0):
    mu = decay
    sentiment = sentiment*(1-mu) + force
    
    if sentiment > 1:
        sentiment = 1
        
    return sentiment

#functions for partial state update block 3

#Decision processes: trigger function policy
##-----------------------------------------

def trigger_function(params, step, sL, s):
    
    network = s['network']
    funds = s['funds']
    supply = s['supply']
    proposals = get_nodes_by_type(network, 'proposal')
    tmin = params['tmin']
    
    accepted = []
    triggers = {}
    for j in proposals:
        if network.nodes[j]['status'] == 'candidate':
            requested = network.nodes[j]['funds_requested']
            age = network.nodes[j]['age']
            threshold = trigger_threshold(requested, funds, supply)
            if age > tmin:
                conviction = network.nodes[j]['conviction']
                if conviction >threshold:
                    accepted.append(j)
        else:
            threshold = np.nan
            
        triggers[j] = threshold
                
        
                    
    return({'accepted':accepted, 'triggers':triggers})

def decrement_funds(params, step, sL, s, _input):
    
    funds = s['funds']
    network = s['network']
    accepted = _input['accepted']

    #decrement funds
    for j in accepted:
        funds = funds - network.nodes[j]['funds_requested']
    
    key = 'funds'
    value = funds
    
    return (key, value)

def update_proposals(params, step, sL, s, _input):
    
    network = s['network']
    accepted = _input['accepted']
    triggers = _input['triggers']
    participants = get_nodes_by_type(network, 'participant')
    proposals = get_nodes_by_type(network, 'proposals')
    sensitivity = params['sensitivity']
    
    for j in proposals:
        network.nodes[j]['trigger'] = triggers[j]
    
    #bookkeeping conviction and participant sentiment
    for j in accepted:
        network.nodes[j]['status']='active'
        network.nodes[j]['conviction']=np.nan
        #change status to active
        for i in participants:
        
            #operating on edge = (i,j)
            #reset tokens assigned to other candidates
            network.edges[(i,j)]['tokens']=0
            network.edges[(i,j)]['conviction'] = np.nan
            
            #update participants sentiments (positive or negative) 
            affinities = [network.edges[(i,p)]['affinity'] for p in proposals if not(p in accepted)]
            if len(affinities)>1:
                max_affinity = np.max(affinities)
                force = network.edges[(i,j)]['affinity']-sensitivity*max_affinity
            else:
                force = 0
            
            #based on what their affinities to the accepted proposals
            network.nodes[i]['sentiment'] = get_sentimental(network.nodes[i]['sentiment'], force, False)
            
    
    key = 'network'
    value = network
    
    return (key, value)

def update_sentiment_on_release(params, step, sL, s, _input):
    
    network = s['network']
    proposals = get_nodes_by_type(network, 'proposal')
    accepted = _input['accepted']
    
    proposals_outstanding = np.sum([network.nodes[j]['funds_requested'] for j in proposals if network.nodes[j]['status']=='candidate'])
    
    proposals_accepted = np.sum([network.nodes[j]['funds_requested'] for j in accepted])
    
    sentiment = s['sentiment']
    force = proposals_accepted/proposals_outstanding
    if (force >=0) and (force <=1):
        sentiment = get_sentimental(sentiment, force, False)
    else:
        sentiment = get_sentimental(sentiment, 0, False)
    
    key = 'sentiment'
    value = sentiment
    
    return (key, value)

def participants_decisions(params, step, sL, s):
    network = s['network']
    participants = get_nodes_by_type(network, 'participant')
    proposals = get_nodes_by_type(network, 'proposal')
    candidates = [j for j in proposals if network.nodes[j]['status']=='candidate']
    sensitivity = params['sensitivity']
    
    gain = .01
    delta_holdings={}
    proposals_supported ={}
    for i in participants:
        force = network.nodes[i]['sentiment']-sensitivity
        delta_holdings[i] = network.nodes[i]['holdings']*gain*force
        
        support = []
        for j in candidates:
            affinity = network.edges[(i, j)]['affinity']
            cutoff = sensitivity*np.max([network.edges[(i,p)]['affinity'] for p in candidates])
            if cutoff <.5:
                cutoff = .5
            
            if affinity > cutoff:
                support.append(j)
        
        proposals_supported[i] = support
    
    return({'delta_holdings':delta_holdings, 'proposals_supported':proposals_supported})

def update_tokens(params, step, sL, s, _input):
    
    network = s['network']
    delta_holdings = _input['delta_holdings']
    proposals = get_nodes_by_type(network, 'proposal')
    proposals_supported = _input['proposals_supported']
    participants = get_nodes_by_type(network, 'participant')
    alpha = params['alpha']
    
    for i in participants:
        network.nodes[i]['holdings'] = network.nodes[i]['holdings']+delta_holdings[i]
        supported = proposals_supported[i]
        total_affinity = np.sum([ network.edges[(i, j)]['affinity'] for j in supported])
        for j in proposals:
            if j in supported:
                normalized_affinity = network.edges[(i, j)]['affinity']/total_affinity
                network.edges[(i, j)]['tokens'] = normalized_affinity*network.nodes[i]['holdings']
            else:
                network.edges[(i, j)]['tokens'] = 0
            
            prior_conviction = network.edges[(i, j)]['conviction']
            current_tokens = network.edges[(i, j)]['tokens']
            network.edges[(i, j)]['conviction'] =current_tokens+alpha*prior_conviction
    
    for j in proposals:
        network.nodes[j]['conviction'] = np.sum([ network.edges[(i, j)]['conviction'] for i in participants])
    
    key = 'network'
    value = network
    
    return (key, value)

def update_supply(params, step, sL, s, _input):
    
    supply = s['supply']
    delta_holdings = _input['delta_holdings']
    delta_supply = np.sum([v for v in delta_holdings.values()])
    
    supply = supply + delta_supply
    
    key = 'supply'
    value = supply
    
    return (key, value)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The Partial State Update Blocks
partial_state_update_blocks = [
    {
        'policies': {
            #new proposals or new participants
            'random': driving_process
        },
        'variables': {
            'network': update_network,
            'funds':increment_funds,
            'supply':increment_supply
        }
    },
    {
      'policies': {
          'completion': check_progress #see if any of the funded proposals completes
        },
        'variables': { # The following state variables will be updated simultaneously
            'sentiment': update_sentiment_on_completion, #note completing decays sentiment, completing bumps it
            'network': complete_proposal #book-keeping
        }
    },
        {
      'policies': {
          'release': trigger_function #check each proposal to see if it passes
        },
        'variables': { # The following state variables will be updated simultaneously
            'funds': decrement_funds, #funds expended
            'sentiment': update_sentiment_on_release, #releasing funds can bump sentiment
            'network': update_proposals #reset convictions, and participants sentiments
                                        #update based on affinities
        }
    },
    {
        'policies': {
            'participants_act': participants_decisions, #high sentiment, high affinity =>buy
                                                        #low sentiment, low affinities => burn
                                                        #assign tokens to top affinities
        },
        'variables': {
            'supply': update_supply,
            'network': update_tokens #update everyones holdings
                                    #and their conviction for each proposal
        }
    }
]

n= 25 #initial participants
m= 3 #initial proposals

initial_sentiment = .5

network, initial_funds, initial_supply, total_requested = initialize_network(n,m,total_funds_given_total_supply,trigger_threshold)

initial_conditions = {'network':network,
                      'supply': initial_supply,
                      'funds':initial_funds,
                      'sentiment': initial_sentiment}

#power of 1 token forever
# conviction_capactity = [2]
# alpha = [1-1/cc for cc in conviction_capactity]
# print(alpha)

params={
    'sensitivity': [.75],
    'tmin': [7], #unit days; minimum periods passed before a proposal can pass
    'sentiment_decay': [.001], #termed mu in the state update function
    'alpha': [0.5],
    'base_completion_rate': [10],
    'trigger_func': [trigger_threshold]
}


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Settings of general simulation parameters, unrelated to the system itself
# `T` is a range with the number of discrete units of time the simulation will run for;
# `N` is the number of times the simulation will be run (Monte Carlo runs)
time_periods_per_run = 250
monte_carlo_runs = 1

simulation_parameters = config_sim({
    'T': range(time_periods_per_run),
    'N': monte_carlo_runs,
    'M': params
})


from cadCAD.configuration import append_configs

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The configurations above are then packaged into a `Configuration` object
append_configs(
    initial_state=initial_conditions, #dict containing variable names and initial values
    partial_state_update_blocks=partial_state_update_blocks, #dict containing state update functions
    sim_configs=simulation_parameters #dict containing simulation parameters
)

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD import configs
import pandas as pd

exec_mode = ExecutionMode()
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run = Executor(exec_context=multi_proc_ctx, configs=configs)

i = 0
for raw_result, tensor_field in run.execute():
    result = pd.DataFrame(raw_result)
    print()
    print(f"Tensor Field: {type(tensor_field)}")
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print(f"Output: {type(result)}")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
    i += 1
