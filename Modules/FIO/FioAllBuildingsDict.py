from Modules.FIO.FioPull import FIO_PULL

def FioBuildingsDict():

    buildings_list = FIO_PULL('building/allbuildings')

    buildings_dict = {}

    for fiobuild in buildings_list:        

        build = fiobuild['Ticker']
        
        buildings_dict[build] = fiobuild
        

    return buildings_dict