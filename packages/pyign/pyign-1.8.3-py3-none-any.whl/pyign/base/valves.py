########################### valves ################################
# This module holds the classes for the physical relay output which 
# controls the valves and igniter of the test stand.
####################################################################
from pyign.base._base_class_ import Valve, Igniter


class ValveState(Valve):
    """The ValveState Class contains the valve class instances.
        
        Each Valve is slated into the system which creates an object of its
        parent class and adds the object to a dynamic list.
        
        ----------
        Valve Parameters:

        Name - The Name follows the P&ID format

        State - The state signifies if the valve is open or closed. Default = 0

        ----------
        Returned Parameters:

        Valve Object

        Array of Valve Objects

        """
    valve_110 = Valve.slate('ABV-PR-110') #ABV-PR-110 Ox Press
    valve_120 = Valve.slate('ABV-PR-120') #ABV-PR-120 Fuel Press
    valve_210 = Valve.slate('ABV-OX-210') #ABV-OX-210 Ox Vent
    valve_310 = Valve.slate('ABV-FU-310') #ABV-FU-310 Fuel Vent
    valve_220 = Valve.slate('ABV-OX-220') #ABV-OX-220 Ox Isolation
    valve_320 = Valve.slate('ABV-FU-320') #ABV-FU-320 Fuel Isolation
    valve_230 = Valve.slate('ABV-OX-230') #ABV-OX-230 Ox Chill
    valve_330 = Valve.slate('ABV-FU-330') #ABV-FU-330 Fuel Purge
    valve_240 = Valve.slate('ABV-OX-240') #ABV-OX-240 Ox Main
    valve_340 = Valve.slate('ABV-FU-340') #ABV-FU-340 Fuel Main
    valve_250 = Valve.slate('ABV-OX-250') #ABV-OX-250 Ox Fill
    valve_610 = Valve.slate('ABV-WS-610') #ABV-WS-610 Water Suppression
    valve_620 = Valve.slate('ABV-WS-620') #ABV-WS-620 Fire-Be-Gone

def getAllVLVNames(self = ValveState):
    """Returns an array of names for each object instance in the Valve class"""
    return self.vlv_names

def getAllVLVStates(self = ValveState):
    """Returns an array of the state of each object instance in the valve class"""
    states = [x.state for x in self.vlv_list]
    return states

def getVLVState(string, self = ValveState):
    """Returns the valve's current state for the object named in the string parameter"""
    string = string.upper()
    for x in self.vlv_list:
        if string == x.name:
            single_vst = x.state
            break
    return single_vst

def assignAllVLVStates(array, self = ValveState):
    """Assign is used by input matrix from LabVIEW to assign each valve's current value"""
    i = 0
    for x in self.vlv_list:
        x.state = array[i]
        i += 1
    return self


def setVLVState(string, state, self = ValveState):
    """Set is used to set the state of the valve specified by the input string.
    
        ----------
        Parameters:

        OPEN is defined as '1'

        CLOSE is defined as '0'

        The Horizontal Test Stand performs a SAFE state by receiving no power, or assigning '0' to 
        all the valves. The hardware for the vents results in the vents opening instead of closing.
        The OPEN/CLOSE logic for these valves are reversed, resulting in the valve class functions to 
        be written as seen below in the setVLVState function.

        """
    if string == 'ABV-PR-110':
        self.valve_110.state = state
    elif string == 'ABV-PR-120':
        self.valve_120.state = state
    elif string == 'ABV-OX-210':
        state = 1 - state
        self.valve_210.state = state
    elif string == 'ABV-FU-310':
        state = 1 - state
        self.valve_310.state = state
    elif string == 'ABV-OX-220':
        self.valve_220.state = state
    elif string == 'ABV-FU-320':
        self.valve_320.state = state
    elif string == 'ABV-OX-230':
        self.valve_230.state = state
    elif string == 'ABV-FU-330':
        self.valve_330.state = state
    elif string == 'ABV-OX-240':
        self.valve_240.state = state
    elif string == 'ABV-FU-340':
        self.valve_340.state = state
    elif string == 'ABV-OX-250':
        self.valve_250.state = state
    elif string == 'ABV-WS-610':
        self.valve_610.state = state
    elif string == 'ABV-WS-620':
        self.valve_620.state = state

def initValveState(self = ValveState):
    """Initiates the valves to their SAFE configuration"""
    for x in self.vlv_list:
        x.state = 0
    return self


class IgniterState(Igniter):
    """The IgniterState Class contains the Igniter class instance.
        
        The relay for the igniter is slated into the system which creates an object of its
        parent class.
        
        ----------
        Igniter Parameters:

        Name - Igniter

        State - The state signifies if the Igniter is ACTIVE '1' or INACTIVE '0'. Default = 0

        ----------
        Returned Parameters:

        Igniter Object

        """
    igniter = Igniter.slate('Igniter') 


def getIGNState(self = IgniterState):
    """Returns the state of the igniter object."""
    return self.igniter.state

def setIGNState(state, self = IgniterState):
    """Sets the state of the igniter object."""
    self.igniter.state = state
    return self

def assignIGNState(state, self = IgniterState):
    """Assign is used by input matrix from LabVIEW to assign the current igniter state"""
    self.igniter.state = state
    return self
