# What is PDI

## The component in the MCU

What if I told you that PDI was more than just a meer communications protocol? What if I told you that it was a complex state machine, so complex in fact that it could nearly be mistaken for a processor.. Well, I would be telling the truth.

## The instruction set

### LDS

The LDS instruction loads up to 4 bytes of data from a given direct address and sends it back to the host.
The opcode has the form:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | A | A | B | B |

AA and BB follow the [size rules](#size-rules) below

### LD

The LD instruction loads up to 4 bytes of data from the address given by the internal indirect addressing `ptr` register which can only be read by this instruction.
The opcode has the form:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | P | P | B | B |

PP defines an addressing form given by the [pointer rules section](#pointer-rules) below.
BB follows the [size rules section](#size-rules) below

### STS

The STS instruction stores up to 4 bytes of data to a given direct address.
The opcode has the form:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | A | A | B | B |

AA and BB follow the [size rules](#size-rules) below

### ST

The ST instruction stores up to 4 bytes of data to the address given by the internal indirect addressing `ptr` register which can only be directly written to by this instruction.
The opcode has the form:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | P | P | B | B |

PP defines an addressing form given by the [pointer rules section](#pointer-rules) below.
BB follows the [size rules section](#size-rules) below

### Size rules

There are two size types (A and B) in the official protocol documentation.. however, they're identical so we only document them once here. A is always used for address length encoding, and B for data.

The 2-bit value defines the number of bytes that follow the instruction for the specific type of value following.
When present the A value is transmitted first, then the B.

The following table defines the possible bit values and their meanings:

| Value | Meaning |
| :---: |:--------|
|  0 0  | 1 byte  |
|  0 1  | 2 bytes |
|  1 0  | 3 bytes |
|  1 1  | 4 bytes |

### Pointer rules

The pointer register and all access for it are encoded in the LD and ST instructions with the following form:

| Value |      Meaning     |
| :---: |:-----------------|
|  0 0  | *ptr             |
|  0 1  | *(ptr++)         |
|  1 0  | ptr              |
|  1 1  | ptr++ (reserved) |

**NB**: The pointer register is written to by all direct addressing instructions which is undocumented by the datasheets and has a profound impact on the instruction ordering that must be kept.

## Native PDI protocol

## JTAG-PDI protocol
