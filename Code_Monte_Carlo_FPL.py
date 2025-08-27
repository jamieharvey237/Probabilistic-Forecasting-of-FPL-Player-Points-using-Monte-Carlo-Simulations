import numpy as np

def points_fwd(xg, xa): #Points calculation for a forward
    goals = np.random.poisson(xg)
    assists = np.random.poisson(xa)
    points = (goals * 6) + (assists * 3) + 2 # constant +2 for appearance
    return points

haaland_xg = 0.75 #Data from "Understat"
haaland_xa = 0.11
expected_points = (haaland_xg * 6) + (haaland_xa * 3) + 2

# Run simulations for different values of n
n_sims = [10, 50, 100, 500, 1000, 5000, 10000, 100000, 1000000,5000000]
sim_avg = np.zeros(len(n_sims))

for n in range(len(n_sims)):
    sim_points= [points_fwd(haaland_xg, haaland_xa) for _ in range(n_sims[n])]
    sim_average_points = np.mean(sim_points)
    sim_avg[n]=sim_average_points
    error=abs(sim_avg[n]-expected_points)*100/expected_points
    print("N=%i, Simulated Points = %.2f, Expected Points = %.2f, Error: %.1f%%" %(n_sims[n],sim_avg[n],expected_points, error))

# Plot the results
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(n_sims, sim_avg, 'b-', label='Simulated Average')
plt.axhline(y=expected_points, color='r', linestyle='--', label='Analytical Expected Value')
plt.xscale('log') # Use a log scale to see the early trials clearly
plt.xlabel('Number of Simulations (Log Scale)')
plt.ylabel('Points Scored')
plt.title('Monte Carlo Convergence: Simulated vs. Expected FPL Points for Erling Haaland')
plt.legend()
plt.grid(True)
plt.show()
