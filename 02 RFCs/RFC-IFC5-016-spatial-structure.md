
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-016](https://docs.google.com/forms/d/e/1FAIpQLSdbV-KqEX8Xmiwc3d_R3RHuXS6mko2uBygFdM71plgWptHZrQ/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1tnkwFqGFUClv0UyG1r56l0MUWsw22QiFpkCwCfGUgcI/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-016">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-016+%E2%80%94+&labels=IFC5-016&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdbV-KqEX8Xmiwc3d_R3RHuXS6mko2uBygFdM71plgWptHZrQ/viewform">📋 Take the feedback form</a></td>
</tr></table>


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

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-016) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-016+%E2%80%94+&labels=IFC5-016&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1tnkwFqGFUClv0UyG1r56l0MUWsw22QiFpkCwCfGUgcI/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-016">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-016+%E2%80%94+&labels=IFC5-016&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdbV-KqEX8Xmiwc3d_R3RHuXS6mko2uBygFdM71plgWptHZrQ/viewform">📋 Take the feedback form</a></td>
</tr></table>
