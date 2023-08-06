########################### _PyIGN_Test_Bedrock ######################
# Python Script that is used to test PyIGN modules.
# This script tests Bedrock functuality.
######################################################################

# Python Imports
import numpy as np

# Local Imports
from pyign.__PyIGN__ import (getLabviewArray, PyIGN_LabVIEW, Nanny_Alerts)

from pyign.base.sensors import (assignPTValues, assignTCValues, assignSNSCalc, assignLCValues, getPTValue, getAllPTStatus, getAllTCStatus,
                                assignLSValues, getAllLCStatus, getAllLSStatus, getAllPTNames, getAllTCNames, getAllLCNames, getAllLSNames,
                                getAllPTLowerLimits, getAllPTUpperLimits, getAllTCLowerLimits, getAllTCUpperLimits, getAllLCLowerLimits,
                                getAllLCUpperLimits, setAllPTStatus, setAllTCStatus, setAllLCStatus, setAllLSStatus, getAllPTValues, 
                                getAllTCValues, getAllLCValues, getAllLSValues, getAllLSLimits, getAllLS, getPTIndex)
# from pyign.base.states import (setAllReadBackStates, setAllReadBackResets, getNanny, setAbortState, setAbortTripped, getAllGOStates,
#                                getSeqState, setSeqState, getAbortTripped, getIgniterTest, getIgniterArm, getAbortState, assignAllGOStates, 
#                                setSeq)

if __name__ == '__main__':
    print("\nBegin Main Test ... \n")
    
    """
    Input is a 16 x 17 matrix that is imported from LabVIEW.
    Values are manually input using the data_pass0 matrix to 
    simulate these values for testing python functionality.
    """

######## Bedrock Testing ######
data_pass0 = [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0 Abort/Ist
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1 Phase
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2 Timer
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3 Valve St
            [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4 Nanny/GO's
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4 Sequence
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #6 NONE
            [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7 Bedrock
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #8 NONE
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9 NONE
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #10 Loops
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #11 Signals
            [15, 200, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 0, 0, 0, 0], #12 PT
            [18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13 TC
            [3, 30, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #14 LC
            [13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #15 LS


Global_Time = '12:30:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Bedrock Test 1: Bang up Ox Side (Increase Pressure)")
print(" PT Input Value: ", data_pass0[12][4])
print(" Input Valve States: ", data_pass0[3][1:13])
print(" Expected Abort State : 0, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 1, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
print(" Returned Valve States:", new_data[3:16])
print('')
print(notification[0])
print(notification[1])

data_pass0[0][1] = new_data[0] #Abort state
data_pass0[4][1] = new_data[1] #Nanny state
print(data_pass0)
data_pass0[3][1] = new_data[3]
data_pass0[12][4] = 190

Global_Time = '12:32:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Bedrock Test 2: Bang up Ox Side (Do Nothing)")
print(" PT Input Value: ", data_pass0[12][4])
print(" Input Valve States: ", data_pass0[3][1:13])
print(" Expected Abort State : 0, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 1, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
print(" Returned Valve States:", new_data[3:16])
print('')
print(notification[0])
print(notification[1])

data_pass0[0][1] = 0 #Abort state
data_pass0[4][1] = new_data[1] #Nanny state
data_pass0[3][1] = new_data[3]
data_pass0[12][4] = 201
data_pass0[12][6] = 210

Global_Time = '12:33:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Bedrock Test 3: Bang up Ox Side (Above Target)")
print(" PT Input Value: ", data_pass0[12][4], " and ", data_pass0[12][6])
print(" Input Valve States: ", data_pass0[3][1:13])
print(" Expected Abort State : 0, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 1, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
print(" Returned Valve States:", new_data[3:16])
print('')
print(notification[0])
print(notification[1])


### FUEL SIDE ###
data_pass0 = [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1 Phase
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2 Timer
            [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3 Valve St
            [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4 Nanny/GO's
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4 Sequence
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #6 NONE
            [3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7 Bedrock
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #8 NONE
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9 NONE
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #10 Loops
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #11 Signals
            [15, 200, 700, 700, 700, 100, 700, 100, 700, 700, 700, 700, 700, 300, 300, 0, 0, 0, 0], #12 PT
            [18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13 TC
            [3, 30, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #14 LC
            [13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #15 LS

Global_Time = '12:40:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Bedrock Test 1: Bang up Fuel Side (Increase Pressure)")
print(" PT Input Value: ", data_pass0[12][5])
print(" Input Valve States: ", data_pass0[3][1:13])
print(" Expected Abort State : 0, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 1, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
print(" Returned Valve States:", new_data[3:16])
print('')
print(notification[0])
print(notification[1])

data_pass0[0][1] = new_data[0] #Abort state
data_pass0[4][1] = new_data[1] #Nanny state
data_pass0[3][2] = new_data[4]
data_pass0[12][5] = 195
data_pass0[12][7] = 197

Global_Time = '12:41:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Bedrock Test 2: Bang up Fuel Side (Do Nothing)")
print(" PT Input Value: ", data_pass0[12][5], " and ", data_pass0[12][7])
print(" Input Valve States: ", data_pass0[3][1:13])
print(" Expected Abort State : 0, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 1, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
print(" Returned Valve States:", new_data[3:16])
print('')
print(notification[0])
print(notification[1])

data_pass0[0][1] = new_data[0] #Abort state
data_pass0[4][1] = new_data[1] #Nanny state
data_pass0[3][2] = new_data[4]
data_pass0[12][5] = 201
data_pass0[12][7] = 201

Global_Time = '12:42:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Bedrock Test 3: Bang up Fuel Side (Above Target, Close Valve)")
print(" PT Input Value: ", data_pass0[12][5], " and ", data_pass0[12][7])
print(" Input Valve States: ", data_pass0[3][1:13])
print(" Expected Abort State : 0, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 1, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
print(" Returned Valve States:", new_data[3:16])
print('')
print(notification[0])
print(notification[1])


print("\n ... End Main Test \n")
