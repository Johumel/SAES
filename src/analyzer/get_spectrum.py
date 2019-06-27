#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:07:48 2019

@author: john.onwuemeka
"""
import numpy as np
from mtspec import mtspec

def get_spectrum(self,st1,ns1,st2,ns2):
 
    '''
    Take waveforms of signal and noise (pre-Pphase arrrival waveform) and 
    generates spectra using the multiptaper spectrum estimation method of
    Prieto et al., (2009) implemented in python by Krischer (2016). This function 
    would naturally calculate the sqrt of the sum of the power spectrum from all
    3 channels (E,N,& Z) if they are available otherwise it will estimate the spectrum with
    the number (1 or 2) of available channels

    Inputs:
    --------
    st1 and st2 --> signal waveforms of event1 and event2 respectively
    ns1 and ns2 --> noise waveforms of event1 and event2 respectively
    
    Returns:
    ---------
    snr            --> signal-to-noise ratio (SNR)
    freqsignal     --> frequency bins of spectra
    signal         --> signal spectrum
    noise          --> noise spectrum
    snr_no_resp    --> SNR of instrument response corrected signal
    freq_no_resp   --> frequency bins of instrument response corrected signal
    signal_no_resp --> spectrum of instrument response corrected signal waveform
    noise_no_resp  --> spectrum of instrument response corrected noise waveform
   
    '''
    
    numtapers,stationlist = self.num_tapers,self.stationlist
    pms = {}; fsds = {}; pmn ={}; fsdn = {}; fsd = {}; pms_no_ir = {}; pmn_no_ir = {};
    snr = None; freqsignal = None; signal = None; noise = None; 
    snr_no_resp = None; signal_no_resp = None; noise_no_resp = None; freq_no_resp = None
    i = 0
    fact = 1.0e9
    nfftlen = len(st2[0].data)+1#int(2**np.ceil(np.log2(len(st2[0].data))))
    if st2:
        st2.detrend('demean')
        st2.detrend('linear')
        ns2.detrend('demean')
        ns2.detrend('linear')
        for tr in st2:     
            time_bandwidth = (numtapers+1)/2
            pms_no_ir[i], fsd[i],jacknife,_,_ = mtspec(data=np.multiply(tr.data,fact,dtype=float), delta=tr.stats.delta,time_bandwidth=time_bandwidth, number_of_tapers=int(numtapers), nfft=nfftlen,statistics=True,quadratic=True)
            pmn_no_ir[i],_,jacknife,_,_ = mtspec(data=np.multiply(ns2[i].data,fact,dtype=float), delta=ns2[i].stats.delta,time_bandwidth=time_bandwidth, number_of_tapers=int(numtapers), nfft=nfftlen,statistics=True,quadratic=True)
            i+=1
#        for key in pms_no_ir.keys(): pms_no_ir[key] = np.divide(pms_no_ir[key],st2[0].stats.delta)
#        for key in pmn_no_ir.keys(): pmn_no_ir[key] = np.divide(pmn_no_ir[key],st2[0].stats.delta)
        #for key in pms_no_ir.keys(): pms_no_ir[key] = np.divide(pms_no_ir[key],st2[0].stats.delta)
        #for key in pmn_no_ir.keys(): pmn_no_ir[key] = np.divide(pmn_no_ir[key],st2[0].stats.delta)
        signal_no_resp = np.sqrt(sum(pms_no_ir.values()))
        noise_no_resp = np.sqrt(sum(pmn_no_ir.values()))
        snr_no_resp = np.divide(signal_no_resp,noise_no_resp,dtype='float64')
        freq_no_resp = fsd[0]
    if self.method == 1 or self.remove_resp == 'yes':
        fact = 1.0e9
    else:
        fact = 1.0
    nfftlen = len(st1[0].data)+1#int(2**np.ceil(np.log2(len(st1[0].data))))
    i = 0
    if st1:    
        st1.detrend('demean')
        st1.detrend('linear')
        ns1.detrend('demean')
        ns1.detrend('linear')
        for tr in st1:
            time_bandwidth = (numtapers+1)/2
            pms[i], fsds[i],jacknife,_,_ = mtspec(data=np.multiply(tr.data,fact,dtype=float), delta=tr.stats.delta,time_bandwidth=time_bandwidth, number_of_tapers=int(numtapers),nfft=nfftlen, statistics=True,quadratic=True)
            pmn[i],fsdn[i],jacknife,_,_ = mtspec(data=np.multiply(ns1[i].data,fact,dtype=float), delta=ns1[i].stats.delta,time_bandwidth=time_bandwidth, number_of_tapers=int(numtapers), nfft=nfftlen,statistics=True,quadratic=True)
            i += 1
#        for key in pms.keys(): pms[key] = np.multiply(pms[key],st1[0].stats.delta)
#        for key in pmn.keys(): pmn[key] = np.multiply(pmn[key],st1[0].stats.delta)
        #for key in pms_no_ir.keys(): pms_no_ir[key] = np.divide(pms_no_ir[key],st1[0].stats.delta)
        #for key in pmn_no_ir.keys(): pmn_no_ir[key] = np.divide(pmn_no_ir[key],st1[0].stats.delta)
        signal = np.sqrt(sum(pms.values()))           
        noise = np.sqrt(sum(pmn.values()))
        snr = np.divide(signal,noise,dtype='float64')
        freqsignal=fsds[0];
        fe1 = len(signal)
        fe2 = len(noise)    
        if fe1 < fe2:
            padlen = fe2-fe1
            signal = np.lib.pad(signal,(0,padlen),'edge')
        elif fe2 < fe1:
            padlen = fe1-fe2
            signal= np.lib.pad(signal,(0,padlen),'edge')
    pre_filt = stationlist[st1[0].stats.station.strip()]['pre_filt']
    if pre_filt:
        highend = np.where(freq_no_resp >= pre_filt[2] )[0][0]
        lowend = np.where(freq_no_resp >= pre_filt[1] )[0][0]
    else:       
        lowend = 0
        highend = np.where(freq_no_resp >= max(freq_no_resp)-5)[0][0]
        pass
    if lowend and highend:
        if st1:
            freqsignal = freqsignal[slice(lowend,highend)]; snr = snr[slice(lowend,highend)];signal = signal[slice(lowend,highend)]
            noise = noise[slice(lowend,highend)];
        if st2:
            freq_no_resp = freq_no_resp[slice(lowend,highend)]; snr_no_resp = snr_no_resp[slice(lowend,highend)]
            signal_no_resp = signal_no_resp[slice(lowend,highend)]; noise_no_resp = noise_no_resp[slice(lowend,highend)]
    return snr, freqsignal, signal,noise,snr_no_resp,freq_no_resp,signal_no_resp,noise_no_resp