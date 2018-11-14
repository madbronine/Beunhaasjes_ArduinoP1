import tkinter as tk
from tkinter import *
import random
import time

# Class to store x and y position with its index (time frame)


class Point:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_index(self):
        return self.index

# Class to hold the graph


class Graph():
    # Initialize with a root frame, min value and max value
    def __init__(self, root, min_value, max_value):
        self.root = root
        self.entry = tk.Entry(root)
        stvar = tk.StringVar()
        stvar.set("one")

        # Offset from bottom and sides
        self.offset = 50  # offset from bottom

        self.min_value = min_value
        self.max_value = max_value

        # Create canvas
        self.canvas = tk.Canvas(
            root, width=550, height=450, background='white')
        self.canvas.grid(row=0, column=1)

        # reate frame
        frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky="n")

        # Update canvas to update values from canvas itself
        root.update()

        self.create_grid()
        self.create_data()

        self.data = self.create_data()  # Create data
        self.max_x = 0

        # self.create_graph_line(0, 20, 10, 18)

        # Creates grid based on size and parameters

    def create_grid(self):
        canv = self.canvas

        self.value_width = canv.winfo_width()-(self.offset * 2)
        self.value_height = canv.winfo_height()-(self.offset * 2)

        # print(self.value_width)

        value_length = 24  # max 24 items

        self.value_offset_height = round(self.value_height / value_length)

        # Starting from offset self.offset
        # our heigt = canv.winfo_height()
        # our width = canv.winfo_width()
        # amount = canv.winfo_width() - self.offset / 24
        amount = 24
        amount_box_x = round((canv.winfo_width() - self.offset) / amount)

        max_difference = self.max_value - self.min_value
        step_size = round(max_difference/amount)
        # print('max', step_size)

        self.box_size = amount_box_x
        self.step = step_size

        # create vertical lines
        for x in range(0, amount):
            start_xPos = self.offset
            end_xPos = canv.winfo_width() - self.offset
            end_yPos = canv.winfo_height() - self.offset
            canv.create_line(start_xPos + (x * amount_box_x), 0, start_xPos +
                             (x * amount_box_x), end_yPos,
                             width=1, tags="field", fill="lightgray")

        amount_box_y = round((canv.winfo_height() - self.offset) / 24)
        self.amount_boxy = amount_box_y
        max_size = self.min_value + step_size * (amount-1)

        # create horizontal lines
        for y in range(0, amount):
            start_yPos = self.offset
            end_xPos = canv.winfo_width()

            value = max_size-(step_size * y)

            canv.create_line(self.offset,
                             start_yPos + (y * amount_box_y) - self.offset,
                             end_xPos,
                             start_yPos + (y * amount_box_y) - self.offset,
                             width=1, tags="field", fill="lightgray")

            canv.create_text(self.offset/2, start_yPos + (y * amount_box_y) -
                             self.offset, fill="darkblue",
                             font="Times 7", text=value, tags="field")

            if value == 0:
                self.zero_height = start_yPos + \
                    (y * amount_box_y) - self.offset

        # Create bottom and side lines
        canv.create_line(self.offset, 0, self.offset, start_yPos + (amount *
                         amount_box_y) - self.offset,
                         width=2, tags="field", fill="black")

        canv.create_line(self.offset,
                         start_yPos + (amount * amount_box_y) - self.offset,
                         start_xPos + (amount * amount_box_x),
                         start_yPos + (amount * amount_box_y) - self.offset,
                         width=2, tags="field", fill="black")

        # print(':', self.zero_height)

    # Fill graph with data
    def create_data(self):
        # print(':', self.zero_height)

        data = list()
        length = round(self.canvas.winfo_width() / self.offset)
        for x in range(0, 25):
            v = self.zero_height
            p = Point(x, v, x)
            data.append(p)
        return data

    # Draw graphic

    def create_graph(self):
        canv = self.canvas
        # loop through data!

        first = True
        old_pos = 0

        for point in self.data:
            if first is False:
                xPos = (old_pos.get_x() - self.max_x) * self.box_size
                yPos = old_pos.get_y()
                old_x = (point.get_x() - self.max_x) * self.box_size
                old_y = point.get_y()

                old_pos = point

                self.create_graph_line(
                    old_x, old_y, xPos, yPos, point.get_index())

            else:
                old_pos = point
                first = False

    # Draw line to canvas
    def create_graph_line(self, old_x, old_y, new_x, new_y, index):
        canv = self.canvas

        # print(new_y)
        canv.create_line(old_x + 50, old_y, new_x + 50, new_y,
                         width=2, tags="data")  # Canvas.winfo_width

        canv.create_text(new_x + self.offset,
                         canv.winfo_height() - (self.offset/2),
                         fill="darkblue", font="Times 7",
                         text=index, tags="data")

    # Add data to the graph
    def add_data(self, value):
        self.data.pop(0)  # Remove first item
        # yPos = (value / self.step)
        value = self.zero_height - (value/self.step * (self.amount_boxy))
        lastx = self.data[len(self.data)-1]  # Get last list item
        p = Point(lastx.get_x() + 1, value, lastx.get_index() + 1)
        self.max_x = self.max_x + 1

        self.data.append(p)
        self.canvas.delete('data')
        self.create_graph()


if __name__ == '__main__':
    root = tk.Tk()
    gui = Graph(root, 0, 6000)  # for lux
    # gui=Graph(root, -20, 20) # for Temp
    print('Start')
    root.mainloop()
