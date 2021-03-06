```{toctree}
:hidden:

pdi
memory
programming
debugging/index
license
contributors

```

# Tempest JTAG-PDI RE project

## What is Tempest

Tempest is the Atmel JTAG-PDI protocol documentation and RE project.

## What does this contain

This project contains documentation on the JTAG-PDI protocol used by many of the ATXMega series and similar processors.
It documents both the program, and debug components with the intention of providing a clean source of documentation for 3rd party implementations of PDI.

The goal is to allow for a full Open-Source implementation of program and debug tooling for these chips thereby eliminating the need/reliance on Windows-only vendor tools for FOSS projects.

## Table of contents

* [What is PDI](pdi.md)
* [Memory Map](memory.md)
* [Programming Interface](programming.md)
* [Debug Interface](debugging/index.md)
  * [Getting started](debugging/index.md#getting-started)
  * [Reading processor state](debugging/index.md#reading-processor-state)
  * [Single-stepping](debugging/index.md#single-stepping)

## Licensing

This project is licensed under the Creative Commons [CC-BY-SA](https://creativecommons.org/licenses/by-sa/2.0/) and can be found in [LICENSE](license.md)

## Contributors

See [contributors](contributors.md) for a complete list of project contibutors
