# Loaf

A **Loaf** is a **Local Operations Attachment Frame**.

A Loaf is the attachment and interconnect layer that lets multiple Slices
operate together as one BREAD. It is not the complete device by itself;
the complete device is the BREAD.

For the full terminology reference, see [Terminology](../terminology.md).

## Concept

A Loaf provides some combination of:

- physical attachment for Slices
- backplane, carrier, chassis, or wiring structure
- shared power distribution
- communication paths between Slices and the controller
- controller interface circuitry, headers, or cabling
- enclosure, mounting, service, or safety interfaces

The controller may be an SBC, MCU, PC, or another compute element that can
speak the required BREADS communication interface and has sufficient resources
to operate the BREAD. The controller may be integrated into the Loaf or
connected through it, but a controller alone is not a Loaf unless it also
provides the Loaf attachment/interconnect role.

## Relationship To Other Parts

```text
BREADS = compatibility standard
BREAD  = complete device
Loaf   = attachment/interconnect layer
Slice  = capability module attached through the Loaf
Grain  = adjacent support hardware
```

## Design Direction

Loaf designs should make it clear how Slices connect, how power is distributed,
how the controller communicates with the Slice set, and what mechanical context
the assembled BREAD expects.
