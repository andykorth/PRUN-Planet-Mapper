import Modules.Calcs.Shipping
import pandas as pd
import itertools


# fio pull the contracts and pass into funct
# id_dict is unique contracts
# contract_dict is a list of contracts to the same start-> end
def shipping_contracts(contracts):

    contract_dict = {}
    id_dict = {}

    for item in contracts:
        origin = item['OriginPlanetNaturalId']
        dest = item['DestinationPlanetNaturalId']
        lm = item['PlanetNaturalId']
        key = origin + '->' + dest 
        weight = item['CargoWeight']
        vol = item['CargoVolume']
        money = item['PayoutPrice']
        unique_id = item['ContractNaturalId']
        id_dict[unique_id] = [key, origin, dest, lm, weight, vol, money, unique_id]
        if key not in contract_dict.keys():
            contract_dict[key] = [[key, origin, dest, lm, weight, vol, money, unique_id]]       
        else:
            contract_dict[key].append([key, origin, dest, lm, weight, vol, money, unique_id])   

    return contract_dict, id_dict
    

def cargo(ship):
    if ship == 'LCB':
        ship_cargo = [2000,2000]
    elif ship == 'WCB':
        ship_cargo = [3000,1000]
    elif ship == 'VCB':
        ship_cargo = [1000,3000]
    else:
        ship_cargo = [500,500]
    return ship_cargo

# needs cargo size [weight/vol]
# feed in contract and id dict
# outputs a dict of full ship loads for a single ship type
# outputs a 2nd dict with contract info for mapping back to id dict

def full_load(ship_cargo,contract_dict, id_dict):
    
    full_ship_dict = {}
    full_ship_dict_contractinfo = {}
    full_load_count = 1
    cols = ['key', 'origin', 'dest', 'lm', 'weight', 'vol', 'money', 'id']

    valid_dict = {}
    for pair in contract_dict.keys():
        for contract in contract_dict[pair]:
            weight = contract[4]
            vol = contract[5]
            origin = contract[1]
            dest = contract[2]
            money = contract[6]
            
            if weight <= ship_cargo[0] or vol <= ship_cargo[1]:
                
                if weight > ship_cargo[0]*.99 or vol > ship_cargo[1]*.99:
    #checks if contract is near a full load and adds to load dict
                    full_ship_dict[full_load_count] = [origin, dest, money]
                    full_ship_dict_contractinfo[full_load_count] = [contract[7]]
                    full_load_count = full_load_count + 1
                    continue
                    
                if pair not in valid_dict.keys():
                    valid_dict[pair] = [contract]
                else:
                    valid_dict[pair].append(contract)

    for key in valid_dict.keys():
    
        df = pd.DataFrame(valid_dict[key],columns=cols)
        df['dollar_per_ton'] = df['money'] / df[['weight', 'vol']].max(axis=1)
        df['full_load']= 'available'
        origin = df.iloc[0]['origin']
        dest = df.iloc[0]['dest']
        
        
        limit = 1
        while limit != 30:
            
            df_available = df.loc[df['full_load']=='available']
            if df_available.shape[0] == 0:
                break
            
            load_value = [0,[]]
        
            total_weight = df['weight'].sum()
            total_vol = df['vol'].sum()
        
            if  total_weight <= ship_cargo[0] and total_vol <= ship_cargo[1]:
                load_value[0] = df['money'].sum()
                load_value[1] = df['id'].values.tolist()
                
                full_ship_dict[full_load_count] = [origin, dest, load_value[0]]       
                full_ship_dict_contractinfo[full_load_count] = load_value[1]
                full_load_count = full_load_count + 1
                
                break
        
            else:
                df_sorted = df_available.sort_values(['dollar_per_ton'], ascending = [False])
                df_filtered = df_sorted.iloc[0:10]
                size = df_filtered.shape[0]
                combo = []
                for combo_var in range(size):
                    combo_var = combo_var +1
                    combo.extend(list(itertools.combinations(df_filtered.index, combo_var)))
        
                for single_combo in combo:
                    combo_df = df_filtered.loc[list(single_combo)]
                    if combo_df['weight'].sum() <= ship_cargo[0] and combo_df['vol'].sum() <= ship_cargo[1] and combo_df['money'].sum() > load_value[0]:
                        load_value[0] = combo_df['money'].sum()
                        load_value[1] = list(single_combo)
                        
                df.loc[load_value[1],'full_load'] = limit
                load_value[1] = df_available.loc[load_value[1],'id'].values.tolist()    
        
                full_ship_dict[full_load_count] = [origin, dest, load_value[0]]       
                full_ship_dict_contractinfo[full_load_count] = load_value[1]
                full_load_count = full_load_count + 1
            
            
        
            limit = limit+1

    return full_ship_dict, full_ship_dict_contractinfo


# runs the empty back funct and halves it since it does round trips
# ship cost needs to be accurate and taken out later so that the empty back calc finds the best fuel use
def flight_time(origin ,dest, ship):
    if origin == dest:
        return [0,0]
    shipcheck = Modules.Calcs.Shipping.shipping_optimizer_emptyback(ship, 12000, origin, dest)
    shipcheck = pd.DataFrame(shipcheck)

    return [(1/(shipcheck.iloc[0]['loads daily'])) / 2 , shipcheck.iloc[0]['empty back cost'] / 2]


#used with the optimizer to move forward one contract
def flight_combo(end, current_days, current_money, index, ship, loads, maxdays, full_ship_dict):
    
    current_origin = index[-1]
    current_origin = full_ship_dict[current_origin][1]
    load_one_forward = []
    load_one_complete = []

    for load in loads:
        if load in index:
            continue

        temp_days = current_days       
        temp_dest, next_dest, next_money = full_ship_dict[load] 
        temp_money = current_money + next_money
        temp_index = index[:]
        temp_index.append(load)

        temp_flight = flight_time(current_origin, temp_dest, ship)
        temp_flight2 = flight_time(temp_dest, next_dest, ship)

        temp_days = temp_days + temp_flight[0] + temp_flight2[0]
        temp_money = temp_money - (temp_flight[1] + temp_flight2[1])

        end_flight_check = flight_time(next_dest, end, ship)

        if temp_days + end_flight_check[0] > maxdays:
            continue
        else:
            load_one_forward.append([temp_days,'pending',temp_money,temp_index])
            load_one_complete.append([temp_days,'complete',temp_money,temp_index])

    return load_one_forward, load_one_complete


# outputs dataframe with tier1 full trips sorted by cost
# needs to be used in conjunction with the shipdict by ship type contract info
# and id dict to back into all the contracts for each leg
def shipment_optimizer(start, end, ship, full_ship_dict):

    maxdays = 3
    flight_combos = []
    pending_combos = []
    combo_template = ['days','pending','total_cash','index']
    loads = []

    for load in full_ship_dict.keys():
        
        temp_dest, next_dest, next_money = full_ship_dict[load]
        
        temp_flight = flight_time(start, temp_dest, ship)
        temp_flight2 = flight_time(temp_dest, next_dest, ship)
        
        temp_days = temp_flight[0] + temp_flight2[0]
        temp_money = next_money - (temp_flight[1] + temp_flight2[1])
        
        end_flight_check = flight_time(next_dest, end, ship)
        
        if temp_days + end_flight_check[0] > maxdays:
            continue
        else:
            loads.append(load)
            flight_combos.append([temp_days,'complete',temp_money,[load]])
            pending_combos.append([temp_days,'pending',temp_money,[load]])

    limit = 0
    while limit != 15:
        new_pending = []
        for pend in pending_combos:
            temp_pend, temp_complete = flight_combo(end, pend[0], pend[2], pend[3], ship, loads, maxdays, full_ship_dict)
            if temp_pend == []:
                break
            for tp in temp_pend:
                new_pending.append(tp)
            for tc in temp_complete:
                flight_combos.append(tc)
                
        if temp_pend == []:
            break
        pending_combos = new_pending
        limit = limit + 1

    temp_flight_combos = []
    for x in flight_combos:
        load = x[3]
        load = load[-1]
        temp_dest, next_dest, next_money = full_ship_dict[load]
        end_flight_check = flight_time(next_dest, end, ship)
        days = x[0]+end_flight_check[0]
        money = x[2]-end_flight_check[1]
        temp_flight_combos.append([days, money+days*12000,x[3]])
    no_contract = flight_time(start, end, ship)
    temp_flight_combos.append([no_contract[0],-no_contract[1],'no_contracts'])

    df_fc = pd.DataFrame(temp_flight_combos, columns=['days','money','contract_index'])
    df_fc['money per day'] = df_fc['money'] / df_fc['days']
    
    return df_fc.sort_values(['money per day'],ascending = False)

