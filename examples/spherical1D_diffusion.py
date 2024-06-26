# -*- coding: utf-8 -*-
"""
Diffusion in 1D spherical coordinates.


"Initial sphere diffusing into an infinite medium"

Reference:
J. Crank (1975) "The Mathematics of Diffusion", 2nd Ed., 
Clarendon Press (Oxford), pages 29-30, Equation 3.8, Figure 3.1 


The code is based on Matlab FVTool example:

https://github.com/simulkade/FVTool/tree/master/Examples/External/Diffusion1DSpherical_Analytic-vs-FVTool-vs-Fipy

script:
    diffusion1Dspherical_FVTool.m
    
240309  **UNFINISHED PROGRAM. WORK IN PROGRESS.** Awaiting implementation of
        terms for SphericalGrid1D.
"""
import numpy as np
from numpy import pi
import pyfvtool as pf

## Define the domain and create a mesh structure
# Here we work in a 1D spherical coordinate system (r coordinate)
L = 10.0  # domain length
Nr = 2000 # number of cells
m = pf.SphericalGrid1D(Nr, L)

## Create the boundary condition structure
BC = pf.BoundaryConditions(m) # all 'no flux' boundary condition structure

## Cell variables
D = pf.CellVariable(m, 1.0)
alfa = pf.CellVariable(m, 1.0)

## Solution variable and define initial condition
c_init = 0.0
c_old = pf.CellVariable(m, c_init, BC)
r = c_old.domain.cellcenters.r
c_old.value[r<1.0] = 1.0   # TO DO: find a better syntax for this

# calculate volumes of FV cellslices
#  We use this for demonstrating mass conservation
cellA = m.facecenters.r[0:-1]
cellB = m.facecenters.r[1:]
cellvol = 4/3 * pi * (cellB**3 - cellA**3)
cellsum = np.sum(cellvol)

t = 0.0 # overall time
deltat = 0.0625/20 #  time step

# output total mass in the system
m_tot = np.sum(c_old.value * cellvol)
print(t,m_tot)

# loop for "time-stepping" the solution
# It outputs the spatial profile C(r) after
# 20, 80 and 320 time-steps
# This corresponds to t=0.0625, t=0.25 and t=1, respectively.
ti = 0
for s in [20,60,240]:
  for n in range(s):
      M_trans, RHS_trans = pf.transientTerm(c_old, deltat, alfa)
      Dave = pf.harmonicMean(D)
      Mdiff = pf.diffusionTerm(Dave)
      Mbc, RHSbc = pf.boundaryConditionsTerm(BC)
      M = M_trans-Mdiff+Mbc
      RHS = RHS_trans+RHSbc
      c = pf.solveMatrixPDE(m,M, RHS)
      t += deltat
      c_old.update_value(c)
  m_tot = np.sum(c.value * cellvol)
  print(n,t,m_tot)
  
  # TO DO: output result, compare to analytic solution?
  ##  See FVTool repo (there's some Python there)

