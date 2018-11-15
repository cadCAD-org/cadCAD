flatten = lambda l: [item for sublist in l for item in sublist]

def flatmap(f, items):
        return list(map(f, items))