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
    FSL =  0b0000010_00000_00000_001_000000_110011
    FSR =  0b0000010_00000_00000_101_000000_110011
    for i in range(1000):    
        mav_putvalue_src1 = 0
        mav_putvalue_src2 = 33
        mav_putvalue_src3 = 0
        mav_putvalue_instr = FSR

        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
    
        yield Timer(4) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value

        cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        assert dut_output == expected_mav_putvalue, error_message
