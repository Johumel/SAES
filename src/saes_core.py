#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 09:16:40 2019

@author: john.onwuemeka
"""

import os
# from .saesutils.read_controlfile import read_controlfile
# from .saesutils.get_prefilts import get_prefilts
# from .saesutils.read_xml import read_xml


class saes_core(object):
    """
    A class used to ...

    ...

    Attributes
    ----------

    Methods
    -------

    """
    from .saesutils.read_controlfile import read_controlfile
    from .saesutils.get_prefilts import get_prefilts
    from .saesutils.read_xml import read_xml
    from .handlers.saes_main import saes_main

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
        self.fixed_window = None
        # read_controlfile(self)
        # read_xml(self,1)
        # if self.method in [1,3] and not self.stationxml:
        #     raise FileNotFoundError('stationxml file not found')
        # if self.stationlist and os.path.exists(self.maindir+'/input/pre_filt.list'):
        #     get_prefilts(self)
        #saes_main(self)
        self.read_controlfile()
        self.read_xml(1)
        if self.method in [1,3] and not self.stationxml:
            raise FileNotFoundError('stationxml file not found')
        if self.stationlist and os.path.exists(self.maindir+'/input/pre_filt.list'):
            self.get_prefilts()
        self.saes_main()
