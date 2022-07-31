# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    #mav_putvalue_src1 = 0x5
    #mav_putvalue_src2 = 0x0
    #mav_putvalue_src3 = 0x0
    #mav_putvalue_instr = 0x101010B3
    ANDN = 0b0100000_00000_00000_111_00000_0110011
    ORN =  0b0100000_00000_00000_110_00000_0110011
    XNOR = 0b0100000_00000_00000_100_00000_0110011
    SLO =  0b0010000_00000_00000_001_00000_0110011
    SRO =  0b0010000_00000_00000_101_00000_0110011
    ROL =  0b0110000_00000_00000_001_00000_0110011
    ROR =  0b0110000_00000_00000_101_00000_0110011
    SH1ADD =  0b0010000_00000_00000_010_00000_0110011
    SH2ADD =  0b0010000_00000_00000_100_00000_0110011
    SH3ADD =  0b0010000_00000_00000_110_00000_0110011
    SBCLR = 0b0100100_00000_00000_001_00000_0110011
    SBSET = 0b0010100_00000_00000_001_00000_0110011
    SBINV = 0b0110100_00000_00000_001_00000_0110011
    SBEXT = 0b0100100_00000_00000_101_00000_0110011
    GORC = 0b0010100_00000_00000_101_00000_0110011
    GREV = 0b0110100_00000_00000_101_00000_0110011
    
    
    CMIX = 0b0000011_00000_00000_001_00000_0110011
    CMOV = 0b0000011_00000_00000_101_00000_0110011
    FSL =  0b0000010_00000_00000_001_00000_0110011
    FSR =  0b0000010_00000_00000_101_00000_0110011

    CLZ =  0b0110000_00000_00000_001_00000_0010011
    CTZ =  0b0110000_00001_00000_001_00000_0010011
    PCNT = 0b0110000_00010_00000_001_00000_0010011
    SEXTB = 0b0110000_00100_00000_001_00000_0010011
    SEXTH = 0b0110000_00101_00000_001_00000_0010011
    CRC32B = 0b0110000_10000_00000_001_00000_0010011
    CRC32H = 0b0110000_10001_00000_001_00000_0010011
    CRC32W = 0b0110000_10010_00000_001_00000_0010011
    CRC32CB = 0b0110000_11000_00000_001_00000_0010011
    CRC32CH = 0b0110000_11001_00000_001_00000_0010011
    CRC32CW = 0b0110000_11010_00000_001_00000_0010011

    CLMUL = 0b0000101_00000_00000_001_00000_0110011
    CLMULH = 0b0000101_00000_00000_011_00000_0110011
    CLMULR = 0b0000101_00000_00000_010_00000_0110011
    MIN = 0b0000101_00000_00000_100_00000_0110011
    MAX = 0b0000101_00000_00000_101_00000_0110011
    MINU = 0b0000101_00000_00000_110_00000_0110011
    MAXU = 0b0000101_00000_00000_111_00000_0110011
    BDEP = 0b0100100_00000_00000_110_00000_0110011
    BEXT = 0b0000100_00000_00000_110_00000_0110011
    PACK = 0b0000100_00000_00000_100_00000_0110011
    PACKU = 0b0100100_00000_00000_100_00000_0110011
    PACKH = 0b0000100_00000_00000_111_00000_0110011
    SHFL = 0b0000100_00000_00000_001_00000_0110011
    UNSHFL = 0b0000100_00000_00000_101_00000_0110011
    BFP = 0b0100100_00000_00000_111_00000_0110011


    

    instr = [ORN,XNOR,SLO,SRO,ROL,ROR,SH1ADD,SH2ADD,SH3ADD,SBCLR,SBSET,SBINV,SBEXT,GORC,GREV,CMIX,CLZ,CTZ,PCNT,SEXTB,SEXTH,CRC32B,CRC32H,CRC32W,CRC32CB,CRC32CH,CRC32CW]
    instr2 = [CLMUL,CLMULH,CLMULR,MIN,MAX,MINU,MAXU,BDEP,BEXT,PACK,PACKU,PACKH,SHFL,UNSHFL,BFP]
    for ins in instr:
        for i in range(1000):    
            #dut.RST_N.value <= 0
            #yield Timer(10) 
            #dut.RST_N.value <= 1
            
            mav_putvalue_src1 = random.randint(0,(2**32) - 1)
            mav_putvalue_src2 = 0 #random.randint(0,(2**32) - 1)
            mav_putvalue_src3 = random.randint(0,(2**32) - 1)
            mav_putvalue_instr = CMOV

            # expected output from the model
            expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

            # driving the input transaction
            dut.mav_putvalue_src1.value = mav_putvalue_src1
            dut.mav_putvalue_src2.value = mav_putvalue_src2
            dut.mav_putvalue_src3.value = mav_putvalue_src3
            dut.EN_mav_putvalue.value = 1
            dut.mav_putvalue_instr.value = mav_putvalue_instr
        
            yield Timer(1) 

            # obtaining the output
            dut_output = dut.mav_putvalue.value

            cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
            cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
            
            # comparison
            error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)} for inputs \n mav_putvalue_src1 = {hex(mav_putvalue_src1)} \n mav_putvalue_src2 = {hex(mav_putvalue_src2)} \n mav_putvalue_src3 = {hex(mav_putvalue_src3)} '
            assert dut_output == expected_mav_putvalue, error_message
