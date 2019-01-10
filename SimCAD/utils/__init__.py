def pipe(x):
    return x


def print_pipe(x):
    print(x)
    return x


def flatten(l):
    return [item for sublist in l for item in sublist]


def flatmap(f, items):
    return list(map(f, items))


def key_filter(l, keyname):
    return [v[keyname] for k, v in l.items()]


def rename(new_name, f):
    f.__name__ = new_name
    return f