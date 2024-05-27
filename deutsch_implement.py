from qiskit import QuantumCircuit
import time  
import numpy as np
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from texttable import Texttable


#Oracle maker  setting for Deutsch alorithm only support 1 bit query
def oracle_maker(queryfunc_type):

    oracle = QuantumCircuit(2) # 1 Qubit + 1 Junk_Qbit

    #queryfunc_type == 0 (f0) : Not define anything
    if queryfunc_type == 1:
        oracle.cx(0,1)

    elif queryfunc_type == 2:
        oracle.cx(0,1)
        oracle.x(1)

    elif queryfunc_type == 3:
        oracle.x(1)
    
    else:
        if queryfunc_type != 0:
            raise ValueError(" Please input Type of Query function in 0,1,2,3 ")

    return oracle


def deutsch_algorithm(oracle):
    qt_circuit = QuantumCircuit(2,1)
    #Make Step Phi1
    qt_circuit.x(1)
    #Make Step Phi2
    qt_circuit.h(range(2))
    #Make Step Phi3
    qt_circuit = qt_circuit.compose(oracle,qubits=[0,1])
    #Make Step Phi4
    qt_circuit.h(range(1))
    #Make Step Measurement to Classical Bit
    qt_circuit.measure(range(1), range(1))
    
    return qt_circuit



if __name__ == '__main__':
    print("------ Please Select Type of Query function ------")
    table = Texttable()
    table.header(["input x", "f0(x)","f1(x)","f2(x)","f3(x)"])
    table.add_row(["0","0","0","1","1"])
    table.add_row(["1","0","1","0","1"])
    print(table.draw())
    fn = int(input("Select Query input function (0,1,2,3) : "))



    #Defin Oracle following type of Query function
    oracle = oracle_maker(fn)
    #Make Quantum Circuit for Deutsch algorithm
    print("------- Oracle Circuit -------\n",oracle)
    qt_circuit = deutsch_algorithm(oracle)

    #Make The Simulator follow Real-World noise
    simulator = AerSimulator()
    #Run 1000 times with Simulator
    measurement_result = simulator.run(qt_circuit,shots=1000,memory=True).result()
    counter = measurement_result.get_counts(qt_circuit)
    #See the result
    print("The Query function type is f",fn)
    print("------- The Total Circuit is -------\n",qt_circuit)
    print("Mesurement result of Qubit 0 is ",counter)


