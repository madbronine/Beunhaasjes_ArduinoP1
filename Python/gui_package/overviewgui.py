from tkinter import *
import gui_package.gui as ui
import gui_package.graph_builder as graph
import serial_controller as ser_con

class OverviewGUI():

    temperature = 0.0
    lux = 0

    sensorMin = -10
    sensorMax = 40
    minDist = 10
    maxDist = 200
    interval = 40
    finalInterval = 40
    screen_state = True
    automatic = False
    readingOffset = 6
    stopped = True


    type = "UNKNOWN"
    sunscreenStatus = "Ingerold"

    # Constructor
    def __init__(self, root, type, device):
        self.type = type
        self.gui = root
        self.vartype = IntVar()
        self.device = device
        self.isset = False
        self.build()

    # Update method for the rol in/rol out radiobuttons
    def radioButton(self):
        self.screen_state = not self.screen_state

    # Sends settings to Arduino
    def sendSettings(self):
        self.progressbar['maximum']=(self.interval) * 100 + self.readingOffset
        if self.type == "TEMP":
            ser_con.update_device(self.device, int(self.interval), int(self.sensorMin * 10), int(self.sensorMax * 10), int(self.minDist), int(self.maxDist), int(not self.automatic), int(self.screen_state))
        elif self.type == "LIGHT":
            ser_con.update_device(self.device, int(self.interval), int(self.sensorMin), int(self.sensorMax), int(self.minDist), int(self.maxDist), int(not self.automatic), int(self.screen_state))
        self.progressbar.stop()
        self.stopped = True
        self.finalInterval = int(self.interval)

    # Builds the UI elements
    def build(self):
        mainframe = self.gui.add_frame(self.gui.notebook, 0, 0, 1, 1)
        self.mainframe = mainframe

        sensorFrame = self.gui.add_frame(mainframe, 0, 1, 1, 1)
        sunscreenFrame = self.gui.add_frame(mainframe, 0, 3, 1, 1)
        graphFrame = self.gui.add_frame(mainframe, 1, 0, 1, 4)

        sensorFrameTitle = self.gui.add_label(mainframe, "Sensor", 0, 0)
        sensorFrameTitle['padding'] = 8
        sensorFrameTitle['font'] = ("unspecified", 18)
        sensorFrameTitle['anchor'] = CENTER
        sunscreenFrameTitle = self.gui.add_label(mainframe, "Zonnescherm", 0, 2)
        sunscreenFrameTitle['padding'] = 8
        sunscreenFrameTitle['font'] = ("unspecified", 18)
        sunscreenFrameTitle['anchor'] = CENTER
        if self.type == "TEMP":
            self.my_graph = graph.Graph(graphFrame, -10, 30)
        elif self.type == "LIGHT":
            self.my_graph = graph.Graph(graphFrame, 0, 6000)

        if self.type == "TEMP":

            self.tempText = self.gui.add_label(sensorFrame, "20.3 °C", 1, 3)
            self.tempText['padding'] = 8
            self.gui.add_action(self.updateTemp)
            self.minslider = self.gui.add_slider(sensorFrame, 0, 30, 1, 0, 1, 1)
            self.minslider['command']=self.updateSensorMinMax
            self.maxslider = self.gui.add_slider(sensorFrame, 15, 50, 1, 1, 1, 1)
            self.maxslider['command']=self.updateSensorMinMax

        elif self.type == "LIGHT":
            self.gui.add_label(sensorFrame, "Licht", 0, 0)['padding'] = 8
            self.luxText = self.gui.add_label(sensorFrame, "150 Lux", 1, 3)
            self.luxText['padding'] = 8
            self.gui.add_action(self.updateLight)
            self.minslider = self.gui.add_slider(sensorFrame, 0, 1000, 1, 0, 1, 1)
            self.minslider['command']=self.updateSensorMinMax
            self.maxslider = self.gui.add_slider(sensorFrame, 200, 6000, 1, 1, 1, 1)
            self.maxslider['command']=self.updateSensorMinMax
        else:
            print("Unkown device type")

        self.minText = self.gui.add_label(sensorFrame, "Min: 100", 0, 0)
        self.minText['padding'] = 8
        self.maxText = self.gui.add_label(sensorFrame, "Max: 200", 0, 1)
        self.maxText['padding'] = 8

        self.intervalText = self.gui.add_label(sensorFrame, "Interval:", 0, 2)
        self.intervalText['padding'] = 8
        self.intervalSlider = self.gui.add_slider(sensorFrame, 1, 12, 1, 2, 1, 1)
        self.intervalSlider['command']=self.updateInterval
        self.intervalSlider['variable']=IntVar()
        self.gui.add_label(sensorFrame, "Huidig:", 0, 3)['padding'] = 8

        self.gui.add_label(sensorFrame, "Refresh:", 0, 4)['padding'] = 8
        self.progressbar = self.gui.add_progressbar(sensorFrame, "determinate", 1, 4, 4)
        self.progressbar.start(10)

        self.minDistSlider = self.gui.add_slider(sunscreenFrame, 5, 50, 1, 0, 1, 1)
        self.minDistSlider['command']=self.updateDistMinMax
        self.minDistSlider['variable']=IntVar()
        self.maxDistSlider = self.gui.add_slider(sunscreenFrame, 10, 400, 1, 1, 1, 1)
        self.maxDistSlider['command']=self.updateDistMinMax
        self.maxDistSlider['variable']=IntVar()

        self.minDistText = self.gui.add_label(sunscreenFrame, "Min:", 0, 0)
        self.minDistText['padding'] = 8
        self.gui.add_checkbutton(sunscreenFrame, "Automatisch", 2, 0, self.checkbox)
        self.maxDistText = self.gui.add_label(sunscreenFrame, "Max:", 0, 1)
        self.maxDistText['padding'] = 8
        self.gui.add_radiobutton(sunscreenFrame, "Rol in", self.vartype, 0, self.radioButton, 2, 1)

        self.gui.add_label(sunscreenFrame, "Status:", 0, 2)['padding'] = 8
        self.sunScreenStatusText = self.gui.add_label(sunscreenFrame, "Ingerold", 1, 2)
        self.sunScreenStatusText['padding'] = 8

        self.gui.add_radiobutton(sunscreenFrame, "Rol out", self.vartype, 1, self.radioButton, 2, 2)

        self.gui.add_button(sunscreenFrame, "Update Settings", 0, 3, self.sendSettings, 3, 2)

        sensorFrame['padding'] = 8
        sunscreenFrame['padding'] = 8

        data = self.device.get_data()
        self.updateValues(data.get_timer(), data.get_setting_min(), data.get_setting_max(), data.get_setting_min_distance(), data.get_setting_max_distance(), 1, 0)

        self.gui.notebook.add(mainframe, text=self.type)

        self.isset = True

    # Updates all the values of the class
    def updateValues(self, interval, tempMin, tempMax, distMin, distMax, automatic, screen_state):
        self.interval = interval
        if self.type == "TEMP":
            self.sensorMin = float(tempMin) * 0.1
            self.sensorMax = float(tempMax) * 0.1
        elif self.type == "LIGHT":
            self.sensorMin = tempMin
            self.sensorMax = tempMax

        self.minDist = distMin
        self.maxDist = distMax
        self.automatic = automatic
        self.screen_state = screen_state

        self.intervalSlider.set(interval * 0.2)
        self.maxDistSlider.set(distMax)
        self.minDistSlider.set(distMin)
        self.progressbar['maximum']=(self.interval) * 100 + 20

        self.minslider.set(self.sensorMin)
        self.maxslider.set(self.sensorMax)
        self.updateDistMinMax(None)
        self.updateSensorMinMax(None)
        self.updateInterval(None)

    # Updates screen state
    def updateScreenState(self, state):
        self.sunscreenStatus = state
        word = "Unknown"
        if state == 0:
            word = "Opgerold."
        elif state == 1:
            word = "Rollen..."
        elif state == 2:
            word = "Uitgerold."
        self.sunScreenStatusText['text'] = word

    # Updates the main sensor value
    def update(self, value):
        if value == None:
            return

        if self.stopped == True:
            self.progressbar.start(10)
            self.stopped = False
            self.step = 0

        self.step = self.step + 1

        if self.step >= int(self.finalInterval * 0.2):
            if self.type == "TEMP":
                self.temperature = value * 0.1
                self.my_graph.add_data(self.temperature)
                self.updateTemp()
            elif self.type == "LIGHT":
                self.lux = value
                self.my_graph.add_data(self.lux)
                self.updateLight()
            self.step = 0

    # Updates the min and max distance values
    def updateDistMinMax(self, value):
        self.minDist = int(self.minDistSlider.get())
        self.maxDist = int(self.maxDistSlider.get())

        if self.minDist > self.maxDist:
            self.maxDist = self.minDist
            self.maxDistSlider.set(self.maxDist)

        if self.maxDist < self.minDist:
            self.minDist = self.maxDist
            self.minDistSlider.set(self.maxDist)

        self.minDistText['text'] = "Min: {} cm".format(self.minDist)
        self.maxDistText['text'] = "Max: {} cm".format(self.maxDist)

    # Updates the min and max sensor values
    def updateSensorMinMax(self, value):
        if self.isset == True:
            self.sensorMin = self.minslider.get()
            self.sensorMax = self.maxslider.get()

        if self.sensorMin > self.sensorMax :
            self.sensorMax = self.sensorMin
            self.maxslider.set(self.sensorMax)

        if self.type == "LIGHT":
            self.minText['text'] = "Min: {} Lux".format(int(self.sensorMin))
            self.maxText['text'] = "Max: {} Lux".format(int(self.sensorMax))
        elif self.type == "TEMP":
            self.minText['text'] = "Min: %.1f °C" % self.sensorMin
            self.maxText['text'] = "Max: %.1f °C" % self.sensorMax

    # Updates the interval slider and related text
    def updateInterval(self, value):
        self.interval = int(int(self.intervalSlider.get()) * 5)
        if self.interval < 60:
            self.intervalText['text']="Interval: {} s".format(self.interval)
        else:
            self.intervalText['text']="Interval: {} m".format(int(self.interval / 60))

    # removes the tab from notebook
    def remove(self):
        self.gui.notebook.forget(self.mainframe)

    # updates temperature text
    def updateTemp(self):
        self.tempText['text'] = "%.1f °C" % self.temperature

    # updates checkbox value
    def checkbox(self):
        self.automatic = not self.automatic

    # updates lux text
    def updateLight(self):
        self.luxText['text'] = "{} Lux".format(self.lux)
