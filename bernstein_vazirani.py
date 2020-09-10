import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_textbook.tools import random_state, array_to_latex

from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy

N = 3

def oracle(N):
    bv_o = QuantumCircuit(N+1)
    b_str = format(np.random.randint(2**N),"0b")
    print("Hidden string = ", b_str)
    for i, qubit in enumerate(b_str[::-1]):
        if qubit == '1':
            bv_o.cx(i, N)
    return bv_o

qc = QuantumCircuit(N+1, N)
qc.h(range(N+1))
qc.z(N)
qc.barrier()

qc += oracle(N)
qc.barrier()

qc.h(range(N))
qc.barrier()

for i in range(N):
    qc.measure(i,i)

print(qc.draw())

backend = BasicAer.get_backend("qasm_simulator")
shots = 100
results = execute(qc, backend = backend, shots = shots).result()
answer  = results.get_counts()
fig = plot_histogram(answer)
plt.show()

    