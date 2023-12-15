from functools import reduce
from collections import defaultdict
from itertools import product
import warnings
from typing import Union
from cadCAD.types import *
from typing import List, Dict, Union

import functools
import operator

from pandas import DataFrame # type: ignore


class SilentDF(DataFrame):
    def __repr__(self):
        return str(hex(id(DataFrame)))


def append_dict(dict: dict, new_dict: dict) -> dict:
    """
    >>> append_dict({1: 2, 3: 4}, {3: 5})
    {1: 2, 3: 5}
    """
    dict.update(new_dict)
    return dict


def arrange_cols(df: DataFrame, reverse=False) -> DataFrame:
    """
    Reorders `df` columns so that the variable order is `session_metrics`
    followed by `sys_metrics` and `results_cols`
    """
    session_metrics = ['session_id', 'user_id', 'simulation_id', 'run_id']
    sys_metrics = ['run', 'timestep', 'substep']
    result_cols = list(set(df.columns) - set(session_metrics) - set(sys_metrics))
    result_cols.sort(reverse=reverse)
    return df[session_metrics + sys_metrics + result_cols]


class IndexCounter:
    def __init__(self):
        self.i = 0

    def __call__(self):
        self.i += 1
        return self.i


def compose(*functions: Tuple[callable]) -> object:
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def pipe(x: object) -> object:
    return x


def print_pipe(x: object) -> object:
    print(x)
    return x


def tupalize(k: object, vs: Union[list, dict]):
    """
    >>> tupalize(1, 1)
    [(1, 1)]
    >>> tupalize(1, [2, 3])
    [(1, 2), (1, 3)]
    """
    l = []
    if isinstance(vs, list):
        for v in vs:
            l.append((k, v))
    else:
        l.append((k, vs))
    return l

def flattenDict(l: dict) -> list:
    """
    >>> flattenDict({1: [1, 2, 3], 4: 5})
    [{1: 1, 4: 5}, {1: 2, 4: 5}, {1: 3, 4: 5}]
    """
    flat_list = [tupalize(k, vs) for k, vs in l.items()]
    flat_dict = [dict(items) for items in product(*flat_list)]
    return flat_dict


def flatten(l: Union[list, dict]):
    if isinstance(l, list):
        return functools.reduce(operator.iconcat, l, [])
    elif isinstance(l, dict):
        return flattenDict(l)


def flatMap(f, collection):
    return flatten(list(map(f, collection)))


def dict_filter(dictionary, condition):
    return dict([(k, v) for k, v in dictionary.items() if condition(v)])


def get_max_dict_val_len(g: Dict[str, List[int]]) -> int:
    return len(max(g.values(), key=len))


def tabulate_dict(d: Dict[str, List[int]]) -> Dict[str, List[int]]:
    max_len = get_max_dict_val_len(d)
    _d = {}
    for k, vl in d.items():
        if len(vl) != max_len:
            _d[k] = vl + list([vl[-1]] * (max_len-1))
        else:
            _d[k] = vl

    return _d


def flatten_tabulated_dict(d: Dict[str, List[int]]) -> List[dict[str, int]]:
    max_len = get_max_dict_val_len(d)
    dl: List[dict] = [{} for i in range(max_len)]

    for k, vl in d.items():
        for v, i in zip(vl, list(range(len(vl)))):
            dl[i][k] = v

    return dl


def contains_type(_collection, type):
    return any(isinstance(x, type) for x in _collection)


def drop_right(l, n):
    return l[:len(l) - n]


def key_filter(l, keyname):
    if (type(l) == list):
        return [v[keyname] for v in l]
        # Keeping support to dictionaries for backwards compatibility
        # Should be removed in the future
    warnings.warn(
        "The use of a dictionary to describe Partial State Update Blocks will be deprecated. Use a list instead.",
        FutureWarning)
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


def curry_pot(f, *argv):
    sweep_ind = f.__name__[0:5] == 'sweep'
    arg_len = len(argv)
    if sweep_ind is True and arg_len == 4:
        return f(argv[0])(argv[1])(argv[2])(argv[3])
    elif sweep_ind is False and arg_len == 4:
        return f(argv[0], argv[1], argv[2], argv[3])
    elif sweep_ind is True and arg_len == 3:
        return f(argv[0])(argv[1])(argv[2])
    elif sweep_ind is False and arg_len == 3:
        return f(argv[0], argv[1], argv[2])
    else:
        raise TypeError('curry_pot() needs 3 or 4 positional arguments')
