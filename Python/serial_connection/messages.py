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
"succeed" : 11,
"request_id" : 12,   # Request id (module should response with response with 12)

"set_timer" : 20,       # Request to change timer (should response with 11)
"get_timer" : 21,       # Request to change timer (should response with 11)
"set_sensor_min" : 22,  # Request to change sensor min value (should response with 11)
"get_sensor_min" : 23,  # Request to get sensor min value (should response with 11)
"set_sensor_max" : 24,  # Request to change sensor max value (should response with 11)
"get_sensor_max" : 25,  # Request to change sensor max value (should response with 11)

}

# messages modules can send
response_messages = {
"succeed" : 10, # Getting data
"error" : 11,   # Error received
"data" : 12,    # Incomming data (send 11 to receive data)

"sensor" : 20   # Request sensor data
}
