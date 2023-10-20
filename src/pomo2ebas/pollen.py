class Pollen():
    """
    Pollen object (EBAS translation name, concentration, flag, uncertainty)
    """
    def __init__(self, ebas_name, value, flag, uncertainty):
        self.ebas_name = ebas_name
        self.value = value
        self.flag = flag
        self.uncertainty = uncertainty

class Pollen_Concentration():
    def __init__(self,concentration, accuracy):
        self.concentration = concentration
        self.accuracy = accuracy

def get_station_pollen_list_object(station_pollen_list):
    """
    Convers station pollen list into array of ebas pollen list 
    with zero defualt values 
    and station pollen name as a key
    
    Since the entire list must be sent to EBAS, we first fill in all of the values with zero 
    before setting the predicted value usign set_prediction_pollen_vlues function.
    """
    ebas_pollen_list = {}
    for station_pollen in station_pollen_list:
        for k, v in station_pollen.items():
            ebas_pollen_list[k] = Pollen(v,[0],[[]],0)
    return ebas_pollen_list

def get_station_pollen_list(station_pollen_list):
    """
    Convers station pollen list into array of station names pollen list 
    """
    pollen_list = {}
    for pollen in station_pollen_list:
        for k, v in pollen.items():
            pollen_list[k] = k
    return pollen_list

def set_prediction_pollen_vlues(pollen_object_list, pollen_predicted_list):
    
    for predicted_pollen in pollen_predicted_list:
        pollen_object_list[predicted_pollen].value = [pollen_predicted_list[predicted_pollen].concentration]
        pollen_object_list[predicted_pollen].flag = [[]]
        pollen_object_list[predicted_pollen].uncertainty = (1 - pollen_predicted_list[predicted_pollen].accuracy) 
        #print(predicted_pollen, pollen_object_list[predicted_pollen].value,pollen_object_list[predicted_pollen].uncertainty)
        

    return pollen_object_list
    