from typing import Callable, List, Dict, Tuple

StateVariable = object
Parameter = List[object]

Params = dict
State = dict
Signal = dict
History = List[List[State]]
Substep = int
VariableUpdate = Tuple[str, object]

Policy = Callable[[Params, Substep, History, State], Signal]
StateUpdate = Callable[[Params, Substep, History, State, Signal], VariableUpdate]

StateUpdateBlock = Dict[str, object]
TimestepBlock = List[StateUpdateBlock]

InitialValue = Tuple[object, type]
Param = Tuple[object, type]
ParamSweep = Tuple[List[object], type]