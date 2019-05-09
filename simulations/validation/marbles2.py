from cadCAD.configuration import append_configs
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

T = 50 #iterations in our simulation
n = 3 #number of boxes in our network
m = 2 #for barabasi graph type number of edges is (n-2)*m

G = nx.barabasi_albert_graph(n, m)
k = len(G.edges)

balls = np.zeros(n,)

for node in G.nodes:
    rv = np.random.randint(1,25)
    G.nodes[node]['initial_balls'] = rv
    balls[node] = rv

scale=100
nx.draw_kamada_kawai(G, node_size=balls*scale,labels=nx.get_node_attributes(G,'initial_balls'))

initial_conditions = {'balls': balls, 'network': G}


def update_balls(params, step, sL, s, _input):
    delta_balls = _input['delta']
    new_balls = s['balls']
    for e in G.edges:
        move_ball = delta_balls[e]
        src = e[0]
        dst = e[1]
        if (new_balls[src] >= move_ball) and (new_balls[dst] >= -move_ball):
            new_balls[src] = new_balls[src] - move_ball
            new_balls[dst] = new_balls[dst] + move_ball

    key = 'balls'
    value = new_balls

    return (key, value)


def update_network(params, step, sL, s, _input):
    new_nodes = _input['nodes']
    new_edges = _input['edges']
    new_balls = _input['quantity']

    graph = s['network']

    for node in new_nodes:
        graph.add_node(node)
        graph.nodes[node]['initial_balls'] = new_balls[node]
        graph.nodes[node]['strat'] = _input['node_strats'][node]

    for edge in new_edges:
        graph.add_edge(edge[0], edge[1])
        graph.edges[edge]['strat'] = _input['edge_strats'][edge]

    key = 'network'
    value = graph
    return (key, value)


def update_network_balls(params, step, sL, s, _input):
    new_nodes = _input['nodes']
    new_balls = _input['quantity']
    balls = np.zeros(len(s['balls']) + len(new_nodes))

    for node in s['network'].nodes:
        balls[node] = s['balls'][node]

    for node in new_nodes:
        balls[node] = new_balls[node]

    key = 'balls'
    value = balls

    return (key, value)


def greedy_robot(src_balls, dst_balls):
    # robot wishes to accumlate balls at its source
    # takes half of its neighbors balls
    if src_balls < dst_balls:
        delta = -np.floor(dst_balls / 2)
    else:
        delta = 0

    return delta


def fair_robot(src_balls, dst_balls):
    # robot follows the simple balancing rule
    delta = np.sign(src_balls - dst_balls)

    return delta


def giving_robot(src_balls, dst_balls):
    # robot wishes to gice away balls one at a time
    if src_balls > 0:
        delta = 1
    else:
        delta = 0

    return delta

robot_strategies = [greedy_robot,fair_robot, giving_robot]

for node in G.nodes:
    nstrats = len(robot_strategies)
    rv  = np.random.randint(0,nstrats)
    G.nodes[node]['strat'] = robot_strategies[rv]

for e in G.edges:
    owner_node = e[0]
    G.edges[e]['strat'] = G.nodes[owner_node]['strat']


def robotic_network(params, step, sL, s):
    graph = s['network']

    delta_balls = {}
    for e in graph.edges:
        src = e[0]
        src_balls = s['balls'][src]
        dst = e[1]
        dst_balls = s['balls'][dst]

        # transfer balls according to specific robot strat
        strat = graph.edges[e]['strat']
        delta_balls[e] = strat(src_balls, dst_balls)

    return_dict = {'nodes': [], 'edges': {}, 'quantity': {}, 'node_strats': {}, 'edge_strats': {}, 'delta': delta_balls}

    return (return_dict)


def agent_arrival(params, step, sL, s):
    node = len(s['network'].nodes)
    edge_list = s['network'].edges

    # choose a m random edges without replacement
    # new = np.random.choose(edgelist,m)
    new = [0, 1]  # tester

    nodes = [node]
    edges = [(node, new_node) for new_node in new]

    initial_balls = {node: np.random.randint(1, 25)}

    rv = np.random.randint(0, nstrats)
    node_strat = {node: robot_strategies[rv]}

    edge_strats = {e: robot_strategies[rv] for e in edges}

    return_dict = {'nodes': nodes,
                   'edges': edges,
                   'quantity': initial_balls,
                   'node_strats': node_strat,
                   'edge_strats': edge_strats,
                   'delta': np.zeros(node + 1)
                   }
    return (return_dict)


partial_state_update_blocks = [
    {
        'policies': {
        # The following policy functions will be evaluated and their returns will be passed to the state update functions
            'p1': robotic_network
        },
        'variables': {  # The following state variables will be updated simultaneously
            'balls': update_balls

        }
    },
    {
        'policies': {
        # The following policy functions will be evaluated and their returns will be passed to the state update functions
            'p1': agent_arrival
        },
        'variables': {  # The following state variables will be updated simultaneously
            'network': update_network,
            'balls': update_network_balls
        }
    }
]

simulation_parameters = {
    'T': range(T),
    'N': 1,
    'M': {}
}
append_configs(
    sim_configs=simulation_parameters, #dict containing state update functions
    initial_state=initial_conditions, #dict containing variable names and initial values
    partial_state_update_blocks= partial_state_update_blocks #, #dict containing state update functions
    # policy_ops=[lambda a, b: {**a, **b}]
)
# config = Configuration(initial_state=initial_conditions, #dict containing variable names and initial values
#                        partial_state_update_blocks=partial_state_update_blocks, #dict containing state update functions
#                        sim_config=simulation_parameters #dict containing simulation parameters
#                       )
