# cpu.py

NESRAM = bytearray(0x800)

A = 0
X = 0
Y = 0

C = 0 # Carry
Z = 0 # Zero
N = 0 # Negative

SP = 0 # Stack Pointer

I = 0 # Interrupt Disable
D = 0 # Decimal Mode