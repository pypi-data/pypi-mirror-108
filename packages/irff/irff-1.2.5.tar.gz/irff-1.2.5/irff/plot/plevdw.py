#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
from os import system, getcwd, chdir,listdir
from os.path import isfile # exists
from irff.irff_np import IRFF_NP
from irff.AtomDance import AtomDance
from irff.plot.deb_bde import deb_bo
import argh
import argparse
import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from ase.io.trajectory import Trajectory
from ase.io import read
import json as js


r      = 0.5
images = []

while r<1.9:
      r += 0.01
      atoms = Atoms('H2',
                    positions=[(0, 0, 0), (r, 0, 0)],
                    cell=[10.0, 10.0, 10.0],
                    pbc=[1, 1, 1])
      images.append(atoms)

# deb_bo(images,i=0,j=1)

def taper(r,vdwcut=10.0):
    tp = 1.0+np.divide(-35.0,np.power(vdwcut,4.0))*np.power(r,4.0)+ \
         np.divide(84.0,np.power(vdwcut,5.0))*np.power(r,5.0)+ \
         np.divide(-70.0,np.power(vdwcut,6.0))*np.power(r,6.0)+ \
         np.divide(20.0,np.power(vdwcut,7.0))*np.power(r,7.0)
    return tp


def vdw(r,ffield='ffield.json',bd='C-C',ai='H',aj='H',
         gamma=1.0,gammaw=1.0,vdw1=1.0,rvdw=2.0):
    atomi,atomj = bd

    gm3  = np.power(1.0/gamma,3.0)
    r3   = np.power(r,3.0)
    
    rr   = np.power(r,vdw1) + np.power(1.0/gammaw,vdw1)
    f13  = np.power(rr,1.0/vdw1)

    tpv  = taper(r)

    expvdw1 = np.exp(0.5*alfa*(1.0-np.divide(f13,2.0*rvdw)))
    expvdw2 = np.square(expvdw1)
    evdw    = tpv*Devdw*(expvdw2-2.0*expvdw1)
    return evdw


with open('ffield.json','r') as lf:
     j = js.load(lf)
     p = j['p']

gammaw   = np.sqrt(p['gammaw_'+atomi]*p['gammaw_'+atomj])
r = np.linspace(0.4,8.0,100)

ev = vdw(r)

plt.figure(figsize=figsize)     
plt.plot(bopsi,alpha=0.8,linewidth=2,linestyle=':',color='k',label=r'$BO_p^{\sigma}$')
plt.plot(boppi,alpha=0.8,linewidth=2,linestyle='-.',color='k',label=r'$BO_p^{\pi}$')
plt.plot(boppp,alpha=0.8,linewidth=2,linestyle='--',color='k',label=r'$BO_p^{\pi\pi}$')
plt.plot(bo0,alpha=0.8,linewidth=2,linestyle='-',color='g',label=r'$BO^{t=0}$')
plt.plot(bo1,alpha=0.8,linewidth=2,linestyle='-',color='y',label=r'$BO^{t=1}$')
plt.plot(eb,alpha=0.8,linewidth=2,linestyle='-',color='r',label=r'$E_{bond}$ ($-E_{bond}/%4.2f$)' %-emin_)
plt.plot(esi,alpha=0.8,linewidth=2,linestyle='-',color='r',label=r'$E_{esi}$ ($E_{si}/%4.2f$)' %emx)
plt.legend(loc='best',edgecolor='yellowgreen')
plt.savefig('deb_bo.pdf')
if show: plt.show()
plt.close()
