import numpy as np
import matplotlib.pyplot as plt
import datetime
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms import QAOA, SamplingVQE, NumPyMinimumEigensolver
from qiskit_algorithms.utils import algorithm_globals
from qiskit.circuit.library import TwoLocal
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_finance.data_providers import RandomDataProvider
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_aer.primitives import Sampler

# --- 1. Define the Problem Data ---
num_assets = 4  # Number of assets (equals number of qubits)
seed = 123
algorithm_globals.random_seed = seed

# Generate expected return (mu) and covariance matrix (sigma) from random data
stocks = [f"TICKER{i}" for i in range(num_assets)]
data = RandomDataProvider(
    tickers=stocks,
    start=datetime.datetime(2020, 1, 1),
    end=datetime.datetime(2020, 1, 30),
    seed=seed,
)
data.run()
mu = data.get_period_return_mean_vector()
sigma = data.get_period_return_covariance_matrix()

# Optimization parameters
risk_factor = 0.5  # Qiskit's 'q' parameter: risk-aversion coefficient
budget = num_assets // 2  # Number of assets to select (e.g., 2 out of 4)
penalty = num_assets      # Scaling for the budget constraint penalty

# --- 2. Formulate as a Quadratic Program (QP) ---
portfolio = PortfolioOptimization(
    expected_returns=mu,
    covariances=sigma,
    risk_factor=risk_factor,
    budget=budget,
)

# Convert the classical portfolio problem into a Quadratic Program (QP)
qp = portfolio.to_quadratic_program()
print(f"Quadratic Program:\n{qp.prettyprint()}")

# --- 3. Solve using a Quantum Algorithm (QAOA) ---
# The MinimumEigenOptimizer converts the QP to an Ising Hamiltonian and solves it.

# Define the classical optimizer for the QAOA/VQE
cobyla = COBYLA(maxiter=250)

# 3a. Solve using Quantum Approximate Optimization Algorithm (QAOA)
qaoa_mes = QAOA(sampler=Sampler(), optimizer=cobyla, reps=3) # reps=3 is the circuit depth
qaoa = MinimumEigenOptimizer(qaoa_mes)
qaoa_result = qaoa.solve(qp)

# --- 4. Post-Process and Print Results ---
def print_result(result, name):
    selection = result.x
    value = result.fval
    # The 'x' vector is a binary selection: 1 means select the asset, 0 means don't.
    selected_assets = [stocks[i] for i, x in enumerate(selection) if x == 1]
    
    # Calculate classical return and risk for the resulting portfolio
    weights = selection / np.sum(selection) if np.sum(selection) > 0 else np.zeros(num_assets)
    port_return = np.dot(mu, weights)
    port_risk = np.sqrt(np.dot(weights.T, np.dot(sigma, weights)))

    print(f"\n--- {name} Result ---")
    print(f"Selected Assets: {selected_assets}")
    print(f"Optimal Binary Selection: {selection}")
    print(f"Objective Value: {value:.4f}")
    print(f"Portfolio Return (Approx): {port_return:.4f}")
    print(f"Portfolio Risk (Approx): {port_risk:.4f}")

print_result(qaoa_result, "QAOA Quantum Portfolio")

# --- Bonus: Classical Reference Solution (NumPy Minimum Eigensolver) ---
# This uses a classical exact method to find the true optimal solution.
exact_solver = NumPyMinimumEigensolver()
exact_optimizer = MinimumEigenOptimizer(exact_solver)
exact_result = exact_optimizer.solve(qp)
print_result(exact_result, "Classical Exact Solver")
