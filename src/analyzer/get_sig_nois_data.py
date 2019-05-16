#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:39:20 2019

@author: john.onwuemeka
"""
from obspy.core import read
from .remove_ir import remove_ir
import warnings

def get_sig_nois_data(self,fname,origtime,Atime,Btime,time_win,wv_fig,phase,evid,baz,rmv_instr_resp):
    st = read(fname)
    if Atime:
        Atime = Atime - max(0.05,st[0].stats.delta)  
    if Btime:
        Btime = Btime - max(0.05,st[0].stats.delta)  
    comp1 = st[0].stats.channel.strip()
    if 'Z' in comp1:
        comp2,comp3 = comp1[0:2]+'E',comp1[0:2]+'N'
    elif 'E' in comp1:
        comp2,comp3 = comp1[0:2]+'N',comp1[0:2]+'Z'
    elif 'N' in comp1:
        comp2,comp3 = comp1[0:2]+'E',comp1[0:2]+'Z' 
    try:
        st += read(fname.replace(comp1,comp2))
    except:
        warnings.warn('Could not read %s channel for %s' % \
                          (comp2,st[0].stats.station),UserWarning)
        pass
    try:
        st += read(fname.replace(comp1,comp3))
    except:
        warnings.warn('Could not read %s channel for %s' % \
                          (comp3,st[0].stats.station),UserWarning)
        pass
    st.detrend(type='linear')
    st.detrend(type='demean')
    st.taper(max_percentage=0.05)
    if wv_fig is not True:  
        sts = st.copy()       
        if self.method in [2,3] and st[0].stats.channel[1:3] in ['NN','NE','NZ'] and rmv_instr_resp is False:
            sts.integrate().integrate()
        elif self.method in [2,3] and st[0].stats.channel[1:3] in ['HN','HE','HZ'] and rmv_instr_resp is False:
            sts.integrate()
        st = remove_ir(self,st,baz,evid,'DISP')
        ns = st.copy()
        nss = sts.copy() 
        if phase == 'S':
            sts.trim(starttime = Btime, endtime = Btime + time_win)
            st.trim(starttime = Btime, endtime = Btime + time_win)
        elif phase == 'P':
            sts.trim(starttime = Atime, endtime = Atime + time_win)
            st.trim(starttime = Atime, endtime = Atime + time_win)
        if not Atime and phase == 'S':
            nss.trim(starttime = st[0].stats.starttime + 1. ,\
                        endtime = st[0].stats.starttime + 1.+time_win)
            ns.trim(starttime = st[0].stats.starttime + 1. ,\
                        endtime = st[0].stats.starttime + 1.+time_win)
            nsstart = st[0].stats.starttime + 1.
        elif Atime and phase == 'S':
            nss.trim(starttime = Atime - (time_win+1) ,\
                        endtime = Atime - 1) 
            ns.trim(starttime = Atime - (time_win+1) ,\
                        endtime = Atime - 1) 
            nsstart = Atime - (time_win+1)
        elif phase == 'P':
            nss.trim(starttime = Atime - (time_win+1) ,\
                        endtime = Atime - 1) 
            ns.trim(starttime = Atime - (time_win+1) ,\
                        endtime = Atime - 1) 
            nsstart = Atime - (time_win+1)
    elif wv_fig is True:
        sts = None
        nss = None
        ns = None
        st = remove_ir(self,st,baz,evid,'VEL')
        nsstart = None
        time_win_add = 5.0
        sts
        if Btime and not Atime:    
            st.trim(starttime = origtime,endtime = \
                       (Btime + time_win+time_win_add+.1))
            nsstart = sts[0].stats.starttime + 1.
        elif Atime and Btime:
            time_win_add = (Btime - Atime)*2
            st.trim(starttime = (Atime -(time_win+2)),endtime = (Btime + time_win+time_win_add+.1))
            nsstart = Atime - (time_win+1)
        elif  Atime and not Btime :
            st.trim(starttime = (Atime - (time_win+2)),endtime = (Atime + time_win+time_win_add+.1))
            nsstart = Atime - (time_win+1)
    return sts,nss,nsstart,st,ns
