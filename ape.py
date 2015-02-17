#!/usr/bin/env python

import re

def readBP(filename):
	file = open(filename, 'r')
	while file.readline().find("ORIGIN") == -1:
		pass
	contents = file.read()
	return re.sub('[^AGCTagct]', '', contents).upper()

def writeBP(filename, bp):
	file = open(filename, 'w')
	file.write("LOCUS\n")
	file.write("ORIGIN\n")
	file.write(bp)
	file.close()

#def readAPE()
#def writeAPE()