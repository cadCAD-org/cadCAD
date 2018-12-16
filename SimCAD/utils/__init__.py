from collections import defaultdict
from itertools import product
# from fn.func import curried


def pipe(x):
    return x


def print_pipe(x):
    print(x)
    return x


def flattenDict(l):
    def tupalize(k, vs):
        l = []
        if isinstance(vs, list):
            for v in vs:
                l.append((k, v))
        else:
            l.append((k, vs))
        return l

    flat_list = [tupalize(k, vs) for k, vs in l.items()]
    flat_dict = [dict(items) for items in product(*flat_list)]
    return flat_dict


def flatten(l):
    if isinstance(l, list):
        return [item for sublist in l for item in sublist]
    elif isinstance(l, dict):
        return flattenDict(l)


def flatMap(f, collection):
    return flatten(list(map(f, collection)))


def dict_filter(dictionary, condition):
    return dict([(k, v) for k, v in dictionary.items() if condition(v)])


def contains_type(_collection, type):
    return any(isinstance(x, type) for x in _collection)


def drop_right(l, n):
    return l[:len(l)-n]


def mech_sweep_filter(mechanisms):
    mech_states_dict = dict([(k, v['states']) for k, v in mechanisms.items()])
    return dict([
        (k, dict_filter(v, lambda v: isinstance(v, list))) for k, v in mech_states_dict.items()
            if contains_type(list(v.values()), list)
    ])


def state_sweep_filter(raw_exogenous_states):
    return dict([(k, v) for k, v in raw_exogenous_states.items() if isinstance(v, list)])

# def flatmap(f, items):
#     return list(map(f, items))


def key_filter(l, keyname):
    return [v[keyname] for k, v in l.items()]


def groupByKey(l):
    d = defaultdict(list)
    for key, value in l:
        d[key].append(value)
    return list(dict(d).items()).pop()


# @curried
def rename(new_name, f):
    f.__name__ = new_name
    return f

# def rename(newname):
#     def decorator(f):
#         f.__name__ = newname
#         return f
#     return decorator