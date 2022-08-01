import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_main(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    cocotb.log.info('#### CTB: Develop your test here! ######')

 #   inputs = []
    for i in range(2**5):
        await FallingEdge(dut.clk)
        dut.N.value = i
 #       inputs.append(in_bit)
 #       if (len(inputs) > 9):
 #           inputs.pop(0)
        await RisingEdge(dut.clk)
        out = dut.sqrt.value
        print(out.integer)
 #       print(inputs)
 #       if (len(inputs) > 4):
 #           if (inputs[-5:-1] == [1,0,1,1]):
 #               assert dut.seq_seen.value == 1, f"Output is incorrect: {dut.seq_seen.value} != 1"
 #           else:
 #               assert dut.seq_seen.value == 0, f"Output is incorrect: {dut.seq_seen.value} != 0"
 #       else:
 #               assert dut.seq_seen.value == 0, f"Output is incorrect: {dut.seq_seen.value} != 0"