import numpy as np

# Run simulations for different values of n
n_sims = 1000000

#Player stats---------------------------------------------------------
#replace with data frame at future stage
haaland_xg = 0.75 
haaland_xa = 0.11
haaland_pos="FWD"
mci_xcs=12/38
mci_gw_fdr=3

salah_xg=0.72
salah_xa=0.41
salah_pos="MID"
liv_xcs=14/38 #expected clean sheets
liv_gw_fdr=4 #chelsea gameweek fixture difficulty rating

palmer_xg=0.5
palmer_xa=0.3
palmer_pos="MID"
che_xcs= 10/38
che_gw_fdr=3 #chelsea gameweek fixture difficulty rating

#Points calculators-------------------------------------------------
def points_calc(pos,xg,xa,xcs,FDR):
    FDR_coefficient=np.array([1.2,1,0.95,0.85]) # Can be edited to be more conservative
    
    goals = np.random.poisson(xg)
    assists = np.random.poisson(xa)
    clean_sheet = np.random.binomial(1, p=xcs) #binomial dist for success/failure outcomes
    
    if pos == "FWD":
        points = round(FDR_coefficient[FDR-2]*((goals * 4) + (assists * 3) + 2)) # constant +2 for appearance
    elif pos == "MID":
        points = round(FDR_coefficient[FDR-2]*((goals * 5) + (assists * 3) + (1*clean_sheet) + 2)) # constant +2 for appearance
    elif pos == "DEF":
        points = round(FDR_coefficient[FDR-2]*((goals * 6) + (assists * 3) + (4*clean_sheet) + 2)) # constant +2 for appearance
    elif pos == "GKP":
        points = round(FDR_coefficient[FDR-2]*((goals * 10) + (assists * 3) + (4*clean_sheet) + 2)) # constant +2 for appearance
    else:
        "Error in calculating points"
    return points
        
def captain_selector(p1, p1_pos, xg_p1, xa_p1, xcs_p1, fdr_p1, p2, p2_pos, xg_p2, xa_p2, xcs_p2, fdr_p2): #need to put player names and position in "" string format
    p1_sim_points=np.array([points_calc(p1_pos,xg_p1,xa_p1,xcs_p1,fdr_p1) for _ in range(n_sims)])
    p2_sim_points=np.array([points_calc(p2_pos,xg_p2,xa_p2,xcs_p2,fdr_p2)  for _ in range(n_sims)])
    
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

captain=captain_selector("SALAH", salah_pos,salah_xg,salah_xa,liv_xcs,liv_gw_fdr,"PALMER", palmer_pos,palmer_xg,palmer_xa,che_xcs,che_gw_fdr)




