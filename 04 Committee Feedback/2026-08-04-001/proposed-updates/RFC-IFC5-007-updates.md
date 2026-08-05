# Proposed Updates: RFC-IFC5-007 Scene Graph vs ECS
**Batch:** 2026-08-04-001
**Themes addressed:** 3, 6

---

## Change 1: Expand IfcRel* removal rationale in background
**Section:** [§2 Background](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#2-background)
**Type:** Background expansion
**Rationale:** The RFC does not explain why IfcRel* was removed. Without this, committee members cannot evaluate whether the removal was deliberate or an oversight. aothms's explanation is the clearest available: in Express, objectified relationships provided modularity through inverses and abstract supertypes within a global schema; in ECS, typed components with identity and provenance already provide this.

**Proposed addition:**
> **On the removal of IfcRel* objectified relationships:** In IFC4 Express, objectified relationships (IfcRel* entities) served a specific purpose: they provided schema-level modularity through inverse attributes and abstract supertypes, allowing new relationship types to be added without modifying existing entity definitions. In an ECS model this mechanism is unnecessary — any typed component can carry provenance and identity, and new relationship semantics can be expressed as new component types without touching existing ones. The IFC 5 development work therefore removes IfcRel* as a first-class construct. This decision is contested; see RFC-008 for the open comparison.

---

## Change 2: Resolve absorbed Topic 17 — geometry authority
**Section:** Topic 17 (geometry authority when semantic and mesh disagree)
**Type:** Add proposed resolution
**Rationale:** louistrue's prototype (Discussion #3) provides a concrete answer to Topic 17: the highest-tier representation present is authoritative; all lower tiers are derived caches. This should be documented as a candidate resolution.

**Proposed addition:**
> **Topic 17 — candidate resolution (from prototype evidence):** The louistrue geometry-tiers prototype proposes a tier-authority rule: the highest tier present (procedural > BRep > mesh) is authoritative; lower tiers are derived caches. A derived tier carries a content hash (JCS + SHA-256) of its source, allowing consumers to detect freshness without re-deriving. This is one concrete answer; the committee should decide whether to adopt it. See RFC-014 §5 for the tradeoff table.
