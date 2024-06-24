# -*- coding: utf-8 -*-
"""
Funtions to manage monitor types.
Reads from xml or imput files for each station
"""

import xml.etree.ElementTree as ElementTree
from dateutil.parser import parse
from .pollen import Pollen_Concentration
import pytz
import json
from datetime import datetime




class SylvaGeneric(object):
    """Concrete implementation for SYLVA generic monitor """

    json_root = None

    def __init__(self, json_input) -> None:
        self.json_root = json.loads(json_input)

    def timestamp_to_datetime(self, timestamp: int):
        """Returns a given timestamp string as a datetime (for example datetime.datetime(2023, 9, 10, 3, 0, 3))."""
        ts = datetime.fromtimestamp(timestamp)
        return ts

    def get_device_id(self) -> str:
            return(self.json_root['device']['id'])
            

    def get_device_serial(self) -> str:
        if ('serial_number' in self.json_root['device']):
            return self.json_root['device']['serial_number']
        else:
            return None

    def get_software_version(self) -> str:
        if ('software_version' in self.json_root['device']):
            return self.json_root['device']['software_version']
        else:
            return None

    def get_predicted_pollen_list(self, station_pollen_list):
        """Transforms whatevers comes from given io_wrapper to pollen list with measurments."""

        start = int(self.json_root['start'])
        end = int(self.json_root['end'])

        pollen = {}

        for detected_pollen in self.json_root['pollen']:
            pollen_name = detected_pollen['name']
            if pollen_name in station_pollen_list:
                pollen[pollen_name] = Pollen_Concentration(float(detected_pollen['concentration']), float(detected_pollen['uncertainty']))

        d = {}
        d["start"] = self.timestamp_to_datetime(start)
        d["end"] = self.timestamp_to_datetime(end)
        d["pollen"] = pollen

        return d



class BAA500(object):
    """Concrete implementation for Hund monitor BAA500."""

    xml_root = None

    def __init__(self, xml) -> None:
        self.xml_root = ElementTree.fromstring(xml)

    def timestamp_to_datetime(self, timestamp: str):
        """Returns a given timestamp string from BAA500 XML file as a datetime (for example datetime.datetime(2023, 9, 10, 3, 0, 3))."""
        ts = parse(timestamp)
        
        # Sometime, the instrument writes as start time "10:00:03" or "10:01:10" we set minutes and seconds back to 0 
        if ts.time().minute <= 10:
            ts = ts.replace(minute=0)
            
        ts = ts.replace(second=0)

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

    def measure_accuracy(self, pollen_name):
        """
        This function measures the qualitaet mass or accuracy average.
        It simply adds the total accuracy for all identified particles of the same kind 
        and divides it by the number of the same detected particles.
        
        The resulting number is then multiplied by the value of the concentration of the same kind and divided by 100
        Uncertainty is calculated this way if this uncertainty is related to the measurement value..
        """
        for pollen in self.xml_root.findall("./Pollenliste"):
            pollenname = pollen.get("Lateinischer_Name_Pollenart")
            if pollenname == pollen_name:
                qualitaetsmass_saum = 0
                count = 0
                for pollen_concentration in pollen.iter("Polle"):
                    qualitaetsmass_saum = qualitaetsmass_saum + float(pollen_concentration.get("Qualitaetsmass"))
                    count += 1
                return qualitaetsmass_saum / count
        return 0

    def get_device_id(self) -> str:
        return self.xml_root.find("./WMO-Stationsnummer").text
    
    def get_device_serial(self) -> str:
        if (self.xml_root.findall("./Seriennummer")):
            return self.xml_root.find("./Seriennummer").text
        else:
            return None

    def get_software_version(self) -> str:
        if (self.xml_root.findall("./Version_PomoAI")):
            return self.xml_root.find("./Version_PomoAI").text
        else:
            return "1.46.13981"

    def get_predicted_pollen_list(self, station_pollen_list):
        """Transforms whatevers comes from given io_wrapper to pollen list with measurments."""

        start = self.xml_root.find("./Beginn_der_Probenahme")
        end = self.xml_root.find("./Ende_der_Probenahme")

        pollen = {}

        for konzentration in self.xml_root.findall("./Konzentrationsliste/Konzentrationsinformation"):
            pollen_name = konzentration.get("Lateinischer_Name_Pollenart")
            if pollen_name in station_pollen_list:
                accuracy = self.measure_accuracy(pollen_name)
                uncertainty = 1 - accuracy
                pollen[pollen_name] = Pollen_Concentration(float(konzentration.get("Pollenkonzentration")), uncertainty)

        d = {}
        d["start"] = self.timestamp_to_datetime(start.text)
        d["end"] = self.timestamp_to_datetime(end.text)
        d["pollen"] = pollen

        return d
