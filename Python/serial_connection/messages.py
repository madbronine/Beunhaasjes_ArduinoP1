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
"detect" : 10,      # Send detecton message (module should response with a 10)
"request_id" : 12,   # Request id (module should response with response with 12)
"get_sensor_value" : 13,  # Request sensor value
"set" : 14,  # update setting
"get" : 15,  # retrieve setting


"timer" : 20,       # Request to change timer (should response with 11)
"sensor_min" : 22,  # Request to change sensor min value (should response with 11)
"sensor_max" : 24,  # Request to change sensor min value (should response with 11)
"distance_min" : 26,  # Request to get sensor min value (should response with 11)
"distance_max" : 28,  # Request to change sensor max value (should response with 11)
"current_state" : 30  # Request current sunscreen state


}

# messages modules can send
response_messages = {
"succeed" : 10, # Getting data
"error" : 11,   # Error received
"data" : 12,    # Send data

}
