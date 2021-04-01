#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 23:31:20 2019
@author: john.onwuemeka; Ge Li
"""
import numpy as np
from ..create_plots import *
from .analyze_spec import *
from .get_good_snr_freq_range import *
from ..saesutils.get_time_window import *
from obspy.core import read

def spec_calc(self,file1,file2,wv):
    '''
    Handles spectra (including spectral ratios) computation and SNR analysis

    Inputs:
    ---------
    file1: filename of event 1
    file2: filename of event 2 (if analysing spectral ratios)
    wv: wave type (P or S)

    Returns:
    ---------
    specratio: spectral ratio (if analysing spectral ratios)
    freqsignalm: spectral ratio frequency bins (if analysing spectral ratios)
    rawefc: Uncorrected (instrument response corrected not applied) event 2 frequency bins (if analysing spectral ratios)
    rawe:   Uncorrected (instrument response corrected not applied) event 2 signal spectrum (if analysing spectral ratios)
    rawen:  Uncorrected (instrument response corrected not applied) event 2 noise spectrum (if analysing spectral ratios)
    rawmfc: Uncorrected (instrument response corrected not applied) event 1 frequency bins
    rawm:   Uncorrected (instrument response corrected not applied) event 1 signal spectrum
    rawmn:  Uncorrected (instrument response corrected not applied) event 1 noise spectrum
    trt1:   Source-to-station travel time of event 1
    trt2:   Source-to-station travel time of event 2 (if analysing spectral ratios)
    time_win: Time window length (sec)
    sts1:   Instrument response corrected event 1 signal spectrum
    sts2:   Instrument response corrected event 2 signal spectrum (if analysing spectral ratios)
    '''

    ev1 = self.mainev
    ev2 = self.egfev
    if not self.fixed_window:
        if ev1 and ev2:
            t1 = get_time_window(self.evlist[ev1][1][3])
            t2 = get_time_window(self.evlist[ev2][1][3])
            time_win = max(t1,t2)
        else:
            time_win = get_time_window(self.evlist[ev1][1][3])
    else:
        time_win = self.fixed_window
    specratio = []; rawefc = []; rawe = []; rawen = []; rawmfc = []; rawm = [];
    rawmn = []; trt1 = None; trt2 = None; sts1 = []; sts2 = []
    if (read(file1)[0].stats.channel != read(file2)[0].stats.channel and self.method in [2,3]) or self.method == 1 or self.remove_resp.lower() == 'yes':
        snr1, freqsignal1, signal1,noise1,snr_no_resp1,freq_no_resp1,signal_no_resp1,noise_no_resp1,\
        trt1,sts1 = analyze_spec(self,file1,ev1,'main',time_win,True,wv)
    elif read(file1)[0].stats.channel == read(file2)[0].stats.channel and self.method in [2,3]:
        snr1, freqsignal1, signal1,noise1,snr_no_resp1,freq_no_resp1,signal_no_resp1,noise_no_resp1,\
        trt1,sts1 = analyze_spec(self,file1,ev1,'main',time_win,False,wv)
    rawm = signal_no_resp1; rawmfc = freq_no_resp1; rawmn = noise_no_resp1
    if file2 and len(sts1) != 0:
        if read(file1)[0].stats.channel != read(file2)[0].stats.channel or self.remove_resp.lower() == 'yes':
            snr2, freqsignal2, signal2,noise2,snr_no_resp2,freq_no_resp2,signal_no_resp2,\
            noise_no_resp2,trt2,sts2 = analyze_spec(self,file2,ev2,'egf',time_win,True,wv)
        else:
            snr2, freqsignal2, signal2,noise2,snr_no_resp2,freq_no_resp2,signal_no_resp2,\
            noise_no_resp2,trt2,sts2 = analyze_spec(self,file2,ev2,'egf',time_win,False,wv)
        rawe = signal_no_resp2; rawefc = freq_no_resp2; rawen = noise_no_resp2
        if signal1.any() and signal2.any():
            signalm,signale,freqsignalm,freqsignale,_,_ = get_good_snr_freq_range(self.snrthres,signal1,signal2,snr1,snr2,freqsignal1,
                                freqsignal2,noise1,noise2)
            specratio = np.divide(signalm,signale,dtype=float)
    if self.method in [1,3] and len(sts2) == 0:
        rawm,_,rawmfc,_,rawmn,_ = get_good_snr_freq_range(self.snrthres,signal_no_resp1,
                                       None,snr_no_resp1,None,freq_no_resp1,
                                       None,noise_no_resp1,None)
    if len(specratio) == 0 or self.method == 1:
        specratio = float('Nan'); freqsignalm = None;
    return specratio, freqsignalm,rawefc,rawe,rawen,rawmfc,rawm,rawmn,trt1,trt2,time_win,sts1,sts2
