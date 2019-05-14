#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:03:26 2019

@author: john.onwuemeka
"""
import numpy as np
import re, warnings,os
from .read_eventlist import read_eventlist

def read_controlfile(self):
    
    paramfile = open(self.controlfilename).readlines()
    list1 = [list(filter(None, re.split('[: \n#]',paramfile[j])))[0] for j in range(len(paramfile))]
    list2 = [list(filter(None, re.split('[: \n#]',paramfile[j])))[1] for j in range(len(paramfile))]
#        list1 = np.asarray(list1)
    list1 = np.asarray([i.lower() for i in list1])
    list2 = np.asarray(list2)
    index = np.where(list1 == 'maindir' )[0]
    if index.tolist():
        self.maindir = list2[index[0]]
        if not os.path.isdir(self.maindir):
            raise AttributeError('%s does not exist' % self.maindir)
    index = np.where(list1 == 'method' )[0]
    if index.tolist():
        self.method = int(list2[index[0]])
        if self.method not in [1,2,3] :
            raise AttributeError('method must be 1, 2 or 3')
    index = np.where(list1 == 'wave_type')[0]

    if index.tolist():
        if list2[index[0]].upper() == 'P':
            self.wvtype1 = 'P'
        elif list2[index[0]].upper() == 'S':
            self.wvtype2 = 'S'
        elif list2[index[0]].upper() == 'BOTH':
            self.wvtype1 = 'P'
            self.wvtype2 = 'S'
        else:
            raise AttributeError('wvtype must be P, S, or both')
    index = np.where(list1 == 'remove_resp')[0]
    if index.tolist():
        self.remove_resp = list2[index[0]].upper()
        if self.remove_resp.upper() not in ['NO','YES'] :
            raise AttributeError('remove_instr_response must be yes or no')
    index = np.where(list1 == 'showfc2')[0]
    if index.tolist():
        self.showfc2 = list2[index[0]].upper()
        if self.showfc2.upper() not in ['NO','YES'] :
            raise AttributeError('showfc2 must be yes or no')
    index = np.where(list1 == 'freesurface_cor')[0]
    if index.tolist():
        self.freesurface_cor = list2[index[0]].upper()
        if self.freesurface_cor.upper() not in ['NO','YES']:
            raise AttributeError('freesurface_cor must be yes or no')
    index = np.where(list1 == 'freesurface_vs')[0]
    if index.tolist():
        self.freesurface_vs = list2[index[0]]
        if self.freesurface_vs is not None and not isinstance(self.freesurface_vs,float):
            raise AttributeError('freesurface_vs must be a float in km/s')
    index = np.where(list1 == 'freesurface_vp')[0]
    if index.tolist():
        self.freesurface_vp = list2[index[0]]
        if self.freesurface_vp is not None and not isinstance(self.freesurface_vp,float):
            raise AttributeError('freesurface_vp must be a float in km/s')
    index = np.where(list1 == 'sumtype')[0]
    if index.tolist():
        self.sumtype = list2[index[0]]
        if self.sumtype.lower() not in ['weighted', 'mean','median']:
            raise AttributeError('spectral ratio summation type (sumtype) must weighted,median or mean')
    index = np.where(list1 == 'blacklist_stations')[0]
    if index.tolist():
        if not isinstance(list2[index[0]][1:-1].split(','), list):
            raise AttributeError('Blacklist must be a list of strings.')
        self.blacklist_stations = [i.strip() for i in list2[index[0]][1:-1].split(',')]
    index = np.where(list1 == 'whitelist_events')[0]
    if index.tolist():
        if not isinstance(list2[index[0]][1:-1].split(','), list):
            raise AttributeError('Event must be a list of event IDs')
        self.whitelist_evl = [i.strip() for i in list2[index[0]][1:-1].split(',')]
    index = np.where(list1 == 'blacklist_events')[0]
    if index.tolist():
        if not isinstance(list2[index[0]][1:-1].split(','), list):
            raise AttributeError('Event must be a list of event IDs')
        self.blacklist_evl = [i.strip() for i in list2[index[0]][1:-1].split(',')]
    index = np.where(list1 == 'source_model')[0]
    if index.tolist():
        self.source_model = list2[index[0]]
        if self.source_model.lower() not in ['vb','fb','b']:
            warnings.warn('Source type must be vb, fb, or b. Defaulting to vb ...')
            self.source_model = 'vb'
    index = np.where(list1 == 'autofit_single_spec')[0]
    if index.tolist():
        self.autofit_single_spec = list2[index[0]]
        if self.autofit_single_spec.lower() not in ['yes','no']:
            warnings.warn('Autofitting single spectrum must be yes or no. Defaulting to yes ...')
            self.autofit_single_spec = 'yes'
    index = np.where(list1 == 'numworkers' )[0]
    if index.tolist():
        if  not isinstance(int(list2[index[0]]),int):
            raise AttributeError('Number of parallel workers must be an integer.')
        self.numworkers = int(list2[index[0]])
    index = np.where(list1 == 'snr_threshold' )[0]
    if index.tolist():
        try:
            if  isinstance(int(list2[index[0]]),int) or isinstance(int(list2[index[0]]),float):
                self.snrthres = int(list2[index[0]])
        except:
            raise AttributeError('SNR must be a float or integer.')
        pass
    index = np.where(list1 == 'num_tapers' )[0]
    if index.tolist():
        try:
            if  isinstance(int(list2[index[0]]),int) or isinstance(int(list2[index[0]]),float):
                self.num_tapers = int(list2[index[0]])
        except:
            raise AttributeError('No. of tapers must be a float or integer.')
        pass

    #self.evlist = self.read_eventlist()
    read_eventlist(self)
    return None