# IFC5 Architecture Initiative — Process Guide

**Version:** 0.1 Draft  
**Status:** Working Document  
**Maintained by:** IFC5 Architecture Initiative Working Group  

---

## Quick Links

| Resource | Link |
|---|---|
| **GitHub Repository** | [github.com/Drshelden/IFCV5Work](https://github.com/Drshelden/IFCV5Work) |
| **RFC Index** | [GitHub](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md) · [Google Doc](https://docs.google.com/document/d/1L4wD92OdDVGm5cvcPiAGYWQBF9pDHbHXni6ohOS5rKE/edit) |
| **Decision Register** | [GitHub CSV](https://github.com/Drshelden/IFCV5Work/blob/master/01%20Decision%20Register/IFC5_Decision_Register.csv) |
| **RFC Priority Survey** | [📋 Take the survey](https://forms.gle/vgu13dUKTpaqWEaE9) |
| **GitHub Discussions** | [View all discussions](https://github.com/Drshelden/IFCV5Work/discussions) |
| **Individual RFC Feedback Forms** | Links in the header/footer of each RFC |

---

## Quick Start

New to the initiative? Do these three things:

**1. Orient yourself (15 min)**
Read the [RFC Index](https://docs.google.com/document/d/1L4wD92OdDVGm5cvcPiAGYWQBF9pDHbHXni6ohOS5rKE/edit) to see all 38 topics under discussion, grouped by tier. Skim two or three RFCs that look relevant to your work.

**2. Vote on priorities (10 min)**
Fill out the [RFC Priority Survey](https://forms.gle/vgu13dUKTpaqWEaE9). Rate each RFC on whether it should be resolved as part of IFC5 architecture work. This takes about 10 minutes and directly shapes what gets worked on first.

**3. Give detailed feedback on one RFC (30–60 min)**
Pick an RFC in a tier you know well. Open it via the link in the RFC Index (GitHub or Google Doc). Use the feedback form linked in the RFC header to submit structured comments — or start a [GitHub Discussion](https://github.com/Drshelden/IFCV5Work/discussions) if you prefer open-ended dialogue.

That's it. The rest of this guide covers the process in detail for those who want it.

---

## What This Initiative Is

The IFC5 Architecture Initiative is a structured effort to develop the architectural foundations of IFC5 through transparent, evidence-based decision-making. Rather than writing a complete specification upfront, we first capture the reasoning, alternatives, and consensus behind each major architectural decision. Once decisions mature, they are promoted into normative specification text with minimal additional work.

The initiative is organized around **architectural decisions**, not files or GitHub issues. Each significant question — identity, relationships, namespaces, OpenUSD alignment, ECS design, etc. — becomes a structured **Request for Comments (RFC)** that progresses through a defined lifecycle from idea to normative text.

---

## Guiding Principles

1. **Decisions before specification.** Write the architecture first; the spec follows from consensus, not the other way around.
2. **One RFC per decision.** Each RFC addresses exactly one architectural question. Bundling decisions makes consensus harder and traceability impossible.
3. **Alternatives required.** Every RFC must document at least two alternatives, including the IFC4.x convention and one IFCX or ECS-based approach. A recommendation without alternatives is not ready for review.
4. **Evidence over opinion.** Arguments should be grounded in examples, prototypes, use cases, or prior art. Assertions without evidence carry less weight.
5. **Prototypes gate acceptance.** Where the RFC flags a prototype as required, no decision moves to Committee Review until the prototype is complete and documented.
6. **Structured feedback.** Reviewers classify their comments (see below). This prevents important objections from getting buried in discussion threads.

---

## The Folder Structure

This [Google Drive folder](https://drive.google.com/drive/folders/1U9J-6hAr5pM_Q28JChDcistHsAHgi33y) is the authoritative home for architecture work. [GitHub](https://github.com/Drshelden/IFCV5Work) remains the home for implementations, validators, example files, and specification source.

| Folder | Contents |
|---|---|
| `00 Architecture Overview` | This guide, the Architecture Overview document, roadmap, and meeting notes |
| `01 Decision Register` | The master spreadsheet tracking every architectural decision and its status |
| `02 RFCs` | One document per RFC, named `RFC-IFC5-XXX-short-title.docx` |
| `03 Reference Examples` | Canonical comparison examples (Hello Wall, Small Building, MEP, etc.) across IFC-SPF, IFC-ECS, and IFCX |
| `04 Committee Feedback` | Comment resolution logs, ballot responses, and structured feedback collected via forms |
| `05 Normative Specification` | Specification text — only populated after decisions reach Accepted status |
| `06 Prototype Implementations` | Links, notes, and documentation pointing to the GitHub prototype repository |

> **File naming convention for RFCs:** `RFC-IFC5-XXX-short-title.docx` where XXX matches the Decision ID in the Decision Register (e.g. `RFC-IFC5-001-entity-identity.docx`).

---

## The Decision Lifecycle

Every architectural decision moves through the following stages. The Decision Register tracks the current status of each.

```
Idea → Framed → Open Review → Prototype Required → Prototype Complete
     → Committee Review → Public Review → Accepted → Normative → Stable
```

| Stage | Meaning | Who Acts |
|---|---|---|
| **Idea** | Topic identified, not yet structured | Anyone |
| **Framed** | RFC drafted with problem statement and at least two alternatives | RFC Author |
| **Open Review** | RFC published for community comment | Working Group |
| **Prototype Required** | RFC flagged as needing a prototype before consensus can be reached | Working Group |
| **Prototype Complete** | Prototype built, documented, and linked in RFC | RFC Author + Engineers |
| **Committee Review** | Formal committee ballot | Committee Chair |
| **Public Review** | Wider public comment period | Committee Chair |
| **Accepted** | Consensus reached, decision adopted | Committee |
| **Normative** | Decision incorporated into specification text | Editors |
| **Stable** | Specification text stable; no further revision expected | Editors |

Transitions between stages require explicit action by the working group or committee — a decision does not advance automatically.

---

## How to Write an RFC

Use the RFC template in `02 RFCs/` as your starting point. Each RFC covers exactly one decision.

### RFC Sections

1. **Problem Statement** — What is broken, ambiguous, or missing? What decisions are blocked without resolving this?
2. **Background** — Relevant history, prior art, related standards, or earlier decisions this builds on.
3. **Existing IFC4.x Convention** — How is this handled today? Include schema references or examples.
4. **Proposed Approaches** — At minimum: the IFCX proposal and the IFC-ECS alternative. Document other alternatives briefly.
5. **Tradeoffs** — Compare approaches across: expressiveness, backward compatibility, tooling complexity, OpenUSD alignment, community familiarity.
6. **Recommendation** — The RFC author's current best thinking. This is not a committee decision; it is a starting point for discussion.
7. **Open Questions** — Numbered list of unresolved questions reviewers should focus on (Q1, Q2, etc.).
8. **Prototype** — Whether a prototype is required, where it lives, and its current status.
9. **Consequences** — What downstream decisions this unlocks or constrains if accepted.
10. **References** — Links to GitHub issues, related RFCs, IFC4.x schema sections, papers.

### RFC Quality Bar

Before marking an RFC as Open Review, the author should verify:

- [ ] Exactly one decision is addressed
- [ ] At least two alternatives are documented
- [ ] The IFC4.x convention is documented
- [ ] Tradeoffs are compared, not just listed
- [ ] Open Questions are numbered
- [ ] Prototype need is declared (Yes/No)
- [ ] Decision ID is assigned and added to the Decision Register

---

## How to Review an RFC

When you review an RFC, classify every comment using one of the following types. This allows the author to triage responses efficiently and ensures that blocking objections are visible.

| Type | Use When |
|---|---|
| **Editorial** | Grammar, clarity, wording — does not affect the technical content |
| **Technical Defect** | The RFC contains an error of fact or logic |
| **Semantic Concern** | The proposal may not mean what the author intends |
| **Compatibility Concern** | The proposal conflicts with existing IFC4.x usage or tooling |
| **Alternative Proposal** | You have a different approach not covered in the RFC |
| **Evidence** | You have data, examples, or prototypes relevant to the decision |
| **Blocking Objection** | You believe the RFC cannot be accepted as written |
| **General Support** | You support the recommendation |

Submit feedback via the **structured Google Form linked in the header and footer of each RFC** — this is the fastest path. For detailed technical comments, annotate the Google Doc directly. For broader discussion, open a [GitHub Discussion](https://github.com/Drshelden/IFCV5Work/discussions).

---

## How GitHub and Google Drive Work Together

This initiative deliberately separates **architecture** from **implementation**.

| Work Type | Home |
|---|---|
| Architectural discussion, RFCs, decisions | [Google Drive](https://drive.google.com/drive/folders/1U9J-6hAr5pM_Q28JChDcistHsAHgi33y) |
| Prototypes, schemas, validators, example files | GitHub (`buildingSMART/IFC5-development`, `Drshelden/IFC-ECS`) |
| Specification source (normative text) | [GitHub](https://github.com/Drshelden/IFCV5Work) (Markdown, after decisions are Accepted) |
| Bug reports, implementation issues | [GitHub Issues](https://github.com/Drshelden/IFCV5Work/issues) |
| Structured RFC feedback | Google Forms (linked in each RFC) |
| Broader discussion | [GitHub Discussions](https://github.com/Drshelden/IFCV5Work/discussions) |

Do not use GitHub Issues as the primary vehicle for architectural decisions. Discussion fragments across issues, context is lost, and it becomes very difficult to reach and record consensus. Large architectural questions belong in an RFC.

---

## How to Participate

### If you are new to the initiative

1. Read this guide.
2. Review the Decision Register (`01 Decision Register/`) to understand what is under discussion.
3. Pick one or two decisions in **Open Review** status and read the corresponding RFCs.
4. Submit comments using the classification system above.

### If you want to propose a new topic

1. Add a row to the Decision Register with status **Idea**, a brief topic description, and your name as Owner.
2. Draft an RFC using the template in `02 RFCs/`.
3. Share the draft with the working group for early feedback before moving to Open Review.

### If you are an RFC author

1. Own the decision through its lifecycle. You are responsible for updating the RFC, responding to comments, and coordinating any required prototypes.
2. Keep the Decision Register row up to date as status changes.
3. When the decision reaches Accepted, work with the editors to produce normative specification text.

### If you are a committee member

1. Engage during Committee Review with structured feedback.
2. Use the Blocking Objection category for genuine blockers — reserve it for issues that make a decision technically unsound or incompatible with IFC requirements.
3. Decisions that accumulate General Support and no unresolved Blocking Objections are ready to advance.

---

## Meetings and Notes

Meeting notes are stored in `00 Architecture Overview/`. Each meeting note captures:

- Decisions made (with Decision ID references)
- Action items (owner, due date)
- Unresolved questions carried forward
- Comments received and their resolution status

---

## Long-Term Vision

This initiative is building a living **Architecture Decision Book** for IFC5. When complete, it will provide a transparent, traceable record of every major design decision in IFC5 — what was considered, what was rejected and why, and what consensus was reached.

This record is valuable not just for building the specification, but for every implementer, researcher, and future contributor who needs to understand why IFC5 is designed the way it is.

---

*Last updated: July 2026. For questions about this process, contact the IFC5 Architecture Initiative working group.*
