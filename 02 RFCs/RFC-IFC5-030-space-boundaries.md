<!-- rfc-links -->
> **IFC5-030 — Space Boundaries and Topology** · Tier 3 — Domain Modeling
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-030) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-030+%E2%80%94+&labels=IFC5-030)

# RFC-IFC5-030: Space Boundaries and Topology

| Field | Value |
|---|---|
| **Decision ID** | IFC5-030 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-008, IFC5-016 |
| **Prototype Required** | No |
| **Source Topics** | Topic 36 |

---

## 1. Problem Statement

IFC4.x space boundaries (IfcRelSpaceBoundary, first/second/third level) encode the thermal and airflow topology of a building. They are critical for energy analysis. In IFC5, it is not defined how space boundaries map — whether they become child nodes of spaces, explicit relationship objects, or are dropped as out of scope.

## 2. Background

Space boundaries link spaces to the bounding elements (walls, floors, ceilings, windows) that form their thermal envelope. Second-level boundaries include connection geometry (the exact polygon of the boundary surface in local space). This information is required by energy simulation tools (EnergyPlus, IDA ICE, etc.).

In IFCX Hello Wall examples, space boundaries are not present. Whether this is an intentional omission or a placeholder is unclear.

## 3. Existing IFC4.x Convention

- IfcRelSpaceBoundary: links IfcSpace to bounding IfcElement
- 1st level: identifies which elements bound a space
- 2nd level: adds connection geometry (IfcConnectionGeometry)
- 3rd level: resolves openings within boundary surfaces
- Each boundary has identity, physical/virtual classification, and internal/external flag

## 4. Proposed Approaches

### 4.1 Space boundaries as child nodes of spaces

Each IfcRelSpaceBoundary becomes a named child node under its space. Boundary geometry and element reference are attributes. Aligns with scene-graph approach.

### 4.2 Space boundaries as explicit relationship objects

IfcRelSpaceBoundary is preserved as a named relationship node. Boundary geometry and element reference are preserved with full fidelity. Maximum compatibility with energy analysis tools.

### 4.3 Space boundaries as attributes on bounding elements

Each bounding element carries a `boundedSpaces` attribute listing the spaces it bounds. Inverse of the IFC4.x model; simpler traversal from element perspective.

### 4.4 Space boundaries deferred to a domain extension

Core IFC5 does not include space boundary encoding. Energy analysis exchanges use a domain extension or separate file.

## 5. Tradeoffs

| Dimension | Child nodes | Explicit objects | Element attributes | Deferred |
|---|---|---|---|---|
| Energy analysis tool compatibility | Moderate | High | Low | None |
| Scene-graph alignment | High | Low | Low | N/A |
| Boundary geometry fidelity | Moderate | High | Low | N/A |
| IFC4.x round-trip | Moderate | High | Low | None |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Are 2nd-level space boundaries (with connection geometry) in scope for IFC5 core, or only for energy analysis profiles?

**Q2.** Must space boundary identity (GlobalId) be preserved for simulation tool workflows?

**Q3.** How are corresponding boundaries (the matching boundary on the adjacent space) represented?

**Q4.** How are virtual boundaries (e.g., open boundaries between adjacent spaces) distinguished from physical ones?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Tied to relationship modeling (IFC5-008)
- Tied to spatial structure (IFC5-016)
- Relevant to model views (IFC5-020) — energy analysis profile

## 10. References

- IFC4 IfcRelSpaceBoundary schema
- buildingSMART Space Boundary Add-on View


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-030) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-030+%E2%80%94+&labels=IFC5-030)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
