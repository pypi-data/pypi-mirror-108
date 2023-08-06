########################### ehms_core #############################
#
#
###################################################################

# third-party libraries
import numpy as np

# local imports
from pyign.manifest._built_in_ import *
from pyign.manifest._engine_config_ import *
from pyign.base.valves import ValveState as vst
from pyign.base.valves import IgniterState as ist
from pyign.base.states import GoState as gst
from pyign.base.states import AbortState as abt
from pyign.base.valves import getAllVLVStates, setIGNState, getIGNState, setVLVState
from pyign.base.states import (setAllReadBackStates, setAllReadBackResets, getNanny, setAbortState, setAbortTripped, getAllGOStates,
                               getSeqState, setSeqState, getAbortTripped, getIgniterTest, getIgniterArm, getAbortState, assignAllGOStates, 
                               setSeq)
from pyign.base.sensors import (assignPTValues, assignTCValues, assignSNSCalc, assignLCValues, getPTValue, getAllPTStatus, getAllTCStatus,
                                assignLSValues, getAllLCStatus, getAllLSStatus, getAllPTNames, getAllTCNames, getAllLCNames, getAllLSNames,
                                getAllPTLowerLimits, getAllPTUpperLimits, getAllTCLowerLimits, getAllTCUpperLimits, getAllLCLowerLimits,
                                getAllLCUpperLimits, setAllPTStatus, setAllTCStatus, setAllLCStatus, setAllLSStatus, getAllPTValues, 
                                getAllTCValues, getAllLCValues, getAllLSValues, getAllLSLimits, getAllLS)
from pyign.core.notification_core import setAbortString, getAbortString



def assignAllReadBack(resetArray, valueArray):
    """Access and changes all the sensors values to the input value from the matrix.
        For PT, TC, and LC classes the 3rd element of each sensor represents the current
        sensor value.  For the LS class, the 2nd element of each sensor repressents the
        current sensor value.

    Parameters
    ----------
    rbst : Pressure Transducer Sensor Class
    readback_values : Thermocouple Sensor Class


    Returns
    -------
    rbst : Pressure Transducer Sensor Class
            With updated values.

    args[0] = rbst
    args[1] = rb_values
    args[2] = rb_reset
    """
    """
    args[0].setAbortTripped(args[0], args[1][0])
    args[0].setIgniterTripped(args[0], args[1][1])
    args[0].setOxMainTripped(args[0], args[1][2])
    args[0].setFuelMainTripped(args[0], args[1][3])
    args[0].setDewarLevelTripped(args[0], args[1][4])

    args[0].resetAbortTripped(args[0], args[2][0])
    args[0].resetIgniterTripped(args[0], args[2][1])
    args[0].resetOxMainTripped(args[0], args[2][2])
    args[0].resetFuelMainTripped(args[0], args[2][3])
    args[0].resetDewarLevelTripped(args[0], args[2][4])
    """

    """
    args[0].abort_tripped[0] = args[1][0]
    args[0].igniter_tripped[0] = args[1][1]
    args[0].ox_main_tripped[0] = args[1][2]
    args[0].fuel_main_tripped[0] = args[1][3]
    args[0].dewar_level_tripped[0] = args[1][4]

    args[0].abort_tripped[1] = args[2][0]
    args[0].igniter_tripped[1] = args[2][1]
    args[0].ox_main_tripped[1] = args[2][2]
    args[0].fuel_main_tripped[1] = args[2][3]
    args[0].dewar_level_tripped[1] = args[2][4]
    """
    setAllReadBackResets(resetArray)
    return 

def assignAllSNSCalc():
    """Access and changes protected Igniter State class data. The returned value representation
       is an integer. This approach is a secure method to access and change saved system igniter
       state values.

    Parameters
    ----------
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    value : int
        Set igniter value from 0 for 'SAFE' to 1 for 'ACTIVE'.

    Returns
    -------
    igniter_state : int
         0 = 'SAFE' system Igniter State, 1 = 'ACTIVE' system Igniter State

    args[0] = clc
    args[1] = ptl
    args[2] = tcl
    """

    value_215 = (getPTValue('PT-OX-210') + getPTValue('PT-OX-211'))/2
    value_315 = (getPTValue('PT-FU-310') + getPTValue('PT-FU-311'))/2
    value_dewer = (getPTValue('PT-OX-240') - getPTValue('PT-OX-210'))
    assignSNSCalc('PT-OX-CLC-215', value_215)
    assignSNSCalc('PT-FU-CLC-315', value_315)
    assignSNSCalc('PT-OX-CLC-DEWAR', value_dewer)
    return 

def getAllSensorStatus():
    """Access and reads protected sensor state class data using single integer value. The returned
       value representation is a 1 by 1 integer list array.

    Parameters
    ----------
    sensor_limits : int array
        Values for all the system sensors.
    igniter_state : int
        Values for valve state range from 0 for 'SAFE' to 1 for 'ACTIVE'.

    Returns
    -------
    indicator_state : int
         0 = 'GO' system indicators, 1 = 'NOGO' system system indicators.

    args[0] = ptl
    args[1] = tcl
    args[2] = lcl
    args[3] = lsl
    """
    return getAllPTStatus(), getAllTCStatus(), getAllLCStatus(), getAllLSStatus()

def getAllSensorNames():
    """Access and reads protected sensor state class data using single integer value. The returned
       value representation is a 1 by 1 integer list array.

    Parameters
    ----------
    sensor_limits : int array
        Values for all the system sensors.
    igniter_state : int
        Values for valve state range from 0 for 'SAFE' to 1 for 'ACTIVE'.

    Returns
    -------
    indicator_state : int
         0 = 'GO' system indicators, 1 = 'NOGO' system system indicators.


    args[0] = ptl
    args[1] = tcl
    args[2] = lcl
    args[3] = lsl
    """
    return getAllPTNames(), getAllTCNames(), getAllLCNames(), getAllLSNames()

def getAllNannySensorStatus():
    """Access and reads protected sensor state class data using single integer value. The returned
       value representation is a 1 by 1 integer list array.

    Parameters
    ----------
    sensor_limits : int array
        Values for all the system sensors.
    igniter_state : int
        Values for valve state range from 0 for 'SAFE' to 1 for 'ACTIVE'.

    Returns
    -------
    indicator_state : int
         0 = 'GO' system indicators, 1 = 'NOGO' system system indicators.

    args[0] = ptl
    args[1] = tcl
    args[2] = lcl
    """
    return getAllPTStatus(), getAllTCStatus(), getAllLCStatus()

def getSensorLimits():
    """Access protected class data to evaluate and monitor the system sensor limits states. The
       returned value representation is a numpy array of 0's add 1's. This approach is a secure
       method to access and read systems sensor values.

    Parameters
    ----------
    limits : int numpy array
        Values for all the system sensors.
    igniter_state : int
        Values for valve state range from 0 for 'SAFE' to 1 for 'ACTIVE'.

    Returns
    -------
    indicator_state : int
         0 = 'GO' system indicators, 1 = 'NOGO' system system indicators.

    args[0] = ptl
    args[1] = tcl
    args[2] = lcl
    """
    return (getAllPTLowerLimits(), getAllPTUpperLimits(), getAllTCLowerLimits(), getAllTCUpperLimits(),
            getAllLCLowerLimits(), getAllLCUpperLimits())

def setAllSensorStatus(ptArray, tcArray, lcArray, lsArray):
    """Access and changes all protected Sensor 'GO' Limits class data using three sensor arrays.
       The returned values represent arrays of 1 and 0 integer numpy arrays. This approach is a
       secure method to access and change saved system Sensor 'GO' values.

    Parameters
    ----------
    pt_limits : int numby array
        Values for PT state range from 0 for 'GO' to 1 for 'NOGO'.
    tc_limits : int numby array
        Values for TC state range from 0 for 'GO' to 1 for 'NOGO'.
    lc_limits : int numby array
        Values for LC state range from 0 for 'GO' to 1 for 'NOGO'.
    ls_limits: int array
        Values for LS state range from 0 for 'GO' to 1 for 'NOGO'.
    value : int numby array
        Set PT Limits values from 0 for 'GO' to 1 for 'NOGO'.
    value : int numby array
        Set TC Limits values from 0 for 'GO' to 1 for 'NOGO'.
    value : int numby array
        Set LC Limits values from 0 for 'GO' to 1 for 'NOGO'.
    value : int array
        Set LS Limits values from 0 for 'GO' to 1 for 'NOGO'.

    Returns
    -------
    pt_limits : int numpy array
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'GO' system PT Limits.
    tc_limits : int numpy array
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ###] = 'GO' system TC Limits.
    lc_limits : int numpy array
         [0, 0, 0] = 'GO' system LC Limits.
    ls_limits : int array
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'GO' system Ls Limits.

    """
    setAllPTStatus(ptArray)
    setAllTCStatus(tcArray)    
    setAllLCStatus(lcArray)
    setAllLSStatus(lsArray)
    return

def checkNannyLimits():
    """Check if any sensor is out of limit range, if out of bounds is detected, abort is tripped
       and system enters 'SAFE' mode.

    Parameters
    ----------
    nanny : int
        Value for Nanny mode system state indicates if test stand can automatically enter 'SAFE'
        mode if value is 0, and automated monitoring system is operating if value is 1.
    pt_limits : int numpy array
        Values for pressure transducer limits.
    tc_limits : int numpy array
        Values for thermocouple limits.
    lc_limits : int numpy array
        Values for load cell limits.
    pt_data : float numpy array
        Sensed pressure transducer data.
    tc_data : float numpy array
        Sensed thermocouple data.
    lc_data : float numpy array
        Sensed load cell data.

    Returns
    -------
    abort_state : int
         0 = system state is nominal, 1 = system abort.

    args[0] = nanny
    args[1] = ptl
    args[2] = tcl
    args[3] = lcl
    """
    if getNanny() == ACTIVE:
        pt_array, tc_array, lc_array = getAllNannySensorStatus()
        # TURNING OFF TC & LC ABORT DURING FIRST TEST FIRE #
        # if (np.sum(pt_array) + np.sum(tc_array) + np.sum(lc_array)) != SAFE:
        # TURNING OFF TC & LC ABORT DURING FIRST TEST FIRE #
        if (np.sum(pt_array)) != SAFE:
            setAbortState(ACTIVE)
            setAbortTripped(ACTIVE)
    return 

def checkAbort():
    """Check Abort State, if abort has been tripped, all valves and the igniter are set to 'SAFE'
       state until system is restarted.

    Parameters
    ----------
    valve_states : int numby array
        Values for valve state range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    abort_state : int
        Values for abort state range from 0 for 'System Performance Nominal' to 1 for 'Abort'.

    Returns
    -------
    valve_states : int numpy array
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
    igniter_state : int
         0 = 'SAFE' system Igniter State, 1 = 'ACTIVE' system Igniter State.

    args[0] = vst
    args[1] = ist
    args[2] = abt
    args[3] = gst
    """
    if getAbortState() == ACTIVE:
        
        vst.valve_110.state = SAFE
        vst.valve_120.state = SAFE
        vst.valve_210.state = SAFE
        vst.valve_310.state = SAFE
        vst.valve_220.state = SAFE
        vst.valve_320.state = SAFE
        vst.valve_230.state = SAFE
        vst.valve_330.state = SAFE
        vst.valve_240.state = SAFE
        vst.valve_340.state = SAFE
        vst.valve_250.state = SAFE
        vst.valve_610.state = SAFE
        ist.igniter.state = SAFE
        abt.nanny.state = SAFE
        gst.go_command.state = SAFE
        gst.go_ox.state = SAFE
        gst.go_fuel.state = SAFE
        gst.go_water_suppression.state = SAFE
        gst.go_camera.state = SAFE
        gst.go_office.state = SAFE
        gst.go_record.state = SAFE

       
    return 

def checkGo():
    """Check GO State, if all control panels are NOT a 'GO', set Igniter State 'SAFE' mode.

    Parameters
    ----------
    valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    go_state : int numpy array
        Values for system ready or 'GO' state indicates if a tests firing sequence can commence.
        If any of the three control panel operators return 0 or 'NOGO', the system will
        automatically dissable the firing sequence.

    Returns
    -------
    igniter_state : int
         0 = 'SAFE' system Igniter State, 1 = 'ACTIVE' system Igniter State.

    args[0] = vst
    args[1] = ist
    args[2] = gst
    """
    if np.sum(getAllGOStates()) != len(getAllGOStates()):
        setIGNState(INACTIVE)
    return 

def checkAutoSequence():
    """Check GO and Nanny States, if all control panels are NOT a 'ACTIVE', set Sequence State to 'none' mode.

    Parameters
    ----------
    valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    go_state : int numpy array
        Values for system ready or 'GO' state indicates if a tests firing sequence can commence.
        If any of the three control panel operators return 0 or 'NOGO', the system will
        automatically dissable the firing sequence.

    Returns
    -------
    sequence_state : int
         0 = 'none' system sequence state, 1 = 'enable sequence' system sequence state.

    args[0] = sqst
    args[1] = nanny
    args[2] = gst
    """
    if getSeqState() != 0:
        setSeq('none')
    return getSeqState()


def checkSequence():
    """Check GO and Nanny States, if all control panels are NOT a 'ACTIVE', set Sequence State to 'none' mode.

    Parameters
    ----------
    valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    go_state : int numpy array
        Values for system ready or 'GO' state indicates if a tests firing sequence can commence.
        If any of the three control panel operators return 0 or 'NOGO', the system will
        automatically dissable the firing sequence.

    Returns
    -------
    sequence_state : int
         0 = 'none' system sequence state, 1 = 'enable sequence' system sequence state.

    args[0] = sqst
    args[1] = nanny
    args[2] = gst
    """
    if (getNanny() == ACTIVE) & (np.sum(getAllGOStates()) == len(getAllGOStates())):
        setSeqState('enable sequence')
    return 

def checkFlowMeter(ButtonString):
    """Check GO and Nanny States, if all control panels are NOT a 'ACTIVE', set Sequence State to 'none' mode.

    Parameters
    ----------
    valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    go_state : int numpy array
        Values for system ready or 'GO' state indicates if a tests firing sequence can commence.
        If any of the three control panel operators return 0 or 'NOGO', the system will
        automatically dissable the firing sequence.

    Returns
    -------
    sequence_state : int
         0 = 'none' system sequence state, 1 = 'enable sequence' system sequence state.

    args[0] = sqst
    args[1] = flow meter state
    """
    if (ButtonString == ACTIVE):
        setSeqState('sequence flow meter')
    return

def checkSensors():
    """Check sensor GO State, if all sensors are NOT a 'GO', set Igniter State 'SAFE' mode.

    Parameters
    ----------
    pt_limits : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = Pressure Transducer 'GO' state.
    tc_limits : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = Thermocouple 'GO' state.
    lc_limits : int numpy array
            [0, 0, 0] = Load Cell 'GO' state.
    ls_limits : int array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = Limit Switch 'GO' state.

    Returns
    -------
    sensor_state : int
         0 = System sensor 'GO', 1 = 'NOGO' system sensor state.

    args[0] = ptl
    args[1] = tcl
    args[2] = lcl
    args[3] = lsl
    args[4] = pt_data
    args[5] = tc_data
    args[6] = lc_data
    args[7] = ls_data
    """
    """
    pt_lower_limits, pt_upper_limits, tc_lower_limits, tc_upper_limits, lc_lower_limits, lc_upper_limits, ls_limits = getSensorLimits(args[0], args[1], args[2],args[3])

    pt = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(pt_lower_limits, args[4], pt_upper_limits))
    tc = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(tc_lower_limits, args[5], tc_upper_limits))
    lc = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(lc_lower_limits, args[6], lc_upper_limits))
    ls = list(INACTIVE if i[0] == i[1] else ACTIVE for i in zip(args[7], ls_limits))

    return setAllSensorStatus(args[0], args[1], args[2], args[3], pt, tc, lc, ls)
    """"""
    pt_lower_limits, pt_upper_limits, tc_lower_limits, tc_upper_limits, lc_lower_limits, lc_upper_limits = getSensorLimits(args[0], args[1], args[2])
    pt = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(pt_lower_limits, args[3], pt_upper_limits))
    tc = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(tc_lower_limits, args[4], tc_upper_limits))
    lc = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(lc_lower_limits, args[5], lc_upper_limits))
    """
    pt = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(getAllPTLowerLimits(), getAllPTValues(), getAllPTUpperLimits()))
    tc = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(getAllTCLowerLimits(), getAllTCValues(), getAllTCUpperLimits()))
    lc = list(INACTIVE if i[0] < i[1] < i[2] else ACTIVE for i in zip(getAllLCLowerLimits(), getAllLCValues(), getAllLCUpperLimits()))
    ls = list(INACTIVE if i[0] < i[1] else ACTIVE for i in zip(getAllLSValues(), getAllLSLimits()))
    return setAllSensorStatus(pt, tc, lc, ls)


def checkAbortNotifications(TimeStamp):
    """Updates Alert_String if a System Abort was triggered this cycle.
        
        If nanny is on AND abort was tripped, then update message.
        If nanny is on AND abort hasn't been tripped, then reset notification.
        Otherwise keep the notification the same. This allows a system abort 
        message to stay active on the LabVIEW user display panel until nanny 
        is reinitiated. 

        ----------
        Function Input:

        TimeStamp - current time of day

        """
    if (getNanny() == ACTIVE and getAbortTripped() == ACTIVE):      # An Abort was tripped this execution
        checkAbortTriggers(TimeStamp)                                   # Update message
    elif (getNanny() == ACTIVE and getAbortTripped() == INACTIVE):  # Nanny is on and no abort
        setAbortString('No Alerts','')                                  # Set default message


def checkAbortTriggers(TimeStamp):
    """
    args[0] = ptl
    args[1] = tcl
    args[2] = lcl
    args[3] = lsl
    args[4] = abt
    args[5] = string array
    args[6] = time stamp
    """
    pt_status,  tc_status,  lc_status, ls_status = getAllSensorStatus()
    pt_names,  tc_names,  lc_names, ls_names = getAllSensorNames()
    if ((sum(pt_status) == 0) and (sum(tc_status) == 0) and (sum(lc_status) == 0)):
        message = 'Manual Abort Tripped at ' + TimeStamp
        setAbortString(message, '')
    else:
        if sum(pt_status) != 0:
            pt_message = 'Pressure Transducers:\n'
            for i in range(len(pt_status)):
                if pt_status[i] == 1:
                    pt_message = pt_message + pt_names[i] + ', '
            pt_message = pt_message + '\n'
        else:
            pt_message = ''
        if sum(tc_status) != 0:
            tc_message = 'Thermocouples:\n'
            for i in range(len(tc_status)):
                if tc_status[i] == 1:
                    tc_message = tc_message + tc_names[i] + ', '
            tc_message = tc_message + '\n'
        else:
            tc_message = ''
        if sum(lc_status) != 0:
            lc_message = 'Load Cells:\n'
            for i in range(len(lc_status)):
                if lc_status[i] == 1:
                    lc_message = lc_message + lc_names[i] + ', '
            lc_message = lc_message + '\n'
        else:
            lc_message = ''
        message = 'System Abort Tripped at ' + TimeStamp
        sensor_message = pt_message + tc_message + lc_message
        setAbortString(message, sensor_message)
    setAbortTripped(SAFE)


def secureValveStates():
    """Access protected class data to evaluate and monitor all 11 of the system actuated valve
       states. The numpy data structure representation is a 1 by 11 integer numpy array. This
       approach is a secure method to access saved valve system state values. A valve state value
       equal to 0 represents valve 'SAFE' orientation.

    Parameters
    ----------
    valve_states : int array
        Values for valve state range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    abort_state : int
        Values for abort state range from 0 for 'System Performance Nominal' to 1 for 'Abort'.
    checkAbort : int
        Nested Function checks if a system abort has been tripped.

    Returns
    -------
    valve_states : int numpy array
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

    args[0] = vst
    args[1] = ist
    args[2] = abt
    args[3] = gst
    """
    checkAbort()
    return getAllVLVStates()


def secureIgniterState():
    """Access protected class data to evaluate and monitor the system igniter states. The returned
       value representation is an integer ranging from 0 to 1. This approach is a secure method to
       access saved system Igniter State values. The method calls two nested functions.

    Parameters
    ----------
    valve_states : int numpy array
        Values for valve state range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    igniter_state : int
        Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
    abort_state : int
        Values for abort state range from 0 for 'System Performance Nominal' to 1 for 'Abort'.
    go_state : int numpy array
        Values for go state range from 0 for 'NOGO' to 1 for 'GO'.
    checkGo : int
        Nested Function checks if all systems are 'GO' for startup sequence.
    checkAbort : int
        Nested Function checks if a system abort has been tripped.

    Returns
    -------
    igniter_state : int
         0 = 'SAFE' system Igniter State, 1 = 'ACTIVE' system Igniter State.

    args[0] = vst
    args[1] = ist
    args[2] = abt
    args[3] = gst
    """

    if getIgniterTest() == ACTIVE: # 'Igniter Test' button IS selected
        setVLVState('ABV-OX-240', CLOSE)
        setVLVState('ABV-FU-340', CLOSE)
        setIGNState(ACTIVE)
        checkAbort()
    else: # 'Igniter Test' button IS NOT selected
        checkGo()
        checkAbort()
    return getIGNState()
