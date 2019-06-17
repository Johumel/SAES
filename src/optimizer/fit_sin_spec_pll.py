#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 01:58:44 2019

@author: john.onwuemeka
"""
import numpy as np
from scipy.optimize import curve_fit
from .sinspec_model import sinspec_model
from joblib import Parallel, delayed


def fit_sin_spec_pll(pms,fn,station,fc1min,fc1max,trt,model,numworkers):
    '''
    Description:
    -------------
    This function handles single spectrum fitting to determine all the free 
    parameters (corner frequency, low frequency asymptote, Q-value, n-value,
    gamma-value. It utilizes joblib parallel computing module to generate
    a set of fitting model with different combinations of n & gamma and 
    decides the best fit based on normalised RMS of each model; the model 
    with the lowest RMS is selected as the optimum model.

    Input:
    ------    
    pms        --> Spectrum
    fn         --> frequency bins
    fc1min     --> lower bound of fc
    fc1max     --> upper bound of fc
    trt        --> travel time of event
    model      --> choice of source model
    numworkers --> number of workers for parallel computation

    Returns:
    ---------
    popt --> container of determined optimum model parameters
    pcov --> container for the covariance matrix of the optimum model
     
    '''

    popt,pcov = None,None
    if model.lower() == 'vb':
        Q1,Q2 = 200.,1500.
        datas,boundregion = pms,np.asarray([])
        try:
            if min(fn) < 1:
                brindex = np.where(fn <= 1.)[0][-1]
            elif min(fn) > 1:
                brindex = np.where(fn >= (min(fn)+2))[0][0]
            boundregion = datas[slice(0,brindex)]
        except:
            pass
        if boundregion.any():
            lb = np.median(boundregion)*0.9
            ub = lb*1.5
        else:
            lb = max(datas)*0.95
            ub = lb*1.5
        nn1 = np.linspace(1.8,3.,7)
        nn2 = np.linspace(1.,2.,6)
        fn=fn[slice(0,len(datas))]
        popt1,pcov1 = [],[]
        for i in range(len(nn1)):
            popt_pcov_get = Parallel(n_jobs=numworkers)(delayed(ppl_omfc)(fn,datas,lb,ub,fc1min,fc1max,trt,Q1,Q2,nn1[i],nn2[j]) for j in range(len(nn2)))
            for k in popt_pcov_get:
                if k[0] is not None:
                    popt1.append(k[0])
                    pcov1.append(k[1])
        numres = []
        popt1 = np.asarray(popt1)

        ''' here we use calculate the normalised RMS and select the fitting
        parameters with the least RMS. It comes with additional cost but is
        will mostly produce the best automated reliable fits'''

        for i in popt1:
            residua = np.power(np.subtract(datas,sinspec_model(fn, *i)),2) #L1 norm
            normresidua = np.sqrt(np.sum(residua)/np.sum(np.power(datas,2)))
            numres.append(normresidua)
        index = np.where(np.asarray(numres)== min(numres))[0][0]
        popt,pcov = popt1[index], pcov1[index]
    else:
        raise Exception("To run single spectrum fitting in parallel", \
                            " set method to vb ")
    return popt,pcov

def ppl_omfc(fn,datas,lb,ub,fc1min,fc1max,trt,Q1,Q2,i,j):
    try:
        popt,pcov = curve_fit(sinspec_model, fn,datas ,method='trf',
                          absolute_sigma=True,
                          bounds=((lb,fc1min+0.01,i-0.01,j-0.01,Q1,trt-0.0001),
                                  (ub,fc1max,3.,2.,Q2,trt)),max_nfev = 100000)
    except:
        popt,pcov = None,None
    return popt,pcov