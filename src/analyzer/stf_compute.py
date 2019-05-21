#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 02:53:55 2019
@author: john.onwuemeka
"""

import numpy as np
from obspy.signal.filter import lowpass
from mtspec import mt_deconvolve

# Read the data
def stf_compute(st_main,st_egf,num_tapers):

    nfftlen = max(1000,st_main[0].stats.npts)
    delta = st_main[0].stats.delta
    half_nyq = np.arange(0,nfftlen)
    x = half_nyq*delta
    time_bandwidth = (num_tapers+1)/2
    y = []
    for tr_main, tr_egf in zip(st_main,st_egf):
        pms = mt_deconvolve(tr_main.data, tr_egf.data, delta,
                          nfft=nfftlen,
                          time_bandwidth=time_bandwidth, number_of_tapers=num_tapers,
                          weights='adaptive', demean=True)
        
        stf_deconv = pms['deconvolved']
        first_half = stf_deconv[np.where((half_nyq >= 0) & (half_nyq <= nfftlen/2) )[0]]
        second_half = stf_deconv[np.where((half_nyq > nfftlen/2) & (half_nyq <= nfftlen+1))[0]]
        yx = np.concatenate((second_half,first_half))
        yx = lowpass(yx,4, 1./delta, corners=4, zerophase=True)
#        yx = [i+abs(min(yx)) for i in yx]
        yx = [i/max(yx) for i in yx]
        y.append(yx)
    y = np.median(y,axis=0)
    return x,y