#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 18:16:46 2019

@author: john.onwuemeka; Ge Li
"""
import numpy as np
from scipy.optimize import curve_fit
from .sinspec_model import sinspec_model
import matplotlib.pyplot as plt

def fit_sin_spec(pms,fn,station,fc1min,fc1max,trt,style,model):
     """
     Description:
     -------------
 	 Single spectrum fitting function for a user-defined source model.
     This function searches for the combination of parameters that give the
     optimum result. It utilizes the least-square curve_fit function of scipy.
     The 'manual' option allows user to review each spectrum fit and make
     'discard or keep' decision.

     Input:
     -----------------
     pms        --> single spectrum amplitudes
     fn         --> single spectrum frequency bins
     station    --> station
     fc1min     --> lower bound of corner frequency
     fc1max     --> upper bound of corner frequency
     trt        --> travel time
     style      --> user-defined parameter used if a user wants to review each
                    single spectrum model fit
     model      --> Source model

     Returns:
     ----------------------
     popt       --> model fit parameters
     pcov       --> model fit covariance matrix

     """
     
     popt = [None]; pcov = [None]
     ''' style options: 'auto','manual' '''
     ''' model options: 'B' - Brune, 'fB' -- fixed Boatwright,
                        'vB' -- variable Boatwright '''
     if model.upper() == 'B':
        n1,n2,n3,n4 = 2,1,2,1
     elif model.upper() == 'FB':
        n1,n2,n3,n4 = 4,2,4,2
     elif model.upper() == 'VB':
        n1,n2,n3,n4 = 2,1,3,2
     else:
        raise Exception('Model options must be B, FB, or VB')
     if style.lower() == 'yes':
        style = 'AUTO'
     elif style.lower() == 'no':
        style = 'MANUAL'
     else:
        raise Exception("Style must be 'A', 'M', 'AUTO' or 'MANUAL'")
     Q1,Q2 = 200.,2000.
     datas,boundregion = pms, np.asarray([])
     try:
        if min(fn) < 1:
            brindex = np.where(fn >= 0.8)[0][0]
        elif min(fn) > 1:
            brindex = np.where(fn >= (min(fn)+2))[0][0]
        boundregion = datas[slice(0,brindex)]
     except:
         pass
     if boundregion.any():
         lb = np.median(boundregion)*0.8
     else:
         lb = max(datas)*0.95
     ub = lb*1.5
     nn1 = np.arange(n1,n3,0.2)
     nn2 = np.arange(n2,n4,0.2)
     plotok = 'No'
     while plotok is 'No':
         for i in nn1:
                 for j in nn2:
                     if plotok == 'No':
                         if style.upper()  == 'AUTO':
                             plotok = 'yes'
                         else:
                             n1 = i
                             n2 = j
                         fn=fn[slice(0,len(datas))]
                         popt, pcov = curve_fit(sinspec_model, fn,datas ,method='trf',absolute_sigma=True,bounds=((lb,fc1min,n1-0.01,n2-0.01,Q1,trt-0.0001),(ub,fc1max,n3,n4,Q2,trt)),maxfev=100000)
                         if style.upper() == 'MANUAL':
                             print('fit for %s' % station)
                             figr = plt.figure(3,figsize=(8,5))
                             axb = figr.add_subplot(111)
                             axb.loglog(fn, sinspec_model(fn, *popt), 'k--', label='model fit',linewidth=2)
                             bb = np.log10(min(fn)).round()
                             axb.set_xlim([10**bb,fc1max*1.5])
                             axb.loglog(fn,datas,linewidth = 1,color = 'r',label = 'data')
                             figr.show()
                         if plotok not in  ['1','yes','y']:
                            plot = None
                            while plotok not in ['1','0','no','yes','y','n']:
                                print("Please tell me if the plot is ok. Valid options are: 1, 0, no, yes, y or n")
                                plotok = input('Is the fit ok? ')
                         if not plotok or plotok in ['0','no','n']:
                            plotok = 'No'
                         else:
                            break
     return popt,pcov
