#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:34:52 2019

@author: john.onwuemeka
"""
import numpy as np 

def read_ext_timetable(self):
    data = np.genfromtxt(self.maindir+'/input/tt.dat',dtype=['U16','U16','f8','f8'])
    evid_tt = [data[i][0] for i in range(len(data))]
    P_tt,S_tt = {},{}
    for i in range(len(data)): P_tt[evid_tt[i]].append([data[i][2],data[i][1]])
    for i in range(len(data)): S_tt[evid_tt[i]].append([data[i][3],data[i][1]])
    evid_tt = sorted(list(set(evid_tt)))
    return P_tt,S_tt,evid_tt
