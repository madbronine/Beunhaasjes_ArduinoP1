# © Jeroen - 31-10-2018
# This file handles: Sending and receiving data from modules

import serial
import time


def identify_device(com_port, cmd, res):
    result = {}

    # create serial with comport and max timeout 2 seconds
    ser = initialize_serial(com_port, 2)

    # Give serial Initialize time
    time.sleep(2)

    #expect 1 bit data back!
    datalength = 1
    # Send our command + expected result length
    response = send_data(ser, cmd, datalength)

    # if response matched expected result command
    if response == res:
        msg = get_message(ser,  4) # expect 4 bits return result
        result['error'] = False
        result['type'] = msg
        result['serial'] = ser
    else:
        result['error'] = True

    # returns error, type and serial
    return result



def initialize_serial(com_port, time_out):
    #Initialize serial connection
    ser = serial.Serial(
       port = com_port,
       baudrate = 19200,
       bytesize = serial.EIGHTBITS,
       parity = serial.PARITY_NONE,
       stopbits = serial.STOPBITS_ONE,
       timeout = time_out
    )
    return ser


# Sends data to the module
def send_data(ser, data_to_send, response_length):
    ser.flushInput(); # If we missed data which we didn't need, remove it, otherwish this will conflict new data!

    print('Going to send int: ', data_to_send)

    #converted_data = [data_to_send]
    converted_data = bytearray([data_to_send])

    print('converted:', converted_data, '- type:', type(converted_data))
    ser.write(converted_data)

    msg = get_message(ser, response_length)

    return msg

# Returns data from the module
def get_message(ser, length):
    msg = ser.read(length) # read max (length) bytes

    if len(msg) > 1:
        dec_msg = msg.decode()
        print('Module returns:', msg, '- Decoded:', dec_msg)
        return msg.decode() # message is an int
    else:
        dec_msg = ord(msg.decode())
        print('Module returns:', msg, '- Decoded:', dec_msg)
        return dec_msg # message is an int
