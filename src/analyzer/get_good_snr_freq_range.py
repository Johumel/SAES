#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:16:36 2019

@author: john.onwuemeka
"""

import numpy as np

def get_good_snr_freq_range(signal1,signal2,snr1,snr2,freqsignal1,freqsignal2,noise1,noise2,snrthres):
        datas = None; datae = None; fnm = None; fne = None; 
        noisem = None; noisee = None; snrm = None; snre = None
        quit_calc = 'N'
        try:
            try:
                spm_low = np.where(snr1 >= snrthres )[0][0]
            except:
                spm_low = 0
            try:
                half_up = snr1[slice(spm_low,len(snr1)-1)]
                spm_high = np.where(half_up < snrthres )[0][0] + spm_low 
            except:
                spm_high = len(snr1) - 1
        except:
            quit_calc = 'Y'
            pass
        if signal2 is not None:#.any():# and spm.any():
            try:
                spe_low = np.where(snr2 >= snrthres)[0][0]
            except:
                spe_low = 0
            try:
                half_up = snr2[slice(spe_low,len(snr2)-1)]
                spe_high = np.where(half_up < snrthres )[0][0] + spe_low                 
            except:
                spe_high = len(snr2) - 1
            low_end = max(spe_low,spm_low)
            high_end = min(spe_high,spm_high)
            fnm = freqsignal1[slice(low_end,high_end)] # change to sp later
            fne = freqsignal2[slice(low_end,high_end)]
            datas = signal1[slice(low_end,high_end)] # change to sp later
            datae = signal2[slice(low_end,high_end)]
            snrm = snr1[slice(low_end,high_end)]
            snre = snr2[slice(low_end,high_end)]
            noisem = noise1[slice(low_end,high_end)]
            noisee = noise2[slice(low_end,high_end)]
        else:
            if quit_calc == 'N':
                fnm = freqsignal1[slice(spm_low,spm_high)] # change to sp later
                datas = signal1[slice(spm_low,spm_high)] # change to sp later
                snrm = snr1[slice(spm_low,spm_high)]
                noisem = noise1[slice(spm_low,spm_high)]
        return datas,datae,snrm,snre,fnm,fne,noisem,noisee 