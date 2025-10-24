from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..simulation_logic import run_simulation  # Import the logic function

# Create an APIRouter instance
router = APIRouter(
    prefix="/circuit",  # All routes in this file start with /circuit
    tags=["Quantum Simulation"],
)

# Define the data structure for the request body
class CircuitRequest(BaseModel):
    """Data model for the circuit received from the frontend."""
    qasm: str  # QASM string representation of the circuit
    shots: int = 1024

@router.post("/run-circuit/")
async def run_circuit_endpoint(request: CircuitRequest):
    """
    API endpoint to run a quantum circuit simulation.
    
    The path will be /circuit/run-circuit/
    """
    try:
        # Call the separated backend logic
        counts, image_base64 = run_simulation(request.qasm, request.shots)
        
        return {
            "counts": counts,
            "histogram_image_png_base64": image_base64
        }
        
    except ValueError as ve:
        # Handle specific logic errors (e.g., missing measurements)
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(ve)}")
    except Exception as e:
        # Handle all other unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error during simulation: {str(e)}")
