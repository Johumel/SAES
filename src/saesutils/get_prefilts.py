#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:03:38 2019

@author: john.onwuemeka
"""
import numpy as np
import re

def get_prefilts(self):
    """
    Description:
    ------------
    Read the pre-defined response removal frequency range for each station.

    Parameters/Input:
    -----------------

    Returns/Modificatoins:
    -----------------------

    """
    prefilts = open(self.maindir+'/input/pre_filt.list').readlines()
    list1 = [list(filter(None, re.split('[: \n#]',prefilts[j])))[0] for j in range(len(prefilts)-1) if prefilts[j] != '\n']
    list2 = [list(filter(None, re.split('[: \n#]',prefilts[j])))[1] for j in range(len(prefilts)-1) if prefilts[j] != '\n']
    list1 = np.asarray(list1)
    list2 = np.asarray(list2)
    for i in range(len(list1)):
        try:
            prefilt = [float(j) for j in list2[i][1:-1].split(',')]
            if len(prefilt) == 4:
                self.stationlist[list1[i]]['pre_filt'] = prefilt
        except:
            prefilt = None
            pass
    return None
