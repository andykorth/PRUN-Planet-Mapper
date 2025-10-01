from Modules.FIO.FioPull import FIO_PULL

def FioNaturalSystemsList():
    
    rawfio = FIO_PULL('/systemstars')         
    NS =[]
    for item in rawfio:
        NS.append(item['NaturalId'])
    
    if len(NS) != 637:                             
        return 'failed validation, expected 637, returned '+ len(NS)
    
    return NS