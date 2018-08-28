#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 15:29:01 2018

@author: wyzhou

Ryan J Toolin creates the first half of the code in Matlab @5/2/2018,
which is rewritten in Python by Weiyue Zhou @5/4/2018
The second half is written by Weiyue Zhou @

Activation Calculation of foils in CLASS Accelerator
Refer to SOP#4 CSP at ISN Weiyue Zhou

a(t) = N*xs(i)*phi*(1-e^-(lamb*t))
"""
import math
# (p,n) Reations: 0: 64Ni to 64Cu, 1: 54Cr to 54Mn, 2: 57Fe to 57Co, 3: 95Mo to 95Tc, 4: 55Mn to 55Fe
# (p,alpha) Reactions: 5: 61Ni to 58Co, 6: 64Ni to 61Co, 7: 57Fe to 54Mn, 8: 94Mo to 91Nb 
#                      9: 98Mo to 95Nb, 10: 100Mo to 97Nb
# Constants
Na = 6.02E23; # avogadro's # (g/mole)
pi = 3.1416

# Crossections
xsconv = 10**-24; # convert barns to cm^2
xs = [0.0331,0.0791,0.0455,5.99E-4,0.0761,5.87E-8,3.179E-7,1.19E-6,1.343E-5,2.952E-6,5.78E-4]; # cross section barns from JANIS
for i in range (len(xs)):
    xs[i] *= xsconv # cross section (cm^2)

# Sample
V = 5.89E-04 # irradiated volume of each sample (cm^3)
AW = [64,54,57,95,55,61,64,57,94,98,100] # rough atomic weight

# Atom Densities
rhom = [8.9,7.19,7.87,10.28,7.21,8.9,8.9,7.87,10.28,10.28,10.28] # rough mass density of pure element (g/cm^2)
abund = [0.0093,0.0236,0.0212,0.1587,1.0,0.0114,0.0093,0.0212,0.01587,0.2429,0.0974] # rough abundance of each isotope
N = [] # list contains atom densities of parent isotopes
for i in range(len(rhom)):
    N.append(rhom[i]*Na*abund[i]/AW[i]) # rough atom density (atoms/cm^3)
    
# Product Half-Lifes and Decay Constants [64Cu,54Mn,57Co,95Tc,55Fe,58Co,61Co,54Mn,91Nb,95Nb,97Nb]
thalf = [12.70*3600, 312.03*24*3600, 271.79*24*3600, 20*3600, 2.73*365*24*3600,\
         70.86*24*3600, 1.65*3600, 312.3*24*3600, 10.15*24*3600, 86.6*3600, 1.2*3600]

# half-life(s)
DC=[] # decay constants
for i in range (len(thalf)):
    DC.append(math.log(2)/thalf[i]) # decay constans

# Beam Characteristics
beamc = 400*10**-9 # beam current on target (A or C/s)
beame = beamc*6.25E18 # convert beam current to (electrons/s)
beamd = 0.25 # beam radius (cm)
xsbeam = pi*beamd**2 # beam crossectional area (cm^2)
phi = beame/xsbeam # beam density #/(cm^2*s)


# Process I: Activation by Ryan Toolin
# Atom activated
t = 8*3600; # run time (s)
AA = [] # # of atoms activated in a period of 8 hours
for i in range(len(N)):
    AA.append(V*N[i]*xs[i]*phi*(1-math.exp(-DC[i]*t))/DC[i]) # Atoms activated in #
AAA = [] # radioactivities 
for i in range(len(AA)):
    AAA.append(DC[i]*AA[i]*10**6/(3.7E10)) # Radioactivity in uCi at the end of 8 hours irradiation time

# Gamma Constants obtained from Oak Ridge National Laboratory (ORNL)
# Specific Gamma-Ray Dose Constants for Nuclides Important to Dosimetry and
# Radiological Assessment May 1982
Gamma_mSv = [3.514E-5, 1.381E-4, 4.087E-5, 2.089E-4, 0, 1.652E-4 ,\
             2.286E-5, 1.381E-4, 2.413E-4, 1.295E-4, 1.168E-4]; # Gamma Constants (mSv)/(MBq*hr)@1m away
Gamma = []
for i in range (len(Gamma_mSv)):
    Gamma.append(3.7*Gamma_mSv[i]*1E4) # Gamma Constants (mrem/(uCi*hr) @ 1cm away

# Initial dose rate immediately after irradiation @ 1cm away for 
DR_Ini = []
for i in range(len(AAA)):
    DR_Ini.append(AAA[i]*Gamma[i])    
    

# Process II: Radioactive Decay by Weiyue Zhou    
    
# Atomic ratio of each alloys 
SS316L = [0.113,0.181,0.647,0.014,0.020,0.113,0.113,0.647,0.014,0.014,0.014] # Ni,Cr, Fe, Mo, Mn, Ni, Ni, Fe, Mo, Mo, Mo
Hastelloy_N = [0.722,0.083,0.055,0.102,0.009,0.722,0.722,0.055,0.102,0.102,0.102] # Ni,Cr, Fe, Mo, Mn, Ni, Ni, Fe, Mo, Mo, Mo
Incoloy_800HT = [0.307,0.224,0.454,0,0,0.307,0.307,0.454,0,0,0] # Ni,Cr, Fe, Mo, Mn, Ni, Ni, Fe, Mo, Mo, Mo
Ni20Cr = [0.780,0.220,0,0,0,0.780,0.780,0,0,0,0] # Ni,Cr, Fe, Mo, Mn, Ni, Ni, Fe, Mo, Mo, Mo
Ni10Cr = [0.889,0.111,0,0,0,0.889,0.889,0,0,0,0] # Ni,Cr, Fe, Mo, Mn, Ni, Ni, Fe, Mo, Mo, Mo
Ni201 = [1,0,0,0,0,1,1,0,0,0,0] # Ni,Cr, Fe, Mo, Mn, Ni, Ni, Fe, Mo, Mo, Mo

Alloys = [SS316L, Hastelloy_N, Incoloy_800HT, Ni20Cr, Ni10Cr, Ni201] # A list of alloys
Alloys_names = ['SS316L', 'Hastelloy_N', 'Incoloy_800HT', 'Ni20Cr', 'Ni10Cr', 'Ni201'] # A list of alloy names

# Calculating initial radoacitivity of each alloy
for alloy in range(len(Alloys)):
    total_initial_radioactivities = 0
    for i in range(len(Alloys[alloy])):
        total_initial_radioactivities += Alloys[alloy][i]*AAA[i]
    print ('Total initial radioactivity of '+ Alloys_names[alloy]+' is ' + str(round (total_initial_radioactivities,4))+' uCi.')

print()

# Calculating initial dose rate of each alloy
for alloy in range(len(Alloys)):
    total_initial_dose_rate = 0
    for i in range(len(Alloys[alloy])):
        total_initial_dose_rate += Alloys[alloy][i]*DR_Ini[i]
#        print ('Initial dose rate of ' + str(i) + ' is '+ str(Alloys[alloy][i]*DR_Ini[i]))
    print ('Total initial dose rate of '+ Alloys_names[alloy]+' is ' + str(round(total_initial_dose_rate,4)) +' mrem/h @ 1cm distance.')        

# Decay Process

def Decay (eff_element,end_DR,DR_Ini,DC):
    """
    Function Decay takes the effective elements inside of a certain alloy,
    and the required dose rate to be lower than,
    and initial dose rates,
    and decay constants
    returns the time in days 
    """
    DR_Ini_alloy = []
    for i in range (len (DR_Ini)):
        DR_Ini_alloy.append(DR_Ini[i]* eff_element[i]) # for each alloy atomic concentration, 
                                        # calculate the initial dose rate
    DR = DR_Ini_alloy[:] # Dose Rate @ t = 0 decay time
    t=0 # t in [s]
    while True:
        for j in range(len(DR_Ini_alloy)):
            DR[j]=DR_Ini_alloy[j]*math.exp(-DC[j]*t) # update dose rates
        DC_Total = 0
        for i in range(len(DR)):
            DC_Total += DR[i] # calculate total dose rate at time t
        if DC_Total < end_DR: # criteria to stop iteration
            return t/3600/24 # return time in days
        else:
            t+=60 # increase time by 60s

## Output results for t to reach required dose rates:
#end_DR = float (input ('Please input the required dose rate in mR/h @ 1cm distance: '))
#print ('The required cooling time for SS316L is '+str (round(Decay(SS316L,end_DR,DR_Ini,DC),2))+' days')
#print ('The required cooling time for Hastelloy N is '+str (round(Decay(Hastelloy_N,end_DR,DR_Ini,DC),2))+' days')
#print ('The required cooling time for Incoloy 800HT is '+str (round(Decay(Incoloy_800HT,end_DR,DR_Ini,DC),2))+' days')
#print ('The required cooling time for Ni-20Cr is '+str (round(Decay(Ni20Cr,end_DR,DR_Ini,DC),2))+' days')
#print ('The required cooling time for Ni-10Cr is '+str (round(Decay(Ni10Cr,end_DR,DR_Ini,DC),2))+' days')
#print ('The required cooling time for Ni201 is '+str (round(Decay(Ni201,end_DR,DR_Ini,DC),2))+' days')

def simpleDecay (eff_element,T,ini,DC):
    """
    Function simple Decay is similar with funtion Decay but instead of returning the time required 
    to cool down to certain level, it returns the radioactivity after a T in days
    """
    T = T*24*3600
    Ini_alloy = []
    for i in range (len (ini)):
        Ini_alloy.append(ini[i]* eff_element[i]) # for each alloy atomic concentration, 
                                        # calculate the initial quantity
    End_alloy = [] # to store the end quantity after T
    for i in range(len(Ini_alloy)):
        End_alloy.append(Ini_alloy[i]*math.exp(-DC[i]*T)) # calcuate the end quantity
    End_total_quantity = 0.0
    for j in End_alloy:
        End_total_quantity += j
    return round (End_total_quantity, 4)
        
# Output results of radioactivity after a time entered:
while True:
    T = int (input('Please input the time in days: '))
    for i in range(len(Alloys)):
        print ('The radioactivity of ' + Alloys_names[i] + ' after ' + str(T) + ' days is ' + str(simpleDecay (Alloys[i],T,AAA,DC))+' uCi.' )
    print ()
    for i in range(len(Alloys)):
        print ('The dose rate of ' + Alloys_names[i] + ' after ' + str(T) + ' days is ' + str(simpleDecay (Alloys[i],T,DR_Ini,DC))+' mR/h @ 1cm distance.' )
