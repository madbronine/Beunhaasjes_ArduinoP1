# © Jeroen - 30-10-2018

from serial_connection.serial_finder import *
from serial_connection.serial_handler import *

#Dictionary with avaible ports and type
avaible_ports = {}
# avaible_ports = { "COM0" : "Temperature" }


#Dictionary with identify code and type
controller_types =	{
  "TEMP": "Temperature",
  "LIGHT": "Light",
}

#Run the controller
def run():
    refresh_ports()

#Refresh our dictionary (Check if there are new modules connected or old modules disconnected)
def refresh_ports():
    print('Refreshing com ports...')

    # In get_ports() they should be tested to check if they are controll units
    global avaible_ports
    avaible_ports = get_ports(avaible_ports);

def get_modules():
    return avaible_ports

# Returns the value of the sensor
def read_module(comport):
    #To-do: communicate with the arduino!
    if comport in avaible_ports:
        return ({'Port': comport, 'type-code': avaible_ports[comport], 'type': controller_types[avaible_ports[comport]], 'sensor': 'TO-DO'})

    return None
