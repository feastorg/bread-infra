# Slice Naming Convention

Slice modules follow a structured naming format to remain compact yet descriptive:

```js
Slice_<FUNCTION>_(<ID>)
```

## General Rules

- `<FUNCTION>`: A short, uppercase code that identifies the slice’s primary role (e.g. `TEMP` for templates, `PRTO` for prototyping, `THRM` for thermocouple reading, `DCMT` for DC motor control).
- `<ID>`: A concise identifier used **only when multiple versions** of a slice exist. This may reflect a specific sensor model (e.g. `31855`) for function cards or layout type (e.g. `S2L` for small 2-layer) and controller platform (e.g. `NUCL` for Nucleo) for template boards.

Additional guidance:

- If the slice has **only one known version**, no `<ID>` is required.  
  Example: `Slice_RLHT`
- If a slice is extended or forked into **multiple variants**, suffix the name to indicate:
  - A different sensor or IC (e.g. `31856`)
  - A different layout or platform (e.g. `NANO`, `NUCL`, or `S2L`)

The goal is to balance **descriptive clarity** with **compact naming**, supporting consistent tracking of hardware variants across repositories and documentation.

---

## Variant Naming Patterns

## 🔌 Component-Based Slices

Used when multiple revisions of the function-specific slice exist with different hardware implementations:

| Example            | Meaning                           |
| ------------------ | --------------------------------- |
| `Slice_THRM_6675`  | Thermocouple reader using MAX6675 |
| `Slice_THRM_31855` | Uses MAX31855                     |
| `Slice_THRM_31856` | Uses MAX31856                     |

---

## 🧩 Template/Generic Slices (by layout or controller)

Used for general-purpose template and prototyping slices that vary in size, complexity, or host MCU:

| Example               | Meaning                                             |
| --------------------- | --------------------------------------------------- |
| `Slice_TEMP_NANO_S2L` | Small board, Arduino Nano, 2-layer template         |
| `Slice_TEMP_NUCL_L4L` | Large board, STM32 Nucleo, 4-layer template         |
| `Slice_PRTO_CONN_S2L` | Small 2-layer prototyping board with connectors     |
| `Slice_PRTO_SMT_S2L`  | Small 2-layer prototyping board with SMT components |

**Note**:

- **Template slices** should specify the **host platform** (e.g. `NANO`, `NUCLEO`) as most designs are tightly coupled to the specific MCU footprint.

- **Prototyping slices** (e.g. `PRTO`) should be **platform-agnostic** when possible and designed to accommodate all currently supported platforms (e.g. `NANO` and `NUCLEO32`), unless the design intentionally targets a platform-specific feature or constraint.

- Always include **board dimensions** and **layer count** for hardware selection clarity.

## 🔄 Revisions

A repo name carries no revision. A board's generation and revision ("DCMT
G3 r1") and its release tags (`g3-r1`) are defined in
[Terminology](../terminology.md#generations-revisions-and-interfaces), and
every revision of a design stays in the one repo.

A design that becomes a different product, with a different function, IC or
platform, gets its own `<ID>` and its own repository, as in the patterns
above.

The template repos carried `-r1` and `-r2` suffixes until 2026-11-27, when
they were renamed to follow this rule.
