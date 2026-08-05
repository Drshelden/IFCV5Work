# Proposed Updates: RFC-IFC5-033 Change and Collaboration
**Batch:** 2026-08-04-001
**Themes addressed:** 7

---

## Change 1: Add content-hash supersession pattern to Approaches
**Section:** [Proposed Approaches](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md)
**Type:** Add approach
**Rationale:** Theme 7: component `id` fields are currently unused for anything beyond uniqueness; there is no mechanism for marking one component as superseding another. louistrue's content-hash pattern provides a lightweight supersession/staleness mechanism that gives `id` a functional role.

**Proposed new approach:**
> **Content-hash supersession (candidate approach):** A component that is derived from or intended to supersede another carries: (1) the source component's `id` in a `supersedesId` field, and (2) a `sourceHash` field (`sha256-<hex>`) containing the RFC 8785 JCS canonical hash of the source component at derivation time. A consumer can then determine whether the derived component is `fresh` (hash matches the source as currently known), `stale` (hash differs — source has changed since derivation), or `unknown` (no hash). This pattern is lightweight, requires no central registry, and is machine-verifiable without trusting the producer. It is compatible with the open-world assumption: a missing `supersedesId` means the component is independent, not that no supersession exists.
