from tkinter import *
import gui_package.gui as ui
import gui_package.graph_builder as graph
import serial_controller as ser_con

class OverviewGUI():

    device = None

    gui = None
    mainframe = None

    temperature = 0.0
    lux = 0

    type = "UNKNOWN"

    tempText = None
    luxText = None

    minDistSlider = None
    maxDistSlider = None

    minDistText = None
    maxDistText = None

    intervalSlider = None

    minText = None
    maxText = None

    min = -10
    max = 40
    minDist = 10
    maxDist = 200
    interval = 40
    screen_state = True
    automatic = False

    sunscreenStatus = "Ingerold"

    def __init__(self, root, type, device):
        self.type = type
        self.gui = root
        self.vartype = IntVar()
        self.device = device
        self.isset = False
        self.build()

    def radioButton(self):
        self.screen_state = not self.screen_state

    def sendSettings(self):
        if self.type == "TEMP":
            ser_con.update_device(self.device, int(self.interval), int(self.min * 10), int(self.max * 10), int(self.minDist), int(self.maxDist), int(not self.automatic), int(self.screen_state))
        elif self.type == "LIGHT":
            ser_con.update_device(self.device, int(self.interval), int(self.min), int(self.max), int(self.minDist), int(self.maxDist), int(not self.automatic), int(self.screen_state))

    def build(self):
        mainframe = self.gui.add_frame(self.gui.notebook, "grey", 0, 0, 1, 1)
        self.mainframe = mainframe

        sensorFrame = self.gui.add_frame(mainframe, "grey", 0, 0, 1, 1)
        sunscreenFrame = self.gui.add_frame(mainframe, "grey", 0, 1, 1, 1)
        graphFrame = self.gui.add_frame(mainframe, "grey", 1, 0, 1, 2)

        # graph.build(graphFrame, 'Tijd', 'Temperatuur in ℃',  -20, 50)

        if self.type == "TEMP":
            self.gui.add_label(sensorFrame, "Temperatuur", 0, 0)['padding'] = 8
            self.tempText = self.gui.add_label(sensorFrame, "20.3 °C", 1, 3)
            self.tempText['padding'] = 8
            self.gui.add_action(self.updateTemp)
            self.gui.add_label(sensorFrame, "Min", 3, 0)['padding'] = 8
            self.minslider = self.gui.add_slider(sensorFrame, 0, 30, 3, 1, 1, 3)
            self.minslider['orient']=VERTICAL
            self.minslider['command']=self.updateTempMinMax
            self.gui.add_label(sensorFrame, "Max", 4, 0)['padding'] = 8
            self.maxslider = self.gui.add_slider(sensorFrame, 15, 50, 4, 1, 1, 3)
            self.maxslider['orient']=VERTICAL
            self.maxslider['command']=self.updateTempMinMax

        elif self.type == "LIGHT":
            self.gui.add_label(sensorFrame, "Licht", 0, 0)['padding'] = 8
            self.luxText = self.gui.add_label(sensorFrame, "150 Lux", 1, 3)
            self.luxText['padding'] = 8
            self.gui.add_action(self.updateLight)
            self.gui.add_label(sensorFrame, "Min", 3, 0)['padding'] = 8
            self.minslider = self.gui.add_slider(sensorFrame, 0, 1000, 3, 1, 1, 3)
            self.minslider['orient']=VERTICAL
            self.minslider['command']=self.updateTempMinMax
            self.gui.add_label(sensorFrame, "Max", 4, 0)['padding'] = 8
            self.maxslider = self.gui.add_slider(sensorFrame, 200, 10000, 4, 1, 1, 3)
            self.maxslider['orient']=VERTICAL
            self.maxslider['command']=self.updateTempMinMax
        else:
            print("Unkown device type")

        self.minText = self.gui.add_label(sensorFrame, "Min: 100", 1, 0)
        self.minText['padding'] = 8
        self.maxText = self.gui.add_label(sensorFrame, "Max: 200", 1, 1)
        self.maxText['padding'] = 8

        self.gui.add_label(sensorFrame, "Interval:", 0, 2)['padding'] = 8
        self.intervalSlider = self.gui.add_slider(sensorFrame, 2, 60, 1, 2, 1, 1)
        self.intervalSlider['command']=self.updateInterval
        self.intervalSlider['variable']=IntVar()
        self.gui.add_label(sensorFrame, "Huidig:", 0, 3)['padding'] = 8

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

        self.gui.add_button(sunscreenFrame, "Update Settings", 0, 3, self.sendSettings, 3)

        sensorFrame['padding'] = 8
        sunscreenFrame['padding'] = 8

        data = self.device.get_data()
        self.updateValues(data.get_timer(), data.get_setting_min(), data.get_setting_max(), data.get_setting_min_distance(), data.get_setting_max_distance(), 1, 0)

        self.gui.notebook.add(mainframe, text=self.type)

        self.isset = True

    def updateValues(self, interval, tempMin, tempMax, distMin, distMax, automatic, screen_state):
        self.interval = interval
        if self.type == "TEMP":
            self.min = float(tempMin) * 0.1
            self.max = float(tempMax) * 0.1
        elif self.type == "LIGHT":
            self.min = tempMin
            self.max = tempMax

        self.minDist = distMin
        self.maxDist = distMax
        self.automatic = automatic
        self.screen_state = screen_state

        self.intervalSlider.set(interval)
        self.maxDistSlider.set(distMax)
        self.minDistSlider.set(distMin)

        self.minslider.set(self.min)
        self.maxslider.set(self.max)
        self.updateDistMinMax(None)
        self.updateTempMinMax(None)
        self.updateInterval(None)

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

    def update(self, value):
        if value == None:
            return

        if self.type == "TEMP":
            self.temperature = value * 0.1
            self.updateTemp()
        elif self.type == "LIGHT":
            self.lux = value
            self.updateLight()

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

    def updateTempMinMax(self, value):
        if self.isset == True:
            self.min = self.minslider.get()
            self.max = self.maxslider.get()

        if self.min > self.max :
            self.max = self.min
            self.maxslider.set(self.max)

        if self.type == "LIGHT":
            self.minText['text'] = "Min: {} Lux".format(int(self.min))
            self.maxText['text'] = "Max: {} Lux".format(int(self.max))
        elif self.type == "TEMP":
            self.minText['text'] = "Min: %.1f °C" % self.min
            self.maxText['text'] = "Max: %.1f °C" % self.max

    def updateInterval(self, value):
        self.interval = int(self.intervalSlider.get())

    def remove(self):
        self.gui.notebook.forget(self.mainframe)

    def updateTemp(self):
        self.tempText['text'] = "%.1f °C" % self.temperature

    def checkbox(self):
        self.automatic = not self.automatic

    def updateLight(self):
        self.luxText['text'] = "{} Lux".format(self.lux)
