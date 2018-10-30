import serial
from serial.tools import list_ports

# Returns a list with ports that are currently attached
def get_ports(available_ports):
    # Get all comports connected
    ports = list_ports.comports()   #list of all ports connected
    result = []                     #list to store comports

    for port in ports:
        port_found = port[0]        #port that has been found
        result.append(port_found)   #add port to the list

    return result


# Handles module searching
def find_available_ports():
    ports = list_ports.comports()   #list of all ports connected
    result = []                     #list of ports (com ID)


    for port in ports:
        result.append(port)   #add port to the list

    # Return the list
    return result

# Check if ports are new, existing or disconnected
def check_ports(available_ports, found_ports):
    ports_to_remove = []

    #For each old port
    for port in available_ports:
        if port in found_ports:
            found_ports.remove(port)
        else:
            ports_to_remove.append(port)

    for port in ports_to_remove:
        found_modules.pop(port)

    return {}
