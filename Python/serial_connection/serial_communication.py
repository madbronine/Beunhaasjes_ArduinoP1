# © Jeroen - 31-10-2018
# This file handles: Sending and receiving data from modules

import serial
import time

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





#       Code below is for DEBUGGING
#------------------------------------------------------

def test_loop():

    test_ser = initialize_serial('COM4', 2)

    while True:
        print('start')
        time.sleep(2)
        dataLength = 4
        result = send_data(test_ser, 5, dataLength) # Debug case -> 5 returns TYPE if dataLength = 2 it returns TY 
        time.sleep(2)
        result = send_data(test_ser, 6, 4) # expect response of 2 bytes


        time.sleep(5)
        print('stop')
        time.sleep(5)


        # send_data(ser, 5, 4)
        #
        # print('-------------')
        #
        # time.sleep(2)
        # send_data(ser, 1, 4)
        #
        # print('-------------')
        #
        # time.sleep(2)
        # send_data(ser, 102, 4)
        #
        # print('-------------')


        #time.sleep(2)
        #send_data(ser, 5, 4)



test_loop()
