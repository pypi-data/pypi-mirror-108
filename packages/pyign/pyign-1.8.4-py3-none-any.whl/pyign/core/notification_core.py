########################### notification_core########################
# This module holds the Notification class that uses string arrays
# to provide text based feedback to Output to the control display.
######################################################################

class Notifications(list):
    """The Notification Class contains the string array used to output notifications to LabVIEW.
        
        The Alert_String is a two element array used to provide user feedback about system tripped
        aborts. The array is updated in the Nanny/EHMS module using the checkAbortNotifications 
        function. If a sensor's value is outside of its bounds, the first string will display
        that a system abort occurred and the time. The second element is utilized to display the
        specific sensor(s) that tripped the abort. 
        """
    Alert_String = ['No Alerts', '']

def setAbortString(title, message):
    """Sets the first and second element of the string array"""
    Notifications.Alert_String[0] = title
    Notifications.Alert_String[1] = message

def getAbortString():
    """Returns the array string"""
    return Notifications.Alert_String


