from typing import TypedDict, Callable, Union, Dict, List, Tuple, Iterable
from collections import deque

State = Dict[str, object]
Parameters = Dict[str, object]
SweepableParameters = Dict[str, List[object]]
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
    T: Iterable # Generator for the timestep variable
    N: int # Number of MC Runs
    M: Union[Parameters, SweepableParameters] # Parameters / List of Parameter to Sweep

TargetValue = object
EnvProcess: Callable[[State, SweepableParameters, TargetValue], TargetValue]
EnvProcesses = Dict[str, Callable]
TimeSeq = Iterable
SimulationID = int
Run = int
SubsetID = int
SubsetWindow = Iterable
N_Runs = int

ExecutorFunction = Callable[[Parameters, StateHistory, StateUpdateBlocks, EnvProcesses, TimeSeq, SimulationID, Run, SubsetID, SubsetWindow, N_Runs], object]
ExecutionParameter = Tuple[ExecutorFunction, Parameters, StateHistory, StateUpdateBlocks, EnvProcesses, TimeSeq, SimulationID, Run, SubsetID, SubsetWindow, N_Runs]


class SessionDict(TypedDict):
    user_id: str
    experiment_id: int
    session_id: str
    simulation_id: int
    run_id: int
    subset_id: int
    subset_window: deque
