import networkx as nx
from scipy.stats import expon, gamma
import numpy as np
import matplotlib.pyplot as plt

#helper functions
def get_nodes_by_type(g, node_type_selection):
    return [node for node in g.nodes if g.nodes[node]['type']== node_type_selection ]

def get_edges_by_type(g, edge_type_selection):
    return [edge for edge in g.edges if g.edges[edge]['type']== edge_type_selection ]

def total_funds_given_total_supply(total_supply):
    
    #can put any bonding curve invariant here for initializatio!
    total_funds = total_supply
    
    return total_funds

#maximum share of funds a proposal can take
default_beta = .2 #later we should set this to be param so we can sweep it
# tuning param for the trigger function
default_rho = .001

def trigger_threshold(requested, funds, supply, beta = default_beta, rho = default_rho):
    
    share = requested/funds
    if share < beta:
        return rho*supply/(beta-share)**2
    else: 
        return np.inf

def initialize_network(n,m, funds_func=total_funds_given_total_supply, trigger_func =trigger_threshold ):
    network = nx.DiGraph()
    for i in range(n):
        network.add_node(i)
        network.nodes[i]['type']="participant"
        
        h_rv = expon.rvs(loc=0.0, scale=1000)
        network.nodes[i]['holdings'] = h_rv
        
        s_rv = np.random.rand() 
        network.nodes[i]['sentiment'] = s_rv
    
    participants = get_nodes_by_type(network, 'participant')
    initial_supply = np.sum([ network.nodes[i]['holdings'] for i in participants])
    
    initial_funds = funds_func(initial_supply)    
    
    #generate initial proposals
    for ind in range(m):
        j = n+ind
        network.add_node(j)
        network.nodes[j]['type']="proposal"
        network.nodes[j]['conviction']=0
        network.nodes[j]['status']='candidate'
        network.nodes[j]['age']=0
        
        r_rv = gamma.rvs(3,loc=0.001, scale=10000)
        network.node[j]['funds_requested'] = r_rv
        
        network.nodes[j]['trigger']= trigger_threshold(r_rv, initial_funds, initial_supply)
        
        for i in range(n):
            network.add_edge(i, j)
            
            rv = np.random.rand()
            a_rv = 1-4*(1-rv)*rv #polarized distribution
            network.edges[(i, j)]['affinity'] = a_rv
            network.edges[(i,j)]['tokens'] = 0
            network.edges[(i, j)]['conviction'] = 0
            
        proposals = get_nodes_by_type(network, 'proposal')
        total_requested = np.sum([ network.nodes[i]['funds_requested'] for i in proposals])
        
    return network, initial_funds, initial_supply, total_requested

def trigger_sweep(field, trigger_func,xmax=.2,default_alpha=.5):
    
    if field == 'token_supply':
        alpha = default_alpha
        share_of_funds = np.arange(.001,xmax,.001)
        total_supply = np.arange(0,10**9, 10**6) 
        demo_data_XY = np.outer(share_of_funds,total_supply)

        demo_data_Z0=np.empty(demo_data_XY.shape)
        demo_data_Z1=np.empty(demo_data_XY.shape)
        demo_data_Z2=np.empty(demo_data_XY.shape)
        demo_data_Z3=np.empty(demo_data_XY.shape)
        for sof_ind in range(len(share_of_funds)):
            sof = share_of_funds[sof_ind]
            for ts_ind in range(len(total_supply)):
                ts = total_supply[ts_ind]
                tc = ts /(1-alpha)
                trigger = trigger_func(sof, 1, ts)
                demo_data_Z0[sof_ind,ts_ind] = np.log10(trigger)
                demo_data_Z1[sof_ind,ts_ind] = trigger
                demo_data_Z2[sof_ind,ts_ind] = trigger/tc #share of maximum possible conviction
                demo_data_Z3[sof_ind,ts_ind] = np.log10(trigger/tc)
        return {'log10_trigger':demo_data_Z0,
                'trigger':demo_data_Z1,
                'share_of_max_conv': demo_data_Z2,
                'log10_share_of_max_conv':demo_data_Z3,
                'total_supply':total_supply,
                'share_of_funds':share_of_funds}
    elif field == 'alpha':
        alpha = np.arange(.5,1,.01)
        share_of_funds = np.arange(.001,xmax,.001)
        total_supply = 10**9
        demo_data_XY = np.outer(share_of_funds,alpha)

        demo_data_Z4=np.empty(demo_data_XY.shape)
        demo_data_Z5=np.empty(demo_data_XY.shape)
        demo_data_Z6=np.empty(demo_data_XY.shape)
        demo_data_Z7=np.empty(demo_data_XY.shape)
        for sof_ind in range(len(share_of_funds)):
            sof = share_of_funds[sof_ind]
            for a_ind in range(len(alpha)):
                ts = total_supply
                a = alpha[a_ind]
                tc = ts /(1-a)
                trigger = trigger_func(sof, 1, ts)
                demo_data_Z4[sof_ind,a_ind] = np.log10(trigger)
                demo_data_Z5[sof_ind,a_ind] = trigger
                demo_data_Z6[sof_ind,a_ind] = trigger/tc #share of maximum possible conviction
                demo_data_Z7[sof_ind,a_ind] = np.log10(trigger/tc)
        
        return {'log10_trigger':demo_data_Z4,
               'trigger':demo_data_Z5,
               'share_of_max_conv': demo_data_Z6,
               'log10_share_of_max_conv':demo_data_Z7,
               'alpha':alpha,
               'share_of_funds':share_of_funds}
        
    else:
        return "invalid field"
    
def trigger_plotter(share_of_funds,Z, color_label,y, ylabel,cmap='jet'):
    dims = (10, 5)
    fig, ax = plt.subplots(figsize=dims)

    cf = plt.contourf(share_of_funds, y, Z.T, 100, cmap=cmap)
    cbar=plt.colorbar(cf)
    plt.axis([share_of_funds[0], share_of_funds[-1], y[0], y[-1]])
    #ax.set_xscale('log')
    plt.ylabel(ylabel)
    plt.xlabel('Share of Funds Requested')
    plt.title('Trigger Function Map')

    cbar.ax.set_ylabel(color_label)