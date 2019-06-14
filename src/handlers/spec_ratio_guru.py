#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 17:31:20 2019

@author: john.onwuemeka
"""

from ..analyzer import spec_calc
from ..analyzer.stf_compute import stf_compute
from .begin_spec_analysis import begin_spec_analysis
from obspy.core import read
import glob,os
import numpy as np


def spec_ratio_guru(self,j,wv):
    '''
    Spectra ratio computations starts here. 
    The spec_calc function is called from here to compute individual spectra
    and spectra ratios for each event pair for each station. The spectra are
    then passed onto another handler function that does teh rest of the job.
    
    Input:
    ------
    j    --> main event
    wv   --> wave type (P or S)
        
    Returns:
    ---------
    None
        
    '''

    if (j not in self.blacklist_evl and j in self.evdict.keys()) or (j in self.whitelist_evl and j in self.evdict.keys()):
        for k in self.evdict[j].keys():
            specmain = {}; freqmain = {}; wefc = {}; we = {}; wen = {}; trte = {}; 
            egffile = {};wmfc = {}; wm = {}; wmn = {};  mainfile = {};
            trtm = {}; ccvals={}; stfy = {}; stfx = {}
            stlst = [i[0] for i in self.evdict[j][k]]
            cclist = [i[1] for i in self.evdict[j][k]] 
            if wv == 'S':
                try:
                    evfold1 = self.maindir+'/data/'+j+'/*.*HN.*.SAC' #Event1 files
                    evfold2 = self.maindir+'/data/'+k+'/*.*HN.*.SAC' #Event2 files
                    time1, time2 = self.S_tt[j],self.S_tt[k]
                except:
                    pass
            elif wv == 'P':
                try:
                    evfold1 = self.maindir+'/data/'+j+'/*.*HZ.*.SAC' #Event1 files
                    evfold2 = self.maindir+'/data/'+k+'/*.*HZ.*.SAC' #Event2 files
                    time1, time2 = self.P_tt[j],self.P_tt[k]
                except:
                    pass        
            foldera1 = sorted(glob.glob(evfold1))
            foldera2 = sorted(glob.glob(evfold2))
            if j != k and k not in self.blacklist_evl: #Double check that both events are not the same
                print('%s with %s' % (j,k))          
                file1 = None; file2 = None
                for x in range(0,len(foldera2)):
                    mt = read(foldera2[x])
                    station = mt[0].stats.station.strip()
                    cmponent = mt[0].stats.channel.strip()
                    netsta = mt[0].stats.network.strip()+'.'+mt[0].stats.station.strip() 
                    for l in range(0,len(foldera1)):
                        mta = os.path.basename(foldera1[l])
                        if station in mta and cmponent in mta:
                            file1 = foldera1[l]
                            file2 = foldera2[x]
                            if ''.join(netsta.split('.')) in stlst:
                                indx = np.where(np.asarray(stlst) == ''.join(netsta.split('.')))[0][0]   
                                if self.sumtype.lower() == 'weighted':
                                    xcor = cclist[indx] 
                                else:
                                    xcor = 1.                                   
                                if file1 and file2:
                                    if self.evlist[j][1][3] > self.evlist[k][1][3]:
                                        self.mainev = j
                                        self.egfev = k
                                    else:
                                        self.mainev = k
                                        self.egfev = j
                                        file1,file2 = file2,file1
                                    if time1 and time2 and netsta  not in self.blacklist_stations and xcor:
                                        specratio,freqbin,rawefc,rawe,rawen,\
                                        rawmfc,rawm,rawmn,trav_time_main,trav_time_egf,time_win,st_main,st_egf = \
                                        spec_calc(self,file1,file2,wv)
                                        xx,yy = stf_compute(st_main,st_egf,self.num_tapers)
                                        if (np.isnan(specratio)).any() != True: 
                                             specmain[station] = specratio; freqmain[station] = freqbin
                                             egffile[station] = file2; mainfile[station] = file1 
                                             wefc[station] = rawefc; we[station]=rawe;wen[station]=rawen;
                                             wmfc[station] = rawmfc;wm[station]=rawm;wmn[station]=rawmn;
                                             trtm[station] = trav_time_main; 
                                             trte[station] = trav_time_egf; 
                                             ccvals[station] = xcor;
                                             stfy[station] = yy; stfx[station] = xx;

            if specmain:
                begin_spec_analysis(self,specmain,freqmain,egffile,mainfile,wm,
                                    wmfc,wmn,trtm,we,wefc,wen,trte,time_win,
                                    ccvals,wv,stfy,stfx)
    return None