# MUX Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![](https://i.imgur.com/3rrl0Bu.png)

## Verification Environment

The test drives inputs to the Design Under Test which takes in 1-bit input ( apart from *clk* and *reset* ) *inp_bit*  and gives 1-bit output *seq_seen*. 

A 1000 bit long random sequence of 1s and 0s is assigned to the input signal at every falling clock edge using 
```
   for i in range(1000):
        await FallingEdge(dut.clk)
        in_bit = random.randint(0,1)
        dut.inp_bit.value = in_bit
```
Also, last 9 bits of the sequence are stored in a list *inputs*

The assert statement is used to check whether *seq_seen* goes high when the sequence 1011 is entered and also to check whether it remains low otherwise

The assert statement

```
if (len(inputs) > 4):
    if (inputs[-5:-1] == [1,0,1,1]):
        assert dut.seq_seen.value == 1, f"Output is incorrect: {dut.seq_seen.value} != 1"
    else:
        assert dut.seq_seen.value == 0, f"Output is incorrect: {dut.seq_seen.value} != 0"
else:
        assert dut.seq_seen.value == 0, f"Output is incorrect: {dut.seq_seen.value} != 0"

```
*len(inputs) > 4* is checked to make sure atleast 4 bits have been entered in order to avoid index out of range error.

*inputs[-5:-1]* is checked instead of *inputs[-4:]* because *seq_seen* goes high one clock cycle after the pattern 1011 is inputed  


The following error is seen:
```
assert dut.seq_seen.value == 1, f"Output is incorrect: {dut.seq_seen.value} != 1"
                     AssertionError: Output is incorrect: 0 != 1
```
## Test Scenario
- Input Sequence : ...01111011
- Expected Output: seq_seen = 1
- Observed Output in the DUT dut.seq_seen.value = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
SEQ_1:
begin
  if(inp_bit == 1)
    next_state = IDLE;   ====> bug
  else
    next_state = SEQ_10;
end

```
When in state *SEQ_1*, if *inp_bit == 1* then the state should not change i.e. *next_state = SEQ_1* . Instead, it is being changed to *IDLE*.

## Test Scenario
- Input Sequence : ...11101011
- Expected Output: seq_seen = 1
- Observed Output in the DUT dut.seq_seen.value = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
SEQ_101:
begin
  if(inp_bit == 1)
    next_state = SEQ_1011;
  else
    next_state = IDLE;    =====> bug
end

```
When in state *SEQ_101*, if *inp_bit == 0* then the state should change to *SEQ_10* i.e. *next_state = SEQ_10* . Instead, it is being changed to *IDLE*.

## Test Scenario
- Input Sequence : ...01011011
- Expected Output: seq_seen = 1
- Observed Output in the DUT dut.seq_seen.value = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
SEQ_1011:
begin
  next_state = IDLE;   =====> bug
end

```
When in state *SEQ_1011*, the state is being changed to *IDLE* irrespective of the input, which is wrong. If *inp_bit == 0* then the state should change to *SEQ_10* i.e. *next_state = SEQ_10* Also,  if *inp_bit == 1* then the state should change to *SEQ_1* i.e. *next_state = SEQ_1*.

## Design Fix
Updating the design and re-running the test makes the test pass.

![](https://i.imgur.com/oh52jY7.png)

The updated design is checked in as adder_fix.v

## Verification Strategy
Passed a 1000 bit long random sequence of 1s and 0s and checked whether *seq_seen* goes high when the sequence 1011 is entered and whether it remains low otherwise.

## Is the verification complete ?
Yes. All possible state transistions have been simulated.