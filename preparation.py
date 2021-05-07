from .types import Param, SystemParameters, InitialState, Dict, List, ParamSweep


def prepare_params(params: SystemParameters) -> Dict[str, List[object]]:
    simple_params = {k: [v.value]
                     for k, v in params.items()
                     if type(v) is Param}
    sweep_params = {k: v.value
                    for k, v in params.items()
                    if type(v) is ParamSweep}
    cleaned_params = {**simple_params, **sweep_params}
    return cleaned_params


def prepare_state(state: InitialState) -> Dict[str, object]:
    cleaned_state = {k: v.value
                     for k, v in state.items()}
    return cleaned_state
