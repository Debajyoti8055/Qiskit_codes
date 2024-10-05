plain_text='0101'
key='1100'

# plain text
for i, char in enumerate(plain_text):
    if char == '1':
        qc.x(pt[i])

for i, char in enumerate(key):
    if char == '1':
        qc.x(k[i])