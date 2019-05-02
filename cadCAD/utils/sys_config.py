from cadCAD.configuration.utils import ep_time_step


def increment(y, incr_by):
    return lambda _g, step, sL, s, _input: (y, s[y] + incr_by)

def track(y):
    return lambda _g, step, sL, s, _input: (y, s[y].x)

def simple_state_update(y, x):
    return lambda _g, step, sH, s, _input: (y, x)

def simple_policy_update(y):
    return lambda _g, step, sH, s: y

def update_timestamp(y, timedelta, format):
    return lambda _g, step, sL, s, _input: (
        y,
        ep_time_step(s, dt_str=s[y], fromat_str=format, _timedelta=timedelta)
    )

def add(y, x):
    return lambda _g, step, sH, s, _input: (y, s[y] + x)

def s(y, x):
    return lambda _g, step, sH, s, _input: (y, x)


# def repr(_g, step, sL, s, _input):
#     y = 'z'
#     x = s['state_udo'].__repr__()
#     return (y, x)