#################### _PyIGN_Test_Notifications ##########################
# Python Script that is used to test PyIGN modules.
# This script tests Abort notification output.
# It uses a manual input matrix and calls the PyIGN functions.
# Returns the expected and returned values for testing the notifications
#########################################################################

# Python Imports
import numpy as np

# Local Imports
from pyign.__PyIGN__ import (getLabviewArray, PyIGN_LabVIEW, Nanny_Alerts)

from pyign.base.sensors import (assignPTValues, assignTCValues, assignSNSCalc, assignLCValues, getPTValue, getAllPTStatus, getAllTCStatus,
                        assignLSValues, getAllLCStatus, getAllLSStatus, getAllPTNames, getAllTCNames, getAllLCNames, getAllLSNames,
                        getAllPTLowerLimits, getAllPTUpperLimits, getAllTCLowerLimits, getAllTCUpperLimits, getAllLCLowerLimits,
                        getAllLCUpperLimits, setAllPTStatus, setAllTCStatus, setAllLCStatus, setAllLSStatus, getAllPTValues, 
                        getAllTCValues, getAllLCValues, getAllLSValues, getAllLSLimits, getAllLS, getPTIndex)



if __name__ == '__main__':
    print("\nBegin Main Notification Test ... \n")
    
    """
    Input is a 16 x 17 matrix that is imported from LabVIEW.
    Values are manually input using the data_pass0 matrix to 
    simulate these values for testing python functionality.
    """

### Notification ###

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
            [15, 2000, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 0, 0, 0, 0], #12 PT
            [18, 0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13 TC
            [3, 30, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #14 LC
            [13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #15 LS

Global_Time = '12:30:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Nanny is on, Sensors are within bounds")
print(" Expected Abort State : 0, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 1, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: ", data_pass0[3][1:13])
print(" Returned Valve States:", new_data[3:16])
print(" Expected Nanny Alert:")
print("No Alerts")
print(" Returned Nanny Alert:")
print(notification[0])
print(notification[1])
print('')


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
            [15, 200000, 700, 700, 700, 100, 700, 100, 700, 700, 700, 700, 700, 700, 700, 0, 0, 0, 0], #12 PT
            [18, 0, 2000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13 TC
            [3, 30, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #14 LC
            [13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #15 LS

Global_Time = '12:45:60'
(new_data, notification) = PyIGN_LabVIEW(data_pass0,Global_Time)
print()
print(" Notification System Tripped Abort")
print(" Expected Abort State : 1, Returned Abort State: ", new_data[0])
print(" Expected Returned Nanny State: 0, Returned Nanny State: ", new_data[1])
print(" Expected Valve States: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
print(" Returned Valve States:", new_data[3:16])
print(" Expected Nanny Alert:")
print("System Abort Tripped at ", Global_Time)
print("Pressure Transducers:")
print("PT-PR-110, PT-PR-140,")
print("Thermocouples:")
print("TC-OX-210,")
print('')
print(" Returned Nanny Alert:")
print(notification[0])
print(notification[1])
print('')


print("\n ... End Main Test \n")
    