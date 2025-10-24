import numpy as np
import datetime

# Qiskit Libraries
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_finance.data_providers import RandomDataProvider
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_aer.primitives import Sampler

# --- 1. Define Problem Inputs ---
num_assets = 4  # The number of assets (and qubits)
seed = 123
algorithm_globals.random_seed = seed

# Generate mock financial data (Expected Returns & Covariances)
data = RandomDataProvider(
    tickers=[f"TICKER{i}" for i in range(num_assets)],
    start=datetime.datetime(2020, 1, 1),
    end=datetime.datetime(2020, 1, 30),
    seed=seed,
)
data.run()
mu = data.get_period_return_mean_vector()    # Expected returns
sigma = data.get_period_return_covariance_matrix() # Covariance matrix

# Optimization parameters
risk_factor = 0.5   # Risk aversion (higher = more risk-averse)
budget = 2          # Maximum number of assets to select

# --- 2. Formulate as a Quadratic Program (QP) ---
# The classical Mean-Variance problem is structured for quantum conversion.
portfolio = PortfolioOptimization(
    expected_returns=mu,
    covariances=sigma,
    risk_factor=risk_factor,
    budget=budget,
)
qp = portfolio.to_quadratic_program()

# --- 3. Solve with Quantum Approximate Optimization Algorithm (QAOA) ---
print("--- Starting Quantum Optimization (QAOA) ---")

# 3a. Setup the classical optimizer (for the hybrid loop)
cobyla = COBYLA(maxiter=250)

# 3b. Setup the QAOA Minimum Eigensolver
# Sampler is used to execute the quantum circuit and get results.
qaoa_mes = QAOA(sampler=Sampler(), optimizer=cobyla, reps=3)
qaoa = MinimumEigenOptimizer(qaoa_mes)

# 3c. Solve the problem
qaoa_result = qaoa.solve(qp)

# --- 4. Post-Process and Display Results ---
def print_portfolio_result(result, name):
    selection = result.x
    selected_assets = [f"TICKER{i}" for i, x in enumerate(selection) if x == 1]
    
    # Calculate performance of the selected portfolio
    weights = selection / np.sum(selection) if np.sum(selection) > 0 else np.zeros(num_assets)
    port_return = np.dot(mu, weights)
    port_risk = np.sqrt(np.dot(weights.T, np.dot(sigma, weights)))

    print(f"\n✅ {name} Result:")
    print(f"   Selected Assets (Binary): {selection.astype(int)}")
    print(f"   Assets Chosen: {selected_assets}")
    print(f"   Objective Value (Cost): {result.fval:.4f}")
    print(f"   Portfolio Return (Approx): {port_return:.4f}")
    print(f"   Portfolio Risk (Std. Dev.): {port_risk:.4f}")

print_portfolio_result(qaoa_result, "QAOA Quantum Portfolio")

# --- Bonus: Classical Exact Solver for Verification ---
# Use a classical solver to find the true optimal solution for comparison.
exact_solver = NumPyMinimumEigensolver()
exact_optimizer = MinimumEigenOptimizer(exact_solver)
exact_result = exact_optimizer.solve(qp)

print_portfolio_result(exact_result, "Classical Exact Portfolio")
