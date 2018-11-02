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

    # Find all currently attached ports and check if our current devices are still connected
    all_ports = ser_scan.find_available_ports()
    not_used_ports = remove_disconnected_devices(all_ports)

    if len(not_used_ports) > 0:
    #    print('UNUSED: ' , not_used_ports)
        # Now we test or new devices
        new_devices = identify_devices(not_used_ports)
        current_devices.update(new_devices)
    #else:
    #    print('No unused devices!')


# Returns dictionary with all connected devices
def get_devices():
    # print('Getting all connected devices')
    return current_devices # Example value:    {'com1' : Temperature, 'com2' : Light}

# Reads the sensor data from the given device
def get_sensor_data(device_com_port):
    print('Gets all sensor data')
    return None # Example value:    namedtuple('sensor_value' : 5)




# Sets the max value with parameter data for the sensor of given device
def get_distance_max(module, value):

    #Check connection
    isConnected = ser_scan.check_connection(module.get_port())
    result = {}

    if isConnected == True:
        #print('Set sensor max value. Command: {0}  value: {1}   device: {2}'.format(command, value, device_com_port))
        print('Is connected, trying to send!')

        # Get serial
        ser = module.get_ser()
        # Get codes
        send_code = msg.send_code('get_distance_max')
        resp_code = msg.response_code('succeed')

        # Send code
        response = ser_com.send_data(ser, send_code['code']) # Expect 1 bit?
        print('-- Response @@@@@@@@@@@', response, '---', resp_code['code'])
        if response == resp_code['code']:
            print('Response correct!')
            data = ser_com.get_message(ser) # Expect 1 bit?
            print('DATA: ', data)
        else:
            result = {"error" : True, "msg" : 'Wrong response'}
    else:
        result = {"error" : True, "msg" : 'Not connected'}

    return result


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
        new_module = identy_device(comport)
        new_devices[comport] = new_module

    return new_devices

def identy_device(comport):
    #First send identify message
    send_code = msg.send_code('detect') # Debug 5 we will see
    resp_code = msg.response_code('succeed')

    result = ser_com.identify_device(comport, send_code['code'], resp_code['code'])

    if result['error'] == False:
        return create_module(result['serial'], result['type'], comport)

    return None

def create_module(ser, type, comport):
    # TO-DO: Create module data! (or use default...?)
    data = get_data(ser)

    new_module = Module(ser,comport, type, data)
    return new_module

# Get all data from the arduino to initialize the module class
def get_data(ser):
    #

    timer = 0
    sensor_min = 0
    sensor_max = 0
    data = Module_Data(timer, sensor_min, sensor_max)
    return data
