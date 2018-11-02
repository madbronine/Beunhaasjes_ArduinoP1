# © Jeroen - 31-10-2018
# This file handles: Sending and receiving data from modules

import serial
import time

# Identifies the device on comport
def identify_device(com_port, cmd, res):
    # Here do we store results
    result = {}

    # create serial with comport and max timeout 2 seconds
    ser = initialize_serial(com_port, 2)

    # Give serial Initialize time
    time.sleep(2)

    # Send our command + expected result length
    response = send_data(ser, cmd)

    # if response matched expected result command
    if response == res:
        # Get the next text messages with the ID
        msg = get_text_message(ser,  4) # expect 4 bits return result
        # Fill in the result
        result['error'] = False
        result['type'] = msg
        result['serial'] = ser
    else:
        # Not expected! Fill in the result
        result['error'] = True

    # returns the message: error, type and serial
    return result


# Creates a serial connection
def initialize_serial(com_port, time_out):
    #Initialize serial connection based on parameters
    ser = serial.Serial(
       port = com_port,
       baudrate = 19200,
       bytesize = serial.EIGHTBITS,
       parity = serial.PARITY_NONE,
       stopbits = serial.STOPBITS_ONE,
       timeout = time_out
    )
    # Returns serial connection
    return ser


# Sends data to the module
def send_data(ser, data_to_send):
    # If we missed data which we didn't need, remove it, otherwish this will conflict new data!
    ser.flushInput();

    # Debug line:
    #print('Going to send int: ', data_to_send)

    # Convert data to bytes
    converted_data = bytearray([data_to_send])

    # Debug line:
    #print('converted:', converted_data, '- type:', type(converted_data))

    # Send data
    ser.write(converted_data)

    # Get response message
    response = get_message(ser)

    # Return the response message
    return response

# Returns data from the module
def get_message(ser):
    # Retrieve data!
    msga = ser.readline()

    # Debug line:
    #print('received: ', msga, type(msga))
    # Create int from 2 bytes (little endian)
    val = int.from_bytes(msga, "little")
    return val


# Get an character messe
def get_text_message(ser, length):
    # Retrieve data!
    msg = ser.readline()
    val = int.from_bytes(msg, "little")

    # Decode the message
    dec_msg = msg.decode()

    # Debug line:
    #print('Module returns:', msg, '- Decoded:', dec_msg)
    return msg.decode()
