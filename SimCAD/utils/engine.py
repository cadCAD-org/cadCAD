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