from tkinter import *
import math
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
        self.G = 0.00001
        self.color = color
        self.scale = scale
        self.bodies = bodies
        self.pause = 1
        self.selectedBody = None
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.canvas_onclick)
        self.centerX = 0
        self.centerY = 0
        
        self.buttonText = StringVar()
        self.playButton = Button(self.root, textvariable = self.buttonText, width = 10,
                             bg = "grey", command = self.canvas_pause)
        self.buttonText.set("Play")
        self.playButton.grid(column=0, row = 9, columnspan = 2)

        label = Label(root, text = "Mass: ")
        label.grid(column = 0, row = 15)

        self.massField = Entry(self.root, text = "")
        self.massField.grid(column=1, row = 15)

        self.submitButton = Button(self.root, text = "Submit", width = 10,
                             bg = "grey", command = self.alterSize)
        self.submitButton.grid(column=0,row = 16, columnspan = 2)

    
    def moveBodies(self):
        #print(self.pause)
        for body in self.bodies:
            if body.selected == True and body.color == "red":
                self.canvas.itemconfig(body.id,fill = "green")
                body.color = "green"
            elif body.selected == False and body.color == "green":
                self.canvas.itemconfig(body.id,fill = "red")
                body.color = "red"
            if self.pause == -1:    
                body.move()
                body.vectors()
        self.canvas.after(20, self.moveBodies)

    def clickOnObject(self, event):
        for body in self.bodies:
            if (((event.x-body.x)**2+(event.y-body.y)**2)**0.5 < body.size/2):
                return body
        return None

    def canvas_onclick(self, event):
        check = self.clickOnObject(event)
        if check != None:
            if self.selectedBody == check: self.selectedBody = None
            check.selected = not check.selected
            for body in self.bodies:
                if body.num != check.num: body.selected = False
                else:
                    if check.selected == True: self.selectedBody = check
        elif self.selectedBody != None:
            dx,dy = (event.x - self.selectedBody.x),(event.y - self.selectedBody.y)
            self.selectedBody.vx = dx/10
            self.selectedBody.vy = dy/10
            self.selectedBody.vectors()
            self.selectedBody.selected = False
            self.selectedBody = None
        else:
            body = Body(self.canvas, "red", event.x, event.y, 
                        0, 0, 10, len(self.bodies), self)
            #for other in self.bodies:
                #other.selected = False
            self.bodies.append(body)
    
    def alterSize(self):
        if self.selectedBody != None:
            print(self.massField.get)
            self.selectedBody.size = int(self.massField.get())
            self.canvas.delete(self.selectedBody.id)
            self.selectedBody.id = self.canvas.create_oval(self.selectedBody.x-self.selectedBody.size/2,
                                   self.selectedBody.y-self.selectedBody.size/2, 
                                   self.selectedBody.x+self.selectedBody.size/2,
                                   self.selectedBody.y+self.selectedBody.size/2,
                                   fill = self.selectedBody.color)
            self.selectedBody.updateMass()
            self.massField.delete(0, 'end') 

    def canvas_pause(self):
        self.pause *= -1
        self.buttonText.set(["Pause","Play"][int((self.pause+1)/2)])


space = Space(root, canvas, "red")
space.moveBodies()  
root.mainloop()