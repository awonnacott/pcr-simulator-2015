#!/usr/bin/env python

import re

def reverseComplement(bp):
	bpdict = {'A':'T','a':'t','C':'G','c':'g','G':'C','g':'c','T':'A','t':'a'}
	return re.compile('|'.join(bpdict.keys())).sub(lambda x : bpdict[x.group()], bp)[::-1]

def generatePrimers(template, output, primerCap = ""):
	templateFIndex = template.find(output)
	templateRIndex = template.find(output) + len(output)
	fPrimer = template[templateFIndex:templateFIndex+18]
	rPrimer = reverseComplement(bp=template[templateRIndex-18:templateRIndex])
	return [primerCap + fPrimer, reverseComplement(bp=primerCap) + rPrimer]

def simulatePCR(template, fPrimer, rPrimer):
	templateFIndex=-1
	templateFLength=-1
	for i in range(8,50)[::-1]:
		templateFIndex = template.find(fPrimer[-i:])
		if templateFIndex > -1:
			templateFLength=i
			break
	if templateFIndex == -1:
		return ""
	templateRIndex=-1
	templateRLength=-1
	for i in range(8,50)[::-1]:
		templateRIndex = template.find(reverseComplement(bp=rPrimer[-i:]))
		if templateRIndex > -1:
			templateRLength=i
			break
	if templateRIndex == -1:
		return ""
	shouldNotContainBitsOPrimers = template[templateFIndex+templateFLength-7:templateRIndex+7]
	if (shouldNotContainBitsOPrimers.find(fPrimer[-8:]) > -1) or (shouldNotContainBitsOPrimers.find(reverseComplement(bp=rPrimer[-8:])) > -1):
		return None
	return fPrimer[:-templateFLength]+template[templateFIndex:templateRIndex+templateRLength]+reverseComplement(rPrimer[:-templateRLength])
