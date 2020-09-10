from qiskit import BasicAer, execute, IBMQ, QuantumCircuit, QuantumRegister
from qiskit.visualization import plot_histogram

from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy

import numpy as np
import matplotlib.pyplot as plt
from qft import qft

class qpe:
    def __init__(self, N):
        self.N = N
        self.qc = QuantumCircuit(N+1, N)
    
    def qpe(self):
        self.qc.h(range(N))
        self.qc.x(N)
        self.qc.barrier()
        self.kickback()
        self.qc.barrier()
        qft_class = qft(N)
        inv_qft = qft_class.inverse_qft()
        self.qc.append(inv_qft,range(N))
        self.qc.barrier()
        self.qc.measure(range(N), range(N))
        return self.qc

    def kickback(self):
        repetitions = 1
        for counting_qubit in range(N):
            for i in range(repetitions):
                self.qc.cu1(np.pi/4, counting_qubit, N); # This is C-U
            repetitions *= 2

if __name__ == "__main__":
    N = 3
    qpe = qpe(N)
    qpe_circuit = qpe.qpe()

    print(qpe_circuit.draw())

    backend = BasicAer.get_backend('qasm_simulator')
    shots = 2048
    results = execute(qpe_circuit, backend=backend, shots=shots).result()
    answer = results.get_counts()

    plot_histogram(answer)
    plt.show()
