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
    data = create_data(new_module)

    new_module.set_data(data)
    return new_module

# Get all data from the arduino to initialize the module class
def create_data(module):
    print('IMPORTANT: Not correct data yet')
    timer = get_sensor_setting(module, 'get_timer')
    sensor_min = get_sensor_setting(module, 'get_sensor_min')
    sensor_max = get_sensor_setting(module, 'get_sensor_max')
    distance_min = get_sensor_setting(module, 'get_distance_min')
    distance_max = get_sensor_setting(module, 'get_distance_max')

    print('@@@$%#!%^$^#% MESSAGE:' , distance_min['message'])

    data = Module_Data(timer['data'], sensor_min['data'], sensor_max['data'], distance_min['data'], distance_max['data'])
    return data

# Get given sensor setting from specified module
def get_sensor_setting(module, send_cmd):
    result = {'error' : False, 'message' : None, 'data' : None} # Store result!

    isConnected = ser_scan.check_connection(module.get_port()) #Check connection

    if isConnected == True: # are we connected
        send_code = msg.send_code(send_cmd)   # Get send code
        resp_code = msg.response_code('succeed') # Get response code

        if  send_code['error'] == False and resp_code['error'] == False: # No error
            response = get_value(module, send_code['code'], resp_code['code']) # Get data

            if response['error'] == False:
                result['error'] = False
                result['data'] = response['data']
            else:
                result['error'] = True
                result['message'] = response['message']
        else:
            # Invalid code
            result['error'] = True
            result['message'] = "Invalid send code!"
    else:
        result['error'] = True
        result['message'] = "No connection!"

    return result




# Handles sending and receiving
def get_value(module, send_code, resp_code):
    result = {}

    resp = ser_com.send_data(module.get_ser(), send_code) # Retrieve message

    if resp == resp_code:
        data = ser_com.get_message(module.get_ser()) # Retrieve message
        result['error'] = False
        result['data'] = data
    else:
        result['message'] = "Invalid response code: {0} - asked for {1}".format(resp, resp_code)
        result['error'] = True

    return result
