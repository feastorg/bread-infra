# Slice Concept

This page introduces Slices within BREADS.

For the full terminology reference, see [Terminology](../terminology.md).

## What is a Slice?

A **Slice** is a **Standardized Logic Interface and Capability Element**.

A Slice is a BREADS-compatible capability module used to build the functional
core of a BREAD. Slices add capabilities such as sensing, actuation,
power handling, interface support, integrated behavior, template support, or
prototyping support.

Slices are designed to work with a Loaf, which provides the attachment,
interconnect, power, communication paths, and controller interface needed to
combine multiple Slices into one BREAD.

## What BREADS defines for Slices

BREADS defines the compatibility expectations that let Slices work together:

- mechanical envelope and mounting conventions
- Slice bus connector and pinout expectations
- power and logic-voltage expectations
- communication interface conventions
- manifest and documentation expectations
- artifact and validation expectations

## Slice Categories

Current Slice categories:

1. **Actuation**: output modules that drive components or physical processes.
2. **Sensing**: input modules that measure physical, chemical, or electrical
   conditions.
3. **Integrated**: modules that combine sensing and actuation for a specific
   closed-loop or multi-function capability.
4. **Power**: modules that convert, condition, switch, or distribute power.
5. **Interface**: modules that connect the BREAD to external equipment
   or expose additional device interfaces.
6. **Template**: base designs for new Slice development.
7. **Prototype**: general-purpose boards for experimenting, breakout work, or
   early hardware development.

## Current Slice Examples

| Name | Type | Notes |
|---|---|---|
| [Slice_TEMP_NANO_S2L-r2](https://github.com/feastorg/Slice_TEMP_NANO_S2L-r2) | Template | 70x100mm 2-layer Nano template |
| [Slice_DCMT](https://github.com/feastorg/Slice_DCMT) | Actuation | DC motor driver |
| [Slice_RLAY](https://github.com/feastorg/Slice_RLAY) | Actuation | 4-channel relay |
| [Slice_SERV](https://github.com/feastorg/Slice_SERV) | Actuation | Servo controller |
| [Slice_STEP](https://github.com/feastorg/Slice_STEP) | Actuation | Stepper motor driver carrier |
| [Slice_STPC](https://github.com/feastorg/Slice_STPC) | Actuation | Stepper motor controller carrier |
| [Slice_HEAT](https://github.com/feastorg/Slice_HEAT) | Integrated | DC heating element controller |
| [Slice_RLHT](https://github.com/feastorg/Slice_RLHT) | Integrated | Relay heater controller |
| [Slice_BUCK](https://github.com/feastorg/Slice_BUCK) | Power | Buck converter / analog signal generator |
| [Slice_SOLR](https://github.com/feastorg/Slice_SOLR) | Power | Field solar power |
| [Slice_LVAI](https://github.com/feastorg/Slice_LVAI) | Sensing | Low-voltage analog input reader |
| [Slice_THRM_31855](https://github.com/feastorg/Slice_THRM_31855) | Sensing | Thermocouple reader |
| [Slice_IAQM](https://github.com/feastorg/Slice_IAQM) | Sensing | Industrial air quality monitor |
| [Slice_LOAD](https://github.com/feastorg/Slice_LOAD) | Sensing | Load cell amplifier |
| [Slice_AOEM](https://github.com/feastorg/Slice_AOEM) | Sensing | Atlas Scientific OEM carrier |
| [Slice_LEPD](https://github.com/feastorg/Slice_LEPD) | Sensing | LED-photodiode photometer |
| [Slice_USBP](https://github.com/feastorg/Slice_USBP) | Interface | USB passthrough |

