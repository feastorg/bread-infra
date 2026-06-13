# bread-infra TODO

## GRAIN

- [ ] Decide what GRAIN is an acronym for (or confirm it is not one — it may
      just be a plain English word in the BREAD food-metaphor hierarchy).

## CRUST

- [ ] Define what CRUST will mean as a hardware class. Current thinking:
      PCBs with very little or no active components — passive converters,
      signal adapters, connector breakouts, level-shift boards, etc. Needs
      a formal definition before the class is introduced.
- [ ] Decide whether CRUST is a sub-category of GRAIN (e.g. `category: crust`
      inside grain.yaml) or a separate top-level manifest type with its own
      `crust.yaml` and schema.
- [ ] Repurpose the empty `spec/crust/` directory (currently unused after
      `spec/grain/` was created from it) or remove it once CRUST is defined.
