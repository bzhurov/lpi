#!/usr/bin/env python

import sys

f = open(sys.argv[1], "r")

def print_mul(par, mul):
	sys.stdout.write(str(par) + ';')
	for i in xrange(len(mul)):
		sys.stdout.write(str(mul[i]))
		if i < len(mul) - 1:
			sys.stdout.write(';')
		else:
			sys.stdout.write("\n")

start = False
startPar = False
endPar = False
startMul = False
startRead = True

for rwl in f:
	rwl = rwl.rstrip("\n\r")
	# Check '==='
	if len(rwl) > 0 and rwl[0] == '=':
		start = True
		endPar = False

		if not startRead:
			print_mul(par, mul)
		else:
			startRead = False

		par = None
		mul = []

		continue
	if not start:
		continue

	# Try to find PAR
	if len(rwl) > 26 and rwl[23:26] == "PAR" and not endPar:
		startPar = True
		continue
	if startPar:
		par = float(rwl[22:33])
		# print "PPPPPP:", par
		startPar = False
		endPar = True
		continue

	# print len(rwl), rwl[19:29]
	# Try to read multiplier
	if len(rwl) > 85 and rwl[19:29] == "Multiplier":
		mul.append(float(rwl[35:47]))
		mul.append(float(rwl[49:61]))
		mul.append(float(rwl[74:86]))


