#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:20:07 2019

@author: john.onwuemeka; Ge Li
"""

def read_xml(self):
    """
    Read station meta data and response file. Current version only uses xml created obspy format
    which is slightly different from xml created with pyrocko. We haven't yet tested with xml created
    by other applications/codes so it may work for those too.

    Parameters:
    xml_format (int): input_file_type, 1--obspy; 2--pyrocko;

    Returns:
    --------
    stationxml (): station metadata, e.g. location and name network, and response file.
    stationlist (dict): two-level dictionary contains the stations info.
        [station_name][station_info],
                      station_info:
                      'lat':latitude
                      'lon':longitude
                      'elev':elevation
                      'pre_filt': pre-defined filtering frequency range for response correction

    """
    #load stationxml
    stationlist = {}
    #if xml_format == 1:
    try:
        from obspy import read_inventory
        stationxml = read_inventory(self.maindir+'/input/stations.xml',format='STATIONXML')
#        if len(stationxml._networks) == 1:
#            for i in stationxml._networks[0]:
#                stationlist[i._code] = {}
#                stationlist[i._code]['lat'] = i._latitude
#                stationlist[i._code]['lon'] = i._longitude
#                stationlist[i._code]['elev'] = i._elevation/1000.
#                stationlist[i._code]['pre_filt'] = []
#        else:
        for j in stationxml._networks:
            for i in j:
                stationlist[i._code] = {}
                stationlist[i._code]['lat'] = i._latitude
                stationlist[i._code]['lon'] = i._longitude
                stationlist[i._code]['elev'] = i._elevation/1000.
                stationlist[i._code]['pre_filt'] = []
        self.stationxml = stationxml
        self.stationlist = stationlist
    #elif xml_format == 2:
    except:
        from pyrocko.io import stationxml
        stationxml = stationxml.load_xml(filename=self.maindir+'/input/stations.xml').get_pyrocko_stations()
        for i in stationxml:
            j = i.station
            stationlist[j] = {}
            stationlist[j]['lat'] = i.lat
            stationlist[j]['lon'] = i.lon
            stationlist[j]['elev'] = i.elevation/1000.
            stationlist[j]['pre_filt'] = []
        self.stationlist = stationlist
        self.stationxml = stationxml
    #else:
    #    self.stationxml = None
    #    self.stationlist = None

    return  None
