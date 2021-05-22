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

### LDCS

The LDCS instruction allows reading of the PDI internal registers. PDI uses a 16-register stackless "CPU" (it's not a CPU but close enough for this). See [PDI registers](#pdi-registers) below for more information on these registers.
They are encoded numerically in order in the bottom half of the instruction, which has the form:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | R | R | R | R |

RRRR defines which register to read.

### STCS

The STCS instruction allows writing to the PDI internal registsers. See [PDI registers](#pdi-registers) below for more information on these registers.
They are encoded numerically inorder in the bottom half of the instruction, which has the form:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | R | R | R | R |

RRRR defines which register to write.

### Size Rules

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

### Pointer Rules

The pointer register and all access for it are encoded in the LD and ST instructions with the following form:

| Value |      Meaning     |
| :---: |:-----------------|
|  0 0  | *ptr             |
|  0 1  | *(ptr++)         |
|  1 0  | ptr              |
|  1 1  | ptr++ (reserved) |

**NB**: The pointer register is written to by all direct addressing instructions which is undocumented by the datasheets and has a profound impact on the instruction ordering that must be kept.

### PDI Registers

The PDI "CPU" has 16 internal 8-bit registers.
Some of these are documented, others are "reserved" (they may actually be unused, but it's unclear at this time if they are or if they're not just additional special-function CSRs).
All of these registers are CSRs that define status for and control how debug and programming will run.

| Register# |  Alias  |
| :-------: |:--------|
|  0 0 0 0  | status  |
|  0 0 0 1  | reset   |
|  0 0 1 0  | control |
|  0 0 1 1  | r3      |
|  0 1 0 0  | r4      |

The rest are "reserved".

#### Status Register

The status register's bits have the following meanings assigned to them:

| 8 | 7 | 6 | 5 | 4 |   3   |   2   | 1 |
|:-:|:-:|:-:|:-:|:-:|:-----:|:-----:|:-:|
| - | - | - | - | - | DBGEN | NVMEN | - |
| R | R | R | R | R |  R/W  |  R/W  | R |
| 0 | 0 | 0 | 0 | 0 |   0   |   0   | 0 |

The bottom row defines the reset state of this register.

* NVMEN is the Flash/EEPROM Non-Voltile Memory access enable
* DBGEN is the debugger PDI component enable

These bits cannot be written high - this operation is acomplished using the key instruction.
Writing a 0 to an enable bit disables that specific function, writing a 1 preserves its current state.

#### Reset Register

The reset register is both a control and status register. It has two meanings.

As a control register (write) it means:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|             RESET             |
|              R/W              |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

As a status register (read) it means:

| 8 | 7 | 6 | 5 | 4 | 3 | 2 |   1   |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-----:|
| - | - | - | - | - | - | - | RESET |
| R | R | R | R | R | R | R |  R/W  |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |   0   |

Writing 0x59 to this register puts the device in reset, wiht a caviat as given below.
Writing to a value other than this (such as 0) takes the device back out of reset.

When DBGEN is 1 in the status register, the operation of this register is modified to, instead of causing a full reset, only cause a device halt. This is how pause/resume is acomplished in combination with r3/r4.
When not held in reset-pause by this register, it is still possible for the main CPU to not be running as a result of r3/r4 state. This is covered in their documentation sections.

## Native PDI protocol

## JTAG-PDI protocol
