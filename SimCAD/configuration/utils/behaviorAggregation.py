from fn.op import foldr
from fn.func import curried


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
    def set_base_value(target_dict, source_dict, key):
        if key not in target_dict:
            return get_base_value(type(source_dict[key]))
        else:
            return target_dict[key]

    key_set = set(list(d1.keys()) + list(d2.keys()))

    return {k: f(set_base_value(d1, d2, k), set_base_value(d2, d1, k)) for k in key_set}


def dict_elemwise_sum():
    return dict_op(add)


# class BehaviorAggregation: