#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:57:06 2019

@author: john.onwuemeka
"""
import numpy as np
#import math


def sinspec_model(fn,a,b,c,d,f,trt):
    ''' Here we model the single spectrum with the assumption
    that anaelastic attenuatic and geometrical spreading effects
    are corrected by quality factor Q and distance term R '''
    #fn = frequency bins
    # a = seismic momemt
    # b = corner frequency
    # c = nvalue
    # d = gamma
    # e = travel time
    # f = Quality factor
    #fun = @(fc,fn) (fc(1)*exp(-pi*fn*t/fc(5)))./((1+(fn/fc(2)).^(fc(3)*fc(4))).^(1/fc(4)))
    var1 = (-1 * np.pi * trt)/f
    var2 = np.exp([i*var1 for i in fn])
    var3 = [i*a for i in var2]
    var4 = np.power(np.divide(fn,b),d*c,dtype=float)
    var5 = [i+1. for i in var4]
    var6 = np.power(var5,1./d,dtype=float)
    theor_model = [i/j for i,j in zip(var3,var6)]
    return theor_model