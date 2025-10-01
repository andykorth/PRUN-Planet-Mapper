
from multiprocessing import Pool
from Modules.Transformers.abc_planet_system_keygen import abc_key
from Modules.Transformers.StaticPairs import system_pairs
from Modules.Transformers.StaticSystemConns import system_conns
from Modules.Transformers.Parsec import parsec
from Modules.FIO.FioNaturalSystems import FioNaturalSystemsList
import json

conns = system_conns()
systems = FioNaturalSystemsList()
parsec_dict = parsec()



# Steps all paths forward once and creates new paths for valid systems
# simple dijakstra pushing forward in all directions only eleminating paths once the path is worse than the current best completed path
# or the path enters a system with more parsecs than another path
# parsecs as weight tested in-game in an older version and assumed still accurate
def next_path(path_list, complete_path, system_lowest_path,end):
      
    new_path_list = []
    for path in path_list:
        starting_parsecs = path[0]
        for con in conns[path[-1]]:
            new_path = path[:]
            new_path[0] = new_path[0] + parsec_dict[con[0]]
            
            if new_path[0] > system_lowest_path[con[1]] or new_path[0] > complete_path[0]:
                continue
            system_lowest_path[con[1]] = new_path[0]
            new_path.append(con[1])
    
            if con[1] == end:
                complete_path = new_path
            
            new_path_list.append(new_path)
    return new_path_list, complete_path, system_lowest_path


# returns a single fastest path
# can be modified to return complete_path for the [sys1, sys2,..etc] order of the jumps
def fastest_path(start,end):
    
    path_list = [[0,start]]
    complete_path = [1000,'']
    system_lowest_path = {}

    for system in systems:
        system_lowest_path[system] = 1000

    bounds = 0
    while bounds != 100:

        path_list, complete_path, system_lowest_path = next_path(path_list, complete_path, system_lowest_path, end)
        bounds = bounds +1
        if path_list == []:
            break
    final = [abc_key(start,end),complete_path[0],len(complete_path)-2]
    return final


# returns a list of all paths [pair,parsecs,jump count]
# using Pool with around 1MB per process
def all_systempairs_fastest_path():            

    pairs = system_pairs()
    
    map_list = []
    for pair in pairs.items():
        map_list.append(pair[1])

    with Pool() as p:
        return p.starmap(fastest_path,map_list)


def JumpDict():
    jump_list = all_systempairs_fastest_path()
    jump_dict = {}
    
    for pair in jump_list:
        jump_dict[pair[0]] = [pair[1],pair[2]]

    return jump_dict



