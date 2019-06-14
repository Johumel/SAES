#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 09:08:46 2019

@author: john.onwuemeka
"""
import numpy as np
from ..optimizer import fit_sin_spec
from .save_output import *
from ..optimizer.srfit import *
from ..create_plots import *


#As the name goes, it begins the spectral analysis for spectra ratio
def begin_spec_analysis(self,specmain,freqmain,egffile,mainfile,wm,wmfc,wmn,
                        trtm,we,wefc,wen,trte,time_win,ccvals,wv,stfy,stfx):
    '''
    Function that pre-arranges the station spectral ratios and their 
    corresponding frequency bins to be of equal length. It discards spectral
    ratios whose lowest frequency bin is more than 70% of the single spectrum 
    corner frequency estimate for the given main event. Representative spectral
    ratio and station weighting for each event pair is computed and applied.
    It calls get_best_fit which returns optimum fitting parameters for the 
    representative spectral ratio. It call the spectral ratio and single 
    spectrum (if user requested both single spectrum calculations in addition 
    to spectral ratio) figure generation functions and sends results to the
    save_output function.
    
    Input:
    -------
    specmain   --> dict of station spectral ratios
    freqmain   --> dict of station spectral ratios frequency bins
    egffile    --> filename of egf event for one station
    mainfile   --> filename of main event for one station
    wm         --> dict of main events's station single spectrum
    wmfc       --> dict of imain events's  station single spectrum 
    frequency bins
    wmn        --> dict of main events's  station single spectrum noise
    trtm       --> dict of main event to stations first arrival travel time
    we         --> dict of egf events's  station single spectrum
    wefc       --> dict of egf events's  station single spectrum frequency bins
    wen        --> dict of egf events's  station single spectrum noise
    trte       --> dict of egf event to stations first arrival travel time
    time_win   --> time window length
    ccvals     --> station spectral ratio weighting factors
    wv         --> wave type
    stfy       --> source time function amplitudes (not yet activated)
    stfx       --> source time function time bins (not yet activated)
    
    Returns:
    ---------
    None
    
    '''
        
    if bool(specmain) == True and bool(freqmain) == True:
            lste = list(specmain.keys())
            fcmainlist = {}
            for i in lste:                
                popt,pcov = fit_sin_spec(wm[i],wmfc[i],i,min(wmfc[i]),max(wmfc[i])*0.5,trtm[i],'yes',self.source_model)
                fcmain = round(popt[1],1)
                fcmainlist[i] = fcmain
                if freqmain[i][0] > fcmain*0.7:
                    del specmain[i],freqmain[i],wmfc[i]
                    del wm[i],wmn[i],wefc[i],we[i],wen[i]
                    del trtm[i],trte[i],fcmainlist[i]
                    del egffile[i],mainfile[i],stfy[i],stfx[i],ccvals[i]
            mini_freq = []; mini_freq_bin = []; max_freq = []
            lste = list(specmain.keys())
            arre = list(range(len(lste)))
            arre_freq = list(range(len(lste)))
            rel_stf = list(range(len(lste)))
            for index in lste:
                freqmain[index] = np.asarray([float('%.2f' % i) for i in freqmain[index]])
                mini_freq.append(min(freqmain[index]))
                max_freq.append(max(freqmain[index]))
                mini_freq_bin.append(index)
            i = 0
            weight=[]
            if self.sumtype == 'weighted':
                sumccvals = [ccvals[key] for key in ccvals.keys()]
                weight=[ccvals[index]/sum(sumccvals) for index in lste]
            for index in lste:
                startpoint = np.where(freqmain[index] >= max(mini_freq))[0][0]
                endpoint = np.where(freqmain[index] >= min(max_freq))[0][0]
                arre[i] = specmain[index][slice(startpoint,endpoint)]
                arre_freq[i] = freqmain[index][slice(startpoint,endpoint)]
                i += 1
            if arre_freq:
                lengths = [len(i) for i in arre]
                maxlength = np.max(lengths)
                indes = np.where(lengths == maxlength)[0][0]
                for i in range(len(arre)):
                    lendiff =   maxlength - len(arre_freq[i])
                    if lendiff > 0:
                        arre[i] = np.pad(arre[i],(0,lendiff),'edge')
                        arre_freq[i] = np.pad(arre_freq[i],(0,lendiff),'edge')
                rel_stf = [stfy[index] for index in lste]
                if self.sumtype == 'weighted':
                    specratio = np.ma.average(arre,axis=0,weights=weight)
                    rel_stf = np.ma.average(rel_stf,axis=0,weights=weight)
                elif self.sumtype == 'mean':
                    specratio = np.average(arre,axis=0)
                    rel_stf = np.average(rel_stf,axis=0)
                else:
                    specratio = np.median(arre,axis=0)
                    rel_stf = np.median(rel_stf,axis=0)
                freqbin = arre_freq[indes]
                indexx = np.where(mini_freq == min(mini_freq))[0][0]
                indexx = mini_freq_bin[indexx]
                fcmax = fcmainlist[max(fcmainlist, key=lambda i: fcmainlist[i])]
                fcmin = fcmainlist[min(fcmainlist, key=lambda i: fcmainlist[i])]*0.1
                fig,ax_spec =  make_figures_spec(self,specmain,freqmain,wmfc,wm,wmn,wefc,we,wen,indexx,time_win,mainfile,egffile,wv)
                frqprtub,freqfinal,tplier,allresidua0,popt,pcov = get_best_fit(self,freqbin,specratio,fcmin,fcmax)
                ax_spec.loglog(freqbin,specratio, 'k--', label='data',linewidth = 2)
                if allresidua0:
                    ubm,lbm,ube,lbe = get_bounds(specratio)
                    if ube > lbe and min(allresidua0) <= .9:
                        normresidua = min(allresidua0)
                        maxy = max(max(specmain.values(),key=len))
                        specrat_fit_plot(self,freqbin,specratio, tplier, frqprtub,allresidua0,ax_spec,popt,maxy)
                        save_output(self,popt, pcov,normresidua,None,None,None,wv)
                save_fig(self,fig,'spec',0,wv)
#                stf_plot(self,stfx[lste[0]],rel_stf,wv)
    if self.method == 3 or bool(specmain) == False:
        make_figures_ind(self,wm,wmfc,wmn,trtm,wv)
    return None