class Word:
	
	def __init__(self, length, constrained, setChars, index):
		self._index = index										# Unique word index
		self._length = length								    # Length of the word
		self._constrained = constrained						    # The number of characters linked to other characters
		self._set = setChars									    # The number of characters already set
		self._chars = ["" for x in range(length+1)] 			    # A position for each character in the word + 1 initial blank to allow easy use with depth
		self._pointers = [(None, 0) for x in range(length+1)]	# Pointers to other word who ith character is linked to word's ith character (pointer to word, index in word)

	# Edward's
	def __repr__(self):
		return f"({self._index}, {self._length})"

	# Sean's
	# def __repr__(self):
    #    string = f"""{self.chars[1:]}, Word {self.index}, Length {self.length}, {self.constrained} constraints with {self.set} set characters"""
    #    return string

	def length(self):
		return self._length

	# Modify all the connected words - fill in the connected blank
	def propagate(self):
		# Implement 
		pass

	# Whether or not letter x has been assigned a letter or if it is a blank
	def set(self, x):
		return not self._chars[x] == ""

	def showPointers(self):
		print(self._pointers)

	def setIndex(self, index):
		self._index = index

	def setLength(self, length):
		self._length = length

	def setConstrained(self, constrained):
		self._constrained = constrained

	def setSetChars(self, setChars):
		self._set = setChars

	def setChar(self, index, char):
		self._chars[index] = char

	def setChars(self, chars):
		self._chars = chars

	def setPointer(self, index, pointer):
		self._pointers[index] = pointer
		
	def setPointers(self, pointers):
		self._pointers = pointers
