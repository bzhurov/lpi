import numpy as np

def f(t, x, pars):
	#Variables
	M1 = x[0]
	M2 = x[1]
	M3 = x[2]
	MI = x[3]
	P1 = x[4]
	P2 = x[5]
	P3 = x[6]
	PI = x[7]
	S = x[8]
	#Parameters
	pR = pars[0]
	gt = pars[1]
	kRud = pars[2]
	kRur = pars[3]
	rp = pars[4]
	rs = pars[5]
	kur = pars[6]
	dp = pars[7]
	rm = pars[8]
	rmI = pars[9]
	kua = pars[10]
	dm = pars[11]
	kRr = pars[12]
	delta = pars[13]
	omega = pars[14]
	ds = pars[15]
	kRd = pars[16]
	ka = pars[17]
	kud = pars[18]
	kd = pars[19]
	kr = pars[20]
	eta = pars[21]
	#Additional equations
	sigma=kd/(delta*dp+kud)
	kappa=kr/kur
	H1=(P1**2)*kappa*sigma+1
	H2=(P2**2)*kappa*sigma+1
	H3=(P3**2)*kappa*sigma+1
	kappaS=ka*pR/kua
	sigmaR=kRd*kd/(delta*dp+kRud*kud)
	kappaR=kRr*kr/(kRur*kur)
	HS=(S**2)*kappaR*(kappaS**2)*sigmaR+1
	#ODE System
	odeRightPart = np.zeros(9)
	odeRightPart[0] = -M1*dm+gt*rm/H3
	odeRightPart[1] = -M2*dm+gt*rm/H1
	odeRightPart[2] = -M3*dm+rm*(omega*(gt-gt/((S**2)*kRr*kappa*(kappaS**2)*sigmaR/kRur+1))+gt/H2)
	odeRightPart[3] = -MI*dm+gt*rm*rmI/H1
	odeRightPart[4] = (M1*rp-2*(P1**2)*delta*dp*sigma-P1*dp)/(4*P1*sigma+1+8*P1*gt*kappa*sigma/(H1**2))
	odeRightPart[5] = (M2*rp-2*(P2**2)*delta*dp*sigma-P2*dp)/(4*P2*sigma+1+4*P2*gt*kappa*sigma/(H2**2))
	odeRightPart[6] = (M3*rp-2*(P3**2)*delta*dp*sigma-P3*dp)/(4*P3*sigma+1+4*P3*gt*kappa*sigma/(H3**2))
	odeRightPart[7] = MI*rp-PI*dp
	odeRightPart[8] = (PI*rs-(S**2)*delta*dp*(kappaS**2)*sigmaR-S*(ds+eta))/(4*(S**2)*(kappaS**2)*sigmaR+4*S*gt*kRr*kappa*(kappaS**2)*sigmaR/(kRur*((S**2)*kRr*kappa*(kappaS**2)*sigmaR/kRur+1)**2)+kappaS+1)
	return odeRightPart

def getInit():
	init = np.zeros(9)
	init[0] = 0.000000
	init[1] = 0.000000
	init[2] = 0.000000
	init[3] = 0.000000
	init[4] = 0.000000
	init[5] = 0.000000
	init[6] = 0.000000
	init[7] = 0.000000
	init[8] = 0.000000
	return init

def getPars():
	pars = np.zeros(22)
	pars[0] = 5.000000
	pars[1] = 20.000000
	pars[2] = 0.034000
	pars[3] = 1.666700
	pars[4] = 0.100000
	pars[5] = 0.006700
	pars[6] = 0.900000
	pars[7] = 0.003300
	pars[8] = 0.000000
	pars[9] = 0.100000
	pars[10] = 0.100000
	pars[11] = 0.003300
	pars[12] = 0.000833
	pars[13] = 0.000000
	pars[14] = 1.000000
	pars[15] = 0.000017
	pars[16] = 0.034000
	pars[17] = 0.050000
	pars[18] = 0.500000
	pars[19] = 0.025000
	pars[20] = 0.012000
	pars[21] = 0.006700
	return pars

def setPar(name, value, pars):
	#define parnames dict
	pardict = {
		"pR" : 0,
		"gt" : 1,
		"kRud" : 2,
		"kRur" : 3,
		"rp" : 4,
		"rs" : 5,
		"kur" : 6,
		"dp" : 7,
		"rm" : 8,
		"rmI" : 9,
		"kua" : 10,
		"dm" : 11,
		"kRr" : 12,
		"delta" : 13,
		"omega" : 14,
		"ds" : 15,
		"kRd" : 16,
		"ka" : 17,
		"kud" : 18,
		"kd" : 19,
		"kr" : 20,
		"eta" : 21,
		}
	if name in pardict.keys():
		pars[ pardict[name] ] = value
	return pars

def getDim():
	return 9

