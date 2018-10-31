# © Jeroen - 30-10-2018
# file containing messages for communication

import collections

# Returns a send code based on the type. Returns error if it's not existing
def send_code(message):
    if message in send_messages:
        # Message exists. Fill response
        return {'error' : False, 'message': message, 'code' : send_messages[message]}
    else:
        # Not existing message return error
        return {'error' : True}


# messages modules can receive
send_messages = {
"detect" : 10,      # Send detecton message (module should response with a 10)
"succeed" : 11,
"request_id" : 12,   # Request id (module should response with response with 12)


"set_timer" : 20,       # Request to change timer (should response with 12)
"set_sensor_min" : 21,  # Request to change sensor min value (should response with 12)
"set_sensor_max" : 22,  # Request to change sensor max value (should response with 12)

}

# messages modules can send
response_messages = {
10 : "succeed", # Getting data
11 : "error",   # Error received
12 : "data",    # Incomming data (send 11 to receive data)

20 : "sensor"   # Request sensor data
}
