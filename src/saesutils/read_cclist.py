#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:30:07 2019

@author: john.onwuemeka
"""
import numpy as np

def read_cclist(self):
    evid1,evid2 = None,None
    data = np.genfromtxt(self.maindir+'/input/cclist.dat',skip_header=1,dtype=['U10','U24','U24','f8'])
    evid1 = [data[i][1] for i in range(len(data))]
    evid2 = [data[i][2] for i in range(len(data))]  
    sta_cc = [data[i][0] for i in range(len(data))] 
    cc_val = [data[i][3] for i in range(len(data))] 
    evdict = {}
    for i,j,k,l in zip(evid1,evid2,sta_cc,cc_val):
        if i not in evdict.keys():
            evdict[i] = {}
        if j not in evdict[i].keys():
            evdict[i][j] = []
        evdict[i][j].append([k,l])
    self.evdict = evdict
    return evid1 
