import yaml



class Stations(object):
    """ It imports from yaml a list of stations and allows to manage them. """
    def __init__(self, config_file: str):
        self.yaml_path = config_file
        self.stations = self.__get_stations()        
        
    def __get_stations(self):
        with open(self.yaml_path, 'r') as cf: 
            stations_read = yaml.load(cf, Loader=yaml.FullLoader)
        return stations_read["stations"]
    
    def get_stations(self):
        """ Returns a dict of stations""" 
        return self.stations
    
    def get_station_by_id(self, id: str):
     """ Returns the station with the given ID or None if no such station exists. """
     for station in self.stations:
         if(station["station"]["id"] == id):
             return station["station"]
     return None
 
    
 
 
