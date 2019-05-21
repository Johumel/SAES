#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 23:31:20 2019
@author: john.onwuemeka
"""
import numpy as np
from ..create_plots import *
from .analyze_spec import *
from ..saesutils.get_time_window import *
from obspy.core import read

def spec_calc(self,file1,file2,wv):
    ev1 = self.mainev
    ev2 = self.egfev
    sts2 = None
    sts1 = None
    if ev1 and ev2:
        t1 = get_time_window(self.evlist[ev1][1][3])
        t2 = get_time_window(self.evlist[ev2][1][3])
        time_win = max(t1,t2)
    else:
        time_win = get_time_window(self.evlist[ev1][1][3])
    specratio = []; rawefc = []; rawe = []; rawen = []; rawmfc = []; rawm = [];
    rawmn = []; trt1 = None; trt2 = None;
    if (read(file1)[0].stats.channel != read(file2)[0].stats.channel and self.method in [2,3]) or self.method == 1 or self.remove_resp.lower() == 'yes':
        snr1, freqsignal1, signal1,noise1,snr_no_resp1,freq_no_resp1,signal_no_resp1,noise_no_resp1,\
        trt1,sts1 = analyze_spec(self,file1,ev1,'main',time_win,True,wv)
    elif read(file1)[0].stats.channel == read(file2)[0].stats.channel and self.method in [2,3]:
        snr1, freqsignal1, signal1,noise1,snr_no_resp1,freq_no_resp1,signal_no_resp1,noise_no_resp1,\
        trt1,sts1 = analyze_spec(self,file1,ev1,'main',time_win,False,wv)
    rawm = signal_no_resp1; rawmfc = freq_no_resp1; rawmn = noise_no_resp1
    signalm = np.asarray([])
    if file2:

        if read(file1)[0].stats.channel != read(file2)[0].stats.channel or self.remove_resp.lower() == 'yes':
            snr2, freqsignal2, signal2,noise2,snr_no_resp2,freq_no_resp2,signal_no_resp2,\
            noise_no_resp2,trt2,sts2 = analyze_spec(self,file2,ev2,'egf',time_win,True,wv)

        else:
            snr2, freqsignal2, signal2,noise2,snr_no_resp2,freq_no_resp2,signal_no_resp2,\
            noise_no_resp2,trt2,sts2 = analyze_spec(self,file2,ev2,'egf',time_win,False,wv)
        rawe = signal_no_resp2; rawefc = freq_no_resp2; rawen = noise_no_resp2
        signalm,signale,freqsignalm,freqsignale,_,_ = get_good_snr_freq_range(self.snrthres,signal1,signal2,snr1,snr2,freqsignal1,
                                freqsignal2,noise1,noise2)
        if signalm.any() and signale.any():
            specratio = np.divide(signalm,signale,dtype=float)
    if self.method in [1,3] and not signalm.any():
        rawm,_,rawmfc,_,rawmn,_ = get_good_snr_freq_range(self.snrthres,signal_no_resp1,
                                       None,snr_no_resp1,None,freq_no_resp1,
                                       None,noise_no_resp1,None)
    if len(specratio) == 0 or self.method == 1:
        specratio = float('Nan'); freqsignalm = None;
    return specratio, freqsignalm,rawefc,rawe,rawen,rawmfc,rawm,rawmn,trt1,trt2,time_win,sts1,sts2

def get_good_snr_freq_range(snrthres,signal1,signal2,snr1,snr2,freqsignal1,freqsignal2,noise1,noise2):
    datas = None; datae = None; fnm = None; fne = None;
    noisem = None; noisee = None; #snrm = None; snre = None
    quit_calc = 'N'
    try:
        try:
            spm_low = np.where(snr1 >= snrthres )[0][0]
        except:
            spm_low = 0
        try:
            half_up = snr1[slice(spm_low,len(snr1)-1)]
            spm_high = np.where(half_up < snrthres )[0][0] + spm_low
        except:
            spm_high = len(snr1) - 1
    except:
        quit_calc = 'Y'
        pass
    if signal2 is not None:
        try:
            spe_low = np.where(snr2 >= snrthres)[0][0]
        except:
            spe_low = 0
        try:
            half_up = snr2[slice(spe_low,len(snr2)-1)]
            spe_high = np.where(half_up < snrthres )[0][0] + spe_low
        except:
            spe_high = len(snr2) - 1
        low_end = max(spe_low,spm_low)
        high_end = min(spe_high,spm_high)
        fnm = freqsignal1[slice(low_end,high_end)] # change to sp later
        fne = freqsignal2[slice(low_end,high_end)]
        datas = signal1[slice(low_end,high_end)] # change to sp later
        datae = signal2[slice(low_end,high_end)]

        noisem = noise1[slice(low_end,high_end)]
        noisee = noise2[slice(low_end,high_end)]
    else:
        if quit_calc == 'N':
            fnm = freqsignal1[slice(spm_low,spm_high)] # change to sp later
            datas = signal1[slice(spm_low,spm_high)] # change to sp later
            noisem = noise1[slice(spm_low,spm_high)]
    return datas,datae,fnm,fne,noisem,noisee
