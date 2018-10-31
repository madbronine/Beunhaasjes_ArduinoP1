# © Jeroen - 30-10-2018
# This file handles connections by itself, run should be called in the main program loop
# This file can used to interact

import serial_connection.serial_handler as ser_hand
import serial_connection.serial_finder as ser_find
import messages as msg

# Dictionary containing all devices currently found
current_devices = {} # Example data: {'COM5' : 'Temperature'}

#       Code below is handled by the program
#------------------------------------------------------

#Run the controller
def run():
    print('running the controller (updating connections)')
    refresh_ports()

# Returns dictionary with all connected devices
def get_devices():
    print('Get all connected devices')
    return None # Example value:    {'com1' : Temperature, 'com2' : Light}

# Reads the sensor data from the given device
def get_sensor_data(device_com_port):
    print('Gets all sensor data')
    return None # Example value:    namedtuple('sensor_value' : 5)

# Sets the max value with parameter data for the sensor of given device
def set_sensor_max(device_com_port, value):
    command = msg.send_code('set_sensor_max')
    print('Set sensor max value. Command: {0}  value: {1}   device: {2}'.format(command, value, device_com_port))

    return None # Returns error true or false

# Sets the min value with parameter data for the sensor of given device
def set_sensor_min(device_com_port, value):
    print('Set sensor min value')
    return None # Returns error true or false

#       Code below is handled by the controller
#------------------------------------------------------

# Refreshes the dectionary devices
def refresh_ports():
    # First check if we still have every device!
    print('@ Scanning devices...')

    global current_devices

    current_devices['COM3'] = 'TYPE'

    #Find new devices
    new_devices = ser_find.get_new_ports(current_devices) # Get a list of all com ports in use

    # Refresh our current connections (and check for changes)
    print('Before testing: ', current_devices)
    current_devices = ser_find.check_ports(current_devices, new_devices) # Get a list of all com ports in use
    print('After testing: ', current_devices)

    # Check the new com devices
    print('Check for type: ', new_devices)


    #current_devices
    print('@ done scanning')


# Prepares the ardiuno for sending data
def prepare_sending(device_com_port, send_command, data):
    print('preparing to send')
    #can_send = serial_communication.send(port, command)
    print('Did we get response 10 (succeed)?, if not throw an error!')

    can_send = False # Response from arduino!

    if can_send == True:
        print('Sending data')
        send_data(device_com_port, data)
    else:
        print('Communication denied? throw error!')

# Sends data to the ardiuno
def send_data(device_com_port, data):
    print('sending data: {0} to {1}'.format(data, device_com_port))
    #result = serial_communication.send(port, command)
    # if result = response 10 (succeed), return True

    print('sending {1} to {0}')
    print('received {0}')
    print('sending data {0}')
    print('result {0}')

# DEBUG
set_sensor_max('com4', 5)
