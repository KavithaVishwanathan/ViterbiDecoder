#!/usr/bin/python
#import pudb; pu.db
import re
from collections import defaultdict

def readCorpus(featurefile):
	if (featurefile.find("-name") != -1):
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
				nptag = contents[2]
				nametag = ""
				lines.append((word,tag,nptag,nametag))
			else:
				lines.append(contents)
		return lines

def readNameFile():
	namefile = open("names.txt", 'r')
	names = []
	for line in namefile:
		name = line.strip('\n').split()
		names.append(name[0].upper())
	return names

def readLocationFile():
	locationfile = open("locations.txt", 'r')
	locations = []
	for line in locationfile:
		location = line.strip("\n").replace("\t",'').replace("\r","").split(" ")
		locations.extend(location)
	locations = list(set(locations))
	locations = [location.upper() for location in locations]
	return locations

def readCompanyFile():
	companyfile = open("companylist.csv", 'r')
	companies = []
	for line in companyfile:
		company = line.strip('\n').replace('"','').split(',')
		companies.extend(company)
	companies = list(set(companies))
	companies = [company.upper() for company in companies]
	return companies

def featureBuilder(featurefile, outputfile):
	names = readNameFile()
	locations = readLocationFile()
	companies = readCompanyFile()

	with open(outputfile,'w') as resultfile:
		lines = readCorpus(featurefile)
		for i in range(len(lines)):
			#doc start
			if lines[i][0] == "-DOCSTART-":
				resultfile.write("-DOCSTART-" + "\t" + "-X-" + "\t" + "O" + "\t" +"O" + "\n")

			#empty line
			elif len(lines[i]) == 1:
				resultfile.write("\n")

			else:
				firstWord = isFirstWord(lines[i-1])
				capitalized = isCapitalized(lines[i])
				#prevName = findPrevName(prevLine)
				prevComma = isPrevComma(lines[i-1])
				person = isPerson(lines[i],names)
				location = isLocation(lines[i],locations)
				prevtag = findPrevtag(lines[i-1])
				nexttag = findNexttag(lines[i+1])
				prevword = findPrevWord(lines[i-1])
				prevPrevword = findPrevPrevWord(lines[i-2])
				nextword = findNextWord(lines[i+1])
				wordCaps = isWordCaps(lines[i])
				prevNPhrase = findPrevNPhrase(lines[i-1])
				nextNPhrase = findNextNPhrase(lines[i+1])
				#conjunction = isConjunction(lines[i])
				noAlpha = isNoAlpha(lines[i])
				company = isCompany(lines[i],companies)
				if (i+2) < len(lines):
					nextNextWord = findNextNextWord(lines[i+2])

				#prevWordAtorBy = isPrevWordAtorBy(lines[i-1])

				resultfile.write(lines[i][0] + "\t" + "firstWord=" + firstWord + "\t" + "isCapitalized=" + capitalized + "\t" 
					+ "isPrevComma=" + prevComma + "\t" + "isPerson=" + person + "\t" + "prevtag=" + prevtag + "\t"
					+ "currtag=" + lines[i][1] + "\t" + "nexttag=" + nexttag + "\t" + "prevword=" + prevword + "\t"
					+ "currword=" + lines[i][0] + "\t" + "nextword=" + nextword + "\t" + "prevtoPrevWord=" + prevPrevword + "\t"
					+ "isNoAlpha=" + noAlpha + "\t" + "isCompany=" + company + "\t" + "isLocation=" + location + "\t"
					+ "prevNPhrase=" + prevNPhrase + "\t" + "currNPhrase=" + lines[i][2] + "\t" + "nextNPhrase=" + nextNPhrase + "\t"
					+ lines[i][3] + "\n")
				# "isPrevWordAtorBy=" + prevWordAtorBy + "\t" + "isLocation=" + location + "\t" "nextNextWord=" + nextNextWord + "\t"
#def checkFeature(prevLine, currLine, nextLine,names):
	

def isFirstWord(prevLine):
	if len(prevLine) == 1:
		return "true"
	else:
		return "false"

def isCapitalized(currLine):
	if currLine[0] == currLine[0].capitalize():
		return "true"
	else:
		return "false"

def findPrevtag(prevLine):
	if len(prevLine) == 1:
		return "@@"
	else:
		return prevLine[1]

def findNexttag(nextLine):
	if len(nextLine) == 1:
		return "@@"
	else:
		return nextLine[1]

def findPrevWord(prevLine):
	if len(prevLine) == 1:
		return "@@"
	else:
		return prevLine[0]

def findPrevPrevWord(prevPrevLine):
	if len(prevPrevLine) == 1 or prevPrevLine[0] == "-DOCSTART-":
		return "@@"
	else:
		return prevPrevLine[0]

def findNextWord(nextLine):
	if len(nextLine) == 1:
		return "@@"
	else:
		return nextLine[0]

def findNextNextWord(nextNextLine):
	if len(nextNextLine) == 1:
		return "@@"
	else:
		return nextNextLine[0]

def findPrevNPhrase(prevLine):
	if len(prevLine) == 1:
		return "@@"
	else:
		return prevLine[2]

def findNextNPhrase(nextLine):
	if len(nextLine) == 1:
		return "@@"
	else:
		return nextLine[2]

def isPrevComma(prevLine):
	if prevLine[0] == ",":
		return "true"
	else:
		return "false"	

def isPerson(currLine,names):
	if currLine[0].upper() in names:
		return "true"
	else:
		return "false"

def isLocation(currLine,locations):
	if currLine[0].upper() in locations:
		return "true"
	else:
		return "false"	

def isCompany(currLine,companies):
	if currLine[0].upper() in companies:
		return "true"
	else:
		return "false"	

def isWordCaps(currLine):
	if currLine[0].isupper():
		return "true"
	else:
		return "false"

def isPrevWordAtorBy(prevLine):
	if prevLine[0].lower() == "at" or prevLine[0].lower() == "by":
		return "true"
	else:
		return "false"

def isConjunction(currLine):
	if currLine[1] == "CC":
		return "true"
	else:
		return "false"

def isNoAlpha(currLine):
	if re.search('[a-zA-Z]', currLine[0]) == None:
		return "true"
	else:
		return "false"	


#pass the input file name and the output filename
#featureBuilder("CONLL_train.pos-chunk-name", "train.feature")
#featureBuilder("CONLL_dev.pos-chunk","dev.feature")
featureBuilder("CONLL_test.pos-chunk","test.feature")
#readLocationFile()