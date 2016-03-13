#!/usr/bin/env python

from sys import argv, stdout, stderr, stdin

if len(argv) != 2:
	stderr.write("Usage: " + argv[0] + " <macros>\n")
	exit(1)

f = open(argv[1], "r")
if not f:
	stderr.write("Cannot open file `" + argv[1] + "' for reading\n")
	exit(1)
lN = 0
mc = {}
for rln in f:
	lN += 1
	sln = rln.strip(" \t\r\n\v")
	if not sln:
		continue
	xln = sln.split("\t")
	if len(xln) != 2:
		stderr.write("Macro line #" + str(lN) + ": bad line `" + rln.rstrip("\r\n") + "'\n")
		continue
	if xln[0] in mc:
		stderr.write("Macro line #" + str(lN) + ": duplicate name '" + xln[0] + "'\n")
		continue
	mc[xln[0]] = xln[1]

lN = 0
for ln in stdin:
	lN += 1
	out = ln
	todo = 1
	repCMax = 100
	repC = 0
	while todo and repC < repCMax:
		repC += 1
		todo = 0
		for mcn in mc:
			xres = ""
			bg = 0
			while bg < len(out):
				end = out.find(mcn, bg)
				if end == -1:
					end = len(out)
					break
				xres += out[bg:end]
				xres += mc[mcn]
				bg = end + len(mcn)
				end = bg
			xres += out[bg:end]
			if xres != out:
				todo += 1
			out = xres
	if repC >= repCMax:
		stderr.write("Input line #" + str(lN) + ": too many levels (>" + str(repCMax) + \
			", probably an infinite loop) in macro substitution: line `" + ln.rstrip("\r\n") + "'\n")
	else:
		stdout.write(out)
exit(0)
