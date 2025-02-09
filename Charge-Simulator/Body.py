from tkinter import *
import math
import numpy as np


class Body:
    def __init__(self, canvas, charge, x, y, vx, vy, size, num, space = None):
        self.num = num
        self.canvas = canvas
        color = "red" if charge == 1 else "blue"
        self.id = canvas.create_oval(x-size/2, y-size/2, x+size/2, y+size/2, fill=color)
        self.lineID = self.canvas.create_line(x,y,x+10*vx,y+10*vy)
        self.charge = charge
        self.selected = False

        self.position = np.array([x, y], dtype='float64')
        self.velocity = np.array([vx, vy], dtype='float64')
        self.force = np.array([0.0, 0.0])
        
        self.size = size
        self.mass = 4/3*math.pi*(size/2)**3
        self.space = space

    def __repr__(self):
        return str(self.num)

    @staticmethod
    def pair_force(body_pair, space):
        body1, body2 = body_pair
        dpos = body2.position - body1.position
        sign = body1.charge * body2.charge

        force = (dpos/np.linalg.norm(dpos)**3)*space.G*body1.mass*body2.mass
        body1.force -= force*sign
        body2.force += force*sign

    def contains(self, pos):
        return np.linalg.norm(self.position - pos) < self.size/2

    def move(self):
        acc = self.force/self.mass
        self.velocity += acc
        self.position += self.velocity
        
        self.canvas.move(self.id, self.velocity[0], self.velocity[1])
        self.force = np.array([0.0, 0.0])
    
    def update_vector(self):
        self.canvas.delete(self.lineID)
        self.lineID = self.canvas.create_line(self.position[0],self.position[1],self.position[0]+10*self.velocity[0],
                                              self.position[1]+10*self.velocity[1], fill = "white")

    def update_shape(self, flipCharge=False, size=None):
        if flipCharge:
            self.charge *= -1
        if size != None:
            self.size = size
            self.mass = 4/3*math.pi*(size/2)**3

            self.canvas.delete(self.id)
            self.id = self.canvas.create_oval(self.position[0]-self.size/2,
                                            self.position[1]-self.size/2, 
                                            self.position[0]+self.size/2,
                                            self.position[1]+self.size/2)
        color = "red" if self.charge == 1 else "blue"
        self.canvas.itemconfig(self.id, fill = color)