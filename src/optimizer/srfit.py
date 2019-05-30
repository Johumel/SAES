#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 22:03:22 2019

@author: john.onwuemeka
"""
import numpy as np
from scipy.optimize import curve_fit
from .specr_model import specr_model
from joblib import Parallel, delayed

def get_bounds(spectra):
    """
    Description:
    ------------
    Get bounds of fitting parameters

    Parameters/Input:
    -----------------
    spectral ():

    Returns/Modifications:
    ----------------------
    ubm (float),
    lbm (float),
    ube (float),
    lbm (float),

    """
    indx = np.where(spectra < spectra[0]*0.8)[0][0]
    boundregion = spectra[slice(0,indx)]
    lbm = max(boundregion)*0.9
    ubm = max(boundregion)*1.4
    lbe = min(spectra)*0.6
    ube = min(spectra)*1.2
    return ubm,lbm,ube,lbe


def bestfit(freqbin,specratio,multiplier,maxf,freq,freq_calc,freqzy,fcmin,fcmax,model):
    """
    Description:
    ------------
    Fit the spectra ratio


    Parameters/Input:
    -----------------
    freqbin ():
    specratio
    multiplier
    maxf
    freq
    freq_calc
    freqzy
    fcmin
    fcmax
    model

    Returns/Modifications:
    ----------------------
    normresidua (),
    popt (),
    pcov (),

    """
#    try:
    specratio = np.multiply(specratio,multiplier,dtype=float)
#        fcmin = fcmin*0.1
#        fcmax = fcmax*1.5
    upper_fn = fcmin*2
    ubm,lbm,ube,lbe = get_bounds(specratio)
    if model.upper() == 'B':
        n1,n2,n3,n4 = 2,1,2,1
    elif model.upper() == 'FB':
        n1,n2,n3,n4 = 4,2,4,2
    elif model.upper() == 'VB':
        n1,n2,n3,n4 = 2,1,3,2
    if freq_calc is True:
        popt, pcov = curve_fit(specr_model, freqbin,specratio ,method='trf',bounds=((fcmin,upper_fn,lbm,lbe,n1-0.01,n2-0.01),(fcmax,max(freqbin),ubm,ube,n3,n4)),loss='soft_l1',verbose=0,tr_solver='lsmr',maxfev=1000)
    else:
        if freqzy:
            popt, pcov = curve_fit(specr_model, freqbin,specratio ,method='trf',bounds=((freqzy*.95,upper_fn,lbm,lbe,n1-0.01,n2-0.01),(freqzy*1.05,50.,ubm,ube,n3,n4)),loss='soft_l1',verbose=0,tr_solver='lsmr',maxfev=1000)
        elif not freqzy:
            popt, pcov = curve_fit(specr_model, freqbin,specratio ,method='trf',bounds=((fcmin,upper_fn,lbm,lbe,n1-0.01,n2-0.01),(fcmax,50.,ubm,ube,n3,n4)),loss='soft_l1',verbose=0,tr_solver='lsmr',maxfev=10000)
    residua = np.power(np.subtract(specratio,specr_model(freqbin, *popt)),2)
    normresidua = np.sqrt(np.sum(residua)/np.sum(np.power(specratio,2)))
#        vc = max(specr_model(freqbin, *popt))
#    except:
#        normresidua = -1; popt = [];  pcov = []
    return normresidua,popt,pcov

#this section gets the best model fit for the data
def get_best_fit(self,freqbin,specratio,fcmin,fcmax):

#    try:
    allresidua = []; allmultiplier = [];
    allmultiplier = np.arange(0.1,2.0,0.1) #this is just used to scale the amplitude
    maxf = max(freqbin)

    #Get the fitting with the lowest rms
    allresidua = Parallel(n_jobs=self.numworkers)(delayed(bestfit)(freqbin,specratio,allmultiplier[m],maxf,freq = None,freq_calc=False,freqzy = None,fcmin=fcmin,fcmax=fcmax,model=self.source_model) for m in range(len(allmultiplier)))
    if allresidua:
        allresidua1 =  [i[0] for i in allresidua]
        index = np.where(allresidua1 == min(allresidua1))[0][0]
        multiplier = allmultiplier[index]
        allfreq = [i[1][0] for i in allresidua]
        freqfinal = allfreq[index]

    #So why am I recalculating this? Ok, I remember
    # perturbing the frequency to improve fc value
    freqz = np.linspace(fcmin,fcmax,num = len(allmultiplier),endpoint=True)
    allresidua = Parallel(n_jobs=self.numworkers)(delayed(bestfit)(freqbin,specratio,allmultiplier[index],maxf,freq = None,freq_calc=False,freqzy = freqz[m],fcmin=fcmin,fcmax=fcmax,model=self.source_model) for m in range(len(freqz)))
    if allresidua:
        allresidua1 =  [i[0] for i in allresidua]
        index = np.where(allresidua1 == min(allresidua1))[0][0]
        allfreq = [i[1][0] for i in allresidua]
        freqfinal = allfreq[index]
        freqperturb = allfreq
        popt = [i[1] for i in allresidua]
        popt = popt[index]
        pcov = [i[2] for i in allresidua]
        pcov = pcov[index]
    else:
        freqperturb = None; freqfinal = None; multiplier = None; allresidua1 = None; popt = None; pcov = None

#    except:
#        freqperturb = None; freqfinal = None; multiplier = None; allresidua1 = None; popt = None; pcov = None
    return freqperturb,freqfinal,multiplier,allresidua1,popt,pcov
