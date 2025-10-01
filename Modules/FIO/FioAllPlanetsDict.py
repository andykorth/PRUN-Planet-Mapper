from Modules.FIO.FioPull import FIO_PULL
from Modules.FIO.FioNaturalPlanets import FioNaturalPlanetsList

def FioNaturalPlanets():

    planet_data_list = FIO_PULL('/planet/allplanets/full')

    NP_validate = FioNaturalPlanetsList()
    non_validated = []

    all_planets_dict = {}

    for planetdata in planet_data_list:        

        NP = planetdata['PlanetNaturalId']

        if NP in NP_validate:

            all_planets_dict[NP] = planetdata

        else:
            non_validated.append(NP)

    if len(non_validated) != 0:
        unvaldict = {}
        unvaldict['unvalidated'] = non_validated
        return unvaldict

    else:
        return all_planets_dict