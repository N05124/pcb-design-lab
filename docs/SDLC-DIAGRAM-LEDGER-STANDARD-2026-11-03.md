# Portfolio SDLC and Diagram-Ledger Compliance Standard — 2026-11-03

**Owner directive — documentation and planning only.** Applies to this repository proportionately to its purpose, whether a library, application, research project, infrastructure tool, website or policy repository. No automatic code generation, paid inference, CI activation, branch merge, release, or override of existing project-specific gates is authorized by this document.

> Nose to the grindstone without observing the work will grind your fingers away.

## Lifecycle: observe, construct, integrate, verify, prototype, iterate
0. **Observe and map.** Inventory actual project scope, existing source, reusable capabilities, missing requirements, dependencies, owner holds and current evidence. Define explicit denominator and acceptance criteria. Avoid pretending a green build or completed document proves full project completeness.
1. **Specify and diagram.** Produce versioned architecture and workflow diagrams with stable identifiers, contracts, inputs/outputs, data models, units where applicable, error states, invariants, expected results, provenance, ownership, accessibility/security/privacy requirements and traceable acceptance assertions.
2. **Construct full authorized codebase.** Prefer complete intended source coverage over indefinite polishing of one milestone. Use bounded, dependency-aware implementation packets and reusable components. Mark generated code UNVERIFIED_DRAFT until tested. Never silently implement held work or duplicate canonical components. For non-code repositories, construct their full authorized artifact set instead.
3. **Cohesion and integration.** Assemble packages and modules, resolve symbol ownership and dependencies, run actual builds/static checks and integration tests against a pinned environment; capture failures rather than claiming success.
4. **Verification.** Run unit, integration, property, security, reference-vector and regression tests as applicable. An independent reviewer evaluates integrity and recorded evidence; a test assertion is an expectation, not proof of passing.
5. **Prototype and acceptance.** Exercise representative end-to-end workflows, realistic object/parameter contracts, UI interactions, accessibility and target platforms where applicable. Distinguish simulated from native evidence.
6. **Iterate.** Reconcile observed defects against versioned diagrams, update expected results with justification, impact-map dependents, add regression assertions and repeat. Keep design, implementation and evidence synchronized.

## Required diagram-ledger (machine-readable where practical)
For each in-scope capability record:
- Stable CapabilityID, ComponentID, owner, status, priority, source branch/SHA, specification/diagram version and content hash.
- Requirements and acceptance criteria; upstream/downstream dependency IDs; interfaces and data/parameter schemas; units/tolerances and standards provenance when relevant.
- Preconditions, postconditions, invariants, error and state transitions; expected output or explicit UNKNOWN; deterministic fixture IDs.
- Implementation paths and commits; test paths; commands/toolchain/environment; observed outcomes and evidence links; independent reviewer/disposition.
- Impact analysis on changes: affected interfaces, fixtures, diagrams, downstream consumers and documentation.
- A clear distinction among DESIGN_EXPECTATION, IMPLEMENTATION_CLAIM, OBSERVED_EVIDENCE and ACCEPTANCE_DISPOSITION. Do not silently overwrite old versions.

## Prompt compliance contract for Claude / Together / any agent
Each development instruction MUST identify:
1. **Intent and scope:** CapabilityIDs, target branch/files, approved owner, exclusions and explicit holds.
2. **Context:** pinned source SHA, exact diagram/packet hashes, existing reusable APIs and relevant source references; no speculative claims about repository state.
3. **Deliverables:** bounded files, API contracts, tests/fixtures, documentation and expected outputs, with stable paths and completion markers.
4. **Constraints:** project language/toolchain/platform, modularity, error handling, concurrency, security, accessibility, data/privacy/standards requirements, budget and no-duplicate/no-secret rules.
5. **Acceptance:** mechanically checkable syntax/structure and expected assertions; later compile/test/native evidence must be independently recorded, not implied.
6. **Provenance:** agent/model, prompt version/hash, input SHA, output SHA, timestamps, cost where applicable, failure/retry identifiers, and reviewer.
7. **Stop conditions:** missing authorization, ambiguous owner, held component, invalid packet, over-budget, truncated response, unavailable toolchain or ungrounded scientific claim. Stop or defer rather than invent evidence.
8. **Handoff:** exact progress counts, blockers, pending decisions, next dependency-aware work packet; do not dispatch overlapping work.

## Reporting and completion measurement
At each checkpoint, show the actual denominator and counts for mapped, specified, drafted, syntactically complete, compiled/integrated, tested, prototyped and independently accepted items. Keep project-specific weightings documented. Never equate draft coverage with evidence-weighted completion. Include build/test commands, exit codes, skips, commit hashes, failed assertions and owner decisions. Treat missing evidence as NOT RUN, not PASS.

## Governance / rollout
- This standard is a portfolio baseline, **not** a replacement for stronger repository-specific controls. Existing holds, PR gates, budgets, compliance requirements and production restrictions take precedence.
- For active projects: coordinator should inspect existing architecture, write a gap/delta report and adopt this standard in future prompts, without interrupting active jobs or duplicating paid work.
- For dormant, static or policy repositories: keep this as a dormant governance reference; do not manufacture implementation tasks.
- Before any bulk construction: establish scope/denominator and diagram-ledger; then prefer source coverage, followed by coordinated cohesion, verification and prototype iteration.
- No automatic implementation kickoff is authorized merely by receiving this document.

## Coordinator adoption prompt
**CLAUDE / COORDINATOR:** Read this standard, compare it with the repository's current process, identify only material deviations, and propose the smallest non-disruptive compliance update. Preserve ongoing work and existing owner approvals. Create a versioned diagram-ledger index and prompt template only when useful to the project. Report project-specific lifecycle stage, coverage denominator, evidence gaps and next safe action. Do not start development, spend money, or merge anything without existing authorization.
