import pymongo
from pymongo import MongoClient
from Modules.Storage.mongopw import mongopass, db_addr
from Modules.Versioning.Versioning import PAD_Version_Validation

if mongopass == '':
    mongo = MongoClient('mongodb://'+db_addr+':27017/')
else:
    mongo = MongoClient('mongodb://'+db_addr+':27017/',username='admin',password=mongopass)    

Varname = {
            0: 'Starting_PAD',
            1: 'Static',
            2: 'COG',
            3: 'COG_Miss',
            4: 'Outputs',
            5: 'Base_Amort',
            6: 'Ship_Daily_Cost',
            7: 'Available_Ship_Types',
            8: 'Natural_Planets',
            'TestCollection': 'Testing'
}

def StoreMongo(app, collection, key, value):
    
    check = MongoVal(app, collection, key)
    if check != 'good':
        return check
    
    collection_des = Varname[collection]
    
    mongoapp = mongo[app]
    mongocollection = mongoapp[collection_des]
    
    check = mongocollection.find_one({str(key):{'$exists': True}})
                    
    if check == None:
        mongocollection.insert_one({str(key):value})
        return 'added'
                    
    else:
                    
        return 'dupe'

def ReadMongo(app, collection, key):
                    
    check = MongoVal(app, collection, key)
    if check != 'good':
        return check

    collection_des = Varname[collection]
                    
    mongoapp = mongo[app]
    mongocollection = mongoapp[collection_des]
                    
    data = mongocollection.find_one({str(key):{'$exists': True}})
                    
    if data == None:
        return 'not found'
                    
    return data[str(key)]
                    
def MongoVal(app, collection, key):
        
    if app != 'PAD':
        return 'wrong app'
                    
    if collection == 'TestCollection':
        return 'good'
        
    if collection not in range(9):
        return 'bad collection'
    
    check2 = PAD_Version_Validation(collection, key)
    if check2 == 'failed val':
        return 'bad key'
    
    return 'good'
  