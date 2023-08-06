########################### bedrock_core ####################
# Bedrock module holds functions implementing a bang-bang 
# feedback controller.
#############################################################
from pyign.manifest._built_in_ import *
from pyign.manifest._engine_config_ import *
from pyign.base.states import (getNanny)
from pyign.base.valves import (setVLVState)

def bed_rock_up(valve_string, sensor_value, target, window):
    """Controls the specified valve to OPEN or CLOSE based on parameters.

        Bang-up closes the valve when the sensor is above target and will
        open the valve when it falls below the target window.

        This function can only be used if Nanny is turned on.

        Parameters
        ----------
        valve_string : name of valve to be controlled
        
        sensor_value : The current sensor reading value

        target : The optimal value that the sensor should be reading

        window : This value is the variance allowed from the target value
   
        Returns
        -------
        Commands the specified Valve to OPEN or CLOSE

        """
    if getNanny() == ACTIVE:
        if sensor_value >= target:
            setVLVState(valve_string, CLOSE)
        elif sensor_value < (target - window):
            setVLVState(valve_string, OPEN)
    return 

def bed_rock_down(valve_string, sensor_value, target, window): 
    """Controls the specified valve to OPEN or CLOSE based on parameters.

        Bang-down opens the valve when the sensor is above target and will
        close the valve when it falls below the target window.

        This function can only be used if Nanny is turned on.

        Parameters
        ----------
        valve_string : name of valve to be controlled
        
        sensor_value : The current sensor reading value

        target : The optimal value that the sensor should be reading

        window : This value is the variance allowed from the target value
   
        Returns
        -------
        Commands the specified Valve to OPEN or CLOSE

        """
    if getNanny() == ACTIVE:
        if (-sensor_value) >= (-target):
            setVLVState(valve_string, CLOSE)
        elif (-sensor_value) < ((-target) - window):
            setVLVState(valve_string, OPEN)
    return 

