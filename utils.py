from .types import Signal, StateUpdate, VariableUpdate

def generic_suf(variable: str,
                signal: str='') -> StateUpdate:
    """
    Generate a State Update Function that assigns the signal value to the 
    given variable. By default, the signal has the same identifier as the
    variable.
    """
    if signal is '':
        signal = variable
    else:
        pass

    def suf(_1, _2, _3, _4, signals: Signal) -> VariableUpdate:
        return (variable, signals[signal])
    return suf