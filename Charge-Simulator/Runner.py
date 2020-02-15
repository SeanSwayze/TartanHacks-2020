from tkinter import *
import math
import itertools
from Body import *
import tkinter.font
from PIL import Image, ImageTk

root = Tk()
root.title = "Game"

canvas = Canvas(root, width=1200, height=800, bg = "black")
canvas.grid(column = 2, row = 0, rowspan=20)

class Space:
    def __init__(self, root, canvas, scale = 1, bodies = []):
        self.G = 0.25

        self.canvas = canvas
        self.root = root
        self.scale = scale
        self.bodies = bodies

        self.pause = 1
        self.selectedBody = None
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.canvas_onleftclick)
        self.canvas.bind("<Button-3>", self.canvas_onrightclick)
        self.canvas.bind("<MouseWheel>", self.canvas_onmousewheel)
        self.centerX = 0
        self.centerY = 0
        
        self.buttonText = StringVar()
        self.playButton = Button(self.root, textvariable = self.buttonText, width = 10,
                             bg = "grey", command = self.canvas_pause)
        self.buttonText.set("Play")
        self.playButton.grid(column=0, row = 9, columnspan = 2)
    
    def moveBodies(self):
        #print(self.pause)
        if not self.pause == -1:
            return
        bodies_pairs = list(itertools.combinations(self.bodies, 2))
        for pair in bodies_pairs:
            Body.pair_force(pair, self)
        for body in self.bodies:
            body.move()
            body.update_vector()

    def loop(self):
        #print(self.pause)
        self.moveBodies()
        self.canvas.after(20, self.loop)

    def clickOnObject(self, event):
        for body in self.bodies:
            if body.contains(np.array([event.x, event.y])):
                return body
        return None

    def canvas_onleftclick(self, event):
        check = self.clickOnObject(event)
        if self.selectedBody == None:
            if check == None:
                body = Body(self.canvas, 1, event.x, event.y,
                        0, 0, 10, len(self.bodies), self)
                if self.selectedBody != None:
                    self.selectedBody = None
                self.bodies.append(body)
            else:
                self.selectedBody = check
                self.selectedBody.selected = True
                self.canvas.itemconfig(self.selectedBody.id,outline = "white")
        else:
            if self.selectedBody == check:
                self.canvas.itemconfig(self.selectedBody.id,outline = "")
                self.selectedBody.selected = False
                self.selectedBody = None
            else:
                dx,dy = (event.x - self.selectedBody.position[0]),(event.y - self.selectedBody.position[1])
                self.selectedBody.velocity = [dx/10, dy/10]
                self.selectedBody.update_vector()
            
    def canvas_onrightclick(self, event):
        check = self.clickOnObject(event)
        if self.selectedBody == None:
            if check != None:
                check.update_shape(flipCharge=True)
        else:
            if self.selectedBody == check:
                check.update_shape(flipCharge=True)
            else:
                self.selectedBody.velocity = [0, 0]
                self.selectedBody.update_vector()

    def canvas_onmousewheel(self, event):
        if self.selectedBody != None:
            self.selectedBody.update_shape(size=max(10, self.selectedBody.size + event.delta/10))
            self.canvas.itemconfig(self.selectedBody.id,outline = "white")
            self.selectedBody.update_vector()

    def canvas_pause(self):
        self.pause *= -1
        self.buttonText.set(["Pause","Play"][int((self.pause+1)/2)])


space = Space(root, canvas)
space.loop()
root.mainloop()