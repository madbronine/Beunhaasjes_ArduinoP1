import serial_controller as ser_con
import time

def main():
    # program loop
    while(True):
        print('=============')

        #Refresh the port list
        ser_con.run()

        curDevices = ser_con.get_devices()
        print('Current com devices: {0}'.format(curDevices))

        print('===========')
        print('')
        print('')

        time.sleep(2) #This and import time should be removed (when main program loop is added + timed)

#####################################################

# Start program!
main()
