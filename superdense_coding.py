import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_textbook.tools import random_state, array_to_latex

from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy

def create_bell_pair(qc, a, b):
    qc.h(a)
    qc.cx(a, b)

def alice_gates(qc, qubit, message):
    if(message == '00'):
        pass
    elif(message == '01'):
        qc.z(qubit)
    elif(message == '10'):
        qc.x(qubit)
    elif(message == '11'):
        qc.z(qubit)
        qc.x(qubit)
    else:
        print("Wrong number of  bits in message")
        exit()

def bob_gates(qc, a, b):
    qc.cx(a, b)
    qc.h(a)

qc = QuantumCircuit(2)
create_bell_pair(qc, 0, 1)
qc.barrier()

message = input("Enter 2 bit message to send to Bob:")
alice_gates(qc, 0, message)
qc.barrier()

bob_gates(qc, 0, 1)
qc.barrier()

qc.measure_all()
print(qc.draw())

# backend = BasicAer.get_backend("qasm_simulator")
# job = execute(qc, backend, shots = 1024)
# sim_result = job.result().get_counts(qc)
# print(sim_result)

# plot_histogram(sim_result)
# plt.show()
shots  = 256
IBMQ.load_account()
# Get the least busy backend
provider = IBMQ.get_provider(hub = 'ibm-q')
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 and not x.configuration().simulator and x.status().operational == True))
print("least busy backend: ", backend)
# Run our circuit
job = execute(qc, backend=backend, shots=shots)
job_monitor(job)

# Plotting our result
result = job.result()
fig = plt.figure()
plot_histogram(result.get_counts(qc))
plt.show()

correct_results = result.get_counts(qc)[message]
accuracy = (correct_results/shots)*100
print("Accuracy = %.2f%%" % accuracy)

    

