import serial_controller as ser_con
import time

def main():
    # program loop
    while(True):
        print('=============')

        #Refresh the port list, could be threaded?
        ser_con.run()

        #Returns an list of all connected devices
        current_devices = ser_con.get_devices()
        print('Current com devices: {0}'.format(current_devices))
        #print('Test:', current_devices['COM4'])

        # handle data of devices:
        print('data not handled')

        print('===========')
        print('')
        print('')

        time.sleep(2) #This and import time should be removed (when main program loop is added + timed)

#####################################################

# Start program!
main()
