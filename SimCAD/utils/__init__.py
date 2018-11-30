def print_fwd(x):
    print(x)
    return x


flatten = lambda l: [item for sublist in l for item in sublist]


def flatmap(f, items):
        return list(map(f, items))


def key_filter(l, keyname):
    return [v[keyname] for k, v in l.items()]