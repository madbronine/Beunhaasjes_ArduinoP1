import controllers
import time

def main():
    # program loop
    while(True):
        print('program loop')

        #
        controllers.find_comports()

        time.sleep(2) #This and import time should be removed (when main program loop is added + timed)


#####################################################

# Start program!
main()
