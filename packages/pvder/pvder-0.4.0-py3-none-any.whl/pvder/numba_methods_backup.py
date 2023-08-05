


#ma = ma_calc(self.Kp_GCC,self.ua,self.xa)
			#mb = mb_calc(self.Kp_GCC,self.ub,self.xb)
			#mc = mc_calc(self.Kp_GCC,self.uc,self.xc)



#self.vta = vta_calc(ma,self.Vdc)
			#self.vtb = vtb_calc(mb,self.Vdc)
			#self.vtc = vtc_calc(mc,self.Vdc)
#self.Vtrms = Vtrms_calc(self.vta,self.vtb,self.vtc)
			#self.Vrms = Vrms_calc(self.va,self.vb,self.vc)
			#self.Vrms_min = Vrms_min_calc(self.va,self.vb,self.vc)
			#self.Irms = Irms_calc(self.ia,self.ib,self.ic)

#self.Vtabrms = Vtabrms_calc(self.vta,self.vtb)
				#self.Vabrms = Vabrms_calc(self.va,self.vb)
				
#self.S = S_calc(self.vta,self.vtb,self.vtc,self.ia,self.ib,self.ic)
			#self.S_PCC = S_PCC_calc(self.va,self.vb,self.vc,self.ia,self.ib,self.ic)

    #self.iaload1 = self.iphload1_calc(self.va)
				#self.ibload1 = self.iphload1_calc(self.vb)
				#self.icload1 = self.iphload1_calc(self.vc)
				#self.S_G = self.S_G_calc()
				#self.S_load1 = self.S_load1_calc()

#self.ia_ref = self.ia_ref_calc()
			#self.ib_ref = self.ib_ref_calc()
			#self.ic_ref = self.ic_ref_calc()
        
#self.we = self.we_calc() #Calculate inverter frequency from PLL equation

"""
@numba.njit(debug=debug_flag,cache=cache_flag)
def ma_calc(Kp_GCC,ua,xa): #Average duty cycle - Phase A
	#Phase A duty cycle.
	#Returns:
		complex: Duty cycle.
	
	return Kp_GCC*ua + xa #PI controller equation
	#return utility_functions.m_calc(Kp_GCC,ua,xa)

@numba.njit(debug=debug_flag,cache=cache_flag)
def mb_calc(Kp_GCC,ub,xb): #Average duty cycle - Phase B
	#Phase B duty cycle.
	#Returns:
	#	complex: Duty cycle.
	
	return Kp_GCC*ub + xb #PI controller equation

@numba.njit(debug=debug_flag,cache=cache_flag)
def mc_calc(Kp_GCC,uc,xc): #Average duty cycle - Phase C
	#Phase C duty cycle.
	#Returns:
	#	complex: Duty cycle.
	
	return Kp_GCC*uc + xc #PI controller equation	

@numba.njit(debug=debug_flag,cache=cache_flag)
def vta_calc(ma,Vdc):
	#Inverter terminal voltage -  Phase A
	return ma*(Vdc/2)

@numba.njit(debug=debug_flag,cache=cache_flag)
def vtb_calc(mb,Vdc):
	#Inverter terminal voltage -  Phase B
	return mb*(Vdc/2)

@numba.njit(debug=debug_flag,cache=cache_flag)
def vtc_calc(mc,Vdc):
	#Inverter terminal voltage -  Phase C
	return mc*(Vdc/2)

@numba.njit(cache=cache_flag)
def S_calc(vta,vtb,vtc,ia,ib,ic): #Apparent power output at inverter terminal
	#Inverter apparent power output
	return (1/2)*(vta*ia.conjugate() + vtb*ib.conjugate() + vtc*ic.conjugate())
	#return utility_functions_numba.S_calc(vta,vtb,vtc,ia,ib,ic)

#Apparent power output at PCC - LV side
@numba.njit(cache=cache_flag)
def S_PCC_calc(va,vb,vc,ia,ib,ic):
	Power output at PCC LV side
	return (1/2)*(va*ia.conjugate() + vb*ib.conjugate() + vc*ic.conjugate())
	#return utility_functions_numba.S_calc(.va,.vb,.vc,.ia,.ib,.ic)

@numba.njit(cache=cache_flag)
def Vtrms_calc(vta,vtb,vtc):
	#Inverter terminal voltage -	RMS
	return utility_functions_numba.Urms_calc(vta,vtb,vtc)

@numba.njit(cache=cache_flag)
def Vrms_calc(va,vb,vc):
	#PCC LV side voltage - RMS
	return utility_functions_numba.Urms_calc(va,vb,vc)

@numba.njit(cache=cache_flag)
def Vrms_min_calc(va,vb,vc):
	#PCC LV side voltage - RMS
	
	return utility_functions_numba.Urms_min_calc(va,vb,vc)

@numba.njit(cache=cache_flag)		
def Irms_calc(ia,ib,ic):
	#nverter current - RMS
	return utility_functions_numba.Urms_calc(ia,ib,ic)

@numba.njit(cache=cache_flag)
def Vtabrms_calc(vta,vtb):
	#Inverter terminal voltage - line to line	RMS
		
	return abs(vta-vtb)/math.sqrt(2)

@numba.njit(cache=cache_flag)	
def Vabrms_calc(va,vb):
	#PCC LV side voltage - line to line	RMS
	return abs(va-vb)/math.sqrt(2)
"""