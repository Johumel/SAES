#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:20:07 2019

@author: john.onwuemeka
"""

def read_xml(self,xml_format):
        """
        Read station meta data and response file.

        Parameters:
        xml_format (int): input_file_type, 1--obspy; 2--pyrocko;

        Returns/Modifications:
        stationxml (): station metadata, e.g. location and name network, and response file.
        stationlist (dict): two-level dictionary contains the stations info.
            [station_name][station_info],
                          station_info:
                          'lat':latitude
                          'lon':longitude
                          'elev':elevation
                          'pre_filt': pre-defined filtering frequency range for response removal

        """
        #load stationxml
        stationlist = {}
        if xml_format == 1:
            from obspy import read_inventory
            stationxml = read_inventory(self.maindir+'/input/stations.xml',format='STATIONXML')
            if len(stationxml._networks) == 1:
                for i in stationxml._networks[0]:#                for j in i:
                    stationlist[i._code] = {}
                    stationlist[i._code]['lat'] = i._latitude
                    stationlist[i._code]['lon'] = i._longitude
                    stationlist[i._code]['elev'] = i._elevation/1000.
                    stationlist[i._code]['pre_filt'] = []
            else:
                for i in stationxml._networks:#                for j in i:
                    stationlist[i._stations[0].code] = {}
                    stationlist[i._stations[0].code]['lat'] = i._stations[0].latitude
                    stationlist[i._stations[0].code]['lon'] = i._stations[0].longitude
                    stationlist[i._stations[0].code]['elev'] = i._stations[0].elevation/1000.
                    stationlist[i._stations[0].code]['pre_filt'] = []
            self.stationxml = stationxml
            self.stationlist = stationlist
        elif xml_format == 2:
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
        else:
            self.stationxml = None
            self.stationlist = None

        return  None
