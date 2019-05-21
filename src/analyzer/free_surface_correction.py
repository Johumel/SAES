#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:04:42 2019

@author: john.onwuemeka
"""
import numpy as np
from scipy.signal import hilbert
from obspy.taup import TauPyModel
Taumo = TauPyModel(model="iasp91")
from obspy.geodetics import locations2degrees as loc2deg
import warnings


def free_surface_correction(self,stream,evid):

    """
    This section computes free surface correction, which mostly
    affect surface station, based on the method in Aki & Richards, 1980;
    House, L. and Boatwright, J., 1980; Kennett, B.L.N., 1991; Kim et al., ??

    Parameters:
    stream (obspy stream): Input 3 component waveform data
    evid (int): Event id.

    Returns:
    
    """

    tr = stream.select(component='T')
    tr += stream.select(component='R')
    tr += stream.select(component='Z')
    evid = str(evid)
    evid = int(evid)#[3:12])
    station = self.stationxml.get_coordinates(stream[0].stats.network.strip()+'.'+stream[0].stats.station.strip()+'..'+\
                        stream[0].stats.channel.strip(), stream[0].stats.starttime)
    latst = station['latitude']; lonst = station['longitude']
    latev = self.evlist[evid][1]
    lonev = self.evlist[evid][2]
    depthev = self.evlist[evid][3]

    # Assumin Vp = 4.8km/s and a poisoon solid Vp/Vs = 1.73
    try:
        if self.freesurface_vp is not None:
            Vp = self.freesurface_vp
    except:
        Vp = 4.8
        pass

    try:
        if self.freesurface_vs is not None:
            Vs = self.freesurface_vs
    except:
        Vs = Vp/1.73
        pass

    epidist = loc2deg(latev,lonev,latst,lonst)
    raypath = Taumo.get_travel_times(source_depth_in_km=depthev,distance_in_degree=epidist,
                                     phase_list=('p','P','s', 'S'))
    if raypath:
            rayparam = raypath[0].ray_param*0.0174533*111 #roughly converts s/rad to s/km
            Z = tr[2].data
            R = tr[1].data
            T = tr[0].data
            A = (1 - (2*Vs**2*rayparam**2))/(2*(np.sqrt(1-(Vs**2*rayparam**2))))
            B = Vs * rayparam
            C = (1 - (2*Vs**2*rayparam**2))/(2*(np.sqrt(1-(Vp**2*rayparam**2))))
            D = Vs**2*rayparam/Vp
            if rayparam < 1/Vp:
                trp = np.add(np.multiply(Z,C),np.multiply(D,R))
                trv = np.subtract(np.multiply(A,R),np.multiply(B,Z))
                trh = np.multiply(T,0.5)
            elif rayparam >= 1/Vp:
                Z = np.imag(hilbert(Z))
                trp = np.add(np.multiply(Z,C),np.multiply(D,R))
                trv = np.subtract(np.multiply(A,R),np.multiply(B,Z))
                trh = np.multiply(T,0.5)
            stream.select(component='R')[0].data = trv
            stream.select(component='T')[0].data = trh
            stream.select(component='Z')[0].data = trp
    else:
        warnings.warn('Could not determine ray parameter for %s at %s' %(evid,stream[0].stats.station.strip()),
                      UserWarning)
    return stream
