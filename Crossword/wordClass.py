class word:
	
	def __init__(self, length, constrained, setChars):
		self.length = length								# Length of the word
		self.constrained = constrained						# The number of characters linked to other characters
		self.set = setChars									# The number of characters already set
		self.chars = ["" for x in range(length+1)] 			# A position for each character in the word + 1 initial blank to allow easy use with depth
		self.pointers = [None for x in range(length+1)]		# Pointers to other word who ith character is linked to word's ith character
