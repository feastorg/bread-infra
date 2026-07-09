# Slice Concept

A **Slice** is a **Standardized Logic Interface and Capability Element**.

Each Slice contributes a specific capability to a BREAD while presenting
a standard BREADS-compatible interface. A Slice may provide sensing, actuation,
power, interface, integrated control, template, or prototyping capability.

A Slice generally includes:

- a PCB in the Slice mechanical format
- a Slice bus connector and compatible pinout
- local circuitry for its capability
- local MCU or logic when needed
- a `slice.yaml` manifest
- design artifacts and documentation

Slices are combined through a Loaf. The Loaf provides the attachment,
interconnect, power distribution, communication paths, and controller interface
that allow multiple Slices to operate as one BREAD.

