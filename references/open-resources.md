# Free and open resources for advanced PCB design

Versions and links checked 2026-10-23. Descriptions are our own one-line summaries.

## KiCad

| Resource | What it is |
|---|---|
| [KiCad 10.0 release notes](https://www.kicad.org/blog/2026/03/Version-10.0.0-Released/) | 10.0.0 shipped 2026-03-20: design variants, time-domain length tuning, design blocks, a graphical DRC-rule editor, Allegro/PADS/gEDA importers. **Latest stable at snapshot: 10.0.7** (tag 2026-10-06). |
| [docs.kicad.org](https://docs.kicad.org/) | Official manuals for 10.0 (current), 9.0, 8.0, 7.0 and nightly |
| [kicad-cli reference (10.0)](https://docs.kicad.org/10.0/en/cli/cli.html) | DRC/ERC, Gerber/ODB++/IPC-2581/STEP export, rendering, file upgrade — the basis of CI for boards. Note `pcb drc` arrived in 8.0; 7.0's CLI is export-only. |
| [IPC API for add-on developers](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/) | The new automation API (since 9.0), protobuf over a socket. Needs the GUI running in 9/10; headless use is planned for 11. |
| [kicad-python](https://pypi.org/project/kicad-python/) | Official Python client for the IPC API (0.8.0, Aug 2026) |
| [SWIG `pcbnew` bindings](https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/) | The classic Python module this repo's scripts use. Deprecated since 9.0, removal planned for 11.0 — port long-lived tools to the IPC API. |

## Signal integrity, power integrity, EMC

| Resource | What it is | Cost |
|---|---|---|
| [TI SPRAAR7 — High-Speed Interface Layout Guidelines](https://ti.com/lit/spraar7) | Practical rules for USB 2/3, PCIe, SATA, HDMI, SGMII, CSI: pair spacing, via stubs and back-drilling, sample 6/8/10-layer stackups, ESD placement | Free PDF |
| [AMD UG583 — UltraScale PCB Design Guide](https://docs.amd.com/r/en-US/ug583-ultrascale-pcb-design) | The most thorough free board-design guide around: PDN, DDR3/4, LPDDR4/4x/5 topologies, multi-gigabit transceivers, PCIe/USB/Ethernet | Free |
| [ADI AN-1142 — High-Speed ADC PCB Layout](https://www.analog.com/en/resources/app-notes/an-1142.html) | Mixed-signal layout: exposed-pad grounding, decoupling, why not to split grounds | Free |
| [Sierra Circuits design guides](https://www.protoexpress.com/pcb-design-guides/) | ~30 e-books incl. a 115-page high-speed guide, HDI/UHDI, stackups, vias, RF, KiCad step-by-step | Free (form) |
| [Eric Bogatin — Signal Integrity Journal columns](https://www.signalintegrityjournal.com/blogs/4-eric-bogatin-signal-integrity-journal-technical-editor/post/1539-bogatins-20-rules-for-engineers) | Rules of thumb and estimation from the field's best-known teacher; he also launched a free 25-module "Transmission Lines 101" masterclass in 2025 ([announcement](https://www.signalintegrityjournal.com/articles/3944-the-eecosystem-and-professor-dr-eric-bogatin-launch-free-masterclass-for-electronics-engineers)) | Free |
| [Rick Hartley — "How to Achieve Proper Grounding"](https://resources.altium.com/p/us-how-to-achieve-proper-grounding-rick-hartley-expert-live-training) | The classic talk on return paths and fields; watch it before your first 4-layer board | Free |
| [Phil Salmony (Phil's Lab) articles](https://resources.altium.com/experts/phil-salmony) | DDR with FPGAs, crosstalk, USB-C PD; his YouTube channel walks through complete KiCad designs | Free |
| [Robert Feranec / FEDEVEL](https://robert.fedevel.com/other/about-robert) | Long-form layout interviews and walkthroughs on YouTube (academy courses are paid) | Free videos |
| Saturn PCB Toolkit | Windows freeware calculator: impedance, current capacity (IPC-2152), via properties, crosstalk | Freeware |
| [JLCPCB capabilities](https://jlcpcb.com/capabilities/PCB-capabilities) | A concrete, published set of fab limits to design against (trace/space, vias, HDI, impedance tolerance) | Free |

## Open-source EDA and design automation

| Tool | Version | Licence | Use it for |
|---|---|---|---|
| [KiCad](https://www.kicad.org/) | 10.0.7 | GPL-3 | Schematic + layout, the base of this repo |
| [Freerouting](https://github.com/freerouting/freerouting) | 2.5.0 (2026-10-05) | GPL-3 | Autorouting via Specctra DSN/SES; 2.5 adds native CLI binaries and a KiCad-IPC mode. Ships its own **PCBench** fixture set of ~1,150 KiCad-10 boards in `scripts/benchmark/fixtures/` |
| [tscircuit](https://github.com/tscircuit/tscircuit) | 0.0.3012 | MIT | Boards as TypeScript/React code, with its own autorouter |
| [atopile](https://github.com/atopile/atopile) | 0.15.9 | MIT | Code-first hardware language that targets KiCad |
| [SKiDL](https://github.com/devbisme/skidl) | 2.2.3 | MIT | Netlists in Python |
| [Horizon EDA](https://github.com/horizon-eda/horizon) | 2.7.2 | GPL-3 | Standalone EDA built around a curated parts pool |
| [LibrePCB](https://librepcb.org/) | 2.1.1 | GPL-3 | Beginner-friendly standalone EDA |
| [openEMS](https://docs.openems.de/intro.html) | 0.37.0 | GPL-3 | 3D FDTD field solver: verify impedance, S-parameters, antennas |
| [ngspice](https://ngspice.sourceforge.io/) | 47 | BSD-3 | SPICE engine used by KiCad's simulator |
| [Qucs-S](https://github.com/ra3xdh/qucs_s) | 26.1.1 | GPL | Simulator GUI over ngspice/Xyce; good for RF matching |
| [KiBot](https://github.com/INTI-CMNB/KiBot) | 1.9.1 | AGPL-3 | One-YAML release automation for KiCad projects |
| [InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom) | 2.12.0 | MIT | Assembly-friendly interactive BOM |
| [KiCadRoutingTools](https://github.com/drandyhaas/KiCadRoutingTools) | 0.23.7 | MIT | Python/Rust routing helpers |
| [kicad-happy](https://github.com/aklofas/kicad-happy) | — | MIT | AI-agent skills for KiCad review, EMC checks, SPICE and fab prep |

## Benchmarks and datasets

| Benchmark | What it is |
|---|---|
| Freerouting PCBench (in the [Freerouting repo](https://github.com/freerouting/freerouting)) | ~1,150 boards with raw/unrouted/ground-truth files, four difficulty tiers, generated with KiCad 10.0.2. Freerouting reports ~75 % clean overall but ~49 % on 6+ layer boards. |
| [PCB-Bench](https://github.com/digailab/PCB-Bench) (ICLR 2026) | ~3.7k QA items on placement/routing + 174 real projects |
| [PCBWorld](https://arxiv.org/html/2607.05915v1) | KiCad-engine routing environment, 20k synthetic + 679 real boards |
| DeepPCB vs Quilter ([write-up](https://deeppcb.ai/deeppcb-vs-quilter-open-source-routing-compared-2026/)) | Vendor-published comparison on three open boards — reproduced with Freerouting in this repo's [benchmark](../benchmark/RESULTS.md) |

## MIT

See [curriculum/mit-ocw.md](../curriculum/mit-ocw.md). Outside OCW, [pcb.mit.edu](https://pcb.mit.edu/) (CC BY-SA 4.0) is the most directly useful MIT PCB material.
