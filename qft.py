from qiskit import BasicAer, execute, IBMQ, QuantumCircuit
from qiskit.visualization import plot_histogram, plot_bloch_multivector

from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy

from qiskit_textbook.widgets import scalable_circuit

import numpy as np
import matplotlib.pyplot as plt

class qft:
    def __init__(self, N):
        self.qc = QuantumCircuit(N)
        self.N = N
        self.add_gates(self.N)
        self.qc.barrier()
        self.swap_registers(self.N)
        self.qc.barrier()

    def qft(self):
        return self.qc

    def add_gates(self, N):
        if(N == 0):
            return
        N -= 1
        self.qc.h(N)
        for qubit in range(N):
            self.qc.cu1(np.pi/2**(N-qubit), qubit, N)
        self.add_gates(N)

    def swap_registers(self, N):
        for qubit in range(N//2):
            self.qc.swap(qubit, N-qubit-1)
        return self.qc

    def inverse_qft(self):
        return self.qc.inverse()

if __name__ == "__main__":
    N = 3
    b = np.random.randint(2**N)
    b = format(b,"0b")
    print("Number = ",b)

    qc = QuantumCircuit(N)

    for qubit, i in  enumerate(b[::-1]):
        if(i == '1'):
            qc.x(qubit)

    qc.barrier()
    qft = qft(N)
    qc += qft.qft()
    # scalable_circuit(qc)

    inv_qft_circuit = qft.inverse_qft()
    qc += inv_qft_circuit
    qc.measure_all()
    print(qc.draw())

    # backend = BasicAer.get_backend("statevector_simulator")
    # statevector = execute(qft, backend=backend).result().get_statevector()
    # plot_bloch_multivector(statevector)
    # plt.show()

    backend = BasicAer.get_backend("qasm_simulator")
    shots = 256
    results = execute(qc, backend = backend, shots = shots).result()
    counts = results.get_counts()
    plot_histogram(counts)
    plt.show()