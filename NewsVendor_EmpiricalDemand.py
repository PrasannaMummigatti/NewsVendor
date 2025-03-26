import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  # For percentage formatting

# Parameters
unit_cost = 5  # Cost per unit
selling_price = 10  # Selling price per unit
stockout_cost_per_unit = 3  # Cost per unit of unsatisfied demand
excess_cost_per_unit = 2  # Cost per unit of unsold inventory
order_quantities = [i for i in range(10,200) if i%5==0]  # Different order quantities to test
#order_quantities = [i for i in range(10,200)]  # Different order quantities to test
simulations = 1000  # Number of demand simulations

# Example Empirical Demand Data (replace with real observed data)
empirical_demand_data = np.array([80, 95, 110, 130, 85, 90, 105, 125, 100, 115, 140, 75, 120, 135, 145, 70, 100, 110])

# Generate demand samples by resampling from empirical data
np.random.seed(0)
demand_data = np.random.choice(empirical_demand_data, size=simulations, replace=True)

# Compute empirical probability distribution
unique_values, counts = np.unique(demand_data, return_counts=True)
probabilities = counts / simulations  # Convert to probabilities
percentages = probabilities * 100  # Convert to percentage

# Compute Cumulative Distribution Function (CDF)
cumulative_probabilities = np.cumsum(probabilities)  # Cumulative sum

# Initialize results list
results = []

# Simulate for each order quantity
for Q in order_quantities:
    total_cost = 0
    total_revenue = 0
    total_profit = 0
    total_stockout_cost = 0
    total_excess_cost = 0
    
    for demand in demand_data:
        revenue = min(demand, Q) * selling_price
        cost = Q * unit_cost
        
        # Stockout cost (if demand > Q)
        stockout_cost = max(0, demand - Q) * stockout_cost_per_unit
        
        # Excess inventory cost (if Q > demand)
        excess_cost = max(0, Q - demand) * excess_cost_per_unit
        
        # Profit calculation including stockout and excess costs
        profit = revenue - cost - stockout_cost - excess_cost

        # Accumulate totals
        total_revenue += revenue
        total_cost += cost
        total_stockout_cost += stockout_cost
        total_excess_cost += excess_cost
        total_profit += profit
    
    # Store results
    results.append({
        'Order Quantity': Q,
        'Total Cost': total_cost,
        'Total Revenue': total_revenue,
        'Total Stockout Cost': total_stockout_cost,
        'Total Excess Cost': total_excess_cost,
        'Profit': total_profit
    })

# Convert results list to DataFrame
results_df = pd.DataFrame(results)

# Find the optimal order quantity (Q*) that gives the highest profit
optimal_Q = results_df.loc[results_df['Profit'].idxmax(), 'Order Quantity']
print(f"Optimal Order Quantity (Q*): {optimal_Q}")

# --------- PLOT 1: Empirical Demand Histogram & PMF ---------
"""""
plt.figure(figsize=(10, 6))
plt.ylim(0,0.15)
plt.xticks(np.arange(60, 160, 5))
plt.grid(False)
# Plot histogram
#plt.hist(demand_data, bins=len(empirical_demand_data), edgecolor='black', alpha=0.7, color='skyblue', density=True, label="Empirical Demand Histogram")

# Overlay Probability Mass Function (PMF) using stem plot
markerline, stemlines, baseline = plt.stem(unique_values, probabilities, linefmt='r-', markerfmt='ro', basefmt=" ")

# Style the PMF plot
plt.setp(stemlines, linewidth=1.5)
plt.setp(markerline, markersize=8)

# Label each probability value as a percentage
for x, y in zip(unique_values, percentages):
    plt.text(x, y / 100, f'{y:.1f}%', ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

# Show Optimal Q* Line
plt.axvline(optimal_Q, color='black', linestyle='dashed', linewidth=2, label=f'Optimal Q* = {optimal_Q}')

# Labels and formatting
plt.xlabel('Demand')
plt.ylabel('Probability')
plt.title('Empirical Demand Probability Mass Function (PMF) with Optimal Q*')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
"""
# --------- PLOT 2: Cost, Profit & Revenue vs. Order Quantity ---------
plt.figure(figsize=(10, 6))

# Plot Profit, Stockout Cost, Excess Cost, and Revenue
plt.plot(results_df['Order Quantity'], results_df['Profit'], marker='', linestyle='-', label="Profit", color='g')
plt.plot(results_df['Order Quantity'], results_df['Total Stockout Cost'], marker='', linestyle='--', label="Stockout Cost", color='r')
plt.plot(results_df['Order Quantity'], results_df['Total Excess Cost'], marker='', linestyle='-.', label="Excess Cost", color='b')
#plt.plot(results_df['Order Quantity'], results_df['Total Revenue'], marker='^', linestyle='-', label="Revenue", color='purple')

# Labels and legend
plt.xlabel('Order Quantity')
plt.ylabel('Cost / Profit / Revenue')
plt.title('Profit, Stockout Cost, Excess Cost  vs. Order Quantity')
plt.legend()
plt.grid(True)

# Find the maximum profit value
optimal_profit = results_df.loc[results_df['Order Quantity'] == optimal_Q, 'Profit'].values[0]

# Show Optimal Q* Vertical Line
plt.axvline(optimal_Q, color='black', linestyle='dashed', linewidth=2, label=f'Optimal Q* = {optimal_Q}')
# Show Optimal Profit Horizontal Line
plt.axhline(optimal_profit, color='gray', linestyle='dotted', linewidth=2, label=f'Optimal Profit = {optimal_profit:.2f}')


# Show plot
plt.show()

"""# --------- PLOT 3: Cumulative Distribution Function (CDF) ---------
plt.figure(figsize=(10, 6))

# Plot CDF
#plt.plot(unique_values, cumulative_probabilities, marker='o', linestyle='-', color='b', label='Empirical CDF')
plt.step(unique_values, cumulative_probabilities, where='post', linestyle='-', color='b', linewidth=2, label='Empirical CDF')

# Get the cumulative probability at Q*
Q_cdf_value = np.interp(optimal_Q, unique_values, cumulative_probabilities)

# Show Optimal Q* Lines
plt.axvline(optimal_Q, color='black', linestyle='dashed', linewidth=2, label=f'Optimal Q* = {optimal_Q}')
plt.axhline(Q_cdf_value, color='gray', linestyle='dotted', linewidth=2, label=f'P(D ≤ {optimal_Q}) = {Q_cdf_value:.2f}')

# Labels and formatting
plt.xlabel('Demand')
plt.ylabel('Cumulative Probability')
plt.title('Empirical Demand Cumulative Distribution Function (CDF) \n For per unit cost = 5, selling price = 10, stockout cost = 3, CR=0.625')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.show()
"""
# --------- PLOT 1: PMF & CDF Subplots ---------
# Get the cumulative probability at Q*
Q_cdf_value = np.interp(optimal_Q, unique_values, cumulative_probabilities)


fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# --- (A) Probability Mass Function (PMF) ---
#axes[0].hist(demand_data, bins=len(empirical_demand_data), edgecolor='black', alpha=0.7, color='skyblue', density=True, label="Empirical Demand Histogram")

# Overlay PMF using stem plot
markerline, stemlines, baseline = axes[0].stem(unique_values, probabilities, linefmt='r-', markerfmt='ro', basefmt=" ")

# Style the PMF plot
plt.setp(stemlines, linewidth=1.5)
plt.setp(markerline, markersize=8)

# Label each probability value as a percentage
for x, y in zip(unique_values, percentages):
    axes[0].text(x, y / 100, f'{y:.1f}%', ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

# Show Optimal Q* Line
axes[0].axvline(optimal_Q, color='black', linestyle='dashed', linewidth=2, label=f'Optimal Q* = {optimal_Q}')

# Format y-axis as percentages
axes[0].yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
axes[0].set_ylim(0,0.12)
# Labels & title
#axes[0].set_xlabel('Demand')
axes[0].set_ylabel('Probability (%)')
axes[0].set_title('Empirical Demand PMF and CDF with Optimal Q* For per unit cost = 5, selling price = 10, stockout cost = 3, CR=0.625',fontsize=10)
axes[0].legend()
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# --- (B) Cumulative Distribution Function (CDF) ---
axes[1].step(unique_values, cumulative_probabilities, where='post', linestyle='-', color='b', linewidth=2, label='Empirical CDF')

# Show Optimal Q* Lines
axes[1].axvline(optimal_Q, color='black', linestyle='dashed', linewidth=2, label=f'Optimal Q* = {optimal_Q}')
axes[1].axhline(Q_cdf_value, color='gray', linestyle='dotted', linewidth=2, label=f'P(D ≤ {optimal_Q}) = {Q_cdf_value:.2f}')
axes[1].set_ylim(0,1)
# Labels & title
axes[1].set_xlabel('Demand')
axes[1].set_ylabel('Cumulative Probability')
#axes[1].set_title('Empirical Demand CDF (Step Plot)',fontsize=15)
axes[1].legend()
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
