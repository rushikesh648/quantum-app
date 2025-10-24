import streamlit as st
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt
import numpy as np

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Qiskit Circuit Builder",
    layout="centered"
)

st.title("Interactive Quantum Circuit Builder ⚛️")
st.markdown("Use the controls below to build a quantum circuit and see the diagram in real-time.")

# --- UI Controls (Frontend) ---

# Get number of qubits from the user
num_qubits = st.sidebar.slider(
    "Number of Qubits",
    min_value=1,
    max_value=5,
    value=2,
    step=1
)

# Get gate selection from the user
st.sidebar.subheader("Apply Gates")

# Radio buttons for gate selection
gate_options = {
    "Hadamard (H)": "h",
    "Pauli-X (X)": "x",
    "CNOT (CX)": "cx",
    "Identity (I)": "id"
}
selected_gate_name = st.sidebar.radio("Select a Gate:", list(gate_options.keys()))
selected_gate_code = gate_options[selected_gate_name]

# Text input for qubit on which to apply the gate
qubit_index_input = st.sidebar.text_input(
    "Qubit Index(es) (e.g., 0 or 0,1 for CNOT)",
    value="0"
)

# Button to add the gate
if 'circuit' not in st.session_state:
    st.session_state.circuit = QuantumCircuit(num_qubits, num_qubits)
    st.session_state.num_qubits = num_qubits

# Re-initialize circuit if number of qubits changes
if st.session_state.num_qubits != num_qubits:
    st.session_state.circuit = QuantumCircuit(num_qubits, num_qubits)
    st.session_state.num_qubits = num_qubits

def add_gate():
    """Function to parse input and add the gate to the circuit."""
    try:
        # Parse qubit indices
        indices = [int(i.strip()) for i in qubit_index_input.split(',') if i.strip()]
        
        # Check if indices are valid
        if not all(0 <= i < num_qubits for i in indices):
            st.error(f"Invalid qubit index. Must be between 0 and {num_qubits - 1}.")
            return
        
        # Apply the selected gate
        qc = st.session_state.circuit
        
        if selected_gate_code == "h" or selected_gate_code == "x" or selected_gate_code == "id":
            if len(indices) != 1:
                st.error(f"{selected_gate_name} requires exactly one qubit index.")
                return
            getattr(qc, selected_gate_code)(indices[0])
        elif selected_gate_code == "cx":
            if len(indices) != 2:
                st.error("CNOT requires exactly two qubit indices (control, target).")
                return
            qc.cx(indices[0], indices[1])
        
        st.session_state.circuit = qc
    
    except ValueError:
        st.error("Invalid input for qubit indices. Please use comma-separated integers.")

def measure_all():
    """Function to add measurements to all qubits."""
    try:
        qc = st.session_state.circuit
        # Add measurements if not already added
        if not qc.clbits:
            # Recreate circuit with classical bits if not present
            st.session_state.circuit = QuantumCircuit(qc.num_qubits, qc.num_qubits)
            qc = st.session_state.circuit
            # Re-apply all existing operations
            for instruction in st.session_state.circuit.data:
                qc.append(instruction.operation, instruction.qubits, instruction.clbits)
        
        qc.measure(range(qc.num_qubits), range(qc.num_qubits))
        st.session_state.circuit = qc
        
    except Exception as e:
        st.error(f"An error occurred while adding measurements: {e}")

st.sidebar.button("Add Gate to Circuit", on_click=add_gate)
st.sidebar.button("Add Measurements", on_click=measure_all)
st.sidebar.button("Reset Circuit", on_click=lambda: st.session_state.update(circuit=QuantumCircuit(num_qubits, num_qubits)))

# --- Visualization (Frontend Output) ---

st.subheader("Current Quantum Circuit Diagram")

try:
    # Use Qiskit's circuit drawer with 'mpl' output (requires matplotlib)
    fig = st.session_state.circuit.draw(output='mpl', style={'fontsize': 10})
    
    # Display the Matplotlib figure in Streamlit
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error displaying circuit: {e}")
    st.info("Try resetting the circuit or checking the number of qubits for CNOT.")

st.sidebar.info("This is an example of using **Streamlit** for the frontend, running **Qiskit** (the backend logic) in Python, and displaying the results using **Matplotlib**.")

# --- YouTube Video Link ---
# This video is a general introduction to Qiskit, the library used in the backend of this frontend code.
The video below provides a good introduction to the Qiskit framework, which is used to define and visualize the quantum circuit in this frontend application.
[Run Quantum Circuits with Qiskit Primitives](https://www.youtube.com/watch?v=NTplT4WnNbk)
