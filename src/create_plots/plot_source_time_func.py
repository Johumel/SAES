#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 22:35:41 2019

@author: john.onwuemeka
"""

import numpy as np
import matplotlib.pyplot as plt
from obspy.core import read
from mtspec import mt_deconvolve
from obspy.signal.filter import lowpass


def plot_source_time_func(self,file1,file2,time_win):
    #adapted from mtspec manual (krischer, 2016)
    if self.wvtype == 'P':
        starttime1 = self.P_tt[self.mainev]
        starttime2 = self.P_tt[self.egfev]
    elif self.wvtype == 'S':
        starttime1 = self.S_tt[self.mainev]
        starttime2 = self.S_tt[self.egfev]
    st1 = read(file1)
    st2 = read(file2)
    delt = st1[0].stats.delta
    channel = st1[0].stats.channel
    chalist = [channel[0:2]+i for i in ('Z','N','E')]
    RSTF = {}
    for i in chalist:
        try:
            st1 = read(file1.replace(chalist[0],i),starttime=starttime1,endtime=starttime1+time_win)
            st2 = read(file2.replace(chalist[0],i),starttime=starttime2,endtime=starttime2+time_win)
            st_mtd = mt_deconvolve(st1[0].data, st2[0].data, delt,nfft=len(st1[0].data),
                      time_bandwidth=4, number_of_tapers=7,weights='constant',
                      demean=True)
        except OSError:
            pass
        st_dec = st_mtd['deconvolved']
#        freq_dec = st_mtd['frequencies']
        xlen = len(st_dec)
        time = np.linspace(0, xlen*delt,xlen)
        l1 = np.arange(0, xlen)
        index1 = np.where((l1 >= 0,l1 <= xlen / 2))[0]
        sla = st_dec[index1]
#        sla_freq = freq_dec[index1[:-1]]
        index2 = np.where((l1 > xlen / 2) & (l1 <= xlen + 1))[0]
        slb = st_dec[index2]
#        slb_freq = freq_dec[index2[:-1]]
        slba = np.concatenate((sla, slb))
#        slba_freq = np.concatenate((sla_freq, slb_freq))
#        index3 = np.where(slba == max(slba))[0]
#        freqmin = 2*slba_freq[index3[:-1]]
        slba = lowpass(slba, 5, st1[0].stats.sampling_rate, corners=4, zerophase=True)
        slba /= slba.max()
        RSTF[i] = []
        RSTF[i] = slba
    RSTF = sum(RSTF.values())
    RSTF /= RSTF.max() 
    return time,RSTF
#    fig.save(self.output_dir+'/'+evname1+'_STF.pdf',dpi=200)
