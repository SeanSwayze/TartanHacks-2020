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

#earth = Image.open("Earth.png")
#earth = earth.resize((100, 100), Image.ANTIALIAS)
#photo = ImageTk.PhotoImage(earth)
#label = Label(root, image = photo)
#label.image = earth
#label.grid(column = 0, row = 2, rowspan = 2, columnspan = 2)

class Space:
    def __init__(self, root, canvas, color = "black", scale = 1, bodies = []):
        self.canvas = canvas
        self.root = root
        self.G = 0.001
        self.color = color
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
            body.vectors()

    def loop(self):
        #print(self.pause)
        self.moveBodies()
        self.canvas.after(20, self.loop)

    def clickOnObject(self, event):
        for body in self.bodies:
            if (((event.x-body.position[0])**2+(event.y-body.position[1])**2)**0.5 < body.size/2):
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
                self.selectedBody.vectors()
            
    def canvas_onrightclick(self, event):
        check = self.clickOnObject(event)
        if self.selectedBody == None:
            if check != None:
                check.charge *= -1
                check.set_color()
        else:
            if self.selectedBody == check:
                check.charge *= -1
                check.set_color()
            else:
                self.selectedBody.velocity = [0, 0]
                self.selectedBody.vectors()



    def canvas_onmousewheel(self, event):
        if self.selectedBody != None:
            self.selectedBody.size += event.delta/10
            self.selectedBody.size = max(10, self.selectedBody.size)
            self.selectedBody.updateMass()

            self.canvas.delete(self.selectedBody.id)
            self.selectedBody.id = self.canvas.create_oval(self.selectedBody.position[0]-self.selectedBody.size/2,
                                   self.selectedBody.position[1]-self.selectedBody.size/2, 
                                   self.selectedBody.position[0]+self.selectedBody.size/2,
                                   self.selectedBody.position[1]+self.selectedBody.size/2)
            self.canvas.itemconfig(self.selectedBody.id,outline = "white")
            self.selectedBody.set_color()
            self.selectedBody.vectors()            

    def canvas_pause(self):
        self.pause *= -1
        self.buttonText.set(["Pause","Play"][int((self.pause+1)/2)])


space = Space(root, canvas, "red")
space.loop()  
root.mainloop()