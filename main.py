from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import quantum_circuit  # Import the router

# Initialize FastAPI app
app = FastAPI(title="Modular Quantum App API")

# Setup CORS middleware for frontend communication (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(quantum_circuit.router)

@app.get("/")
def read_root():
    return {"message": "Quantum Simulation API is running. Go to /docs for endpoints."}

# --- How to run the backend server ---
# 1. Ensure you are in the 'quantum-app/' directory.
# 2. Run the command: uvicorn main:app --reload
# 3. The API will be available at http://127.0.0.1:8000/
# 4. The circuit simulation endpoint is: http://127.0.0.1:8000/circuit/run-circuit/
