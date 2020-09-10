from qiskit import BasicAer, IBMQ, execute, QuantumCircuit
from qiskit.visualization import plot_histogram

from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
from qiskit_textbook.tools import simon_oracle

import numpy as np
import matplotlib.pyplot as plt 

N = 3

b = format(np.random.randint(2**N), "0"+str(N)+"b")
print("Hidden string = ", b)

qc = QuantumCircuit(N*2, N)

qc.h(range(N))
qc.barrier()

s_o = simon_oracle(b)
qc += s_o
qc.barrier()

qc.h(range(N))
qc.barrier()

qc.measure(range(N), range(N))

print(qc.draw())

backend = BasicAer.get_backend("qasm_simulator")
shots = 1024
results = execute(qc, backend=backend, shots=shots).result()
counts = results.get_counts()
plot_histogram(counts)
plt.show()






