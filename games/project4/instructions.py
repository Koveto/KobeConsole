import cpu


def UpdateZN(value):
    """
    Update Zero and Negative flags based on value.
    """

    value &= 0xFF

    cpu.Z = 1 if value == 0 else 0
    cpu.N = 1 if (value & 0x80) else 0


# Load Accumulator
# Assembly: LDA $05
#
# A = NESRAM[addr]
#
# Updates:
# A
# Z
# N
def LDA(addr):
    cpu.A = cpu.NESRAM[addr]
    UpdateZN(cpu.A)


# Store Accumulator
# Assembly: STA $05
#
# NESRAM[addr] = A
def STA(addr):
    cpu.NESRAM[addr] = cpu.A & 0xFF


# Load X Register
# Assembly: LDX $05
#
# X = NESRAM[addr]
#
# Updates:
# X
# Z
# N
def LDX(addr):
    cpu.X = cpu.NESRAM[addr]
    UpdateZN(cpu.X)


# Store X Register
# Assembly: STX $05
#
# NESRAM[addr] = X
def STX(addr):
    cpu.NESRAM[addr] = cpu.X & 0xFF


# Load Y Register
# Assembly: LDY $05
#
# Y = NESRAM[addr]
#
# Updates:
# Y
# Z
# N
def LDY(addr):
    cpu.Y = cpu.NESRAM[addr]
    UpdateZN(cpu.Y)


# Store Y Register
# Assembly: STY $05
#
# NESRAM[addr] = Y
def STY(addr):
    cpu.NESRAM[addr] = cpu.Y & 0xFF


# Load Accumulator Immediate
# Assembly: LDA #$05
#
# A = value
#
# Updates:
# A
# Z
# N
def LDAI(value):
    cpu.A = value & 0xFF
    UpdateZN(cpu.A)


# Load X Immediate
# Assembly: LDX #$05
#
# X = value
#
# Updates:
# X
# Z
# N
def LDXI(value):
    cpu.X = value & 0xFF
    UpdateZN(cpu.X)


# Load Y Immediate
# Assembly: LDY #$05
#
# Y = value
#
# Updates:
# Y
# Z
# N
def LDYI(value):
    cpu.Y = value & 0xFF
    UpdateZN(cpu.Y)

# Transfer A to X
# Assembly: TAX
#
# X = A
#
# Updates:
# X
# Z
# N
def TAX():
    cpu.X = cpu.A & 0xFF
    UpdateZN(cpu.X)


# Transfer A to Y
# Assembly: TAY
#
# Y = A
#
# Updates:
# Y
# Z
# N
def TAY():
    cpu.Y = cpu.A & 0xFF
    UpdateZN(cpu.Y)


# Transfer X to A
# Assembly: TXA
#
# A = X
#
# Updates:
# A
# Z
# N
def TXA():
    cpu.A = cpu.X & 0xFF
    UpdateZN(cpu.A)


# Transfer Y to A
# Assembly: TYA
#
# A = Y
#
# Updates:
# A
# Z
# N
def TYA():
    cpu.A = cpu.Y & 0xFF
    UpdateZN(cpu.A)


# Increment X Register
# Assembly: INX
#
# X = X + 1
#
# Updates:
# X
# Z
# N
def INX():
    cpu.X = (cpu.X + 1) & 0xFF
    UpdateZN(cpu.X)


# Decrement X Register
# Assembly: DEX
#
# X = X - 1
#
# Updates:
# X
# Z
# N
def DEX():
    cpu.X = (cpu.X - 1) & 0xFF
    UpdateZN(cpu.X)


# Increment Y Register
# Assembly: INY
#
# Y = Y + 1
#
# Updates:
# Y
# Z
# N
def INY():
    cpu.Y = (cpu.Y + 1) & 0xFF
    UpdateZN(cpu.Y)


# Decrement Y Register
# Assembly: DEY
#
# Y = Y - 1
#
# Updates:
# Y
# Z
# N
def DEY():
    cpu.Y = (cpu.Y - 1) & 0xFF
    UpdateZN(cpu.Y)


# Clear Carry Flag
# Assembly: CLC
#
# Carry = 0
def CLC():
    cpu.C = 0


# Set Carry Flag
# Assembly: SEC
#
# Carry = 1
def SEC():
    cpu.C = 1


# Add Immediate To Accumulator
# Assembly: ADC #$05
#
# A = A + value + Carry
#
# Updates:
# A
# C
# Z
# N
def ADCI(value):
    result = cpu.A + value + cpu.C

    cpu.C = 1 if result > 0xFF else 0

    cpu.A = result & 0xFF

    UpdateZN(cpu.A)


# Add Memory To Accumulator
# Assembly: ADC $05
#
# A = A + NESRAM[addr] + Carry
#
# Updates:
# A
# C
# Z
# N
def ADC(addr):
    result = cpu.A + cpu.NESRAM[addr] + cpu.C

    cpu.C = 1 if result > 0xFF else 0

    cpu.A = result & 0xFF

    UpdateZN(cpu.A)

# Increment Memory
# Assembly: INC $05
#
# NESRAM[addr] += 1
#
# Updates:
# Z
# N
def INC(addr):
    cpu.NESRAM[addr] = (cpu.NESRAM[addr] + 1) & 0xFF

    UpdateZN(cpu.NESRAM[addr])


# Decrement Memory
# Assembly: DEC $05
#
# NESRAM[addr] -= 1
#
# Updates:
# Z
# N
def DEC(addr):
    cpu.NESRAM[addr] = (cpu.NESRAM[addr] - 1) & 0xFF

    UpdateZN(cpu.NESRAM[addr])

# Compare Accumulator Immediate
# Assembly: CMP #$05
#
# Compares A against value.
#
# A is NOT modified.
#
# Updates:
# C
# Z
# N
def CMPI(value):

    result = (cpu.A - value) & 0xFF

    cpu.C = 1 if cpu.A >= value else 0

    UpdateZN(result)

# Logical AND Immediate
# Assembly: AND #$05
#
# Performs:
#
# A = A AND value
#
# Updates:
# A
# Z
# N
def ANDI(value):

    cpu.A = (cpu.A & value) & 0xFF

    UpdateZN(cpu.A)

# Logical AND Memory
# Assembly: AND $05
#
# Performs:
#
# A = A AND NESRAM[addr]
#
# Updates:
# A
# Z
# N
def AND(addr):

    cpu.A = (cpu.A & cpu.NESRAM[addr]) & 0xFF

    UpdateZN(cpu.A)

# Logical OR Immediate
# Assembly: ORA #$05
#
# Performs:
#
# A = A OR value
#
# Updates:
# A
# Z
# N
def ORAI(value):

    cpu.A = (cpu.A | value) & 0xFF

    UpdateZN(cpu.A)

# Logical OR Memory
# Assembly: ORA $05
#
# Performs:
#
# A = A OR NESRAM[addr]
#
# Updates:
# A
# Z
# N
def ORA(addr):

    cpu.A = (cpu.A | cpu.NESRAM[addr]) & 0xFF

    UpdateZN(cpu.A)

# Exclusive OR Immediate
# Assembly: EOR #$05
#
# Performs:
#
# A = A XOR value
#
# Updates:
# A
# Z
# N
def EORI(value):

    cpu.A = (cpu.A ^ value) & 0xFF

    UpdateZN(cpu.A)

# Exclusive OR Memory
# Assembly: EOR $05
#
# Performs:
#
# A = A XOR NESRAM[addr]
#
# Updates:
# A
# Z
# N
def EOR(addr):

    cpu.A = (cpu.A ^ cpu.NESRAM[addr]) & 0xFF

    UpdateZN(cpu.A)

# Compare X Register Immediate
# Assembly: CPX #$05
#
# Compare X against value.
#
# X is NOT modified.
#
# Updates:
# C
# Z
# N
def CPXI(value):

    result = (cpu.X - value) & 0xFF

    cpu.C = 1 if cpu.X >= value else 0

    UpdateZN(result)

# Compare Y Register Immediate
# Assembly: CPY #$05
#
# Compare Y against value.
#
# Y is NOT modified.
#
# Updates:
# C
# Z
# N
def CPYI(value):

    result = (cpu.Y - value) & 0xFF

    cpu.C = 1 if cpu.Y >= value else 0

    UpdateZN(result)

# Branch if Equal
# Assembly: BEQ
#
# Returns True if Zero flag is set.
def BEQ():
    return cpu.Z == 1

# Branch if Not Equal
# Assembly: BNE
#
# Returns True if Zero flag is clear.
def BNE():
    return cpu.Z == 0

# Branch if Carry Set
# Assembly: BCS
#
# Returns True if Carry is set.
def BCS():
    return cpu.C == 1

# Branch if Carry Clear
# Assembly: BCC
#
# Returns True if Carry is clear.
def BCC():
    return cpu.C == 0

# Transfer X to Stack Pointer
# Assembly: TXS
#
# SP = X
#
# Updates:
# none
def TXS():
    cpu.SP = cpu.X

# Set Interrupt Disable Flag
# Assembly: SEI
#
# Prevents CPU interrupts.
#
# Updates:
# I
def SEI():
    cpu.I = 1


# Clear Decimal Flag
# Assembly: CLD
#
# Disables decimal arithmetic mode.
#
# Updates:
# D
def CLD():
    cpu.D = 0

# Branch if Positive
# Assembly: BPL
#
# Returns True when the Negative flag is clear.
def BPL():
    return cpu.N == 0

# Branch if Minus
# Assembly: BMI
#
# Returns True when the Negative flag is set.
def BMI():
    return cpu.N == 1

# Load Accumulator Indexed By X
# Assembly: LDA address,x
#
# A = NESRAM[address + X]
#
# Updates:
# A
# Z
# N
def LDAX(addr):
    cpu.A = cpu.NESRAM[addr + cpu.X]
    UpdateZN(cpu.A)

# Logical OR Immediate
# Assembly: ORA #$05
#
# A = A OR value
#
# Updates:
# A
# Z
# N
def ORAI(value):

    cpu.A = (cpu.A | value) & 0xFF

    UpdateZN(cpu.A)

# Load X Indexed By Y
# Assembly: LDX address,y
#
# X = NESRAM[address + Y]
#
# Updates:
# X
# Z
# N
def LDXY(addr):

    cpu.X = cpu.NESRAM[addr + cpu.Y]

    UpdateZN(cpu.X)