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

### Turn the debug interface on

```pdi
key debug
ldcs status
```

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

### Set up run-to-address

sts.u32 0x00000020 0x29 0x01 0x00 0x00
sts.u32 0x00000024 0x00 0x00 0x00 0x00
sts.u8 0x00000040 0x00
sts.u8 0x00000040 0x00
sts.u16 0x00000028 0x00 0x01
sts.u8 0x00000048 0x00

### Single-step debugging

```{include} single-stepping.md
```
