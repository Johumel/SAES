#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:37:53 2019

@author: john.onwuemeka
"""
from obspy.core import read
from .get_sig_nois_data import *
from .get_spectrum import *
from .remove_ir import *
from obspy.clients.iris import Client
import warnings
from pyproj import Geod
gref = Geod(ellps='WGS84')

def analyze_spec(self,fname,evid,evtype,time_win,rmv_instr_resp,wv):
    st = read(fname)
    Ptime,Stime = None,None
    if self.S_tt[evid]:
        for i in self.S_tt[evid]:
            if i[1] == st[0].stats.station.strip():
                Stime = i[0]
    if self.P_tt[evid]:
        for i in self.P_tt[evid]:
            if i[1] == st[0].stats.station.strip():
                Ptime = i[0]

#    Ptime,Stime = self.P_tt[evid],self.S_tt[evid]
    origtime = self.evlist[evid][0]
    late = self.evlist[evid][1][0]
    lone = self.evlist[evid][1][1]
#    depthe = self.evlist[evid][1][2]
#    magnitude = self.evlist[evid][1][3]
    lats = self.stationlist[st[0].stats.station.strip()]['lat']
    lons = self.stationlist[st[0].stats.station.strip()]['lon']
#    baz = Client().distaz(lats,lons,late,lone)['backazimuth']
    _,baz,dist = gref.inv(lone,late,lons,lats,radians=False)
    self.baz[evtype] = baz
    if baz < 0:
        baz = baz + 360
    if wv.upper() == 'S' and Stime:

        trt = Stime - origtime
#        nsstart = 10. fname,origtime,Atime,Btime,time_win,wv_fig,phase
        sts1,nss1,nsstart = get_sig_nois_data(fname,None,Ptime,Stime,time_win,False,'S')
        sts1.detrend(type='demean')
        sts1.detrend(type='linear')
        sts1.taper(max_percentage=0.05)
        nss1.detrend(type='demean')
        nss1.detrend(type='linear')
        nss1.taper(max_percentage=0.05)
        sts2 = sts1.copy()
        nss2 = nss1.copy()
        if self.method in [2,3] and sts1[0].stats.channel[1:3] in ['NN','NE','NZ'] and rmv_instr_resp is False:
            sts1.integrate().integrate()
            nss1.integrate().integrate()
            sts2,nss2 = remove_ir(self,sts2,nss2,baz,evid,'DISP')
        elif self.method in [2,3] and sts1[0].stats.channel[1:3] in ['HN','HE','HZ'] and rmv_instr_resp is False:
            sts1.integrate()
            nss1.integrate()
            sts2,nss2 = remove_ir(self,sts2,nss2,baz,evid,'DISP')
        elif rmv_instr_resp is True: 
            sts1,nss1 = remove_ir(self,sts1,nss1,baz,evid,'DISP')
            sts2,nss2 = remove_ir(self,sts2,nss2,baz,evid,'DISP')
        else:
            sts2,nss2,sts1,nss1 = None,None,None,None
#        if Ptime:
#            stn,_,_ = get_sig_nois_data(fname,origtime,Ptime,Stime,time_win,True,None)
#        else:
#            stn,_,_ = get_sig_nois_data(fname,origtime,None,Stime,time_win,True,None)
    if wv.upper() == 'P' and Ptime:
        trt = Ptime - origtime
        sts1,nss1,nsstart = get_sig_nois_data(fname,None,Ptime,None,time_win,False,'P')
        sts1.detrend(type='demean')
        sts1.detrend(type='linear')
        sts1.taper(max_percentage=0.05)
        nss1.detrend(type='demean')
        nss1.detrend(type='linear')
        nss1.taper(max_percentage=0.05)
        sts2 = sts1.copy()
        nss2 = nss1.copy()
        if self.method in [2,3] and sts1[0].stats.channel[1:3] in ['NN','NE','NZ'] and rmv_instr_resp is False:
            sts1.integrate().integrate()
            nss1.integrate().integrate()
            sts2,nss2 = remove_ir(self,sts2,nss2,baz,evid,'DISP')
        elif self.method in [2,3] and sts1[0].stats.channel[1:3] in ['HN','HE','HZ'] and rmv_instr_resp is False:
            sts1.integrate()
            nss1.integrate()
            sts2,nss2 = remove_ir(self,sts2,nss2,baz,evid,'DISP')
        elif rmv_instr_resp is True: 
            sts1,nss1 = remove_ir(self,sts1,nss1,baz,evid,'DISP')
            sts2,nss2 = remove_ir(self,sts2,nss2,baz,evid,'DISP')
        else:
            sts2,nss2,sts1,nss1 = None,None,None,None
#        stp,nsp = remove_ir(self,stp,nsp,baz,evid,'DISP')
#        if not Stime:
#            stn,_,_ = get_sig_nois_data(fname,origtime,Ptime,None,time_win,True,None)
#        if Stime:
#            stn,_,_ = get_sig_nois_data(fname,origtime,Ptime,Stime,time_win,True,None)
#        nstart = Ptime - stn[0].stats.starttime - (time_win+1)
#    stn = self.remove_ir(st,None,baz,evid,'VEL')
#    create_plots.plot_waveform(stn,nsstart,Ptime,Stime,time_win,evtype,self.ax)
#    snr, freqsignal, signal,noise,snr_no_resp,freq_no_resp,signal_no_resp,noise_no_resp
    
    snr, freqsignal, signal,noise,snr_no_resp,freq_no_resp,signal_no_resp,noise_no_resp = get_spectrum(self,sts1,nss1,sts2,nss2)
#    if self.remove_resp.lower() == 'yes':
#        snr_no_resp = copy.deepcopy(snr); freq_no_resp = copy.deepcopy(freqsignal)
#        signal_no_resp = copy.deepcopy(signal); noise_no_resp = copy.deepcopy(noise)
#    print(signal_no_resp)
    return snr, freqsignal, signal,noise,snr_no_resp,freq_no_resp,signal_no_resp,noise_no_resp,trt
