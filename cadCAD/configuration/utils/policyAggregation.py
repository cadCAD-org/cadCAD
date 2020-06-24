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


# @curried
# def foldr_dict_vals(f, d):
#     return foldr(f)(list(d.values()))
#
#
# def sum_dict_values():
#     return foldr_dict_vals(add)


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
#     return {k: f(set_base_value(d1, d2, k), set_base_value(d2, d1, k)) for k in key_set}
#
# def dict_elemwise_sum():
#     return dict_op(add)
