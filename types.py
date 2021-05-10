from typing import Callable, List, Dict, Tuple, Union, NamedTuple

StateVariable = object
Parameter = Tuple[object]

Params = Dict[str, object]
State = Dict[str, object]
Signal = Dict[str, object]
History = List[List[State]]
Substep = int
VariableUpdate = Tuple[str, object]

Policy = Callable[[Params, Substep, History, State], Signal]
StateUpdate = Callable[[Params, Substep, History, State, Signal], VariableUpdate]

StateUpdateBlock = Dict[str, object]
TimestepBlock = List[StateUpdateBlock]

class InitialValue(NamedTuple):
    value: object
    type: type


class Param(NamedTuple):
    value: object
    type: type


class ParamSweep(NamedTuple):
    value: Tuple[object]
    type: type


InitialState = Dict[str, InitialValue]
SystemParameters = Dict[str, Union[Param, ParamSweep]]
