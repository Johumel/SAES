#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 17:31:14 2019

@author: john.onwuemeka; Ge Li
"""
from ..analyzer import spec_calc
from ..create_plots import *
from obspy.core import read
import glob,os

def sin_spec_guru(self,evid1,wv,dlist):
    '''
    Single spectra computations begins here. This function calls spec_calc to
    get the spectra of each station, then passes them on to make_figures_ind.
    It performs most of the quality checks and only passes spectrum that meet
    set conditions and thresholds (e.g. SNR threshold, minimum frequency range,
    etc).

    Input:
    ------
    evid1    --> individual events ID list
    wv       --> wave type (P or S)
    dlist    --> list of events to skip so as to avoid repetition as they would have been already solved for.

    Returns:
    ---------
    None
    '''

    ind_spec = {}; freq_ind_spec = {};  ind_trtm = {};
    indv_noise = {}; time_window = {};
    for j in range(0,len(evid1)):
        if  evid1[j] not in dlist and evid1[j] not in self.blacklist_evl:
            self.output_dir = self.maindir+'/output/'+evid1[j]+'/'
            if not os.path.exists(self.output_dir ):
                os.makedirs(self.output_dir )
            if wv == 'S':
                try:
                    evfold1 = self.maindir+'/data/'+str(evid1[j])+'/*.?HN.*.SAC' #Event1 files
                    time1 = self.S_tt[evid1[j]]
                except:
                    pass
            elif wv == 'P':
                try:
                    evfold1 = self.maindir+'/data/'+str(evid1[j])+'/*.*HZ.*.SAC' #Event1 files
                    time1 = self.P_tt[evid1[j]]
                except:
                    pass
            foldera2 = sorted(glob.glob(evfold1))
            self.mainev = evid1[j]
            for x in range(0,len(foldera2)):
                file1  = foldera2[x]
                mt = read(file1)
                station = mt[0].stats.station.strip()
                netsta = mt[0].stats.network.strip()+'.'+mt[0].stats.station.strip()
                if time1 and netsta  not in self.blacklist_stations:
                    _,_,_,_,_,rawmfc,rawm,rawmn,trt1,_,time_win,_,_ = spec_calc(self,file1,None,wv)
                    ind_spec[station] = rawm; freq_ind_spec[station] = rawmfc;
                    time_window[station] = time_win;indv_noise[station] = rawmn
                    ind_trtm[station] =  trt1;
            dlist.append(evid1[j])
            lste = list(ind_spec.keys())
            for i in lste:
                if ind_spec[i] is None:
                    del ind_spec[i],freq_ind_spec[i],indv_noise[i]
                    del ind_trtm[i],time_window[i]
            lste = list(ind_spec.keys())
            if lste:
                make_figures_ind(self,ind_spec,freq_ind_spec,indv_noise,ind_trtm,wv)
            if not os.listdir(self.output_dir):os.rmdir(self.output_dir)
#            try:
#                os.rmdir(self.output_dir)
#            except OSError:
#                pass
    return None
