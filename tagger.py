#!/usr/bin/python
import numpy as np
from collections import defaultdict
from itertools import chain


def trainWSJCorpus():
	#read the training pos file
	posfile = open("WSJ_02-21.pos", 'r')
	prevpos = "start"
	wordcout_dict = defaultdict(int)
	tags = {}

	for line in posfile:
		wordpos = line.split("\t")
		if len(wordpos) > 1:
			word = wordpos[0]
			currpos = wordpos[1].strip("\n")
			tags.setdefault(word,[]).append(currpos)
			StateCount(currpos,word,prevpos, wordcout_dict)
			prevpos = currpos
		else:
			StateCount("end","",prevpos, wordcout_dict)
			prevpos = "start"

	#to remove duplicates from list
	tag_dict = {}
	for k,v in tags.items():
		tag_dict[k] = list(set(v))
	return wordcout_dict, tag_dict

def StateCount(currpos,word,prevpos, wordcout_dict):
	if prevpos == "start":
		key1 = "STATE START"
		wordcout_dict[key1] += 1
	if currpos != "end": 
		key2 = "STATE " + currpos
		wordcout_dict[key2] += 1
		key3 = currpos + " emit " + word
		wordcout_dict[key3] += 1
	key4 = prevpos + " to " + currpos
	wordcout_dict[key4] += 1


def FindStates(tokenList, tag_dict):
	finalStateList = ["START"]
	stateList = []
	for token in tokenList:
		if token in tag_dict:
			stateList.append(tag_dict[token])
	combinedStateList = list(set(chain.from_iterable(stateList)))
	for i in range(0,len(combinedStateList)-1):
		finalStateList.append(combinedStateList[i])
	finalStateList.append("END")
	return finalStateList

def obs():
	finallist = []
	lineList = ["START"]
	posfile = open("WSJ_24.words", 'r')
	for line in posfile:
		if len(line) > 1:
			lineList.append(line.strip("\n"))
		else:
			lineList.append("END")
			finallist.append(lineList)
			lineList = ["START"]
	return finallist

def viterbi():
	wordcout_dict, tag_dict = trainWSJCorpus()
	obslist = obs()
	for tokenList in obslist:
		stateList = FindStates(tokenList, tag_dict)
		print stateList
		print tokenList
		# matrix = np.zeros(((len(stateList)),len(tokenList)))
		# matrix[0,0] = 1
		# print matrix.shape
		# for t in xrange(1,len(tokenList)-1):
		# 	for i in xrange(1,len(stateList)-1):
		# 		for j in xrange(0,len(stateList)-1):
		# 			tran_prob = ( wordcout_dict[stateList[i] + " to " + stateList[j]] ) / wordcout_dict["STATE " + stateList[j]]
		# 			emit_prob = ( wordcout_dict[stateList[j] + " emit " + tokenList[t]] )/ wordcout_dict["STATE " + stateList[j]]
		# 			score = matrix[i,t] * tran_prob * emit_prob
		# 			if score > matrix[j,t+1]:
		# 				matrix[j,t+1] = score
		# 				best_parent[j] = i

		matrix = np.zeros(((len(stateList)),len(tokenList)))
		matrix[0,0] = 1
		print matrix.shape
		for i in xrange(1,len(tokenList)):
			for j in xrange(1,len(stateList)):
				(prob, state) = max((matrix[i-1,k],k) for k in xrange(0,len(stateList)))
				matrix[i,j] = prob
		print matrix
		print matrix.shape

	#print  stateList

viterbi()	

