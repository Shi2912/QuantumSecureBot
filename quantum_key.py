from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.compiler import transpile

def generate_quantum_key(bits=8):
    qc = QuantumCircuit(bits, bits)

    # Put qubits in superposition
    qc.h(range(bits))

    # Measure
    qc.measure(range(bits), range(bits))

    simulator = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1).result()
    counts = result.get_counts()

    key = list(counts.keys())[0]
    return key
