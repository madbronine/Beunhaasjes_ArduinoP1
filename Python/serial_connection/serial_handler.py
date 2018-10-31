# © Jeroen - 31-10-2018
#handles serial connection (wip)

import serial
from serial.tools import list_ports


import serial

class Serial_Handler:
    def __init__(self):
        print('init')


class Serial_Communication:
    def __init__(self):
        print('init')

#----------------------------------------------

def get_devices():
    print('Check arduino connection and type')
    return None

#---------------------------------------------
















#Dictionary with avaible ports and type
avaible_ports = {}
# avaible_ports = { "COM0" : "Temperature" }


#Dictionary with identify code and type
controller_types =	{
  "TEMP": "Temperature",
  "LIGHT": "Light",
}



#Refresh our dictionary (Check if there are new modules connected or old modules disconnected)
def refresh_ports():
    print('Refreshing com ports...')

    # In get_ports() they should be tested to check if they are controll units
    global avaible_ports
    avaible_ports = ser_find.get_ports(avaible_ports);

def get_modules():
    return avaible_ports

# Returns the value of the sensor
def read_module(comport):
    #To-do: communicate with the arduino!
    if comport in avaible_ports:
        return ({'Port': comport, 'type-code': avaible_ports[comport], 'type': controller_types[avaible_ports[comport]], 'sensor': 'TO-DO'})

    return None

def get_sensor(comport):
    return 'null'
