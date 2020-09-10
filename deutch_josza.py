import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_textbook.tools import random_state, array_to_latex

from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy

N = 3

def const_oracle():
    co = QuantumCircuit(N+1)
    output = np.random.randint(2)
    if output == 1:
        co.x(N)
    return co

def bal_oracle():
    bo = QuantumCircuit(N+1)
    b_str = format(np.random.randint(2**N),"0"+str(N)+"b")
    for qubit in range(len(b_str)):
        if  b_str[qubit] == '1':
            bo.x(qubit)
        bo.cx(qubit, N)
        if  b_str[qubit] == '1':
            bo.x(qubit)
    return bo

dj = QuantumCircuit(N+1, N)
oracle_type = input("Enter b for balanced and c for constant:")

for qubit in range(N):
    dj.h(qubit)

dj.x(N)
dj.h(N)

if oracle_type == 'b':
    dj += bal_oracle()
elif oracle_type == 'c':
    dj += const_oracle()
else:
    print("Wrong input. Exiting program.")
    exit(0)

dj.h(range(N))

for i in range(N):
    dj.measure(i,i)

print(dj.draw())

# backend = BasicAer.get_backend("qasm_simulator")
# shots = 100
# results = execute(dj, backend = backend).result()
# answer = results.get_counts()
# # fig = plt.figure()
# fig = plot_histogram(answer)
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