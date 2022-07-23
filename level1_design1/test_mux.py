# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    for i in range (31):
        dut.inp0.value = 0
        globals()[f"dut.inp{i}.value"] == f"{0}"

    for i in range(31):
        dut.sel.value = i
        globals()[f"dut.inp{i}.value"] == f"{2}"
        await Timer(2, units='ns')
        
        assert dut.out.value == 2, f"Adder result is incorrect: {dut.out.value} != 2"
        globals()[f"dut.inp{i}.value"] == f"{0}"


    cocotb.log.info('##### CTB: Develop your test here ########')
