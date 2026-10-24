# Bounties, prizes, and paid work for PCB design

Snapshot taken **2026-10-23**. Deadlines move and contests get cancelled — check each official page before you invest time. Status labels:

- **OPEN** — official page fetched on the snapshot date shows a future deadline
- **LIKELY OPEN** — confirmed via a secondary source or an undated official page
- **EXPIRED** — listed because it recurs or still has value as a practice target

## Bottom line

- There is **no active cash-prize autorouter or AI-layout competition** right now. The closest things are reproducible benchmarks with no prize money (see the end of this page).
- The **Hackaday Prize has not run since 2023**.
- **tscircuit's Algora bounties are mostly stale**; tscircuit now pays contributors through a weekly sponsorship scheme instead.
- The best-paying open opportunities with real PCB requirements are the **PCBWay 9th Project Design Contest**, **EasyEDA Spark 2026**, and the **heypcb Hardware Challenge**.

## 1. Open now, with specific PCB requirements

| Contest | What it asks for | Reward | Deadline | Status |
|---|---|---|---|---|
| [heypcb Hardware Challenge](https://heypcb.ai/challenge) | Any board designed in heypcb (an AI PCB tool), published to their gallery. Forks need substantial original work. Judged on quality and whether it would work if built. | Two winners, each $500 cash + $500 credit + internship and founding-engineer interview | 30 Nov 2026 | OPEN |
| [PCBWay 9th Project Design Contest](https://www.pcbway.com/activity/9th-project-design-contest.html) | Original projects in Edge AI & IoT, Robotics, Power (BMS, converters, solar), Mechanical, or Open. Scored 30 % design complexity, 30 % impact, 25 % docs, 15 % votes. | 1st $2,000 + Jetson Orin Nano Super; 2× $1,500; 3× $800; 10× $100 popular vote | 24 Jan 2027 | OPEN |
| EasyEDA Spark 2026 ([JLCCNC](https://jlccnc.com/blog/easyeda-spark-contest), [JLCPCB news](https://jlcpcb.com/news/jlc-spark-conference-2026)) | Design in EasyEDA Pro, build with JLC, publish open on OSHWLab. Ages 16+. | $85,000 pool, top project up to $30,000; fab costs largely covered | Register 30 Nov, submit 31 Dec 2026 (sources disagree; one says Mar 2027) | LIKELY OPEN |
| [Sierrathon](https://www.protoexpress.com/event/sierrathon/) (Sierra Circuits + SJSU) | One-day, in-person: given schematic, BOM and constraints incl. diff pairs → choose stackup, place, route to DRC, defend trade-offs. **Students only.** | $2,000 1st + free fab/assembly | 21 Nov 2026 | OPEN |
| [Hackster: Build the AU 2027 Product](https://www.hackster.io/contests/autodesk-university-2027-product) | Handheld/wearable accessory for Arduino UNO Q, designed in Autodesk Fusion, fabbed by PCBWay. Has a "Best Fusion Electronics Design" prize. | 3× $1,000; winning concept produced at ~750 units | Final submissions 20 Dec 2026 | OPEN |
| [Hackster Infineon Boss Battle](https://www.hackster.io/contests/infineon-boss-battle) | PSOC Edge AI kit project (custom PCB optional) | $1,000 + 2× $500 | 3 Jan 2027 | OPEN |
| [CircuitDigest IoT & AI Inference Challenge](https://circuitdigest.com/contest/iot-ai-inference-design-challenge-2026/) (DigiKey) | **India only.** IoT/edge-AI builds. | ₹7 lakh pool | Ideas 30 Dec 2026 | OPEN (registration from 5 Nov) |
| [Hackaday Retrocomputing Challenge](https://hackaday.io/contest/206399-retrocomputing-contest) | Retro computing builds | 3× $150 DigiKey cards | 27 Oct 2026 | OPEN (closing) |

## 2. Paid work on PCB tooling (autorouters, EDA, code-as-hardware)

| Program | What it pays for | Reward | Status |
|---|---|---|---|
| [tscircuit sponsorship](https://docs.tscircuit.com/contributing/bounties-and-sponsorship) | Any merged PR across the tscircuit org, scored weekly; autorouter work lives in [tscircuit-autorouter](https://github.com/tscircuit/tscircuit-autorouter/wiki) | $15–$500 per payout, from your last 4 weeks of scores | OPEN, ongoing |
| [tscircuit autorouting datasets](https://docs.tscircuit.com/contributing/contributing-autorouting-dataset) | Contribute routing test datasets + benchmark scenarios (example: [dataset-srj33-drc-failures](https://github.com/tscircuit/dataset-srj33-drc-failures)) | Counts toward sponsorship | OPEN |
| [tscircuit on Algora](https://algora.io/tscircuit/home) | Historic per-issue bounties ($20k+ paid out). The large recent ones closed in Jul–Sep 2026. | Was $1–$170/issue | STALE |
| [atopile on Algora Challenges](https://algora.io/challenges/atopile) | Publishing modules, EDA integrations, test frameworks or tutorials to the atopile registry | $1,000 per accepted contribution | UNKNOWN — confirm with atopile first |
| [NLnet open call](https://nlnet.nl/news/2026/20260903-call.html) | Open-source grants; recently funded **KiCad FEM** (PCB physics simulation). Check EDA/hardware scope. | Historically €5k–50k | OPEN until 3 Nov 2026 12:00 CET |

## 3. Commission and freelance markets

| Market | What's there |
|---|---|
| [Upwork — KiCad jobs](https://www.upwork.com/freelance-jobs/kicad/) | ~316 listings; fixed-price jobs commonly $100–$600 (reviews, DFM tweaks), plus hourly product work |
| [Cad Crowd — KiCad jobs](https://www.cadcrowd.com/jobs/kicad) | Fixed, hourly and contest formats; October postings include an analog front end, a 4-layer smartwatch board, and a Pi 5 HAT review |
| AI-trainer roles (e.g. via Handshake) | Reviewing AI-generated schematics and layouts; several postings closed — check each |

The KiCad forum has no formal jobs category.

## 4. Free fabrication (no cash, but it removes the cost of trying)

- JLCPCB [free PCB applications](https://jlcpcb.com/help/article/how-to-apply-for-free-pcb) and [Brand Advocate program](https://jlcpcb.com/help/article/get-free-pcbs-get-paid-to-build-join-the-jlcpcb-brand-advocate-program)
- [PCBWay project sponsorship](https://www.pcbway.com/project/sponsor/crowdfunding.aspx)

## 5. Recently expired — good practice targets

These have published rules and boards, so they make excellent self-graded exercises even without prize money.

| Challenge | Why it's worth doing anyway |
|---|---|
| [comma.ai PCBGolf](https://github.com/commaai/PCBGolf) ([leaderboard](https://comma.ai/leaderboard)) | Shrink a real 12 V / USB hub / CAN / STM32H7 board. Score = volume (mm³) + 50 × vias + 5,000 × copper layers. $1,000 cash prize ended 12 Oct 2026; still listed as a **hiring screen**. Leader at snapshot: 8,886. |
| [UK PCB Challenge 2026](https://github.com/heisendelta/PCB-Challenge-2026) (PCBWay + Jane Street) | Hand-route a 4-layer board for minimum area at 0.15 mm trace / 0.12 mm clearance / 0.3 mm via, zero DRC errors, no autorouter. KiCad 10. |
| [PCBWay 2026 KiCad Design Contest](https://www.pcbway.com/activity/2026-kicad-pcb-design-contest.html) | Annual; ran Apr–Jun 2026. Watch for the 2027 edition. |
| [Hackster Board Designer Competition](https://www.hackster.io/contests/board-designer) | 2025 edition; may recur. |

## 6. Benchmarks without prizes (for autorouter / AI-layout work)

| Benchmark | What it is |
|---|---|
| DeepPCB vs Quilter comparison ([write-up](https://deeppcb.ai/deeppcb-vs-quilter-open-source-routing-compared-2026/)) | Three public KiCad boards — STRF (98 airwires), PocketBeagle (290), BeagleConnect Freedom (414) — form a de facto reproducible routing benchmark |
| [PCB-Bench](https://github.com/digailab/PCB-Bench) (ICLR 2026) | ~3.7k QA items on placement/routing plus 174 real OSHWHub projects |
| [PCBWorld](https://arxiv.org/html/2607.05915v1) | KiCad-engine routing environment, 20k synthetic + 679 real boards, scored on "clean pass" (fully routed, zero violations). Code not yet released at snapshot. |
| This repo's [benchmark](../benchmark/) | Strip-and-reroute of real KiCad boards with KiCad-DRC grading |

## Not found

No current DARPA or other government program targeting PCB layout automation; no PCB bounties on IssueHunt, Opire or Polar; no paid public challenges from Flux, JITX, CELUS, Cadstrom, Quilter or Diode.
