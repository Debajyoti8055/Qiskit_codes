def my_oracle(qc, r_key, r_ancilla, r_cipher, r_text, r_output, n):
    #Compute cipher text possibilities by XORing
    cipher(qc, r_key, r_text, n)
    
    #Checking whether the generated cipher text is equal to the given cipher text
    for i in range(n):
        qc.cx(r_cipher[i], r_ancilla[i])
        qc.cx(r_text[i], r_ancilla[i])
        qc.x(r_ancilla[i])
        
    #Set 'output' bit if the cipher text is matched
    qc.mcx(r_ancilla, r_output)
    
    qc.barrier()
    
    #Uncompute cipher to reset ancilla & plain text qubits
    #Reset ancilla qubit
    for i in range(n):
        qc.x(r_ancilla[i])
        qc.cx(r_cipher[i], r_ancilla[i])
        qc.cx(r_text[i], r_ancilla[i])
    qc.barrier()
    #Reset plain text by inverse cipher process
    cipher(qc, r_key, r_text, n)
    
    qc.barrier()