import pandas as pd
import math
from Modules.Calcs.JumpCalc import JumpDict
from Modules.Transformers.StaticPairs import stl_pairs
from Modules.Transformers.StaticSystemStars import system_stars
from Modules.Transformers.abc_planet_system_keygen import abc_key
from Modules.FIO.FioAllPlanetsDict import FioNaturalPlanets


stl_pairs_dict = stl_pairs()
system_stars = system_stars()
planets_data = FioNaturalPlanets()
cxcode = ['BEN','MOR','HRT','ANT','ARC','HUB']
jump_dict = JumpDict()


# holds all stats by shiptype
class Ship:
    def __init__(self, ship_type):


        #sf sf fuel 
        #stl_ sf fuel
        #stl_R pairs combined oribal axis

        if ship_type == 'LCB':
            
            # STL Normal Burn roughly 170 sf in app/dep
            self.sf_hours_norm = 2.56
            self.sf_norm = 410
            self.cx_discount_hours_norm = 0.575
            self.cx_discount_sf_norm = 119
            
            # STL Low Burn  roughly 110 sf in app/dep
            self.sf_hours_low = 4
            self.sf_low = 235
            self.cx_discount_hours_low = 2.29
            self.cx_discount_sf_low = 60
           
            # STL only Flight info
            self.stl_35 = 209
            self.stl_35_r = 300
            self.stl_15 = 307
            self.stl_15_r = 600
            self.stl_1 = 489
            self.stl_1_r = 1500
            
        elif ship_type == 'WCB':

            # STL Normal Burn roughly 196 sf in app/dep
            self.sf_hours_norm = 2.73
            self.sf_norm = 454
            self.cx_discount_hours_norm = 1
            self.cx_discount_sf_norm = 224
            
            # STL Low Burn  roughly 110 sf in app/dep
            self.sf_hours_low = 4.11
            self.sf_low = 283
            self.cx_discount_hours_low = 2
            self.cx_discount_sf_low = 60
            
            # STL Flight info
            self.stl_35 = 209*1.1
            self.stl_35_r = 300
            self.stl_15 = 307*1.1
            self.stl_15_r = 600
            self.stl_1 = 489*1.1
            self.stl_1_r = 1100
        elif ship_type == 'VCB':

            # STL Normal Burn roughly 196 sf in app/dep
            self.sf_hours_norm = 2.06
            self.sf_norm = 386
            self.cx_discount_hours_norm = 0.35
            self.cx_discount_sf_norm = 200
            
            # STL Low Burn  roughly 110 sf in app/dep
            self.sf_hours_low = 2.58
            self.sf_low = 283
            self.cx_discount_hours_low = 2
            self.cx_discount_sf_low = 100


            #STL Flight info
            self.stl_35 = 209*.8
            self.stl_35_r = 300
            self.stl_15 = 307*.8
            self.stl_15_r = 600
            self.stl_1 = 489*.8
            self.stl_1_r = 1500



        elif ship_type == 'STD':

            # STL Normal Burn roughly 125 sf in app/dep
            self.sf_hours_norm = 2
            self.sf_norm = 302
            self.cx_discount_hours_norm = 0.75
            self.cx_discount_sf_norm = 100
            
            # STL Low Burn  roughly 75 sf in app/dep
            self.sf_hours_low = 2.71
            self.sf_low = 192
            self.cx_discount_hours_low = 1
            self.cx_discount_sf_low = 50


            #STL Flight info
            self.stl_35 = 209*.6
            self.stl_35_r = 300
            self.stl_15 = 307*.6
            self.stl_15_r = 600
            self.stl_1 = 489*.6
            self.stl_1_r = 1500


            

    def get_attributes(self):
        return self.sf_hours_norm, self.sf_hours_low, self.sf_norm, self.sf_low, self.cx_discount_hours_norm, self.cx_discount_sf_norm, self.stl_35, self.stl_35_r, self.stl_15, self.stl_15_r, self.stl_1, self.stl_1_r


# stats for FTL engines by shiptype and given gw
def ff_stats(ship,gw):
    max_parsec_hr = 5.1
    ff_parsec_4800gw = 14.288758698493655
    charge_time = gw * 0.025 / 7200  # per hour
    if gw < 4800:
        parsec_per_hour = gw * max_parsec_hr / 7200 + 0.7070473423355021 * ((2800 - (gw-2000))/2800)
        if gw < 2000:
            parsec_per_hour = parsec_per_hour + 0.1 * ((800 - (gw-1200))/800)
        if gw < 1200:
            return 'error gw too low'
    else:
        parsec_per_hour = gw * max_parsec_hr / 7200
    ff_per_parsec = gw * ff_parsec_4800gw / 4800

    if ship == 'WCB':
        vol_bonus = 1632 / 2682
        parsec_per_hour = parsec_per_hour / vol_bonus
        if gw > 4800:
            bonus = 0.285
            bonus_ratio = gw / 7200
            bonus = bonus * bonus_ratio
            parsec_per_hour = parsec_per_hour * (1+bonus)

    if ship == 'STD':
        charge_time = gw * 0.125 / 7200
        vol_bonus = 963 / 2682
        parsec_per_hour = parsec_per_hour / vol_bonus

    if ship == 'VCB':
        vol_bonus = 3732 / 2682
        parsec_per_hour = parsec_per_hour / vol_bonus
    
    return charge_time, parsec_per_hour, ff_per_parsec


# calc for STL only flights using the planets oribtal axis as a weight
# pairs are assumed very fast if they are both close to the sun
# pairs assumed to have higher deviations in flight times the further from the sun and flights might be much shorter than calc in ideal windows
# pairs that exceed a certain orbital axis use a 1 load daily FTL round trip
def stl(ship, system, start, end):

    my_ship = Ship(ship)

    stl_sf = 0
    stl_loads = 0
    stl_ff = 0

    for pair in stl_pairs_dict[system]:
        if pair[0] == start and pair[1] == end:
            parval = pair[2]
        if pair[1] == start and pair[0] == end:
            parval = pair[2]

    if parval <= my_ship.stl_35_r:
        stl_sf = my_ship.stl_35 * 1.9
        stl_loads = 3.5
        
    elif parval <= my_ship.stl_15_r:
        stl_sf = my_ship.stl_15 * 1.9
        stl_loads = 1.5
        
    elif parval <= my_ship.stl_1_r:
        stl_sf = my_ship.stl_1 * 1.9
        stl_loads = 1
        
    else:                       #greater than stl_1_r
        stl_sf = 274*3.8
        stl_ff = 60*4
        stl_loads = 1

    return stl_loads, stl_ff, stl_sf



# main shipping calc that will revert to the STL calc if in the same system
# sampled planets appear to increase in STL hours on high grav planets esp gas giants and fuel is added for these
# sampled cx don't have full STL flights and a large portion of time and fuel removed from the calc
# fuel use and shipping windows are returned for round trips
def shipping_lpd(ship, start, end, gw, sf_burn): 

    if start == end:
        return 'error same planet'

    my_ship = Ship(ship)
    
    ftl_loads = 0
    ff_used = 0
    sf_used = 0
    grav_sf = 0
    
    cxd = 0
    if start in cxcode:
        cxd = 1
        
    if end in cxcode:
        cxd = cxd + 1
        
    
    if start not in cxcode:
        grav_sf = grav_sf + (planets_data[start]['Gravity']-1)*66
    if end not in cxcode:
        grav_sf = grav_sf + (planets_data[end]['Gravity']-1)*66
    
    sys1 = system_stars[start]
    sys2 = system_stars[end]

    if sys1 == sys2:
        return stl(ship, sys1, start, end)

    par = jump_dict[abc_key(sys1,sys2)][0]
    jumps = jump_dict[abc_key(sys1,sys2)][1]

    charge_time, parsec_per_hour, ff_per_parsec = ff_stats(ship,gw)    
    
    ff_used = ff_per_parsec * par
    ff_hours = par / parsec_per_hour
    charge_hours = charge_time * jumps
    
    if sf_burn == 'norm':
        sf_used = my_ship.sf_norm
        sf_hours = my_ship.sf_hours_norm
        sf_hours = sf_hours - my_ship.cx_discount_hours_norm * cxd
        sf_used = sf_used - my_ship.cx_discount_sf_norm * cxd

    if sf_burn == 'low':
        sf_used = my_ship.sf_low
        sf_hours = my_ship.sf_hours_low
        sf_hours = sf_hours - my_ship.cx_discount_hours_low * cxd
        sf_used = sf_used - my_ship.cx_discount_sf_low * cxd
        
    sf_used = sf_used + grav_sf
    hours = sf_hours + ff_hours
    
    if hours <= 3:
        ftl_loads = 3.5
        ff_used = ff_used * 2
        sf_used = sf_used * 1.9
        return ftl_loads, ff_used, sf_used, ff_hours, par, parsec_per_hour;
    if hours <= 6:
        ftl_loads = 1.5
        ff_used = ff_used * 2
        sf_used = sf_used * 1.9
        return ftl_loads, ff_used, sf_used, ff_hours, par, parsec_per_hour;
    if hours <= 11:
        ftl_loads = 1
        ff_used = ff_used * 2
        sf_used = sf_used * 1.9
        return ftl_loads, ff_used, sf_used, ff_hours, par, parsec_per_hour;
    if hours > 11:
        ftl_loads = 1/(math.floor((hours-1)/12) + 1)   ## 1 hr buffer 1/multiple of 12hrs gives loads
        ff_used = ff_used * 2
        sf_used = sf_used * 1.9
        return ftl_loads, ff_used, sf_used, ff_hours, par, parsec_per_hour;

# goal is to compare the time cost and fuel cost to find the best flight
# a list of combinations of flights are returned starting at 7200 gw and going down 400 until 1200 gw
# stl is tested for a low and normal fuel use at every gw
# combinations are ranked using fuel cost plus ship time given the daily value. the lowest value is the best value
def shipping_optimizer_emptyback(ship, ship_value_daily, start, end):
    
    max_gw = 7200
    max_ff = 4000
    min_gw = 1200
    dollar_per_sf = 14.79141344
    dollar_per_ff = 15.1124692
    
    gw_used = 7200
    combo_list = []

    while gw_used >= 1200:
        sf_multiplier = 1
        needs_refuel = 'No'
        temp_norm = shipping_lpd(ship, start, end, gw_used, 'norm')

        dollars = ship_value_daily / temp_norm[0] + dollar_per_ff * temp_norm[1] + dollar_per_sf * temp_norm[2]
        
        if temp_norm[1] > max_ff:  #checks fuel use and continues if over max tank
            gw_used = gw_used - 400
            
            if gw_used == 1200 and combo_list == []:                                             #checks if a refeul is required at min gw. 
                combo_list.append([dollars+ ship_value_daily + 2*(dollar_per_sf * temp_norm[2]), #increases cost by 1 day and extra sf for landing
                                   1/(1/temp_norm[0] +1),                                        # adds 1 day to days per load and converts back to loads per day
                                    gw_used,
                                   'low_sf_burn',
                                   'Yes'])
                break
            continue
        
        combo_list.append([dollars,temp_norm[0],gw_used,'norm_sf_burn','no'])
        
        temp_low = shipping_lpd(ship, start, end, gw_used, 'low')
        dollars = ship_value_daily / temp_low[0] + dollar_per_ff * temp_low[1] + dollar_per_sf * temp_low[2]
        combo_list.append([dollars,temp_low[0],gw_used,'low_sf_burn','no'])

        gw_used = gw_used - 400



    col_des = ['empty back cost', 'loads daily', 'gw', 'sf_burn','refuel_midway']
    df = pd.DataFrame(combo_list, columns=col_des)
    df_sorted = df.sort_values(['empty back cost'], ascending = [True])
    
    return df_sorted
