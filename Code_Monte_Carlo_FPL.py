import numpy as np
import requests as rq
import pandas as pd

# Run simulations for different values of n
n_sims = 1000000

#Import and clean FPL API data-----------------
#Player Data
api_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
api_data = rq.get(api_url).json()
player_data_full=pd.DataFrame(api_data['elements'])
player_data_full.set_index('web_name', inplace=True) #inplace=True simply replaces the data frame instead of making a copy (more efficient)
player_data = player_data_full[['element_type','expected_goals_per_90','expected_assists_per_90','expected_goals_conceded_per_90']].copy() #limit to relevant data
player_data.index.name = 'Name'
player_data.columns = ['Position','xG','xA','xGC'] #note for positions: 1=GKP, 2=DEF, 3=MID, 4=FWD
player_data['xCS'] = np.exp(-player_data['xGC']) #Calculating xCS based on xGC per 90 as no accurate xCS data per 90 at start of season


#Points calculators-------------------------------------------------
def predict_player_points(pos,xg,xa,xcs):
    
    goals = np.random.poisson(xg)
    assists = np.random.poisson(xa)
    clean_sheet = np.random.binomial(1, p=xcs) #binomial dist for success/failure outcomes
    
    if pos == 4: # FWD
        points = (goals * 4) + (assists * 3) + 2 # constant +2 for appearance
    elif pos == 3: # MID
        points = (goals * 5) + (assists * 3) + (1*clean_sheet) + 2 # constant +2 for appearance
    elif pos == 2: # DEF
        points = (goals * 6) + (assists * 3) + (4*clean_sheet) + 2 # constant +2 for appearance
    elif pos == 1: # GKP
        points = (goals * 10) + (assists * 3) + (4*clean_sheet) + 2 # constant +2 for appearance
    else:
        "Error in calculating points"
    return points
        
def captain_selector(p1, p1_pos, xg_p1, xa_p1, xcs_p1, fdr_p1, p2, p2_pos, xg_p2, xa_p2, xcs_p2, fdr_p2): #need to put player names and position in "" string format
    p1_sim_points=np.array([predict_player_points(p1_pos,xg_p1,xa_p1,xcs_p1,fdr_p1) for _ in range(n_sims)])
    p2_sim_points=np.array([predict_player_points(p2_pos,xg_p2,xa_p2,xcs_p2,fdr_p2)  for _ in range(n_sims)])
    
    p1_wins=0 #metric tally initialisation
    p2_wins=0
    
    # 1. Highest Average Points
    p1_avg=p1_sim_points.mean()
    p2_avg=p2_sim_points.mean()
    if p1_avg>p2_avg:
        p1_wins+=1
        print("Higher points average:", p1)
    else:
        p2_wins+=1
        print("Higher points average:", p2)
        
    #2. Likelihood of "haul"
    haul=10
    p1_haul=np.sum(p1_sim_points>=haul)
    p2_haul=np.sum(p2_sim_points>=haul)
    if p1_haul>p2_haul:
        p1_wins+=1
        print("Higher haul count:", p1)
    elif p1_haul<p2_haul:
        p2_wins+=1
        print("Higher haul count:", p2)
    else:
        print("Equal hauls")
    
    #3. Likelihood of "blank"
    blank=2
    p1_blank=np.sum(p1_sim_points<=blank)
    p2_blank=np.sum(p2_sim_points<=blank)
    if p1_blank>p2_blank:
        p2_wins+=1
        print("Lower blank count:", p2)
    elif p1_blank<p2_blank:
        p1_wins+=1
        print("Lower blank count:", p1)
    else:
        print("Equal blanks")
    
    #4. Volatility of points (riskiness)---------------------------------------
    p1_std=np.std(p1_sim_points)
    p2_std=np.std(p2_sim_points)
    if p1_std>p2_std:
        p2_wins+=1
        print("Less volatile:", p2)
    elif p1_std<p2_std:
        p1_wins+=1
        print("Less volatile:", p1)
    else:
        print("Equal volatility")
        
    #5. Risk adjusted points return metric------------------------------------
    p1_risk_adj_points=p1_avg/p1_std
    p2_risk_adj_points=p2_avg/p2_std

    if p1_risk_adj_points>p2_risk_adj_points:
        p1_wins+=1
        print("Best risk-adjusted points return:", p1)
    elif p1_risk_adj_points<p2_risk_adj_points:
        p2_wins+=1
        print("Best risk-adjusted points return:", p2)
    else:
        print("Equal risk-adjusted points return")
    
    #Best captain based on overall metric wins---------------------------------
    if p1_wins>p2_wins:
        captain=p1
        print("Captain Selection:", p1)
    elif p1_wins<p2_wins:
        captain=p2
        print("Captain Selection:", p2)
    else:
        if p1_avg>p2_avg:
            captain=p1
            print("Captain Selection:", p1)
        elif p2_avg>p1_avg:
            captain=p1
            print("Captain Selection:", p2)
        else:
            captain="N/A"
            print("Captain Selection Inconclusive")
    
    return captain

def predict_team_points(team_players, captain):
    team_players_pred_points = []
    for player in team_players:
        player_points=predict_player_points(player_data.loc[player,'Position'],player_data.loc[player,'xG'],player_data.loc[player,'xA'],player_data.loc[player,'xCS'])
        team_players_pred_points.append(player_points)
    
    captain_points=predict_player_points(player_data.loc[captain,'Position'],player_data.loc[captain,'xG'],player_data.loc[captain,'xA'],player_data.loc[captain,'xCS'])

    team_total_pred_points=sum(team_players_pred_points)+captain_points #captain has double points
    return team_total_pred_points

#team_id=int(input("Team ID? "))
team_players = ['M.Salah','Wood', 'Konsa', 'Digne' ]
team_total_pred_points=predict_team_points(team_players, 'M.Salah')
    
print(team_total_pred_points)





