import numpy as np

#Define Fixture Difficulty Rating----------------------------------
#introducing a coefficient which alters expected points based on quality of opposition using FDR
FDR_coefficient=np.array([1.2,1,0.95,0.85])

#Points calculators-------------------------------------------------
def points_fwd(xg, xa, FDR): #Points calculation for a forward
    goals = np.random.poisson(xg)
    assists = np.random.poisson(xa)
    points = FDR_coefficient[FDR-2]*((goals * 6) + (assists * 3) + 2) # constant +2 for appearance
    return points

def points_mid(xg, xa, xcs, FDR): #Assumption of no DC for attacking midfielders for now
    goals = np.random.poisson(xg)
    assists = np.random.poisson(xa)
    clean_sheet = np.random.binomial(1, p=xcs) #binomial dist for success/failure outcomes
    points = FDR_coefficient[FDR-2]*((goals * 5) + (assists * 3) + (1*clean_sheet) + 2) # constant +2 for appearance
    return points


#Player stats---------------------------------------------------------
#haaland_xg = 0.75 #Data from "Footystats"
#haaland_xa = 0.11

salah_xg=0.72
salah_xa=0.41
liv_xcs=14/38 #expected clean sheets
liv_gw_fdr=4 #chelsea gameweek fixture difficulty rating

palmer_xg=0.5
palmer_xa=0.3
che_xcs= 10/38
che_gw_fdr=3 #chelsea gameweek fixture difficulty rating

# Run simulations for different values of n
n_sims = 1000000

#Create set of points returns
salah_sim_points = np.array([points_mid(salah_xg,salah_xa,liv_xcs,liv_gw_fdr) for _ in range(n_sims)])
palmer_sim_points = np.array([points_mid(palmer_xg,palmer_xa,che_xcs,che_gw_fdr) for _ in range(n_sims)])

#Calculate key metrics to decide best captain -----------------------------------------
salah_metric_wins=0 #counter for how many categories each player wins in
palmer_metric_wins=0

# 1. Highest Average Points
salah_avg=salah_sim_points.mean()
palmer_avg=palmer_sim_points.mean()
if salah_avg>palmer_avg:
    salah_metric_wins+=1
    print("Higher points average: Salah")
else:
    palmer_metric_wins+=1
    print("Higher points average: Palmer")
    
#2. Likelihood of "haul"
haul=10
salah_haul=np.sum(salah_sim_points>=haul)
palmer_haul=np.sum(palmer_sim_points>=haul)
if salah_haul>palmer_haul:
    salah_metric_wins+=1
    print("Higher haul count: Salah")
elif salah_haul<palmer_haul:
    palmer_metric_wins+=1
    print("Higher haul count: Palmer")
else:
    print("Equal hauls")

#3. Likelihood of "blank"
blank=2
salah_blank=np.sum(salah_sim_points<=blank)
palmer_blank=np.sum(palmer_sim_points<=blank)
if salah_blank>palmer_blank:
    palmer_metric_wins+=1
    print("Lower blank count: Palmer")
elif salah_blank<palmer_blank:
    salah_metric_wins+=1
    print("Lower blank count: Salah")
else:
    print("Equal blanks")
    
#4. Volatility of points (riskiness)---------------------------------------
salah_std=np.std(salah_sim_points)
palmer_std=np.std(palmer_sim_points)
if salah_std>palmer_std:
    palmer_metric_wins+=1
    print("Less volatile: Palmer")
elif salah_std<palmer_std:
    salah_metric_wins+=1
    print("Less volatile: Salah")
else:
    print("Equal volatility")
    
#5. Risk adjusted points return metric------------------------------------
salah_risk_adj_points=salah_avg/salah_std
palmer_risk_adj_points=palmer_avg/palmer_std

if salah_risk_adj_points>palmer_risk_adj_points:
    salah_metric_wins+=1
    print("Best risk-adjusted points return: Salah")
elif salah_risk_adj_points<palmer_risk_adj_points:
    palmer_metric_wins+=1
    print("Best risk-adjusted points return: Palmer")
else:
    print("Equal risk-adjusted points return")
    
#Best captain based on overall metric wins---------------------------------
if salah_metric_wins>palmer_metric_wins:
    print("Captain Selection: Salah")
elif salah_metric_wins<palmer_metric_wins:
    print("Captain Selection: Palmer")
else:
    if salah_avg>palmer_avg:
        print("Captain Selection: Salah")
    elif palmer_avg>salah_avg:
        print("Captain Selection: Palmer")
    else:
        print("Captain Selection Inconclusive")



