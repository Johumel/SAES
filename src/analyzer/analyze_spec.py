#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:37:53 2019

@author: john.onwuemeka
"""
from obspy.core import read
from .get_sig_nois_data import *
from .get_spectrum import *
from pyproj import Geod
gref = Geod(ellps='WGS84')

def analyze_spec(self,fname,evid,evtype,time_win,rmv_instr_resp,wv):
    st = read(fname)
    Ptime,Stime,sts1,sts2 = None,None,[],None
    snr, freqsignal, signal,noise,snr_no_resp,freq_no_resp,signal_no_resp,\
    noise_no_resp,trt = None,None,None,None,None,None,None,None,None
    if self.S_tt[evid]:
        for i in self.S_tt[evid]:
            if i[1] == st[0].stats.station.strip():
                Stime = i[0]
    if self.P_tt[evid]:
        for i in self.P_tt[evid]:
            if i[1] == st[0].stats.station.strip():
                Ptime = i[0]
    origtime = self.evlist[evid][0]
    late = self.evlist[evid][1][0]
    lone = self.evlist[evid][1][1]
    lats = self.stationlist[st[0].stats.station.strip()]['lat']
    lons = self.stationlist[st[0].stats.station.strip()]['lon']
    _,baz,dist = gref.inv(lone,late,lons,lats,radians=False)
    self.baz[evtype] = baz
    if baz < 0:
        baz = baz + 360
    if wv.upper() == 'S' and Stime:
        trt = Stime - origtime
        sts1,nss1,nsstart,sts2,nss2 = get_sig_nois_data(self,fname,None,Ptime,Stime,time_win,False,'S',evid,baz,rmv_instr_resp)
    if wv.upper() == 'P' and Ptime:
        trt = Ptime - origtime
        sts1,nss1,nsstart,sts2,nss2 = get_sig_nois_data(self,fname,None,Ptime,Stime,time_win,False,'P',evid,baz,rmv_instr_resp) 
    if len(sts1) != 0 or sts2:
        snr, freqsignal, signal,noise,snr_no_resp,freq_no_resp,signal_no_resp,noise_no_resp = get_spectrum(self,sts1,nss1,sts2,nss2)
    return snr, freqsignal, signal,noise,snr_no_resp,freq_no_resp,signal_no_resp,noise_no_resp,trt,sts1
