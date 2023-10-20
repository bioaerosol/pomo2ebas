import datetime
from nilutility.datatypes import DataObject
from ebas.domain.basic_domain_logic.time_period import estimate_period_code, estimate_sample_duration_code
from config import Defaults
from ebas.io.file.nasa_ames import EbasNasaAmes

class Nas(object):
    """ Store that holds a list of stations and allows to manage them. """
    def __init__(self):
        self.defaults = Defaults()
        self.nas = EbasNasaAmes()

    def set_fileglobal_metadata(self, station):
        """
       Set file global metadata for the EbasNasaAmes file object
    
       Parameters:
           nas    EbasNasaAmes file object
       Returns:
           None
       """
        # The software version should always be included in the revdesc metadata. This will just describe the changes over time while not interfering with the dataset structure.
      
        # But whether you want to change the instr_name or the method element is not straightforward. You need to keep in mind, that each time the instr_name or the method element changes, we start a new dataset in EBAS, i.e. the time series are ruptured.
        # We recommend changing those metadata only if there are changes which rupture the time series anyway (e.g. very different results, not comparable; or different species measured). In your case that would be maybe a completely new instrument model (change instr_name) or a processing algorithm which changes the results significantly (change method).
       
        # All times reported to EBAS need to be in UTC!
        # Setting the timezone here explicitly should remind you to check your data
        self.nas.metadata.timezone = self.defaults.get_default("Config","timezone") 
    
        # Revision information
        self.nas.metadata.revdate = datetime.datetime.utcnow()
        
        # Station metadata
        self.nas.metadata.datalevel = self.defaults.get_default("Config","datalevel")  #live data
        self.nas.metadata.station_code = station["station_code"]
        self.nas.metadata.lab_code = station["lab_code"]
        self.nas.metadata.method = station["method"] #should start with lab code
        self.nas.metadata.instr_type = station["instr_type"]
        
        # We must alter the name whenever we make significant modifications to our data intake. such as a novel processing algorithm.
        self.nas.metadata.instr_name = station["instr_name"]
        self.nas.metadata.matrix = station["matrix"]
        self.nas.metadata.revdesc = station["revdesc"]
        self.nas.metadata.projects = [self.defaults.get_default("Config","projects")]# the same as framework
        
        # Data Originator Organisation
        self.nas.metadata.org = DataObject(
            OR_CODE = station["org"]["OR_CODE"],
            OR_NAME = station["org"]["OR_NAME"],
            OR_ACRONYM = station["org"]["OR_ACRONYM"], 
            OR_UNIT = station["org"]["OR_UNIT"],
            OR_ADDR_LINE1 = station["org"]["OR_ADDR_LINE1"], 
            OR_ADDR_LINE2 = station["org"]["OR_ADDR_LINE2"],
            OR_ADDR_ZIP = station["org"]["OR_ADDR_ZIP"], 
            OR_ADDR_CITY = station["org"]["OR_ADDR_CITY"], 
            OR_ADDR_COUNTRY = station["org"]["OR_ADDR_COUNTRY"]
        )
        
        # Data Originator related to the principal investigators
        for originator in station["originators"] :      
            #we can add as many as we need
            self.nas.metadata.originator.append(DataObject(
                PS_LAST_NAME = originator["originator"]["PS_LAST_NAME"], 
                PS_FIRST_NAME = originator["originator"]["PS_FIRST_NAME"],
                PS_EMAIL = originator["originator"]["PS_EMAIL"],
                PS_ORG_NAME = originator["originator"]["PS_ORG_NAME"],
                PS_ORG_ACR = originator["originator"]["PS_ORG_ACR"], 
                PS_ORG_UNIT = originator["originator"]["PS_ORG_UNIT"],
                PS_ADDR_LINE1 = originator["originator"]["PS_ADDR_LINE1"], 
                PS_ADDR_LINE2 = originator["originator"]["PS_ADDR_LINE2"],
                PS_ADDR_ZIP = originator["originator"]["PS_ADDR_ZIP"], 
                PS_ADDR_CITY = originator["originator"]["PS_ADDR_CITY"],
                PS_ADDR_COUNTRY = originator["originator"]["PS_ADDR_COUNTRY"],
                #PS_ORCID = None,
                PS_ORCID = originator["originator"]["PS_ORCID"],
            ))
        
        for submitter in station["submitters"] :
            # Data Submitters (contact for data technical issues)
            self.nas.metadata.submitter.append(DataObject(
                PS_LAST_NAME = submitter["submitter"]["PS_LAST_NAME"], 
                PS_FIRST_NAME = submitter["submitter"]["PS_FIRST_NAME"],
                PS_EMAIL = submitter["submitter"]["PS_EMAIL"],
                PS_ORG_NAME = submitter["submitter"]["PS_ORG_NAME"],
                PS_ORG_ACR = submitter["submitter"]["PS_ORG_ACR"], 
                PS_ORG_UNIT = submitter["submitter"]["PS_ORG_UNIT"],
                PS_ADDR_LINE1 = submitter["submitter"]["PS_ADDR_LINE1"], 
                PS_ADDR_LINE2 = submitter["submitter"]["PS_ADDR_LINE2"],
                PS_ADDR_ZIP = submitter["submitter"]["PS_ADDR_ZIP"], 
                PS_ADDR_CITY = submitter["submitter"]["PS_ADDR_CITY"],
                PS_ADDR_COUNTRY = submitter["submitter"]["PS_ADDR_COUNTRY"],
                PS_ORCID= submitter["submitter"]["PS_ORCID"],
            ))
    
    
    def set_time_axes(self,station,sample_times):
        """
        Set the time axes and related metadata for the EbasNasaAmes file object.
        
        Parameters:
            nas    EbasNasaAmes file object
        Returns:
            None
        """
        
        # define start and end times for all samples
        self.nas.sample_times = sample_times
        
        # period code is an estimate of the current submissions period, so it should
        # always be calculated from the actual time axes.
        self.nas.metadata.period = estimate_period_code(self.nas.sample_times[0][0], self.nas.sample_times[-1][1])
        
        # Is the whole time covered in this file
        # Sample duration can be set automatically
        self.nas.metadata.duration = estimate_sample_duration_code(self.nas.sample_times)
        # estimated media
        # or set it hardcoded:
        # nas.metadata.duration = '3mo'
        
        # Resolution code can be set automatically
        # But be aware that resolution code is an identifying metadata element.
        # That means, several submissions of data (multiple years) will
        # only be stored as the same dataset if the resolution code is the same
        # for all submissions!
        # That might be a problem for time series with varying resolution code
        # (sometimes 2 months, sometimes 3 months, sometimes 9 weeks, ...). You
        # might consider using a fixed resolution code for those time series.
        # Automatic calculation (will work from ebas.io V.3.0.7):
        #nas.metadata.resolution = estimate_resolution_code(self.nas.sample_times)
        self.nas.metadata.resolution = station["resolution"]

        # avgs between start times.
        # or set it hardcoded:
        # self.nas.metadata.resolution = '3mo' or self.nas.metadata.resolution = '3h'
        
        # It's a good practice to use Jan 1st of the year of the first sample
        # endtime as the file reference date (zero point of time axes).
        self.nas.metadata.reference_date = \
            datetime.datetime(self.nas.sample_times[0][1].year, 1, 1)
            
            
    
    def set_variables(self, station, pollen_list):
        """
        Set metadata and data for all variables for the EbasNasaAmes file object.
        
        Parameters:
            nas    EbasNasaAmes file object
        Returns:
            None
        """
        for pollen in pollen_list:

            values = pollen_list[pollen].value   # missing value is None!
            flags = pollen_list[pollen].flag
            # we can leave it empty else wise we have to look for the flags in pollen 
            # https://ebas-submit.nilu.no/templates/Pollen/lev0
            # [] means no flags for this measurement
            # [999] missing or invalid flag needed because of missing value (None)
            # [632, 665] multiple flags per measurement possible
            # https://ebas-submit.nilu.no/templates/comments/valid_parameters
            
            metadata = DataObject()
            metadata.comp_name = pollen_list[pollen].ebas_name
            metadata.unit = station["unit"]

            self.nas.variables.append(DataObject(values_=values, flags=flags, flagcol=True,metadata=metadata))
        
            # uncertainty
            # Uncertainty is calculated this way if this uncertintay is related to the measurment value.
            values = [x * pollen_list[pollen].uncertainty / 100.0 for x in pollen_list[pollen].value]
            flags = pollen_list[pollen].flag
            
            metadata = DataObject()
            metadata.comp_name = pollen_list[pollen].ebas_name
            metadata.unit = station["unit"]
            metadata.statistics = 'uncertainty'
        
            self.nas.variables.append(DataObject(values_=values, flags=flags, flagcol=True,metadata=metadata))



    def create_nas_file(self):
        """
        Create EbasNasaAmes file object.
        
        Parameters:
           None
        Returns:
            None
        """
        # write the file:
        self.nas.write(createfiles=True)
        # createfiles=True
        #     Actually creates output files, else the output would go to STDOUT.
        # You can also specify:
        #     destdir='path/to/directory'
        #         Specify a specific relative or absolute path to a directory the
        #         files should be written to
        #     flags=FLAGS_COMPRESS
        #         Compresses the file size by reducing flag columns.
        #         Flag columns will be less explicit and thus less intuitive for
        #         humans to read.
        #     flags=FLAGS_ALL
        #         Always generate one flag column per variable. Very intuitive to
        #         read, but increases filesize.
        #     The default for flags is: Generate one flag column per file if the
        #     flags are the same for all variables in the file. Else generate one
        #     flag column per variable.
        #     This is a trade-off between the advantages and disadvantages of the
        #     above mentioned approaches.
        