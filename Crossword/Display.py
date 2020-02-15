from tkinter import *
import math, string

root = Tk()
root.title = "Crosswords"

canvas = Canvas(root, width=1200, height=800, bg = "white")
canvas.grid(column = 2, row = 0, rowspan=15)

canvasHeight = 700
canvasWidth = 1020
sideBarWidth = 130

class wordBoard():
    def __init__(self,width,height,root,canvas,margins = 50):
        self.root = root
        self.canvas = canvas
        self.width = width
        self.height = height
        self.selected = None
        self.fills = [[0]*width for i in range(height)] #The fill of each square
        self.fillIds = [[None]*width for i in range(height)] #The ids of the text
        self.elements = [[None]*width for i in range(height)] #The ids of every square
        self.ids = [] #Every object in the canvas in no particular order
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.canvasOnclick)
        self.canvas.bind("<Double-Button-1>", self.canvasOn2click)
        self.canvas.bind("<Key>", self.canvasOnKeyPress)
        self.canvas.bind("<BackSpace>", self.canvasOnDelete)
        self.margins = margins
        self.xMargins = 0
        self.yMargins = 0
        self.cellDims = 100

    def drawBoard(self):
        baseCellWidth = min(100,(canvasWidth-2*self.margins)//self.width)
        baseCellHeight = min(100,(canvasHeight-2*self.margins)//self.height)
        self.cellDims = min(baseCellWidth,baseCellHeight)
        self.xMargins = (canvasWidth-self.cellDims*self.width)//2
        self.yMargins = (canvasHeight-self.cellDims*self.height)//2
        print(self.width,self.height,baseCellWidth,baseCellHeight,self.cellDims)
        for row in range(self.height):
            for col in range(self.width):
                item = canvas.create_rectangle(self.xMargins+col*self.cellDims, 
                                               self.yMargins+row*self.cellDims,
                                               self.xMargins+(col+1)*self.cellDims, 
                                               self.yMargins+(row+1)*self.cellDims,
                                               width = max(1,min(3,self.cellDims//20)))
                self.ids.append(item)
                self.elements[row][col] = item


    def canvasOnclick(self,event):
        if ((event.x in range(self.xMargins,self.cellDims*self.width+self.xMargins)) and 
            (event.y in range(self.yMargins,self.cellDims*self.height+self.yMargins))):
            row = (event.y-self.yMargins)//self.cellDims
            col = (event.x-self.xMargins)//self.cellDims
            if self.selected == self.elements[row][col]:
                self.canvas.itemconfig(self.selected, outline = "black")
                self.selected == None
            else:
                self.canvas.itemconfig(self.selected, outline = "black")
                self.selected = self.elements[row][col]
                self.canvas.itemconfig(self.selected, outline = "red")
                #self.canvas.delete(self.elements[row][col])
                #self.elements[row][col] = canvas.create_rectangle(self.xMargins+col*self.cellDims, 
                #                               self.yMargins+row*self.cellDims,
                #                               self.xMargins+(col+1)*self.cellDims, 
                #                               self.yMargins+(row+1)*self.cellDims,
                #                               width = max(1,min(3,self.cellDims//20)),
                #                               outline = "red", 
                #                               fill = ["white","black"][self.fills[row][col]])
                #if self.fillIds[row][col] != None:
                #    self.addLetter(self.canvas.itemcget(self.elements[row][col],"text"),row,col)
                #sself.selected = self.elements[row][col]

    def canvasOn2click(self,event):
        if ((event.x in range(self.xMargins,self.cellDims*self.width+self.xMargins)) and 
            (event.y in range(self.yMargins,self.cellDims*self.height+self.yMargins))):
            row = (event.y-self.yMargins)//self.cellDims
            col = (event.x-self.xMargins)//self.cellDims
            self.canvas.itemconfig(self.elements[row][col],
                                   fill = ("white" if self.canvas.itemcget(self.elements[row][col], "fill") == "black" else "black"))
            self.fills[row][col] = 1-self.fills[row][col]
    
    def findCoords(self, ID):
        for row in range(len(self.elements)):
            if ID in self.elements[row]:
                return row,self.elements[row].index(ID)

    def addLetter(self,char,row,col):
        if self.fillIds[row][col] != None:
            self.canvas.delete(self.fillIds[row][col])
        textSize = int(self.cellDims//1.2)
        self.fillIds[row][col] = canvas.create_text((col+0.5)*self.cellDims+self.xMargins,
                                                    (row+0.5)*self.cellDims+self.yMargins,
                                                    text = char,
                                                    font = f"Times {textSize}")
        self.ids.append(self.fillIds[row][col])

    def canvasOnKeyPress(self,event):
        if self.selected != None and ((event.char in string.ascii_lowercase) or (event.char in string.ascii_uppercase)):
            char = event.char
            row,col = self.findCoords(self.selected)
            self.addLetter(char,row,col)
            

    def canvasOnDelete(self,event):
        print("delete")
        if self.selected != None:
            row,col = self.findCoords(self.selected)
            self.canvas.delete(self.fillIds[row][col])
            self.fillIds[row][col] = None



    def destroy(self):
        for item in self.ids:
            self.canvas.delete(item)

class Space():
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.currentBoard = None

        self.widthLabel = Label(self.root, text = "Width: ")
        self.widthLabel.grid(column = 0, row = 0)
        self.widthField = Entry(self.root, text = "")
        self.widthField.grid(column=1, row = 0)

        self.heightLabel = Label(self.root, text = "Height: ")
        self.heightLabel.grid(column = 0, row = 1)
        self.heightField = Entry(self.root, text = "")
        self.heightField.grid(column=1, row = 1)

        self.submitButton = Button(self.root, text = "Submit", width = 10,
                                bg = "grey", command = self.createCrossword)
        self.submitButton.grid(column=0,row = 2, columnspan = 2)

    def submitCWDims(self):
        height = self.heightField.get()
        width = self.widthField.get()
        try: height = int(height)
        except: pass
        try: width = int(width)
        except: pass
        self.heightField.delete(0, 'end')
        self.widthField.delete(0, 'end') 
        return width,height

    def createCrossword(self):
        width,height = self.submitCWDims()
        print(self.currentBoard)
        if self.currentBoard != None:
            self.currentBoard.destroy()
        board = wordBoard(width,height,self.root,canvas)
        board.drawBoard()
        self.currentBoard = board

    def run(self):
        self.root.after(20, self.run)

space = Space(root,canvas)
space.run()
root.mainloop()
