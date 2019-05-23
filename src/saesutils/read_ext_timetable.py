#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:34:52 2019

@author: john.onwuemeka
"""
import numpy as np
from obspy.core import UTCDateTime

def read_ext_timetable(self):
    """
    Read arrival time from external timetale file and create a dict
    of the P and S arrival times.
    
    time table format --> eventID station timepick(UTC) phasename(P,S)
    
    Parameters:
    
    Returns/Modifications:
    
    """
    
    data = np.genfromtxt(self.maindir+'/input/tt.dat',skip_header = 1,dtype=['U24','U12','U32','U2'])
    evid_tt = [data[i][0] for i in range(len(data))]
    P_tt,S_tt = {},{}
    for i in range(len(data)):
        if data[i][3].upper() == 'P':
            P_tt[evid_tt[i]].append([UTCDateTime(data[i][2]),data[i][1]])
        elif data[i][3].upper() == 'S':
            S_tt[evid_tt[i]].append([UTCDateTime(data[i][2]),data[i][1]])
#    evid_tt = sorted(list(set(evid_tt)))
    self.P_tt = P_tt
    self.S_tt = S_tt
    return None
