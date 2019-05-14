#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:39:20 2019

@author: john.onwuemeka
"""
from obspy.core import read
import warnings

def get_sig_nois_data(fname,origtime,Atime,Btime,time_win,wv_fig,phase):
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
    nss = None
    if wv_fig is not True:
        if phase == 'S':
            sts = read(fname,starttime = Btime, endtime = Btime + time_win)
        elif phase == 'P':
            sts = read(fname,starttime = Atime, endtime = Atime + time_win)    
        if not Atime and phase == 'S':
            nss  = read(fname,starttime = st[0].stats.starttime + 1. ,\
                        endtime = st[0].stats.starttime + 1.+time_win)
            nsstart = st[0].stats.starttime + 1.
        elif Atime and phase == 'S':
            nss  = read(fname,starttime = Atime - (time_win+1) ,\
                        endtime = Atime - 1) 
            nsstart = Atime - (time_win+1)
        elif phase == 'P':
            nss  = read(fname,starttime = Atime - (time_win+1) ,\
                        endtime = Atime - 1) 
            nsstart = Atime - (time_win+1)
        try:
            if phase == 'S':
                sts += read(fname.replace(comp1,comp2),starttime = Btime, endtime = Btime + time_win)
            elif phase == 'P':
                sts += read(fname.replace(comp1,comp2),starttime = Atime, endtime = Atime + time_win)    
#            sts += read(fname.replace(comp1,comp2),starttime = Atime, \
#                        endtime = Atime + time_win)
            if not Atime and phase == 'S':
                nss  += read(fname.replace(comp1,comp2),starttime = \
                             st[0].stats.starttime + 1. ,endtime = \
                             st[0].stats.starttime + 1.+time_win)
            elif Atime and phase == 'S':
                nss  += read(fname.replace(comp1,comp2),starttime = \
                             Atime - (time_win+1) ,endtime = Atime - 1)
            elif phase == 'P':
                nss  += read(fname.replace(comp1,comp2),starttime = Atime - \
                            (time_win+1) ,endtime = Atime - 1) 
        except:
            warnings.warn('Could not read east channel for %s' % \
                          sts[0].stats.station,
                      UserWarning)
            pass
        try:
            if phase == 'S':
                sts += read(fname.replace(comp1,comp3),starttime = Btime, endtime = Btime + time_win)
            elif phase == 'P':
                sts += read(fname.replace(comp1,comp3),starttime = Atime, endtime = Atime + time_win)    
#            sts += read(fname.replace(comp1,comp2),starttime = Atime, \
#                        endtime = Atime + time_win)
            if not Atime and phase == 'S':
                nss  += read(fname.replace(comp1,comp3),starttime = \
                             st[0].stats.starttime + 1. ,endtime = \
                             st[0].stats.starttime + 1.+time_win)
            elif Atime and phase == 'S':
                nss  += read(fname.replace(comp1,comp3),starttime = \
                             Atime - (time_win+1) ,endtime = Atime - 1)
            elif phase == 'P':
                nss  += read(fname.replace(comp1,comp3),starttime = Atime - \
                            (time_win+1) ,endtime = Atime - 1) 
        except:
            warnings.warn('Could not read east channel for %s' % \
                          sts[0].stats.station,
                      UserWarning)
            pass
    elif wv_fig is True:
        nsstart = None
        time_win_add = 5.0
        if Btime and not Atime:    
            sts = read(fname,starttime = origtime,endtime = \
                       (Btime + time_win+time_win_add+.1))
            sts += read(fname.replace(comp1,comp2),starttime = \
                        origtime,endtime = (Btime + time_win+time_win_add+.1))
            sts += read(fname.replace(comp1,comp1),starttime = \
                        origtime,endtime = (Btime + time_win+time_win_add+.1))
            nsstart = sts[0].stats.starttime + 1.
        elif Atime and Btime:
            time_win_add = (Btime - Atime)*2
            sts = read(fname,starttime = (Atime -(time_win+2)),endtime = (Btime + time_win+time_win_add+.1))
            sts += read(fname.replace(comp1,comp2),starttime = (Atime - (time_win+2)),endtime = (Btime + time_win+time_win_add+.1))
            sts += read(fname.replace(comp1,comp3),starttime = (Atime - (time_win+2)),endtime = (Btime + time_win+time_win_add+.1))
            nsstart = Atime - (time_win+1)
        elif  Atime and not Btime :
            sts = read(fname,starttime = (Atime - (time_win+2)),endtime = (Atime + time_win+time_win_add+.1))
            sts += read(fname.replace(comp1,comp2),starttime = (Atime - (time_win+2)),endtime = (Atime + time_win+time_win_add+.1))
            sts += read(fname.replace(comp1,comp3),starttime = (Atime - (time_win+2)),endtime = (Atime + time_win+time_win_add+.1))
            nsstart = Atime - (time_win+1)
    return sts,nss,nsstart
