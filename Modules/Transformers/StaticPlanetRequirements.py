from Modules.FIO.FioAllPlanetsDict import FioNaturalPlanets


planets_data = FioNaturalPlanets()


def build_requirements_dict():

    build_dict = {}

    inconsequential = ['LSE', 'TRU', 'PSL', 'LDE', 'LTA']
    
    for planet in planets_data.keys():

        temp_list = []
        
        for requirement in planets_data[planet]['BuildRequirements']:
            ticker = requirement['MaterialTicker']

            if ticker in inconsequential:
                continue

            temp_list.append(ticker)

        build_dict[planet] = temp_list

    return build_dict