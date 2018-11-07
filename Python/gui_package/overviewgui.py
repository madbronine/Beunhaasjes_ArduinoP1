import gui_package.gui as ui

class OverviewGUI():

    gui = None
    slider = None
    number = 1;

    def __init__(self):
        gui = ui.GUI("Centrale", 500, 200)
        self.gui = gui
        self.build()
        self.gui.add_action(self.updateSlider)

    def build(self):
        self.gui.add_label("Temp", 1, 1)
        self.gui.add_button("0024", 2, 1, None)
        self.gui.add_button("22,2", 3, 1, None)
        self.gui.add_label("°C", 4, 1)

        self.gui.add_label("UV", 1, 2)
        self.gui.add_button("2", 2, 2, None)
        self.gui.add_button("3", 3, 2, None)
        self.gui.add_label("Sun", 4, 2)

        slider = self.gui.add_slider(0, 100, 2, 3)
        self.slider = slider

    def update(self, temp):
        return 1

    def updateSlider(self):
        self.slider['label'] = "{}".format(self.number)
        self.number = self.number + 1
