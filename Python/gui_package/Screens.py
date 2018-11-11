#Robertjan- 05-11-2018

from tkinter import*
#from model import*

class Screen:
    def __init__(self, mater):

        master =Tk()
        master.title("Home")
        master.mainloop()

    def main(self, master):
        main_frame = Frame.configure(master, width = 800, height =750)

    def light(self, main_frame):

        Light_frame = Frame.configure(main_frame, width = 200, height =150, bg="pink")
        light_frame.grid(column= 0 , row=0 ,sticky=W)
        Light_lable = Lable.grid(light_frame, tekst ="Licht sterkte", column=0, row=0, sticky =N)
        Light_info = Lable.grid(light_frame, tekst = "4", column= 1, row =1, sticky =S)
        #IF Censor outpute = Thrue:
           # print (light())
        #else
            #geef geen outpute

    def temp(self, main_frame):
        temp_frame = Frame.configure(main_frame, width = 200, height =150, bg="red")
        temp_frame.grid(column= 1 , row=1 ,sticky=W)
        temp_lable = Lable.grid(temp_frame, tekst ="Gem.temperatuur", column=0, row=0, sticky =N)
        temp_info = Lable.grid(temp_frame, tekst = "22", column= 1, row =1, sticky =S)
         #IF Censor outpute = Thrue:
           # print (tenmp())
        #else
            #geef geen outpute

    def light_inpute(self, main_frame):
        l_imput_frame = Frame.configure(main_frame, width = 200, height =150, bg="blue")
        l_imput_frame.grid(column= 0 , row=0 ,sticky=E)
        l_output_lable = Lable.grid(l_imput_frame, tekst ="Licht sterkte", column=0, row=0, sticky =N)
        l_imput_slider = Scale(l_imput_frame, from_=-10, to=40, orient=HORIZONTAL).grid(column = 1 ,row=1, sticky=S)
        #IF Censor outpute = Thrue:
           # print (light())
        #else
            #geef geen outpute

    def temp_inpute(self, main_frame):
        t_imput_frame = Frame.configure(main_frame, width = 200, height =150, bg="green")
        t_imput_frame.grid(column= 0 , row=0 ,sticky=E)
        t_output_lable = Lable.grid(t_imput_frame, tekst ="Licht sterkte", column=0, row=0, sticky =N)
        t_imput_slider = Scale(t_imput_frame, from_=-10, to=40, orient=HORIZONTAL).grid(column = 1 ,row=1, sticky=S)
        #IF Censor outpute = Thrue:
           # print (light())
        #else
            #geef geen outpute



    def start_GUI(self):
        print(main)







