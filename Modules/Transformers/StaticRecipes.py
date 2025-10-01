from Modules.FIO.FioRecipesDict import FioRecipesDict
from Modules.FIO.FioMaterialsDict import FioMaterialsDict

def StaticRecipes():
    fio_recipes = FioRecipesDict()
    fio_mat = FioMaterialsDict()
    re = ['minerals','gases','ores','liquids']
    
    for key, value in fio_mat.items():
        if value['CategoryName'] in re:
            fio_recipes['=>'+key] = {'RecipeName': '=>'+key, 'Inputs': [], 'Outputs': [{'Ticker': key, 'Amount': 0}]}

    fio_recipes['2xZIR=>1xZR 2xSIO']['Outputs'] = [{'Ticker': 'ZR', 'Amount': 1},{'Ticker': 'SIO', 'Amount': 2}]
    fio_recipes['2xBER=>1xBE 1xAL 1xSIO']['Outputs'] = [{'Ticker': 'BE', 'Amount': 1}, {'Ticker': 'AL', 'Amount': 1}, {'Ticker': 'SIO', 'Amount': 1}]
    
    return fio_recipes
    