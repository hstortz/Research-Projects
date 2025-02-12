""" This game is inspired by the Google Dinosaur Game. Play as Santa, and press
the spacebar to jump over trees! Make sure to click on the new window once
you press the 'Start' button. Get 100 points to win the game! """

""" Created by: Hannah Stortz, Camille Stich, Etsub Yayehyirad """
""" St. Olaf College, CSCI 121A, Fall 2021 """

"""#################################################################################################"""

import tkinter as tk
import random
from time import sleep
from tkinter import *

"""#################################################################################################"""

# global variables needed in the StartGame code
canvas_width = 815
canvas_height = 500
score = 0
jump = False
spacing = 0
santa_height = 0

def StartGame():
    """ the code that runs when the start button is pressed """
    win = tk.Tk()
    win.title("Holi-Dazed")
    my_canvas = tk.Canvas(win, width=canvas_width, height=canvas_height)
    my_canvas.grid(row=2, column=1)

    # reset global variables to make each instance of StartGame appear like the first instance
    # i.e. clear data
    global score
    score = 0
    global jump
    jump = False
    global spacing
    spacing = 0

    # import the background image
    bg_img = PhotoImage(file="background.png", master=win)
    my_canvas.create_image(0, 0, anchor=NW, image=bg_img)

    # import santa image
    santa_img = PhotoImage(file="santa.png", master=win)

    # import tree image
    tree_img = PhotoImage(file="tree.png", master=win)

    def crashed():
        """ what happens when santa crashes into a tree """
        win.destroy()
        CrashScreen()

    def winner():
        """ what happens when you reach a score of 100 and win the game """
        global score
        score = 100
        win.destroy()
        WinnerScreen()

    def tick():
        """ creates a timer loop that updates the score by adding 1 to it every second """
        global score
        
        # create a label that shows the score
        score_label = tk.Label(win, text="Score: "+str(score), font=("broadway", 30))
        score_label.grid(row=1, column=1, sticky=tk.E+tk.W)
        score += 1

        # when you reach a score of 100, end the game and show the winning screen!
        # set to 102 instead of 100 because it goes too early for some reason
        if score == 102:
            winner()
            
        my_canvas.after(1000, tick)
        
    tick() # get the timer started

    class Santa:
        """ creates a character, santa, that jumps """

        def __init__(self):
            
            global canvas_width
            global canvas_height

            # make variables to configure santa, and create the object
            self.x = 10
            self.y = canvas_height-97
            self.santa = my_canvas.create_image(self.x, self.y, anchor=NW, image=santa_img)

            # make variables related to santa jumping
            self.speed = 5
            jump = False # trigger to jump
            win.bind("<space>", self.jump)

        def jump(self, event):
            """ makes santa jump when you press the space bar """
            global jump
            global santa_height
            x = 0
            y = 0
               
            if event.char == " " and jump == False:
                jump = True
                diff = 0 # difference in the initial level
                y = -9 # initial y value of speed
                grav = .2 # gravity
                while diff >= 0: # when santa is in the air
                    santa_height += 1
                    my_canvas.move(self.santa, x, y)
                    my_canvas.update()
                    sleep(.001) # pause time
                    diff -= y # updated jumping height
                    y += grav # updating speed in y
                santa_height = 0
                y = 0 # return to original speed
                jump = False

    Santa() # create the santa object

    class Tree:
        """ creates trees that move from the right of the screen to the left """

        def __init__(self):
            global canvas_width
            global canvas_height

            # make variables for the coordinates of the corners of the tree
            self.x = canvas_width+10
            self.y = canvas_height-130

            # create a green rectangle for the tree
            self.tree = my_canvas.create_image(self.x, self.y, anchor=NW, image=tree_img)
            self.moveTree()

        def moveTree(self):
            """ moves the trees from the right to the left of the screen """
            my_canvas.move(self.tree, -5, 0)

            """ define hit-boxes for trees """
            if my_canvas.coords(self.tree)[0] <= 58 and my_canvas.coords(self.tree)[0] >= -20 and santa_height <= 15:
                crashed() # crashes when santa jumps too late and hits the front of a tree
            elif my_canvas.coords(self.tree)[0] <= 60 and my_canvas.coords(self.tree)[0] >= -25 and santa_height >= 73:
                crashed() # crashes when santa jumps too soon and lands on the front of a tree

            my_canvas.after(33, self.moveTree)

    def create_trees():
        """ create new trees after a set amount of time """
        Tree()
        spacing = random.randrange(2000, 6000, 1000)
        my_canvas.after(spacing, create_trees)

    create_trees() # get the create_trees loop started

    # start the GUI event loop for the game code
    win.mainloop()

"""#################################################################################################"""

def WinnerScreen():
    """ the screen that shows up when santa crashes into a tree. allows you to go back to the title screen """

    def title_pressed():
        win3.destroy()
        TitleScreen()

    # set up the window for the winning screen           
    win3 = tk.Tk()
    win3.title("Holi-Dazed")
    canvas_width3 = 815
    canvas_height3 = 500
    my_canvas = tk.Canvas(win3, width=canvas_width3, height=canvas_height3) 
    my_canvas.grid(row=2, column=1)

    # import background image and add text
    bg_img = PhotoImage(file="confetti.png")
    my_canvas.create_image(-125, -80, anchor=NW, image=bg_img)
    text = tk.Label(win3, text="Congratulations! You win!", font=("Broadway", 30), fg="white", bg = "#CD1313", relief = RIDGE)
    text.place(x=180,y=30)

    # add a cute santa image
    happy_santa_img = PhotoImage(file="happy santa.png")
    my_canvas.create_image(135, 100, anchor=NW, image=happy_santa_img)

    # import the score
    text = tk.Label(win3, text="Final Score: " + str(score), font=("Broadway", 20), fg="green", bg = "white", relief = RIDGE)
    text.grid(row = 3, column = 1)
     
    # create title screen button 
    StartButton = tk.Button(win3, text='TITLE SCREEN',font=('Broadway', 20), fg="#CD1313", bg = "white", relief = RAISED)
    StartButton.place(x=300, y=360)
    StartButton['command'] = title_pressed

    # create quit button
    QuitButton = tk.Button(win3, text="QUIT", font=('Broadway', 20), fg="#CD1313", bg = "white", relief = RAISED, command=win3.destroy)
    QuitButton.place(x=363, y= 430)
     
    # start the GUI event loop for the title screen
    win3.mainloop()

"""#################################################################################################"""

def CrashScreen():
    """ the screen that shows up when santa crashes into a tree. allows you to go back to the title screen """

    def title_pressed():
        win2.destroy()
        TitleScreen()

    # set up the window for the crash screen           
    win2 = tk.Tk()
    win2.title("Holi-Dazed")
    canvas_width2 = 815
    canvas_height2 = 500
    my_canvas = tk.Canvas(win2, width=canvas_width2, height=canvas_height2)
    my_canvas.grid(row=2, column=1)

    # import background image and add text
    bg_img = PhotoImage(file="sleeping.png")
    my_canvas.create_image(-125, -80, anchor=NW, image=bg_img)
    text = tk.Label(win2, text="Oops! You are Holi-Dazed!", font=("Broadway", 30), fg="white", bg = "#CD1313", relief = RIDGE)
    text.place(x=180,y=30)

    # import the score
    text = tk.Label(win2, text="Final Score: " + str(score), font=("Broadway", 20), fg="green", bg = "white", relief = RIDGE)
    text.grid(row = 3, column = 1)

    # create title screen button 
    StartButton = tk.Button(win2, text='TITLE SCREEN',font=('Broadway', 20), fg="#CD1313", bg = "white", relief = RAISED)
    StartButton.place(x=300, y=360)
    StartButton['command'] = title_pressed

    # create quit button
    QuitButton = tk.Button(win2, text="QUIT", font=('Broadway', 20), fg="#CD1313", bg = "white", relief = RAISED, command=win2.destroy)
    QuitButton.place(x=363, y= 430)
     
    # start the GUI event loop for the title screen
    win2.mainloop()

"""#################################################################################################"""

def TitleScreen():
    """ the title screen that allows you to quit or play the game """

    def pressed_start():
        win1.destroy()
        StartGame()
    
    # set up the window for the title screen           
    win1 = tk.Tk()
    win1.title("Holi-Dazed")
    canvas_width1 = 815
    canvas_height1 = 500
    my_canvas = tk.Canvas(win1, width=canvas_width1, height=canvas_height1)
    my_canvas.grid(row=2, column=1)

    # import title screen background image
    bg_img = PhotoImage(file="title.png", master=win1)
    my_canvas.create_image(0, 0, anchor=NW, image=bg_img)
    text = tk.Label(win1, text="~Holi-Dazed~", font=("Broadway", 50), fg="white", bg = "#CD1313", relief = RIDGE)
    text.place(x=230,y=30)


    # create start button 
    StartButton = tk.Button(win1, text='START',font=('Broadway', 20), fg="#CD1313", bg = "white", relief = RAISED)
    StartButton.place(x=350, y=360)
    StartButton['command'] = pressed_start

    # create quit button
    QuitButton = tk.Button(win1, text="QUIT", font=('Broadway', 20), fg="#CD1313", bg = "white", relief = RAISED, command=win1.destroy)
    QuitButton.place(x=362, y= 430) 
     
    # start the GUI event loop for the title screen
    win1.mainloop()

"""#################################################################################################"""

TitleScreen()
