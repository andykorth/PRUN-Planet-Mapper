from Modules.FIO.FioPull import FIO_PULL
from Modules.Transformers.StaticPlanetRequirements import build_requirements_dict
import pandas as pd
import numpy as np

# takes a list of population reports from FIO and finds the greatest(newest)
# builds a dict pop type and planet with the most recent 12 weeks in acsending order
def pop():

    infrastructure = FIO_PULL('/infrastructure/all')
    infra_dict = {}  
    
    for item in infrastructure:
        key = item['PlanetNaturalId']
        infra_dict[key] = item
         
    faillist = []
    pop_dict = {}
    for planet in infra_dict.keys():
        
        masterlist = []
        poplist = infra_dict[planet]['Reports']
        tempdict = {}
        for x in poplist:
            key = x['SimulationPeriod']
            value = []
            pio = x['NextPopulationPioneer']
            sets = x['NextPopulationSettler']
            tech = x['NextPopulationTechnician']
            eng = x['NextPopulationEngineer']
            sci = x['NextPopulationScientist']
            extrapio = 0
            extrasets = 0
            extratech = 0
            extraeng = 0
            extrasci = 0
            ################################# PIO
            if x['PopulationDifferencePioneer'] >0 and x['OpenJobsPioneer'] < x['PopulationDifferencePioneer']:
                extrapio = x['PopulationDifferencePioneer'] - x['OpenJobsPioneer']
            if x['UnemploymentRatePioneer'] > 0:
                extrapio = extrapio + x['NextPopulationPioneer'] * x['UnemploymentRatePioneer']
                ############################## SET
            if x['PopulationDifferenceSettler'] >0 and x['OpenJobsSettler'] < x['PopulationDifferenceSettler']:
                extrasets = x['PopulationDifferenceSettler'] - x['OpenJobsSettler']
            if x['UnemploymentRateSettler'] > 0:
                extrasets = extrasets + x['NextPopulationSettler'] * x['UnemploymentRateSettler']
                ############################### TECH
            if x['PopulationDifferenceTechnician'] >0 and x['OpenJobsTechnician'] < x['PopulationDifferenceTechnician']:
                extratech = x['PopulationDifferenceTechnician'] - x['OpenJobsTechnician']
            if x['UnemploymentRateTechnician'] > 0:
                extratech = extratech + x['NextPopulationTechnician'] * x['UnemploymentRateTechnician']
                ################################# ENG
            if x['PopulationDifferenceEngineer'] >0 and x['OpenJobsEngineer'] < x['PopulationDifferenceEngineer']:
                extraeng = x['PopulationDifferenceEngineer'] - x['OpenJobsEngineer']
            if x['UnemploymentRateEngineer'] > 0:
                extraeng = extraeng + x['NextPopulationEngineer'] * x['UnemploymentRateEngineer']
                #################################### SCI
            if x['PopulationDifferenceScientist'] >0 and x['OpenJobsScientist'] < x['PopulationDifferenceScientist']:
                extrasci = x['PopulationDifferenceScientist'] - x['OpenJobsScientist']
            if x['UnemploymentRateScientist'] > 0:
                extrasci = extrasci + x['NextPopulationScientist'] * x['UnemploymentRateScientist']
            pio = pio - extrapio
            sets = sets - extrasets
            tech = tech - extratech
            eng = eng - extraeng
            sci = sci - extrasci
            value = [pio,sets,tech,eng,sci]
            tempdict[key] = value
        simlist = []
        for x in tempdict.keys():
            simlist.append(x)
        try:
            maxsim = max(simlist)
        except:
            faillist.append(planet)
            continue
        temppio = [planet+"-PIO",planet,'PIO',0,0,0,0,0,0,0,0,0,0,0,0]
        tempsets = [planet+"-SET",planet,'SET',0,0,0,0,0,0,0,0,0,0,0,0]
        temptech = [planet+"-TECH",planet,'TECH',0,0,0,0,0,0,0,0,0,0,0,0]
        tempeng = [planet+"-ENG",planet,'ENG',0,0,0,0,0,0,0,0,0,0,0,0]
        tempsci = [planet+"-SCI",planet,'SCI',0,0,0,0,0,0,0,0,0,0,0,0]
    
        for x in range(12):
            currentsim = maxsim - x
            try:
                temppio[-1-x] = tempdict[currentsim][0]
                tempsets[-1-x] = tempdict[currentsim][1]
                temptech[-1-x] = tempdict[currentsim][2]
                tempeng[-1-x] = tempdict[currentsim][3]
                tempsci[-1-x] = tempdict[currentsim][4]
            except:
                continue
        masterlist.append(temppio)
        masterlist.append(tempsets)
        masterlist.append(temptech)
        masterlist.append(tempeng)
        masterlist.append(tempsci)
        pop_dict[planet] = masterlist
    return pop_dict

# returns a dict with key as planet and provides a list with each pop type for the most recent report
# example {'UV-351c': [40,000, 20,000, 10,000, 1,000, 150]}
def current_pop():

    pops = pop()
    
    current_pop_dict = {}
    pop_order = ['PIO','SET','TECH','ENG','SCI']
    
    for planet in pops.keys():
        templist = [0,0,0,0,0]
        
        for pop_list_item in pops[planet]:
            index = pop_order.index(pop_list_item[2])
            templist[index] = pop_list_item[-1]
            
        popcheck = 0
        for pop_num in templist:
            popcheck = popcheck + pop_num

        if popcheck <= 100:
            continue
        else:
            current_pop_dict[planet] = templist
    return current_pop_dict



def popbyrequirement(ticker):

    req_planets = []
    brl = build_requirements_dict()
    pop_list = pop()
    
    for planet in brl.keys():
        try:
            if ticker in brl[planet]:
                for pop_type in pop_list[planet]:
                    temp_list = pop_type[3:]
                    req_planets.append(temp_list)
        except:
            continue

    np_list = np.array(req_planets)
    np_list = np.sum(np_list, axis=0)
    
    return np_list

def df_popbyrequirement():
    
    require_dict_planetpop = {}
    header = ['Week-11', 'Week-10','Week-9','Week-8','Week-7','Week-6','Week-5','Week-4','Week-3','Week-2','Week-1','Week-Current']
    index_ticker = ['MCG', 'AEF', 'SEA', 'HSE', 'TSH', 'INS', 'MGC', 'BL']

    for iticker in index_ticker:
        require_dict_planetpop[iticker] = popbyrequirement(iticker)

    df = pd.DataFrame.from_dict(require_dict_planetpop, orient='index', columns = header)

    return df.round(decimals=0)
