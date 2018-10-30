import controller
import time

def main():
    # program loop
    while(True):
        print('=============')

        #Refresh the port list
        controller.run()
        print('Current com devices: {0}'.format(controller.get_modules()))

        print('===========')
        print('')
        print('')

        time.sleep(2) #This and import time should be removed (when main program loop is added + timed)

#####################################################

# Start program!
main()
