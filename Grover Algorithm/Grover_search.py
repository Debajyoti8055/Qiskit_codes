from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np
import math as m

def X_transformation(qc, qreg, state):
    '''
    transforms the state of system, applying X gates according to 0's and 1's in the vector 'state'
    '''
    for j in np.arange(len(state)):
        if (int(state[j]) == 0):
            qc.x(qreg[int(j)])

def n_NOT(qc,control, target, anc):
    '''
    performs an n-NOT gate
    '''
    n=len(control)
    instructions=[]
    active_ancilla=[]
    q_unused=[]
    q=0
    a=0
    while((n>0) or (len(q_unused)!=0) or (len(active_ancilla)!=0)):
        if(n>0):
            if((n-2)>=0):
                instructions.append([control[q],control[q+1],anc[a]])
                active_ancilla.append(a)
                a+=1
                q+=2
                n-=2
            if((n-2)==-1):
                q_unused.append(q)
                n-=1
        elif(len(q_unused)!=0):
            if(len(active_ancilla)!=1):
                instructions.append([control[q],anc[active_ancilla[0]],anc[a]])
                del active_ancilla[0]
                del q_unused[0]
                active_ancilla.append(a)
                a=a+1
            else:
                instructions.append([control[q],anc[active_ancilla[0]],target])
                del active_ancilla[0]
                del q_unused[0]
        elif(len(active_ancilla)!=0):
            if(len(active_ancilla)>2):
                instructions.append([anc[active_ancilla[0]],anc[active_ancilla[1]],anc[a]])
                active_ancilla.append(a)
                del active_ancilla[0]
                del active_ancilla[0]
                a=a+1
            elif(len(active_ancilla)==2):
                instructions.append([anc[active_ancilla[0]],anc[active_ancilla[1]],target])
                del active_ancilla[0]
                del active_ancilla[0]
    for i in np.arange(len(instructions)):
        qc.ccx(instructions[i][0],instructions[i][1],instructions[i][2])
    del instructions[-1]
    for i in np.arange(len(instructions)):
        qc.ccx(instructions[0-(i+1)][0],instructions[0-(i+1)][1],instructions[0-(i+1)][2])
    
def Grover_Oracle(mark, qc, q, an1, an2):
    '''
    picks out the marked state and applies a negative phase
    '''
    qc.h(an1[0])
    X_transformation(qc, q, mark)
    if(len(mark)>2):
        n_NOT(qc, q, an1[0], an2)
    if(len(mark)==2):
        qc.ccx(q[0], q[1], an1[0])
    X_transformation(qc, q, mark)
    qc.h(an1[0])
    
def Grover_Diffusion(mark, qc, q, an1, an2):
    '''
    ammends the instructions for a Gorver Diffusion Operation to the QuartumCircuit
    '''
    zeros_state=[]
    for i in np.arange(len(mark)):
        zeros_state.append(0)
        qc.h(q[int(i)])
    Grover_Oracle(zeros_state, qc, q, an1, an2)
    for j in np.arange(len(mark)):
        qc.h(q[int(j)])       

def Grover(Q, marked):
    '''
    Ammends all the instructions for a Gorver Search
    '''
    q=QuantumRegister(Q,name='q')
    an1=QuantumRegister(1,name='anc')
    an2=QuantumRegister(Q-2,name='nanc')
    c=ClassicalRegister(Q,name='c')
    qc=QuantumCircuit(q,an1,an2,c,name='qc')
    for j in np.arange(Q):
        qc.h(q[int(j)])
    qc.x(an1[0])
    iterations=round(m.pi/4*2**(Q/2.0))
    for i in np.arange(iterations):
        Grover_Oracle(marked, qc, q, an1, an2)
        Grover_Diffusion(marked, qc, q, an1, an2)
    return qc,q,an1,an2,c
    
N=3
# q=QuantumRegister(N,name='q')
# c=ClassicalRegister(N,name='c')
# anc=QuantumRegister(1,name='anc')
# nanc=QuantumRegister(N-2,name='nanc')
# # qc=QuantumCircuit(q,c,name='qc')
# G_qc=QuantumCircuit(q,anc,nanc,name='qc')
marked=[1,1,1]
# print(np.arange(N))
# for i in np.arange(N): #prepare our system in an equal superposition of all 2^N
#     G_qc.h(q[int(i)])
# # G_qc.measure(q,c)
# G_qc.x(anc[0])

# iteration=3
# for i in np.arange(iteration):
#     G_qc.Grover_Oracle(marked,G_qc,q,anc,nanc)
#     G_qc.Grover_Diffusion(marked,G_qc,q,anc,nanc)
G_qc,q,anc,nanc,c=Grover(N,marked)
G_qc.measure(q,c)
print(G_qc)
    
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
backend = AerSimulator(method="matrix_product_state")
tr_circ = transpile(G_qc, basis_gates = ['u3', 'cx'], optimization_level = 3)
result = backend.run(tr_circ).result()
counts = result.get_counts()
plot_histogram(counts,figsize=(30,10))
    
    
    
    
    
    
    
    
    
    
    
    