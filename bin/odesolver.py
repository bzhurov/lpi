#!/usr/bin/env python
#This is main ode solver program
#Firstly - set path variable
import numpy as np
from sys import path, argv
from lpi.ode.solver import solve as odesolver

cpars = {
	'rm': 0.045,
	'omega': 1.0
}

t, y = odesolver(file = argv[1], randinit = [30, 30, 30, 30, 100, 100, 100, 100, 100], 
	total = 5e10, relax = 1e5, dt = 0.1, pars = cpars, save = argv[2], dtsave = 100)


import matplotlib.pyplot as plt
plt.plot(t, y[:,1], 'o')
plt.show()
