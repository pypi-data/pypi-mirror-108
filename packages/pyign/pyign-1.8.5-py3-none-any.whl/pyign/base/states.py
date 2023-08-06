########################### states ##################################
# This module holds the state classes used for the application
#
######################################################################
from pyign.base._base_class_ import System, Tripped, Go

class AbortState(System):
    """The Abort State of a System determines if an 'Abort' has been triggered and the system is 
        in manditory 'SAFE' mode.

        Attributes
        ----------
        state : 'Abort' State [1]
        state[0] : 'Go' State
        state[1] : 'Abort Has Been triggered' State
        nanny : Monitor System [1]
        """
    abort_state = System(0)     #Initialize 'Abort' State
    nanny = System(0) 
    abort_tripped = System(0) 

    def abort_nanny_status(self):
        abort_nanny_status = [self.abort_state.state, self.nanny.state]
        return abort_nanny_status  #Return Abort and Nanny States

def getAbortState(self = AbortState):
    """Returns the current state of the Abort"""
    return self.abort_state.state  

def getNanny(self = AbortState):
    """Returns the current state of Nanny"""
    return self.nanny.state 

def getAbortTripped(self = AbortState):
    """Returns if an Abort has been tripped"""
    return self.abort_tripped.state 

def setAbortState(state, self = AbortState):
    """Sets the state of the Abort object."""
    self.abort_state.state = state  

def setNanny(state, self = AbortState):
    """Sets the state of the Nanny object."""
    self.nanny.state = state  

def setAbortTripped(state, self = AbortState):
    """Sets the state of the Abort tripped object."""
    self.abort_tripped.state = state 

def assignAbortState(state, self = AbortState):
    """Assign is used by input matrix from LabVIEW to assign the current Abort state"""
    self.abort_state.state = state  

def assignNanny(state, self = AbortState):
    """Assign is used by input matrix from LabVIEW to assign the current Nanny state"""
    self.nanny.state = state  

def assignAbortTripped(state, self = AbortState):
    """Assign is used by input matrix from LabVIEW to assign the current Abort tripped state"""
    self.abort_tripped.state = state 


class IgniterArm(System):
    """The Igniter Arm determines if the engine igniter has lit.

        Attributes
        ----------
        igniter_arm : Igniter Arm [1]
        arm_active_status : Arm State [1]
        """
    # igniter_tripped_status = System(0)
    arm_active_status = System(0)  #Arm State
    igniter_test = System(0)

    def igniter_arm_active_status(self):
        igniter_arm_active_status = [self.arm_active_status.state, self.igniter_test.state]
        return igniter_arm_active_status  #Return All Ingitor Arm ACTIVE States

def getArmActive(self = IgniterArm):
    return self.arm_active_status.state  #Return Arm State

def getIgniterTest(self = IgniterArm):
    return self.igniter_test.state  #Return Igniter Testing State

def getIgniterArm(string, self = IgniterArm):
    string = string.upper()
    if string == 'ARM ACTIVE':
        single_ist = self.arm_active_status.state
    elif string == 'IGNITER TEST':
        single_ist = self.igniter_test.state
    return single_ist

def setArmActive(arm_active_status, self = IgniterArm):
    self.arm_active_status.state = arm_active_status  #Set Arm State

def setIgniterTest(igniter_test, self = IgniterArm):
    self.igniter_test.state = igniter_test  #Set Igniter Testing State


class GoState(Go):
    """A 'GO' signal is required from all control ends before beginning the ignition phase.

        Attributes
        ----------
        go_command : com Panel State
        go_ox : Ox Panel State
        go_fuel : Fuel Panel State
        go_water_suppression
        go_camera
        go_office
        go_record
        go_igniter_in
        """
    go_command = Go.slate('Command')
    go_ox = Go.slate('Ox')
    go_fuel = Go.slate('Fuel')
    go_water_suppression = Go.slate('Water Suppression')
    go_camera = Go.slate('Camera')
    go_office = Go.slate('Office')
    go_record = Go.slate('Record')
    go_igniter_in = Go.slate('Igniter IN')

def getAllGONames(self = GoState):
    return self.go_names

def getAllGOStates(self = GoState):
    states = [x.state for x in self.go_list]
    return states

def setGOState(string, state, self = GoState):
    string = string.upper()
    for x in self.go_list:
        if string == x.name:
            x.state = state
            break
    return self

def assignAllGOStates(array, self = GoState):
    i = 0
    for x in self.go_list:
        x.state = array[i]
        i += 1
    return self

def setAllGOStates(array, self = GoState):
    i = 0
    for x in self.go_list:
        x.state = array[i]
        i += 1
    return self


class ReadBackState(Tripped):
    """The Feed Back State outputs states to LabVIEW which feeds back into PyIGN.

        Attributes
        ----------
        igniter_tripped : Igniter Tripped Status [1]
        ox_main_tripped : Ox Main Tripped Status [2]
        fuel_main_tripped : Fuel Main Tripped Status [3]
        dewar_level_tripped : Dewar Level Tripped Status [4]
        """
    abort2_tripped = Tripped.slate('abort tripped')
    igniter2_tripped = Tripped.slate('igniter tripped')
    ox_main_tripped = Tripped.slate('ox main tripped')
    fuel_main_tripped = Tripped.slate('fuel main tripped')
    dewar_level_tripped = Tripped.slate('dewar level tripped')

def getAllReadBackNames(self = ReadBackState):
    return self.trp_names

def getAllReadBackStates(self = ReadBackState):
    states = [x.state for x in self.trp_list]
    return states

def getAllReadBackResets(self = ReadBackState):
    resets = [x.reset for x in self.trp_list]
    return resets

def setAllReadBackStates(stateArray, self = ReadBackState):
    i = 0
    for x in self.trp_list:
        x.state = stateArray[i]
        i += 1
    return self


def setAllReadBackResets(resetArray, self = ReadBackState):
    i = 0
    for x in self.trp_list:
        x.reset = resetArray[i]
        i += 1
    return self


def getReadBack(string, self = ReadBackState):
    """Access protected class data to evaluate and monitor the system readback status. The returned
       value representation is a int equal to 0 when 'INACTIVE or 1 when 'ACTIVE'. This approach is
       a secure method to access and read systems igniter value.

    Parameters
    ----------
    igniter_tripped : int
        Value for igniter ACTIVE range from 0 for 'INACTIVE' to 1 for 'Activated'.
    ox_main_tripped : str
        Set strings range from '1-4' for each test stand readback class.

    Returns
    -------
    readback_state : int
         0 = 'INACTIVE' system readback ACTIVE, 1 = 'Activated' system readback ACTIVE

    args[0] = rbst
    args[1] = str
    """
    string = string.lower()
    if string == 'abort tripped':
        single_rbst = self.abort2_tripped.state
    elif string == 'igniter tripped':
        single_rbst =self.igniter2_tripped.state
    elif string == 'ox main tripped':
        single_rbst = self.ox_main_tripped.state
    elif string == 'fuel main tripped':
        single_rbst = self.fuel_main_tripped.state
    elif string == 'dewar level tripped':
        single_rbst = self.dewar_level_tripped.state
    return single_rbst

def setReadBack(string, state, self = ReadBackState):
    """Access and changes protected readback status class data. The returned value representation
       is an integer. This approach is a secure method to access and change saved system readback
       state values.

    Parameters
    ----------
    readback_state : int
        Values for readback state range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    value : int
        Set readback value from 0 for 'SAFE' to 1 for 'ACTIVE'.

    Returns
    -------
    readback_state : int
         0 = 'SAFE' system readback state, 1 = 'ACTIVE' system readback state

    args[0] = rbst
    args[1] = value string
    args[2] = value
    """
    string = string.lower()
    if string == 'abort tripped':
        self.abort2_tripped.state = state
    elif string == 'igniter tripped':
        self.igniter2_tripped.state = state
    elif string == 'ox main tripped':
        self.ox_main_tripped.state = state
    elif string == 'fuel main tripped':
        self.fuel_main_tripped.state = state
    elif string == 'dewar level tripped':
        self.dewar_level_tripped.state = state
    return self

def setReadBackReset(string, reset, self = ReadBackState):
    """Access and changes protected readback reset class data. The returned value representation
       is an integer. This approach is a secure method to access and change saved system readback
       state values.

    Parameters
    ----------
    readback_state : int
        Values for readback state range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    value : int
        Set readback value from 0 for 'SAFE' to 1 for 'ACTIVE'.

    Returns
    -------
    readback_state : int
         0 = 'SAFE' system readback state, 1 = 'ACTIVE' system readback state

    args[0] = rbst
    args[1] = value string
    args[2] = value
    """
    string = string.lower()
    if string == 'abort reset':
        self.abort2_tripped.reset = reset
    elif string == 'igniter reset':
        self.igniter2_tripped.reset = reset
    elif string == 'ox main reset':
        self.ox_main_tripped.reset = reset
    elif string == 'fuel main reset':
        self.fuel_main_tripped.reset = reset
    elif string == 'dewar level reset':
        self.dewar_level_tripped.reset = reset
    return self




class SequenceState(System):
    seq_state = System(0)  #Initialize 'Sequence' State
    seq_check = System(0)  #Initialize 'Sequence Check' State
    seq_active = System(0)  #Initialize 'Sequence Active' State
    seq_flow_meter = System(0)  #Initialize 'Sequence Flow Meter' State

def getSeqState(self = SequenceState):
        return self.seq_state.state

def getSeqCheck(self = SequenceState):
        return self.seq_check.state

def getSeqActive(self = SequenceState):
        return self.seq_active.state

def getSeqFlowMeter(self = SequenceState):
        return self.seq_active.state

def setSeqState(input_name, self = SequenceState):
    input_name = input_name.lower()
    if input_name == 'enable sequence':
        self.seq_check.state = 1
    if input_name == 'sequence active':
        self.seq_active.state = 1
    if input_name == 'sequence flow meter':
        self.seq_flow_meter.state = 1
    return 

def setSeq(input_name, self = SequenceState):
    input_name = input_name.lower()
    if input_name == 'none':
        self.seq_state.state = 0
    elif input_name == 'cold flow':
        self.seq_state.state = 1
    elif input_name == 'startup':
        self.seq_state.state = 2 
    elif input_name == 'ox vent':
        self.seq_state.state = 3
    elif input_name == 'fuel vent':
        self.seq_state.state = 4
    elif input_name == 'system cycle':
        self.seq_state.state = 5
    elif input_name == 'purge 1':
        self.seq_state.state = 6
    elif input_name == 'purge 2':
        self.seq_state.state = 7
    elif input_name == 'valve firing sim':
        self.seq_state.state = 8
    elif input_name == 'igniter active':
        self.seq_state.state = 9
    return self.seq_state.state
