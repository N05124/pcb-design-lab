# MIT OpenCourseWare map for PCB designers

Every URL below was checked on 2026-10-23. Descriptions are our own summaries; the course material itself lives on MIT's sites.

**Licence.** OCW content is [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) (see OCW's [Terms of Use](https://www.ocw.mit.edu/pages/privacy-and-terms-of-use/)). You may copy and remix it for non-commercial use with attribution and share-alike. MIT's name and logos are trademarks and are not covered. This repo therefore *links* to OCW rather than mirroring it. If you build derived notes from OCW in this repo, keep them in `curriculum/notes/`, credit the course, and keep that folder CC BY-NC-SA.

**Big caveat.** OCW has no course dedicated to PCB layout. Board-level material is scattered across the courses marked ⭐ below. The most PCB-specific MIT material is outside OCW: [pcb.mit.edu](https://pcb.mit.edu/) (IAP class, CC BY-SA 4.0) and the How to Make (Almost) Anything / Fab Academy electronics pages.

**Course numbers.** MIT renumbered EECS in 2022 (e.g. 6.002 → 6.200). OCW mostly still hosts the older numbered versions, which are the ones linked here.

---

## 1. Circuit fundamentals

| Course | OCW term | Link | Why it matters for boards | Materials |
|---|---|---|---|---|
| 6.002 Circuits and Electronics | Spring 2007 | [ocw](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) | The lumped-circuit model every schematic assumes — and its last lecture shows where that model breaks, which is exactly where signal integrity starts. | 26 video lectures, notes, labs, psets, exams |
| 6.071J Electronics, Signals & Measurement | Spring 2006 | [ocw](https://ocw.mit.edu/courses/6-071j-introduction-to-electronics-signals-and-measurement-spring-2006/) | Measurement-first electronics; directly useful for board bring-up and debug. | Notes, labs, psets, exams |
| 6.01SC Intro to EECS I (circuits unit) | Spring 2011 | [ocw](https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011/pages/lecture-videos/) | Gentle video intro to circuits and op-amps. Optional. | Videos, text, psets |
| 6.200 (current, non-OCW) | Spring 2026 | [circuits.mit.edu](https://circuits.mit.edu/S26) | Today's version of 6.002 with modern design labs (DAC, ECG, boost converter, RP2040). | Slides, psets, design labs |

## 2. Analog electronics and lab practice

| Course | OCW term | Link | Why it matters | Materials |
|---|---|---|---|---|
| 6.091 Hands-On EE Lab Skills | IAP 2008 | [ocw](https://ocw.mit.edu/courses/6-091-hands-on-introduction-to-electrical-engineering-lab-skills-january-iap-2008) | Instruments, soldering, simple logic — the skills you need before your first board. | Notes, labs |
| EC.S06 Practical Electronics | Fall 2004 | [ocw](https://ocw.mit.edu/courses/edgerton-center/ec-s06-practical-electronics-fall-2004) | Rules of thumb for building circuits that work, ending in a project. | Notes, labs, psets |
| 6.101 Intro Analog Electronics Lab | Spring 2007 | [ocw](https://ocw.mit.edu/courses/6-101-introductory-analog-electronics-laboratory-spring-2007/) · [2019 site](https://web.mit.edu/6.101/www/s2019/main.html) | Design, build, debug discrete analog circuits; the 2019 site adds optional PCB fabrication and switch-mode supplies. | Labs, psets, project |
| 6.012 Microelectronic Devices & Circuits | 2009 | [spring](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-spring-2009) · [fall](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009) | Transistor physics behind datasheet parameters. | Notes, psets, projects |
| 6.301 Solid-State Circuits | Fall 2010 | [ocw](https://ocw.mit.edu/courses/6-301-solid-state-circuits-fall-2010/pages/syllabus) | Practical transistor-level analog design with build-and-test labs. | Recitations, labs |
| RES.6-010 Electronic Feedback Systems | Spring 2013 | [ocw](https://ocw.mit.edu/courses/res-6-010-electronic-feedback-systems-spring-2013/resources/lecture-1-introduction-and-basic-concepts/) | Op-amp stability and compensation — why regulators and amplifiers oscillate on real boards. | 20 video lectures, textbook, psets |
| 6.302 Feedback Systems | Spring 2007 | [ocw](https://ocw.mit.edu/courses/6-302-feedback-systems-spring-2007/pages/syllabus/) | Feedback applied to power converters and PLLs. | Labs, psets |
| 6.331 Advanced Circuit Techniques | Spring 2002 | [ocw](https://ocw.mit.edu/courses/6-331-advanced-circuit-techniques-spring-2002/pages/syllabus/) | Follow-on to 6.301. Thin materials. | Labs |

## 3. Electromagnetics — the foundation of signal integrity

| Course | OCW term | Link | Why it matters | Materials |
|---|---|---|---|---|
| ⭐ 6.013 Electromagnetics & Applications | Spring 2009 | [ocw](https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/) · [free textbook](https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/resources/mit6_013_s09_coursetextbook_pdf/) | Maxwell to guided waves and radiation; the physics behind impedance, reflections and emissions. | Free textbook, notes, solved psets |
| ⭐ 6.630 Electromagnetics | Fall 2006 | [ocw](https://ocw.mit.edu/courses/6-630-electromagnetics-fall-2006) · [matching handout](https://live.ocw.mit.edu/courses/6-630-electromagnetics-fall-2006/resources/match/) | Transmission-line theory tied back to circuits; impedance matching. | Psets, MATLAB demos |
| 6.641 EM Fields, Forces & Motion | Spring 2009 | [ocw](https://ocw.mit.edu/courses/6-641-electromagnetic-fields-forces-and-motion-spring-2009) | Quasistatics: capacitive and inductive coupling (crosstalk), magnetics. | Notes, solved psets |
| 6.632 EM Wave Theory | Spring 2003 | [ocw](https://ocw.mit.edu/courses/6-632-electromagnetic-wave-theory-spring-2003/) | Graduate wave theory; only for RF/EMC modelling. | Psets |
| 6.007 EM Energy: Motors to Lasers | Spring 2011 | [ocw](https://www.ocw.mit.edu/courses/6-007-electromagnetic-energy-from-motors-to-lasers-spring-2011) | Optional applied EM. | Notes, videos |

## 4. Signals and systems

| Course | OCW term | Link | Why it matters | Materials |
|---|---|---|---|---|
| 6.003 Signals and Systems | Fall 2011 | [ocw](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011) | Frequency response and sampling: filters, ADC front ends, and the spectrum of a fast edge. | Videos, solved psets |
| RES.6-007 Signals and Systems (Oppenheim) | Spring 2011 | [ocw](https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/pages/readings/) | The classic alternative lecture series. | Videos, psets |

## 5. Digital, FPGA and microcontroller labs

| Course | OCW term | Link | Why it matters | Materials |
|---|---|---|---|---|
| 6.111 Intro Digital Systems Lab | Spring 2006 | [ocw](https://ocw.mit.edu/courses/6-111-introductory-digital-systems-laboratory-spring-2006/) | FPGA timing and clocking — the source of most high-speed board constraints. | Notes, labs, projects |
| 6.115 Microcomputer Project Lab (non-OCW) | 2026 | [site](https://ee6115b.mit.edu/) | Microcontroller labs and datasheet collections. | Help-session videos |

## 6. Power electronics

| Course | OCW term | Link | Why it matters | Materials |
|---|---|---|---|---|
| ⭐ 6.622 Power Electronics | Spring 2023 | [ocw](https://live.ocw.mit.edu/courses/6-622-power-electronics-spring-2023) · [Lecture 38: gate drive & layout](https://ocw.mit.edu/courses/6-622-power-electronics-spring-2023/resources/mit6_622s23_lecture_38_mp4/) | Newest power course on OCW; Lecture 38 is the only OCW lecture squarely about layout. | Videos, notes, psets, project |
| ⭐ 6.334 Power Electronics | Spring 2007 | [ocw](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007) · [ch.14 EMI filtering](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/resources/ch14) | Magnetics, snubbers, thermal design and EMI filters. | Notes, psets |
| 6.131 Power Electronics Lab (non-OCW) | Fall 2026 | [site](https://web.mit.edu/6.131/www/) | Hands-on inverters and motor drives. | Datasheets, projects |

## 7. RF and high-speed

| Course | OCW term | Link | Why it matters | Materials |
|---|---|---|---|---|
| ⭐ 6.776 High Speed Communication Circuits | Spring 2005 | [ocw](https://ocw.mit.edu/courses/6-776-high-speed-communication-circuits-spring-2005/) · [Smith chart handout](https://ocw.mit.edu/courses/6-776-high-speed-communication-circuits-spring-2005/resources/imp_ad_smithchar) | Transmission lines, LNAs, VCOs, PAs, with an RF build lab. | Notes, labs, projects |
| ⭐ 6.976 High Speed Comm. Circuits & Systems | Spring 2003 | [ocw](https://ocw.mit.edu/courses/6-976-high-speed-communication-circuits-and-systems-spring-2003) · [transmission-line lecture](https://ocw.mit.edu/courses/6-976-high-speed-communication-circuits-and-systems-spring-2003/resources/lec2) | Transmission lines, synthesisers, clock and data recovery. | Notes, projects |
| 6.661 Receivers, Antennas & Signals | Spring 2003 | [ocw](https://ocw.mit.edu/courses/6-661-receivers-antennas-and-signals-spring-2003/) | Optional antennas and receivers. | Notes, psets |

## 8. PCB layout, fabrication, manufacturing

| Resource | Term | Link | Why it matters |
|---|---|---|---|
| ⭐ 2.996 Biomedical Devices Design Lab (OCW) | Fall 2007 | [ocw](https://ocw.mit.edu/courses/mechanical-engineering/2-996-biomedical-devices-design-laboratory-fall-2007) · [lab description](https://ocw.mit.edu/courses/2-996-biomedical-devices-design-laboratory-fall-2007/resources/lab_descrip) | The only OCW course whose labs are about PCB design: part selection, layout, assembly. |
| MAS.863 How to Make (Almost) Anything (OCW) | Fall 2002 | [ocw](https://live.ocw.mit.edu/courses/mas-863-how-to-make-almost-anything-fall-2002/) | PCB design and milling alongside embedded work (dated). |
| ⭐ HTMAA 2025 (non-OCW) | 2025 | [fab.cba.mit.edu](https://fab.cba.mit.edu/classes/863.25/) | Weekly electronics design and production assignments. |
| ⭐ Fab Academy topic pages (non-OCW) | current | [design](https://academy.cba.mit.edu/classes/electronics_design/index.html) · [production](https://academy.cba.mit.edu/classes/electronics_production/index.html) | EDA tools incl. KiCad, DRC/ERC, SPICE, planes; milling, materials, reflow, QFN/BGA. |
| ⭐⭐ The Art and Science of PCB Design (non-OCW, CC BY-SA 4.0) | IAP 2026 | [pcb.mit.edu](https://pcb.mit.edu/) · [syllabus](https://pcb.mit.edu/syllabus) · [2025 archive](https://pcb.mit.edu/archive/IAP2025) | The most directly relevant MIT course: schematic, layout, DFM, fab and SMT assembly in KiCad/Altium. **Start here.** |

Searched and not found: a 2.S998 electronics course, and any OCW course on grounding, shielding or EMC as its main subject.
