

def PAD_Version(Version_List, count =0):              
    PAD_Key = 'PAD_'                        
    for item in Version_List:
        valed_item = PAD_Version_Validation(count,item)  
        if valed_item == 'failed val':       
            return 'failed val'             
        count = count + 1                    
        PAD_Key = PAD_Key+'V'+str(item)      
    return PAD_Key+'V'                      
                                             
def PAD_Version_Check(RunKey,RunVar):       
                                            
    Var_Positions = []                      
    
    for var in range(len(RunKey)):
        if RunKey[var] == 'V':
            Var_Positions.append(var)
            
    Start = Var_Positions[RunVar]
    End = Var_Positions[RunVar+1]
    RunVar_Version = RunKey[Start+1:End]
    
    Varname = {
                0: 'Starting_PAD',
                1: 'Static',
                2: 'COG',
                3: 'COG_Miss',
                4: 'Outputs',
                5: 'Base_Amort',
                6: 'Ship_Daily_Cost',
                7: 'Available_Ship_Types',
                8: 'Natural_Planets'
    }
    
    return ['PAD',Varname[RunVar],RunVar_Version]

def PAD_Version_Validation(list_position,val):
    
    increasing_int = [0,1,2,3,4,7,8]
    
    if list_position in increasing_int:
        
        if val %1 == 0 and val >= 0 and val <= 999:
            return val
        
    elif list_position == 5 and val <= 720 and val %15 == 0:
        return val

    elif list_position == 6 and val <= 2000 and val %100 == 0: 
        return val
            
    return 'failed val'

#0 Starting_PAD        - enter version from old pad
#1 Static              - Starting at version 1 and increasing +1
#2 COG                 - Starting at version 1 and increasing +1
#3 COG_Miss            - Starting at version 1 and increasing +1, 0 for none
#4 Outputs             - Starting at version 1 and increasing +1
#5 Base_Amort (days)   - enter days as int 0-720 increments of 15, 30/360
#6 Ship_daily_Cost     - increments of 100 FF, max 2000
#7 Available_Ship_type - Starting at version 1 and increasing +1
#8 Natural_Planets     - Starting at version 1 and increasing +1