#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: john.onwuemeka; Ge Li
"""
import numpy as np

def get_time_window(mag):

    """
    This is to estimate a time-window based on the magnitude of the event.

    keeping in mind that the minimum resolvable frequency is the inverse
    of the data length in second. Here we assume Vs = 3.75, future release
    with use maybe iasp91 velocity model or user-defined velocity model. We
    assume a constant stress drop of 10 MPa and Brune's model.

    Parameters:
    mag (float), earthquake magnitude.

    Returns:
    time_win(float), time window.
    
    """

    Vs = 3750.
    fc = 0.37*Vs*(16*0.1*1e6/(7*np.power(10,(1.5*(mag + 6.073)))))**(1./3.)
    time_win = np.floor(1./fc)
    if time_win < 1.0:
        time_win = 1.0
    return 2.*time_win
