import json
import requests
from CommonPaths import fio_base_dir

def FIO_APIKEY():
    with open(fio_base_dir+'auth.json', 'r') as file:
        apiauth = json.load(file)
        
    FIOAPIKEY = requests.post('https://rest.fnar.net/auth/login',json=apiauth)
    
    if FIOAPIKEY.status_code != 200:
        return "failed to get key"
    else:
        FIOAPIKEY = json.loads(FIOAPIKEY.content)
        return FIOAPIKEY['AuthToken']