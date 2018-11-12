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

def response_code(code):
    if code in response_messages:
        # Response exists. Fill response
        return {'error' : False, 'message': code, 'code' : response_messages[code]}
    else:
        # Not existing message return error
        return {'error' : True}



# messages modules can receive
send_messages = {
"detect" : 10,      # Send detecton message
"request_id" : 12,   # Request id
"get_sensor_value" : 13,  # Request sensor value
"set" : 14,  # update setting
"get" : 15,  # retrieve setting


"timer" : 20,           # Request to change sensor measure timer
"sensor_min" : 22,      # Request to change sensor min value
"sensor_max" : 24,      # Request to change sensor min value
"distance_min" : 26,    # Request to change distance sensor min value
"distance_max" : 28,    # Request to change distance sensor max value
"current_state" : 30,   # Request current sunscreen state
"toggle_manual" : 32,   # Request to change to manual
"set_screen" : 34       # Request to change sun_screen status

}

# messages modules can send
response_messages = {
"succeed" : 10, # Getting data
"error" : 11,   # Error received
"data" : 12,    # Send data

}
