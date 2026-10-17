from instructions import *
from defines import *
from constants import *

def InitializeMemory():
    pass

def MoveAllSpritesOffscreen():
    pass

def InitializeNameTables():
    pass

def WritePPUReg1():
    pass

def InitScroll():
    pass

def UpdateScreen():
    pass

# Start
SEI()
CLD()
LDAI(0b00010000)
STA(PPU_CTRL_REG1)
LDXI(0xFF)
TXS()
LDA(PPU_STATUS)
"""
# VBlank1
while True:
    LDA(PPU_STATUS)
    if not BPL():
        break
# VBlank2
while True:
    LDA(PPU_STATUS)
    if not BPL():
        break
"""
LDYI(ColdBootOffset)
LDXI(0x05)
# WBootCheck
cold_boot_required = False
while True:
    LDAX(TopScoreDisplay)
    CMPI(10)
    if BCS():
        cold_boot_required = True
        break
    DEX()
    if not BPL():
        break
if not cold_boot_required:
    LDA(WarmBootValidation)
    CMPI(0xA5)
    if not BNE():
        LDYI(WarmBootOffset)
# ColdBoot
InitializeMemory()
STA(SND_DELTA_REG + 1)
STA(OperMode)
LDAI(0xA5)
STA(WarmBootValidation)
STA(PseudoRandomBitReg)
LDAI(0b00001111)
STA(SND_MASTERCTRL_REG)
LDAI(0b00000110)
STA(PPU_CTRL_REG2)
MoveAllSpritesOffscreen()
InitializeNameTables()
INC(DisableScreenFlag)
LDA(Mirror_PPU_CTRL_REG1)
ORAI(0b10000000)
WritePPUReg1()
# VRAM_AddrTable_Low
# VRAM_AddrTable_High
# VRAM_Buffer_Offset
# NonMaskableInterrupt
LDA(Mirror_PPU_CTRL_REG1)
ANDI(0b01111111)
STA(Mirror_PPU_CTRL_REG1)
ANDI(0b01111110)
STA(PPU_CTRL_REG1)
LDA(Mirror_PPU_CTRL_REG2)
ANDI(0b11100110)
LDY(DisableScreenFlag)
if not BNE():
    LDA(Mirror_PPU_CTRL_REG2)
    ORAI(0b00011110)
# ScreenOff
STA(Mirror_PPU_CTRL_REG2)
ANDI(0b11100111)
STA(PPU_CTRL_REG2)
LDX(PPU_STATUS)
LDAI(0x00)
InitScroll()
STA(PPU_SPR_ADDR)
LDAI(0x02)
STA(SPR_DMA)
LDX(VRAM_Buffer_AddrCtrl)
# LDAX(VRAM_AddrTable_Low) # we skipped this!
STA(0x00)
# LDAX(VRAM_AddrTable_High)
STA(0x01)
UpdateScreen()
LDYI(0x00)
LDX(VRAM_Buffer_AddrCtrl)
CPXI(0x06)
if not BNE():
    INY()
# InitBuffer
# LDXY(VRAM_Buffer_Offset) # this instruction does not exist yet
