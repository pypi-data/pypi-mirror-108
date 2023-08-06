############################# __PyIGN__ ##############################
# Main Module that takes in telematry input matrix, parses the
#  data and returns the new data to be output to the hardware.
######################################################################

# Python Imports
import numpy as np

# Local Imports
from pyign.manifest._built_in_ import *

from pyign.manifest._engine_config_ import *

from pyign.core.ehms_core import (secureValveStates, secureIgniterState, assignAllSNSCalc, 
                          checkNannyLimits, checkGo, checkAbort, checkSensors,checkSequence, 
                          assignAllReadBack, checkAbortTriggers, 
                          checkAbortNotifications, checkAutoSequence)
from pyign.core.auto_core import (commence_fu_cold_flow, commence_cryo_cold_flow, commence_hotfire, commence_ox_vent, 
                          commence_fuel_vent, commence_system_cycle, commence_purge_1, commence_purge_2, 
                          commence_valve_firing_sim, commence_leak_check, commence_cryo_fill, commence_igniter_checkout)
from pyign.base.states import (assignAbortState, assignNanny, assignAllGOStates, getReadBack, getAbortState, getNanny, getAllGOStates, 
                       getSeqState, getSeqFlowMeter, getSeqActive, getArmActive, setArmActive, setSeqState, setSeq,
                       setIgniterTest, getIgniterTest, getIgniterArm, getAbortTripped)
from pyign.base.valves import (getAllVLVStates, getVLVState, assignAllVLVStates, setVLVState, assignIGNState, initValveState)
from pyign.base.sensors import (getPTStatus, getTCStatus, getLCStatus, setAllPTStatus, setAllTCStatus, assignLSValues,
                        setAllLCStatus,assignPTValues, assignTCValues, assignLCValues)
from pyign.core.bedrock_core import (bed_rock_down, bed_rock_up)
from pyign.core.notification_core import (getAbortString)

# from _built_in_ import *

# from _engine_config_ import *

# from ehms_core import (secureValveStates, secureIgniterState, assignAllSNSCalc, 
#                      checkNannyLimits, checkGo, checkAbort, checkSensors,checkSequence, 
#                      assignAllReadBack, checkAbortTriggers, 
#                      checkAbortNotifications, checkAutoSequence)
# from auto_core import (commence_fu_cold_flow, commence_cryo_cold_flow, commence_hotfire, commence_ox_vent, 
#                      commence_fuel_vent, commence_system_cycle, commence_purge_1, commence_purge_2, 
#                      commence_valve_firing_sim, commence_leak_check, commence_cryo_fill, commence_igniter_checkout)
# from states import (assignAbortState, assignNanny, assignAllGOStates, getReadBack, getAbortState, getNanny, getAllGOStates, 
#                   getSeqState, getSeqFlowMeter, getSeqActive, getArmActive, setArmActive, setSeqState, setSeq,
#                   setIgniterTest, getIgniterTest, getIgniterArm, getAbortTripped)
# from valves import (getAllVLVStates, getVLVState, assignAllVLVStates, setVLVState, assignIGNState, initValveState)
# from sensors import (getPTStatus, getTCStatus, getLCStatus, setAllPTStatus, setAllTCStatus, assignLSValues,
#                    setAllLCStatus,assignPTValues, assignTCValues, assignLCValues)
# from bedrock_core import (bed_rock_down, bed_rock_up)
# from notification_core import (getAbortString)

# def readControlArray():
def getLabviewArray():
    checkAbort()
    labview_array = [0]*58
    labview_array[0] = getAbortState()
    labview_array[1] = getNanny()
    labview_array[2] = secureIgniterState()
    labview_array[19:27] = getAllGOStates()
    labview_array[3:16] = secureValveStates()
    labview_array[16] = getSeqState()
    labview_array[17] = getSeqFlowMeter()
    labview_array[18] = getSeqActive()
    labview_array[27] = getReadBack('abort tripped')
    labview_array[28] = getReadBack('igniter tripped')
    labview_array[29] = getArmActive()
    labview_cluster = (labview_array, getAbortString())
    return labview_cluster

#def PyIGN(Input_Matrix, Global_Time):
def PyIGN_LabVIEW(Input_Matrix, Global_Time):
    initValveState()
    timer_input = np.zeros(1)
    input = np.zeros((16, 19), dtype=np.int32)

    timer_input = np.array(Input_Matrix[2][1], dtype=np.float32)
    input = np.array(Input_Matrix, dtype=np.int32)
    idx = np.array(input[:,0] + 1, dtype=np.int32)

    setSeqState('sequence active')
    assignAbortState(input[0,1]) #Set Abort
    assignNanny(input[4,1]) #Set Nanny
    assignAllGOStates(input[4,2:idx[4]]) #Set Go States
    assignIGNState(input[0,3]) #Set Igniter
    setArmActive(input[11,1]) #Set Igniter Arm 
    setIgniterTest(input[5,8]) #Set Ingiter Test
    assignAllVLVStates(input[3,1:idx[3]]) #Set All Valves

    assignAllReadBack(input[9,1:idx[9]], input[10,1:idx[10]]) #Set All ReadBack
    assignPTValues(input[12,1:idx[12]])
    assignTCValues(input[13,1:idx[13]])
    assignLCValues(input[14,1:idx[14]])
    assignLSValues(input[15,1:idx[15]])
    assignAllSNSCalc()

    checkSensors()
    checkAbort()
    checkAutoSequence()

    if input[5,2] == ACTIVE: #Startup Button
        commence_hotfire(timer_input) #Check Hotfire
    elif input[5,1] == ACTIVE: #Cold Flow Button
        if input[11,4] == ACTIVE: #Cryo Button
            commence_cryo_cold_flow(timer_input, input[11,3]) #Check Cold Flow
        elif input[11,4] == INACTIVE: #Fuel Button
            commence_fu_cold_flow(timer_input, input[11,3]) #Check Cold 
    elif input[5,3] == ACTIVE: #Cycle Ox Vent 
        commence_ox_vent(timer_input) #Check Ox Vent Cycle
    elif input[5,4] == ACTIVE: #Cycle Fuel Vent
        commence_fuel_vent(timer_input) #Check Fuel Vent Cycle
    elif input[5,6] == ACTIVE: #Purge 1 (sec)
        commence_purge_1(timer_input) #Check One Second Purge
    elif input[5,7] == ACTIVE: #Purge 2 (sec)
        commence_purge_2(timer_input) #Check Two Second Purge
    elif input[5,5] == ACTIVE: #Cycle System
        commence_system_cycle(timer_input) #Check System Cycle
    elif input[10,2] == ACTIVE: #Igniter Tripped
        pass
    elif input[5,9] == ACTIVE: #Valve Firing Sim
        commence_valve_firing_sim(timer_input) #Check Valve Firing Sim

    if input[7,1] or input[7,2] == ACTIVE:
        if input[7,1] == ACTIVE: #Ox Leak Check
            commence_leak_check('ABV-PR-110', 'PT-OX-CLC-215')
        if input[7,2] == ACTIVE: #Fuel Leak Check
            commence_leak_check('ABV-PR-120', 'PT-FU-CLC-315')
    elif input[7,3] == ACTIVE:
        if getReadBack('dewar level tripped') == ACTIVE:
            setVLVState('ABV-OX-230', CLOSE)
        else:
            commence_cryo_fill()

        # IGNITER CHECKOUT TESTING #
    if (getIgniterTest() == ACTIVE) and (getIgniterArm('arm ACTIVE') == ACTIVE): # Igniter Test Button & Igniter is Armed
        commence_igniter_checkout(timer_input)
    elif (getIgniterTest() == ACTIVE) and (getIgniterArm('arm ACTIVE') != ACTIVE):
        setIgniterTest(INACTIVE)
        setSeq('igniter active')


    checkNannyLimits() #Check Limits
    checkAbortNotifications(Global_Time)
    return getLabviewArray()
    #return readControlArray()


def Nanny_Alerts():
    return getAbortString()

