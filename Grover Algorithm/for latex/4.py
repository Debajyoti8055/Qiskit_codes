qc = QuantumCircuit(r_text, r_key, r_cipher, r_ancilla, r_output, r_class)
#loading plain text
plain_text = '0101'
load_input(qc, r_text, plain_text, n)
#Preparing key in a superposition state
load_key(qc, r_key, n)
#loading known cipher text
cipher_text = '1001'
load_input(qc, r_cipher, cipher_text, n)
#Preparing output qubit
qc.x(r_output)
qc.h(r_output)
qc.barrier()
# Iteration
my_oracle(qc, r_key, r_ancilla, r_cipher, r_text, r_output, n)
qc.barrier()
qc.append(diffuser(n), r_key)
qc.barrier()
