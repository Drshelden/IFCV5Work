# IFC5 Architecture Initiative

This repository is the working home for the **IFC5 Architecture Initiative** — a structured, evidence-based effort to develop the architectural foundations of IFC5 through transparent decision-making.

Rather than writing a complete specification upfront, the initiative captures the reasoning, alternatives, and consensus behind each major architectural decision first. Decisions mature through a defined lifecycle, then are promoted into normative specification text.

---

## How This Works

Every significant architectural question becomes a **Request for Comments (RFC)**. Each RFC documents the problem, at least two alternatives (always including the IFC4.x convention), tradeoffs, a recommendation, and open questions for reviewers to focus on.

RFCs progress through a lifecycle:

```
Idea → Framed → Open Review → [Prototype Required → Prototype Complete]
     → Committee Review → Public Review → Accepted → Normative → Stable
```

The **[Decision Register](01%20Decision%20Register/IFC5_Decision_Register.csv)** is the authoritative source of truth for where every RFC currently stands.

For the complete process guide — including how to write an RFC, how to classify review comments, and how GitHub and other tools work together — see:

> **[`00 Architecture Overview/IFC5_Process_Guide.md`](00%20Architecture%20Overview/IFC5_Process_Guide.md)**

---

## Repository Structure

```
/
├── 00 Architecture Overview/
│   └── IFC5_Process_Guide.md       ← Start here. Full process, roles, lifecycle.
│
├── 01 Decision Register/
│   └── IFC5_Decision_Register.csv  ← All 38 RFCs: status, tier, dependencies, owners.
│
├── 02 RFCs/
│   ├── README.md                   ← RFC index organized by tier.
│   ├── RFC-IFC5-001-*.md
│   ├── RFC-IFC5-002-*.md
│   └── ... (38 RFCs total)
│
├── 03 Reference Examples/          ← Canonical comparison examples (Hello Wall, etc.)
│
├── 04 Committee Feedback/          ← Comment resolution logs and ballot responses.
│
├── 05 Normative Specification/     ← Populated only after decisions reach Accepted status.
│
└── 06 Prototype Implementations/   ← Notes and links to GitHub prototype repositories.
```

---

## The 38 RFCs at a Glance

All RFCs are currently at **Idea** status — no decisions have been made yet. The RFC index below links to every file. See [`02 RFCs/README.md`](02%20RFCs/README.md) for the full table with prototype flags and source topic references.

### Tier 1 — Foundational
*Resolve these first. All downstream RFCs depend on them.*

| RFC | Title |
|---|---|
| [IFC5-001](02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) | Strategic Architecture Mode |
| [IFC5-002](02%20RFCs/RFC-IFC5-002-normative-model-formalism.md) | Normative Information Model Formalism |
| [IFC5-003](02%20RFCs/RFC-IFC5-003-identity-model.md) | Identity Model ⚗️ |
| [IFC5-004](02%20RFCs/RFC-IFC5-004-path-model.md) | Path Model and Addressing ⚗️ |
| [IFC5-005](02%20RFCs/RFC-IFC5-005-namespaces.md) | Namespace and Qualified Names |
| [IFC5-006](02%20RFCs/RFC-IFC5-006-serialization-encoding.md) | Serialization and Encoding |

### Tier 2 — Core Architecture
*Major structural decisions. Depend on Tier 1.*

| RFC | Title |
|---|---|
| [IFC5-007](02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) | Scene Graph vs. ECS vs. Hybrid Architecture ⚗️ |
| [IFC5-008](02%20RFCs/RFC-IFC5-008-relationship-modeling.md) | Relationship Modeling Strategy ⚗️ |
| [IFC5-009](02%20RFCs/RFC-IFC5-009-class-type-representation.md) | Class and Type Representation |
| [IFC5-010](02%20RFCs/RFC-IFC5-010-composition-inheritance.md) | Composition, Inheritance, and Instancing ⚗️ |
| [IFC5-011](02%20RFCs/RFC-IFC5-011-document-structure.md) | Document-Level Structure |
| [IFC5-012](02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) | Modular Schema Imports |
| [IFC5-023](02%20RFCs/RFC-IFC5-023-attribute-representation.md) | Attribute Representation |
| [IFC5-024](02%20RFCs/RFC-IFC5-024-type-system-primitives.md) | Type System, Primitives, Enumerations, SELECTs |
| [IFC5-025](02%20RFCs/RFC-IFC5-025-collections-cardinality.md) | Collections and Cardinality |

### Tier 3 — Domain Modeling
*Domain-specific decisions. Depend on Tier 2.*

| RFC | Title |
|---|---|
| [IFC5-013](02%20RFCs/RFC-IFC5-013-property-sets.md) | Property Sets and Properties ⚗️ |
| [IFC5-014](02%20RFCs/RFC-IFC5-014-geometry-architecture.md) | Geometry Architecture ⚗️ |
| [IFC5-015](02%20RFCs/RFC-IFC5-015-openusd-alignment.md) | OpenUSD Alignment ⚗️ |
| [IFC5-016](02%20RFCs/RFC-IFC5-016-spatial-structure.md) | Spatial Structure and Decomposition |
| [IFC5-017](02%20RFCs/RFC-IFC5-017-material-modeling.md) | Material Modeling |
| [IFC5-026](02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md) | Openings, Voids, and Fillings ⚗️ |
| [IFC5-027](02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md) | Classification and External Dictionaries |
| [IFC5-028](02%20RFCs/RFC-IFC5-028-units-measures.md) | Units and Measures |
| [IFC5-029](02%20RFCs/RFC-IFC5-029-presentation-appearance.md) | Presentation and Appearance |
| [IFC5-030](02%20RFCs/RFC-IFC5-030-space-boundaries.md) | Space Boundaries and Topology |
| [IFC5-031](02%20RFCs/RFC-IFC5-031-metadata-custom-data.md) | Metadata and Custom Data |

### Tier 4 — Process & Governance
*Conformance, versioning, federation, and cross-cutting concerns.*

| RFC | Title |
|---|---|
| [IFC5-018](02%20RFCs/RFC-IFC5-018-backward-compatibility.md) | Backward Compatibility and Round-Tripping ⚗️ |
| [IFC5-019](02%20RFCs/RFC-IFC5-019-validation-framework.md) | Validation Framework |
| [IFC5-020](02%20RFCs/RFC-IFC5-020-model-views-exchange.md) | Model Views and Exchange Requirements |
| [IFC5-021](02%20RFCs/RFC-IFC5-021-federation-external-references.md) | Federation and External References |
| [IFC5-022](02%20RFCs/RFC-IFC5-022-versioning-schema-evolution.md) | Versioning and Schema Evolution |
| [IFC5-032](02%20RFCs/RFC-IFC5-032-extensibility.md) | Extensibility |
| [IFC5-033](02%20RFCs/RFC-IFC5-033-change-collaboration.md) | Change, Transactions, and Collaboration |
| [IFC5-034](02%20RFCs/RFC-IFC5-034-performance-scale-database.md) | Performance, Scale, and Database Implications ⚗️ |
| [IFC5-035](02%20RFCs/RFC-IFC5-035-web-linked-data.md) | Web and Linked-Data Alignment |
| [IFC5-036](02%20RFCs/RFC-IFC5-036-ai-machine-readability.md) | AI and Machine-Readability |
| [IFC5-037](02%20RFCs/RFC-IFC5-037-security-trust.md) | Security and Trust |
| [IFC5-038](02%20RFCs/RFC-IFC5-038-governance-conformance.md) | Governance, Conformance, and Interoperability Testing |

⚗️ = prototype required before this RFC can advance to Committee Review.

---

## How to Participate

### New to the initiative?

1. Read the **[Process Guide](00%20Architecture%20Overview/IFC5_Process_Guide.md)**.
2. Check the **[Decision Register](01%20Decision%20Register/IFC5_Decision_Register.csv)** to see what is under active discussion.
3. Pick one or two RFCs in **Open Review** status and read them.
4. Submit comments using the classification system below.

### Submitting comments

When reviewing an RFC, classify every comment using one of these types so the author can triage efficiently:

| Type | Use when |
|---|---|
| **Editorial** | Grammar, clarity, wording — no technical impact |
| **Technical Defect** | The RFC contains an error of fact or logic |
| **Semantic Concern** | The proposal may not mean what the author intends |
| **Compatibility Concern** | Conflicts with IFC4.x usage or existing tooling |
| **Alternative Proposal** | You have a different approach not covered in the RFC |
| **Evidence** | You have data, examples, or prototypes relevant to the decision |
| **Blocking Objection** | The RFC cannot be accepted as written — reserve for genuine blockers |
| **General Support** | You support the recommendation |

**How to submit:**
- For general comments, open a **GitHub Issue** and reference the RFC ID (e.g. `IFC5-007`).
- For line-level edits or corrections, open a **Pull Request** against the RFC file.
- For extended technical discussion, start a **GitHub Discussion** in the relevant thread.

Please do not open Issues for broad architectural debates — if a topic isn't covered by an existing RFC, propose a new one by following the RFC authoring process in the [Process Guide](00%20Architecture%20Overview/IFC5_Process_Guide.md).

### Proposing a new RFC

1. Open an Issue with the label `new-rfc` describing the decision gap.
2. Draft the RFC using the structure defined in the [Process Guide](00%20Architecture%20Overview/IFC5_Process_Guide.md) (sections: Problem Statement, Background, IFC4.x Convention, Proposed Approaches, Tradeoffs, Recommendation, Open Questions, Prototype, Consequences, References).
3. Submit a Pull Request adding the file to `02 RFCs/` with the next available RFC ID.
4. The working group will review and move it to Open Review status when ready.

### Working on a prototype

If an RFC is flagged ⚗️, a prototype is required before it can advance. To contribute:

1. Check the RFC's **Prototype** section for current status and any linked repositories.
2. Coordinate with the RFC owner before starting — duplication of effort is common.
3. When complete, document the prototype in `06 Prototype Implementations/` and update the RFC's Prototype section with a link and summary of findings.

---

## Guiding Principles

1. **Decisions before specification.** Write the architecture first; the spec follows from consensus.
2. **One RFC per decision.** Bundling decisions makes consensus harder and traceability impossible.
3. **Alternatives required.** Every RFC must document at least two alternatives, including the IFC4.x convention.
4. **Evidence over opinion.** Arguments grounded in examples, prototypes, or prior art carry more weight.
5. **Prototypes gate acceptance.** No ⚗️ RFC advances to Committee Review until its prototype is complete.
6. **Structured feedback.** Use the comment classification system — it prevents important objections from getting buried.

---

*IFC5 Architecture Initiative · July 2026 · All RFCs at Idea status — no decisions made yet.*
