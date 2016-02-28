#!/usr/bin/python
import numpy as np
from collections import defaultdict

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

def trainWSJCorpus():
	#read the training pos file
	posfile = open("WSJ_02-21.pos", 'r')
	prevpos = "start"
	wordcout_dict = defaultdict(int)
	for line in posfile:
		wordpos = line.split("\t")
		if len(wordpos) > 1:
			word = wordpos[0]
			currpos = wordpos[1].strip("\n")
			StateCount(currpos,word,prevpos, wordcout_dict)
			prevpos = currpos
		else:
			StateCount("end","",prevpos, wordcout_dict)
			prevpos = "start"
	return wordcout_dict

def FindTags():
	posfile = open("WSJ_02-21.pos", 'r')
	tags = {}
	for line in posfile:
		wordpos = line.split("\t")
		if len(wordpos) > 1:
			word = wordpos[0]
			tag = wordpos[1].strip("\n")
			tags.setdefault(word,[]).append(tag)
	#to remove duplicates from list
	tag_dict = {}
	for k,v in tags.items():
		tag_dict[k] = list(set(v))
	return tag_dict

def FindStates(tokenList):
	tag_dict = FindTags()
	stateList = []
	for token in tokenList:
		stateList.append(tag_dict[token])
	return stateList

def obs():
	finallist = []
	lineList = []
	posfile = open("WSJ_24.words", 'r')
	for line in posfile:
		if len(line) > 1:
			lineList.append(line.strip("\n"))
		else:
			finallist.append(lineList)
			lineList = []
	return finallist

def viterbi():
	obslist = obs()
	for tokenList in obslist:
		stateList = FindStates(tokenList)
		#np.zeros((len(stateList)),len(tokenList))
	print  stateList

viterbi()	

