from collections import namedtuple
from inspect import getmembers, ismethod
from pandas.core.frame import DataFrame

from cadCAD.utils import SilentDF


def val_switch(v):
    if isinstance(v, DataFrame) is True:
        return SilentDF(v)
    else:
        return v


class udcView(object):
    def __init__(self, d, masked_members):
        self.__dict__ = d
        self.masked_members = masked_members

    def __repr__(self):
        members = {}
        variables = {
            k: val_switch(v) for k, v in self.__dict__.items()
            if str(type(v)) != "<class 'method'>" and k not in self.masked_members # and isinstance(v, DataFrame) is not True
        }
        members['methods'] = [k for k, v in self.__dict__.items() if str(type(v)) == "<class 'method'>"]

        members.update(variables)
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

    def get_view(self, masked_members):
        return udcView(self.members_dict, masked_members)

    def get_namedtuple(self):
        return namedtuple("Hydra", self.members_dict.keys())(*self.members_dict.values())


def UDO(udo, masked_members=['obj']):
    return udcBroker(udo).get_view(masked_members)


def udoPipe(obj_view):
    return UDO(obj_view.obj, obj_view.masked_members)
