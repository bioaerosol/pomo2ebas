# -*- coding: utf-8 -*-
"""
Funtions to manage monitor types.
Reads from xml or imput files for each station
"""

import xml.etree.ElementTree as ElementTree
from dateutil.parser import parse
from .pollen import Pollen_Concentration
import pytz

class BAA500(object):
    """ Concrete implementation for Hund monitor BAA500. """

    @staticmethod
    def timestamp_to_datetime(self, timestamp: str):
        """ Returns a given timestamp string from BAA500 XML file as a datetime (for example datetime.datetime(2023, 9, 10, 3, 0, 3)). """
        ts = parse(timestamp)
        ts = self.convert_datetime_timezone(ts, "Europe/Berlin", "UTC")
        ts = parse(ts)
        return ts
        

    def convert_datetime_timezone(self, dt, from_time_zone, to_time_zone):
        from_time_zone = pytz.timezone(from_time_zone)
        to_time_zone = pytz.timezone(to_time_zone)

        dt = from_time_zone.localize(dt)
        dt = dt.astimezone(to_time_zone)
        dt = dt.strftime("%Y-%m-%d %H:%M:%S")
        return dt
    
    @staticmethod
    def measure_accuracy(pollen_name, root):
        """It measures the qualitaet mass or accuracy average """
        for pollen in root.findall("./Pollenliste"):
            pollenname = pollen.get("Lateinischer_Name_Pollenart")
            if (pollenname==pollen_name):
                qualitaetsmass_saum = 0 
                count = 0
                for pollen_concentration in pollen.iter("Polle"):
                   qualitaetsmass_saum = qualitaetsmass_saum + float(pollen_concentration.get("Qualitaetsmass"))
                   count += 1
                return(qualitaetsmass_saum/count)
        return 0
    
    def get_predicted_pollen_list(self,  io_wrapper, station_pollen_list):
        """ Transforms whatevers comes from given io_wrapper to pollen list with measurments. """
        
        
        # uncomment for testing
        # tree = ElementTree.parse(r"C:\Users\Tofahito\Desktop\ZAUM\EBAS\data\samples\more samples\20230910030003_A223329\20230910030003_A223329\analysis\polle-ad_01-20230910030003-pmon-00025-A223329-xml.xml") 
        # root = tree.getroot()
        
        xml = ""
        for line in io_wrapper:
            xml += line

        if len(xml.strip()) == 0:
            raise ValueError("Invalid input given.")

        root = ElementTree.fromstring(xml)

        start = root.find("./Beginn_der_Probenahme")
        end = root.find("./Ende_der_Probenahme")
        instr_name = root.find("./WMO-Stationsnummer")

        pollen = {}

        for konzentration in root.findall("./Konzentrationsliste/Konzentrationsinformation"):
            pollen_name = konzentration.get("Lateinischer_Name_Pollenart")
            if pollen_name in station_pollen_list:
                accuracy = BAA500.measure_accuracy(pollen_name, root)
                pollen[pollen_name] = Pollen_Concentration(float(konzentration.get("Pollenkonzentration")),accuracy)

        d = {}
        d["start"] = BAA500.timestamp_to_datetime(self,start.text)
        d["end"] = BAA500.timestamp_to_datetime(self,end.text)
        d["instr_name"] = "POMO_BAA500_" + instr_name.text
        d["pollen"] = pollen
        return d
        