#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 18:16:46 2019

@author: john.onwuemeka
"""
import numpy as np
from scipy.optimize import curve_fit
from .sinspec_model import sinspec_model
import matplotlib.pyplot as plt

def fit_sin_spec(pms,fn,station,fc1min,fc1max,trt,style,model):
     """
     Description:
     -------------
 	 Constraining the low frequency asymptote
 	 this will ensure that any bump in the spectrum does not bias the estimate
     of the omega this part gives the user some room to determine good fit but
     can also run without user input.

     Parameters/Input:
     -----------------

     Returns/Modifications:
     ----------------------


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
#     try:
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
     #Compute and Plot for variable Q
     nn1 = np.arange(n1,n3,0.2)
     nn2 = np.arange(n2,n4,0.2)
     plotok = 'No'
     while plotok is 'No':
         for i in nn1:
                 for j in nn2:
                     if plotok == 'No':
                         if style.upper()  == 'AUTO':
                             plotok = 1
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
                         if plotok != 1:
                             plotok = input('Is the fit ok? ')
                         if not plotok or int(plotok) != 1:
                            plotok = 'No'
                         else:
                            break
#
#
#     except:
#         popt = [None]; pcov = [None]
#         pass
     return popt,pcov
