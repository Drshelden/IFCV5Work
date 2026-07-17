
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-007](https://docs.google.com/forms/d/e/1FAIpQLSce4Os8BRJuMZBYqrfrBmj3h92ziHWZobz3CtV3G-IirF6GiA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) · [📝 Google Doc](https://docs.google.com/document/d/1nKwwHvS0g_69IfDc4kR0DpfNZBQgPHp7EvzuVJ-Jit8/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-007) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-007+%E2%80%94+&labels=IFC5-007&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSce4Os8BRJuMZBYqrfrBmj3h92ziHWZobz3CtV3G-IirF6GiA/viewform)


# RFC-IFC5-007: Scene Graph vs. ECS vs. Hybrid Architecture

| Field | Value |
|---|---|
| **Decision ID** | IFC5-007 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-001, IFC5-003, IFC5-004 |
| **Prototype Required** | Yes |
| **Absorbs** | Topic 58 (Ambiguities requiring explicit architectural decisions) |

---

## 1. Problem Statement

The two primary IFC5 proposals — IFCX and IFC-ECS — represent fundamentally different architectural paradigms. IFCX is a hierarchical scene graph with path-addressed nodes and inherited composition. IFC-ECS is a flat component array where entities are identified by GUID and components are attached independently. These two models make different tradeoffs, and it is not clear whether they can or should be unified.

This RFC asks: what is the primary structural organization of an IFC5 model?

## 2. Background

Both proposals share a common JSON substrate (see IFC5-039) and the concept of a "component" as a dictionary carrying semantic data. The structural differences are significant:

**IFCX component structure:**
```json
{
  "path": "/IfcProject/Site/Building/Wall-001",
  "attributes": {
    "ifc:Name": { "type": "IfcLabel", "value": "Wall-001" },
    "ifc:IsExternal": { "type": "IfcBoolean", "value": false }
  },
  "children": {
    "Geometry": { "path": "/IfcProject/Site/Building/Wall-001/Geometry", "attributes": { ... } }
  },
  "inherits": "/Templates/StandardWall"
}
```
Key structural fields: `path` (entity reference and address), `attributes`, optional `children`, optional `inherits`. No explicit component identity or component type beyond namespace conventions in attribute keys.

**IFC-ECS component structure:**
```json
{
  "entityGuid": "14adb22b-d474-48a2-8e8f-6d4c067c1953",
  "componentGuid": "5e3f2a1c-8b9d-4a3e-b2f7-9c1d0e4f6a8b",
  "componentType": "IfcWallIdentity",
  "attributes": {
    "Name": "Wall-001",
    "IsExternal": false
  }
}
```
Key structural fields: `entityGuid` (entity reference), `componentGuid` (component identity), `componentType` (semantic role), `attributes`. No hierarchy. Multiple components per entity aggregated at query time by matching `entityGuid`.

**Convergence point:** Both treat a component as a dict with an entity reference field and an attributes payload. This common structure is made explicit in IFC5-039. The divergence is in: (a) whether entity reference is path-based or GUID-based, (b) whether hierarchy is explicit or absent, (c) whether component identity is tracked, and (d) whether component type is a field or a namespace prefix.

Both have Hello Wall examples in `03 Reference Examples/`.

## 3. Existing IFC4.x Convention

IFC4.x is neither a scene graph nor an ECS. It uses explicit relationship entities (IfcRelAggregates, IfcRelContainedInSpatialStructure) to organize objects, and a deep inheritance hierarchy for type classification.

## 4. Proposed Approaches

### 4.1 Scene graph (IFCX / USD-aligned)

The primary organizational structure is a hierarchical `children` tree. IFC semantic relationships are mapped to hierarchy where possible. ECS-style component attachment is expressed as namespaced attribute groups on scene nodes.

### 4.2 Flat ECS

The primary structure is a flat array of components. Hierarchy is an optional derived view. Components contain all semantic data. Scene graph behavior is a query-time construction.

### 4.3 Hybrid: semantic scene graph with ECS attribute semantics

The top-level structure is a scene graph for navigation and hierarchy. Semantic data is organized as component-like attribute groups (ECS semantics without a flat array). Best of both; most complex.

### 4.4 Dual representation with defined mapping

IFC5 normatively defines both representations with a lossless mapping between them. Files declare which representation they use.

### 4.5 Common component primitive with profile-specific organization

IFC5 defines a shared component structure (see IFC5-039): a dict with an entity reference, an optional component type, optional component identity, and an attributes payload. Files organized as a scene graph place these components on hierarchy nodes; files organized as ECS collect them in a flat array. The same component dict structure is valid in both. Profile is declared at the document level.

This approach makes the scene-graph vs. ECS distinction a document-level organizational choice rather than a data model difference. The component is the fundamental unit; how components are organized is the profile.

## 5. Tradeoffs

| Dimension | Scene graph | Flat ECS | Hybrid | Dual rep | Common primitive |
|---|---|---|---|---|---|
| USD alignment | High | Low | Moderate | Partial | Moderate |
| Runtime query performance | Moderate | High | Moderate | High | High (ECS side) |
| IFC4.x round-trip | Moderate | Low | Moderate | High | Moderate |
| Authoring tool integration | High | Low | Moderate | Low | Moderate |
| File size / redundancy | Moderate | Low | Moderate | High | Low |
| Conceptual simplicity | Moderate | High | Low | Low | High |
| Override / archetype support | High (path-based) | Low | Moderate | High | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Can a scene graph and a flat ECS represent exactly the same IFC semantic information? If not, which constructs cannot be represented in each?

**Q2.** Is the `children` map in IFCX semantically equivalent to IFC decomposition (IfcRelAggregates), or is it a navigational convenience?

**Q3.** If ECS is the runtime model, must the exchange format serialize the ECS directly, or may it use a more human-friendly scene graph that is translated to ECS at load time?

**Q4.** Should a wall with multiple semantic relationships (spatial containment, material association, type definition) appear in the hierarchy once, multiple times, or be addressed by multiple paths?

**Q5.** Should components have a **required minimum field set** regardless of architectural approach — e.g., an entity reference (GUID or path), an optional component type, and an attributes payload — so that cross-profile tools can process IFC5 data without knowing the full architectural mode?

**Q6.** In the ECS model, components associated with a specific entity must be aggregated at runtime by matching `entityGuid`. Should this aggregation behavior be **normatively specified** (including ordering and conflict resolution rules), or left to implementation? Does the scene graph model have an equivalent aggregation step?

**Q7.** IFCX's `path` field serves simultaneously as an entity identity and a structural address. IFC-ECS's `entityGuid` is purely an identity. Are these semantically equivalent, or does the path-as-address create a dependency on the parent hierarchy that GUID does not? (See also IFC5-003, IFC5-004.)

## 8. Prototype

- **Required:** Yes
- **Notes:** Demonstrate the Hello Wall example in both representations and define a lossless mapping between them.

## 9. Consequences

This is the highest-dependency RFC after IFC5-001. It directly shapes:
- Relationship modeling (IFC5-008)
- Class and type representation (IFC5-009)
- Spatial structure (IFC5-016)
- Geometry architecture (IFC5-014)
- Property sets (IFC5-013)
- Archetype and override mechanisms (IFC5-040) — the feasibility of GUID-based overrides vs. path-based overrides depends critically on which architecture is chosen
- Foundational component primitive definition (IFC5-039)

## 11. Absorbed Topic: Architectural Ambiguities (Topic 58)

Topic 58 of the source inventory lists 20 ambiguities that require explicit architectural decisions. These are not a separate RFC — they are the specific questions this RFC (and the tier-1/tier-2 RFCs it depends on) must answer. They are listed here as a checklist to ensure none are lost:

1. Is IFCX fundamentally ECS, scene graph, or hybrid? **(This RFC)**
2. Are IFC classes first-class schema types or classification attributes? **(IFC5-009)**
3. Are relationships retained explicitly or inferred from hierarchy? **(IFC5-008)**
4. Is `children` semantically equivalent to IFC decomposition? **(IFC5-016)**
5. Is `inherits` semantically equivalent to IFC type assignment? **(IFC5-010)**
6. Are path and identity the same concept? **(IFC5-003, IFC5-004)**
7. Are repeated path records compositional layers or fragmented authoring? **(IFC5-011)**
8. Are property sets preserved or flattened? **(IFC5-013)**
9. Are type objects classes, prototypes, or ordinary data nodes? **(IFC5-009)**
10. Is OpenUSD compatibility syntactic, semantic, or conceptual? **(IFC5-015)**
11. Is tessellated geometry sufficient for standard exchange? **(IFC5-014)**
12. Can an IFCX file be validated without resolving remote imports? **(IFC5-019)**
13. Are namespaces URI-backed? **(IFC5-005)**
14. Can extensions redefine existing IFC attributes? **(IFC5-032)**
15. How are conflicts between inherited and directly authored values resolved? **(IFC5-010)**
16. Which information is authoritative when hierarchy and explicit relationships disagree? **(IFC5-008)**
17. Which information is authoritative when semantic and mesh geometry disagree? **(IFC5-014)**
18. What constitutes lossless IFC4.x migration? **(IFC5-018)**
19. How are partial models distinguished from invalid models? **(IFC5-019)**
20. What minimum subset must every IFCX implementation support? **(IFC5-038)**

## 10. References

- IFCX Hello Wall: `03 Reference Examples/hello-wall.ifcx`
- IFC-ECS Hello Wall: `03 Reference Examples/hello-wall-ifc-ecs.json`
- OpenUSD architecture documentation


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) · [📝 Google Doc](https://docs.google.com/document/d/1nKwwHvS0g_69IfDc4kR0DpfNZBQgPHp7EvzuVJ-Jit8/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-007) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-007+%E2%80%94+&labels=IFC5-007&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSce4Os8BRJuMZBYqrfrBmj3h92ziHWZobz3CtV3G-IirF6GiA/viewform)
