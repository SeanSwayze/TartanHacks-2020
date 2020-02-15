#from fileToWordList import *
#from node import *
import string
lower = string.ascii_lowercase


dictionary = ["a","ba","bad","abad","ad","caba","add","cad"]


class Node: 
    def __init__(self, parent, letter, depth, word, height = 0):
        self.parent = parent
        self.letter = letter
        self.depth = depth
        self.word = word
        self.pointers = [None for x in range(26)]
        self.height = height

    def __repr__(self):
        return f"{self.letter},{self.word},{self.pointers}"

#Converts a trie into a list of words
def trieToList(root,string = ""):
    if root.word: strings = [string+root.letter]
    else: strings = []
    for node in root.pointers:
        if node != None:
            result = trieToList(node,string = string+root.letter)
            strings += result
    return strings

#Creates a new trie with every word in a given dictionary, returns root
def listToTrie(dictionary):
    def getHeight(node): return node.height
    root = Node(None,"",0,False)
    for word in dictionary:
        newNode = root
        depth = 0
        for char in word:
            depth += 1
            if newNode.pointers[lower.index(char)] == None:
                newNode.pointers[lower.index(char)] = Node(newNode,char,depth,False)
                newNode = newNode.pointers[lower.index(char)]
                testNode = newNode.parent
                while testNode != root:
                    testNode.height = 0
                    for node in testNode.pointers:
                        if node != None: 
                            testNode.height = max(testNode.height,node.height)
                    testNode = testNode.parent
            else:
                newNode = newNode.pointers[lower.index(char)]
        newNode.word = True
    return root

#Determines whether a word is in the trie, returns boolean
def wordInTrie(word,node):
    for char in word:
        if node.pointers[lower.index(char)] != None:
            node = node.pointers[lower.index(char)]
        else:
            return False
    return node.word

#Returns a list of the number of words of each length
def findLens(dictionary):
    lengths = [0]*max(list(map(len,dictionary)))
    for word in dictionary: lengths[len(word)-1] += 1
    return lengths


root = listToTrie(dictionary)
words = trieToList(root)

print(words)
print(findLens(words))
