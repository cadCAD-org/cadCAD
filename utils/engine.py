from datetime import datetime

def datetime_range(start, end, delta, dt_format='%Y-%m-%d %H:%M:%S'):
    reverse_head = end
    [start, end] = [datetime.strptime(x, dt_format) for x in [start, end]]

    def _datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    reverse_tail = [dt.strftime(dt_format) for dt in _datetime_range(start, end, delta)]
    return reverse_tail + [reverse_head]

def last_index(l):
    return len(l)-1

def retrieve_state(l, offset):
    return l[last_index(l) + offset + 1]

# def exo_proc_trigger(mech_step, update_f, y):
#     if mech_step == 1:
#         return update_f
#     else:
#         return lambda step, sL, s, _input: (y, s[y])



# def apply_exo_proc(s, x, y):
#     if s['mech_step'] == 1:
#         return x
#     else:
#         return s[y]

# def es5p2(step, sL, s, _input): # accept timedelta instead of timedelta params
#     y = 'timestamp'
#     x = ep_time_step(s, s['timestamp'], seconds=1)
#     return (y, x)