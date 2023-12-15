from typing import NamedTuple, Tuple, Dict, Union, List

class InitialValue(NamedTuple):
    value: object
    type: type


class Param(NamedTuple):
    value: object
    type: type


class ParamSweep(NamedTuple):
    value: List[object]
    type: type

InitialState = Dict[str, InitialValue]
SystemParameters = Dict[str, Union[Param, ParamSweep]]