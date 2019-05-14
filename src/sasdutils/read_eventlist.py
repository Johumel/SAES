#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:49:20 2019

@author: john.onwuemeka
"""
import numpy as np
from obspy.core import UTCDateTime

def read_eventlist(self):
    '''event list must be in this format
    year month day hour minute second lat lon depth magnitude eventID'''
    data = np.genfromtxt(self.maindir+'/input/events.dat',dtype='U16')
    if self.whitelist_evl and not self.blacklist_evl:
        evids = self.whitelist_evl
    elif self.whitelist_evl and self.blacklist_evl:
        evids = [i for i in self.whitelist_evl if i not in self.blacklist_evl]
    elif self.blacklist_evl and not self.whitelist_evl:
        
        evids = [str(int(data[i][10])) for i in range(len(data)) if str(int(data[i][10])) not in self.blacklist_evl]
    else:
        evids = [str(int(data[i][10])) for i in range(len(data))]
    allids = np.asarray([str(int(data[i][10])) for i in range(len(data))])
    times,metadata = [],[]
    for i in range(len(evids)):
        index = np.where(allids == evids[i])[0]
        if index.size > 0:
            index = index[0]
            times.append(UTCDateTime(int(data[index][0]),int(data[index][1]),int(data[index][2]),int(data[index][3]),
                                 int(data[index][4]),float(data[index][5])))
            metadata.append([float(data[index][6]),float(data[index][7]),float(data[index][8]),float(data[index][9])])
    for i,j,k in zip(evids,times,metadata):
        self.evlist[i] = []
        self.evlist[i].append(j)
        self.evlist[i].append(k)
    return None
