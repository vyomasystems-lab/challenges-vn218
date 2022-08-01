# Bitmanipulation Coprocessor Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![](https://i.imgur.com/3rrl0Bu.png)

## Verification Environment

The test drives inputs to the Design Under Test which takes in four 32-bit inputs *mav_putvalue_src1*, *mav_putvalue_src2*,  *mav_putvalue_src3*, *mav_putvalue_instr*, one 1-bit input *EN_mav_putvalue* and gives out a 33-bit output *mav_putvalue*

Values are assigned to the input ports using 
```
    for ins in instr:
        for i in range(10000):              
            mav_putvalue_src1 = random.randint(0,(2**32) - 1)
            mav_putvalue_src2 = random.randint(0,(2**32) - 1)
            mav_putvalue_src3 = random.randint(0,(2**32) - 1)
            
            #random imm gen
            '''
            ins = (bin(ins)[2:]).zfill(32)
            ins = ins[32-32:32-25] + (bin(random.randint(0,2*5 - 1))[2:]).zfill(5) + ins[32-20:]
            ins = int(str(ins),2)
            '''
            '''
            ins = (bin(ins)[2:]).zfill(32)
            ins = ins[32-32:32-26] + (bin(random.randint(0,2**6 - 1))[2:]).zfill(6) + ins[32-20:]
            ins = int(str(ins),2)
            '''
            mav_putvalue_instr = ins

            # driving the input transaction
            dut.mav_putvalue_src1.value = mav_putvalue_src1
            dut.mav_putvalue_src2.value = mav_putvalue_src2
            dut.mav_putvalue_src3.value = mav_putvalue_src3
            dut.EN_mav_putvalue.value = 1
            dut.mav_putvalue_instr.value = mav_putvalue_instr
```
instr is a list containing the instructions. 10000 random cases are being checked for each instruction. For instructions for which the output depends on imm_value, the imm_value is generated randomly.

The assert statement is used to check whether the output *mav_putvalue* is equal to the output of the python model *expected_mav_putvalue*

The assert statement

```
error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)} for inputs \n mav_putvalue_src1 = {hex(mav_putvalue_src1)} \n mav_putvalue_src2 = {hex(mav_putvalue_src2)} \n mav_putvalue_src3 = {hex(mav_putvalue_src3)} \n mav_putvalue_instr = {hex(mav_putvalue_instr)} '
            assert dut_output == expected_mav_putvalue, error_message
```

The following error is seen:
```
assert dut_output == expected_mav_putvalue, error_message
                     AssertionError: Value mismatch DUT = 0x88200129 does not match MODEL = 0x143403017 for inputs 
                      mav_putvalue_src1 = 0xe5b0189f 
                      mav_putvalue_src2 = 0x5c1b2194 
                      mav_putvalue_src3 = 0x992f3b43 
                      mav_putvalue_instr = 0x40007033 
```
## Test Scenario
- Test Inputs : mav_putvalue_src1 = 0xe5b0189f, mav_putvalue_src2 = 0x5c1b2194, mav_putvalue_src3 = 0x992f3b43, mav_putvalue_instr = 0x40007033 (ANDN)
- Expected Output: out = 0x143403017
- Observed Output in the DUT dut.out.value = 0x88200129

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
On analyzing the outputs for a few more inputs, it becomes clear that the verilog design is computing (mav_putvalue_src1)&(mav_putvalue_src2) instead of (mav_putvalue_src1)&(~mav_putvalue_src2)  


## Verification Strategy
10000 random cases (the test was ran multiple times, so more than 10000) were checked for each instruction. For instructions for which the output depends on imm_value, the imm_value was generated randomly.
Manually inserted special test cases to make sure all the if conditions within an instruction, according to the python model, are triggered.
It was verified that the valid bit stays low when the instruction is invalid. 

## Is the verification complete ?
Cannot say with certainity due to lack of understanding of the RTL code, and it is practically not possible to verify for all possible input combinations. 