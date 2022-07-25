# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    for i in range (31):
        setattr(getattr(dut,f"inp{i}"),"value",0)

    for i in range(31):
        dut.sel.value = i
        setattr(getattr(dut,f"inp{i}"),"value",2)
        await Timer(2, units='ns')        
        print(dut.out.value)
        print(dut.sel.value)
        assert dut.out.value == 2, f"Adder result is incorrect: {dut.out.value} != 2"
        setattr(getattr(dut,f"inp{i}"),"value",0)


    cocotb.log.info('##### CTB: Develop your test here ########')
