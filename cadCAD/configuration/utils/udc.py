from collections import namedtuple
from inspect import getmembers, ismethod


class udcView(object):
    def __init__(self, d):
        self.__dict__ = d

    # returns dict to dataframe
    # def __repr__(self):
    def __repr__(self):
        members = {}
        functionless = {k: v for k, v in self.__dict__.items() if str(type(v)) != "<class 'method'>" and k != 'obj'}
        members['functions'] = [k for k, v in self.__dict__.items() if str(type(v)) == "<class 'method'>"]
        members.update(functionless)
        return f"{members}"


class udcBroker(object):
    def __init__(self, obj, function_filter=['__init__']):
        d = {}
        funcs = dict(getmembers(obj, ismethod))
        filtered_functions = {k: v for k, v in funcs.items() if k not in function_filter}
        d['obj'] = obj
        d.update(vars(obj))  # somehow is enough
        d.update(filtered_functions)

        self.members_dict = d

    def get_members(self):
        return self.members_dict

    def get_view(self):
        return udcView(self.members_dict)

    def get_namedtuple(self):
        return namedtuple("Hydra", self.members_dict.keys())(*self.members_dict.values())


def generate_udc_view(udc):
    return udcBroker(udc).get_view()


def next_udc_view(obj_view):
    return generate_udc_view(obj_view.obj)


