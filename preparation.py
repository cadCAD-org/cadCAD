from .types import Param, SystemParameters, InitialState, Dict, List, ParamSweep
from itertools import product

def sweep_cartesian_product(sweep_params: Dict[str, tuple]) -> Dict[str, tuple]:
    """
    Makes a cartesian product from dictionary values.
    This is useful for plugging inside the sys_params dict, like:
    ```python
    sweep_params = {'a': [0.1, 0.2], 'b': [1, 2]}
    product_sweep 
    sys_params = {**cartesian_product_sweep(sweep_params),
                  'c': [0.1]}
    ```
    Usage:
    >>> sweep_params = {'a': [0.1, 0.2], 'b': [1, 2]}
    >>> cartesian_product_sweep(sweep_params)
    {'a': [0.1, 0.1, 0.2, 0.2], 'b': [1, 2, 1, 2]}
    """
    cartesian_product = product(*sweep_params.values())
    transpose_cartesian_product = zip(*cartesian_product)
    zipped_sweep_params = zip(sweep_params.keys(), transpose_cartesian_product)
    sweep_dict = dict(zipped_sweep_params)
    sweep_dict = {k: list(v) for k, v in sweep_dict.items()}
    return sweep_dict


def prepare_params(params: SystemParameters,
                   cartesian_sweep: bool=False) -> Dict[str, List[object]]:
    simple_params = {k: [v.value]
                     for k, v in params.items()
                     if type(v) is Param}

    sweep_params = {k: v.value
                    for k, v in params.items()
                    if type(v) is ParamSweep}
    if cartesian_sweep is True:
        sweep_params = sweep_cartesian_product(sweep_params)
    else:
        pass
    
    cleaned_params = {**simple_params, **sweep_params}
    return cleaned_params


def prepare_state(state: InitialState) -> Dict[str, object]:
    cleaned_state = {k: v.value
                     for k, v in state.items()}
    return cleaned_state
