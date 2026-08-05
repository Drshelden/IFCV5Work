# Proposed Updates: RFC-IFC5-004 Path Model
**Batch:** 2026-08-04-001
**Themes addressed:** 1, 4

---

## Change 1: Add multi-hierarchy test case to §4.1
**Section:** [§4.1 Current IFCX — fragmented children maps](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#41-current-ifcx--fragmented-children-maps)
**Type:** Add example / test case
**Rationale:** aothms and Ev confirm that multiple simultaneous hierarchies pointing at the same UUID are architecturally supported, but no example demonstrates this. A Hello Wall variant with two concurrent trees (spatial + systems, or spatial + cost breakdown) addressing the same window UUID by different paths would confirm the design works as intended and correct the white paper's closed-world statement.

**Proposed addition:**
> **Planned test case:** A Hello Wall variant demonstrating two simultaneous hierarchies addressing the same window entity by UUID is needed to confirm this design in practice. Until this example exists, the claim that IFCX supports multi-tree views remains unverified. See white paper §3.1.1 for the corrected prose.

---

## Change 2: Add transform composition to §9 Open Questions
**Section:** [§9 Open Questions](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#9-open-questions)
**Type:** Add open question
**Rationale:** The transform composition gap identified in Ev's email (Theme 4) is a direct consequence of the paths-as-views design: when an entity's spatial position is expressed through a view graph rather than a direct parent relationship, which coordinate frame governs transform composition? This is unspecified.

**Proposed new question Q5:**
> **Q5.** When an entity appears in a spatial view that differs from where its local transform was originally authored (e.g., a window component with a wall-relative transform, appearing under a storey in the default spatial view), which graph is authoritative for composing transforms? Options: (a) the SpatialView graph always governs transform composition and the authored transforms must be expressed relative to the view-parent; (b) transforms are always relative to the entity's physical parent (the wall), and the SpatialView is purely navigational with no bearing on coordinate frames; (c) each SpatialView declares a `transformSpace` policy. A Hello Wall variant with a non-identity wall transform (e.g., 30° rotation + offset) is required to test any proposed answer.
