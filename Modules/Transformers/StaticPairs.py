from Modules.Transformers.StaticSystemStars import system_stars
from Modules.FIO.FioNaturalSystems import FioNaturalSystemsList
from Modules.FIO.FioAllPlanetsDict import FioNaturalPlanets
from Modules.Transformers.abc_planet_system_keygen import abc_key



def stl_pairs():  # {'YK-024': [['YK-024a', 'YK-024b', 158.0], ['YK-024a', 'YK-024c', 249.0]}  [planet1, planet2, sum of orbital axis]

    planets_data = FioNaturalPlanets()
    systems = FioNaturalSystemsList()
    system_stars2 = system_stars()
    
    cxcode = ['BEN','MOR','HRT','ANT','ARC','HUB']
    cx = ['UV-351','OT-580','VH-331','ZV-307','AM-783','TD-203']
    cxdist = [planets_data['UV-351b']['OrbitSemiMajorAxis'] * 1.2, planets_data['OT-580b']['OrbitSemiMajorAxis'] * 1.2, planets_data['VH-331a']['OrbitSemiMajorAxis'] * 2, planets_data['ZV-307a']['OrbitSemiMajorAxis'] * 0.5, planets_data['AM-783d']['OrbitSemiMajorAxis'] * 0.9, planets_data['TD-203b']['OrbitSemiMajorAxis'] * 2]
    
    count = 0
    for x in cxcode:
        temp_dict = {}
        temp_dict['OrbitSemiMajorAxis'] = cxdist[count]
        planets_data[x] = temp_dict
        count = count + 1
    
    pairs = {}
    for system in systems:
        count = 0
        pairs[system] = []
        for planet in system_stars2[system]:
            size = len(system_stars2[system]) - count
            axis1 = planets_data[planet]['OrbitSemiMajorAxis']
            templist = system_stars2[system]
            for z in range(size-1):
                second_planet = templist[z+1+count]
                axis2 = planets_data[second_planet]['OrbitSemiMajorAxis']
                templist2 = pairs[system]
                templist2.append([planet,second_planet,round((axis1+axis2)/1000000000,0)])
            count = count + 1

    return pairs

def system_pairs():          # {'QQ-001_OT-580':['QQ-001','OT-580']}     abc_key for unorded pair combinations with a list of the two systems

    systems = FioNaturalSystemsList()

    system_pairs_dict = {}
    
    for system1 in systems:
        for system2 in systems:
            if system1 == system2:
                continue
            key = abc_key(system1, system2)
            system_pairs_dict[key] = [system1, system2]

    
    return system_pairs_dict