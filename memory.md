# Memory Map

The ATXMega256A3U PDI controller has the following memory map:

```text
+==============+ <- 0x00000000
|  "reserved"  |
+==============+ <- 0x00800000
| Application  |
|    Section   |
+--------------+ <- 0x00840000
|  Bootloader  |
|    Section   |
+==============+ <- 0x00842000
|   reserved   |
+==============+ <- 0x008C0000
|    EEPROM    |
+==============+ <- 0x008C1000
|   reserved   |
+==============+ <- 0x008E0200
|  Signature   | Two flash pages
|      Row     | (256 * 2)
+==============+ <- 0x008E0600
|   reserved   |
+==============+ <- 0x008F0020
|    Fuses     |
+==============+ <- 0x008F0026
|   reserved   |
+==============+ <- 0x01000000
|  Data Memory |
| (Mapped IO + |
(     SRAM)    |
+==============+ <- 0x02000000
```
