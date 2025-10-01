from Modules.FIO.FioAPIKEY import FIO_APIKEY
import requests
import json
import os
import time
from CommonPaths import fio_base_dir

def FIO_PULL(location, loop=0):             #1. gets api headers via key check
                                            #2. pulls api data, gets new key if auth fails
    while loop != 2:
        head = FIO_KEY_CHECK()
        
        if head == "failed to get key":
            return head
        
        fiocontent = requests.get('https://rest.fnar.net/'+location,headers=head)
        
        status_code = fiocontent.status_code
        
        if status_code == 200:
            return json.loads(fiocontent.content)
        
        else:

            if status_code == 400:
                return "parse error"

            elif status_code == 204:
                return "no content"

            elif status_code == 404:
                return "path error"                

            elif status_code == 401:       
                os.remove(fio_base_dir+'fiokey.json')
                time.sleep(5)
                if loop == 1:
                    return 'repeating auth error'
                loop = loop + 1
        
    return "other failure"

def FIO_KEY_CHECK():
    if os.path.exists(fio_base_dir+'fiokey.json') == False:
        
        head = {'Authorization':FIO_APIKEY()}
        
        if head == "failed to get key":
            head = 'failed to get key'
        else:
            with open(fio_base_dir+'fiokey.json', 'w') as fp:
                json.dump(head, fp)
            
    else:
        with open(fio_base_dir+'fiokey.json', 'r') as file:
            head = json.load(file)
            
    return head
    
