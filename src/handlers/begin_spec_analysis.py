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
import datetime


#As the name goes, it begins the spectral analysis for spectra ratio
def begin_spec_analysis(self,specmain,freqmain,egffile,mainfile,wm,wmfc,wmn,trtm,we,wefc,wen,trte,time_win,ccvals,wv):
    if bool(specmain) == True and bool(freqmain) == True:
            lste = list(specmain.keys())

            #Ok! I am a bit confused here
            # But I tried to make sure all spectral ratios have the same frequency range
            indexes = [(key, len(specmain[key])) for key in specmain.keys()]
            indexes.sort(key=lambda x: x[1])
            fcmainlist = {}
            startt = datetime.datetime.now()
            for i in lste:                
                popt,pcov = fit_sin_spec(wm[i],wmfc[i],i,min(wmfc[i]),max(wmfc[i])*0.5,trtm[i],'yes',self.source_model)
                fcmain = round(popt[1],1)
                fcmainlist[i] = fcmain
                if freqmain[i][0] > fcmain*0.7:
                    del specmain[i],freqmain[i],wmfc[i]
                    del wm[i],wmn[i],wefc[i],we[i],wen[i]
                    del trtm[i],trte[i],fcmainlist[i]
                    del egffile[i],mainfile[i]
            endt = datetime.datetime.now()
            print('fitsinspec Run time = {}'.format(endt-startt))
            indexes = [(key, len(specmain[key])) for key in specmain.keys()]
            indexes.sort(key=lambda x: x[1])
            mini_freq = []; mini_freq_bin = []; max_freq = []
            lste = list(specmain.keys())
            arre = list(range(len(lste)))
            arre_freq = list(range(len(lste)))
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
                #Just in case the length of the spectral ratios are not the same
                #this will take care of it
                lengths = [len(i) for i in arre]
                maxlength = np.max(lengths)
                indes = np.where(lengths == maxlength)[0][0]
                for i in range(len(arre)):
                    lendiff =   maxlength - len(arre_freq[i])
                    if lendiff > 0:
                        arre[i] = np.pad(arre[i],(0,lendiff),'edge')
                        arre_freq[i] = np.pad(arre_freq[i],(0,lendiff),'edge')

                if self.sumtype == 'weighted':
                    specratio = np.ma.average(arre,axis=0,weights=weight)
                elif self.sumtype == 'mean':
                    specratio = np.average(arre,axis=0)
                else:
                    specratio = np.median(arre,axis=0)
                freqbin = arre_freq[indes]
                indexx = np.where(mini_freq == min(mini_freq))[0][0]
                indexx = mini_freq_bin[indexx]
                fcmax = fcmainlist[max(fcmainlist, key=lambda i: fcmainlist[i])]
                fcmin = fcmainlist[min(fcmainlist, key=lambda i: fcmainlist[i])]*0.1
                fig,ax_spec =  make_figures_spec(self,specmain,freqmain,wmfc,wm,wmn,wefc,we,wen,indexx,time_win,mainfile,egffile,wv)
                startt = datetime.datetime.now()
                frqprtub,freqfinal,tplier,allresidua0,popt,pcov = get_best_fit(self,freqbin,specratio,fcmin,fcmax)
                endt = datetime.datetime.now()
                print('getbestfit Run time = {}'.format(endt-startt))
                ax_spec.loglog(freqbin,specratio, 'k--', label='data',linewidth = 2)
                if allresidua0:
                    ubm,lbm,ube,lbe = get_bounds(specratio)
                    if ube > lbe and min(allresidua0) <= .9:
                        normresidua = min(allresidua0)
                        maxy = max(max(specmain.values(),key=len))
                        specrat_fit_plot(self,freqbin,specratio, tplier, frqprtub,allresidua0,ax_spec,popt,maxy)
                        save_output(self,popt, pcov,normresidua, tplier,None,None,None,wv)
                save_fig(self,fig,'spec',0)

    if self.method == 3 or bool(specmain) == False:
        make_figures_ind(self,wm,wmfc,wmn,trtm,wv)
    return None
