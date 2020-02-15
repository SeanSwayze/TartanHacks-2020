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
	
	print("sH2")
	# Base case: Success. No more words to match
	if wordList.empty():
		return [[]]
	
	# Recursive case
	else:
		print("sH3")
		word = wordList.get(block=False) # currentWord. Next word to be filled in
		solutions = match(word, 1, root, wordList, root)
		return solutions


def match(word, cL, node, wordList, root):
	print("match4")
	# Base case: trie matched against word
	if cL == word.length():
		print("match5")
		# Node is word
		if node.word():
			print("match6")
			# Modify node values appropriately
			solution = node.whichWord()
			word.setChars([""]+list(solution))
			# Propagate changes to other connected nodes
			print("match7")
			word.propagate()
			print("match8")
			# Find list of solution lists
			solutions = solveHelper(wordList, root)
			print("match9")
			# Total solution found
			if solutions:
				print("match10")
				for x in solutions:
					x.append(solution)
				print("match11")
				return solutions
			# Collision occurs down the line
			else:
				print("match12")
				return []
		
		# Node is not word
		else:
			print("match13")
			return []
	
	# Recursive case
	else:
		print("matche14")
		# Next character set
		if word.set(cL): 
			print("matche15")
			# Find next starting node
			nextNode = node.childL(word._chars[cL])
			# No solution
			if (nextNode == None) or (nextNode.maxLength() < word.length()): 
				print("matche16")
				return []
			# Continue with search
			else:
				print("matche17")
				solutions = match(word, cL+1, nextNode, wordList, root)
				return solutions
		
		# Next character blank
		else:
			print("matche18")
			# Iterate through all 26 possibilities (casing on whether or not they are long enough to be an option)
			solutions = []
			for x in range(26):
				print("fl", x)
				# Find next starting node
				nextNode = node.childN(x)
				# No solution
				if (nextNode == None) or (nextNode.maxLength() < word.length()): 
					print("fli", x)
					continue
				# Continue with search
				else:
					print("flie", x)
					solutions += match(word, cL+1, nextNode, wordList, root)
			print("matche19")
			return solutions


# Success: LifoQueue * trie -> string list list
# solve(wordList, root) => list containing a list of all solution lists e.g. [["hi", "die"], ["hi", "bye"]]. Failure returns an empty list
def solve(wordList, root):
	
	wordList = listToLifoQueue(wordList)
	solutions = solveHelper(wordList, root)
	return solutions


def testing():
	#dictionary = ["a","ba","bad","abad","ad","caba","add","cad", "addda"]
	dictionary = ["ba", "abad"]
	root = listToTrie(dictionary)
	#word1 = Word(4, 1, 0, 1)
	word1 = Word(4, 0, 0, 1)
	word2 = Word(3, 2, 0, 2)
	word3 = Word(5, 1, 0, 3)
	#word1._pointers[1] = (word2, 1)
	word2._pointers[1] = (word1, 1)
	word2._pointers[3] = (word3, 2)
	word3._pointers[2] = (word2, 3)
	words = [word1]
	print("Here1")
	print(words[0]._chars)
	solutions = solve(words, root)
	print("Solutions:", solutions)


testing()
