
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-004](https://docs.google.com/forms/d/e/1FAIpQLSfDHMqhIcI00IVfEHG9tAuxbEeahzkNHuRtW12PeneYAp1qyg/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1JD7KHmW5fwjUBapXcve7XN2TvwoOM5LKrx4kwkIIQj0/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-004) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-004+%E2%80%94+&labels=IFC5-004&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfDHMqhIcI00IVfEHG9tAuxbEeahzkNHuRtW12PeneYAp1qyg/viewform)


# RFC-IFC5-004: Path Model and Addressing

| Field | Value |
|---|---|
| **Decision ID** | IFC5-004 |
| **Status** | Draft Recommendation |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | [IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) |
| **Related** | [IFC5-016](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md), [IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md), [IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md) |
| **Prototype Required** | Yes |

> **Extended analysis:** A full treatment of the alternatives, tradeoffs, edge-directionality discussion, and composition override path analysis is in [`IFC5-Path-Model-Architecture-Discussion.md`](../03%20Reference%20Examples/IFC5-Path-Model-Architecture-Discussion.md).

---

## 1. Problem Statement

IFCX uses path strings for two purposes that share a single mechanism: (1) defining the scene graph / spatial hierarchy, and (2) targeting sub-nodes within a prototype for composition overrides. This unification, inherited from OpenUSD, creates several problems in the AEC context:

- **Identity conflated with position.** An entity's UUID is simultaneously its identity and its scene graph address. This enforces a single canonical tree, preventing multiple simultaneous organisational views over the same entity set.
- **Single-tree constraint.** IFC4X supports multiple simultaneous graphs (structural, spatial, maintenance, phase) via the `IfcRel*` family. IFCX's path model has no principled representation for these secondary graphs.
- **Multi-party authorship.** USD's LIVRPS composition resolves conflicting opinions by having one layer win. In federated AEC authorship, design-intent and as-built assertions must coexist with independent provenance — neither silently overwriting the other.
- **Dual-use ambiguity.** The same path namespace serves scene graph organisation and composition override targeting. Separating or unifying these uses is a non-trivial architectural decision with long-term consequences.

---

## 2. Background

In OpenUSD, prim paths are slash-delimited strings (e.g. `/World/Building/Wall`) that simultaneously locate a prim in the scene graph and serve as the address at which composition opinions accumulate. IFCX inherits this design, using UUIDs as path values in the `path` field and labels in the `children` map.

In IFC4X, there is no path concept. Objects are addressed by GlobalId or STEP instance number. Hierarchy is expressed through `IfcRel*` relations — `IfcRelAggregates` for spatial decomposition, `IfcRelContainedInSpatialStructure` for element containment.

---

## 3. The Dual Use of Paths

### 3.1 Scene graph definition

IFCX expresses the spatial hierarchy by fragmenting the tree across path records:

```json
{ "path": "14adb22b-...", "children": { "My_Site": "e0834921-..." } }
{ "path": "e0834921-...", "children": { "My_Building": "e84dc79e-..." } }
{ "path": "44af358b-...", "children": { "Wall": "93791d5d-...", "My_Space": "e3035b71-..." } }
```

Each entity has one canonical path, enforcing a single-tree closed-world assumption.

### 3.2 Composition override targeting

The same path namespace is used to target sub-nodes within a prototype for per-instance overrides, following USD's "over" mechanism. An instance can override any sub-prim of its inherited type at any depth using standard path syntax, and the composition engine resolves LIVRPS at each level.

These two uses of paths are **architecturally distinct** in scope: scene graph paths are global (address entities across the model); composition paths are local (address template slots within one typical). Keeping them unified (as IFCX does) requires implementing the full USD composition engine before any entity can be fully read. Separating them enables flat, schema-free-parseable entity descriptions.

---

## 4. Proposed Approaches for Scene Graph Organisation

### 4.1 Current IFCX — fragmented children maps

Each path record carries a `children` map for one level of the hierarchy. The full tree is assembled by reading multiple records and traversing the graph. Identity and position are the same thing; a single canonical tree is enforced.

**Problem:** Closed-world single-tree assumption. No multi-party authorship. No multiple simultaneous views.

### 4.2 Monolithic SpatialView component

A single typed component carries the complete path→UUID map for a named view:

```json
{
  "type": "ifc:SpatialView",
  "entity": "14adb22b-...",
  "attributes": {
    "name": "spatial-default",
    "children": {
      "My_Project/My_Site/My_Building/My_Storey/Wall": "93791d5d-..."
    }
  }
}
```

**Plusses:** Atomic, immediately readable, full paths explicit, multiple views distinct.  
**Minuses:** Does not scale; federation requires whole-view merge; one provenance block for entire hierarchy; partial updates expensive; closed-world absence semantics.

### 4.3 Distributed SpatialMembership components (child→parent)

Each entity carries a membership component pointing up to its parent in a named view:

```json
{
  "type": "ifc:SpatialMembership",
  "entity": "93791d5d-...",
  "attributes": { "view": { "ref": "view-uuid" }, "parent": { "ref": "44af358b-..." }, "name": "Wall" }
}
```

**Plusses:** OWA-compliant; fine-grained provenance; scales; federation-friendly.  
**Minuses:** Graph traversal required; no atomic snapshot; sibling name uniqueness is a soft constraint; path strings must be reconstructed; redundant with IfcRels for spatial views.

### 4.4 Distributed SpatialMembership (parent→child, one-per-pair)

Each relationship is its own component on the parent entity, one child per component:

```json
{
  "type": "ifc:SpatialMembership",
  "entity": "44af358b-...",
  "attributes": { "view": { "ref": "view-uuid" }, "child": { "ref": "93791d5d-..." }, "pathLabel": "Wall" }
}
```

**Plusses:** OWA-compliant (adding an entity is one new component, no existing modification); consistent with IfcRel directionality.  
**Minuses:** Functionally identical to `IfcRelContainedInSpatialStructure` — re-derives the IfcRel pattern without adding capability.

### 4.5 IfcRels as the view graph (recommended for default spatial view)

The default spatial hierarchy is already expressed by `ifc:IfcRelAggregates` and `ifc:IfcRelContainedInSpatialStructure`. A lightweight `ifc:SpatialView` descriptor names the view and declares which relation types constitute it:

```json
{
  "type": "ifc:SpatialView",
  "entity": "14adb22b-...",
  "attributes": {
    "name": "spatial-default",
    "root": { "ref": "14adb22b-...", "pathLabel": "My_Project" },
    "composedFrom": [
      "ifc:IfcRelAggregates",
      "ifc:IfcRelContainedInSpatialStructure"
    ]
  }
}
```

Path segment labels are carried on the `relatedObjects`/`relatedElements` entries of the IfcRel components via an optional `pathLabel` field:

```json
{
  "type": "ifc:IfcRelContainedInSpatialStructure",
  "entity": "44af358b-...",
  "attributes": {
    "relatedElements": [
      { "ref": "93791d5d-...", "pathLabel": "Wall"     },
      { "ref": "2c2d549f-...", "pathLabel": "Window"   },
      { "ref": "592504dc-...", "pathLabel": "Window_001" }
    ]
  }
}
```

**Plusses:** No redundancy; provenance/OWA/multi-party come free; architecturally consistent; partial updates are cheap (add one IfcRel component); path label co-located with containment assertion.  
**Minuses:** Semantic containment and navigational organisation may need to diverge; custom views without IfcRel types require a fallback.

**Fallback for custom views** (cost breakdown, maintenance zones, phase groupings): the SpatialView descriptor carries an explicit `children` map or references a custom relation type. For custom membership components, parent→child one-per-pair directionality is recommended, consistent with IfcRel conventions.

---

## 5. Composition Override Paths (Slot Names)

For composition override targeting — addressing template slots within an `ifc:IfcTypical` for per-instance override — the proposed architecture uses `slotName` strings within `componentTemplates`. These are **distinct from scene graph paths**:

- Scene graph paths: global scope, address entities across the model
- Slot names: local scope, address component templates within one typical

```json
"componentTemplates": [
  { "slotName": "geometry/Frame",   "type": "usd:MeshGeometry", "inheritable": true },
  { "slotName": "geometry/Glazing", "type": "usd:MeshGeometry", "inheritable": true }
]
```

**Normative requirement:** `slotName` must support `/`-separated path nesting for multi-level typical hierarchies. The composition engine must resolve slot paths recursively through nested typicals. This must be specified normatively in RFC-IFC5-040.

**The separation is correct for the AEC domain.** Unifying scene graph and composition paths (as USD does) requires implementing the full composition engine before any entity can be read. Separating them enables flat, schema-free-parseable entity descriptions and correct multi-view OWA semantics. The one capability lost is unified cross-cutting queries; this is an acceptable tradeoff given the federation and multi-party requirements of AEC.

---

## 6. Edge Directionality

When expressing hierarchy as typed components (approaches 4.3–4.5), the direction of graph edges matters for OWA compliance:

| Direction | Adding entity requires modifying existing component? | Consistent with IfcRels? |
|---|---|---|
| Child → Parent | No | No (IfcRels are parent→child) |
| Parent → Child, accumulated list | Yes — violates OWA for additions | Partially |
| Parent → Child, one-per-pair | No | Yes |

**Recommendation:** For custom view membership components (where no IfcRel type exists), use parent→child one-per-pair. This is OWA-compliant, consistent with IfcRel directionality, and avoids modifying existing components when adding entities.

---

## 7. Tradeoffs Summary

| Criterion | Fragmented IFCX | Monolithic SpatialView | Distributed (child→parent) | IfcRels as view graph |
|---|---|---|---|---|
| Multiple simultaneous views | No | Yes | Yes | Yes |
| OWA compliant | No | Partial | Yes | Yes |
| Scales to large models | Yes | No | Yes | Yes |
| Federation / multi-party | No | Awkward | Clean | Clean |
| Granular provenance | No | No | Yes | Yes |
| Redundancy with IfcRels | N/A | Partial | Full | None |
| Custom views | N/A | Yes | Yes | Requires fallback |
| Path strings stored | Implicit | Yes | No (reconstructed) | No (reconstructed) |

---

## 8. Recommendation

**R1 — Default spatial view.** Express it as the graph induced by `ifc:IfcRelAggregates` and `ifc:IfcRelContainedInSpatialStructure`, named by a lightweight `ifc:SpatialView` descriptor carrying `name`, `root`, and `composedFrom`. Do not introduce a separate `SpatialMembership` component for spatial views — the IfcRels already fulfil this role.

**R2 — Path segment labels.** Add an optional `pathLabel` field to ref objects within `relatedObjects`/`relatedElements` of containment IfcRels. When absent, fall back to the entity's `name` attribute.

**R3 — Custom views.** For organisational hierarchies with no matching IfcRel type, use the SpatialView descriptor with an explicit `children` map, or define a new typed relation component in parent→child one-per-pair form.

**R4 — Composition slot names.** Specify `slotName` normatively in RFC-IFC5-040 as a `/`-separated scoped path system supporting multi-level nesting. Keep scene graph and composition namespaces separate.

**R5 — Identity.** UUID is canonical identity; path strings are derived, reconstructed navigational aliases. A path change never changes a UUID.

---

## 9. Open Questions

**Q1.** For custom view types (cost breakdown, structural system) that recur across many projects — should standard IfcRel types be defined for these in the IFC5 schema, or should they always use the generic fallback?

**Q2.** When two IfcRelAggregates components on the same parent entity have different `participatesIn` view refs (design-intent spatial tree vs. as-built spatial tree), how does a consumer select which to use? Is a query-time view filter sufficient, or does the SpatialView descriptor need an explicit authority rank?

**Q3.** The `pathLabel` field on a ref object is a new pattern in the schema. Should it be defined on `LocalRef` directly, or as a specialised ref type (`ContainedRef`) to avoid polluting all ref usage?

**Q4.** For the composition slot path (`slotName`), what is the normative resolution order when a slot is addressed at multiple levels of nested typicals — innermost wins, or outermost wins?

---

## 10. Consequences

- Determines scene graph navigation model ([IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md))
- Affects federation cross-references ([IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md))
- Determines composition override mechanism ([IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md))
- Requires update to `IfcSpatialViewAttributes` in schema and `hello-wall-ifcy.json` example

---

## 11. References

- [`IFC5-Path-Model-Architecture-Discussion.md`](../03%20Reference%20Examples/IFC5-Path-Model-Architecture-Discussion.md) — Full alternatives analysis with tradeoff tables
- OpenUSD Path documentation and LIVRPS composition model
- IFCX Hello Wall example (`03 Reference Examples/Hello-Wall/hello-wall.ifcx.json`)
- IFCY Hello Wall example (`03 Reference Examples/Hello-Wall/hello-wall-ifcy.json`)


---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1JD7KHmW5fwjUBapXcve7XN2TvwoOM5LKrx4kwkIIQj0/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-004) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-004+%E2%80%94+&labels=IFC5-004&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfDHMqhIcI00IVfEHG9tAuxbEeahzkNHuRtW12PeneYAp1qyg/viewform)
