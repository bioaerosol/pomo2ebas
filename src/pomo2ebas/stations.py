import yaml
from config import Defaults


class Stations(object):
    """ It imports from yaml a list of stations and allows to manage them. """
    def __init__(self):
        self.defaults = Defaults()
        self.yaml_path = self.defaults.get_default("Config","stations_yaml_path")
        self.stations = self.__get_stations()        
        
    def __get_stations(self):
        with open(self.yaml_path, 'r') as cf: 
            stations_read = yaml.load(cf, Loader=yaml.FullLoader)
        return stations_read["stations"]
    
    def get_stations(self):
        """ Returns a dict of stations""" 
        return self.stations
    
    def get_station_by_name(self, name):
     """ Returns the station with the given Name or None if no such station exists. """
     for station in self.stations:
         if(station["station"]["name"] == name):
             return station["station"]
     return None
 
    
 
 
