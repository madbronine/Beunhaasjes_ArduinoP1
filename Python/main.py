import serial_controller as ser_con
import gui_package.overviewgui as ui
import gui_package.welcomegui as welcomeui
import gui_package.gui as central
import time
from module import *


def main():
    centrale = central.GUI("Centrale", 300, 300)
    centrale.add_notebook()
    welcomescreen = welcomeui.WelcomeGUI(centrale)

    framelist = {}

    # program loop
    while(True):

        print('=============')

        # Refresh the port list, could be threaded?7
        ser_con.run()

        # Returns an list of all connected devices
        current_devices = ser_con.get_devices()

        print('Current identified devices: {0}'.format(current_devices))
        print('ALL DEVICE INFO:')
        if len(current_devices.items()) == 0:
            welcomescreen.device_amount(0)
        print("devices:   ", len(current_devices.items()))

        for port, device in current_devices.items():

            print('---------')
            print(device)
            print('---------')

            if device not in framelist:
                framelist[device] = ui.OverviewGUI(centrale,
                                                   device.get_type(), device)
            framelist[device].update(ser_con.get_sensor_setting(device,
                                     'get_sensor_value')['data'])
            framelist[device].updateScreenState(ser_con.get_screen_state(
                                                device))
            welcomescreen.device_amount(len(current_devices.items()))

            print('===========')
            print('')
            print('')

        todelete = []
        todeleteItem = []

        for device in framelist:
            if device.get_port() not in current_devices:
                todelete.append(framelist[device])
                todeleteItem.append(device)

        for frame in todelete:
            frame.remove()

        for item in todeleteItem:
            framelist.pop(item)
        # This and import time should be removed (when main program loop is
        # added + timed)
        time.sleep(5)

# Start program!
main()
