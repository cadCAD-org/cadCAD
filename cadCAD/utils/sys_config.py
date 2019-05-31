from funcy import curry

from cadCAD.configuration.utils import ep_time_step, time_step

def increment(y, incr_by):
    return lambda _g, step, sL, s, _input: (y, s[y] + incr_by)

def track(y):
    return lambda _g, step, sL, s, _input: (y, s[y].x)

def simple_state_update(y, x):
    return lambda _g, step, sH, s, _input: (y, x)

def simple_policy_update(y):
    return lambda _g, step, sH, s: y

def update_timestamp(y, timedelta, format):
    return lambda _g, step, sL, s, _input: (
        y,
        ep_time_step(s, dt_str=s[y], fromat_str=format, _timedelta=timedelta)
    )

def apply(f, y: str, incr_by: int):
    return lambda _g, step, sL, s, _input: (y, curry(f)(s[y])(incr_by))

def add(y: str, incr_by):
    return apply(lambda a, b: a + b, y, incr_by)

def increment_state_by_int(y: str, incr_by: int):
    return lambda _g, step, sL, s, _input: (y, s[y] + incr_by)

def s(y, x):
    return lambda _g, step, sH, s, _input: (y, x)

def time_model(y, substeps, time_delta, ts_format='%Y-%m-%d %H:%M:%S'):
    def apply_incriment_condition(s):
        if s['substep'] == 0 or s['substep'] == substeps:
            return y, time_step(dt_str=s[y], dt_format=ts_format, _timedelta=time_delta)
        else:
            return y, s[y]
    return lambda _g, step, sL, s, _input: apply_incriment_condition(s)


# ToDo: Impliment Matrix reduction
#
# [
#     {'conditions': [123], 'opp': lambda a, b: a and b},
#     {'conditions': [123], 'opp': lambda a, b: a and b}
# ]

# def trigger_condition2(s, conditions, cond_opp):
#     # print(conditions)
#     condition_bools = [s[field] in precondition_values for field, precondition_values in conditions.items()]
#     return reduce(cond_opp, condition_bools)
#
# def trigger_multi_conditions(s, multi_conditions, multi_cond_opp):
#     # print([(d['conditions'], d['reduction_opp']) for d in multi_conditions])
#     condition_bools = [
#         trigger_condition2(s, conditions, opp) for conditions, opp in [
#             (d['conditions'], d['reduction_opp']) for d in multi_conditions
#         ]
#     ]
#     return reduce(multi_cond_opp, condition_bools)
#
# def apply_state_condition2(multi_conditions, multi_cond_opp, y, f, _g, step, sL, s, _input):
#     if trigger_multi_conditions(s, multi_conditions, multi_cond_opp):
#         return f(_g, step, sL, s, _input)
#     else:
#         return y, s[y]
#
# def proc_trigger2(y, f, multi_conditions, multi_cond_opp):
#     return lambda _g, step, sL, s, _input: apply_state_condition2(multi_conditions, multi_cond_opp, y, f, _g, step, sL, s, _input)
#
# def timestep_trigger2(end_substep, y, f):
#     multi_conditions = [
#         {
#             'condition': {
#                 'substep': [0, end_substep]
#             },
#             'reduction_opp': lambda a, b: a and b
#         }
#     ]
#     multi_cond_opp = lambda a, b: a and b
#     return proc_trigger2(y, f, multi_conditions, multi_cond_opp)

#
# @curried



# print(env_trigger(3).__module__)
# pp.pprint(dir(env_trigger))



# @curried
# def env_proc_trigger(trigger_time, update_f, time):
#     if time == trigger_time:
#         return update_f
#     else:
#         return lambda x: x




# def p1m1(_g, step, sL, s):
#     return {'param1': 1}
#
# def apply_policy_condition(policies, policy_id, f, conditions, _g, step, sL, s):
#     if trigger_condition(s, conditions):
#         policies[policy_id] = f(_g, step, sL, s)
#         return policies
#     else:
#         return policies
#
# def proc_trigger2(policies, conditions, policy_id, f):
#     return lambda _g, step, sL, s: apply_policy_condition(policies, policy_id, f, conditions,_g, step, sL, s)

# policies_updates = {"p1": udo_policyA, "p2": udo_policyB}


# @curried
# def proc_trigger(trigger_time, update_f, time):
#     if time == trigger_time:
#         return update_f
#     else:
#         return lambda x: x


# def repr(_g, step, sL, s, _input):
#     y = 'z'
#     x = s['state_udo'].__repr__()
#     return (y, x)