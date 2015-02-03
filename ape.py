#!/usr/bin/env python

import re

def readBP(filename):
	file = open(filename, 'r')
	while file.readline() != "ORIGIN\n":
		pass
	contents = file.read()
	print contents
	return re.sub('[^AGCTagct]', '', contents)

def writeBP(filename, bp):
	file = open(filename, 'w')
	file.write("LOCUS\n")
	file.write("ORIGIN\n")
	file.write(bp)
	file.close()

#def readAPE()
#def writeAPE()