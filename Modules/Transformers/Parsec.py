import math
from Modules.Transformers.StaticSystemConns import system_conns
from Modules.FIO.FioAllSystemsDict import FioNaturalSystems
from Modules.Transformers.StaticPairs import system_pairs



def parsec():

    DPP = 11.94825563  #distance per parsec
    conns = system_conns()
    systems_data = FioNaturalSystems()
    pairs = system_pairs()
    parsec_dict = {}
    
    for pair in pairs.keys():
        system1 = pairs[pair][0]
        system2 = pairs[pair][1] 
    
        adjacent_check = 0
        for con in conns[system1]:
            if con[1] == system2:
                adjacent_check = 1
        if adjacent_check == 1:
            sys1_x = systems_data[system1]['PositionX']
            sys1_y = systems_data[system1]['PositionY']
            sys1_z = systems_data[system1]['PositionZ']
            sys2_x = systems_data[system2]['PositionX']
            sys2_y = systems_data[system2]['PositionY']
            sys2_z = systems_data[system2]['PositionZ']
            
            distval = abs(math.sqrt(((float(sys1_x)-float(sys2_x))**2+((float(sys1_y)-float(sys2_y))**2+((float(sys1_z)-float(sys2_z))**2)))))
            
            parsec_dict[pair] = distval / DPP

    return parsec_dict