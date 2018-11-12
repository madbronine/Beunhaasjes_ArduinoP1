# © Jeroen - 31-10-2018
# This file handles: Sending and receiving data from modules

import serial
import time

# Identifies the device on comport
def identify_device(com_port, cmd, res):
    # Here do we store results
    result = {}

    # create serial with comport and max timeout 2 seconds

    try:
        ser = initialize_serial(com_port, 4)
    except (OSError, serial.SerialException):
        print('ERROR:', com_port, '- COM IN USE')
        result['error'] = True
        return result
    pass

    # Give serial Initialize time
    time.sleep(2)

    # Send our command + expected result length
    response = send_data(ser, cmd)

    if response['error'] == False:
        # if response matched expected result command
        if response['data'] == res:
            # Get the next text messages with the ID
            msg = get_text_message(ser)

            if msg['error'] == False:
                # Fill in the result
                result['error'] = False
                result['type'] = msg['data']
                result['serial'] = ser
            else:
                result['error'] = True
        else:
            # Not expected! Fill in the result
            result['error'] = True
    else:
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


# Sends data to the module with a response
def send_data(ser, data_to_send):
    response = {'error' : True, 'data' : None}

    transmit_data(ser, data_to_send);

    # Get response message
    response = get_message(ser)

    # Return the response message
    return response


# Sends data to the module (doesn't handle any responses)
def transmit_data(ser, data_to_send):
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


# Returns data from the module, msg_length is by default high and low byte
def get_message(ser):
    response = {'error' : True, 'data' : None}
    # Retrieve data!
    bytes = read_untill_eol(ser)

    if bytes['error'] == True: # Got an error
        response['error'] = True
        return response
    # Debug line:
    #print('received: ', msga, type(msga))
    # Create signed int from 2 bytes (little endian)
    val = int.from_bytes(bytes['data'], "little", signed=True)
    # Debug value
    #print('Value is: ', val)
    response['error'] = False;
    response['data'] = val;


    return response


# Get an character messe
def get_text_message(ser):
    response = {'error': True, 'data' : None}
    bytes = read_untill_eol(ser)

    if bytes['error'] == False:
        response['data'] = bytes['data'].decode() # Decode the message
        response['error'] = False

    # Debug line:
    #print('Module returns:', msg, '- Decoded:', dec_msg)
    return response

def read_untill_eol(ser):
    message = {'error' : False, 'data' : None}
    eol = '\r'
    eol = str.encode(eol)
    done = False

    bytes = bytearray()

    while done == False:
        value = ser.read(1) # Retrieve data!

        if value == eol:
            done = True
        elif value == b'': # if we got an empty byte
            message['error'] = True
            done = True
        else:
            bytes.extend(value)

    message['data'] = bytes


    return message # return the message

# Sends an 16 bit signed int (in low and high byte)
def send_word(ser, value):
    #print('result', value)

    # Split int to two bytes
    result = split_int(value);
    #print('result (split)', result)

    #Send low and high byte
    transmit_data(ser, result['low'])
    transmit_data(ser, result['high'])


# Splits value in 2 bytes (low, high)
def split_int(value):
    result = {'low' : value // 256, 'high' : value % 256}
    return result
