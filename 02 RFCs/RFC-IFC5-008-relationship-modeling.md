# RFC-IFC5-008: Relationship Modeling Strategy

| Field | Value |
|---|---|
| **Decision ID** | IFC5-008 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-007 |
| **Prototype Required** | Yes |
| **Source Topics** | Topics 20, 21, 22 |

---

## 1. Problem Statement

IFC4.x uses explicit relationship entities (IfcRel*) as first-class objects to express every kind of association between building objects. IFC5 proposals disagree on whether these should be retained, replaced by scene hierarchy, expressed as reference attributes, or converted to components.

This decision affects the expressiveness, round-trip fidelity, and query behavior of IFC5. The 30+ IfcRel families each carry attributes, identities, and semantic distinctions that may be lost if they are collapsed into hierarchy.

## 2. Background

IFC4.x has explicit relationship families including IfcRelAggregates, IfcRelContainedInSpatialStructure, IfcRelDefinesByType, IfcRelDefinesByProperties, IfcRelAssociatesMaterial, IfcRelVoidsElement, IfcRelSpaceBoundary, and many others. Each can carry its own GlobalId, OwnerHistory, and attributes.

In IFCX Hello Wall examples, some relationships appear to be expressed as hierarchy (children), some as inheritance (inherits), and some are absent.

## 3. Existing IFC4.x Convention

All associations between objects are represented as explicit relationship entity instances. Relationships are queryable, have identity, and can carry attributes. Inverse attributes enable bidirectional traversal.

## 4. Proposed Approaches

### 4.1 Relationships retained as first-class objects

All IfcRel* entities are preserved as named nodes in IFC5. Identity, attributes, and inverse traversal are maintained. High round-trip fidelity; large file size.

### 4.2 Relationships as scene hierarchy

Decomposition and containment relationships are expressed by the `children` tree. Other relationship types become reference attributes. Simple; loses relationship identity and attributes.

### 4.3 Relationships as components (ECS)

Each relationship becomes a component attached to the relating entity. Component has its own GUID and type. Queryable; flat; loses hierarchy semantics.

### 4.4 Hybrid: hierarchy for structural, explicit for semantic

Parent-child hierarchy encodes decomposition and containment. Semantic relationships (material, type, classification, void) remain explicit objects. Preserves the distinctions IFC4.x cares about.

## 5. Tradeoffs

| Dimension | First-class | Hierarchy | Components | Hybrid |
|---|---|---|---|---|
| IFC4.x round-trip | High | Low | Moderate | High |
| File verbosity | High | Low | Moderate | Moderate |
| Query by relationship | Simple | N/A | Simple | Mixed |
| Relationship attributes | Full | Lost | Full | Mixed |
| USD alignment | Low | High | Low | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Which IfcRel families carry attributes or OwnerHistory that must be preserved? Which are pure structure?

**Q2.** Does the `children` map in IFCX examples semantically mean IfcRelAggregates, IfcRelContainedInSpatialStructure, both, or neither?

**Q3.** Can a single encoding strategy handle all 30+ relationship families, or is a family-by-family mapping required?

**Q4.** How are cross-file relationships expressed and validated?

## 8. Prototype

- **Required:** Yes
- **Notes:** Demonstrate void/fill relationships (IfcRelVoidsElement, IfcRelFillsElement) and spatial containment in both IFCX and ECS. Show what information is lost in each.

## 9. Consequences

- Directly affects spatial structure representation (IFC5-016)
- Affects round-trip fidelity (IFC5-018)
- Determines whether inverse attributes are needed (Topic 22)

## 10. References

- IFC4 ADD2 TC1: IfcRelationship hierarchy
- IFCX Hello Wall: `03 Reference Examples/`
