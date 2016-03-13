#!/usr/bin/env python

from sys import stdin, stdout

for rwl in stdin:
	n = len(rwl)
	for i in xrange(0, n):
		if rwl[i] == '*' and i < n - 1 and rwl[i+1] == '*':
			rb = 0
			lb = 0
			firstFound = False
			for j in xrange(i-1, -1):
				if (not firstFound) and (rwl[j] == ' '):
					continue
				if (not firstFound):
					firstFound = True
				if rwl[j] == ')':
					rb += 1
				if rwl[j] == '(':
					lb += 1
				if rwl[j] == '-' or rwl[j] == '+' or rwl[j] == '*' or rwl[j] == '/' or rwl[j] == ' ':
					if rb == lb:
						