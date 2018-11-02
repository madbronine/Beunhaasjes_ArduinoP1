# © Jeroen - 30-10-2018
# file containing class for modules

#Class containg modules
class Module:
    # Module contains its data, so we can use it
    def __init__(self, ser, port, type):
        self.ser = ser    # com-port
        self.port = port    # com-port
        self.type = type    # com-type

    # returns the com-port
    def get_ser(self):
        return self.ser

    # returns the com-port
    def get_port(self):
        return self.port

    # returns the type of module
    def get_type(self):
        return self.type

    # returns the data
    def get_data(self):
        return self.module_data

    # Sets the data
    def set_data(self, module_data):
        self.module_data = module_data

    def __str__(self):
        return "Port: {0} \nser: {1} \ntype: {2} \ndata: {3}".format(self.port, self.ser, self.type, self.module_data)



# Class containing the data of the modules
class Module_Data:
    def __init__(self, timer, sensor_min, sensor_max):
        self.timer = timer    # com-port
        self.sensor_min = sensor_min    # com-type
        self.sensor_max = sensor_max      # serial class

    # Sets the timer setting
    def set_timer(self, timer):
        self.timer = timer

    # Sets the timer setting
    def set_sensor_min(self, sensor_min):
        self.setting_min = sensor_min

    def set_sensor_max(self, sensor_max):
        self.setting_max = sensor_max

    def get_timer(self):
        return self.timer

    def get_setting_min(self):
        return self.sensor_min

    def get_setting_max(self):
        return self.sensor_max

    def __str__(self):
        return "Port: {0} type: {1} data: {2}".format(self.timer, self.sensor_min, self.sensor_max)
