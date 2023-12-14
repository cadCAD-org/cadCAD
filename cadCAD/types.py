from typing import TypedDict, Callable, Union, Dict, List, Tuple

State = Dict[str, object]
Parameters = Dict[str, object]
Substep = int
StateHistory = List[List[State]]
PolicyOutput = Dict[str, object]
StateVariable = object

PolicyFunction = Callable[[Parameters, Substep, StateHistory, State], PolicyOutput]
StateUpdateFunction = Callable[[Parameters, Substep, StateHistory, State, PolicyOutput], Tuple[str, StateVariable]]

class StateUpdateBlock(TypedDict):
    policies: Dict[str, PolicyFunction]
    variables: Dict[str, StateUpdateFunction]


StateUpdateBlocks = List[StateUpdateBlock]
