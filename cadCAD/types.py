from typing import TypedDict, Callable, Union, Dict, List, Tuple, Iterator

State = Dict[str, object]
Parameters = Dict[str, object]
SweepableParameters = Dict[str, list[object]]
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

class ConfigurationDict(TypedDict):
    T: Iterator # Generator for the timestep variable
    N: int # Number of MC Runs
    M: Union[Parameters, SweepableParameters] # Parameters / List of Parameter to Sweep