class ProcurementMethod:
    key = None
    value = None
    min_close_of_bids = None
    
    def __init__(self, key, value, min_close_of_bids):
        self.key = key
        self.value
        self.min_close_of_bids

ODB = ProcurementMethod("Open Domestic Bidding", "Open Domestic Bidding", 20)

procurement_methods = [OBD]



class ProcurementType:
    name = None
    abbreviation = None
    dict_key_name = None

    def __init__(self, name, abbreviation, dict_key_name):
        self.name = name
        self.abbrviation = abbreviation
        self.dict_key_name = dict_key_name


    def get_as_field_choices(self):
        pass
    

procurement_types = [
        ProcurementType("SUPPLIES", "S", "SUPPLIES"),
        ProcurementType("WORKS", "W", "WORKS"),
        ProcurementType("NON-CONSULTANCY SERVICES", "NCS", "NON_CONSULTANCY_SERVICES"),
        ProcurementType("CONSULTANCY SERVICES", "CS", "CONSULTANCY_SERVICES"),
    ]
