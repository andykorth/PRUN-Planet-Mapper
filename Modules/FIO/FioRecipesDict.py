from Modules.FIO.FioPull import FIO_PULL

def FioRecipesDict():

    recipes_list = FIO_PULL('/recipes/allrecipes')

    recipes_dict = {}

    old = ['75xPG=>1xBDE', '100xPE 1xAR 1xTHF=>20xINS', '20xH2O 1xDDT 2xSOI=>10xPIB', '40xH2O 2xDDT 4xSOI=>15xHOP', '30xH2O 1xDDT 3xSOI=>5xGRA']

    for fiorecipe in recipes_list:        

        recipe = fiorecipe['RecipeName']
        
        if recipe == '=>' or recipe in old:
            continue
        
        recipes_dict[recipe] = fiorecipe
        

    return recipes_dict