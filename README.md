# IFC5 Architecture Initiative

This repository contains the working RFCs and decision register for the IFC5 Architecture Initiative — a structured effort to develop the architectural foundations of IFC5 through transparent, consensus-based decision-making.

---

## What We Need From You

There are three things committee members should do, roughly in this order.

**1. Give feedback on the overall approach**

Read the [Process Guide](00%20Architecture%20Overview/IFC5_Process_Guide.md) and the [RFC Index](02%20RFCs/README.md) to get a feel for how the initiative is structured. Then open a [GitHub Discussion](../../discussions) with your reaction:

- Does the RFC-based process make sense for how the committee works?
- Are there structural problems with the approach before we invest further?
- Is anything important missing from how we've set this up?

This feedback will be used to update the process documents and RFC structure before we move into active review.

**2. Prioritize the RFC list**

Look at the 38 RFCs in the [RFC Index](02%20RFCs/README.md) and respond to the **[RFC Priority Poll](../../discussions)** (link to be posted) indicating for each RFC whether it should be:

- **Focus now** — high priority, needs resolution early
- **Defer** — too detailed or premature for this stage
- **Drop or merge** — out of scope or should be absorbed into another RFC

You can also propose additional RFCs that are missing from the list.

**3. Pick one RFC to review in depth**

Once priorities are clearer, we'll move a small set of RFCs to **Open Review**. At that point, read one RFC fully and submit structured comments using the [comment classification system](#submitting-comments) below.

---

## Repository Structure

```
/
├── 00 Architecture Overview/
│   └── IFC5_Process_Guide.md       ← Full process, roles, and lifecycle
│
├── 01 Decision Register/
│   └── IFC5_Decision_Register.csv  ← All 38 RFCs: status, tier, dependencies, owners
│
├── 02 RFCs/
│   ├── README.md                   ← RFC index by tier
│   └── RFC-IFC5-001-*.md through RFC-IFC5-038-*.md
│
├── 03 Reference Examples/          ← Canonical comparison examples
├── 04 Committee Feedback/          ← Comment logs and ballot responses
├── 05 Normative Specification/     ← Populated after decisions reach Accepted status
└── 06 Prototype Implementations/   ← Links to prototype repositories
```

---

## How Decisions Are Made

Every architectural question becomes an RFC. Each RFC documents the problem, at least two alternatives (always including the IFC4.x convention), tradeoffs, a recommendation, and numbered open questions.

RFCs move through this lifecycle:

```
Idea → Framed → Open Review → [Prototype Required → Prototype Complete]
     → Committee Review → Public Review → Accepted → Normative → Stable
```

All 38 RFCs are currently at **Idea** status. No decisions have been made yet.

The [Decision Register](01%20Decision%20Register/IFC5_Decision_Register.csv) tracks current status for every RFC.

---

## Submitting Comments

When reviewing an RFC, classify each comment so the author can triage efficiently:

| Type | Use when |
|---|---|
| **Editorial** | Grammar or clarity — no technical impact |
| **Technical Defect** | Error of fact or logic in the RFC |
| **Semantic Concern** | The proposal may not mean what the author intends |
| **Compatibility Concern** | Conflicts with IFC4.x usage or existing tooling |
| **Alternative Proposal** | You have a different approach not in the RFC |
| **Evidence** | You have data, examples, or prototypes relevant to the decision |
| **Blocking Objection** | The RFC cannot be accepted as written — reserve for genuine blockers |
| **General Support** | You support the recommendation |

- Line-level edits → open a **Pull Request**
- General comments → open a **GitHub Issue** referencing the RFC ID (e.g. `IFC5-007`)
- Broader discussion → start a **GitHub Discussion**

---

## Guiding Principles

1. **Decisions before specification.** Write the architecture first; the spec follows from consensus.
2. **One RFC per decision.** Bundling decisions makes consensus harder and traceability impossible.
3. **Alternatives required.** Every RFC documents at least two alternatives, including the IFC4.x convention.
4. **Evidence over opinion.** Arguments grounded in examples, prototypes, or prior art carry more weight.
5. **Prototypes gate acceptance.** RFCs marked ⚗️ require a working prototype before advancing to Committee Review.
6. **Structured feedback.** Use the comment classification system — it prevents important objections from getting buried.

---

*IFC5 Architecture Initiative · July 2026*
