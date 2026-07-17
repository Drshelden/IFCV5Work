
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-007](https://docs.google.com/forms/d/e/1FAIpQLSce4Os8BRJuMZBYqrfrBmj3h92ziHWZobz3CtV3G-IirF6GiA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1afE8DWWkneA_8SPE1nDTQ9gVwXSMyabRLg4VNbpJfOw/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-007">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-007+%E2%80%94+&labels=IFC5-007&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSce4Os8BRJuMZBYqrfrBmj3h92ziHWZobz3CtV3G-IirF6GiA/viewform">📋 Take the feedback form</a></td>
</tr></table>


# RFC-IFC5-007: Scene Graph vs. ECS vs. Hybrid Architecture

| Field | Value |
|---|---|
| **Decision ID** | IFC5-007 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-001, IFC5-003, IFC5-004 |
| **Prototype Required** | Yes |
| **Source Topics** | Topics 10, 11, 12, 58 |
| **Absorbs** | Topic 58 (Ambiguities requiring explicit architectural decisions) |

---

## 1. Problem Statement

The two primary IFC5 proposals — IFCX and IFC-ECS — represent fundamentally different architectural paradigms. IFCX is a hierarchical scene graph with path-addressed nodes and inherited composition. IFC-ECS is a flat component array where entities are identified by GUID and components are attached independently. These two models make different tradeoffs, and it is not clear whether they can or should be unified.

This RFC asks: what is the primary structural organization of an IFC5 model?

## 2. Background

- **IFCX**: Hierarchical `children` tree; `inherits` for prototype composition; attributes under `attributes`; namespaced. Scene-graph oriented. Close to OpenUSD.
- **IFC-ECS**: Flat array of components; each component has `entityGuid`, `componentGuid`, `componentType`. No hierarchy. Runtime/database oriented.

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

## 5. Tradeoffs

| Dimension | Scene graph | Flat ECS | Hybrid | Dual rep |
|---|---|---|---|---|
| USD alignment | High | Low | Moderate | Partial |
| Runtime query performance | Moderate | High | Moderate | High |
| IFC4.x round-trip | Moderate | Low | Moderate | High |
| Authoring tool integration | High | Low | Moderate | Low |
| File size / redundancy | Moderate | Low | Moderate | High |
| Conceptual simplicity | Moderate | High | Low | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Can a scene graph and a flat ECS represent exactly the same IFC semantic information? If not, which constructs cannot be represented in each?

**Q2.** Is the `children` map in IFCX semantically equivalent to IFC decomposition (IfcRelAggregates), or is it a navigational convenience?

**Q3.** If ECS is the runtime model, must the exchange format serialize the ECS directly, or may it use a more human-friendly scene graph that is translated to ECS at load time?

**Q4.** Should a wall with multiple semantic relationships (spatial containment, material association, type definition) appear in the hierarchy once, multiple times, or be addressed by multiple paths?

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

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-007) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-007+%E2%80%94+&labels=IFC5-007&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1afE8DWWkneA_8SPE1nDTQ9gVwXSMyabRLg4VNbpJfOw/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-007">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-007+%E2%80%94+&labels=IFC5-007&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSce4Os8BRJuMZBYqrfrBmj3h92ziHWZobz3CtV3G-IirF6GiA/viewform">📋 Take the feedback form</a></td>
</tr></table>
