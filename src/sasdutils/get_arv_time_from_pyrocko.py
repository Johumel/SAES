#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: john.onwuemeka; Ge Li
"""
from pyrocko import util
from pyrocko.gui import marker as mk
import numpy as np
from obspy.core import UTCDateTime

def get_arv_time_from_pyrocko(self):
    evids = self.evlist.keys()
    markers = mk.load_markers(self.maindir+'/input/tt.dat')
    mk.associate_phases_to_events(markers)
    indexs = [i for i in range(len(markers)) if isinstance(markers[i],(mk.PhaseMarker))]
    evid_markers_index = [j for i in evids for j in indexs if markers[j]._event.name == i]
#    origtime = [UTCDateTime(markers[i]._event.time) for i in evid_markers_index]
    P_tt,S_tt= {},{}
    for i in evids:
        P_tt[i] = []
        S_tt[i] = []
    for j in evid_markers_index:
        if markers[j]._phasename == 'P': P_tt[markers[j]._event.name].append([UTCDateTime(util.time_to_str(markers[j].tmin)),
                       markers[j].get_nslc_ids()[0][1]])
        if markers[j]._phasename == 'S': S_tt[markers[j]._event.name].append([UTCDateTime(util.time_to_str(markers[j].tmin)),
                       markers[j].get_nslc_ids()[0][1]])
#    evidP = [i for i in P_tt.keys() if P_tt[i]]
#    evidS = [i for i in S_tt.keys() if S_tt[i]]
#    evid_tt = np.asarray(list(set(evidP).intersection(evidS)))
    self.P_tt = P_tt
    self.S_tt = S_tt
    return None