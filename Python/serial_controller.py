# © Jeroen - 30-10-2018
# This file is used to interact with the modules

import serial_connection.serial_communication as ser_com
import serial_connection.serial_scanner as ser_scan
import serial_connection.messages as msg
from module import *

# Dictionary containing all devices currently found
current_devices = {} # Example data: {'COM5' : MODULE}


#       Code below is handled by the program
#------------------------------------------------------


#Run the controller (call with program loop)
def run():
    print('running the controller (updating connections)')

    all_ports = ser_scan.find_available_ports() # Get all attatched comports
    not_used_ports = remove_disconnected_devices(all_ports) # Get al comports NOT ine use

    if len(not_used_ports) > 0: # If we have more then 0 unused ports
        new_devices = identify_devices(not_used_ports) # Identify new devices
        current_devices.update(new_devices) # Update current devices with new devices


# Returns dictionary with all connected devices
def get_devices():
    # print('Getting all connected devices')
    return current_devices # Example value:    {'com1' : Temperature, 'com2' : Light}

# Reads the sensor data from the given device
def get_sensor_data(device_com_port):
    result = {}
    result = {"error" : True, "msg" : None}

    return result # Example value:    namedtuple('sensor_value' : 5)




# Sets the max value with parameter data for the sensor of given device
def get_distance_max(module):
    isConnected = ser_scan.check_connection(module.get_port()) #Check connection
    result = {} # Place to store the result!

    if isConnected == True:
        #print('Set sensor max value. Command: {0}  value: {1}   device: {2}'.format(command, value, device_com_port))
        print('Is connected, trying to send!')
        ser = module.get_ser() # Get serial
        send_code = msg.send_code('get_distance_max')   # Get send code
        resp_code = msg.response_code('succeed')        # Get response code
        response = ser_com.send_data(ser, send_code['code']) # Send command code

        if response == resp_code['code']:              # Check if the response code matches
            data = ser_com.get_message(ser) # Retrieve message
            result = {"error" : False, "data" : data}
        else:
            result = {"error" : True, "msg" : 'Wrong response'}
    else:
        result = {"error" : True, "msg" : 'Not connected'}

    return data


#       Code below is handled by the controller
#------------------------------------------------------

# Removes disconnected devices from current_devices, returns port not scanned yet
def remove_disconnected_devices(all_ports):
    to_remove = []
    ports_not_used = all_ports

    # Loop through existing devices
    for device in current_devices:
        # If the device isn't connected anymore, remove it
        if device not in all_ports:
            # Disconnected
            to_remove.append(device)
        else:
            # We already have this port, (we are using it)
            ports_not_used.remove(device)


    # For reach device in to_remove, remove it from current_devices
    for dev in to_remove:
        if dev in current_devices:
            # Delete our disconnected device
            current_devices.pop(dev)

    return ports_not_used

# Removes disconnected devices from current_devices, returns port not scanned yet
def identify_devices(comports):
    print('Identifying: ', comports)

    # Dict containing new devices
    new_devices = {}

    # Identify every comport
    for comport in comports:
        result = identy_device(comport) # Check every device
        if result["error"] == False:    # Didnt get an error
            new_devices[comport] = result["module"] # Add it

    return new_devices


def identy_device(comport):
    identified_device = {"error" : False, "module" : None}

    #First send identify message
    send_code = msg.send_code('detect') # Debug 5 we will see
    resp_code = msg.response_code('succeed')

    result = ser_com.identify_device(comport, send_code['code'], resp_code['code']) # Result got from the arduino


    if result['error'] == False:    # If didn't get an error
        module = create_module(result['serial'], result['type'], comport)   # Create new module
        identified_device["error"] = False
        identified_device["module"] = module
    else:   # Error
        identified_device["error"] = True

    return identified_device


def create_module(ser, type, comport):
    # TO-DO: Create module data! (or use default...?)
    new_module = Module(ser,comport, type)
    data = get_data(new_module)

    return new_module

# Get all data from the arduino to initialize the module class
def get_data(module):
    print('IMPORTANT: No data yet')

    timer = 0
    sensor_min = 0
    sensor_max = 0
    distance_min = 0;
    distance_max = get_distance_max(module)
    data = Module_Data(timer, sensor_min, sensor_max)
    return data
