########################### sensors ##################################
# This module holds the class instances representing the physical
# sensors read in by DAQmx on the test stand.
######################################################################
from pyign.base._base_class_ import PTSensor, TCSensor, LCSensor, LSSensor, CLCSensor


class PTLimits(PTSensor):
    """The PTLimits Class contains the pressure transducer class instances.
        
        Each sensor is slated into the system which creates an object of its
        parent class and adds the object to a dynamic list.
        The upper and lower limits designate the safe operating limits for
        the stand within those bounds.
        
        ----------
        Sensor Parameters:

        Name - The Name follows the P&ID format

        Lower Limit - The minimum value the sensor reads to still be considered safe.

        Upper Limit - The max value the sensor reads to still be considered safe.

        Status - A status flag '1' if the sensor is outside of its bounds, '0' if its within. Default = 0

        Value - The current value of the sensor assigned by DAQmx, Default = 0

        ----------
        Returned Parameters:

        Sensor Object

        Array of Sensor Objects

        """

    pt_110 = PTSensor.slate('PT-PR-110', -500, 3200)        #PT-PR-110 K-Bottle
    pt_120 = PTSensor.slate('PT-PR-120', -500, 1300)        #PT-PR-120 Fuel Regulator
    pt_130 = PTSensor.slate('PT-PR-130', -500, 1300)        #PT-PR-130 LOx Regulator
    pt_210 = PTSensor.slate('PT-OX-210', -500, 1050)        #PT-OX-210 LOx Tank
    pt_310 = PTSensor.slate('PT-FU-310', -500, 1050)        #PT-FU-310 Fuel Tank
    pt_211 = PTSensor.slate('PT-OX-211', -500, 1050)        #PT-OX-211 Ox Pressure Vent
    pt_311 = PTSensor.slate('PT-FU-311', -500, 1050)        #PT-FU-311 Fuel Pressure Vent
    pt_220 = PTSensor.slate('PT-OX-220', -500, 1500)        #PT-OX-220 LOx Main Line (Pre Flex)
    pt_320 = PTSensor.slate('PT-FU-320', -500, 1500)        #PT-FU-320 Fuel Main Line (Pre Flex)
    pt_230 = PTSensor.slate('PT-OX-230', -500, 1500)        #PT-OX-230 LOx Main (Post Flex)
    pt_330 = PTSensor.slate('PT-FU-330', -500, 1500)        #PT-FU-330 Fuel Main (Post Flex)
    pt_410 = PTSensor.slate('PT-CC-410', -500, 2200)        #PT-CC-410 Combustion Chamber
    pt_140 = PTSensor.slate('PT-PR-140', -500, 500)         #PT-PR-140 Actuator Pnuematic
    pt_240 = PTSensor.slate('PT-OX-240', -50000, 50000)     #PT-OX-240 LOx Dewer Outlet
    pt_420 = PTSensor.slate('PT-CC-420', -500, 2200)        #PT-CC-420 Combustion Chamber Outlet
    # These sensors are currently not being used in the stand #
    #pt_510 = Sensor('PT-RN-510', 0, 0, 0, 1000)        #PT-RN-510 Flow Regen Inlet
    #pt_520 = Sensor('PT-RN-520', 0, 0, 0, 1000)        #PT-RN-520 Flow Regen Outlet

def getAllPTs(self = PTLimits):
    """Returns the array of objects instanciated in the Pressure transducer class"""
    return self.pt_list

def getAllPTNames(self = PTLimits):
    """Returns an array of names for each object instance in the Pressure transducer class"""
    return self.pt_names

def getAllPTLowerLimits(self = PTLimits):
    """Returns an array of lower limit value for each object instance in the Pressure transducer class"""
    return self.pt_lower_limits

def getAllPTUpperLimits(self = PTLimits):
    """Returns an array of upper limit value for each object instance in the Pressure transducer class"""
    return self.pt_upper_limits

def getAllPTStatus(self = PTLimits):
    """Returns an array of status flag for each object instance in the Pressure transducer class"""
    status = [x.status for x in self.pt_list]
    return status

def getAllPTValues(self = PTLimits):
    """Returns an array of sensor value for each object instance in the Pressure transducer class"""
    values = [x.value for x in self.pt_list]
    return values

def getPTStatus(string, self = PTLimits):
    """Returns pressure transducer status flag for the object named in the string parameter"""
    string = string.upper()
    for x in self.pt_list:
        if string == x.name:
            single_pt = x.status
            break
    return single_pt

def getPTValue(string, self = PTLimits):
    """Returns pressure transducer current value for the object named in the string parameter"""
    string = string.upper()
    for x in self.pt_list:
        if string == x.name:
            single_pt = x.value
            break
    return single_pt

def getPTIndex(string, self = PTLimits):
    """Return the pressure transducer position in the object array, specified by the string parameter"""
    string = string.upper()
    i = 0
    for x in self.pt_list:
        if string == x.name:
            idx = i
            break
        i += 1
    return idx

def assignPTValues(array, self = PTLimits):
    """Assign is used by input matrix to assign each sensors current value as read by DAQmx"""
    i = 0
    for x in self.pt_list:
        x.value = array[i]
        i += 1
    return self

def setAllPTStatus(array, self = PTLimits):
    """Set is used by Nanny/EHMS to set the status flag of each sensor"""
    i = 0
    for x in self.pt_list:
        x.status = array[i]
        i += 1
    return self


class TCLimits(TCSensor):
    """ The TCLimits Class contains the thermocouple class instances.
        
        Each sensor is slated into the system which creates an object of its
        parent class and adds the object to a dynamic list.
        The upper and lower limits designate the safe operating limits for
        the stand within those bounds.
        
        ----------
        Sensor Parameters:

        Name - The Name follows the P&ID format

        Lower Limit - The minimum value the sensor reads to still be considered safe.

        Upper Limit - The max value the sensor reads to still be considered safe.

        Status - A status flag '1' if the sensor is outside of its bounds, '0' if its within. Default = 0

        Value - The current value of the sensor assigned by DAQmx, Default = 0

        ----------
        Returned Parameters:

        Sensor Object

        Array of Sensor Objects

        """
    tc_110 = TCSensor.slate('TC-PR-110', -4000, 5000)     #TC-PR-110 Press Bottle (K)
    tc_210 = TCSensor.slate('TC-OX-210', -4000, 5000)     #TC-OX-210 Ox Tank Relief (T)
    tc_310 = TCSensor.slate('TC-FU-310', -4000, 5000)     #TC-FU-310 Fuel Tank Relief (T)
    tc_220 = TCSensor.slate('TC-OX-220', -4000, 5000)     #TC-OX-220 Ox Tank (1/4) (T)
    tc_221 = TCSensor.slate('TC-OX-221', -4000, 5000)     #TC-OX-221 Ox Tank (2/4) (T)
    tc_222 = TCSensor.slate('TC-OX-222', -4000, 5000)     #TC-OX-222 Ox Tank (3/4) (T)
    tc_223 = TCSensor.slate('TC-OX-223', -4000, 5000)     #TC-OX-223 Ox Tank (4/4) (T)
    tc_320 = TCSensor.slate('TC-FU-320', -4000, 5000)     #TC-FU-320 Fuel Tank (K)
    tc_230 = TCSensor.slate('TC-OX-230', -4000, 5000)     #TC-OX-230 Ox Main (Pre Venturi) (T)
    tc_330 = TCSensor.slate('TC-FU-330', -4000, 5000)     #TC-FU-330 Fuel Main (Pre Venturi) (T)
    tc_240 = TCSensor.slate('TC-OX-240', -4000, 5000)     #TC-OX-240 Ox Main Relief (T)
    tc_250 = TCSensor.slate('TC-OX-250', -4000, 5000)     #TC-OX-250 Ox Chill (K)
    tc_260 = TCSensor.slate('TC-OX-260', -4000, 5000)     #TC-OX-260 Ox Main Injector (T)
    tc_410 = TCSensor.slate('TC-CC-410', -4000, 5000)     #TC-CC-410 Combustion Chamber (1/3) (K)
    tc_411 = TCSensor.slate('TC-CC-411', -4000, 5000)     #TC-CC-411 Combustion Chamber (2/3) (K)
    tc_412 = TCSensor.slate('TC-CC-412', -4000, 5000)     #TC-CC-412 Combustion Chamber (3/3) (K)
    tc_520 = TCSensor.slate('TC-RN-520', -5000, 5000)    #TC-RN-520 Regen (K)
    tc_530 = TCSensor.slate('TC-RN-530', -5000, 5000)    #TC-RN-530 Regen (K)

def getAllTCNames(self = TCLimits):
    """Returns an array of names for each object instance in the thermocouple class"""
    return self.tc_names

def getAllTCLowerLimits(self = TCLimits):
    """Returns an array of lower limit value for each object instance in the thermocouple class"""
    return self.tc_lower_limits

def getAllTCUpperLimits(self = TCLimits):
    """Returns an array of upper limit value for each object instance in the thermocouple class"""
    return self.tc_upper_limits

def getAllTCStatus(self = TCLimits):
    """Returns an array of status flag for each object instance in the thermocouple class"""
    status = [x.status for x in self.tc_list]
    return status

def getAllTCValues(self = TCLimits):
    """Returns an array of sensor value for each object instance in the Thermocouple class"""
    values = [x.value for x in self.tc_list]
    return values


def getTCStatus(string, self = TCLimits):
    """Returns thermocouple status flag for the object named in the string parameter"""
    string = string.upper()
    for x in self.tc_list:
        if string == x.name:
            single_tc = x.status
            break
    return single_tc

def getTCValue(string, self = TCLimits):
    """Returns thermocouple current value for the object named in the string parameter"""
    string = string.upper()
    for x in self.tc_list:
        if string == x.name:
            single_tc = x.value
            break

def assignTCValues(array, self = TCLimits):
    """Assign is used by input matrix to assign each sensors current value as read by DAQmx"""
    i = 0
    for x in self.tc_list:
        x.value = array[i]
        i += 1
    return self

def setAllTCStatus(array, self = TCLimits):
    """Set is used by Nanny/EHMS to set the status flag of each sensor"""
    i = 0
    for x in self.tc_list:
        x.status = array[i]
        i += 1
    return self

    # for x in self.tc_list[:]:
    #     x.status = array[x]
    # return self

    # for i, x in enumerate(self.tc_list):
    #     x.status = array[i]
    # return self


class LCLimits(LCSensor):
    """ The LCLimits Class contains the Load Cell class instances.
        
        Each sensor is slated into the system which creates an object of its
        parent class and adds the object to a dynamic list.
        The upper and lower limits designate the safe operating limits for
        the stand within those bounds.
        
        ----------
        Sensor Parameters:

        Name - The Name follows the P&ID format

        Lower Limit - The minimum value the sensor reads to still be considered safe.

        Upper Limit - The max value the sensor reads to still be considered safe.

        Status - A status flag '1' if the sensor is outside of its bounds, '0' if its within. Default = 0

        Value - The current value of the sensor assigned by DAQmx, Default = 0

        ----------
        Returned Parameters:

        Sensor Object

        Array of Sensor Objects

        """

    lc_210 = LCSensor.slate('LC-OX-210', -20000, 10000)    #LC-OX-210 Ox Tank
    lc_310 = LCSensor.slate('LC-FU-310', -20000, 10000)    #LC-FU-310 Fuel Tank
    lc_410 = LCSensor.slate('LC-CC-410', -20000, 10000)    #LC-CC-410 Combustion Chamber


def getAllLCNames(self = LCLimits):
    """Returns an array of names for each object instance in the load cell class"""
    return self.lc_names

def getAllLCLowerLimits(self = LCLimits):
    """Returns an array of lower limit value for each object instance in the load cell class"""
    return self.lc_lower_limits

def getAllLCUpperLimits(self = LCLimits):
    """Returns an array of upper limit value for each object instance in the load cell class"""
    return self.lc_upper_limits

def getAllLCStatus(self = LCLimits):
    """Returns an array of status flag for each object instance in the load cell class"""
    status = [x.status for x in self.lc_list]
    return status

def getAllLCValues(self = LCLimits):
    """Returns an array of sensor value for each object instance in the Load Cell class"""
    values = [x.value for x in self.lc_list]
    return values

def getLCStatus(string, self = LCLimits):
    """Returns load cell status flag for the object named in the string parameter"""
    string = string.upper()
    for x in self.lc_list:
        if string == x.name:
            single_lc = x.status
            break
    return single_lc

def getLCValue(string, self = LCLimits):
    """Returns load cell current value for the object named in the string parameter"""
    string = string.upper()
    for x in self.lc_list:
        if string == x.name:
            single_lc = x.value
            break
    return single_lc

def assignLCValues(array, self = LCLimits):
    """Assign is used by input matrix to assign each sensors current value as read by DAQmx"""
    i = 0
    for x in self.lc_list:
        x.value = array[i]
        i += 1
    return self

def setAllLCStatus(array, self = LCLimits):
    """Set is used by Nanny/EHMS to set the status flag of each sensor"""
    i = 0
    for x in self.lc_list:
        x.status = array[i]
        i += 1
    return self

class LSLimits(LSSensor):
    """ The LSLimits Class contains the Limit Switch class instances.
        
        Each sensor is slated into the system which creates an object of its
        parent class and adds the object to a dynamic list.
        The upper and lower limits designate the safe operating limits for
        the stand within those bounds.
        
        ----------
        Sensor Parameters:

        Name - The Name follows the P&ID format

        Limit - The max value the sensor reads to still be considered safe. Default = NONE

        Status - A status flag '1' if the sensor is outside of its bounds, '0' if its within. Default = 0

        Value - The current value of the sensor assigned by DAQmx, Default = 0

        ----------
        Returned Parameters:

        Sensor Object

        Array of Sensor Objects

        """   
    ls_110 = LSSensor.slate('LS-PR-110', 10)    #LS-PR-110 Ox Tank Press
    ls_120 = LSSensor.slate('LS-PR-120', 10)    #LS-PR-120 Fuel Tank Press
    ls_210 = LSSensor.slate('LS-OX-210', 10)    #LS-OX-210 Ox Tank Vent
    ls_310 = LSSensor.slate('LS-FU-310', 10)    #LS-FU-310 Fuel Tank Vent
    ls_220 = LSSensor.slate('LS-OX-220', 10)    #LS-OX-220 Ox Isolation
    ls_320 = LSSensor.slate('LS-FU-320', 10)    #LS-FU-320 Fuel Isolation
    ls_230 = LSSensor.slate('LS-OX-230', 10)    #LS-OX-230 Ox Chill
    ls_330 = LSSensor.slate('LS-FU-330', 10)    #LS-FU-330 Fuel Purge
    ls_240 = LSSensor.slate('LS-OX-240', 10)    #LS-OX-240 Ox Main
    ls_340 = LSSensor.slate('LS-FU-340', 10)    #LS-FU-340 Fuel Main
    ls_250 = LSSensor.slate('LS-OX-250', 10)    #LS-OX-250 Ox Fill
    ls_350 = LSSensor.slate('LS-FU-350', 10)    #LS-FU-350 Fuel Manual Fill
    ls_610 = LSSensor.slate('LS-WS-610', 10)    #LS-WS-610 Water Suppression

def getAllLS(self = LSLimits):
    """Returns the array of objects instanciated in the limit switch class"""
    return self.ls_list

def getAllLSNames(self = LSLimits):
    """Returns an array of names for each object instance in the limit switch class"""
    return self.ls_names

def getAllLSStatus(self = LSLimits):
    """Returns an array of status flag for each object instance in the limit switch class"""
    status = [x.status for x in self.ls_list]
    return status

def getAllLSValues(self = LSLimits):
    """Returns an array of sensor value for each object instance in the Limit Switch class"""
    values = [x.value for x in self.ls_list]
    return values

def getAllLSLimits(self = LSLimits):
    """Returns an array of limit value for each object instance in the load cell class"""
    return self.ls_limits

def getLSStatus(string, self = LSLimits):
    """Returns limit switch status flag for the object named in the string parameter"""
    string = string.upper()
    for x in self.ls_list:
        if string == x.name:
            single_ls = x.status
            break
    return single_ls

def getLSValue(string, self = LSLimits):
    """Returns Limit Switch current value for the object named in the string parameter"""
    string = string.upper()
    for x in self.ls_list:
        if string == x.name:
            single_ls = x.value
            break
    return single_ls

def assignLSValues(array, self = LSLimits):
    """Assign is used by input matrix to assign each sensors current value as read by DAQmx"""
    i = 0
    for x in self.ls_list:
        x.value = array[i]
        i += 1
    return self

def setAllLSStatus(array, self = LSLimits):
    """Set is used by Nanny/EHMS to set the status flag of each sensor"""
    i = 0
    for x in self.ls_list:
        x.status = array[i]
        i += 1
    return self


class SNSCalc(CLCSensor):
    """ The SNSCalc Class contains pressure transducer class instances used
        specifically for press control automation.
        
        Each sensor is slated into the system which creates an object of its
        parent class and adds the object to a dynamic list.
        The upper and lower limits designate the safe operating limits for
        the stand within those bounds.
        
        ----------
        Sensor Parameters:

        Name - The Name of the sensor instance

        Lower Limit - The minimum value the sensor reads to still be considered safe. Default = NONE

        Upper Limit - The max value the sensor reads to still be considered safe. Default = NONE

        Status - A status flag '1' if the sensor is outside of its bounds, '0' if its within. Default = 0

        Value - The current value of the sensor assigned by DAQmx, Default = 0

        ----------
        Returned Parameters:

        Sensor Object

        Array of Sensor Objects

        """
    pt_clc_215 = CLCSensor.slate('PT-OX-CLC-215')        #PT-OX-CLC-215 LOx Tank
    pt_clc_315 = CLCSensor.slate('PT-FU-CLC-315')        #PT-FU-CLC-315 Fuel Tank
    pt_clc_dewar = CLCSensor.slate('PT-OX-CLC-DEWAR')    #PT-OX-CLC-DEWAR Dewar Outlet

def getAllCLCNames(self = SNSCalc):
    return self.clc_names

def getAllCLCLowerLimits(self = SNSCalc):
    return self.clc_lower_limits

def getAllCLCUpperLimits(self = SNSCalc):
    return self.clc_upper_limits

def getAllCLCStatus(self = SNSCalc):
    status = [x.status for x in self.clc_list]
    return status

def getAllCLCValues(self = SNSCalc):
    values = [x.value for x in self.clc_list]
    return values

def assignSNSCalc(string, value, self = SNSCalc):
    """Access protected class data to evaluate and monitor all 2 of the systems sensors values.
      The numpy data structure representation is a 1 by 2 integer numpy array. This
      approach is a secure method to access saved SNS state values. A SNS state value equal to 0
      represents valve 'GO' reading.

    Access and reads protected SNS state class data using single integer value. The returned value
    representation is a 1 by 1 integer numpy array.

    Parameters
    ----------
    sns_clc : int numby array
        Values for SNS state value range from 0 for 'GO' to 1 for 'NOGO'.
    sns : str
        Set strings range from '110-410' for each of the test stands sns.

    Returns
    -------
    sns_clc : int numpy array
        [0] = 'clcerage' system sns state.

    args[0] = clc
    args[1] = string value
    """
    string = string.upper()
    if string == 'PT-OX-CLC-215':
        self.pt_clc_215.value = value
    elif string == 'PT-FU-CLC-315':
        self.pt_clc_315.value = value
    elif string == 'PT-OX-CLC-DEWAR':
        self.pt_clc_dewar.value = value
    return self
    
def getSNSCalc(string, self = SNSCalc):
    """Access protected class data to evaluate and monitor all 2 of the systems sensors values.
      The numpy data structure representation is a 1 by 2 integer numpy array. This
      approach is a secure method to access saved SNS state values. A SNS state value equal to 0
      represents valve 'GO' reading.

    Access and reads protected SNS state class data using single integer value. The returned value
    representation is a 1 by 1 integer numpy array.

    Parameters
    ----------
    sns_clc : int numby array
        Values for SNS state value range from 0 for 'GO' to 1 for 'NOGO'.
    sns : str
        Set strings range from '110-410' for each of the test stands sns.

    Returns
    -------
    sns_clc : int numpy array
        [0] = 'clcerage' system sns state.

    args[0] = clc
    args[1] = string value
    """
    string = string.upper()
    if string == 'PT-OX-CLC-215':
        single_sns_clc = self.pt_clc_215.value
    elif string == 'PT-FU-CLC-315':
        single_sns_clc = self.pt_clc_315.value
    elif string == 'PT-OX-CLC-DEWAR':
        single_sns_clc = self.pt_clc_dewar.value
    return single_sns_clc