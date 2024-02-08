# What is PDI

## The component in the MCU

What if I told you that PDI was more than just a meer communications protocol? What if I told you that it was a
complex state machine, so complex in fact that it could nearly be mistaken for a processor.. Well, I would be
telling the truth.

## The instruction set

All values transmitted as part of instructions and their effects are transmitted in LSB-first (Little Endian)
byte order.

### LDS

The LDS instruction loads up to 4 bytes of data from a given direct address and sends it back to the host.
The opcode has the form:

```{wavedrom}
{
	"reg":
	[
		{"name": "B", "bits": 2, "type": 2, "attr": "sizeB"},
		{"name": "A", "bits": 2, "type": 3, "attr": "sizeA"},
		{"name": 0, "bits": 1},
		{"name": 0x0, "bits": 3, "type": 4, "attr": "opcode (0x0)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

A and B follow the [size rules](#size-rules) below.

### LD

The LD instruction loads up to 4 bytes of data from the address given by the internal indirect addressing `ptr`
register which can only be read by this instruction.
The opcode has the form:

```{wavedrom}
{
	"reg":
	[
		{"name": "B", "bits": 2, "type": 2, "attr": "sizeB"},
		{"name": "P", "bits": 2, "type": 5, "attr": "ptr mode"},
		{"name": 0, "bits": 1},
		{"name": 0x1, "bits": 3, "type": 4, "attr": "opcode (0x2)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

P defines an addressing form given by the [pointer rules section](#pointer-rules) below.
B follows the [size rules section](#size-rules) below.

### STS

The STS instruction stores up to 4 bytes of data to a given direct address.
The opcode has the form:

```{wavedrom}
{
	"reg":
	[
		{"name": "B", "bits": 2, "type": 2, "attr": "sizeB"},
		{"name": "A", "bits": 2, "type": 3, "attr": "sizeA"},
		{"name": 0, "bits": 1},
		{"name": 0x2, "bits": 3, "type": 4, "attr": "opcode (0x4)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

A and B follow the [size rules](#size-rules) below.

### ST

The ST instruction stores up to 4 bytes of data to the address given by the internal indirect addressing `ptr`
register which can only be directly written to by this instruction.
The opcode has the form:

```{wavedrom}
{
	"reg":
	[
		{"name": "B", "bits": 2, "type": 2, "attr": "sizeB"},
		{"name": "P", "bits": 2, "type": 5, "attr": "ptr mode"},
		{"name": 0, "bits": 1},
		{"name": 0x3, "bits": 3, "type": 4, "attr": "opcode (0x6)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

P defines an addressing form given by the [pointer rules section](#pointer-rules) below.
B follows the [size rules section](#size-rules) below.

### LDCS

The LDCS instruction allows reading of the PDI internal registers. PDI uses a 16-register stackless "CPU" (it's not a
CPU but close enough for this). See [PDI registers](#pdi-registers) below for more information on these registers.
They are encoded numerically in order in the bottom half of the instruction, which has the form:

```{wavedrom}
{
	"reg":
	[
		{"name": "PDI register", "bits": 4, "type": 6, "attr": "parameter"},
		{"name": 0, "bits": 1},
		{"name": 0x4, "bits": 3, "type": 4, "attr": "opcode (0x8)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

The opcode's parameter defines which register to read.

### REPEAT

The REPEAT instruction specifies that the next instruction(!) is to be repeated N times after initial execution,
where N is specified in the bytes following this instruction.
The opcode has the following form:

```{wavedrom}
{
	"reg":
	[
		{"name": "B", "bits": 2, "type": 2, "attr": "sizeB"},
		{"name": 0, "bits": 3},
		{"name": 0x5, "bits": 3, "type": 4, "attr": "opcode (0xa)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

B follows the [size rules section](#size-rules) below and specifies how many bytes follow this instruction to
be 0-padded and loaded into the PDI repeat register

### STCS

The STCS instruction allows writing to the PDI internal registsers. See [PDI registers](#pdi-registers) below for
more information on these registers.
They are encoded numerically inorder in the bottom half of the instruction, which has the form:

```{wavedrom}
{
	"reg":
	[
		{"name": "PDI register", "bits": 4, "type": 6, "attr": "parameter"},
		{"name": 0, "bits": 1},
		{"name": 0x6, "bits": 3, "type": 4, "attr": "opcode (0xc)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

The opcode's parameter defines which register to write.

### KEY

The KEY instruction is used to unlock special functions of the PDI controller.
The opcode has the following form:

```{wavedrom}
{
	"reg":
	[
		{"name": 0, "bits": 5},
		{"name": 0x7, "bits": 3, "type": 4, "attr": "opcode (0xe)"},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

8 bytes follow the key instruction and provide a special unlocking value for the feature you wish to unlock.
There are two known key value constants which are:

* NVM - `0x1289ab45cdd888ff`
* Debug - `0x3a212dd49f7c8121`

These are sent little endian and look like this on the wire:

```{wavedrom}
{
	"signal":
	[
		{
			"name": "clk",
			"wave": "P...................................................................................................",
			"phase": 0.5
		},
		{
			"name": "data",
			"wave": "103.......4103.......4103.......4103.......4103.......4103.......4103.......4103.......4103.......41",
			"data": ["ff", 0, "88", 0, "d8", 0, "cd", 1, "45", 1, "ab", 1, "89", 1, "12", 0]
		},
	],
	"config": {"hscale": 1}
}
```

```{wavedrom}
{
	"signal":
	[
		{
			"name": "clk",
			"wave": "P...................................................................................................",
			"phase": 0.5
		},
		{
			"name": "data",
			"wave": "103.......4103.......4103.......4103.......4103.......4103.......4103.......4103.......4103.......41",
			"data": ["21", 0, "81", 0, "7c", 1, "9f", 0, "d4", 0, "2d", 0, "21", 0, "3a", 0]
		},
	],
	"config": {"hscale": 1}
}
```

### Size Rules

There are two size types (A and B) in the official protocol documentation.. however, they're identical so we
only document them once here. A is always used for address length encoding, and B for data.

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

```{note}
The pointer register is written to by all direct addressing instructions which is undocumented by the datasheets and
has a profound impact on the instruction ordering that must be kept.
```

### PDI Registers

The PDI "CPU" has 16 internal 8-bit registers.
Some of these are documented, others are "reserved" (they may actually be unused, but it's unclear at this time if
they are or if they're not just additional special-function CSRs).
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

```{wavedrom}
{
	"reg":
	[
		{"name": "-", "bits": 1, "attr": ["R", "0"]},
		{"name": "NVMEN", "bits": 1, "attr": ["R/W", "0"]},
		{"name": "DBGEN", "bits": 1, "attr": ["R/W", "0"]},
		{"name": "-", "bits": 5, "attr": ["R", "0"]},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

The bottom row defines the reset state of this register.

* NVMEN is the Flash/EEPROM Non-Voltile Memory access enable
* DBGEN is the debugger PDI component enable

These bits cannot be written high - this operation is acomplished using the key instruction.
Writing a 0 to an enable bit disables that specific function, writing a 1 preserves its current state.

#### Reset Register

The reset register is both a control and status register. It has two meanings.

As a control register (write) it means:

```{wavedrom}
{
	"reg":
	[
		{"name": "RESET", "bits": 8, "attr": ["R/W", "0"]},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

As a status register (read) it means:

```{wavedrom}
{
	"reg":
	[
		{"name": "RESET", "bits": 1, "attr": ["R/W", "0"]},
		{"name": "-", "bits": 7, "attr": ["R", "0"]},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

Writing 0x59 to this register puts the main processor into reset as if asserting the ~RESET pin,
with a caviat as given below.
Writing to a value other than this (such as 0) takes the device back out of reset.

When DBGEN is 1 in the status register, the operation of this register is modified to, instead of causing a full reset,
only cause a device halt. This is how pause/resume is acomplished in combination with r3/r4.
When not held in reset-pause by this register, it is still possible for the main CPU to not be running as a result of
r3/r4 state. This is covered in their documentation sections.

#### Control Register

This control register is used to control turn-around timings for the [native physical protocol](#native-pdi-protocol).
The register's bits have the following meanings assigned to them:

```{wavedrom}
{
	"reg":
	[
		{"name": "GUARDTIME", "bits": 3, "attr": ["R/W", "0"]},
		{"name": "-", "bits": 5, "attr": ["R", "0"]},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

* GUARDTIME specifies the number of idle bits of guard time inserted between PDI RX and TX direction changes.
  It defaults to 128 bits, and what the bits mean is determined by the table below:

| GUARDTIME | number of idle bits |
| :-------: |:--------------------|
|   0 0 0   | 128                 |
|   0 0 1   | 64                  |
|   0 1 0   | 32                  |
|   0 1 1   | 16                  |
|   1 0 0   | 8                   |
|   1 0 1   | 4                   |
|   1 1 0   | 2                   |
|   1 1 1   | 2                   |

#### Register r3

This status regsiter indicates the current state of the debug engine when enabled (otherwise it reads as 0)

```{wavedrom}
{
	"reg":
	[
		{"name": "-", "bits": 3, "attr": ["R", "0"]},
		{"name": "PAUSE", "bits": 1, "attr": ["R", "0"]},
		{"name": "RESET", "bits": 1, "attr": ["R", "0"]},
		{"name": "-", "bits": 3, "attr": ["R", "0"]},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

* The RESET bit indicates whether the processor is currently held in reset and is sort-of a duplicate of the RESET
  bit from the reset CSR.
* The PAUSE bit indicates whether the processor is currently held in execution pause.

#### Register r4

This control register determines whether the debug engine is enabled

```{wavedrom}
{
	"reg":
	[
		{"name": "ENABLE", "bits": 1, "attr": ["R/W", "0"]},
		{"name": "-", "bits": 7, "attr": ["R", "0"]},
	],
	"config": {"hspace": 500, "bits": 8}
}
```

## Native PDI protocol

## JTAG-PDI protocol

This section assumes exiting basic working knowledge of the JTAG standard (IEEE 1149.1-2013). This will only cover
how the protocol works with the TAP and sits above it.

The JTAG-encapsulated form of PDI is rather interesting in construction as it consists of a few elements, some of
which caused by taking a half-duplex, single-data-wire bi-directional protocol with turn-arounds and re-mapping it
to a full-duplex comms protocol. The first of the elements is how ID'ing the device works, the second is entering PDI
mode, and the third is the encapsulation of the PDI data.

### The TAP instruction register

On all Atmel devices implementing JTAG-PDI, the IR is 4 bits wide and defines the following instructions:

| IR Code |     Meaning     |
| :-----: |:----------------|
|   0x0   | Unassigned      |
|   0x1   | External Test   |
|   0x2   | Sample/Pre-load |
|   0x3   | IDCode          |
|   0x4   | Clamp           |
|   0x5   | High-Z          |
|   0x6   | Unassigned      |
|   0x7   | PDI Comms       |
|   0x8   | Unassigned      |
|   0xA   | Unassigned      |
|   0xB   | Unassigned      |
|   0xC   | Unassigned      |
|   0xD   | Unassigned      |
|   0xE   | Unassigned      |
|   0xF   | Bypass          |

Of this table, we only really care about 3 instructions - IDCode (0x3), PDI (0x7), and Bypass (0xF).
The device when TAP reset, enters IDCode by default.

### Identification (IR = IDCode)

The first thing to do when starting a conversation over JTAG is to perform an IDCode to find out what the part is.
With the TAP IR loaded with IDCode, we then expect a value in the following format to be read:

```{wavedrom}
{
	"reg":
	[
		{"name": 1, "bits": 1},
		{"name": "Manufacturer ID", "bits": 11},
		{"name": "Part Number", "bits": 16},
		{"name": "Version", "bits": 4},
	],
	"config": {"hspace": 675, "bits": 32}
}
```

Bit 0 listed here is the constant 1.

The following are a list of known values and the chips they belong to:

|   ID Code   |  Part Number  |
|:-----------:|:--------------|
|  0x6964203F | ATXMega64A3U  |
|  0x6974203F | ATXMega128A3U |
|  0x6974403F | ATXMega192A3U |
|  0x6984203F | ATXMega256A3U |

### PDI Mode (IR = PDI)

Once you have identified a device and confirmed it definitely implements PDI, issue the PDI Comms instruction to the
TAP. This will (until touching IR again) enter PDI mode and drop the TAP into JTAG-PDI mode. From here on in, you can
ignore the TAP completely save for clocking data in and out of the 9-bit register that is now connected between TDI
and TDO.

Of importance to note, the PDI register in the Atmel literature is talked about as if it's a single shift-register
between TDI and TDO, however it it may be helpful to think of it as more like two seperate shift registers - one
connected to TDI and one to TDO  - for the purpose of the exchanges had.

#### PDI Frame Format

PDI data entering and leaving the PDI TAP register has the following format:

| LSB |   |   |   |   |   |   |   | MSB |
|:---:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:---:|
|  0  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |  P  |

This is sent LSB first.

This encapsulation defines 3 special character values of note to emulate certain aspects of the native protocol and
handle that this is full-duplex comms:

* the Break character: 0xBB + P1
* the Delay character: 0xDB + P1
* the Empty character: 0xEB + P1

"+ P1" in the above refers to the parity bit being set to generate a parity error.
The bit transitions for communications to TDI must be performed on the TCK falling edge, and TDO sampled on the rising.

#### The conversation, a worked example

JTAG-PDI does two important things to handle being a full-duplex protocol, the first is that the **target's controller**
will send Empty characters while waiting for more imput and and the **programmer** must use the NUL byte as a dummy
character when expecting the target to send data back. It is important that the programmer not generate parity errors
as this triggers a PDI transaction abort.

In practice this looks a bit like:

```{mermaid}
sequenceDiagram
	participant Programmer
	participant Target
	Programmer-->>Target: LDCS status, m1
	Target-->>Programmer: EMPTY
	Note right of Target: These happen simultaneously<br />with the reply on TDO<br />as you send the request on TDI
	Programmer->>Target: DUMMY (0x00)
	Target-->>Programmer: 0x00
```

In this example, we ask the target for its PDI status, and get the answer '0'
(neither programming nor debug mode enabled).
