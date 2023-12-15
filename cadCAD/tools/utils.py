from cadCAD.types import *

def generic_suf(variable: str,
                signal: str='') -> StateUpdateFunction:
    """
    Generate a State Update Function that assigns the signal value to the 
    given variable. By default, the signal has the same identifier as the
    variable.
    """
    if signal is '':
        signal = variable
    else:
        pass

    def suf(_1, _2, _3, _4, signals: PolicyOutput) -> StateUpdateTuple:
        return (variable, signals[signal])
    return suf