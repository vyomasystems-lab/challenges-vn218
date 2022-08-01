import os
import random
from pathlib import Path
import math

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_main(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    cocotb.log.info('#### CTB: Develop your test here! ######')

    j = 0
    for i in range(2**16+17):
        await FallingEdge(dut.clk)
        if (i < 2**16):
              dut.N.value = i
              dut.in_valid.value = 1
        await RisingEdge(dut.clk)        
        if (dut.out_valid.value):
              out = dut.sqrt.value
              if (j > 1):
                     error = ((math.sqrt(j) - (out.integer/2**6))/math.sqrt(j))*100
                     assert error < 1, f"Large error = {error}% for input = {j}"
              j = j+1 