from Modules.Storage.StoreMongo import StoreMongo
from Modules.Transformers.StaticRecipes import StaticRecipes
from Modules.Transformers.T2_StaticRecipeOutputs import T2_StaticRecipeOutputs
from Modules.FIO.FioNaturalSystems import FioNaturalSystemsList
from Modules.FIO.FioNaturalPlanets import FioNaturalPlanetsList

def StaticDataCreate(version):

    # tier 1

    fio_recipes = StaticRecipes()

    systems = FioNaturalSystemsList()

    crafting_planets = FioNaturalPlanetsList()
    delivery_planets = FioNaturalPlanetsList(cx=1)

    # tier 2 (dependant on t1)

    outputs = T2_StaticRecipeOutputs(fio_recipes)

    # write to mongo

    StoreMongo('PAD',1, version, {'recipes':fio_recipes,
                                 'recipe_outputs':outputs,
                                 'crafting_planets':crafting_planets,
                                 'delivery_planets':delivery_planets})
    