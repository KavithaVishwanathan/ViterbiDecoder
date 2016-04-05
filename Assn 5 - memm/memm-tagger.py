#!/usr/bin/python
#import pudb; pu.db
import numpy as np
from collections import defaultdict
from itertools import chain

#Step 1: Train the WSJ Corpus. The output of this function will be two dictionaries, 
#one will have the count needed for different probablities (emit and trans)
#the other will have all the words and it's corresponding tags as values
def readCorpus(featurefile):
	if (featurefile.find("chunk") != -1):
		chunkfile = open(featurefile, 'r')
		prev = "\n"
		wordcount_dict = defaultdict(int)
		lines = []
		for line in chunkfile:
			lines.append(line.strip("\n").split("\t"))
		return lines
	else:
		chunkfile = open(featurefile, 'r')
		prev = "\n"
		wordcount_dict = defaultdict(int)
		lines = []
		for line in chunkfile:
			contents = line.strip("\n").split("\t")
			if len(contents) > 1:
				word = contents[0]
				tag = contents[1]
				nptag = ""
				lines.append((word,tag,nptag))
			else:
				lines.append(contents)
		return lines

def featureBuilder(featurefile, outputfile):
	with open(outputfile,'w') as resultfile:
		lines = readCorpus(featurefile)
		for i in range(len(lines)):
			if len(lines[i]) == 1:
				resultfile.write("\n")
			elif len(lines[i+1]) == 1 and len(lines[i-1]) == 1:
				firstWord = "true"
				prevword = "@@"
				currword = (lines[i])[0]
				nextword = "@@"
				prevtag = "@@"
				currtag = (lines[i])[1]
				nexttag = "@@"
				nphrase = (lines[i])[2]
				lastword = "true"
				if currtag == "CC":
					isConjunction = "true"
					beforeAndAfterCC = prevtag+"+"+currword+"+"+nexttag
				else:
					isConjunction = "false"
					beforeAndAfterCC = "null"
				if currword[0].isupper():
					isUpperCase = "true"
				else:
					isUpperCase = "false"
				if currword.isupper():
					isWordCaps = "true"
				else:
					isWordCaps = "false"
				if currword.find("-") != -1:
					ishyphenated = "true"
				else:
					ishyphenated = "false"
				resultfile.write(currword + "\t" + "firstWord=" + firstWord + "\t" + "prevTag=" + prevtag + "\t"
					+ "currTag=" + currtag + "\t" + "nextTag=" + nexttag + "\t" + "prevword=" + prevword + "\t"
					+ "currword=" + currword + "\t" + "nextword=" + nextword + "\t" + "isUpperCase=" + isUpperCase + "\t"
					+"beforeAndAfterCC=" + beforeAndAfterCC + "\t" + "isWordCaps=" + isWordCaps + "\t" 
					+ "ishyphenated=" + ishyphenated + "\t"
					+"isConjunction=" + isConjunction +"\t" + "islastword=" +lastword + "\t" + nphrase + "\n")
			elif i == len(lines)-1 or len(lines[i+1]) == 1:
				firstWord = "false"
				prevword = (lines[i-1])[0]
				currword = (lines[i])[0]
				nextword = "@@"
				prevtag = (lines[i-1])[1]
				currtag = (lines[i])[1]
				nexttag = "@@"
				nphrase = (lines[i])[2]
				lastWord = "true"
				if currtag == "CC":
					isConjunction = "true"
					beforeAndAfterCC = prevtag+"+"+currword+"+"+nexttag
				else:
					isConjunction = "false"
					beforeAndAfterCC = "null"
				if currword[0].isupper():
					isUpperCase = "true"
				else:
					isUpperCase = "false"
				if currword.isupper():
					isWordCaps = "true"
				else:
					isWordCaps = "false"
				if currword.find("-") != -1:
					ishyphenated = "true"
				else:
					ishyphenated = "false"
				resultfile.write(currword + "\t" + "firstWord=" + firstWord + "\t" + "prevTag=" + prevtag + "\t"
					+ "currTag=" + currtag + "\t" + "nextTag=" + nexttag + "\t" + "prevword=" + prevword + "\t"
					+"beforeAndAfterCC=" + beforeAndAfterCC + "\t" + "isWordCaps=" + isWordCaps + "\t"
					+ "currword=" + currword + "\t" + "nextword=" + nextword + "\t"  + "isUpperCase=" + isUpperCase + "\t"
					+ "ishyphenated=" + ishyphenated + "\t"
					+"isConjunction=" + isConjunction +"\t" + "islastword=" +lastword + "\t" + nphrase + "\n")
			elif len(lines[i-1]) == 1:
				firstWord = "true"
				prevword = "@@"
				currword = (lines[i])[0]
				nextword = (lines[i+1])[0]
				prevtag = "@@"
				currtag = (lines[i])[1]
				nexttag = (lines[i+1])[1]
				nphrase = (lines[i])[2]
				lastword = "false"
				if currtag == "CC":
					isConjunction = "true"
					beforeAndAfterCC = prevtag+"+"+currword+"+"+nexttag
				else:
					isConjunction = "false"
					beforeAndAfterCC = "null"
				if currword[0].isupper():
					isUpperCase = "true"
				else:
					isUpperCase = "false"
				if currword.isupper():
					isWordCaps = "true"
				else:
					isWordCaps = "false"
				if currword.find("-") != -1:
					ishyphenated = "true"
				else:
					ishyphenated = "false"
				resultfile.write(currword + "\t" + "firstWord=" + firstWord + "\t" + "prevTag=" + prevtag + "\t"
					+ "currTag=" + currtag + "\t" + "nextTag=" + nexttag + "\t" + "prevword=" + prevword + "\t"
					+ "currword=" + currword + "\t" + "nextword=" + nextword + "\t" +"beforeAndAfterCC=" + beforeAndAfterCC + 
					"\t" + "isWordCaps=" + isWordCaps + "\t" + "isUpperCase=" + isUpperCase + "\t" +"isConjunction=" + isConjunction 
					+ "ishyphenated=" + ishyphenated + "\t"
					+"\t" + "islastword=" +lastword + "\t"+ nphrase + "\n")
			else:
				firstWord = "false"
				prevword = (lines[i-1])[0]
				currword = (lines[i])[0]
				nextword = (lines[i+1])[0]
				prevtag = (lines[i-1])[1]
				currtag = (lines[i])[1]
				nexttag = (lines[i+1])[1]
				nphrase = (lines[i])[2]
				lastword = "false"
				if currtag == "CC":
					isConjunction = "true"
					beforeAndAfterCC = prevtag+"+"+currword+"+"+nexttag
				else:
					isConjunction = "false"
					beforeAndAfterCC = "null"
				if currword[0].isupper():
					isUpperCase = "true"
				else:
					isUpperCase = "false"
				if currword.isupper():
					isWordCaps = "true"
				else:
					isWordCaps = "false"
				if currword.find("-") != -1:
					ishyphenated = "true"
				else:
					ishyphenated = "false"
				resultfile.write(currword + "\t" + "firstWord=" + firstWord + "\t" + "prevTag=" + prevtag + "\t"
					+ "currTag=" + currtag + "\t" + "nextTag=" + nexttag + "\t" + "prevword=" + prevword + "\t"
					+ "currword=" + currword + "\t" + "nextword=" + nextword + "\t" + "isUpperCase=" + isUpperCase + "\t"
					+ "ishyphenated=" + ishyphenated + "\t"
					+"beforeAndAfterCC=" + beforeAndAfterCC + "\t" + "isWordCaps=" + isWordCaps + "\t"+"isConjunction=" + 
					isConjunction +"\t" + "islastword=" +lastword + "\t" + nphrase + "\n")		


#pass the input file name and the output filename
#featureBuilder("WSJ_02-21.pos-chunk","WSJ_02-21.feature")
featureBuilder("WSJ_23.pos","WSJ_23.feature")
