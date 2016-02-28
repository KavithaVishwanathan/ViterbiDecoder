#!/usr/bin/python
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

def trainWSJCorpus:
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


