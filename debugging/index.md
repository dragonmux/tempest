```{toctree}
:hidden:
:glob:

*
```

# Debugging

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
