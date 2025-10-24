# Use the Aer simulator (a high-performance classical simulator)
backend = Aer.get_backend('qasm_simulator')

# Run the circuit 1024 times (shots) to get probability distribution
job = backend.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

print("\n--- Quantum Database Query Result ---")
print(f"Counts (Shots=1024): {counts}")

# Plot the results
plot_histogram(counts).savefig("grover_search_result.png") 

# In a classical database search, you have a 1/4 chance to pick the right item 
# if you just guessed. Grover's increases the probability of the correct item to ~100%.

# The key '11' (the marked state) should have the highest count.
# The search result for the marked state |11> has been 'promoted' to nearly 100% probability.
# This demonstrates the quadratic speedup over classical unindexed search.
