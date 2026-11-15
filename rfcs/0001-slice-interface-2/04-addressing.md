# 04 Addressing

[RFC 0001](README.md) · previous: [03 Bus and MCU site](03-bus.md) · next:
[05 Stop and interlock](05-stop.md)

## Addresses

**ADR-1** A slice's I²C address is

    address = 0x10 + 4 × loaf + slot

giving 0x10–0x1F. *loaf* is the chain position minus 1 (0–3), and *slot* is
0–3, counted from the loaf's CHAIN IN end. The slice reads both from SLOT_ID
at boot.

This replaces compile-time addresses (Slice_RLHT sets 0x13 in `config.h`
today), so CRUMBS' discovery changes to match ([08](08-migration.md)).

## SLOT_ID

![The 18 SLOT_ID bins across full scale: bin 0 is a short, bin 17 is open, and code n = 4 × loaf + slot reads in bin n + 1. The nominal reading of each code sits inside its bin; loaf 0 is codes 0–3 (0x10–0x13), loaf 1 codes 4–7, loaf 2 codes 8–11, loaf 3 codes 12–15.](figures/slot-id-bins.svg)

**ADR-2** The slice MUST pull SLOT_ID up with 12.7 k, 1 %, to its ADC
reference, with 100 nF on the pin, so the reading is ratiometric.

**ADR-3** The loaf MUST present code *n* = 4 × loaf + slot to a slot as
R<sub>*n*</sub> from the table below (1 %, E96) from SLOT_ID to ground, through
a switch of 10 Ω or less, and MUST leave SLOT_ID open when it sees no grounded
position line.

In the reference circuit, each position line drives an inverting FET with a
pull-up to VIO, whose output turns on that position's four slot FETs (one per
slot, each in series with its R<sub>*n*</sub>). The FETs MUST have
R<sub>DS(on)</sub> ≤ 10 Ω at V<sub>GS</sub> = 3.0 V. The network runs from VIO,
so it works whether or not the loaf's own supply is up.

**ADR-4** Firmware divides full scale into 18 equal bins and takes bin
⌊18 × reading⌋, with the reading as a fraction of full scale. Bin 0 is a short
and bin 17 is open (no position line grounded, or no loaf); code *n* reads in
bin *n* + 1. A slice MUST require matching reads over at least 50 ms, and MUST
NOT join the bus on bin 0 or bin 17.

| Code *n* | Loaf / slot | Address | R<sub>*n*</sub> (E96, 1 %) | Nominal reading | Bin (fraction of full scale) |
| ---: | :---: | :---: | ---: | ---: | :---: |
| 0 | 0 / 0 | 0x10 | 1.15 k | 0.083 | 1/18 – 2/18 |
| 1 | 0 / 1 | 0x11 | 2.05 k | 0.139 | 2/18 – 3/18 |
| 2 | 0 / 2 | 0x12 | 3.09 k | 0.196 | 3/18 – 4/18 |
| 3 | 0 / 3 | 0x13 | 4.22 k | 0.249 | 4/18 – 5/18 |
| 4 | 1 / 0 | 0x14 | 5.62 k | 0.307 | 5/18 – 6/18 |
| 5 | 1 / 1 | 0x15 | 7.15 k | 0.360 | 6/18 – 7/18 |
| 6 | 1 / 2 | 0x16 | 9.09 k | 0.417 | 7/18 – 8/18 |
| 7 | 1 / 3 | 0x17 | 11.3 k | 0.471 | 8/18 – 9/18 |
| 8 | 2 / 0 | 0x18 | 14.3 k | 0.530 | 9/18 – 10/18 |
| 9 | 2 / 1 | 0x19 | 17.8 k | 0.584 | 10/18 – 11/18 |
| 10 | 2 / 2 | 0x1A | 22.6 k | 0.640 | 11/18 – 12/18 |
| 11 | 2 / 3 | 0x1B | 28.7 k | 0.693 | 12/18 – 13/18 |
| 12 | 3 / 0 | 0x1C | 38.3 k | 0.751 | 13/18 – 14/18 |
| 13 | 3 / 1 | 0x1D | 52.3 k | 0.805 | 14/18 – 15/18 |
| 14 | 3 / 2 | 0x1E | 78.7 k | 0.861 | 15/18 – 16/18 |
| 15 | 3 / 3 | 0x1F | 140 k | 0.917 | 16/18 – 17/18 |

### Margin

The nominal reading is R<sub>*n*</sub> / (12.7 k + R<sub>*n*</sub>). Taking
each resistor at ±1 % and the switch at 0–10 Ω, the worst-case reading stays
at least 2.08 % of full scale inside its bin (code 8 is the tightest), before
ADC error (*estimate*). That is about 21 counts on a 10-bit ADC, so it holds on
10-, 12- and 14-bit converters. The best E24 set gives only 1.51 %, which is
why the table uses E96.

The figure comes from this calculation; rerun it if a value changes:

```python
RP, TOL, RDS = 12.7e3, 0.01, (0.0, 10.0)
R = [1.15e3, 2.05e3, 3.09e3, 4.22e3, 5.62e3, 7.15e3, 9.09e3, 11.3e3,
     14.3e3, 17.8e3, 22.6e3, 28.7e3, 38.3e3, 52.3e3, 78.7e3, 140e3]
worst = 1.0
for n, rb in enumerate(R):
    rs = [rb * (1 + a) + d for a in (-TOL, TOL) for d in RDS]
    ps = [RP * (1 + b) for b in (-TOL, TOL)]
    lo = min(r / (p + r) for r in rs for p in ps)
    hi = max(r / (p + r) for r in rs for p in ps)
    worst = min(worst, lo - (n + 1) / 18, (n + 2) / 18 - hi)
print(f"worst-case margin {worst * 100:.2f} % of full scale")  # 2.08
```

## Reserved addresses

**ADR-5** Qwiic modules live on the controller's own Qwiic bus, so the slice
bus carries only slices and direct-mode sensors. Direct-mode sensors MUST NOT
use:

- the slice band, 0x10–0x1F;
- CRUMBS' avoid list, including 0x61 (the SMBus ARP address);
- 0x60–0x6F, kept for Atlas EZO modules in direct mode. An EZO-DO, whose
  default is 0x61, gets a new address before it goes on the bus direct.
