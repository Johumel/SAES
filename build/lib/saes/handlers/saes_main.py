#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:27:01 2019

@author: john.onwuemeka; Ge Li
"""


from ..saesutils.read_cclist import read_cclist
from ..saesutils.read_ext_timetable import read_ext_timetable
from ..saesutils.get_arv_time_from_pyrocko import get_arv_time_from_pyrocko
from .spec_ratio_guru import spec_ratio_guru
from .sin_spec_guru import sin_spec_guru
import os,datetime

def saes_main(self):

    '''
    Main program handler. This is the main function called to initialize
    all the variables required for the rest of the computation. It calls other
    functions to read and organize P and S waves, cross-correlation table and
    initiate single spectrum and/or spectral ratio functions.
    '''

    sol = self.method
    print(sol)
    if int(sol) in [1,2,3]:
        if int(sol) == 1:
            self.do_ind_spec = 'Y'; self.do_spec_rat = 'N'
            self.soltype = 'ind'
        if int(sol) == 2:
            self.do_ind_spec = 'N'; self.do_spec_rat = 'Y'
            self.soltype = 'spec'
        if int(sol) == 3:
            self.do_ind_spec = 'Y'; self.do_spec_rat = 'Y'
            self.soltype = 'both'
    try:
        get_arv_time_from_pyrocko(self)
    except:
        #pass
        try:
            read_ext_timetable(self)
        except:
            pass
        pass
    if  bool(self.S_tt) == True or bool(self.P_tt) == True:
        if self.do_spec_rat == 'Y':
            evid1 = read_cclist(self)
            dlist = []; dlist_ind = []
            for j in range(0,len(evid1)):
                if  '%s' %(evid1[j]) not in dlist:
                    self.output_dir  = self.maindir+'/output/'+evid1[j]+'/'
                    if not os.path.exists(self.output_dir ):
                        os.makedirs(self.output_dir )
                    if self.wvtype2 == 'S':
                        spec_ratio_guru(self,evid1[j],'S')
                    if self.wvtype1=='P':
                        spec_ratio_guru(self,evid1[j],'P')
                    dlist.append('%s' %(evid1[j]))
                    if self.method == 3:
                        dlist_ind.append(evid1[j])
        if self.do_ind_spec == 'Y':
            evid1 = list(set([i for i in self.evlist.keys()]))
            #print(evid1)
            try:
                dlist_ind = list(set(dlist_ind))
            except NameError:
                dlist_ind = []
                pass
            if self.wvtype2 == 'S':
                sin_spec_guru(self,evid1,'S',evid1)#dlist_ind)
            if self.wvtype1=='P':
                sin_spec_guru(self,evid1,'P',evid1)#dlist_ind)
    else:
        raise FileNotFoundError('Travel time file could not be found')
    return None
