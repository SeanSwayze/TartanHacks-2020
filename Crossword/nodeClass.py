from index import index 

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
	def word():
		return self._word

	# Return word represented by node. 
	def whichWord():
		# Implement
		pass

	# Return nth letter in the word (usual indexing)
	# Requires: n < current depth
	def nthLetter():
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

	def propagate(self, solution):
		# Implement
		pass

	# We need a bunch of update methods 
	# Need to refactor Sean's code to use update methods rather than direct dereferencing
