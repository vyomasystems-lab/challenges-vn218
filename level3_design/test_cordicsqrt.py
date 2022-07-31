import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')

    inputs = []
    for i in range(1000):
        await FallingEdge(dut.clk)
        in_bit = random.randint(0,1)
        dut.inp_bit.value = in_bit
        inputs.append(in_bit)
        if (len(inputs) > 9):
            inputs.pop(0)
        await RisingEdge(dut.clk)
        print(inputs)
        if (len(inputs) > 4):
            if (inputs[-5:-1] == [1,0,1,1]):
                assert dut.seq_seen.value == 1, f"Output is incorrect: {dut.seq_seen.value} != 1"
            else:
                assert dut.seq_seen.value == 0, f"Output is incorrect: {dut.seq_seen.value} != 0"
        else:
                assert dut.seq_seen.value == 0, f"Output is incorrect: {dut.seq_seen.value} != 0"