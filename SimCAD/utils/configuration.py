from datetime import datetime, timedelta
from decimal import Decimal
from fn.func import curried
from fn.op import foldr


def bound_norm_random(rng, low, high):
    # Add RNG Seed
    res = rng.normal((high+low)/2,(high-low)/6)
    if (res<low or res>high):
        res = bound_norm_random(rng, low, high)
    return Decimal(res)


@curried
def proc_trigger(trigger_step, update_f, step):
    if step == trigger_step:
        return update_f
    else:
        return lambda x: x


# accept timedelta instead of timedelta params
def time_step(dt_str, dt_format='%Y-%m-%d %H:%M:%S', days=0, minutes=0, seconds=30):
    dt = datetime.strptime(dt_str, dt_format)
    t = dt + timedelta(days=days, minutes=minutes, seconds=seconds)
    return t.strftime(dt_format)


# accept timedelta instead of timedelta params
def ep_time_step(s, dt_str, fromat_str='%Y-%m-%d %H:%M:%S', days=0, minutes=0, seconds=1):
    if s['mech_step'] == 0:
        return time_step(dt_str, fromat_str, days, minutes, seconds)
    else:
        return dt_str


def exo_update_per_ts(ep):
    @curried
    def ep_decorator(f, y, step, sL, s, _input):
        if s['mech_step'] + 1 == 1:  # inside f body to reduce performance costs
            return f(step, sL, s, _input)
        else:
            return (y, s[y])
    return {es: ep_decorator(f, es) for es, f in ep.items()}


def print_fwd(x):
    print(x)
    return x


def get_base_value(datatype):
    if datatype is str:
        return ''
    elif datatype is int:
        return 0
    elif datatype is list:
        return []
    return 0


def behavior_to_dict(v):
    return dict(list(zip(map(lambda n: 'b' + str(n + 1), list(range(len(v)))), v)))


add = lambda a, b: a + b


@curried
def foldr_dict_vals(f, d):
    return foldr(f)(list(d.values()))


def sum_dict_values():
    return foldr_dict_vals(add)

# AttributeError: 'int' object has no attribute 'keys'
# config7c
@curried
def dict_op(f, d1, d2):
    print('d1')
    print(d1)
    print('d2')
    print(d2)
    print()
    def set_base_value(target_dict, source_dict, key):
        if key not in target_dict:
            return get_base_value(type(source_dict[key]))
        else:
            return target_dict[key]

    key_set = set(list(d1.keys()) + list(d2.keys()))

    return {k: f(set_base_value(d1, d2, k), set_base_value(d2, d1, k)) for k in key_set}


def dict_elemwise_sum():
    return dict_op(add)