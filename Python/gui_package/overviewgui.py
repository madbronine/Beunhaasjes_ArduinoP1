import gui_package.gui as ui

class OverviewGUI():

    gui = None
    tempSlider = None
    tempText = None
    temperature = 1;

    def __init__(self):
        gui = ui.GUI("Centrale", 500, 200)
        self.gui = gui
        self.build()
        self.gui.add_action(self.updateSlider)

    def build(self):
        self.gui.add_label("Temp", 1, 1)
        self.gui.add_button("0024", 2, 1, None)
        self.tempText = self.gui.add_label("##,# °C", 3, 1)

        self.gui.add_label("UV", 1, 2)
        self.gui.add_button("2", 2, 2, None)
        self.gui.add_button("3", 3, 2, None)
        self.gui.add_label("Sun", 4, 2)

        slider = self.gui.add_slider(100, 400, 2, 3)
        self.tempSlider = slider

    def update(self, temp):
        self.temperature = temp

    def updateSlider(self):
        if(self.tempSlider == None):
            return
        self.tempSlider.set(self.temperature)
        self.tempText['text'] = "{} °C".format(self.temperature * 0.1)
