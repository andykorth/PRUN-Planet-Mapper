from Modules.FIO.FioAllPlanetsDict import FioNaturalPlanets
from Modules.FIO.FioNaturalPlanets import FioNaturalPlanetsList
from Modules.Transformers.StaticSystemConns import systemid_to_system

def system_stars():
    
    planets_data = FioNaturalPlanets()
    planets = FioNaturalPlanetsList()
    id_dict = systemid_to_system()
    
    cx_systems = {'UV-351':'BEN', 'OT-580':'MOR', 'VH-331':'HRT', 'ZV-307':'ANT', 'TD-203':'HUB', 'AM-783':'ARC'}
    system_stars = {}
    
    for cx_sys in cx_systems.keys():
        cx = cx_systems[cx_sys]
        system_stars[cx_sys] = [cx]
        system_stars[cx] = cx_sys
    
    for planet in planets:
        sys_id = planets_data[planet]['SystemId']
        sys = id_dict[0][sys_id]
        if sys in system_stars.keys():
            system_stars[sys].append(planet)
        else:
            system_stars[sys] = [planet]
            
        system_stars[planet] = sys

    return system_stars