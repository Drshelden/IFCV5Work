# Toward a Component-Based, Open-World Architecture for IFC5

**Proposed Extensions to the IFCX Initiative**

*IFC5 Working Group — Architecture White Paper*
*July 2026 — Draft for Committee Discussion*

---

## Abstract

This white paper examines the IFCX proposal in light of three core ambitions:
- open-world assumption (OWA) compliance, 
- lossless compatibility with IFC4X's business logic, and 
- AI readiness. 

A set of targeted extensions to IFCX are proposed addressing these ambitions that preserve IFCX' core advances, specifically around composition and extensibility of typed object definitions. These proposals also expand on several IFC4X migration topics that have not yet been explicitly specified by the IFCX initiative, including comprehensive relationship handling, component taxonomy and subtype polymorphism, units modernisation, and multi-party authorship.

The proposed architecture is organised in four layers: 

- foundational JSON data primitives (Layer 1), 
- a component primitive and package envelope with provenance (Layer 1.5), 
- a high fidelity port of IFC4X business logic expressed as typed components (Layer 2), 
- spatial views, typicals, and overlays for composition (Layer 3) that support the key ambitions of the IFCX composition advances. 

A companion Hello Wall example (`hello-wall-ifcy.json`) has been created for direct comparison against the IFCX `hello-wall.ifcx`, together with a typescript scheme definition of this suite of proposals, and a typescript schema `ifc5-layered-schema.ts` has been created.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [IFCX — Key Advances and Limitations](#2-ifcx--key-advances-and-limitations)
3. [The Proposed Layered Architecture](#3-the-proposed-layered-architecture)
4. [Extended Considerations](#4-extended-considerations)
   - [4.1 Package Model](#41-package-model)
   - [4.2 Open-World Attribute Semantics](#42-open-world-attribute-semantics)
   - [4.3 Component Taxonomy and Subtype Polymorphism](#43-component-taxonomy-and-subtype-polymorphism)
   - [4.4 Units and Data Types](#44-units-and-data-types)
   - [4.5 AI Readiness](#45-ai-readiness)
   - [4.6 Backward Compatibility with IFC4X](#46-backward-compatibility-with-ifc4x)
   - [4.7 Recommendations](#47-recommendations)
   - [4.8 Hello Wall — Architecture Comparison](#48-hello-wall--architecture-comparison)
5. [Conclusion](#5-conclusion)

---

## 1. Introduction

IFCX represents a significant advance in building data architecture. It adopts UUID-based addressing, namespaced typed attributes, and USD-inspired composition — each a well-motivated improvement on IFC4X's STEP Physical File format. This paper takes IFCX as its baseline and proposes extensions intended to complete its open-world ambitions and address IFC4X migration topics that remain unspecified.

**Intentions of this paper:**

- Support the IFCX architecture and its core capabilities while evolving it to address:
  - **Open-world requirements** — entity identity decoupled from position; provenance on every assertion; additive multi-party authorship without forced resolution
  - **IFC4X lossless compatibility** — including `IfcRel*` relationship families, property sets, class taxonomy, unit types expressible without information loss, and transmission packaging
  - **AI readiness** — flat, schema-free-parseable data structures; on-demand materialisation expanding typicals to full component sets for AI consumption; provenance distinguishing AI-generated from engineer-stamped values
  - **Explicit spatial views** — organisational hierarchies as named view components, not as entity identity, enabling multiple simultaneous organisations of the same dataset
  - **Simplified building industry syntax** — this proposal recourses to terminology aligned with AECO and V4 concepts priotizied over USD / VFX terminology, in order to streamline human legibility by AEC professionals and to simplify V4-V5 migration.  
- Use `hello-wall.ifcx` as the reference starting point. A companion file, `hello-wall-ifc5.json`, adopts all conventions proposed here and is available for direct comparison.

**Related initiatives.** A parallel IFC-ECS initiative developed a pure Entity–Component–System approach to IFC5, in which every semantic fact is a typed component attached to an entity GUID, with no spatial hierarchy. IFC-ECS did not attempt to address the composition, typical, and override requirements that IFCX correctly identifies as essential; those capabilities were assumed possible as extensions. This paper's Layer 2 relation-handling draws on the component patterns demonstrated in the IFC-ECS Hello Wall example. Indeed the proposed architecture attempts to have "the best of all worlds", combining a foundational component system, a comprehensive V4 business logic evolution, and the composition capabilities of IFCX.

**RFC system.** A set of companion Requests for Comment (RFCs) have been developed to rigorously examine each architectural assumption in IFCX and the broader IFC5 ambition. This paper links to those RFC documents (with links to RFC-IFC5-#### ) for further technical detail; the RFCs would ideally become the basis for a normative reference for recording motivations, options and decisions taken in the development of IFC5.

---

## 2. IFCX — Key Advances and Limitations

### 2.1 Key Advances of IFCX

A very brief summary of the key features of IFCX include:

**UUID as the ground-level identity primitive.** IFCX addresses every entity by UUID in the `path` field and uses UUIDs as values in the `children` map. This is a decisive improvement on IFC4X's STEP instance numbers, which are file-local and unstable under merge. UUIDs are globally unique, cheap to generate, and stable across hierarchy restructuring and federation. The proposed architecture extends this to component identity as well. ([RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md))

**Flat data array with repeated path records.** IFCX organises data as a flat JSON array. Multiple records can reference the same entity UUID, each contributing a different slice of data. In Hello Wall, the wall UUID appears in seven separate records — class, properties, material, geometry, classification, placement, and hierarchy. This decouples entity identity from fact accumulation, and is the structural foundation for open-world authorship. ([RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md))

**Namespaced typed attributes.** Every IFCX attribute is namespace-qualified (`bsi::ifc::class`, `bsi::ifc::prop::IsExternal`, `usd::xformop`, `nlsfb::class`). Any tool can parse an IFCX file into a consistent structure without schema knowledge. This schema-free parseability is the baseline requirement for AI readability. ([RFC-IFC5-036](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md), [RFC-IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md))

**The `inherits` arc for prototype instantiation.** IFCX's `inherits` keyword provides a prototype/instance mechanism: an entity inherits sub-structure and attribute values from a template, carrying only what differs. In Hello Wall, two window instances each inherit from the window type, carrying only their placements. This mirrors USD's geometry instancing pattern and is the right compositional mechanism for large-scale models. The proposed architecture retains and formalises this as the "typical" concept. ([RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md))

**The `children` map for spatial organisation.** The `children` map expresses the IFC spatial hierarchy (Project → Site → Building → Storey) in a human-navigable form aligned with USD's prim hierarchy. The proposed architecture retains this pattern, reformulated as a named view component rather than an identity-defining structure.

### 2.2 Limitations

**2.2.1 Path conflating identity with position.** In IFCX, an entity's UUID is simultaneously its identity and its address in the scene tree. Paths are navigational aliases, not identity. The same UUID may appear in multiple simultaneous hierarchies — a window can be addressed both by its UUID and by paths in a spatial tree, a systems tree, or a discipline overlay simultaneously. The UUID is stable regardless of tree membership; the path is an address that depends on the view. Note that the current Hello Wall example demonstrates only a single spatial hierarchy; a multi-tree example is planned as a test case (see RFC-004). The spatial view concept proposed here separates these concerns: UUID = identity; path = navigational view. ([RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md), [RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md))

The inherited USD composition model (LIVRPS precedence) resolves disagreements by having one opinion win. This is appropriate for a VFX pipeline but inconsistent with multi-party authorship in AEC, where for example a design-intent value and an as-built surveyed value must coexist, each attributed to its source.

A key assumption of this paper is that multiple graphs, paths, and organizations of entities must co-exist outside of the containment / parent-child hierarchy, and that the core relation model developed in IFC4X that allows these multiple graphs to co-exist must be preserved. While there may be workarounds to IFCX that support secondary graphs beside the scene graph, the current IFCX development doesn't explicitly address how these alternative graph structures co-exist with the canonical scene graph decomposition.

**2.2.2 Incomplete relation coverage.** IFCX handles containment via `children` and type assignment via `inherits`. Hello Wall introduces `bsi::ifc::spaceBoundary` as an inline attribute. IFC4X has more than thirty `IfcRel*` families — voids, fills, path connections, interference, load groups, material associations, classification associations, and others — few of which map naturally to a scene hierarchy position or a flat attribute. Without a principled mechanism for relation coverage, lossless round-trip from IFC4X is not achievable. ([RFC-IFC5-008](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md))

**2.2.3 Composition without resolution.** In IFCX, a window instance record carries only its placement. Its class, geometry, material, and properties are in the window type entity, reachable only by resolving the `inherits` arc. A consumer that reads only the instance record sees an incomplete entity. Any tool — including AI reasoning systems — must implement the USD composition engine before it can answer "what is this object?" This is a practical barrier to machine consumption of IFCX data.

> Note: the composition resolution requirement is not entirely new. IFC4 required similar logic for TypeObject → PropertySet → occurrence inheritance, expressed through domain schema prose rather than a formal composition model. IFCX replaces an implicit, idiosyncratic resolution mechanism with an explicit, first-principled one. The burden on consumers is comparable; the gain is that the behaviour is formally specified and testable.

([RFC-IFC5-036](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md))

---

## 3. The Proposed Layered Architecture

The proposed architecture is a set of extensions to IFCX, not a competing proposal. The extensions are organised in four conceptual layers. A single JSON file may contain constructs from all four layers simultaneously; the layering is a design tool, not a file format distinction.

**Architecture overview:**

- **Layer 1 — JSON data primitives.** The normative data model is JSON (null, boolean, number, string, array, object). UUID as canonical identity; URI as resolvable web address; path as navigational alias only.
- **Layer 1.5 — Component primitive + package envelope.** Every semantic assertion is a typed component `{id, type, entity, attributes, provenance}`. Components accumulate around entities; no central entity registry. The package envelope `{ifcPackage, id, provenance, schemas, data[]}` bundles components for transmission with an inherited provenance context.
- **Layer 2 — IFC4X business logic as typed components.** IFC4X class instances → identity components; property sets → property-set components; all `IfcRel*` families → relation components. bSDD URIs for taxonomy. UCUM for units.
- **Layer 3 — Views, typicals, and overlays.** Spatial and organisational hierarchies as named view components (not identity). Window types and similar reusable definitions as explicit Typical entities with `componentTemplates`. Instances reference the typical and carry only overrides. On-demand materialisation expands typicals and overlays into full component sets for consumers that need fully resolved entity descriptions.

### 3.1 Layer 1: Foundational Data Primitives

#### 3.1.1 JSON/Python-Compatible Data Model

The normative data model is JSON: null, boolean, integer, float, string, array, object. All IFC5 data is composed from these types. Alternative encodings (CBOR, MessagePack, Protocol Buffers) are permitted as profiles but must round-trip losslessly to JSON. ([RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md), [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md))

#### 3.1.2 UUID as Canonical Identity

Every named object — entity, component, package, type definition — has a UUID (v4 or v5) as its canonical identity, assigned at creation and never changed. IFC4X GlobalIds are decompressed to standard UUID format on import without information loss.

Three identity levels:

- **UUID** — canonical, stable, globally unique. ([RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md))
- **URI** — resolvable web address mapping a UUID or semantic name to a description (bSDD, schema repository). Optional but recommended for types and classifications. ([RFC-IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md))
- **Path** — navigational address locating an entity in a named view. Not the entity's identity. A path change does not change the UUID. ([RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md))

**Usage guidance.** UUIDs are used wherever an entity, component, or package must be identified or referenced: in the `entity` field of every component, in the `id` field of every component and package, and as the value in `{"ref": "uuid"}` links. A UUID is assigned once at creation and is the only identifier that persists across hierarchy restructuring, federation, and file round-trips. All `IfcRel*` relation targets, all `IfcInstantiates` typical references, and all cross-file federation links use UUIDs.

URIs serve a different role: they point to externally-defined types, classifications, and standards — not to instance entities. The `taxonomy` field of an identity component carries a bSDD URI for the entity's IFC class; `classifications[].uri` points to a classification system entry; and the package `schemas` map carries namespace URIs. When referencing an external resource by its web address, `{"ref": "uri", "fetchedAt": "iso8601"}` is used. URIs do not identify instance entities and must not appear in `entity` fields or `{"ref": ...}` links that target project data.

Paths appear only as keys in a `SpatialView`'s `children` map — human-readable aliases such as `"My_Project/My_Site/My_Building/My_Storey/Wall"`. A path is never used in an `entity` field, a `{"ref": ...}` link, or any cross-file reference.

**Where UUID and URI may overlap.** In one context both can express a type reference: when a window type is defined internally, instances reference it by UUID in `IfcInstantiates`; when the type is externally defined (a bSDD library type with no local UUID), the `taxonomy` URI alone is sufficient as the type pointer. In no other context are the three levels interchangeable.

#### 3.1.3 Typed Attribute and Reference Conventions

All attributes are named and typed; no positional attributes appear anywhere in IFC5. The normative typed-value form is `{"type": "IfcLabel", "value": "Wall-001"}`; bare JSON scalars are permitted where the type is schema-implied. Object references use `{"ref": "uuid"}` for local references and `{"ref": "uri", "fetchedAt": "iso8601"}` for external resources. ([RFC-IFC5-023](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md), [RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md))

---

### 3.2 Layer 1.5: The Component Primitive

A component is the fundamental semantic unit: a typed assertion about one entity.

In IFCX, semantic assertions are expressed as path records in the flat `data` array. A path record carries the entity UUID in the `path` field and adds attributes below it. There is no component-level identity, no `entity` field separate from `path`, and no provenance mechanism:

**IFCX** (`hello-wall.ifcx`):
```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "bsi::ifc::class": {
      "code": "IfcWall",
      "uri": "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWall"
    }
  }
}
```

The proposed architecture introduces a typed component that has its own UUID (`id`), explicitly names its subject entity (`entity`), and carries provenance. The same assertion becomes:

**IFCY** (`hello-wall-ifcy.json`):
```json
{
  "id": "component-uuid",
  "type": "ifc:IfcWallIdentity",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": { "name": "Wall", "predefinedType": "NOTDEFINED" },
  "provenance": {
    "assertedBy": "urn:org:design-team",
    "assertedAt": "2026-07-31T00:00:00Z",
    "authority": "design-intent"
  }
}
```

Key rules:
- The `id` field is the component's own UUID — distinct from the entity UUID it describes. This enables components to be referenced, versioned, or superseded independently.
- An entity exists by virtue of being referenced in at least one component. No entity-declaration step is required.
- Multiple components of the same type from different parties coexist on the same entity. The provenance block — `assertedBy`, `assertedAt`, `authority` — enables consumers to apply their own resolution policy. Authority values include `design-intent`, `as-built`, `survey`, `inferred`, `ai-generated`, `regulatory`, and `materialized-from`.

> **Note — pending committee decision:** The `authority` field ordering constitutes an implicit precedence rule (survey > as-built > design-intent > inferred). This is in tension with the principle that the architecture surfaces conflicts rather than resolving them. The committee must decide between three options: (a) retain the ordering as a normative default for plain queries, requiring consumers to declare when they want a different policy; (b) remove the precedence order and leave query behaviour as implementation-defined with mandatory disclosure; (c) keep provenance metadata but designate conflict resolution as out of scope for this version. Until this is resolved, implementations should treat the authority ordering as advisory only. See RFC-039 and RFC-041.

([RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md), [RFC-IFC5-031](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md), [RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md))

---

### 3.3 Layer 2: IFC4X Business Logic as Typed Components

Layer 2 defines how IFC4X's entities, property sets, and relationships map to typed components. No IFC4X semantic information is lost; the coverage is lossless. ([RFC-IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md))

#### 3.3.1 Entity Identity Components

Each IFC4X class instance becomes a typed identity component. In IFCX, class membership is a flat attribute on the path record; classification appears in a separate record:

**IFCX** (`hello-wall.ifcx`):
```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "bsi::ifc::class": {
      "code": "IfcWall",
      "uri": "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWall"
    }
  }
}
// classification in a separate path record:
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "nlsfb::class": {
      "code": "21.21",
      "uri": "https://identifier.buildingsmart.org/uri/nlsfb/nlsfb2005/2.2/class/21.21"
    }
  }
}
```

In the proposed architecture, class and classifications are consolidated into a single typed identity component, with the bSDD URI carried in `taxonomy` for subtype-chain resolution:

**IFCY** (`hello-wall-ifcy.json`):
```json
{
  "id": "c0000000-0000-0000-0000-000000000006",
  "type": "ifc:IfcWallIdentity",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "name": "Wall",
    "predefinedType": "NOTDEFINED",
    "taxonomy": { "ref": "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWall" },
    "classifications": [
      { "code": "21.21", "uri": "https://identifier.buildingsmart.org/uri/nlsfb/nlsfb2005/2.2/class/21.21", "system": "NL-SfB" }
    ]
  }
}
```

An entity's class membership is determined by which identity component it carries, not by a declaration. ([RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md))

#### 3.3.2 Property Sets as Components

Each IFC4X `IfcPropertySet` becomes a property-set component on the entity it describes. In IFCX, properties are flat namespaced attributes scattered across path records, with no grouping by property set name and no unit encoding:

**IFCX** (`hello-wall.ifcx`):
```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": { "bsi::ifc::prop::IsExternal": true }
}
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "bsi::ifc::prop::Volume": 2.783999976,
    "bsi::ifc::prop::Height": 3.0
  }
}
```

In the proposed architecture, properties are grouped by pset name, carry UCUM-coded units, and support the three-state value convention:

**IFCY** (`hello-wall-ifcy.json`):
```json
{
  "type": "ifc:IfcPropertySet",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "psetName": "Pset_WallCommon",
    "properties": {
      "IsExternal": true,
      "Volume": { "value": 2.784, "unit": "m3" },
      "Height": { "value": 3.0, "unit": "m" },
      "FireRating": null
    }
  }
}
```

`null` values are meaningful under the open-world convention: `FireRating: null` means the fire rating is explicitly unknown. Absent keys mean the property is out of scope for this component. ([RFC-IFC5-013](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md))

#### 3.3.3 Relationships as Components

Every IFC4X `IfcRel*` family becomes a typed relation component. IFCX handles only two relationship types explicitly: containment via `children`, and type assignment via `inherits`. Other relationships are expressed as inline attributes without a principled general model.

> **On the absence of IfcRel\* in IFCX:** IfcRel\* objectified relationships are deliberately absent from IFCX. In IFC4X Express, they provided modularity — through inverse attributes and abstract supertypes — within a monolithic global schema. In an ECS model, typed components with explicit identity and provenance already provide this modularity, making objectified relationships redundant. Complex many-to-many relationships such as system membership and material associations are representable through typed relation components (see the Domestic Hot Water example in the buildingSMART reference repo). Note: this design decision remains contested; see RFC-008 for the open comparison. For example, space boundary in IFCX is an attribute embedded on the boundary geometry node:

**IFCX** (`hello-wall.ifcx`):
```json
{
  "path": "c8ecbf4c-e37a-4489-9133-15163b8a904e",
  "attributes": {
    "bsi::ifc::spaceBoundary": {
      "relatedelement": { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
      "relatingspace":  { "ref": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6" }
    }
  }
}
```

And material is expressed as an `inherits` arc rather than an explicit relation:

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "inherits": { "material": "7a187a90-3dcf-58cc-b3a6-51a9a407c55a" }
}
```

In the proposed architecture, all thirty-plus IFC4X `IfcRel*` families are typed relation components with three cardinality patterns. The same relationships become:

**IFCY** (`hello-wall-ifcy.json`):

Three cardinality patterns cover all cases:

**1:many** — component on the relating entity; related objects as a ref array:

```json
{
  "type": "ifc:IfcRelVoidsElement",
  "entity": "93791d5d-...",
  "attributes": {
    "relatedOpeningElements": [
      { "ref": "409918e0-..." },
      { "ref": "9a7ae044-..." }
    ]
  }
}
```

**1:1** — component on the dependent entity, referencing its host:

```json
{
  "type": "ifc:IfcRelFillsElement",
  "entity": "2c2d549f-...",
  "attributes": { "relatingOpeningElement": { "ref": "409918e0-..." } }
}
```

**M:N** — standalone relation entity with its own UUID, carrying refs to both sides.

Space boundary and material association in IFCY are explicit typed components:

```json
{
  "type": "ifc:IfcRelSpaceBoundary",
  "entity": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6",
  "attributes": {
    "physicalOrVirtualBoundary": "PHYSICAL",
    "internalOrExternalBoundary": "INTERNAL",
    "relatedBuildingElement": { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
    "connectionGeometryBody": { "ref": "911155b7-f688-51ee-8e3e-b97475be2452" }
  }
}
{
  "type": "ifc:IfcRelAssociatesMaterial",
  "entity": "7a187a90-3dcf-58cc-b3a6-51a9a407c55a",
  "attributes": {
    "materialRole": "wall-body",
    "relatedObjects": [{ "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" }]
  }
}
```

This pattern covers all thirty-plus IFC4X relationship families without loss of identity or inverse-traversal capability. ([RFC-IFC5-008](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md), [RFC-IFC5-025](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-025-collections-cardinality.md))

---

### 3.4 Layer 3: Views, Typicals, and Overlays

#### 3.4.1 Paths as Named Views, Not Identity

A spatial or organisational hierarchy is a **named view component** — not an intrinsic property of entities. Multiple views can coexist for the same dataset (spatial structure, structural systems, construction phase, cost breakdown) without any entity changing its UUID or requiring data reorganisation.

Several approaches for expressing named views have been considered — monolithic view components, distributed membership components, and using existing IfcRel components as the view graph — each with different tradeoffs for OWA compliance, federation, scalability, and authorship. These alternatives and their tradeoffs are discussed in full in [`IFC5-Path-Model-Architecture-Discussion.md`](IFC5-Path-Model-Architecture-Discussion.md) and the associated [RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md).

**Recommended approach for the default spatial view:** The default spatial hierarchy is already fully expressed by `ifc:IfcRelAggregates` (Project→Site→Building→Storey) and `ifc:IfcRelContainedInSpatialStructure` (elements within spatial levels). These components exist, carry provenance, and support multi-party authorship. The `ifc:SpatialView` component serves as a lightweight named descriptor — it does not duplicate the hierarchy but declares which relation types constitute it and which entity is the root. For non-standard views (structural systems, cost breakdown) that have no matching IfcRel type, the descriptor carries an explicit `children` map as fallback.

In IFCX, the spatial hierarchy is expressed by fragmenting the tree across multiple path records — each level of containment is a separate record with a `children` map entry pointing one step down:

**IFCX** (`hello-wall.ifcx`):
```json
{ "path": "ab143723-...", "children": { "My_Project": "14adb22b-..." } }
{ "path": "14adb22b-...", "children": { "My_Site":    "e0834921-..." } }
{ "path": "e0834921-...", "children": { "My_Building": "e84dc79e-..." } }
{ "path": "e84dc79e-...", "children": { "My_Storey":  "44af358b-..." } }
{ "path": "44af358b-...", "children": { "Wall": "93791d5d-...", "My_Space": "e3035b71-..." } }
```

This fragmented structure couples identity to position — each entity has exactly one canonical location in one tree. In the proposed architecture, the default spatial view is derived from the IfcRel graph, with a lightweight descriptor naming the view:

**IFCY** (`hello-wall-ifcy.json`) — SpatialView descriptor declares what constitutes the view; the IfcRel components carry the actual hierarchy:
```json
{
  "type": "ifc:SpatialView",
  "entity": "14adb22b-...",
  "attributes": {
    "name": "spatial-default",
    "description": "Default spatial containment hierarchy. Paths are navigational views; entity identity is always the UUID.",
    "root": { "ref": "14adb22b-...", "pathLabel": "My_Project" },
    "composedFrom": [
      "ifc:IfcRelAggregates",
      "ifc:IfcRelContainedInSpatialStructure"
    ]
  }
}
```

Path segment labels are carried on the `relatedObjects`/`relatedElements` entries of the IfcRel components via an optional `pathLabel` field, co-located with the containment assertion and its provenance.

([RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md), [RFC-IFC5-016](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md))

> **Known limitation — transform composition:** The current Hello Wall example works correctly only because the wall has an identity transform (no rotation, no offset). When position is decoupled from identity and an entity appears in a spatial view that differs from where its local transform was originally authored, the authoritative coordinate frame for composing transforms is undefined. Any spatial-view proposal must specify which graph is used for transform composition, and must demonstrate correctness with a non-identity wall transform. This is an open design question tracked in RFC-004 §9.

#### 3.4.2 The Typical — Replacing IfcTypeObject and `inherits`

A **typical** is a named template defining a default component set for instances. It replaces both IFC4X's `IfcTypeObject` and IFCX's `inherits` keyword with a single explicit mechanism.

In IFCX, type assignment is an `inherits` arc — an implicit prototype link that requires USD composition resolution to interpret. The instance carries no explicit description of what it inherits:

**IFCX** (`hello-wall.ifcx`):
```json
{ "path": "2c2d549f-f9fe-4e22-8590-562fda81a690",
  "inherits": { "windowType": "25503984-6605-43a1-8597-eae657ff5bea" } }
{ "path": "2c2d549f-f9fe-4e22-8590-562fda81a690",
  "attributes": { "usd::xformop": { "transform": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[1.768,0,1,1]] } } }
```

In the proposed architecture, the type definition (`IfcTypical`) explicitly names its `componentTemplates` — the slots an instance inherits — and instance composition is expressed by `IfcInstantiates`:

**IFCY** (`hello-wall-ifcy.json`):

```json
{
  "type": "ifc:IfcTypical",
  "entity": "25503984-...",
  "attributes": {
    "name": "WT01",
    "componentTemplates": [
      { "slotName": "class",
        "type": "ifc:IfcWindowIdentity",
        "inheritable": true,
        "attributes": { "predefinedType": "NOTDEFINED" } },
      { "slotName": "properties",
        "type": "ifc:IfcPropertySet",
        "inheritable": true,
        "attributes": { "psetName": "Pset_WindowTypeCommon",
                        "properties": { "Height": { "value": 1.2, "unit": "m" } } } },
      { "slotName": "geometry/Frame",
        "type": "usd:MeshGeometry",
        "inheritable": true,
        "attributes": { "geometryEntity": { "ref": "08f06095-..." } } }
    ]
  }
}
```

An instance references the typical via `ifc:IfcInstantiates` and carries only its overrides:

```json
{ "type": "ifc:IfcInstantiates",
  "entity": "2c2d549f-...",
  "attributes": { "typical": { "ref": "25503984-..." } } }

{ "type": "usd:XformComponent",
  "entity": "2c2d549f-...",
  "attributes": { "transform": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[1.768,0,1,1]] } }
```

([RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md), [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md))

#### 3.4.3 Materialisation — On-Demand Expansion of Typicals and Overlays

**Materialisation is primarily an operation, not a stored artefact.** When a consumer needs the full, resolved description of an entity, the composition engine expands the `IfcTypical` template plus any instance override components into a flat, complete component set. This is what materialisation means: the typical's `componentTemplates` are instantiated for the specific entity, merged with its explicit override components, and presented as a fully resolved picture — with no `IfcInstantiates` arc required to trace.

For example, materialising a window instance means resolving its `IfcTypical` (class, geometry, properties) against its override (`usd:XformComponent`), yielding a flat set of components as if they had been authored directly on the instance.

**Should materialised data be carried in the file?** We recommend against it as a general practice. The authoritative representation is always the typical + instance overrides; a carried materialised copy creates a second source of truth that can drift from the authoritative data when the typical is updated. Consumers that need resolved data should resolve on demand.

That said, there are deployment scenarios where a pre-resolved, carried form is a reasonable optimisation: AI pipeline pre-processing (indexing pre-resolved entities into a vector database), or read-only API responses served to lightweight clients that cannot implement the composition engine. In these specific contexts, an optional `ifc:MaterialisedSnapshot` component may be carried, explicitly marked as derived:

```json
{
  "type": "ifc:MaterialisedSnapshot",
  "entity": "2c2d549f-...",
  "attributes": {
    "resolvedFrom": "WT01",
    "snapshot": {
      "taxonomy": { "ref": "...IfcWindow" },
      "IsExternal": true,
      "Height": { "value": 1.2, "unit": "m" },
      "placement": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[1.768,0,1,1]]
    }
  },
  "provenance": {
    "assertedBy": "https://standards.buildingsmart.org/ifc/v5/resolver",
    "assertedAt": "2026-07-31T00:00:00Z",
    "authority": "materialized-from",
    "derivedFrom": ["25503984-...", "2c2d549f-..."]
  }
}
```

When a carried snapshot is present, the `authority: "materialized-from"` provenance field is the signal that it is a derived, read-only cache — never authoritative. Any tool that both reads and writes IFC data must treat the composition layer as the ground truth and regenerate or drop the snapshot on write. ([RFC-IFC5-036](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md), [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md))

#### 3.4.4 Multi-Party Authorship

Multiple parties contribute components to the same entity without overwriting each other. When two components carry conflicting values for the same attribute (e.g., design-intent height = 3.2 m vs. as-built height = 3.18 m), both coexist. The provenance block — `assertedBy`, `assertedAt`, `authority` — carries what is needed for consumers to apply their own resolution policy. No system-imposed resolution destroys information. This approach stands in stark contrast to the layer approach proposed by USD and considered in the current IFCX development ([RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md), [RFC-IFC5-033](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md), [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md))

---

## 4. Extended Considerations

### 4.1 Package Model

A package is the normative transmission unit — a JSON document bundling a collection of components:

```json
{
  "ifcPackage": "1.0",
  "id": "package-uuid",
  "provenance": {
    "assertedBy": "urn:org:design-team",
    "assertedAt": "2026-07-31T00:00:00Z",
    "authority": "design-intent"
  },
  "schemas": {
    "ifc":   { "uri": "https://standards.buildingsmart.org/ifc/v5" },
    "nlsfb": { "uri": "https://identifier.buildingsmart.org/uri/nlsfb/nlsfb2005/2.2" }
  },
  "data": [ ... ]
}
```

Package-level provenance is inherited by all components in `data[]` that do not carry their own provenance block. This makes the common case concise — a single-author file needs only one provenance declaration — while still supporting mixed-authority packages where individual components override it. ([RFC-IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md), [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md))

---

### 4.2 Open-World Attribute Semantics

Under the open-world assumption ([RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md)), an absent attribute means *not yet asserted*, not false. A third state is needed to distinguish "unknown" from "out of scope." The normative three-state convention:

| State | Representation | Meaning |
|---|---|---|
| Known | typed value | Property is asserted and its value is stated |
| Explicitly unknown | `null` | The asserting party is aware of the attribute but does not have its value |
| Out of scope | key absent | No claim is made; the property may be asserted in another component |

Where richer metadata is needed — e.g., "pending fire-rating review" — an extended form is used: `{ "status": "unknown", "reason": "pending fire rating review" }`.

---

### 4.3 Component Taxonomy and Subtype Polymorphism

IFC4X's class hierarchy (`IfcWall → IfcBuildingElement → IfcElement → IfcProduct`) is essential for query correctness. A query for "all `IfcBuildingElement` instances" must return walls, columns, beams, and all derived types. IFCX's flat class attribute (`bsi::ifc::class: "IfcWall"`) does not encode the supertype chain, so this query fails without external schema knowledge.

The proposed mechanism uses bSDD URIs. Each identity component carries a bSDD URI for its IFC class:

```json
"taxonomy": { "ref": "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWall" }
```

The bSDD API resolves the supertype chain at query time. A local taxonomy cache (a JSON dictionary mapping each class URI to its full supertype chain) can be bundled with any IFC5 package for offline use. ([RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md), [RFC-IFC5-027](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md))

---

### 4.4 Units and Data Types

IFC4X's proprietary measure type system (`IfcLengthMeasure`, `IfcAreaMeasure`, etc.) predates modern interoperability standards. The proposed approach replaces it with UCUM-coded quantity values:

```json
{ "value": 3.2,   "unit": "m"   }
{ "value": 45.0,  "unit": "deg" }
{ "value": 529.0, "unit": "kg/m3" }
```

A normative IFC4X-to-UCUM code mapping table is published as an annex. IFC-specific complex data types (`IfcRectangleProfileDef`, `IfcCompositeCurve`, etc.) are expressed as typed JSON objects re-encoded in the Layer 1 data model. ([RFC-IFC5-028](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md))

---

### 4.5 AI Readiness

AI readiness is a consequence of correctly specifying the data model, not a separate profile. ([RFC-IFC5-036](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md), [RFC-IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md))

- **Layer 1 (data model):** All data is named, typed, schema-free-parseable JSON. Any IFC5 document can be parsed into `{id, type, entity, attributes}` without schema knowledge. Training datasets are consistent across authors. Graph construction requires only `{"ref": "uuid"}` links.
- **Layer 1.5 (provenance):** `authority` fields distinguish authoritative facts from AI-generated or inferred data — essential for responsible AI use in regulated contexts.
- **Layer 2 (flat components):** Flat typed components give AI direct access to IFC semantics. An LLM receiving `IfcWallIdentity`, `Pset_WallCommon`, and `IfcRelVoidsElement` components can reason about the wall's properties and openings without traversing a class hierarchy. The flat array is tabular at the component level and graph-structured at the reference level — matching the strengths of both transformer and graph architectures.
- **Layer 3 (materialisation):** On-demand expansion of typicals and overlays produces a flat, complete component set for any entity. Pre-resolved snapshots may optionally be carried for AI pre-indexing pipelines, eliminating repeated composition work at the cost of a second source of truth that must be managed carefully.

---

### 4.6 Backward Compatibility with IFC4X

The architecture does not claim structural backward compatibility — the file format differs and migration is required. It does claim **lossless semantic coverage**: every piece of information expressible in IFC4X is expressible here without loss of meaning. ([RFC-IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md))

Migration from IFC4X is a deterministic transformation:

- Each `IfcRoot` instance → identity component (e.g., `ifc:IfcWallIdentity`)
- Each `IfcPropertySet` → `ifc:IfcPropertySet` component
- Each `IfcRel*` instance → typed relation component on its relating entity
- GlobalId → decompressed UUID (lossless)
- IFC4X spatial hierarchy → `ifc:SpatialView` named view component
- `IfcTypeObject` → `ifc:IfcTypical` entity

The IFCX `customdata::originalStepInstance` pattern — storing the original SPF line as a string attribute — is endorsed as a migration safety net, clearly marked as non-normative. It may be removed once confidence in the migration is established.

---

### 4.7 Recommendations
This section provides a concise summary of the ~19 recommended enhancements to the IFCX prototype, with links to relevant RFCs for further details and to support structured feedback.

#### Layer 1 — Foundational Data Primitives

**R1.** Adopt JSON as the normative data model. Alternative encodings (CBOR, binary) are permitted as profiles but must round-trip losslessly to JSON. ([RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md), [RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md))

**R2.** Designate UUID (v4 or v5) as canonical identity for all named objects. Path strings are navigational aliases only. ([RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md))

**R3.** Require named, typed attributes throughout. No positional attributes in IFC5. ([RFC-IFC5-023](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md))

**R4.** Standardise `{"ref": "uuid"}` for local references and `{"ref": "uri", "fetchedAt": "iso8601"}` for external references. ([RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md), [RFC-IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md))

#### Layer 1.5 — Component Primitive and Package Model

**R5.** Define the component primitive normatively as `{id, type, entity, attributes, provenance}`. Provenance (`assertedBy`, `assertedAt`, `authority`) required on every component, with package-level default. ([RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md), [RFC-IFC5-031](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md))

**R6.** Adopt open-world entity existence: an entity exists by virtue of being referenced in at least one component. ([RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md))

**R7.** Standardise the three-state attribute model: absent = out of scope; `null` = explicitly unknown; typed value = known. ([RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md))

**R8.** Define the package envelope `{ifcPackage, id, provenance, schemas, data}` as the normative transmission unit. ([RFC-IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md))

#### Layer 2 — IFC4X Business Logic

**R9.** Map all IFC4X entity classes to typed identity components. The component's presence constitutes class membership. ([RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md), [RFC-IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md))

**R10.** Map all IFC4X `IfcPropertySet` instances to property-set components using the three-state value convention. ([RFC-IFC5-013](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md))

**R11.** Map all IFC4X `IfcRel*` families to typed relation components: 1:many on the relating entity; 1:1 on the dependent entity; M:N as standalone entities. ([RFC-IFC5-008](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md), [RFC-IFC5-025](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-025-collections-cardinality.md))

**R12.** Use bSDD URIs as the class taxonomy mechanism. Bundle a local taxonomy cache for offline subtype queries. ([RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md), [RFC-IFC5-027](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md))

**R13.** Replace IFC4X measure types with UCUM-coded quantity values `{"value": n, "unit": "ucum"}`. Publish a normative IFC4X-to-UCUM mapping table. ([RFC-IFC5-028](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md))

#### Layer 3 — Views, Typicals, and Overlays

**R14.** Decouple path from identity. Express spatial hierarchies as named `ifc:SpatialView` components. A dataset may carry any number of simultaneous views. ([RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md), [RFC-IFC5-016](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md))

**R15.** Formalise the typical as the replacement for IFCX `inherits` and IFC4X `IfcTypeObject`. Instances reference the typical via `ifc:IfcInstantiates` and carry explicit override components only. ([RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md), [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md))

**R16.** Treat materialisation as an on-demand expansion operation — the composition engine resolves typicals and overlays into a flat component set when a consumer needs it. Do not recommend carrying materialised data in files as a general practice; only do so for specific deployment purposes (AI pre-indexing, read-only API responses), marking the result with `authority: "materialized-from"` and `derivedFrom` references. ([RFC-IFC5-036](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md))

**R17.** Adopt multi-party authorship as a first-class capability: conflicting components coexist; consumers apply their own resolution policy based on provenance fields. ([RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md), [RFC-IFC5-033](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md))

#### Cross-Cutting

**R18.** State the Weak Open World Assumption (OWA) explicitly as the normative premise for IFC5 in the foundational RFC: absent facts are unknown rather than false; assertions are additive; provenance is required. ([RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md), [RFC-IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md))

**R19.** Address AI readiness at the data model level, not as a profile. Named types, flat component structure, and provenance at Layers 1–2 are sufficient; no separate AI RFC is required if the foundational RFCs are correctly specified. ([RFC-IFC5-036](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md))

---

### 4.8 Hello Wall — Architecture Comparison

The table below summarises how the Hello Wall example is represented in IFCX and the proposed architecture.

| Construct | IFCX | Proposed Architecture |
|---|---|---|
|  Entity identity | `path` field = UUID; class as flat attribute | `ifc:IfcWallIdentity` component on entity UUID; bSDD URI for taxonomy |
| Spatial hierarchy | `children` map (rooted tree defining identity) | `ifc:SpatialView` component (named navigational view, decoupled from identity) |
| Property sets | `bsi::ifc::prop::*` flat attributes on path | `ifc:IfcPropertySet` component; UCUM quantities; three-state values |
| Type / instance (windows) | `inherits` arc to window type UUID | `ifc:IfcTypical` with `componentTemplates`; instances via `ifc:IfcInstantiates` + explicit overrides |
| Void / fill relationship | Not modelled | `ifc:IfcRelVoidsElement` on wall + `ifc:IfcRelFillsElement` on window |
| Material | `inherits` arc to material node | `ifc:IfcRelAssociatesMaterial` component on the material entity |
| Space boundary | `bsi::ifc::spaceBoundary` inline attribute with embedded refs | `ifc:IfcRelSpaceBoundary` component on the space; geometry node ref |
| Class taxonomy / polymorphism | Flat string attribute; no supertype encoding | bSDD URI on each identity component; local taxonomy cache optional |
| Provenance | None | `provenance` block per component; package-level default |
| Multiple spatial organisations | Not supported (single tree) | Multiple `ifc:SpatialView` components per package |
| AI consumption | Requires composition resolution before understanding | Flat typed components directly accessible; on-demand materialisation expands typicals to full component sets; optional carried `ifc:MaterialisedSnapshot` for pre-indexing pipelines |

---

## 5. Conclusion

IFCX identifies the right architectural direction for IFC5: building data as scene description, UUID-based identity, namespaced typed attributes, and prototype/instance composition. The extensions proposed in this paper are intended to carry that direction to its logical conclusions.

Separating path from identity completes the open-world aspiration that the IFCX repeated-path-record structure already gestures toward. Expressing all IFC4X relationship families as typed components closes the relation gap without altering the rest of the architecture. Making the typical mechanism explicit and separate from the identity model clarifies what is inherited and what is overridden, enabling both authoritative authoring and on-demand materialisation to full component sets from the same data. Adding provenance at the component level is the minimum change required to make multi-party, federated BIM data honest about its origins.

The result is an architecture capable of delivering three commitments simultaneously: lossless coverage of IFC4X's business logic; native AI readability at the ground level; and open-world federation without abandoning the composition model that makes IFCX compelling. The companion `hello-wall-ifc5.json` demonstrates each of these commitments in a concrete, directly comparable example.
