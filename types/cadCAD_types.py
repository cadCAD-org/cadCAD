from typing import List, Dict

StateVariable = object
Parameter = List[object]
StateUpdateBlock = Dict[str, Dict[str, callable]]
TimestepBlock = List[StateUpdateBlock]