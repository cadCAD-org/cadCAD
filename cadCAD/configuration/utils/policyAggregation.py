from fn.op import foldr
from fn.func import curried
from collections import Counter

def get_base_value(x):
    if isinstance(x, str):
        return ''
    elif isinstance(x, int):
        return 0
    elif isinstance(x, list):
        return []
    else:
        return 0


def policy_to_dict(v):
    return dict(list(zip(map(lambda n: 'p' + str(n + 1), list(range(len(v)))), v)))


add = lambda a, b: a + b
# df_union = lambda a, b: ...

@curried
def foldr_dict_vals(f, d):
    return foldr(f)(list(d.values()))


def sum_dict_values():
    return foldr_dict_vals(add)


@curried
def dict_op(f, d1, d2):
    def set_base_value(target_dict, source_dict, key):
        if key not in target_dict:
            return get_base_value(source_dict[key])
        else:
            return target_dict[key]

    key_set = set(list(d1.keys()) + list(d2.keys()))


    return {k: f(set_base_value(d1, d2, k), set_base_value(d2, d1, k)) for k in key_set}
#
# @curried
# def dict_op(f, d1, d2):
#     def set_base_value(target_dict, source_dict, key):
#         if key not in target_dict:
#             return get_base_value(source_dict[key])
#         else:
#             return target_dict[key]
#
#     key_set = set(list(d1.keys()) + list(d2.keys()))
#
#     norm_d1 = {k: set_base_value(d1, d2, k) for k in key_set}
#     norm_d2 = {k: set_base_value(d2, d1, k) for k in key_set}
#
#     return {k: f(set_base_value(d1, d2, k), set_base_value(d2, d1, k)) for k in key_set}


# @curried
# def dict_op(f, d1, d2):
#     # d1C = Counter(d1)
#     # d2C = Counter(d2)
#     def set_base_value(target_dict, source_dict, key):
#         if key not in target_dict:
#             return get_base_value(source_dict[key])
#         else:
#             return target_dict[key]
#     key_set = set(list(d1.keys()) + list(d2.keys()))
#     norm_d1 = Counter({k: set_base_value(d1, d2, k) for k in key_set})
#     norm_d2 = Counter({k: set_base_value(d2, d1, k) for k in key_set})
#     # print(norm_d1)
#     # print(norm_d2)
#     print(norm_d1 + norm_d2)
#     # print(f(norm_d1, norm_d2))
#     print()
#     return f(norm_d1, norm_d2)

def dict_elemwise_sum():
    return dict_op(add)
