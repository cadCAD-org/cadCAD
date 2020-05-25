from funcy import curry
from cadCAD.configuration.utils import ep_time_step, time_step


def increment(y, incr_by):
    return lambda _g, step, sL, s, _input, **kwargs: (y, s[y] + incr_by)


def track(y):
    return lambda _g, step, sL, s, _input, **kwargs: (y, s[y].x)


def simple_state_update(y, x):
    return lambda _g, step, sH, s, _input, **kwargs: (y, x)


def simple_policy_update(y):
    return lambda _g, step, sH, s, **kwargs: y


def update_timestamp(y, timedelta, format):
    return lambda _g, step, sL, s, _input, **kwargs: (
        y,
        ep_time_step(s, dt_str=s[y], fromat_str=format, _timedelta=timedelta)
    )


def apply(f, y: str, incr_by: int):
    return lambda _g, step, sL, s, _input, **kwargs: (y, curry(f)(s[y])(incr_by))


def add(y: str, incr_by):
    return apply(lambda a, b: a + b, y, incr_by)


def increment_state_by_int(y: str, incr_by: int):
    return lambda _g, step, sL, s, _input, **kwargs: (y, s[y] + incr_by)


def s(y, x):
    return lambda _g, step, sH, s, _input, **kwargs: (y, x)


def time_model(y, substeps, time_delta, ts_format='%Y-%m-%d %H:%M:%S'):
    def apply_incriment_condition(s):
        if s['substep'] == 0 or s['substep'] == substeps:
            return y, time_step(dt_str=s[y], dt_format=ts_format, _timedelta=time_delta)
        else:
            return y, s[y]
    return lambda _g, step, sL, s, _input, **kwargs: apply_incriment_condition(s)
