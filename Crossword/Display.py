from tkinter import *
import math, string

root = Tk()
root.title = "Crosswords"

canvas = Canvas(root, width=1200, height=800, bg = "white")
canvas.grid(column = 2, row = 0, rowspan=15)

canvasHeight = 700
canvasWidth = 1020
sideBarWidth = 130

class Word:
    def __init__(self, length, constrained, setChars, index):
        self.index = index
        self.length = length
        self.constrained = constrained
        self.set = setChars
        self.chars = ["" for x in range(length+1)]
        self.pointers = [(None, 0) for x in range(length+1)]
    def __repr__(self):
        string = f"""{self.chars[1:]}, Word {self.index}, Length {self.length}, {self.constrained} constraints with {self.set} set characters"""
        return string

    def showPointers(self):
        print(self.pointers)

    def setIndex(self,index):
        self.index = index
    def setLength(self,length):
        self.length = length
    def setConstrained(self,constrained):
        self.constrained = constrained
    def setSetChars(self,setChars):
        self.set = setChars
    def setChar(self,index,char):
        self.chars[index] = char
    def setChars(self,chars):
        self.chars = chars
    def setPointer(self,index,pointer):
        self.pointers[index] = pointer
    def setPointers(self,pointers):
        self.pointers = pointers
    
def isStart(board, x, y):
    result = [0,0]
    if board.fills[y][x] == 1: return result
    if (x-1 not in range(board.width) or board.fills[y][x-1] == 1):
        if (x+1 in range(board.width) and board.fills[y][x+1] == 0): result[0] = 1
    if (y-1 not in range(board.height) or board.fills[y-1][x] == 1):
        if (y+1 in range(board.height) and board.fills[y+1][x] == 0): result[1] = 1
    return result

def convertBoardToWords(board):
    words = []
    for row in range(board.height):
        for col in range(board.width):
            start = isStart(board,col,row)
            if start[0] == 1:
                tempCol = col
                if (tempCol in range(board.width) and board.fills[row][tempCol] == 0):
                    newWord = [col,row,0,""]
                while (tempCol in range(board.width) and board.fills[row][tempCol] == 0):
                    newWord[3] += board.letters[row][tempCol]
                    tempCol += 1
                words.append(newWord)
            if start[1] == 1:
                tempRow = row
                newWord = [col,row,1,""]
                while (tempRow in range(board.height) and board.fills[tempRow][col] == 0):
                    newWord[3] += board.letters[tempRow][col]
                    tempRow += 1
                words.append(newWord)
    return words
                


    #Returns a list of words from the user input

def wordsIntersect(word1, word2):
    if word1[2] == word2[2]: return False
    right = (word1 if word1[2]==0 else word2)
    down = (word1 if word1[2]==1 else word2)
    return (right[1] in range(down[1],down[1]+len(down[3]))) and (down[0] in range(right[0],right[0]+len(right[3])))

def convertWordsToClass(words):
    index = 0
    classes = []
    for i in words:
        setChars = len(i[3])-i[3].count("-")
        classes.append(Word(len(i[3]),0,setChars,index))
        classes[index].setChars([""]+["" if c == "-" else c for c in i[3]])
        for j in words:
            if (i != j) and wordsIntersect(i,j): 
                classes[index].setConstrained(classes[index].constrained + 1)
        index+=1
    for i in range(len(words)):
        for j in range(len(words)):
            if words[i] != words[j] and wordsIntersect(words[i],words[j]):
                if words[i][2]==0:
                    classes[i].setPointer(words[j][0]-words[i][0]+1,(classes[j],words[i][1]))
                else:
                    classes[i].setPointer(words[j][1]-words[i][1]+1,(classes[j],words[i][0]))
    return classes
    
class wordBoard():
    def __init__(self,width,height,root,canvas,margins = 50):
        self.root = root
        self.canvas = canvas
        self.width = width
        self.height = height
        self.selected = None
        self.fills = [[0]*width for i in range(height)] #The fill of each square
        self.fillIds = [[None]*width for i in range(height)] #The ids of the text
        self.letters = [["-"]*width for i in range(height)] #The grid of letters
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
        self.submitButton = Button(self.root, text = "Solve", width = 10,
                                bg = "grey", command = self.activateSolve)
        self.submitButton.grid(column=0,row = 5, columnspan = 2)

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
        self.letters[row][col] = char

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
            self.letters[row][col] = "-"

    def destroy(self):
        for item in self.ids:
            self.canvas.delete(item)

    def activateSolve(self):
        words = convertBoardToWords(self)
        for i in words:
            print(i)
        listOfWords = convertWordsToClass(words)
        for word in listOfWords:
            print(word)
        #send list to Edward

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
