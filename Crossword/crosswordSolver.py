from nodeClass import *
from wordClass import *
from dictToTrie import *
from index import index
from queue import LifoQueue
# https://docs.python.org/3/library/queue.html

# Explanation for bool interpretation of other types
# http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/boolean.html

def listToLifoQueue(words):
	length = len(words)
	lQ = LifoQueue()
	for x in range(len(words)):
		lQ.put(words[length-1-x])
	return lQ


def solveHelper(wordList, root):

	# Base case: Success. No more words to match
	if wordList.empty():
		return [[]]
	
	# Recursive case
	else:
		word = wordList.get(block=False) # currentWord. Next word to be filled in
		solutions = match(word, 1, root, wordList, root)
		return solutions


def match(word, cL, node, wordList, root):

	# Base case: trie matched against word
	if cL == word.length():

		# Node is word
		if node.word():
			solution = node.whichWord()
			word.propagate(solution)
			solutions = solveHelper(wordList, root)
			# Total solution found
			if solutions:
				for x in solutions:
					x.append(solution)
				return solutions
			# Collision occurs down the line
			else:
				return []
		
		# Node is not word
		else:
			return []
	
	# Recursive case
	else:

		# Next character set
		if word.set(cL): 
			# Find next starting node
			nextNode = node.childL(word.letter(cL))
			# No solution
			if (nextNode == None) or (nextNode.maxLength() < word.length()): 
				return []
			# Continue with search
			else:
				solutions = match(word, cL+1, nextNode, wordList, root)
				return solutions
		
		# Next character blank
		else:
			# Iterate through all 26 possibilities (casing on whether or not they are long enough to be an option)
			solutions = []
			for x in range(26):
				# Find next starting node
				nextNode = node.childN(x)
				# No solution
				if (nextNode == None) or (nextNode.maxLength() < word.length()): 
					continue
				# Continue with search
				else:
					solutions += match(word, cL+1, nextNode, wordList, root)
			return solutions


# Success: LifoQueue * trie -> string list list
# solve(wordList, root) => list containing a list of all solution lists e.g. [["hi", "die"], ["hi", "bye"]]. Failure returns an empty list
def solve(wordList, root):
	
	wordList = listToLifoQueue(wordList)
	solutions = solveHelper(wordList, root)


def testing():
	dictionary = ["a","ba","bad","abad","ad","caba","add","cad", "addda"]
	root = listToTrie(dictionary)
	word1 = Word(4, 1, 0, 1)
	word2 = Word(3, 2, 0, 2)
	word3 = Word(5, 1, 0, 3)
	word1._pointers[1] = (word2, 1)
	word2._pointers[1] = (word1, 1)
	word2._pointers[3] = (word3, 2)
	word3._pointers[2] = (word2, 3)
	words = [word1]
	solutions = solve(words, root)
	print(solutions)


testing()
