# MUX Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![](https://i.imgur.com/3rrl0Bu.png)

## Verification Environment

The test drives inputs to the Design Under Test which takes in 31 2-bit data inputs and a 5-bit select input *sel* and gives out a 2-bit output *out*

Values are assigned to the input ports using 
```
    for i in range (31):
        setattr(getattr(dut,f"inp{i}"),"value",0)

    for i in range(31):
        dut.sel.value = i
        inp = random.randint(1,3)
        setattr(getattr(dut,f"inp{i}"),"value",inp)
        await Timer(2, units='ns')        
        
        ##Check output
        
        setattr(getattr(dut,f"inp{i}"),"value",0)
```
Setting all other data input ports to zero, one of the data input port is assigned a random non-zero value *inp*, and then *sel* is assigned the index corresponding to this data input port.

The assert statement is used to check whether the output *out* is equal to *inp*

The assert statement

```
assert dut.out.value == inp, f"Mux output is incorrect: {dut.out.value} != {inp} for sel = {dut.sel.value}""
```

The following error is seen:
```
assert dut.out.value == inp, f"Mux output is incorrect: {dut.out.value} != {inp} for sel = {dut.sel.value}"
                     AssertionError: Mux output is incorrect: 00 != 1 for sel = 01100
```
## Test Scenario
- Test Inputs : inp12 = 1, inpi = 0 (0<=i<=30 ; i !=12), sel = 12
- Expected Output: out = 1
- Observed Output in the DUT dut.out.value = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
5'b01101: out = inp12;   ====> bug
5'b01101: out = inp13;

```
For out = inp12, the case should be sel = 5'b01100 instead of sel = 5'b01101.

## Test Scenario
- Test Inputs : inp30 = 3, inpi = 0 (0<=i<=30 ; i !=30), sel = 30
- Expected Output: out = 3
- Observed Output in the DUT dut.out.value = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
 5'b11101: out = inp29;
 #Missing case here       ====> bug 
 default: out = 0;

```
No case has been specified for sel = 5'b11110. The line ```5'b11110: out = inp30;``` should be added

## Design Fix
Updating the design and re-running the test makes the test pass.

![](https://i.imgur.com/UXa4UEI.png)

The updated design is checked in as /workspace/challenges-vn218/level1_design1_fix/mux_fix.v

## Verification Strategy
Setting all other data input ports to zero, one of the data input port is assigned a random non-zero value *inp*, and then *sel* is assigned the index corresponding to this data input port. Then it is checked whether *out* is equal to *inp*

## Is the verification complete ?
Yes. All possible cases were verified. The default case was verified manually for sel = 31.