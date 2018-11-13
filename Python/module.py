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
    def __init__(self, timer, sensor_min, sensor_max, distance_min, distance_max, toggle_manual):
        self.timer = timer                  # Timer value in MS ??
        self.sensor_min = sensor_min        # Sensor min value
        self.sensor_max = sensor_max        # Sensor max value
        self.distance_min = distance_min    # Distance sensor min value
        self.distance_max = distance_max    # Distance sensor max value

        self.toggle_manual = toggle_manual

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

    def get_setting_min_distance(self):
        return self.distance_min

    def get_setting_max_distance(self):
        return self.distance_max

    def get_manual(self):
        return self.toggle_manual

    def __str__(self):
        return "Timer: {0} sensor_min: {1} sensor_max: {2}  dist_min: {3}  dist_max: {4} manual: {5} ".format(self.timer, self.sensor_min, self.sensor_max, self.distance_min, self.distance_max, self.toggle_manual)
