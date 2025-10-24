from qiskit import QuantumCircuit, qasm2
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import io
import base64
import matplotlib.pyplot as plt
from typing import Tuple, Dict

def run_simulation(qasm_string: str, shots: int) -> Tuple[Dict, str]:
    """
    Runs the simulation logic.

    Returns:
        tuple[Dict, str]: Measurement counts and the Base64-encoded PNG image string.
    """
    # 1. Recreate the circuit from the QASM string
    circuit = qasm2.loads(qasm_string)

    if not circuit.clbits:
        raise ValueError("Circuit is missing classical measurement bits.")

    # 2. Run the simulation
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(circuit)

    # 3. Generate the histogram plot and encode it as a Base64 string
    fig = plot_histogram(counts, figsize=(8, 4))
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig) 
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return counts, image_base64
