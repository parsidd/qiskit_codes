import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_textbook.tools import random_state, array_to_latex

psi = random_state(1)

# Display it nicely
array_to_latex(psi, pretext="|\\psi\\rangle =")
# Show it on a Bloch sphere
plot_bloch_multivector(psi)
plt.show()

init_gate = Initialize(psi)
init_gate.label = "init"

inverse_init_gate = init_gate.gates_to_uncompute()

def create_bell_pair(qc, a, b):
    qc.h(a)
    qc.cx(a, b)

def alice_gates(qc, psi, a):
    qc.cx(psi, a)
    qc.h(psi)

def measure_and_send(qc, a, b):
    qc.measure(a, 0)
    qc.measure(b, 1)

def bob_gates(qc, qubit, crz, crx):
    qc.x(qubit).c_if(crx, 1)
    qc.z(qubit).c_if(crz, 1)

qr = QuantumRegister(3, name = "q")
crz, crx = ClassicalRegister(1,name = "crz"), ClassicalRegister(1, name = "crx")

teleportation_circuit = QuantumCircuit(qr, crz, crx)

teleportation_circuit.append(init_gate, [0])

create_bell_pair(teleportation_circuit, 1 , 2)
teleportation_circuit.barrier()

alice_gates(teleportation_circuit, 0, 1)
teleportation_circuit.barrier()

measure_and_send(teleportation_circuit, 0, 1)
teleportation_circuit.barrier()

bob_gates(teleportation_circuit, 2, crz, crx)

teleportation_circuit.append(inverse_init_gate, [2])
cr_result = ClassicalRegister(1)
teleportation_circuit.add_register(cr_result)
teleportation_circuit.measure(2,2)

print(teleportation_circuit.draw())

backend = BasicAer.get_backend("qasm_simulator")
shots = 100
results = execute(teleportation_circuit, backend = backend).result()
answer = results.get_counts()
# fig = plt.figure()
fig = plot_histogram(answer)
plt.show()
