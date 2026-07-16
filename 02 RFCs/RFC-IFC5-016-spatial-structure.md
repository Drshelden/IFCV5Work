<!-- rfc-links -->
> **IFC5-016 — Spatial Structure and Decomposition** · Tier 3 — Domain Modeling
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-016) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-016+%E2%80%94+&labels=IFC5-016)

# RFC-IFC5-016: Spatial Structure and Decomposition

| Field | Value |
|---|---|
| **Decision ID** | IFC5-016 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-008, IFC5-010 |
| **Prototype Required** | No |
| **Source Topics** | Topics 23, 24 |

---

## 1. Problem Statement

In IFC4.x, spatial structure (Project → Site → Building → Storey → Space) is expressed via IfcRelAggregates and IfcRelContainedInSpatialStructure as separate relationship instances. In IFCX, the same hierarchy is expressed via the `children` map. The question is whether the IFC4.x semantic distinctions (aggregation vs. containment; whole-part vs. spatial containment) survive the mapping to scene hierarchy.

## 2. Background

In IFC4.x, aggregation (IfcRelAggregates) and spatial containment (IfcRelContainedInSpatialStructure) are distinct relationships with distinct semantics. An element may be contained in a storey (containment) but not decompose it (aggregation). Elements can be referenced in multiple spatial structures. In IFCX, all of this collapses into `children`.

## 3. Existing IFC4.x Convention

- IfcProject → IfcSite via IfcRelAggregates
- IfcSite → IfcBuilding via IfcRelAggregates
- IfcBuilding → IfcBuildingStorey via IfcRelAggregates
- IfcBuildingStorey → products via IfcRelContainedInSpatialStructure
- Products may also be referenced via IfcRelReferencedInSpatialStructure (non-owning)

## 4. Proposed Approaches

### 4.1 Scene hierarchy fully replaces spatial structure relationships

`children` encodes both aggregation and containment. Aggregation is implied by direct parenthood. Containment is also direct parenthood. Distinction is lost; round-trip requires heuristic recovery.

### 4.2 Scene hierarchy for aggregation; explicit relationship for containment

The `children` map encodes aggregation. Containment remains an explicit named attribute or relationship object. Preserves the semantic distinction.

### 4.3 All spatial relationships remain explicit

IfcRelAggregates and IfcRelContainedInSpatialStructure are preserved as explicit named objects. The `children` map is a navigational convenience and not normative.

### 4.4 Separate spatial structure sub-graph

A dedicated section of the scene graph encodes the spatial structure. Other hierarchy is organizational only. Spatial containment queries target this sub-graph.

## 5. Tradeoffs

| Dimension | Hierarchy only | Hierarchy + explicit containment | All explicit | Sub-graph |
|---|---|---|---|---|
| File simplicity | High | Moderate | Low | Low |
| Semantic round-trip | Low | High | High | High |
| IFC4.x query compatibility | Low | High | High | High |
| USD scene graph alignment | High | Moderate | Low | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must the distinction between IfcRelAggregates and IfcRelContainedInSpatialStructure survive in IFC5?

**Q2.** Can one element be spatially contained in more than one space (e.g., a column shared between floors)?

**Q3.** How are linear infrastructure spatial structures (IfcFacilityPart, IfcPositioningElement) expressed?

**Q4.** Does coordinate inheritance follow scene hierarchy or spatial structure?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Directly tied to relationship modeling decision (IFC5-008)
- Affects backward compatibility (IFC5-018)

## 10. References

- IFC4 IfcSpatialStructureElement documentation
- IFC4.3 infrastructure spatial structures


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-016) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-016+%E2%80%94+&labels=IFC5-016)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
