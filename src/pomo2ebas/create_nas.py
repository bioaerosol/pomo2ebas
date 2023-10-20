"""

The main section reads pollen predictions from xml and converts them to EbasNasaAmes file format.
        
"""

from stations import Stations
from monitors import BAA500
from pollen import get_station_pollen_list_object,get_station_pollen_list,set_prediction_pollen_vlues
from nas import Nas
import sys
from config import Defaults

defaults = Defaults(config_file="etc/pomo2ebas/defaults.yaml")
stations = Stations(config_file="etc/pomo2ebas/stations.yaml")

# create objects
baa500 = BAA500()
nas = Nas(timezone=defaults.get_default("Config", "timezone"), datalevel=defaults.get_default("Config", "datalevel"), project=defaults.get_default("Config", "projects"))

# load station from yaml
station = stations.get_station_by_name("pomo")

# load station pollen list from yaml
pollen_list = station["pollens"]

# simple list of station pollens from yaml
pollen_simple_list = get_station_pollen_list(pollen_list)

# read station predictions from io_weapper (prompt or input)
io_wrapper = sys.stdin
pollen_predicted_list = baa500.get_predicted_pollen_list(io_wrapper, pollen_simple_list)

# convert pollen list into a list of pollen objects of type Pollen
pollen_object_list = get_station_pollen_list_object(pollen_list)

# Set file global metadata for the EbasNasaAmes file object
nas.set_fileglobal_metadata(station)

# set prediction start and end date and time
sample_times = [(pollen_predicted_list["start"], pollen_predicted_list["end"])]

# Set the time axes and related metadata for the EbasNasaAmes file object.
nas.set_time_axes(station, sample_times)

# set values of predicted pollen
pollen_object_list = set_prediction_pollen_vlues(pollen_object_list, pollen_predicted_list["pollen"])

# set metadata and data for all variables for the EbasNasaAmes file object.
nas.set_variables(station, pollen_object_list)

# create EbasNasaAmes file object.
nas.create_nas_file()
