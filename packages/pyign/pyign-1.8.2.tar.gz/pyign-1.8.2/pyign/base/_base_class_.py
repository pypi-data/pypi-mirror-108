########################### _Base_Class_ #############################
# This module defines the object classes inherited by the application
# Includes object classes for sensors, relays, and system states
######################################################################

class PTSensor:
    pt_list = []
    pt_names = []
    pt_lower_limits = []
    pt_upper_limits = []
    def __init__(self, name, lowerbound, upperbound, status = 0, value = 0):
        self.name = name.upper()
        self.status = status
        self.value = value
        self.lowerbound = lowerbound
        self.upperbound = upperbound
    def set_value(self, value):
        self.value = value
        return self
    @classmethod
    def slate(cls, name, lowerbound, upperbound, status = 0, value = 0):
        obj = cls(name, lowerbound, upperbound, status, value)
        cls.pt_list.append(obj)
        cls.pt_names.append(name)
        cls.pt_lower_limits.append(lowerbound)
        cls.pt_upper_limits.append(upperbound)
        return obj


class TCSensor:
    tc_list = []
    tc_names = []
    tc_lower_limits = []
    tc_upper_limits = []
    def __init__(self, name, lowerbound, upperbound, status = 0, value = 0):
        self.name = name.upper()
        self.status = status
        self.value = value
        self.lowerbound = lowerbound
        self.upperbound = upperbound
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, lowerbound, upperbound, status = 0, value = 0):
        obj = cls(name, lowerbound, upperbound, status, value)
        cls.tc_list.append(obj)
        cls.tc_names.append(name)
        cls.tc_lower_limits.append(lowerbound)
        cls.tc_upper_limits.append(upperbound)
        return obj


class LCSensor:
    lc_list = []
    lc_names = []
    lc_lower_limits = []
    lc_upper_limits = []
    def __init__(self, name, lowerbound = None, upperbound = None, status = 0, value = 0):
        self.name = name.upper()
        self.status = status
        self.value = value
        self.lowerbound = lowerbound if lowerbound is not None else status 
        self.upperbound = upperbound if upperbound is not None else status
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, lowerbound = None, upperbound = None, status = 0, value = 0):
        obj = cls(name, lowerbound, upperbound, status, value)
        cls.lc_list.append(obj)
        cls.lc_names.append(name)
        cls.lc_lower_limits.append(lowerbound) 
        cls.lc_upper_limits.append(upperbound)
        return obj


class CLCSensor:
    clc_list = []
    clc_names = []
    clc_lower_limits = []
    clc_upper_limits = []
    def __init__(self, name, lowerbound = None, upperbound = None, status = 0, value = 0):
        self.name = name
        self.status = status
        self.value = value
        self.lowerbound = lowerbound 
        self.upperbound = upperbound
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, lowerbound = None, upperbound = None, status = 0, value = 0):
        obj = cls(name, lowerbound, upperbound, status, value)
        cls.clc_list.append(obj)
        cls.clc_names.append(name)
        cls.clc_lower_limits.append(lowerbound) 
        cls.clc_upper_limits.append(upperbound)
        return obj


class LSSensor:
    ls_list = []
    ls_names = []
    ls_limits = []
    def __init__(self, name, limit = None, status = 0, value = 0):
        self.name = name.upper()
        self.status = status
        self.value = value
        self.limit = limit if limit is not None else status 
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, limit = None, status = 0, value = 0):
        obj = cls(name, limit, status, value)
        cls.ls_list.append(obj)
        cls.ls_names.append(name)
        cls.ls_limits.append(limit) 
        return obj


class Igniter:
    ign_list = []
    ign_names = []
    def __init__(self, name, state = 0):
        self.name = name
        self.state = state
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, state = 0):
        obj = cls(name, state)
        cls.ign_list.append(obj)
        cls.ign_names.append(name)
        return obj


class Valve:
    vlv_list = []
    vlv_names = []
    def __init__(self, name, state = 0):
        self.name = name.upper()
        self.state = state
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, state = 0):
        obj = cls(name, state)
        cls.vlv_list.append(obj)
        cls.vlv_names.append(name)
        return obj


class Go:
    go_list = []
    go_names = []
    def __init__(self, name, state = 0):
        self.name = name.upper()
        self.state = state
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, state = 0):
        obj = cls(name, state)
        cls.go_list.append(obj)
        cls.go_names.append(name)
        return obj


class Tripped:
    trp_list = []
    trp_names = []
    def __init__(self, name, state = 0, reset = 0):
        self.name = name
        self.state = state
        self.reset = reset
    @classmethod
    def slate(cls, name, state = 0, reset = 0):
        obj = cls(name, state, reset)
        cls.trp_list.append(obj)
        cls.trp_names.append(name)
        return obj


class System:
    sys_list = []
    sys_names = []
    def __init__(self, name, state = 0):
        self.name = name
        self.state = state
    def getname(self):
        return self.name
    @classmethod
    def slate(cls, name, state = 0):
        obj = cls(name, state)
        cls.sys_list.append(obj)
        cls.sys_names.append(name)
        return obj