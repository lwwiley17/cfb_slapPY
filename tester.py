import pandas as pd
from hudl_namespace import *
from pbp_parser import quarters, name_dict
from play_maker_hudl import game_builder
game_info = game_builder(quarters,name_dict)
game = game_info['game']
state = game_info['state']
for drive in game:
    for i in range(len(drive)-1):
        if drive[-(i+1)][play_type] in (type_run, type_pass):
            drive[-(i+1)].update({drive_end:drive[0][drive_end]})
            break
plays = [play for drive in game for play in drive if play != drive[0]]
dex = pd.Series(list(range(1,len(plays)+1)),name = 'Play #')
df = pd.DataFrame(plays, index = dex)

def odk_maker(play,perspective):
    if play[play_type] in (type_run, type_pass, timeout):
        if play[possession] == perspective:
            return('O')
        else: 
            return('D')
    else:
        return('K')
        
def od_score_tol(play):
    if play[possession] == play[home_abbr]:
        return([play[home_score],play[away_score],play[home_tol],play[away_tol]])
    else:
        return([play[away_score],play[home_score],play[away_tol],play[home_tol]])
        

perspective = input('Perspective: {} or {}?'.format(name_dict[home_abbr],name_dict[away_abbr]))
if perspective not in name_dict.values():
    perspective = name_dict[home_abbr]
df[odk] = df.apply(odk_maker, axis=1, args=(perspective,))
df[[off_score,def_score,off_tol,def_tol]] = df.apply(od_score_tol, axis=1, result_type='expand')
if perspective == name_dict[home_abbr]:
    df[pers_score_diff] = df[score_diff]
    df[pers_tol] = df[home_tol]
else:
    df[pers_score_diff] = df[score_diff]*-1
    df[pers_tol] = df[away_tol]

df.to_csv('psu_test.csv')