# IFC5 Path Model — Architecture Discussion

*Discussion paper for RFC-IFC5-004 (Path Model) and RFC-IFC5-040 (Archetypes, Templates, and Overrides)*

*IFC5 Working Group — July 2026*

---

## Table of Contents

1. [The Role of Paths in IFCX](#1-the-role-of-paths-in-ifcx)
2. [Problems with the IFCX Path Model](#2-problems-with-the-ifcx-path-model)
3. [Alternative Approaches for Scene Graph Organisation](#3-alternative-approaches-for-scene-graph-organisation)
   - [3.1 Monolithic SpatialView component](#31-monolithic-spatialview-component)
   - [3.2 Distributed SpatialMembership components](#32-distributed-spatialmembership-components)
   - [3.3 Hybrid: lightweight descriptor + distributed membership](#33-hybrid-lightweight-descriptor--distributed-membership)
   - [3.4 IfcRels as the view graph](#34-ifcrels-as-the-view-graph)
   - [3.5 Graph edge directionality: child→parent vs parent→child](#35-graph-edge-directionality-childparent-vs-parentchild)
4. [The Dual Use of Paths in IFCX](#4-the-dual-use-of-paths-in-ifcx)
   - [4.1 Scene graph definition vs. composition override targeting](#41-scene-graph-definition-vs-composition-override-targeting)
   - [4.2 How the proposed architecture separates these concerns](#42-how-the-proposed-architecture-separates-these-concerns)
   - [4.3 The gap for deeply nested typicals](#43-the-gap-for-deeply-nested-typicals)
   - [4.4 Interaction between the two concerns](#44-interaction-between-the-two-concerns)
5. [Summary Comparison](#5-summary-comparison)
6. [Conclusion and Recommendation](#6-conclusion-and-recommendation)

---

## 1. The Role of Paths in IFCX

IFCX uses path strings for two distinct purposes that share a single mechanism:

**Purpose 1 — Scene graph definition.** The `path` field carries a UUID that locates an entity in the spatial/containment hierarchy. The `children` map on a path record defines parent-child relationships by pairing a string label with a child UUID. Multiple path records at successive levels assemble the full tree:

```json
{ "path": "ab143723-...", "children": { "My_Project": "14adb22b-..." } }
{ "path": "14adb22b-...", "children": { "My_Site": "e0834921-..." } }
{ "path": "e0834921-...", "children": { "My_Building": "e84dc79e-..." } }
{ "path": "e84dc79e-...", "children": { "My_Storey": "44af358b-..." } }
{ "path": "44af358b-...", "children": { "Wall": "93791d5d-...", "My_Space": "e3035b71-..." } }
```

**Purpose 2 — Composition override targeting.** Following USD's LIVRPS composition model, the same path namespace is used to address sub-prims within a prototype for per-instance overrides. A path like `WindowType/Glazing` simultaneously identifies where the Glazing sub-prim sits in the scene graph and serves as the address at which composition opinions accumulate. An instance can target any sub-node of its inherited type at any depth using standard path syntax.

This unification is deliberate in USD: the prim path is the universal addressing mechanism for both spatial organisation and composition. IFCX inherits this design.

---

## 2. Problems with the IFCX Path Model

### 2.1 Identity conflated with position

In IFCX, the `path` field value IS the entity's UUID — identity and scene graph position are the same thing. This creates a closed-world assumption: an entity has exactly one canonical location in exactly one tree. Any alternative organisation of the same data (a structural model, a phase breakdown, a cost breakdown) must either adopt the same tree or fork to a parallel file with a different hierarchy, losing the shared UUID link.

IFC4X explicitly supports multiple simultaneous graphs over the same entity set through the `IfcRel*` family — structural groupings, maintenance zones, fire compartments, phase breakdowns. IFCX's conflation of identity with position makes these secondary graphs second-class concerns with no principled representation.

### 2.2 Single-tree constraint

Because every entity has one canonical path, IFCX implicitly enforces a single scene graph. The fragmented `children` map pattern means each path record defines only one level of the tree at a time. The hierarchy is implicit and scattered — a consumer must read many records and perform graph assembly before any spatial reasoning is possible.

### 2.3 Multi-party authorship

USD's composition model (LIVRPS precedence) resolves conflicting path opinions by having one layer win. This is correct for a VFX pipeline with a known composition order. It is inconsistent with multi-party AEC authorship, where a design-intent spatial assignment and an as-built surveyed position must coexist with independent provenance — neither silently overwriting the other.

### 2.4 Composition without separation

Because scene graph paths and composition paths share one namespace, tools that consume IFCX must implement the full USD composition engine before they can interpret any entity's complete description. There is no "flat" reading of an instance — its class, properties, geometry, and material are distributed across the instance record and its inherited prototype, addressable only through composition resolution.

---

## 3. Alternative Approaches for Scene Graph Organisation

The following approaches address the scene graph problem (Purpose 1 above). The composition override problem (Purpose 2) is addressed separately in Section 4.

### 3.1 Monolithic SpatialView component

A single typed component on the root entity carries the complete path→UUID map for an entire named hierarchy:

```json
{
  "type": "ifc:SpatialView",
  "entity": "14adb22b-...",
  "attributes": {
    "name": "spatial-default",
    "children": {
      "My_Project":                                    "14adb22b-...",
      "My_Project/My_Site":                            "e0834921-...",
      "My_Project/My_Site/My_Building":                "e84dc79e-...",
      "My_Project/My_Site/My_Building/My_Storey":      "44af358b-...",
      "My_Project/My_Site/My_Building/My_Storey/Wall": "93791d5d-..."
    }
  }
}
```

**Plusses:**
- Atomic: the view has one provenance timestamp; the hierarchy is internally consistent
- Full path strings are explicit and immediately readable without traversal
- Multiple simultaneous views are trivially distinct — separate components, separate names
- Sibling name uniqueness is enforced structurally by JSON key uniqueness
- Easy to diff between versions; conflicts are immediately visible
- The view is a named entity (UUID) that can carry metadata

**Minuses:**
- Does not scale: a 50,000-entity model produces one enormous component
- Federation is awkward: two parties contributing to the same view produce competing SpatialView components; merging requires application-level resolution logic
- Provenance is coarse: the entire hierarchy gets one asserter and timestamp; there is no way to express that party A contributed the site structure and party B added the fit-out level
- Partial updates are expensive: moving one entity requires regenerating the full component
- Quietly closed-world: entities absent from the map are implicitly not in the view, in tension with the OWA premise that absent = unknown

---

### 3.2 Distributed SpatialMembership components

Each entity carries a small typed component declaring its parent and label within a named view:

```json
{
  "type": "ifc:SpatialMembership",
  "entity": "93791d5d-...",
  "attributes": {
    "view":   { "ref": "view-entity-uuid" },
    "parent": { "ref": "44af358b-..." },
    "name":   "Wall"
  }
}
```

**Plusses:**
- OWA-compliant: each entity independently asserts its own position; adding an entity to a view requires one new component touching only that entity
- Fine-grained provenance: each membership has its own asserter, timestamp, and authority
- Scales naturally: spatial information is distributed; no single component grows with model size
- Federation-friendly: parties contribute membership components for their own entity subsets without touching each other's components
- Architecturally consistent: typed components on entities, same as everything else

**Minuses:**
- Graph traversal required: consumers must collect all membership components for a view and assemble the tree before any path-based work can happen — no immediate readability
- No atomic snapshot: the hierarchy is distributed across components with potentially different timestamps
- Sibling name uniqueness is a soft constraint: nothing in the data structure prevents two siblings from sharing the same `name`, making path strings non-unique
- Multi-party placement ambiguity: two SpatialMembership components on the same entity in the same view with different `parent` refs are structurally valid but semantically ambiguous — a conflict and an intentional multi-placement are indistinguishable
- Path strings must be reconstructed by walking parent refs upward; they are not stored anywhere
- Root identification requires reading a view descriptor; orphaned entities with missing parent refs look identical to legitimate roots

---

### 3.3 Hybrid: lightweight descriptor + distributed membership

A SpatialView descriptor names the view and anchors its root; distributed SpatialMembership components carry the parent-child relationships. This is a direct combination of the two approaches above.

```json
// View descriptor — one per named view
{
  "type": "ifc:SpatialView",
  "entity": "view-entity-uuid",
  "attributes": { "name": "spatial-default", "root": { "ref": "14adb22b-..." } }
}

// Membership — one per entity per view
{
  "type": "ifc:SpatialMembership",
  "entity": "93791d5d-...",
  "attributes": {
    "view": { "ref": "view-entity-uuid" },
    "parent": { "ref": "44af358b-..." },
    "name": "Wall"
  }
}
```

This gains view discoverability and a named root anchor (from the descriptor) while preserving OWA compliance and fine-grained provenance (from distributed membership).

**Additional downsides introduced by the hybrid:**
- The descriptor and membership components are loosely coupled: a membership can reference a non-existent view UUID; a descriptor can exist with no memberships pointing to it. Neither is an error in the data model, but both are confusing states.
- The path label problem, sibling uniqueness, and cycle detection remain unresolved — inherited from the distributed approach.
- The mechanism introduces a new component type (`ifc:SpatialMembership`) that is **partially redundant** with the spatial containment IfcRel components that already exist. This is the key observation that motivates Section 3.4.

---

### 3.4 IfcRels as the view graph

The spatial hierarchy already exists as typed relation components. In Hello Wall:

- `ifc:IfcRelAggregates` — Project→Site, Site→Building, Building→Storey (part-whole spatial decomposition)
- `ifc:IfcRelContainedInSpatialStructure` — elements (Wall, Space) within a spatial level

These two relation types, traversed from the project root, define the default spatial hierarchy completely. No `SpatialMembership` components are needed — the IfcRels are the membership.

The `ifc:SpatialView` descriptor declares which relation types constitute the view and anchors its root:

```json
{
  "type": "ifc:SpatialView",
  "entity": "view-entity-uuid",
  "attributes": {
    "name": "spatial-default",
    "root": { "ref": "14adb22b-..." },
    "composedFrom": [
      "ifc:IfcRelAggregates",
      "ifc:IfcRelContainedInSpatialStructure"
    ]
  }
}
```

For non-standard views (structural systems, cost breakdowns) that use different relation types, the descriptor references those types instead. For fully custom organisational views with no corresponding IfcRel type, the descriptor falls back to an explicit `children` map.

**Plusses:**
- **No redundancy**: the containment relation is the membership; the hierarchy is expressed once and owned by one component
- Provenance, OWA coexistence, and fine-grained authorship come automatically from the normal component model
- Architecturally consistent: relationships are IfcRels; the view is just a named selection of which relations constitute it
- Multiple simultaneous views are distinct SpatialView descriptors referencing different relation types or different root entities
- Partial updates are handled naturally: adding a wall to a storey is one new `IfcRelContainedInSpatialStructure` component, which automatically updates any view that includes that relation type

**Minuses:**
- `IfcRelAggregates` is a semantic assertion about part-whole decomposition; `IfcRelContainedInSpatialStructure` is a semantic assertion about spatial containment. These are not the same thing as "this entity is at this position in this navigational view." Using semantic relations as navigational structure conflates two concerns that may need to diverge — for example, a design-intent spatial assignment and an as-built spatial assignment, or a structural decomposition that differs from the architectural spatial organisation.
- Multiple views using the same relation type but different entity subsets are not directly distinguishable without additional tagging on the IfcRel components.
- Custom views that don't map to any existing IfcRel type have no coverage; new IfcRel types or a fallback explicit `children` map is required.

**The path label problem (common to all approaches):**

In the monolithic SpatialView, path segment labels (`"Wall"`, `"My_Storey"`) are stored explicitly in the `children` map. In all distributed approaches, labels must come from the entity's own `name` attribute on its identity component. Entity names are not always unique within a sibling set — IFC models regularly contain unnamed entities, duplicate names, and programmatically-generated names unsuitable as path segments.

The cleanest resolution: add an optional `pathLabel` attribute to `IfcRelAggregates` and `IfcRelContainedInSpatialStructure`. The label lives on the same component as the relationship, inherits its provenance, and never drifts from the containment assertion it describes. When absent, the entity's `name` attribute is used as fallback.

```json
{
  "type": "ifc:IfcRelContainedInSpatialStructure",
  "entity": "44af358b-...",
  "attributes": {
    "relatedElements": [{ "ref": "93791d5d-...", "pathLabel": "Wall" }]
  }
}
```

---

### 3.5 Graph edge directionality: child→parent vs parent→child

Approaches 3.2 and 3.3 above use child→parent directionality — each entity carries a component pointing *up* to its parent. The approaches in 3.1 and 3.4 express containment parent→child — the parent entity's component references its children. This is not an arbitrary choice; the direction has real OWA implications.

#### Why child→parent was used in 3.2 and 3.3

In a multi-party federated model, party B adding a new wall to party A's storey should require touching only party B's own components. With child→parent, the new wall carries its own membership component — party A's storey is unmodified:

```json
// Party B adds a wall — writes one component on their own entity only
{
  "type": "ifc:SpatialMembership",
  "entity": "wall-uuid",
  "attributes": {
    "view": { "ref": "view-uuid" },
    "parent": { "ref": "storey-uuid" },
    "name": "New_Wall"
  }
}
```

With parent→child (accumulated children list), party B would need to modify the storey's component to add the new child — a component that party A owns and may be simultaneously editing. This creates a coordination dependency and merge conflict surface.

#### Two variants of parent→child

**Variant 1 — accumulated children list per parent.** One component per parent lists all its direct children:

```json
{
  "type": "ifc:SpatialChildren",
  "entity": "44af358b-...",
  "attributes": {
    "view": { "ref": "view-uuid" },
    "children": {
      "Wall":     { "ref": "93791d5d-..." },
      "My_Space": { "ref": "e3035b71-..." }
    }
  }
}
```

This is effectively the monolithic SpatialView applied per level of the tree. Adding a new child requires regenerating the parent's component — the same OWA problem as the monolithic approach.

**Variant 2 — one component per parent-child pair.** Each relationship is its own component on the parent entity:

```json
{
  "type": "ifc:SpatialMembership",
  "entity": "44af358b-...",
  "attributes": {
    "view":      { "ref": "view-uuid" },
    "child":     { "ref": "93791d5d-..." },
    "pathLabel": "Wall"
  }
}
```

Adding a new wall creates a new component without modifying any existing one — the OWA property is restored. This is functionally equivalent to how `IfcRelContainedInSpatialStructure` works in approach 3.4, where the parent (storey) is the `entity` and the child elements are in `relatedElements`.

#### Tradeoffs

| Criterion | Child → Parent | Parent → Child (one-per-pair) |
|---|---|---|
| Adding an entity requires modifying existing components | No | No (new component per edge) |
| Top-down traversal (rendering a tree) | Scan all, filter by `parent` field | Scan all, filter by `entity` field |
| Bottom-up traversal | Direct (follow `parent` ref) | Scan all, filter by `child` field |
| Sibling name uniqueness | Soft constraint | Soft constraint |
| Sibling ordering | Requires explicit `order` attribute | Requires explicit `order` attribute |
| Path label sits with | The child entity | The parent entity |
| Authorship of position | Child asserts its own parent | Parent asserts its children |

Both one-per-pair variants are OWA-compliant — neither requires modifying existing components when adding entities. The practical difference is authorship semantics: child→parent makes position a fact about the child (the wall says where it belongs); parent→child one-per-pair makes it a fact about the parent (the storey says what it contains). In multi-party authorship, child→parent is marginally cleaner — the party responsible for an entity is the same party that asserts its spatial position.

#### The deeper observation

If parent→child one-per-pair is used, it is functionally identical to `IfcRelContainedInSpatialStructure` (parent as `entity`, child as `relatedElements[0]`). This independently re-derives the IfcRel pattern — which already exists, already carries provenance, and already has semantic meaning. This further strengthens the case for approach 3.4: the generic `SpatialMembership` component in either direction adds a new component type without adding capability beyond what the IfcRel model already provides.

The one remaining justification for a generic membership component is the **custom view case** — organisational hierarchies (cost breakdown, maintenance zones, phase groupings) that have no corresponding semantic IfcRel type. For those, a generic typed component in one-per-pair form is genuinely needed. The direction choice for those components should be parent→child, consistent with how IfcRels work.

---

## 4. The Dual Use of Paths in IFCX

### 4.1 Scene graph definition vs. composition override targeting

In USD — and by inheritance in IFCX — the prim path serves both purposes simultaneously. The path `WindowType/Glazing` identifies the Glazing sub-prim's location in the scene graph AND serves as the address at which composition opinions accumulate. An "over" statement targets a prim by its full scene path and adds an opinion at that address without declaring the prim anew:

```
# USD: override the Glazing sub-prim of WindowType on a per-instance basis
over "WindowInstance" {
    over "Glazing" {
        rel material:binding = </Materials/NewGlass>
    }
}
```

This unification is load-bearing in USD: it means the composition engine has a single namespace for both spatial organisation and prototype override resolution. A query can traverse both concerns in one expression.

In the IFC context: a window instance inheriting from a window type could target the `Glazing` sub-child of the window type to override its material. The path `windowInstance/Glazing` both locates the Glazing sub-prim in the scene graph (as a child of the instance) and identifies which slot of the prototype is being overridden.

### 4.2 How the proposed architecture separates these concerns

The proposed IFCY architecture implicitly separates the two path uses into distinct mechanisms:

- **Scene graph / spatial position** — expressed by `ifc:SpatialView` or IfcRels, operating at entity scope across the whole model (global namespace)
- **Composition override targeting** — expressed by `slotName` strings within `componentTemplates` of an `ifc:IfcTypical`, operating within a single typical's template scope (local namespace)

The `slotName` is already a path-like concept:

```json
"componentTemplates": [
  { "slotName": "geometry/Void",    "type": "usd:MeshGeometry", "inheritable": true, ... },
  { "slotName": "geometry/Frame",   "type": "usd:MeshGeometry", "inheritable": true, ... },
  { "slotName": "geometry/Glazing", "type": "usd:MeshGeometry", "inheritable": true, ... }
]
```

An instance override for a specific slot addresses it by `slotName`, not by scene graph path. These two namespaces do not conflict: scene graph paths address entities in a view (global scope), slot names address component templates within one typical (local scope).

### 4.3 The gap for deeply nested typicals

The flat `slotName` model is adequate for one level of typical nesting — as in Hello Wall, where a window type directly declares three geometry slots. It becomes insufficient for deeply nested assembly typicals. Consider a wall typical that contains a sub-typical for its material layer set, which itself contains a sub-typical for the load-bearing core. An instance override targeting the core material requires addressing a path through nested typicals: something like `"materialLayers/core/material"`.

The current `componentTemplates` structure as described does not specify how this works. Two paths forward:

**Option A — Path-like nesting in `slotName`.** Slot names implicitly encode hierarchical addresses using `/` separators, and the composition engine resolves them recursively through nested typicals. This is functionally equivalent to USD prim paths scoped to the typical's local namespace. The separation of concerns is preserved (slot paths are local; scene graph paths are global), but the slot mechanism becomes a scoped path system and must be normatively specified as such.

**Option B — Explicit override components with typed typical + slot targeting.** An instance carries an explicit override component referencing both the target typical and the slot within it:

```json
{
  "type": "ifc:SlotOverride",
  "entity": "wall-instance-uuid",
  "attributes": {
    "typical": { "ref": "wall-type-uuid" },
    "slot": "materialLayers/core/material",
    "override": { "ref": "new-material-uuid" }
  }
}
```

For deeply nested typicals, the slot path traverses through the nesting hierarchy. This keeps each override explicit, individually addressable, and independently provenanced — at the cost of verbosity for deep hierarchies.

Option A is more concise and closer to the USD model. Option B is more OWA-consistent (each override is a component with its own provenance) and better aligned with the rest of the architecture. Both require normalising `slotName` as a path system in RFC-IFC5-040.

### 4.4 Interaction between the two concerns

The key question is whether separating scene graph paths from composition override paths creates mutual interference. The answer is: **not structurally, but there is a specific loss of expressive power**.

In IFCX/USD, because the path namespace is unified, cross-cutting queries are natural: "find all prims under `Storey/Wall` where the `Glazing` sub-prim's material is X." This traverses scene graph position and composition structure in one expression, because both share one namespace.

When the namespaces are separated — scene graph paths in SpatialView/IfcRels, composition paths in slotNames — such queries require two separate resolution steps: first locate the entity by scene graph traversal, then resolve its composed component set by expanding the typical and applying overrides. For most practical IFC authoring queries this separation is not a problem. It becomes relevant for tools that need to reason about the full composed property set of entities at specific scene graph positions — a pattern common in USD-native tooling but less common in IFC authoring environments today.

The separation is a **deliberate architectural trade-off**: it buys cleaner multi-view support, OWA compliance, and IFC4X relation compatibility for the scene graph at the cost of the unified query capability that USD's single-namespace design provides. For the AEC domain, where multi-party federation and IFC4X round-trip are primary requirements, this trade is correct.

---

## 5. Summary Comparison

| Criterion | Monolithic SpatialView | Distributed SpatialMembership | Hybrid (descriptor + membership) | IfcRels as view graph |
|---|---|---|---|---|
| Path strings stored | Yes | No (reconstructed) | No (reconstructed) | No (reconstructed) |
| Scales to large models | No | Yes | Yes | Yes |
| Federation / multi-party | Awkward (whole-view conflict) | Clean (per-entity) | Clean (per-entity) | Clean (per-entity) |
| Granular provenance | No (one block per view) | Yes (per entity) | Yes (per entity) | Yes (per IfcRel) |
| OWA compliance | Partial (closed-world absence) | Full | Full | Full |
| Sibling name uniqueness | Structural (JSON key) | Soft constraint | Soft constraint | Soft constraint |
| Partial updates | Expensive (full regeneration) | Cheap (one component) | Cheap (one component) | Cheap (one IfcRel) |
| Redundancy with IfcRels | Partial | Full (for spatial views) | Full (for spatial views) | None |
| Semantic conflation risk | Low | Low | Low | Moderate (containment ≠ navigation) |
| Custom / non-IFC views | Yes | Yes | Yes | Requires fallback |
| View discoverability | Yes | Scan required | Yes (descriptor) | Yes (descriptor) |
| Root identification | Implicit (component entity) | Scan or descriptor | Descriptor | Descriptor |
| Cycle detection | Structural (impossible) | Requires full graph | Requires full graph | Requires full graph |
| Edge directionality | Parent→child (map) | Child→parent | Child→parent | Parent→child (per edge) |
| Requires modifying existing components to add entity | Yes (regenerate view) | No | No | No |

---

## 6. Conclusion and Recommendation

### On the scene graph problem

**The IfcRels-as-view-graph approach is the most architecturally consistent choice for the default spatial view.** The default spatial hierarchy IS the union of `IfcRelAggregates` and `IfcRelContainedInSpatialStructure` relations, rooted at the project entity. These components already exist, already carry provenance, and already support OWA coexistence and multi-party authorship. Expressing the same containment information again as `SpatialMembership` components is redundant by design.

The `ifc:SpatialView` descriptor should be retained as a lightweight, named handle that:

1. Names the view (human-readable, with a UUID for reference)
2. Declares its root entity
3. Declares which relation types constitute it (`composedFrom`)
4. Carries its own provenance (who defined this view, for what purpose)

For non-standard views that don't map to existing IfcRel types, the descriptor should support a fallback explicit `children` map. This covers cost breakdowns, maintenance zones, and other custom hierarchies without requiring new IfcRel types for every possible organisational scheme.

**The path label problem should be resolved** by adding an optional `pathLabel` attribute to related-object entries in `IfcRelAggregates` and `IfcRelContainedInSpatialStructure`. The label sits on the same component as the relationship, inherits its provenance, and cannot drift from the containment assertion it annotates. When absent, the related entity's `name` attribute serves as fallback. This is a small, targeted addition that resolves the one genuine gap in the IfcRels-as-view-graph approach without introducing a new component type.

**The semantic conflation concern** — that `IfcRelAggregates` expresses part-whole decomposition while a view expresses navigation — is real but manageable. For the default spatial view, containment and navigation are the same thing; the conflation is harmless. For cases where they must differ (e.g., a structural breakdown that disagrees with the architectural spatial organisation), different IfcRel components with different view participation are the correct expression. Two `IfcRelAggregates` components on the same entity pair, with different `participatesIn` values, express the same semantic containment for different navigational purposes — each independently provenanced.

### On the composition override problem

**Separating scene graph paths from composition override paths is the right decision** for the proposed architecture. The concerns are genuinely different in scope: scene graph paths address entities globally across a model; slot names address component templates locally within a single typical. Unifying them (as IFCX/USD does) ties IFC5's multi-view and multi-party capabilities to USD's closed-world, single-tree composition model — the wrong trade for the AEC domain.

**The `slotName` mechanism must be normatively specified as a scoped path system** in RFC-IFC5-040, including:

- The `/` separator convention for hierarchical slot addressing
- How the composition engine traverses slot paths through nested typicals
- How per-instance overrides targeting a slot are expressed and resolved

Without this specification, implementations will diverge on multi-level override targeting, and the mechanism will be inadequate for production assembly typicals beyond Hello Wall depth.

### Recommendations in brief

| Decision | Recommendation |
|---|---|
| Default spatial view | Implicit in `IfcRelAggregates` + `IfcRelContainedInSpatialStructure`; named by a lightweight `ifc:SpatialView` descriptor (`name`, `root`, `composedFrom`) |
| Path segment labels | Optional `pathLabel` on related-object entries in containment IfcRels; entity `name` as fallback |
| Non-standard / custom views | `ifc:SpatialView` descriptor with explicit `children` map fallback; new IfcRel types for common non-spatial hierarchies |
| Multiple simultaneous views | Multiple `ifc:SpatialView` descriptors, each declaring different root and `composedFrom` relation types |
| Scene graph vs. composition namespaces | Keep separated: scene graph addressing via IfcRels + SpatialView descriptor; composition addressing via `slotName` within `ifc:IfcTypical` |
| `slotName` for nested typicals | Specify `slotName` normatively as a scoped local path system supporting `/`-separated nesting; address in RFC-IFC5-040 |
| `ifc:SpatialMembership` component | **Do not introduce** for spatial/aggregation views — the IfcRel components already fulfil this role. For custom views without a matching IfcRel type, use a generic membership component in **parent→child one-per-pair** form, consistent with IfcRel directionality |
| Edge directionality for custom view components | Parent→child one-per-pair (one component per edge, parent as `entity`) — consistent with IfcRel pattern; OWA-compliant; no modification of existing components required when adding entities |

---

*This discussion paper covers material relevant to RFC-IFC5-004 (Path Model), RFC-IFC5-016 (Spatial Structure), RFC-IFC5-040 (Archetypes, Templates, and Overrides), and RFC-IFC5-041 (Open World vs. Closed World).*
