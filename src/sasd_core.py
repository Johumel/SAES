#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 09:16:40 2019

@author: john.onwuemeka
"""

import os
#from .sasdutils import read_xml,controlfile, get_prefilts
from .handlers.sasd_main import sasd_main
from .sasdutils.read_controlfile import read_controlfile
from .sasdutils.get_prefilts import get_prefilts
from .sasdutils.read_xml import read_xml




class sasd_core(object):

    def __init__(self,controlfilename):

        self.maindir = os.getcwd(); self.mainev = None; self.egfev = None
        self.method = 1
        self.evdict = None
        self.do_spec_rat = None
        self.do_ind_spec = None
        self.evlist = {}
        self.whitelist_evl = []
        self.blacklist_evl = []
        self.output_dir  = None
        self.wvtype2 = None
        self.wvtype1 = None
#        self.soltype = None
        self.stlist_ignore = []
        self.remove_resp = 'NO'
        self.snrthres = 2
        self.showfc2 = 'YES'
        self.freesurface_cor = 'NO'
        self.freesurface_vs = None
        self.freesurface_vp = None
        self.sumtype = 'MEDIAN'
        self.blacklist_stations = []
        self.time_win = None
        self.controlfilename = controlfilename
        self.source_model = 'vb'
        self.autofit_single_spec = 'yes'
        self.output_dir = None
        self.S_tt = {}
        self.P_tt = {}
        self.numworkers = 1
        self.num_tapers = 7
        self.stationxml = None
        self.stationlist = None
        self.baz = {}
        self.baz['main'] = None
        self.baz['egf'] = None
        read_controlfile(self)
        read_xml(self,1)
        if self.method in [1,3] and not self.stationxml:
            raise FileNotFoundError('stationxml file not found')
        if self.stationlist and os.path.exists(self.maindir+'/input/pre_filt.list'):
            get_prefilts(self)
        sasd_main(self)


