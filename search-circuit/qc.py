# --- 1. State Preparation: Put all items in Superposition ---
qc.h(range(n))
# The initial equal superposition state is our 'unindexed' database.

# --- 2. Determine Number of Iterations (Search Complexity) ---
# For optimal search, the number of Grover iterations is roughly 
# proportional to sqrt(N), where N is the number of items.
# For N=4, optimal iterations = floor(pi/4 * sqrt(N)) = floor(pi/4 * 2) = 1.
num_iterations = 1 

# --- 3. Apply Grover's Iteration (The 'Query' Function) ---
for _ in range(num_iterations):
    # Step 3a: Mark the Target State (The Oracle/Condition)
    create_oracle(qc, target_state='11')
    
    # Step 3b: Amplify the Target's Probability (The Diffuser)
    create_diffuser(qc, n)

# --- 4. Read the Result (Measurement) ---
qc.measure(range(n), range(n))

# Visualize the circuit (Optional)
print(qc.draw(output='text', fold=-1))
#
