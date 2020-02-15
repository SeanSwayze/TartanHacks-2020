from tkinter import *
import math

class Body:
    def __init__(self, canvas, color, x, y, vx, vy, size, num, space = None):
        self.num = num
        self.canvas = canvas
        self.id = canvas.create_oval(x-size/2, y-size/2, x+size/2, y+size/2, fill=color)
        self.color = color
        self.selected = False
        self.x = x
        self.y = y
        self.vx, self.vy = vx, vy
        self.size = size
        self.mass =  4/3*math.pi*size**3
        self.space = space
        self.lineID = self.canvas.create_line(self.x,self.y,self.x+10*self.vx,self.y+10*self.vy)

    def __repr__(self):
        return str(self.num)

    def force(self,other):
        force = self.space.G*self.mass*other.mass/((self.x-other.x)**2+(self.y-other.y)**2)**0.5
        angle = math.atan2(other.y-self.y,other.x-self.x)
        fx = force*math.cos(angle)
        fy = force*math.sin(angle)
        return fx,fy

    def move(self):
        ax,ay = 0,0
        for body in self.space.bodies:
            if body.num != self.num:
                fx,fy = self.force(body)
                ax = fx/self.size
                ay = fy/self.size
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        dx = self.x-(self.canvas.coords(self.id)[0]+self.canvas.coords(self.id)[2])/2
        dy = self.y-(self.canvas.coords(self.id)[1]+self.canvas.coords(self.id)[3])/2
        self.canvas.move(self.id, dx, dy)
    
    def vectors(self):
        self.canvas.delete(self.lineID)
        self.lineID = self.canvas.create_line(self.x,self.y,self.x+10*self.vx,
                                              self.y+10*self.vy, fill = "white")