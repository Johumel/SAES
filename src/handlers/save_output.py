#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 09:47:33 2019

@author: john.onwuemeka
"""
import numpy as np
import os
#Saves the output result(parameters) 
def save_output(self,popt_spec,pcov_spec,norm_spec,tiplier,popt_ind,pcov_ind,station,wv):  

    #Begin fitting the spectral ratio
    if self.do_spec_rat == 'Y':
        perr = np.sqrt(np.diag(pcov_spec))
        fcerr = round(float('%.3g' % perr[0]),2)
#        omega_ratio = round(popt_spec[2]/popt_spec[3],2)
        datafile = self.output_dir + self.mainev +'_multiple.dat'
        if not os.path.exists(datafile):
            with open(datafile, 'w') as f:
                f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' %('EGF','fcm','fce','omega_main','omega_egf','fcmerror','residual',
                                                                   'nvalue','gamma','multiplier','WaveType'))
                f.write('\n%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.3f\t%.3f\t%.2f\t%.2f\t%.2f\t%s' % (self.egfev,round(popt_spec[0],1),round(popt_spec[1],1),
                                                                                        round(popt_spec[2],2),round(popt_spec[3],2),
                                                                                        fcerr,norm_spec,round(popt_spec[4],1),
                                                                                        round(popt_spec[5],1),tiplier,wv))
                f.close()
        else:
            with open(datafile, 'a') as f:
                f.write('\n%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.3f\t%.3f\t%.2f\t%.2f\t%.2f\t%s' % (self.egfev,round(popt_spec[0],1),round(popt_spec[1],1),
                                                                                        round(popt_spec[2],2),round(popt_spec[3],2),
                                                                                        fcerr,norm_spec,round(popt_spec[4],1),
                                                                                        round(popt_spec[5],1),tiplier,wv))
                f.close() 
    if self.do_ind_spec == 'Y':
        perr = np.sqrt(np.diag(pcov_ind))
        fcerr = round(float('%.3g' % perr[0]),2)
        omerr = round(float('%.3g' % perr[0]),2)
        datafile = self.output_dir + self.mainev + '_single.dat'
        if not os.path.exists(datafile):
            with open(datafile, 'w') as f:
                f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' %('Station','EVID','fcm','fcmerror','nvalue',
                                                                   'gamma','QValue','omegaCorMain','omegaErrMain','WaveType'))
                f.write('\n%s\t%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.4e\t%.3f\t%s' % (station,self.mainev,round(popt_ind[1],1),fcerr,round(popt_ind[2],1),
                                                                                      round(popt_ind[3],2),round(popt_ind[4],1),round(popt_ind[0],2),omerr,wv))
                                                                                      
                f.close()
        else:
            with open(datafile, 'a') as f:
                f.write('\n%s\t%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.4e\t%.3f\t%s' % (station,self.mainev,round(popt_ind[1],1),fcerr,round(popt_ind[2],1),
                                                                                      round(popt_ind[3],2),round(popt_ind[4],1),round(popt_ind[0],2),omerr,wv))                                                                          
                f.close() 
    return None

