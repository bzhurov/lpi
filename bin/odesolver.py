#!/usr/bin/env python
#This is main ode solver program
#Firstly - set path variable
import argparse
import numpy as np
from sys import path, argv
from lpi.ode.solver import solve as odesolver
import geronorm.solarized

parser = argparse.ArgumentParser(description="Solve and plot SODE")
parser.add_argument
parser.add_argument('ode', type = str, default = '', help = 'file for time series saving')
parser.add_argument('-t', type = float, default = 1e2, help = 'file for time series saving')
parser.add_argument('-dt', type = float, default = 0.1,  help = 'file for time series saving')

pnames = []
for a in argv:
	if len(a) > 2 and a[:2] == '--':
		parser.add_argument(a, type = float, help = 'set value for parameter %s' % a)
		pnames.append(a[2:])
cpars = {}
args = parser.parse_args(argv[1:])
pars = vars(args)
for p in pnames:
	cpars[p] = pars[p]

#defaults
total = 1e2
relax = 1e3
dt = 0.1

#Settings
if 't' in pars:
	total = pars['t']
if 'dt' in pars:
	dt = pars['dt']

t, y = odesolver(file = pars['ode'], 
	total = total, relax = 1e1, dt = dt, dtsave = 1, pars = cpars)


print 'Max :', np.max(y, axis = 0)
print 'Min :', np.min(y, axis = 0)
import matplotlib.pyplot as plt
plt.plot(t, y[:,0], '-')
plt.plot(t, y[:,1], '-')
plt.plot(t, y[:,2], '-')
plt.plot(t, y[:,3], ':')
plt.plot(t, y[:,4], ':')
plt.plot(t, y[:,5], ':')

plt.show()
