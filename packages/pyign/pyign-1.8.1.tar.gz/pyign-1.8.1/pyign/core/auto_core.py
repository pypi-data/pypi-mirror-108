########################### auto_core #############################
#
#
###################################################################


# third-party libraries
# import numpy as np

# # local imports
from pyign.manifest._built_in_ import *
from pyign.manifest._engine_config_ import *
from pyign.core.bedrock_core import (bed_rock_up, bed_rock_down)
from pyign.core.ehms_core import checkSequence, checkFlowMeter, secureIgniterState
from pyign.base.sensors import getSNSCalc, getPTValue, getTCValue
from pyign.base.valves import setVLVState, setIGNState
from pyign.base.states import (getNanny, getSeqCheck, getSeqState, setSeqState, setSeq, 
                               getIgniterArm, setArmActive)


##########################################################################################################################################


## Automated Sequence Timing Calculations ##### THIS METHOD IMPROVES READABILITY AT THE COST OF CHAINING COMMANDS (IE CAN EASILY MIX UP TIMING BY CHANGING ONE VALUE)
# Fuel Cold Flow Timing:
START_FUEL_PURGE___COLDFLOW = (T_MINUS_FUEL_COLDFLOW + START_FUEL_PURGE_COLDFLOW) 
FUEL_PURGE___COLDFLOW = (T_MINUS_FUEL_COLDFLOW + FUEL_PURGE_COLDFLOW) 
FUEL_ISO___COLDFLOW = (T_MINUS_FUEL_COLDFLOW + FUEL_ISO_COLDFLOW) 
FUEL_PRESS___COLDFLOW = (T_MINUS_FUEL_COLDFLOW + FUEL_PRESS_COLDFLOW) 
FUEL_VENT___COLDFLOW = (T_MINUS_FUEL_COLDFLOW + FUEL_VENT_COLDFLOW) 
FUEL_MAIN___COLDFLOW = (T_MINUS_FUEL_COLDFLOW + FUEL_MAIN_COLDFLOW) 
T_MINUS___FUEL_COLDFLOW = T_MINUS_FUEL_COLDFLOW
TOTAL_RUN___FUEL_COLDFLOW = T_MINUS_FUEL_COLDFLOW*2 #THE BURN TIME CANT BE AS LONG AS THE T_MINUS TIME 

# Ox Cold Flow Timing:
CRYO_ISO___COLDFLOW = (T_MINUS_CRYO_COLDFLOW + CRYO_ISO_COLDFLOW) 
CRYO_PRESS___COLDFLOW = (T_MINUS_CRYO_COLDFLOW + CRYO_PRESS_COLDFLOW) 
CRYO_VENT___COLDFLOW = (T_MINUS_CRYO_COLDFLOW + CRYO_VENT_COLDFLOW) 
CRYO_CHILL___COLDFLOW = (T_MINUS_CRYO_COLDFLOW + CRYO_CHILL_COLDFLOW) 
CRYO_MAIN___COLDFLOW = (T_MINUS_CRYO_COLDFLOW + CRYO_MAIN_COLDFLOW) 
T_MINUS___CRYO_COLDFLOW = T_MINUS_CRYO_COLDFLOW
TOTAL_RUN___CRYO_COLDFLOW = T_MINUS_CRYO_COLDFLOW*2 # THE BURN TIME CANT BE AS LONG AS THE T_MINUS TIME 

# - Bedrock Press Timing: 
INTER_PRESS___COLDFLOW = T_MINUS_CRYO_COLDFLOW - (T_MINUS_CRYO_COLDFLOW - INTER_PRESS_COLDFLOW) 
PRE_PRESS___COLDFLOW = T_MINUS_CRYO_COLDFLOW - (T_MINUS_CRYO_COLDFLOW - PRE_PRESS_COLDFLOW) 
BURN_PRESS___COLDFLOW = T_MINUS_CRYO_COLDFLOW - (T_MINUS_CRYO_COLDFLOW - BURN_PRESS_COLDFLOW)

# Fuel & Ox Hotfire Timing:
TOTAL_RUN___HOTFIRE = (T_MINUS_HOTFIRE + T_PLUS_HOTFIRE)

# - Bedrock Press Timing: 
INTER_PRESS___HOTFIRE = T_MINUS_HOTFIRE - (T_MINUS_HOTFIRE - INTER_PRESS_HOTFIRE)
PRE_PRESS___HOTFIRE = T_MINUS_HOTFIRE - (T_MINUS_HOTFIRE - PRE_PRESS_HOTFIRE)
BURN_PRESS___HOTFIRE = T_MINUS_HOTFIRE - (T_MINUS_HOTFIRE - BURN_PRESS_HOTFIRE)

# # - Igniter Timing:
START_IGNITER___HOTFIRE = (T_MINUS_HOTFIRE - START_IGNITER_HOTFIRE) 
IGNITER___HOTFIRE = (T_MINUS_HOTFIRE + IGNITER_HOTFIRE)

# - Fuel Timing:
START_FUEL_MAIN___HOTFIRE = (T_MINUS_HOTFIRE - FUEL_MAIN_DT - FUEL_STAY_TIME) 
START_PURGE___HOTFIRE = (T_MINUS_HOTFIRE + START_PURGE_HOTFIRE) 
FUEL_ISO___HOTFIRE = (T_MINUS_HOTFIRE + FUEL_ISO_HOTFIRE) 
FUEL_PRESS___HOTFIRE = (T_MINUS_HOTFIRE + FUEL_PRESS_HOTFIRE) 
FUEL_VENT___HOTFIRE = (T_MINUS_HOTFIRE + FUEL_VENT_HOTFIRE) 
FUEL_MAIN___HOTFIRE = (T_MINUS_HOTFIRE + FUEL_MAIN_HOTFIRE) 
FUEL_PURGE___HOTFIRE = (T_MINUS_HOTFIRE + FUEL_PURGE_HOTFIRE) 

# - Ox Timing:
START_OX_MAIN___HOTFIRE = (T_MINUS_HOTFIRE - OX_MAIN_DT) 
OX_ISO___HOTFIRE = (T_MINUS_HOTFIRE + OX_ISO_HOTFIRE) 
OX_PRESS___HOTFIRE = (T_MINUS_HOTFIRE + OX_PRESS_HOTFIRE) 
OX_VENT___HOTFIRE = (T_MINUS_HOTFIRE + OX_VENT_HOTFIRE) 
OX_CHILL___HOTFIRE = (T_MINUS_HOTFIRE + OX_CHILL_HOTFIRE) 
OX_MAIN___HOTFIRE = (T_MINUS_HOTFIRE + OX_MAIN_HOTFIRE) 


##########################################################################################################################################


def commence_fu_cold_flow(Timer, ButtonString):
    """Check if  the 'Cold Flow' button has been pressed and preforms fuel side 
        cold flow procedures.

        Parameters
        ----------
        Timer : string
            string input of timestamp
        ButtonString : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
   
        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        a : valve ABV-PR-110
        b : valve ABV-PR-120
        c : valve ABV-OX-210
        d : valve ABV-FU-310
        e : valve ABV-OX-220
        f : valve ABV-FU-320
        g : valve ABV-OX-230
        h : valve ABV-FU-330
        i : valve ABV-OX-240
        j : valve ABV-FU-340
        k : valve ABV-OX-250

        """
    checkSequence()
    if getSeqCheck() == ACTIVE:
        checkFlowMeter(ButtonString)
        if Timer <= TOTAL_RUN___FUEL_COLDFLOW:  # Bedrock
            bed_rock_up('ABV-PR-120', getSNSCalc('PT-FU-CLC-315'), FU_PT_RUN_TARGET, FU_PT_RUN_DEADBAND)
            setSeqState('sequence active')
            if START_FUEL_PURGE___COLDFLOW <= Timer <= FUEL_PURGE___COLDFLOW: # Purge
                setVLVState('ABV-FU-330', OPEN)
            else:
                setVLVState('ABV-FU-330', CLOSE)
            if  Timer <= FUEL_MAIN___COLDFLOW:    # Main
                setVLVState('ABV-FU-340', OPEN)
            else:
                setVLVState('ABV-FU-340', CLOSE)
            if FUEL_PRESS___COLDFLOW <= Timer:    # Press
                setVLVState('ABV-PR-120', CLOSE)
            if FUEL_VENT___COLDFLOW <= Timer:     # Vent
                setVLVState('ABV-FU-310', OPEN)
            if FUEL_ISO___COLDFLOW <= Timer:      # Iso
                setVLVState('ABV-FU-320', CLOSE)
        else:
            setVLVState('ABV-FU-340', CLOSE)
            setSeq('cold flow')
    else:
        setVLVState('ABV-FU-340', CLOSE)
        setSeq('cold flow')
    return


def commence_cryo_cold_flow(Timer, ButtonString):
    """Check if  the 'Cold Flow' button has been pressed and performs cryo side 
        cold flow procedures.

        Parameters
        ----------
        Timer : string
            string input of timestamp
        ButtonString : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
   
        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        a : valve ABV-PR-110
        b : valve ABV-PR-120
        c : valve ABV-OX-210
        d : valve ABV-FU-310
        e : valve ABV-OX-220
        f : valve ABV-FU-320
        g : valve ABV-OX-230
        h : valve ABV-FU-330
        i : valve ABV-OX-240
        j : valve ABV-FU-340
        k : valve ABV-OX-250

        args[0] = vst
        args[1] = timer
        args[2] = sqst
        args[3] = nanny/abt (abort class)
        args[4] = gst
        args[5] = flow meter
        args[6] = ptl (pressure transducer class) or clc (sensor calculation class)
        """
    checkSequence()
    if getSeqCheck() == ACTIVE:
        checkFlowMeter(ButtonString)
        if Timer <= TOTAL_RUN___CRYO_COLDFLOW:
            if INTER_PRESS___COLDFLOW <= Timer < PRE_PRESS___COLDFLOW: # Bedrock Intermediate Press
                bed_rock_up('ABV-PR-110', getSNSCalc('PT-OX-CLC-215'), OX_INTER_PT_TARGET, OX_PT_RUN_DEADBAND)
                setVLVState('ABV-OX-240', CLOSE)
                setVLVState('ABV-FU-340', CLOSE)
                setSeqState('sequence active')
            elif PRE_PRESS___COLDFLOW <= Timer < BURN_PRESS___COLDFLOW: # Bedrock Pre-Press
                bed_rock_up('ABV-PR-110', getSNSCalc('PT-OX-CLC-215'), OX_PRE_PRESS_PT_TARGET, OX_PT_RUN_DEADBAND)
                setVLVState('ABV-OX-240', CLOSE)
                setVLVState('ABV-FU-340', CLOSE)
                setSeqState('sequence active')
            elif  Timer < TOTAL_RUN___CRYO_COLDFLOW:    # Bedrock
                bed_rock_up('ABV-PR-110', getSNSCalc('PT-OX-CLC-215'), OX_PT_RUN_TARGET, OX_PT_RUN_DEADBAND)
                setSeqState('sequence active')
                if T_MINUS___CRYO_COLDFLOW < Timer <= CRYO_MAIN___COLDFLOW:      # Main
                   setVLVState('ABV-OX-240', OPEN)
                   setVLVState('ABV-FU-340', OPEN)
                else:
                    setVLVState('ABV-OX-240', CLOSE)
                    setVLVState('ABV-FU-340', CLOSE)
                if CRYO_ISO___COLDFLOW <= Timer:        # Iso
                    setVLVState('ABV-OX-220', CLOSE)
                if CRYO_PRESS___COLDFLOW <= Timer:      # Press
                    setVLVState('ABV-PR-110', CLOSE)
                if CRYO_VENT___COLDFLOW <= Timer:       # Vent
                    setVLVState('ABV-OX-210', OPEN)
                if CRYO_CHILL___COLDFLOW <= Timer:      # Chill
                    setVLVState('ABV-OX-230', OPEN)
        else:
            setVLVState('ABV-OX-240', CLOSE)
            setVLVState('ABV-FU-340', CLOSE)
            setSeq('cold flow')
    else:
        setVLVState('ABV-OX-240', CLOSE)
        setVLVState('ABV-FU-340', CLOSE)
        setSeq('cold flow')
    return 


def commence_purge_1(Timer):
    """Check if  the 'One Second Purge' button has been pressed and set purge valve to 'OPEN' state.

        Parameters
        ----------
        valve_states : int array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        timer : double
            Values for timer start at 0 and count up.

        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        args[0] = vst
        args[1] = timer
        args[2] = sqst
        """
    if Timer <= PURGE1 :
        setVLVState('ABV-FU-330', OPEN)
    else :
        setVLVState('ABV-FU-330', CLOSE)
        setSeq('purge 1')
    return


def commence_purge_2(Timer):
    """Check if  the 'Two Second Purge' button has been pressed and set purge valve to 'OPEN' state.

        Parameters
        ----------
        valve_states : int array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        timer : double
            Values for timer start at 0 and count up.

        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        args[0] = vst
        args[1] = timer
        args[2] = sqst
        """
    if Timer <= PURGE2 :
        setVLVState('ABV-FU-330', OPEN)
    else :
        setVLVState('ABV-FU-330', CLOSE)
        setSeq('purge 2')
    return 


def commence_hotfire(Timer):
    """Check if  the 'Start Up' button has been pressed and set main valves to 'OPEN' state.

        Parameters
        ----------
        valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
        igniter_state : int
            Values for Igniter State range from 0 for 'SAFE' to 1 for 'ACTIVE'.
        timer_state : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system timer state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        timer : float
            Running timer values starting from time = 0
        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        args[0] = vst
        args[1] = timer
        args[2] = sqst
        args[3] = nanny/abt (abort class)
        args[4] = gst
        args[5] = ist
        args[6] = ptl (pressure transducer class) or clc (sensor calculation class)
        """
    checkSequence()
    if getSeqCheck() == ACTIVE:
        if Timer <= TOTAL_RUN___HOTFIRE:
            setVLVState('ABV-WS-610', OPEN)
            if INTER_PRESS___HOTFIRE <= Timer < PRE_PRESS___HOTFIRE: # Bedrock Intermediate Press
                bed_rock_up('ABV-PR-110', getSNSCalc('PT-OX-CLC-215'), OX_INTER_PT_TARGET, OX_PT_RUN_DEADBAND)
                bed_rock_up('ABV-PR-120', getSNSCalc('PT-FU-CLC-315'), FU_INTER_PT_TARGET, FU_PT_RUN_DEADBAND)
                setVLVState('ABV-OX-240', CLOSE)
                setVLVState('ABV-FU-340', CLOSE)
                setIGNState(SAFE)
                setVLVState('ABV-WS-610', OPEN)
                setSeqState('sequence active')
                if START_IGNITER___HOTFIRE <= Timer <= IGNITER___HOTFIRE:
                    setIGNState(ACTIVE)
                else:
                    setIGNState(SAFE)
            elif PRE_PRESS___HOTFIRE <= Timer < BURN_PRESS___HOTFIRE: # Bedrock Pre-Press
                bed_rock_up('ABV-PR-110', getSNSCalc('PT-OX-CLC-215'), OX_PRE_PRESS_PT_TARGET, OX_PT_RUN_DEADBAND)
                bed_rock_up('ABV-PR-120', getSNSCalc('PT-FU-CLC-315'), FU_PRE_PRESS_PT_TARGET, FU_PT_RUN_DEADBAND)
                setVLVState('ABV-OX-240', CLOSE)
                setVLVState('ABV-FU-340', CLOSE)
                setIGNState(SAFE)
                setVLVState('ABV-WS-610', OPEN)
                setSeqState('sequence active')
                if START_IGNITER___HOTFIRE <= Timer <= IGNITER___HOTFIRE:
                    setIGNState(ACTIVE)
                else:
                    setIGNState(SAFE)
            elif BURN_PRESS___HOTFIRE <= Timer < TOTAL_RUN___HOTFIRE: # Bedrock Hotfire Press 
                bed_rock_up('ABV-PR-110', getSNSCalc('PT-OX-CLC-215'), OX_PT_RUN_TARGET, OX_PT_RUN_DEADBAND)
                bed_rock_up('ABV-PR-120', getSNSCalc('PT-FU-CLC-315'), FU_PT_RUN_TARGET, FU_PT_RUN_DEADBAND)
                setVLVState('ABV-WS-610', OPEN)
                setSeqState('sequence active')
                if START_IGNITER___HOTFIRE <= Timer <= IGNITER___HOTFIRE:
                    setIGNState(ACTIVE)
                else:
                    setIGNState(SAFE)
                if START_OX_MAIN___HOTFIRE <= Timer <= OX_MAIN___HOTFIRE:
                    setVLVState('ABV-OX-240', OPEN)
                else:
                    setVLVState('ABV-OX-240', CLOSE)
                if START_FUEL_MAIN___HOTFIRE <= Timer <= FUEL_MAIN___HOTFIRE:
                    setVLVState('ABV-FU-340', OPEN)
                else:
                    setVLVState('ABV-FU-340', CLOSE)
                if START_PURGE___HOTFIRE <= Timer <= FUEL_PURGE___HOTFIRE:
                    setVLVState('ABV-FU-330', OPEN)
                else:
                    setVLVState('ABV-FU-330', CLOSE)
                if OX_ISO___HOTFIRE <= Timer:
                    setVLVState('ABV-OX-220', CLOSE)
                if FUEL_ISO___HOTFIRE <= Timer:
                    setVLVState('ABV-FU-320', CLOSE)
                if OX_PRESS___HOTFIRE <= Timer:
                    setVLVState('ABV-PR-110', CLOSE)
                if FUEL_PRESS___HOTFIRE <= Timer:
                    setVLVState('ABV-PR-120', CLOSE)
                if OX_VENT___HOTFIRE <= Timer:
                    setVLVState('ABV-OX-210', OPEN)
                if FUEL_VENT___HOTFIRE <= Timer:
                    setVLVState('ABV-FU-310', OPEN)
                if OX_CHILL___HOTFIRE <= Timer:
                    setVLVState('ABV-OX-230', OPEN)
        else:
            setVLVState('ABV-OX-240', CLOSE)
            setVLVState('ABV-FU-340', CLOSE)
            setIGNState(SAFE)
            setVLVState('ABV-WS-610', CLOSE)
            setSeq('startup')
    else:
        setVLVState('ABV-OX-240', CLOSE)
        setVLVState('ABV-FU-340', CLOSE)
        setIGNState(SAFE)
        setVLVState('ABV-WS-610', CLOSE)
        setSeq('startup')
    return 


def commence_ox_vent(Timer):
    """Check if  the 'Cycle Vent' button has been pressed and set main valves to 'OPEN' state.

        Parameters
        ----------
        valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
        timer_state : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system timer state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        timer : float
            Running timer values starting from time = 0
        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        args[0] = vlv
        args[1] = timer
        args[2] = sqst
        """
    if Timer <= VENT:
        setVLVState('ABV-OX-210', OPEN)
    else :
        setVLVState('ABV-OX-210', CLOSE)
        setSeq('ox vent')
    return 


def commence_fuel_vent(Timer):
    """Check if  the 'Cycle Vent' button has been pressed and set main valves to 'OPEN' state.

        Parameters
        ----------
        valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
        timer_state : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system timer state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        timer : float
            Running timer values starting from time = 0
        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        args[0] = vlv
        args[1] = timer
        args[2] = sqst
        """
    if Timer <= VENT:
        setVLVState('ABV-FU-310', OPEN)
    else :
        setVLVState('ABV-FU-310', CLOSE)
        setSeq('fuel vent')
    return 


def commence_system_cycle(Timer):
    """Check if  the 'Cycle All Valves' button has been pressed and set main valves to 'OPEN' state.

        Parameters
        ----------
        valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
        timer_state : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system timer state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        timer : float
            Running timer values starting from time = 0
        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        args[0] = vlv
        args[1] = timer
        args[2] = sqst
        """
    if CYCLE_ONE < Timer <= CYCLE_TWO:
        setVLVState('ABV-PR-110', OPEN)
        setVLVState('ABV-PR-120', OPEN)
    if CYCLE_TWO < Timer <= CYCLE_THREE:
        setVLVState('ABV-PR-110', CLOSE)
        setVLVState('ABV-PR-120', CLOSE)
        setVLVState('ABV-OX-210', CLOSE)
        setVLVState('ABV-FU-310', CLOSE)
    if CYCLE_THREE < Timer <= CYCLE_FOUR:
        setVLVState('ABV-OX-210', OPEN)
        setVLVState('ABV-FU-310', OPEN)
        setVLVState('ABV-OX-250', OPEN)
    if CYCLE_FOUR < Timer <= CYCLE_FIVE:
        setVLVState('ABV-OX-250', CLOSE)
        setVLVState('ABV-OX-220', OPEN)
        setVLVState('ABV-FU-320', OPEN)
    if CYCLE_FIVE < Timer <= CYCLE_SIX:
        setVLVState('ABV-OX-220', CLOSE)
        setVLVState('ABV-FU-320', CLOSE)
        setVLVState('ABV-OX-230', OPEN)
        setVLVState('ABV-FU-330', OPEN)
    if CYCLE_SIX < Timer <= CYCLE_SEVEN:
        setVLVState('ABV-OX-230', CLOSE)
        setVLVState('ABV-FU-330', CLOSE)
        setVLVState('ABV-FU-340', OPEN)
        setVLVState('ABV-OX-240', OPEN)
    if CYCLE_SEVEN < Timer <= CYCLE_EIGHT:
        setVLVState('ABV-FU-340', CLOSE)
        setVLVState('ABV-OX-240', CLOSE)
    if CYCLE_EIGHT < Timer:
        setSeq('system cycle')
    return 


def commence_valve_firing_sim(Timer):
    """Check if  the 'Valve Firing Sim' button has been pressed and set main valves to 'OPEN' state.

        Parameters
        ----------
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        a : valve ABV-PR-110
        b : valve ABV-PR-120
        c : valve ABV-OX-210
        d : valve ABV-FU-310
        e : valve ABV-OX-220
        f : valve ABV-FU-320
        g : valve ABV-OX-230
        h : valve ABV-FU-330
        i : valve ABV-OX-240
        j : valve ABV-FU-340
        k : valve ABV-OX-250

        args[0] = vst
        args[1] = timer
        args[2] = sqst
        """
    setVLVState('ABV-OX-220', CLOSE)
    setVLVState('ABV-FU-320', CLOSE)
    setVLVState('ABV-OX-230', CLOSE)
    setVLVState('ABV-FU-330', CLOSE)
    setVLVState('ABV-OX-240', CLOSE)
    setVLVState('ABV-FU-340', CLOSE)
    if CYCLE_ONE_OPEN < Timer <= CYCLE_ONE_CLOSE:
        setVLVState('ABV-OX-220', CLOSE)
        setVLVState('ABV-FU-320', CLOSE)
        setVLVState('ABV-OX-230', CLOSE)
        setVLVState('ABV-FU-330', CLOSE)
        setVLVState('ABV-OX-240', OPEN)
        setVLVState('ABV-FU-340', OPEN)
    if CYCLE_TWO_OPEN < Timer <= CYCLE_TWO_CLOSE:
        setVLVState('ABV-OX-220', CLOSE)
        setVLVState('ABV-FU-320', CLOSE)
        setVLVState('ABV-OX-230', CLOSE)
        setVLVState('ABV-FU-330', CLOSE)
        setVLVState('ABV-OX-240', OPEN)
        setVLVState('ABV-FU-340', OPEN)
    if CYCLE_THREE_OPEN < Timer <= CYCLE_THREE_CLOSE:
        setVLVState('ABV-OX-220', CLOSE)
        setVLVState('ABV-FU-320', CLOSE)
        setVLVState('ABV-OX-230', CLOSE)
        setVLVState('ABV-FU-330', CLOSE)
        setVLVState('ABV-OX-240', OPEN)
        setVLVState('ABV-FU-340', OPEN)
    if CYCLE_COMPLETE < Timer:
        setVLVState('ABV-OX-220', CLOSE)
        setVLVState('ABV-FU-320', CLOSE)
        setVLVState('ABV-OX-230', CLOSE)
        setVLVState('ABV-FU-330', CLOSE)
        setVLVState('ABV-OX-240', CLOSE)
        setVLVState('ABV-FU-340', CLOSE)
        setSeq('valve firing sim')
    return 


def commence_cryo_fill():
    """Check if  the 'Cold Fill' button has been pressed the fill and chill are 
        controlled until depressed.

        Parameters
        ----------
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        a : valve ABV-PR-110
        b : valve ABV-PR-120
        c : valve ABV-OX-210
        d : valve ABV-FU-310
        e : valve ABV-OX-220
        f : valve ABV-FU-320
        g : valve ABV-OX-230
        h : valve ABV-FU-330
        i : valve ABV-OX-240
        j : valve ABV-FU-340
        k : valve ABV-OX-250
        
        args[0] = vst
        args[1] = nanny/abt (abort class)
        args[2] = ptl or tcl or clc (first control sensor state)
        args[3] = ptl or tcl or clc (second control sensor state)
        """
    if getNanny() == ACTIVE:
        if getPTValue('PT-OX-240') > DEWAR_PT_LOW:
            setVLVState('ABV-OX-250', OPEN)
            setVLVState('ABV-OX-210', OPEN)
        else:
            setVLVState('ABV-OX-250', CLOSE)

        if getTCValue('TC-OX-220') < TANK_TC_TARGET:
            setVLVState('ABV-OX-230', CLOSE)
        else:
            bed_rock_down('ABV-OX-230', getTCValue('TC-OX-250'), OX_CHILL_TARGET, OX_CHILL_DEADBAND)
    return 


def commence_leak_check(ValveString, SensorString):
    """Check if  the 'Leak Check' button is active and press propellant tank.

        Parameters
        ----------
        valve_states : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.
        abort_state : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system timer state.
        clc_state : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system timer state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        valve string : float
            Running timer values starting from time = 0
        sensor string : float
            Running timer values starting from time = 0
        Returns
        -------
        valve_states : int numpy array
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system valve state.

        args[0] = vst
        args[1] = nanny/abt
        args[2] = clc
        args[3] = valve string
        args[4] = sensor string
        args[5] = sensor target
        args[6] = sensor deadband
        """
    if getNanny() == ACTIVE:
        bed_rock_up(ValveString, getSNSCalc(SensorString), LEAK_CHECK_TARGET, LEAK_CHECK_DEADBAND)
    return


def commence_igniter_checkout(Timer):
    """Check if  the 'Ignter Test' and 'Igniter Arm' button is active and press propellant tank.

        Parameters
        ----------
        igniter_states : int numpy array
            [0, 0] = 'SAFE' system Igniter State.
        abort_state : int numpy array
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] = 'SAFE' system timer state.
        button : int
            Values for button press range from 0 for 'INACTIVE' to 1 for 'ACTIVE'.
        timer : float
            Running timer values starting from time = 0
        Returns
        -------
        igniter_states : int numpy array
             [0] = 'SAFE' system valve state.

        args[0] = vst
        args[1] = nanny/abt
        args[2] = clc
        args[3] = valve string
        args[4] = sensor string
        args[5] = sensor target
        args
    """
    if getNanny() == ACTIVE: #Make Sure Nany is 'ON'
        if Timer < IGN_TEST_TOTAL: #Kill test after 15 sec
            if IGN_TEST_ONE < Timer <= IGN_TEST_TWO: #Allow Time Delay before Igniter HIGH
                secureIgniterState() #Hold both Mains "CLOSED"
                setSeq('none')
            else:
                setIGNState(INACTIVE) #Kill high signal
        else:
            setArmActive(INACTIVE)  
            setSeq('igniter active')
    else:
        setArmActive(INACTIVE)
        setSeq('igniter active')