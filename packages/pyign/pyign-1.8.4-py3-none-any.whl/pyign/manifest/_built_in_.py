############## CONSTANTS ##############
OPEN = 1
CLOSE = 0
INACTIVE = 0
ACTIVE = 1
SAFE = 0

VALVE_SAFE = [0]*13
#######################################






###### TARGETS ########

####### Bedrock Press Targets #########
LEAK_CHECK_TARGET = 200.0
FU_PT_RUN_TARGET = 785.0
OX_PT_RUN_TARGET = 765.0
FU_PRE_PRESS_PT_TARGET = 680.0
OX_PRE_PRESS_PT_TARGET = 675.0
FU_INTER_PT_TARGET = 450.0
OX_INTER_PT_TARGET = 400.0
#######################################





####### Bedrock Press Deadbands #######
LEAK_CHECK_DEADBAND = 15.0
FU_PT_RUN_DEADBAND = 15.0
OX_PT_RUN_DEADBAND = 15.0
#######################################




######### Automation Targets ##########
DEWAR_PT_LOW = 0
TANK_TC_TARGET = -300.0
CHILL_TC_LOW_TARGET = -120.0
OX_CHILL_TARGET = -200.0
OX_CHILL_DEADBAND = 50.0
#######################################





######## Bedrock Sensor Type ##########
# (ACTIVE => ptl & INACTIVE => clc) #
TANK_BEDROCK_TYPE = INACTIVE
DEWAR_BEDROCK_TYPE = ACTIVE
#######################################