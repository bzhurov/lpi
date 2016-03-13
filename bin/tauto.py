#!/usr/bin/env python

import sys
sys.path.append('/pylib')
import lpi
import matplotlib.pyplot as plt

fprs = lpi.auto.parser(sys.argv[1], sys.argv[2])

fig = plt.figure()

fprs.draw(plt, brnum = 3)
plt.show()

#print fprs.bifcsv(bifstop = False)
#print fprs.pars
#print fprs.stable