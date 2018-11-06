import serial_controller as ser_con
import time
from module import *

def main():

    testValue = 50

    # program loop
    while(True):

        print('=============')

        #Refresh the port list, could be threaded?
        ser_con.run()

        #Returns an list of all connected devices
        current_devices = ser_con.get_devices()

        print('Current identified devices: {0}'.format(current_devices))
        print('ALL DEVICE INFO:')
        for port, device in current_devices.items():
            print('---------')
            print(device)
            #print('---------')
            print('Time reading:', ser_con.get_sensor_setting(device, 'timer')['data'])
            testValue += 300
            ser_con.set_sensor_data(device, 'timer', testValue)
            print('Time reading after setting:', ser_con.get_sensor_setting(device, 'timer')['data'])

            print('Temperature reading:', ser_con.get_sensor_setting(device, 'get_sensor_value')['data'])

            print('---------')

        # handle data of devices:
        # print('data not handled')

        print('===========')
        print('')
        print('')

        time.sleep(5) #This and import time should be removed (when main program loop is added + timed)

#####################################################


# Start program!
main()
