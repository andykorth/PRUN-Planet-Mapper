from Modules.FIO.FioPull import FIO_PULL
from Modules.FIO.FioNaturalSystems import FioNaturalSystemsList

def FioNaturalSystems():

    system_data_list = FIO_PULL('/systemstars')

    NP_validate = FioNaturalSystemsList()
    non_validated = []

    all_systems_dict = {}

    for systemdata in system_data_list:        

        NP = systemdata['NaturalId']

        if NP in NP_validate:

            all_systems_dict[NP] = systemdata

        else:
            non_validated.append(NP)

    if len(non_validated) != 0:
        unvaldict = {}
        unvaldict['unvalidated'] = non_validated
        return unvaldict

    else:
        return all_systems_dict