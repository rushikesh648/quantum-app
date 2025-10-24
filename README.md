
-----

# ⚛️ Interactive Qiskit Circuit Simulator

This project demonstrates a full-stack application for building, visualizing, and simulating quantum circuits using **Qiskit** (backend logic) served via a **FastAPI** REST API (router) and presented through a simple, interactive **Streamlit** interface (frontend).

## ✨ Features

  * **Interactive Frontend:** Build circuits visually using sliders and buttons powered by Streamlit.
  * **Qiskit Simulation:** Runs the defined circuit on a local Qiskit Aer simulator.
  * **Real-time Visualization:** Displays the circuit diagram and the measurement histogram.
  * **Modular Backend:** Separates the simulation logic from the API routing using FastAPI best practices.

## 🛠️ Project Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | `app.py` (Streamlit) | Collects user input, renders the circuit and histogram images. |
| **Backend API** | `main.py`, `routers/` (FastAPI) | Handles HTTP requests, manages API endpoints. |
| **Core Logic** | `simulation_logic.py` (Qiskit, Aer, Matplotlib) | Executes the quantum simulation and generates results/plots. |

-----

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### 1\. Prerequisites

You need **Python 3.8+** installed on your system.

### 2\. Setup

Create a project directory, set up a virtual environment, and install the required dependencies.

```bash
# Create the project directory structure
mkdir quantum-app
cd quantum-app
mkdir routers

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies for both frontend and backend
pip install streamlit qiskit matplotlib
pip install qiskit qiskit-aer
pip install streamlit fastapi uvicorn qiskit qiskit-aer matplotlib pydantic pillow
```

### 3\. File Creation

Save the code provided previously into the correct files:

| File Path | Content |
| :--- | :--- |
| `app.py` | The Streamlit Frontend Code |
| `main.py` | The Main FastAPI Application Code |
| `routers/quantum_circuit.py` | The FastAPI Router Code |
| `simulation_logic.py` | The Core Qiskit Simulation Logic |

-----

## 💻 Running the Application

This project requires running two separate components: the FastAPI backend API and the Streamlit frontend.

### Step 1: Start the Backend API (FastAPI)

Navigate to the project root directory (`quantum-app`) and run the FastAPI server:

```bash
# Start the FastAPI server on port 8000
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can view the automatically generated interactive documentation at `http://127.0.0.1:8000/docs`.

### Step 2: Start the Frontend (Streamlit)

Open a **new terminal window** (keep the FastAPI server running), activate your virtual environment, and run the Streamlit app:

```bash
# Activate your environment if you closed the first terminal
# source venv/bin/activate 

# Start the Streamlit frontend
streamlit run app.py
```

The interactive application will automatically open in your web browser, usually at `http://localhost:8501`.

-----

## 📚 API Endpoints

The core functionality of the backend is exposed via a single endpoint defined in the router:

| Method | Endpoint | Description | Request Body (JSON) |
| :--- | :--- | :--- | :--- |
| **POST** | `/circuit/run_circuit/` | Runs the Qiskit simulation on the QASM input. | `{"qasm": "OPENQASM 2.0;...", "shots": 1024}` |

-----

## 🤝 Contributing

Contributions are welcome\! Feel free to open issues or submit pull requests for improvements, such as adding more gate types, state vector visualization, or error mitigation techniques.
