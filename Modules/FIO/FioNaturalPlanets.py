from Modules.FIO.FioPull import FIO_PULL

def FioNaturalPlanetsList(cx=0):
    
    rawfio = FIO_PULL('/planet/allplanets')            #{'PlanetNaturalId': 'CH-771c', 'PlanetName': 'CH-771c'}
    NP =[]
    for item in rawfio:
        NP.append(item['PlanetNaturalId'])
    
    if len(NP) != 4155:                                #validation
        return 'failed validation, expected 4155, returned '+ len(NP)
    
    if cx == 1:
        
        cxcode = ['BEN','MOR','HRT','ANT','ARC','HUB']
        for cx_item in cxcode:
            NP.append(cx_item)
    
    return NP