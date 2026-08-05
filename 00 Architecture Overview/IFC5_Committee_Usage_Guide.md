# IFC5 Architecture Initiative — Committee Usage Guide

**Version:** 0.1 Draft · July 2026

---

## What This Setup Is For

The initiative uses a structured workspace — mirrored across GitHub and Google Drive — to move 41 architectural decisions from open questions to normative text. Every tool in the setup (the folder structure, the RFC documents, the forms, the Decision Register, GitHub Discussions) exists to serve that progression. This guide explains how to use it.

---

## The Folder Structure as a Workflow

The seven folders map directly to the stages of work:

**`00 Architecture Overview`** is the starting point. The Process Guide and this document live here. Meeting notes go here too — each note should capture decisions made (with their RFC IDs), action items with owners and due dates, and unresolved questions carried forward.

**`01 Decision Register`** is the committee's shared scoreboard. It tracks every RFC's current status, tier, owner, and prototype requirement. Before and after every meeting, the RFC author for any decision that advanced should update this register. If the register doesn't reflect what was decided in a meeting, the meeting didn't officially happen.

**`02 RFCs`** is where the substantive work lives. One document per decision. This is where committee members spend most of their time during review cycles.

**`03 Reference Examples`** provides concrete test cases — IFC-SPF, IFCX, and IFC-ECS representations of the same building elements. When an RFC debate becomes abstract, the committee should anchor it in one of these examples. If a proposed approach can't be illustrated with a Hello Wall–style example, that's a signal the approach may not be ready.

**`04 Committee Feedback`** stores comment resolution logs and ballot responses. After each review round, the RFC author should log which comments were addressed, which were deferred, and which resulted in RFC changes. This is the audit trail.

**`05 Normative Specification`** starts empty and stays that way until a decision reaches Accepted status. Once it does, the RFC author works with editors to draft specification text here. This folder being mostly empty is expected and healthy during the review phase — it fills as decisions mature.

**`06 Prototype Implementations`** links to GitHub prototype work. RFCs marked ⚗️ cannot advance to Committee Review until a prototype is documented and linked here.

---

## How RFCs Are Processed

Every RFC moves through a defined lifecycle. The committee's job is to advance decisions through it — not to let them sit at Open Review indefinitely.

**Prioritization comes first.** Before any RFC enters Open Review, the committee fills out the RFC Priority Survey. This determines which decisions are worked first. Tier 1 (Foundational) RFCs gate everything else, so if the survey reveals disagreement about priorities, resolve that before opening review on individual RFCs.

**Open Review is structured, not open-ended.** When an RFC enters review, committee members submit feedback through three channels: the structured Google Form linked in the RFC header (required for all substantive input), inline Google Doc comments (for text-specific notes), and GitHub Discussions (for broader technical debate). Every comment must carry a classification label — Editorial, Technical Defect, Semantic Concern, Compatibility Concern, Alternative Proposal, Evidence, Blocking Objection, or General Support. This isn't bureaucratic overhead; it's what allows the RFC author to distinguish a blocking objection from a wording preference and triage accordingly.

**First-round feedback is expansive; second-round is focused.** In the first round, committee members may add new Open Questions, propose alternatives not in the RFC, challenge scope, or identify dependencies. In the second round, the RFC has been revised and feedback should concentrate on whether the revisions resolved the outstanding concerns. The goal is convergence, not indefinite iteration.

**Blocking Objections require explicit handling.** Any comment classified as Blocking Objection must be either resolved (with the resolution noted in `04 Committee Feedback`) or escalated to a formal vote before the RFC can advance. A Blocking Objection is not a veto — it is a documented claim that the RFC is technically unsound or incompatible with IFC requirements, which the committee then adjudicates.

**Prototype-gated RFCs follow a branching path.** If an RFC is marked ⚗️, the working group must commission or build a prototype after Open Review closes. The prototype is documented in `06 Prototype Implementations` and cross-linked in the RFC. Committee Review cannot begin until the prototype is complete and the committee has had an opportunity to evaluate it against the reference examples in `03`.

**Committee Review produces a recorded decision.** When an RFC has cleared Open Review, incorporated feedback, and (if required) completed its prototype, the committee chair opens a formal ballot. The outcome — Accepted, Rejected, or Returned for Revision — is recorded in both the RFC document itself and in the Decision Register. An Accepted decision then triggers specification drafting in `05`.

---

## What the Committee Should Not Do

Do not use GitHub Issues as a substitute for the RFC process. Issues fragment context and make it nearly impossible to reach and record consensus on architectural questions. If a substantive architectural concern surfaces in an issue, promote it to an RFC.

Do not let decisions advance through lifecycle stages without explicit action. The Decision Register does not update itself. Status changes require a deliberate decision — in a meeting, with a recorded outcome.

Do not populate `05 Normative Specification` with text from an RFC that hasn't reached Accepted status. The separation between decision-making and specification-writing is intentional. Writing spec text for an unresolved question is premature and creates confusion about what is and isn't settled.

---

## The Discipline This Requires

The setup only works if committee members engage through the designated channels, classify their comments, and update the Decision Register when status changes. The forms, labels, and folder conventions are not optional polish — they are the mechanism by which the committee's collective intelligence gets captured rather than lost in email threads and meeting chat.

---

*IFC5 Architecture Initiative · July 2026*
