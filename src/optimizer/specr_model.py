#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 18:09:06 2019

@author: john.onwuemeka
"""
import numpy as np

def specr_model(fn, a,b,c1,c2,d,e):

    """
    Description:
    ------------
    Theoretical model for spectral ratio. Preferred model is
    determined by the values of d & e and they are user-defined.

    Input:
    -----------------
    fn    --> freqeuncy bins
    a     --> fc main event
    b     --> fc egf
    c1    --> moment  main
    c2    --> moment  egf
    d     --> n value
    e     --> gamma
    
    Returns:
    ---------------------
    Theor_model --> Theoretical spectral ratio model

    """
    var1 = [i/a for i in fn] 
    var2 = [i/b for i in fn] 
    var3 = np.multiply(e,d,dtype=float)
    var4 = np.power(var1,var3,dtype='float64') 
    var5 = np.power(var2,var3,dtype='float64') 
    var6 = [i+1. for i in var4] 
    var7 = [i+1. for i in var5] 
    var8 = [i/j for i,j in zip(var7,var6)]
    var9 = np.power(var8,1./e,dtype=float)
    theor_model = [i*(c1/c2) for i in var9]
    return theor_model