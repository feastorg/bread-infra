# Origin and citation

BREAD began as an open-source hardware project published on the Open Science
Framework (OSF) by Shane Oberloier, Nicholas G. Whisman, Finn Hafting and
Joshua M. Pearce. The Slices and Loaves in `feastorg` continue those designs.

This page is the master citation for every BREADS-compatible repo. Each Slice
or Loaf README links its own OSF page, if it has one, and points here for the
rest.

## How to cite BREAD

Cite the framework paper:

> Shane Oberloier, Nicholas G. Whisman, Finn Hafting, Joshua M. Pearce.
> Open source framework for a Broadly Expandable and Reconfigurable data
> acquisition and automation device (BREAD). *HardwareX* 15 (2023) e00467.
> <https://doi.org/10.1016/j.ohx.2023.e00467>

The paper's title expands the acronym in a different order from
[Terminology](spec/terminology.md). Quote the title as published.

## Related publications

- Finn K. Hafting, Daniel Kulas, Etienne Michels, Sarvada Chipkar, Stefan
  Wisniewski, David Shonnard, Joshua M. Pearce. Modular Open-Source Design of
  Pyrolysis Reactor Monitoring and Control Electronics. *Electronics* 12(24)
  (2023) 4893. <https://doi.org/10.3390/electronics12244893>
- Finn K. Hafting, Alexander W. H. Chin, Jeff T. Hafting, Joshua M. Pearce.
  Moving the Open-Source Broadly Reconfigurable and Expandable Automation
  Device (BREAD) Towards a Supervisory Control and Data Acquisition (SCADA)
  System. *Technologies* 13(4) (2025) 125.
  <https://doi.org/10.3390/technologies13040125>
- Finn Keith Hafting. *The Rise of BREAD: Leveraging Open-Source Process
  Control*. MESc thesis, Electrical and Computer Engineering, The
  University of Western Ontario, 2024. Supervisor: Joshua M. Pearce.
  <https://hdl.handle.net/20.500.14721/36020>

## OSF project

The master project is **BREAD**, <https://osf.io/u2h4g/>. It holds the
framework README and an `okh-manifest.yml`. Slice and Loaf designs sit on OSF
pages that are either components of that project or separate projects linked
from it.

| OSF page | Title on OSF | Relation to u2h4g | `feastorg` repo |
| --- | --- | --- | --- |
| [6aw9m](https://osf.io/6aw9m/) | BREAD Slice - DC Motor Controller (SLC_DCMT) | linked | [Slice_DCMT](https://github.com/feastorg/Slice_DCMT) |
| [pf6gy](https://osf.io/pf6gy/) | BREAD Slice - Relay Heating Element Controller (SLC_RLHT) | component | [Slice_RLHT](https://github.com/feastorg/Slice_RLHT) |
| [q8nkc](https://osf.io/q8nkc/) | BREAD Slice - Stepper Motor Controller (SLC_STEP) | linked | [Slice_STEP](https://github.com/feastorg/Slice_STEP) |
| [d7vks](https://osf.io/d7vks/) | BREAD Slice - Servo Motor Controller (SLC_SERV) | linked | [Slice_SERV](https://github.com/feastorg/Slice_SERV) |
| [5vxws](https://osf.io/5vxws/) | BREAD Slice - 4 Channel Relay (SLC_RLAY) | linked | [Slice_RLAY](https://github.com/feastorg/Slice_RLAY) |
| [j9rh5](https://osf.io/j9rh5/) | BREAD Slice - USB Port (SLC_USBP) | linked | [Slice_USBP](https://github.com/feastorg/Slice_USBP) |
| [742ez](https://osf.io/742ez/) | BREAD Slice -- Analog Reader / FFT (SLC_LVAI) | linked | [Slice_LVAI](https://github.com/feastorg/Slice_LVAI) |
| [sfehu](https://osf.io/sfehu/) | BREAD Slice - Thermocouple Reader (SLC_THRM) | linked | [Slice_THRM_31855](https://github.com/feastorg/Slice_THRM_31855) |
| [9gm5h](https://osf.io/9gm5h/) | BREAD Slice - Field Solar Power (SLC_SOLR) | linked | [Slice_SOLR](https://github.com/feastorg/Slice_SOLR) |
| [m53fu](https://osf.io/m53fu/) | BREAD Slice-- Heating Element Controller (SLC_HEAT) | linked | [Slice_HEAT](https://github.com/feastorg/Slice_HEAT) |
| [2xpnu](https://osf.io/2xpnu/) | BREAD Slice -- Buck Converter / Analog Signal Generator (SLC_BUCK) | linked | [Slice_BUCK](https://github.com/feastorg/Slice_BUCK) |
| [zbg98](https://osf.io/zbg98/) | BREAD Slice - Bioreactor (SPECIALIZED) (SLC_PHDO) | component | [Slice_PHDO](https://github.com/feastorg/Slice_PHDO) |
| [v5327](https://osf.io/v5327/) | BREAD Slice - Template (SLC_TEMP) | component | [Slice_TEMP_NANO_S2L-r1](https://github.com/feastorg/Slice_TEMP_NANO_S2L-r1) |
| [7mk4w](https://osf.io/7mk4w/) | LOAF_x04 Backplane | component | [Loaf_x004](https://github.com/feastorg/Loaf_x004) |
| [nxrtm](https://osf.io/nxrtm/) | LOAF_ESPC - ESP32 Controller | component | [Loaf_ESPT](https://github.com/feastorg/Loaf_ESPT) |
| [a8nk5](https://osf.io/a8nk5/) | BREAD Slice - Audio Analysis (SLC_AAFT) | linked | none |
| [ajmbe](https://osf.io/ajmbe/) | BREAD Slice - +/- 10A Current Sensor (SLC_CR10) | linked | none |
| [xe6cz](https://osf.io/xe6cz/) | BREAD Slice - +/- 20A Current Sensor (SLC_CR20) | linked | none |
| [xpgf8](https://osf.io/xpgf8/) | BREAD Slice - +/- 40A Current Sensor (SLC_CR40) | linked | none |
| [4mzs8](https://osf.io/4mzs8/) | BREAD Slice - Pump Control Board (Specialized) (SLC_PUMP) | linked | none |
| [x4yqj](https://osf.io/x4yqj/) | BREAD LOAF_x08 | component | none |

Slice_DCMT and Slice_RLHT are tied to their pages by the archive snapshots
they carry: `archive/hw_archive/g1-2021-06-08-mtu` matches the date 6aw9m was
created, and `archive/hw_archive/osf_2022-05-19` matches pf6gy. Every other row
is matched by title only; note that LOAF_ESPC on OSF is Loaf_ESPT here.

Slices not in the table have no OSF page that we know of. Other people have
published BREAD Slices on OSF as separate projects that u2h4g does not link;
they are not listed here.

## Licence of the OSF designs

The master project and most of the pages above carry the GNU General Public
License 3.0 on OSF. SLC_PUMP, SLC_HEAT and SLC_BUCK have no licence set on
their OSF pages. The HardwareX paper is open access under CC BY 4.0.
