# © Jeroen - 30-10-2018
# This file is used to interact with the modules

import serial_connection.serial_communication as ser_com
import serial_connection.serial_scanner as ser_scan
import serial_connection.messages as msg
from module import *

# Dictionary containing all devices currently found
current_devices = {}  # Example data: {'COM5' : MODULE}


#       Code below is handled by the program
# ------------------------------------------------------


# Run the controller (call with program loop)
def run():
    print('running the controller (updating connections)')

    all_ports = ser_scan.find_available_ports()  # Get all attatched comports
    not_used_ports = remove_disconnected_devices(
        all_ports)  # Get al comports NOT ine use

    if len(not_used_ports) > 0:  # If we have more then 0 unused ports
        new_devices = identify_devices(not_used_ports)  # Identify new devices
        # Update current devices with new devices
        current_devices.update(new_devices)


# Returns dictionary with all connected devices
def get_devices():
    # print('Getting all connected devices')
    # Example value:    {'com1' : Temperature, 'com2' : Light}
    return current_devices

# Reads the sensor data from the given device


def get_sensor_data(module):
    distance_min = get_sensor_setting(module, 'get_sensor_value')

    # Example value:    namedtuple('sensor_value' : 5)
    return distance_min['data']


def get_screen_state(module):
    screen_state = get_sensor_setting(module, 'current_state')
    print('STATE:  ', screen_state)
    # Example value:    namedtuple('sensor_value' : 5)
    return screen_state['data']


# Refreshes the data of the device
def refresh_device(module):
    create_data(module)
    module.set_data(module)

# Sends new settings to the arduino, returns True if done


def update_device(device, timer, sens_min, sens_max,
                  dist_min, dist_max, automatic, screen_state):
    set_sensor_data(device, 'timer', timer)
    set_sensor_data(device, 'sensor_min', sens_min)
    set_sensor_data(device, 'sensor_max', sens_max)
    set_sensor_data(device, 'distance_min', dist_min)
    set_sensor_data(device, 'distance_max', dist_max)

    set_sensor_data(device, 'toggle_manual', automatic)
    set_sensor_data(device, 'set_screen', screen_state)

    # set_sensor_data(device, 'current_state', 0)
    # used for request (like temp sensor)

    data = create_data(device)

    # Update new data
    if data is not None:
        device.set_data(data)

    return True

#       Code below is handled by the controller
# ------------------------------------------------------

# Removes disconnected devices from current_devices
# returns port not scanned yet


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

# Removes disconnected devices from current_devices
# returns port not scanned yet


def identify_devices(comports):
    print('Identifying: ', comports)

    # Dict containing new devices
    new_devices = {}

    # Identify every comport
    for comport in comports:
        print('Testing comport:', comport)

        result = identy_device(comport)  # Check every device
        if result["error"] is False:    # Didnt get an error
            new_devices[comport] = result["module"]  # Add it
        else:
            print('Not added')

    return new_devices


def identy_device(comport):
    identified_device = {"error": False, "module": None}

    # First send identify message
    send_code = msg.send_code('detect')  # Debug 5 we will see
    resp_code = msg.response_code('succeed')

    result = ser_com.identify_device(
        comport,
        send_code['code'],
        resp_code['code'])  # Result got from the arduino

    if result['error'] is False:    # If didn't get an error
        module = create_module(
            result['serial'], result['type'], comport)   # Create new module
        identified_device["error"] = False
        identified_device["module"] = module
    else:   # Error
        identified_device["error"] = True

    return identified_device


def create_module(ser, type, comport):
    # TO-DO: Create module data! (or use default...?)
    new_module = Module(ser, comport, type)
    data = create_data(new_module)

    new_module.set_data(data)
    return new_module

# Get all data from the arduino to initialize the module class


def create_data(module):
    timer = get_sensor_setting(module, 'timer')
    sensor_min = get_sensor_setting(module, 'sensor_min')
    sensor_max = get_sensor_setting(module, 'sensor_max')
    distance_min = get_sensor_setting(module, 'distance_min')
    distance_max = get_sensor_setting(module, 'distance_max')
    manual_state = get_sensor_setting(module, 'toggle_manual')

    data = Module_Data(timer['data'],
                       sensor_min['data'],
                       sensor_max['data'],
                       distance_min['data'],
                       distance_max['data'],
                       manual_state['data'])
    # data = Module_Data(timer['data'], 0,0,0,0)
    return data

# Get given sensor setting from specified module


def get_sensor_setting(module, send_cmd):
    result = {'error': False, 'message': None, 'data': None}  # Store result!
    port = module.get_port()

    isConnected = ser_scan.check_connection(port)  # Check connection
    send_code = msg.send_code(send_cmd)   # Get send code
    resp_code = msg.response_code('succeed')  # Get response code

    if isConnected is True:  # are we connected
        if send_code['error'] is False and resp_code['error'] is False:
            response = get_value(
                module, send_code['code'], resp_code['code'])  # Get data
            # print('My response: ', response)
            if response['error'] is False:
                result['error'] = False
                result['data'] = response['data']
            else:
                result['error'] = True
                result['message'] = 'Error occured'
        else:
            # Invalid code
            result['error'] = True
            result['message'] = "Invalid send or resp code!"
            print(result['message'])
    else:
        result['error'] = True
        result['message'] = "No connection!"
        print(result['message'])

    return result

# Handles sending and receiving


def get_value(module, send_code, resp_code):
    getCode = msg.send_code('get')
    result = {'error': True}
    ser = module.get_ser()

    if getCode['error'] is False:  # Code exists
        res = ser_com.send_data(ser, getCode['code'])  # Get var

        if res['data'] is 10:
            rest = ser_com.send_data(ser, send_code)  # Get var

            if rest['data'] is 10:
                result['data'] = ser_com.get_message(ser)['data']
                result['error'] = False

    else:
        # Invalid code
        result['error'] = True
        result['message'] = "Invalid get code!"
        print(result['message'])

    return result


# Handles sending and receiving
def set_sensor_data(module, send_code, value):
    ser = module.get_ser()
    var = msg.send_code(send_code)['code']

    res = ser_com.send_data(ser, 14)  # Get var

    if res['data'] == 10:
        rest = ser_com.send_data(ser, var)  # Get var
        if rest['data'] == 10:
            # final = get_message(ser)['data']
            ser_com.send_word(ser, value)
