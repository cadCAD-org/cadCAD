from decimal import Decimal
import numpy as np

from SimCAD import Configuration, configs
from SimCAD.configuration import exo_update_per_ts, bound_norm_random, \
    ep_time_step

# behavior_ops = []
# behavior_ops = [foldr(dict_elemwise_sum())]

seed = {
    'z': np.random.RandomState(1)
    # 'a': np.random.RandomState(2),
    # 'b': np.random.RandomState(3),
    # 'c': np.random.RandomState(3)
}

#Signals
# Pr_signal
#if s['P_Ext_Markets'] != 0:
#Pr_signal = s['Z']/s['P_Ext_Markets']
#else Pr_signal = 0
#    if Pr_signal < s['Z']/s['Buy_Log']:
beta = Decimal('0.25') #agent response gain
beta_LT = Decimal('0.1') #LT agent response gain
alpha = Decimal('0.091') #21 day EMA forgetfullness between 0 and 1, closer to 1 discounts older obs quicker, should be 2/(N+1)
max_withdraw_factor = Decimal('0.9')
external_draw = Decimal('0.01') # between 0 and 1 to draw Buy_Log to external

# Stochastic process factors
correction_factor = Decimal('0.01')
volatility =  Decimal('5.0')


# Buy_Log_signal =
# Z_signal = 
# Price_signal =
# TDR_draw_signal =
# P_Ext_Markets_signal = 

# Behaviors per Mechanism

# BEHAVIOR 1: EMH Trader
EMH_portion = Decimal('0.250')
EMH_Ext_Hold = Decimal('42000.0')

def b1m1(step, sL, s):
    print('b1m1')
 #   y = 'P_Ext_Markets'
    # Psignal_ext = s['P_Ext_Markets'] / s['Z']
    # Psignal_int = s['Buy_Log'] /  s['Z']
    # if Psignal_ext < Psignal_int:
    #     return beta*(Psignal_int - Psignal_ext) * s['Z']  # Deposited amount in TDR
    # else:
    #     return 0 # Decimal(0.000001)
 #   return (y,x)
    theta = (s['Z']*EMH_portion*s['Price'])/(s['Z']*EMH_portion*s['Price'] + EMH_Ext_Hold * s['P_Ext_Markets'])
    if s['Price'] < (theta*EMH_Ext_Hold * s['P_Ext_Markets'])/(s['Z']*EMH_portion*(1-theta)):
        buy = beta * theta*EMH_Ext_Hold * s['P_Ext_Markets']/(s['Price']*EMH_portion*(1-theta))
        return {'buy_order1': buy}
    elif s['Price'] > (theta*EMH_Ext_Hold * s['P_Ext_Markets'])/(s['Z']*EMH_portion*(1-theta)):
        return {'buy_order1': 0}
    else:
        return {'buy_order1': 0}

def b1m2(step, sL, s):
    print('b1m2')
    theta = (s['Z']*EMH_portion*s['Price'])/(s['Z']*EMH_portion*s['Price'] + EMH_Ext_Hold * s['P_Ext_Markets'])
    if s['Price'] < (theta*EMH_Ext_Hold * s['P_Ext_Markets'])/(s['Z']*EMH_portion*(1-theta)):
        return {'sell_order1': 0}
    elif s['Price'] > (theta*EMH_Ext_Hold * s['P_Ext_Markets'])/(s['Z']*EMH_portion*(1-theta)):
        sell = beta * theta*EMH_Ext_Hold * s['P_Ext_Markets']/(s['Price']*EMH_portion*(1-theta))
        return {'sell_order1': sell}
    else:
        return {'sell_order1': 0}

# BEHAVIOR 3: Herding


# BEHAVIOR 4: HODLers
HODL_belief = Decimal('10.0')
HODL_portion = Decimal('0.250')
HODL_Ext_Hold = Decimal('4200.0')

def b4m2(step, sL, s):
    print('b4m2')
    theta = (s['Z']*HODL_portion*s['Price'])/(s['Z']*HODL_portion*s['Price'] + HODL_Ext_Hold * s['P_Ext_Markets'])
    if s['Price'] <  1/HODL_belief*(theta*HODL_Ext_Hold * s['P_Ext_Markets'])/(s['Z']*HODL_portion*(1-theta)):
        sell = beta * theta*HODL_Ext_Hold * s['P_Ext_Markets']/(s['Price']*HODL_portion*(1-theta))
        return {'sell_order2': sell}
    elif s['Price'] > (theta*HODL_Ext_Hold * s['P_Ext_Markets'])/(s['Z']*HODL_portion*(1-theta)):
        return {'sell_order2': 0}
    else:
        return {'sell_order2': 0}


# BEHAVIOR 2: Withdraw TDR and burn Zeus
# Selling Agent- Arbitrage on TDR ext v TDR int signals
# def b2m1(step, sL, s):
#     Psignal_ext = s['P_Ext_Markets'] / s['Z']
#     Psignal_int = s['Buy_Log'] /  s['Z']
#     if Psignal_ext > Psignal_int:
#         # withdrawn amount in TDR, subject to TDR limit
#         return - np.minimum(beta*(Psignal_ext - Psignal_int) * s['Z'],s['Buy_Log']*max_withdraw_factor) 
#     else:
#         return 0 #- Decimal(0.000001)    
   # return 0

# BEHAVIOR 1: Deposit TDR and mint Zeus
# Buying Agent- Arbitrage on Price and Z signals
# def b1m2(step, sL, s):
#     # Psignal_ext = s['P_Ext_Markets'] / s['Z']
#     # Psignal_int = s['Buy_Log'] /  s['Z']
#     # if Psignal_ext > Psignal_int:
#     #     # withdrawn amount in TDR, subject to TDR limit
#     #     return - np.minimum(beta*(Psignal_ext - Psignal_int) * s['Z'],s['Buy_Log']*max_withdraw_factor) 
#     # else:
#     #     return 0 #- Decimal(0.000001) 
#     # 
#     #   LT more valuable than ST = deposit TDR and mint Z
#     Psignal_LT =  s['Price'] / s['Z']
#     if Psignal_LT > 1:
#         return beta_LT*(Psignal_LT - 1) * s['Z']
#     else:
#         return 0

# Behavior will go here- b2m2, putting in mech 3: b1m3 for debugging
# def b2m2(step, sL, s):
#     # Psignal_LT =  s['Price'] / s['Z']
#     # if Psignal_LT > 1:
#     test = np.arange(1,10)
#     return test

# Selling Agent- Arbitrage on Price and Z signals
# def b1m3(step, sL, s):
#     Psignal_LT =  s['Price'] / s['Z']
#     if Psignal_LT < 1:
#         return - np.minimum(beta_LT*(Psignal_LT - 1) * s['Z'], s['Z']*max_withdraw_factor)
#     else:
#         return 0


# def b2m3(step, sL, s):
#     return 0

# Internal States per Mechanism
# Deposit TDR/Mint Zeus
# def s1m1(step, sL, s, _input):
#     s['Z'] = s['Z'] + _input


# STATES

# ZEUS Fixed Supply
def s1m1(step, sL, s, _input):
    y = 'Z'
    x =  s['Z'] #+  _input # / Psignal_int
    return (y, x)

def s2m1(step, sL, s, _input):
    y = 'Price'
    x = (s['P_Ext_Markets'] - _input['buy_order1']) /s['Z'] *10000
    #x= alpha * s['Z'] + (1 - alpha)*s['Price']
    return (y, x)

def s3m1(step, sL, s, _input):
    y = 'Buy_Log'
    x =   _input['buy_order1'] # / Psignal_int
    return (y, x)

def s4m2(step, sL, s, _input):
    y = 'Sell_Log'
    x = _input['sell_order1'] + _input['sell_order2'] # / Psignal_int
    return (y, x)

def s3m3(step, sL, s, _input):
    y = 'Buy_Log'
    x = s['Buy_Log'] +  _input # / Psignal_int
    return (y, x)

# Price Update
def s2m3(step, sL, s, _input):

    y = 'Price'
    #var1 = Decimal.from_float(s['Buy_Log'])
    x = s['Price'] + s['Buy_Log'] * 1/s['Z'] - s['Sell_Log']/s['Z'] 
     #+ np.divide(s['Buy_Log'],s['Z']) - np.divide() # / Psignal_int
    return (y, x)



def s6m1(step, sL, s, _input):
    y = 'P_Ext_Markets'
    x = s['P_Ext_Markets'] - _input
    #x= alpha * s['Z'] + (1 - alpha)*s['Price']
    return (y, x)

def s2m2(step, sL, s, _input):
    y = 'Price'
    x = (s['P_Ext_Markets'] - _input) /s['Z'] *10000
    #x= alpha * s['Z'] + (1 - alpha)*s['Price']
    return (y, x)

# def s1m1(step, sL, s, _input):
#     Psignal_int = s['Buy_Log'] /  s['Z']
#     y = 'Z'
#     x =  s['Z'] +  _input / Psignal_int
#     return (y, x)

# def s2m1(step, sL, s, _input):
#     y = 'Price'
#     x= alpha * s['Z'] + (1 - alpha)*s['Price']
#     return (y, x)

# def s3m1(step, sL, s, _input):
#     y = 'Buy_Log'
#     x = s['Buy_Log'] + _input # Input already in TDR * s['Z']
#     return (y, x)

# #  Withdraw TDR/Burn Zeus
# def s1m2(step, sL, s, _input):
#     Psignal_int = s['Buy_Log'] /  s['Z']
#     y = 'Z'
#     x =  s['Z'] #+  _input / Psignal_int
#     return (y, x)

# def s2m2(step, sL, s, _input):
#     y = 'Price'
#     x= alpha * s['Z'] + (1 - alpha)*s['Price']
#     return (y, x)

# def s3m2(step, sL, s, _input):
#     y = 'Buy_Log'
#     x = s['Buy_Log'] + _input #* s['Z']
#     # y = 'Buy_Log'
#     # x = s['Buy_Log'] + _input
#     return (y, x)

# def s1m3(step, sL, s, _input):
#     Psignal_int = s['Buy_Log'] /  s['Z']
#     y = 'Z'
#     x =  s['Z'] #+  _input / Psignal_int
#     return (y, x)

# def s2m3(step, sL, s, _input):
#     y = 'Price'
#     x= alpha * s['Z'] + (1 - alpha)*s['Price']
#     return (y, x)

# def s3m3(step, sL, s, _input):
#     y = 'Buy_Log'
#     x = s['Buy_Log'] #+ _input #* s['Z']
#     # y = 'Buy_Log'
#     # x = s['Buy_Log'] + _input
#     return (y, x)

# def s3m4(step, sL, s, _input):
#     y = 'Buy_Log'
#     x = s['Buy_Log']*(1-external_draw) + s['Sell_Log']*external_draw # _input #* s['Z']
#     # y = 'Buy_Log'
#     # x = s['Buy_Log'] + _input
#     return (y, x)

# def s1m3(step, sL, s, _input):
#     s['Z'] = s['Z'] + _input
# def s2m3(step, sL, s, _input):
#     s['Price'] = s['Price'] + _input

# Exogenous States
proc_one_coef_A = -125
proc_one_coef_B = 125
# def es3p1(step, sL, s, _input):
#     s['s3'] = s['s3'] * bound_norm_random(seed['a'], proc_one_coef_A, proc_one_coef_B)
# def es4p2(step, sL, s, _input):
#     s['P_Ext_Markets'] = s['P_Ext_Markets'] * bound_norm_random(seed['b'], proc_one_coef_A, proc_one_coef_B) 
# def es5p2(step, sL, s, _input): # accept timedelta instead of timedelta params
#     s['timestamp'] = ep_time_step(s, s['timestamp'], seconds=1)
def es3p1(step, sL, s, _input):
    y = 's3'
    x = s['s3'] + 1
    return (y, x)
# def es4p2(step, sL, s, _input):
#     y = 'P_Ext_Markets'
#     # bound_norm_random defined in utils.py

#     #x  = s['P_Ext_Markets'] * bound_norm_random(seed['b'], proc_one_coef_A, proc_one_coef_B)
#     expected_change = correction_factor*(s['P_Ext_Markets']-s['Buy_Log'])
#     vol =  np.random.randint(1,volatility)
#     change = expected_change * vol
#     # change_float =  (np.random.normal(expected_change,volatility*expected_change) #Decimal('1.0')
#     #change = Decimal.from_float(change_float)
#     x = s['P_Ext_Markets'] + change 
   
#     return (y, x)

# A change in belief of actual price, passed onto behaviors to make action
def es4p2(step, sL, s, _input):
    y = 'P_Ext_Markets'
    x = s['P_Ext_Markets'] +  bound_norm_random(seed['z'], proc_one_coef_A, proc_one_coef_B)

    return (y,x)


def es5p2(step, sL, s, _input): # accept timedelta instead of timedelta params
    y = 'timestamp'
    x = ep_time_step(s, s['timestamp'], seconds=1)
    return (y, x)
#Environment States
# def stochastic(reference, seed, correction = 0.01):
#     series = np.zeros(len(reference))
#     series[0] = reference[0]
#     for i in range(1,len(reference)):
#         expected_change = correction*(reference[i]-series[i-1])
#         normalized_expected_change = np.abs(expected_change)*(reference[i])/(reference[i-1])
#         seed_int = seed.randint(1,10)
#         change = np.random.normal(expected_change,seed_int*normalized_expected_change)
                
#         series[i] = series[i-1]+change
#         # avoid negative series returns
#         if series[i] <= 0:
#             series[i] = .01
#         #series[i] = series[i-1]+change 
        
#     return [series,seed_int]
# ref3 = np.arange(1,1000)*.1
# test = stochastic(ref3,seed['b']) 

# def env_a(ref3,seed['b']):
#     return stochastic(ref3,seed['b'])
def env_a(x):
    return 100
def env_b(x):
    return 21000000
# def what_ever(x):
#     return x + 1

# Genesis States
state_dict = {
    'Z': Decimal(21000000.0),
    'Price': Decimal(100.0),   # Initialize = Z for EMA
    'Buy_Log': Decimal(0.0),
    'Sell_Log': Decimal(0.0),
    'Trans': Decimal(0.0),
    'P_Ext_Markets': Decimal(25000.0),
   
   # 's2': Decimal(0.0),
   # 's3': Decimal(0.0),
  #  's4': Decimal(0.0),
    'timestamp': '2018-10-01 15:16:24'
}

# exogenous_states = {
# #    "s3": es3p1,
#     "P_Ext_Markets": es4p2,
#     "timestamp": es5p2
# }

exogenous_states = exo_update_per_ts(
    {
 #   "s3": es3p1,
    "P_Ext_Markets": es4p2,
    "timestamp": es5p2
    }
)

env_processes = {
 #   "s3": env_proc('2018-10-01 15:16:25', env_a),
#    "P_Ext_Markets": env_proc('2018-10-01 15:16:25', env_b)
}

# test return vs. non-return functions as lambdas
# test fully defined functions
mechanisms = {
    "m1": {
        "behaviors": {
            "b1": b1m1, # lambda step, sL, s: s['s1'] + 1,
#            "b2": b2m1
        },
        "states": {
            "Z": s1m1,
#            "Price": s2_dummy,
            "Buy_Log": s3m1,
        }
    },
    "m2": {
         "behaviors": {
            "b1": b1m2,
            "b4": b4m2
         },
         "states": {
             "Sell_Log":s4m2,
        }
    },
        "m3": {
            "behaviors": {
        },
            "states": {
                "Price": s2m3,
        }
    },
#     "m3": {
#         "behaviors": {
#             "b1": b1m3,
#             "b2": b2m3
#         },
#         "states": {
#             "Z": s1m3,
#             "Price": s2m3,
#             "Buy_Log": s3m3,
#         }
#     },
#     "m4": {
#         "behaviors": {
#         },
#         "states": {
#         }
#    },
    # "m3": {
    #     "behaviors": {
    #         "b1": b1m3,
    #         "b2": b2m3
    #     },
    #     "states": {
    #         "Z": s1m3,
    #         "Price": s2m3,
    #     }
    # }
     #treat environmental processes as a mechanism
    "ep": {
        "behaviors": {
        },
        "states": {
            "P_Ext_Markets":  es4p2
        }
    }
}

sim_config = {
    "N": 1,
    "T": range(1000)
}

configs.append(Configuration(sim_config, state_dict, seed, exogenous_states, env_processes, mechanisms))