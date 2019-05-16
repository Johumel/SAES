#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:20:52 2019

@author: john.onwuemeka
"""
from obspy.core import Stream
from .free_surface_correction import free_surface_correction

def remove_ir(self,st,baz,evid,output):
    trn2 = Stream()
    respf = self.stationxml
    try:
        trn2 = st.select(component='N')
    except:
        pass
    try:
        trn2 += st.select(component='E')
    except:
        pass
    pre_filt = self.stationlist[st[0].stats.station.strip()]['pre_filt']
    if pre_filt:
        for tr in st:
#            tr.plot()
            tr.remove_response(respf,pre_filt=pre_filt,output = output)
#            tr.plot()
    else:
        for tr in st:
            tr.remove_response(respf,output = output)
    if len(trn2) == 2:
        trn2.rotate('NE->RT',back_azimuth=baz)
        for tr in st:
            if tr.stats.channel.strip()[-1] == 'N':
                tr = trn2[0]
            elif tr.stats.channel.strip()[-1] == 'E':
                tr = trn2[1]
        if self.freesurface_cor is True:
            st = free_surface_correction(self,st,evid)
        trn2.rotate('RT->NE',back_azimuth=baz)
    return st
