def pipe(x):
    return x


def print_pipe(x):
    print(x)
    return x


def flatten(l):
    return [item for sublist in l for item in sublist]

import warnings
def key_filter(l, keyname):
    if (type(l)==list):
        return [v[keyname] for v in l]
    # Keeping support to dictionaries for backwards compatibility
    # Should be removed in the future
    warnings.warn("The use of a dictionary to describe Partial State Update Blocks will be deprecated. Use a list instead.", FutureWarning)
    return [v[keyname] for k, v in l.items()]


def rename(new_name, f):
    f.__name__ = new_name
    return f
