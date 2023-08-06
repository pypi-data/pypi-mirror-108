#!/usr/bin/env python3

###################### Sensor_Test ###############################
# Python Script that is used to test python class modules for
# sensors and ensures the functions are working.
######################################################################

# Python Imports
import numpy as np

# Local Imports
# from sensors import assignPTValues
# from core.sensors import assignPTValues
# from PyIGN.core.sensor import sensors
from pyign.base.sensors import (assignPTValues, assignTCValues, assignSNSCalc, assignLCValues, getPTValue, getAllPTStatus, getAllTCStatus,
                        assignLSValues, getAllLCStatus, getAllLSStatus, getAllPTNames, getAllTCNames, getAllLCNames, getAllLSNames,
                        getAllPTLowerLimits, getAllPTUpperLimits, getAllTCLowerLimits, getAllTCUpperLimits, getAllLCLowerLimits,
                        getAllLCUpperLimits, setAllPTStatus, setAllTCStatus, setAllLCStatus, setAllLSStatus, getAllPTValues, 
                        getAllTCValues, getAllLCValues, getAllLSValues, getAllLSLimits, getAllLS, getPTIndex)


if __name__ == '__main__':
    print("\nBegin Pressure Trandsucer Sensor Test ... \n")
    print("List of PT Sensors: ", getAllPTNames())
    print('')
    ptInput = [2000, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170]
    assignPTValues(ptInput)
    print("Assigned PT Values: ", ptInput)
    print("Actual PT Values: ", getAllPTValues())
    print(" PT-PR-110 Value Expected: ", ptInput[getPTIndex('PT-PR-110')])
    print(" PT-PR-110 Value Returned: ", getPTValue('PT-PR-110'))
    print(" PT-FU-311 Value Expected: ", ptInput[getPTIndex('PT-FU-311')])
    print(" PT-FU-311 Value Returned: ", getPTValue('PT-FU-311'))