# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    for i in range (31):
        setattr(getattr(dut,f"inp{i}"),"value",0)

    for i in range(31):
        dut.sel.value = i
        inp = random.randint(1,3)
        setattr(getattr(dut,f"inp{i}"),"value",inp)
        await Timer(2, units='ns')        
        assert dut.out.value == inp, f"Mux output is incorrect: {dut.out.value} != {inp} for sel = {dut.sel.value}"
        setattr(getattr(dut,f"inp{i}"),"value",0)

