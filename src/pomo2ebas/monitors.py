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
    """Concrete implementation for Hund monitor BAA500."""

    xml_root = None

    def __init__(self, io_wrapper) -> None:
        xml = ""
        for line in io_wrapper:
            xml += line

        if len(xml.strip()) == 0:
            raise ValueError("Invalid input given.")

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
        This funtion measures the qualitaet mass or accuracy average.
        It simply adds the total accuracy for all identified particles of the same kind 
        and divides it by the number of the same detected particles.
        
        The resulting number is then multiplied by the value of the concentration of the same kind and devided by 100
        Uncertainty is calculated this way if this uncertintay is related to the measurment value.
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

    def get_predicted_pollen_list(self, station_pollen_list):
        """Transforms whatevers comes from given io_wrapper to pollen list with measurments."""

        start = self.xml_root.find("./Beginn_der_Probenahme")
        end = self.xml_root.find("./Ende_der_Probenahme")

        pollen = {}

        for konzentration in self.xml_root.findall("./Konzentrationsliste/Konzentrationsinformation"):
            pollen_name = konzentration.get("Lateinischer_Name_Pollenart")
            if pollen_name in station_pollen_list:
                accuracy = self.measure_accuracy(pollen_name)
                pollen[pollen_name] = Pollen_Concentration(float(konzentration.get("Pollenkonzentration")), accuracy)

        d = {}
        d["start"] = self.timestamp_to_datetime(start.text)
        d["end"] = self.timestamp_to_datetime(end.text)
        d["pollen"] = pollen

        return d
