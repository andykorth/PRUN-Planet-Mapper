from Modules.FIO.FioPull import FIO_PULL

def FioMaterialsDict():

    materials_list = FIO_PULL('/material/allmaterials')         #re = ['minerals','gases','ores','liquids']

    materials_dict = {}

    for fiomat in materials_list:        

        mat = fiomat['Ticker']
        
        materials_dict[mat] = fiomat
        

    return materials_dict