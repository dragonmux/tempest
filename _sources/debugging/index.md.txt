# Debugging using PDI

## Getting started

Debug has its own key value that must be sent to enable it. You can check if this needs doing by issuing `ldcs status` to the PDI processor.

The debug key uses the constant 0x3a212dd49f7c8121 to unlock the debug part of the controller.

## Initiating a debug session

### Put the processor into reset

```pdi
stcs reset 0x59
ldcs status
```

The LDCS should return 0x00 if these are the first instructions run in a session.

### Turn the debug interface on

```pdi
key debug
ldcs status
```

The LDCS should return 0x04 if `key nvm` has not been run yet, and 0x06 if it has.

### Take the reset processor and put it in debug pause state

```pdi
stcs r4 1
ldcs r3
stcs reset 0x00
ldcs r3
ldcs r3
```

Writing bit 1 of r4 puts the processor into debug-based pause once reset is released
the first LDCS to r3 is used to verify that r3 is presently 0.
Once reset is released, r3 will initially be 0x14, which should be observed with the second LDCS.
Once debug setup is completed, r4 will then read as 0x04, which should be observed with the final LDCS.

## Running the processor to an address

The following uses hardware breakpoint unit 1, however based on documentation murmers it stands there should be 2.

### Set up run-to-address

```pdi
sts.u32 0x00000020 0x29 0x01 0x00 0x00
sts.u32 0x00000024 0x00 0x00 0x00 0x00
sts.u8 0x00000040 0x00
sts.u8 0x00000040 0x00
sts.u16 0x00000028 0x00 0x01
sts.u8 0x00000048 0x00
```

This sequence performs the following operations (some of them need more figuring out how things work to understand):

* Stores 0x00000129 as the target program address to run the processor to into the first hardware breakpoint unit break address register at 0x00000020. Program addresses are in words which is why they are half what they should be going by `objdump` output.
* Stores 0x00000000 to the first hardware breakpoint unit at its second register at 0x00000024
* Stores 0x00 to a byte register at 0x00000040 (twice) - the purpose for this is not well understood yet but this may be the second hardware breakpoint unit
* Stores 0x0100 to the first hardware breakpoint unit at its third (16-bit) register at 0x00000028
* Stores 0x00 to a byte register at 0x00000048 - the purpose for this is not well understood yet but this may be the second hardware breakpoint unit

### Set the program counter to a specific address

```pdi
sts.u32 0x00000004 0x00 0x00 0x00 0x00
```

This writes the program counter, exposed at +0x4, to its POR value

### Run the program to breakpoint

```pdi
stcs reset 0x00
sts.u8 0x0000000a 0x00
stcs r4 0x01
ldcs r3
ldcs r3
```

This sequence does the following:

* With r4 poked, releases reset so that at this stage enters the processor into a debugger-supervised state
* Stores 0x00 to the debug register 0x0000000a which appears to put the processor in run
* Ensures r4 holds the value 0x01 which ensures the debugger engage bit is set
* Loads the status of the processor from r3 (should read as 0x14 the first time)
* Loads the status of the processor again (should read as 0x04 the second time indicating the breakpoint is hit)

### Clean up

```pdi
sts.u16 0x00000028 0x00 0x00
sts.u8 0x00000048 0x00
```

Cleans up after the debug run by clearing all set breakpoints

## Reading processor state

### Read program counter (PC+1)

```pdi
lds.u32 0x00000004
```

### Clean up verification

```pdi
lds.u8 0x00000050
lds.u8 0x0000000b
```

### Read back Stack Pointer + SREG

```pdi
st.u32 ptr 0x0100003d
repeat 0x02
ld *(ptr++)
```

### Verify state

```pdi
ldcs r3
lds.u8 0x010001ca
lds.u8 0x010001c4
```

```{include} single-stepping.md
```
