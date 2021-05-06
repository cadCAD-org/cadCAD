from typing import Callable, List, Dict, Tuple

StateVariable = object
Parameter = List[object]

Params = dict
State = dict
Signal = dict
History = List[List[State]]
Substep = int

Policy = Callable[[Params, Substep, History, State], dict]
StateUpdate = Callable[[Params, Substep, History, State, Signal], Tuple[str, object]]

StateUpdateBlock = Dict[str, object]
TimestepBlock = List[StateUpdateBlock]