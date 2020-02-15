# Crossword puzzle 

class Node: 

	def __init__(self, parent, letter, depth, word):
		self.parent = parent	# Pointer to parent
		self.letter = letter	# Current letter
		self.depth = depth		# Current depth (first letter is depth = 1)
		self.word = word 		# Bool (Yes or no)
		self.pointers = [None for x in range(26)]

	# Return whether current node is a word: True/False
	def word():
		return self.word

	# Return word represented by node. 
	def whichWord():
		# Implement

	# Return nth letter in the word (usual indexing)
	# Requires: n < current depth
	def nthLetter():
		# Implement



