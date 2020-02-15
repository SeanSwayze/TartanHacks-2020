from index import index 


def listToTrie5(dictionary):
    root = Node(None,"",0,False)
    for word in dictionary:
        newNode = root
        depth = 0
        for char in word:
            depth += 1
            if newNode._pointers[index(char)] == None:
                newNode._pointers[index(char)] = Node(newNode,char,depth,False)
                newNode = newNode._pointers[index(char)]
                testNode = newNode._parent
                while testNode != root:
                    testNode._height = testNode._height
                    for node in testNode._pointers:
                        if node != None: 
                            if node._height+1 > testNode._height:
                                testNode._height = node._height+1
                                testNode._maxLength += 1
                    testNode = testNode._parent
            else:
                newNode = newNode._pointers[index(char)]
        newNode._word = True
    return root

class Node: 

	def __init__(self, parent, letter, depth, word):
		self._parent = parent	# Pointer to parent
		self._letter = letter	# Current letter
		self._depth = depth		# Current depth (first letter is depth = 1)
		self._word = word 		# Bool (Yes or no)
		self._pointers = [None for x in range(26)]	# Pointers to other child nodes
		self._height = 0 		# Longest path existing underneath this nodes
		self._maxLength = depth	# Longest word on whose path node is on (includes the current node)

	def __repr__(self):
		return f"({self._letter},{self._word})"

	# Return whether current node is a word: True/False
	def word(self):
		return self._word

	# Return word represented by node. 
	def whichWord(self):
		node = self
		str = node._letter
		while node._parent:
			node = node._parent
			str += node._letter
		return str[::-1]

	# Return nth letter in the word (usual indexing)
	# Requires: n < current depth
	def nthLetter(self):
		# Implement
		pass

	# Return the node's height
	def depth(self):
		return node._depth

	# Return the node's height
	def height(self):
		return node._height

	# Return max word length on node's path
	def maxLength(self):
		return self._maxLength

	# Returns None on failure
	def childL(self, letter):
		return self._pointers[index(letter)]

	# Returns None on failure
	def childN(self, number):
		return self._pointers[number]

	# We need a bunch of update methods 
	# Need to refactor Edward's + Sean's code to use update methods rather than direct dereferencing

def testing():
	dictionary = ["a","ba","bad","abad","ad","caba","add","cad", "addda"]
	root = listToTrie5(dictionary)
	print(root._pointers[0]._pointers[1]._pointers[0]._pointers[3].whichWord())

#testing()
