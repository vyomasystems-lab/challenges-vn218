# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    for i in range (31):
        globals()[f"dut.inp{i}.value"] = 0

    for i in range(31):
        dut.sel.value = i
        globals()[f"dut.inp{i}.value"] = 2
        await Timer(2, units='ns')
        dut.inp1.value = 2
        for j in range (31):
            print(globals()[f"dut.inp{j}.value"])  
        
        #assert dut.out.value == 2, f"Adder result is incorrect: {dut.out.value} != 2"
        print(dut.out.value)
        print(dut.sel.value)
        globals()[f"dut.inp{i}.value"] = 0


    cocotb.log.info('##### CTB: Develop your test here ########')
