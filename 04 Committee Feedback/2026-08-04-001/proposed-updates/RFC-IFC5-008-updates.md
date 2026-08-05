# Proposed Updates: RFC-IFC5-008 Relationship Modeling
**Batch:** 2026-08-04-001
**Themes addressed:** 3

---

## Change 1: Add side-by-side comparison to Open Questions
**Section:** [Open Questions](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md)
**Type:** Add open question + action
**Rationale:** The IfcRel* dispute (Theme 3) cannot be resolved by argument alone. Both sides have stated positions; a side-by-side comparison of 2-3 concrete many-to-many cases is needed for the committee to make an informed decision.

**Proposed new open question:**
> **Q-NEW: Many-to-many relationship comparison.** The committee requires a side-by-side representation of the following relationships in both approaches — (1) ECS typed component style, (2) IfcRel* objectified style — for exactly these three cases: (a) IfcRelAssociatesMaterial (many walls, one material layer set), (b) IfcRelInterferesElements (two elements, optional description of interference geometry), (c) IfcRelReferencedInSpatialStructure (one element referenced in multiple spatial zones without being contained in any). The comparison must show the data structure, the query pattern, and the provenance attachment point for each. This comparison is a precondition for closing the relationship modeling decision.
