#!/usr/bin/env python

import re

def reverseComplement(bp): # Very efficient. Don't question it.
	bpdict = {'A':'T','a':'t','C':'G','c':'g','G':'C','g':'c','T':'A','t':'a'}
	return re.compile('|'.join(bpdict.keys())).sub(lambda x : bpdict[x.group()], bp)[::-1]

def generatePrimers(template, output, fPrimerCap = "", rPrimerCap = ""):
	templateFIndex = template.find(output[len(fPrimerCap):-len(rPrimerCap)])
	templateRIndex = template.find(output[len(fPrimerCap):-len(rPrimerCap)]) + len(output) - len(fPrimerCap) - len(rPrimerCap)
	fPrimer = fPrimerCap + template[templateFIndex:templateFIndex+26]
	rPrimer = rPrimerCap + reverseComplement(bp=template[templateRIndex-26:templateRIndex])
	return [fPrimer, rPrimer]

def simulatePCR(template, fPrimer, rPrimer):
	# Default values in case primers do not match
	templateFIndex=templateFLength=templateRIndex=templateRLength=-1
	for i in range(8,50)[::-1]: # Count down from 49 to 8 to find maximum primer length
		templateFIndex = template.find(fPrimer[-i:])
		if templateFIndex > -1:
			templateFLength=i
			break
	if templateFIndex == -1: # No match was ever found for forward primer
		return ""
	for i in range(8,50)[::-1]:
		templateRIndex = template.find(reverseComplement(bp=rPrimer[-i:]))
		if templateRIndex > -1:
			templateRLength=i
			break
	if templateRIndex == -1: # No match was ever found for rear primer
		return ""
	shouldNotContainBitsOPrimers = template[templateFIndex+templateFLength-7:templateRIndex+7]
	if (shouldNotContainBitsOPrimers.find(fPrimer[-8:]) > -1) or (shouldNotContainBitsOPrimers.find(reverseComplement(bp=rPrimer[-8:])) > -1):
		# This means that the tail end of a primer was found in the middle of the output strand, not including the part of the output strand meant to match with primers
		return None
	return fPrimer[:-templateFLength]+template[templateFIndex:templateRIndex+templateRLength]+reverseComplement(rPrimer[:-templateRLength])
	#       fPrimer cap                        only the subset between the primer matches                 rPrimer cap