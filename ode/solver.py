#IMPORT LIBS#######################################################################################
import numpy as np
import sys

###################################################################################################
#MAIN TOOL FOR SOLVE ODE
#uses file rp.py of this package to obtain ODE and other
#OPTIONS
#  dt    - the integration time step
#  total - main integration time
#  relax - relax time will be ignored inresult
#  pars  - parameters to be shanges in ode system
#  file  - file with SODE notation
#  randinit - weights for randomizing initial values

def solve(**kwargs):
	#Set path
	sys.path.append('/pylib')
	#Set default values of system parameters
	NST_FSAVE = 100
	total = 10
	dt = 0.01
	relax = 0.0
	saveFile = ''
	issaveFile = False
	#Read input parameters
	if 'total' in kwargs.keys():
		total = kwargs['total']
	if 'dt' in kwargs.keys():
		dt = kwargs['dt']
	if 'dtsave' in kwargs.keys():
		dtsave = kwargs['dtsave']
	if 'relax' in kwargs.keys():
		relax = kwargs['relax']
	if 'file' in kwargs.keys():
		import lpi.ode.rpgen
		lpi.ode.rpgen.fromtxt(kwargs['file'])
	if 'save' in kwargs.keys():
		saveFile = open(kwargs['save'], "w")
		issaveFile = True
	
	import lpi.ode.rp
	pars = lpi.ode.rp.getPars()
	x0 = lpi.ode.rp.getInit()
	dim = lpi.ode.rp.getDim()

	if 'pars' in kwargs.keys():
		chpars = kwargs['pars']
		for p in chpars:
			pars = lpi.ode.rp.setPar(p, chpars[p], pars)
	
	if 'randinit' in kwargs.keys():
		randinit = np.array(kwargs['randinit'])
		if len(randinit) != len(x0):
			sys.stderr.write("Warning : solver::solve can't randomize init,	weights and inits not aligned")
		else:
			x0 = np.random.random(size=dim) * randinit


	from scipy.integrate import ode

	solver = ode(lpi.ode.rp.f).set_integrator('vode', method='bdf', with_jacobian=False)
	solver.set_initial_value(x0, 0.0)
	solver.set_f_params(pars)

	#Relax run
	if relax > 0:
		while solver.successful() and solver.t < relax:
			solver.integrate(solver.t + dt)		
		x0 = solver.y
		solver.set_initial_value(x0, 0.0)
	#Production run
	y = []
	t = []
	#Simple integration
	y.append(x0)
	t.append(0.0)
	if issaveFile:
		np.savetxt(saveFile, [np.concatenate(([0.0], x0))], delimiter = ';')
		savenum = 1
	while solver.successful() and solver.t < total:
		solver.integrate(solver.t + dt)
		if issaveFile and np.abs( dtsave * savenum - solver.t ) < dt:
			np.savetxt(saveFile, [np.concatenate(([solver.t], solver.y))], delimiter = ';')
			savenum += 1
		# else:
		# 	y.append(solver.y)
		# 	t.append(solver.t)

	t = np.array(t)
	y = np.array(y)
	return t, y

###################################################################################################
#MAKE POINCARE MAP TO CALC PERIOD OF OSCILLATIONS
#
def calcPeriod(t, y):
	if len(y.shape) == 2:
		y = y[:, 0]
	ymax = y.max()
	ymin = y.min()
	pcpoints = [ (ymin + i * (ymax - ymin)/4) for i in xrange(1,4) ]