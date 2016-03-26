import re



def fromtxt(filename):
	res = True
	errorMsg = ""
	try:
		ff = open(filename, 'r')
	except ValueError:
		res = False
		errorMsg = "Can't open file `%s' for reading" % filename
		return res, errorMsg
	#Initialise main vars
	init = {}
	pars = {}
	varls = []
	odes = []
	eqs = []
	#Parsing file
	for rwl in ff:
		ss = rwl.translate(None, "\r\n\t ")
		if len(ss) < 3 or ss[0] == '#':
			continue
		if ss[0:3] == 'PAR':
			res, errorMsg, pars = processParStr(ss, pars)
			if not res:
				return res, errorMsg
			continue
		if ss[0:4] == 'INIT':
			res, errorMsg, init = processInitStr(ss, init)
			if not res:
				return res, errorMsg
			continue
		var, ode = checkForODE(ss)
		if var:
			odes.append(ode)
			varls.append(var)
			if var not in init.keys():
				init[var] = (0, True)
			continue
		if checkForEq(ss):
			eqs.append(ss)
	#Write rp file
	writeRPfile(init, pars, varls, odes, eqs)


def processParStr(parstr, pars):
	parstr = parstr.strip("\t ")
	if len(parstr) < 3 or parstr[0:3] != 'PAR':
		return False, "rpgen::processParStr this is not parsStr", pars
	parstr = parstr[3:len(parstr)]
	parstr = parstr.translate(None, "\r\n\t ")
	parstrs = parstr.split(',')
	for pstr in parstrs:
		spar = pstr.split('=')
		try:
			pv = float(spar[1])
		except ValueError:
			return False, "rpgen::processParStr can't convert `%s' to float" % spar[1], pars
		pars[spar[0]] = pv
	return True, '', pars

def processInitStr(initstr, init):
	initstr = initstr.strip("\t ")
	if len(initstr) < 4 or initstr[0:4] != 'INIT':
		return False, "rpgen::processInitStr this is not parsStr", pars
	initstr = initstr[4:len(initstr)]
	initstr = initstr.translate(None, "\r\n\t ")
	initstrs = initstr.split(',')
	for istr in initstrs:
		sinit = istr.split('=')
		try:
			iv = float(sinit[1])
		except ValueError:
			return False, "rpgen::processInitStr can't convert `%s' to float" % sinit[1], init
		init[sinit[0]] = (iv, False)
	return True, '', init

def checkForODE(string):
	string = string.translate(None, "\r\n\t ")
	p = re.compile('d\w+/dt=')
	srch = p.search(string)
	varname = None
	ode = None
	if srch and srch.start() == 0:
		varname = string[(srch.start()+1):(srch.end()-4)]
		ode = string[srch.end():len(string)]
	return varname, ode

def checkForEq(string):
	string = string.translate(None, "\r\n\t ")
	p = re.compile('\w+=')
	srch = p.match(string)
	if srch:
		return True
	else:
		return False

def writeRPfile(init, pars, varls, odes, eqs):
	vdim = len(varls)
	pdim = len(pars)
	parnames = pars.keys()
	f = open('/data/lib/lpi/ode/rp.py', 'w')
	f.write("import numpy as np\n\n")

	#write main f() function
	f.write("def f(t, x, pars):\n")
	f.write("\t#Variables\n")
	for i in xrange(vdim):
		f.write("\t%s = x[%d]\n" %(varls[i], i))
	f.write("\t#Parameters\n")
	for i in xrange(pdim):
		f.write("\t%s = pars[%d]\n" %(parnames[i], i))
	if len(eqs) > 0:
		f.write("\t#Additional equations\n")
		for i in xrange(len(eqs)):
			f.write("\t" + eqs[i] + "\n")
	f.write("\t#ODE System\n")
	f.write("\todeRightPart = np.zeros(%d)\n" % vdim)
	for i in xrange(vdim):
		f.write("\todeRightPart[%d] = %s\n" % (i, odes[i]))
	f.write('\treturn odeRightPart\n\n')

	#write additional functions
	f.write('def getInit():\n')
	f.write("\tinit = np.zeros(%d)\n" % vdim)
	for i in xrange(vdim):
		val, rand = init[ varls[i] ]
		f.write("\tinit[%d] = %f\n" % (i, val))
	f.write("\treturn init\n\n")

	f.write('def getPars():\n')
	f.write("\tpars = np.zeros(%d)\n" % pdim)
	for i in xrange(pdim):
		f.write("\tpars[%d] = %f\n" % (i, pars[ parnames[i] ]) )
	f.write("\treturn pars\n\n")

	f.write("def setPar(name, value, pars):\n")
	f.write("\t#define parnames dict\n")
	f.write("\tpardict = {\n")
	for i in xrange(0, pdim):
		f.write("\t\t\"%s\" : %d,\n" % (parnames[i], i))
	f.write("\t\t}\n")
	f.write("\tif name in pardict.keys():\n")
	f.write("\t\tpars[ pardict[name] ] = value\n")
	f.write("\treturn pars\n\n")

	f.write("def getDim():\n")
	f.write("\treturn %d\n\n" % vdim)

