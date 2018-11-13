import tkinter as tk
from tkinter import *
import random
import threading
import time

continuePlotting = False



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

class Graph():
    def __init__(self, root):
        self.root=root
        self.entry = tk.Entry(root)
        stvar=tk.StringVar()
        stvar.set("one")
        self.offset = 20

        self.canvas=tk.Canvas(root, width=480, height=360, background='white')
        self.canvas.grid(row=0,column=1)

        frame = Frame(self.root)
        frame.grid(row=0,column=0, sticky="n")

        #figure1=self.canvas.create_rectangle(80, 80, 120, 120, fill="blue")

        root.update()

        self.data = self.create_data() # Create data

        self.max_x = 0

        thread = threading.Thread(target = self.generate)
        thread.start()

        #self.create_graph_line(0, 20, 10, 18)

    def create_data(self):
        data = list()
        length = round(self.canvas.winfo_width() / self.offset)
        for x in range(length):
            v = 0
            p = Point(x, v, x)
            data.append(p)
        return data


    def add_data(self, yPos):
        self.data.pop(0) # Remove first item


        lastx = self.data[len(self.data)-1] # Get last list item
        p = Point(lastx.get_x() + 1, yPos, lastx.get_index() + 1)
        self.max_x = self.max_x + 1

        self.data.append(p)


    def generate(self):
        self.create_grid()
        while True:
            v = random.randrange(0, 20)
            self.add_data(v)
            self.canvas.delete('data')
            self.create_graph()
            time.sleep(1)

    def create_grid(self):
        canv = self.canvas


        start_x = 25
        start_y = canv.winfo_height() - 25
        end_x = canv.winfo_width()
        end_y = canv.winfo_height()- 25

        canv.create_line(start_x, start_y, end_x, end_y, width=2, tags="field") # Canvas.winfo_width

        start_x = 25
        start_y = 25
        end_x = 25
        end_y = canv.winfo_height()- 25
        canv.create_line(start_x, start_y, end_x, end_y, width=2, tags="field") # Canvas.winfo_width


        for x in range(1, 25):
            pos = 25 + (20*x)
            canv.create_line(pos, 25, pos, canv.winfo_height() - 25, width=1, tags="field", fill="lightgray") # Canvas.winfo_width

        for y in range(1, 16):
            pos = 20 + (20*y)
            canv.create_line(25, pos, canv.winfo_width() , pos,  width=1, tags="field", fill="lightgray") # Canvas.winfo_width
            canv.create_text(10, pos,fill="darkblue",font="Times 7", text=45-y * 5, tags="field")




    def create_graph(self):
        canv = self.canvas
        # loop through data!

        first = True
        old_pos = 0

        for point in self.data:
            if first == False:
                xPos = (old_pos.get_x() - self.max_x ) * self.offset
                yPos = old_pos.get_y()
                old_x = ( point.get_x() - self.max_x) * self.offset
                old_y = point.get_y()

                old_pos = point

                self.create_graph_line(old_x, old_y + 50, xPos, yPos + 50, point.get_index())

            else:
                old_pos = point
                first = False


        # Draw to field
    def create_graph_line(self, old_x, old_y, new_x, new_y, index):
        canv = self.canvas

        old_y = canv.winfo_height() - (old_y*2)
        new_y = canv.winfo_height() - (new_y*2)
        canv.create_line(old_x + 25, old_y - 65, new_x + 25, new_y - 65, width=2, tags="data") # Canvas.winfo_width

        canv.create_text(new_x + 25, canv.winfo_height() - 15,fill="darkblue",font="Times 7", text=index, tags="data")
