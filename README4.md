# CORDIC square root Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![](https://i.imgur.com/3rrl0Bu.png)

## Verification Environment

The test drives inputs to the Design Under Test which takes in 16-bit input *N* and a 1-bit input *in_valid* (apart from *clk*) and gives a 16-bit output *sqrt* and a 1-bit output *out_valid*. 

Values are assigned to the input ports using  
```
for i in range(2**16+17):             
    await FallingEdge(dut.clk)
    if (i < 2**16):
          dut.N.value = i
          dut.in_valid.value = 1
```
The online architecture of the design is taken advantage of and all possible 16-bit inputs are streamed. range(2**16+17) is used to take care of the 17 cycle latency of the design and make sure all the outputs are collected

The error in output square root value is expected to be less than 1% for all inputs other than N = 1. Hence, the assert statement is used to check whether the error is less than 1%.

The assert statement

```
out = dut.sqrt.value
error = ((math.sqrt(j) - (out.integer/2**6))/math.sqrt(j))*100
assert error < 1, f"Large error = {error}% for input = {j}"

```
out.integer/2**6  because output is in UQ8.6 format.


The following error is seen:
```
assert error < 1, f"Large error = {error}% for input = {j}"
                        AssertionError: Large error = 99.6115746441236% for input = 32768
```
## Test Scenario
- Test Input : N = 2**15
- Expected Error: less than 1%
- Observed Error: more than 99.611%

Hence, there is a design bug

## Design Bug
The inserted bug was

```
 wire [$clog2(width)-1:0] init_sf;  ====> bug

```
*init_sf* can take values from 0 to width. Hence, it's width should be $clog2(width)+1 and not $clog2(width). This bug can be pinpointed because the test fails for N >= 2**15, and it's the first value for which *init_sf = width*.


## Design Fix
Updating the design and re-running the test makes the test pass.

![](https://i.imgur.com/H4WmPJK.png)

The updated design is checked in as /workspace/challenges-vn218/level3_design_fix/cordicsqrt_fix.v

## Verification Strategy
The online architecture of the design is taken advantage of and all possible 16-bit inputs are streamed. 
The error in output square root value is expected to be less than 1% for all inputs other than N = 1. Hence, the assert statement is used to check whether the error is less than 1%.
Output is manually verified for N = 0 and N = 1.

## Is the verification complete ?
Yes. Outputs for all possible inputs have been verified.