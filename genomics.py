#!/usr/bin/env python

def generatePrimers(template, output):
	fPrimer = "AACCGGTTacgcccgAGCCTCCCG" # replace this
	rPrimer = "ATCGGGGTCCCCAAACAAACC"
	return [fPrimer, rPrimer]


def simulatePCR(template, fPrimer, rPrimer):
	output = "AAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCCAAATTTTCCCC" # replace this
	return output


def verifyPrimers(template, fPrimer, rPrimer, output):
	simOutput = simulatePCR(template=template, fPrimer=fPrimer, rPrimer=rPrimer)
	checkPass = simOutput == output
	return [checkPass, simOutput]