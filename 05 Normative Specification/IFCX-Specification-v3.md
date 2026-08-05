# IFCX Format Specification — Alpha Draft

**Version:** Alpha (ifcx_alpha)  
**Date:** 2026-08-05  
**Source repository:** [buildingSMART/IFC5-development](https://github.com/buildingSMART/IFC5-development)  
**Reference example:** `examples/Hello Wall/hello-wall.ifcx`  
**Schema:** `schema/ifcx.tsp` (TypeSpec) → `schema/out/ts/ifcx.d.ts` (generated TypeScript)  
**RFC repository:** [Drshelden/IFCV5Work](https://github.com/Drshelden/IFCV5Work/tree/master/02%20RFCs)
**Cross-reference:** [GitHub](https://github.com/Drshelden/IFCV5Work/blob/master/05%20Normative%20Specification/IFCX-Specification-v3.md) · Google Docs *(link generated on first `sync_and_push` — see `scripts/drive_index.json`)*  

> **Status note.** IFCX is in active architectural development. Decisions marked ⚠ are under active committee discussion; the behavior described reflects the current `hello-wall.ifcx` example and buildingSMART alpha conventions, not a finalized normative standard.

> **Reading note (v3).** Collapsed **▶ IFCY delta** blocks are embedded throughout. Blocks after individual sub-sections show how IFCY approaches the same topic differently. Blocks at the end of numbered sections cover IFCY-only features with no IFCX counterpart.

---


## Table of Contents

- [1. Guiding Principles](#1-guiding-principles)
    - [1.1. JSON as normative data substrate](#11-json-as-normative-data-substrate)
    - [1.2. Scene graph composition model](#12-scene-graph-composition-model)
    - [1.3. Path-addressed node identity](#13-path-addressed-node-identity)
    - [1.4. Namespace-qualified attribute vocabulary](#14-namespace-qualified-attribute-vocabulary)
    - [1.5. Modular schema imports](#15-modular-schema-imports)
    - [1.6. Additive, layer-composable authoring](#16-additive-layer-composable-authoring)
    - [1.7. USD alignment for geometry and composition](#17-usd-alignment-for-geometry-and-composition)
- [2. Document Structure](#2-document-structure)
    - [2.1. Top-level file envelope](#21-top-level-file-envelope)
    - [2.2. Header](#22-header)
    - [2.3. Imports](#23-imports)
    - [2.4. Schemas](#24-schemas)
    - [2.5. Data array](#25-data-array)
- [3. Identity and Addressing](#3-identity-and-addressing)
    - [3.1. Path field as node identity](#31-path-field-as-node-identity)
    - [3.2. UUID-valued paths](#32-uuid-valued-paths)
    - [3.3. Human-readable child edge labels](#33-human-readable-child-edge-labels)
- [4. Graph Primitives](#4-graph-primitives)
    - [4.1. Node record structure](#41-node-record-structure)
    - [4.2. `children` — containment and aggregation](#42-children--containment-and-aggregation)
    - [4.3. `inherits` — type-occurrence composition](#43-inherits--type-occurrence-composition)
    - [4.4. Additive patching — multiple records per path](#44-additive-patching--multiple-records-per-path)
- [5. Type System and Class Identity](#5-type-system-and-class-identity)
    - [5.1. IFC class declaration](#51-ifc-class-declaration)
    - [5.2. Type node geometry sharing](#52-type-node-geometry-sharing)
    - [5.3. Type-level named properties](#53-type-level-named-properties)
- [6. Attribute Conventions](#6-attribute-conventions)
    - [6.1. Namespace `::` syntax](#61-namespace--syntax)
    - [6.2. Scalar value encoding](#62-scalar-value-encoding)
    - [6.3. Object-valued attributes](#63-object-valued-attributes)
    - [6.4. Reference values](#64-reference-values)
- [7. Geometry](#7-geometry)
    - [7.1. USD geometry alignment](#71-usd-geometry-alignment)
    - [7.2. Triangulated mesh](#72-triangulated-mesh)
    - [7.3. Basis curves](#73-basis-curves)
    - [7.4. Transform (placement)](#74-transform-placement)
    - [7.5. Visibility](#75-visibility)
- [8. Spatial Structure and Relationships](#8-spatial-structure-and-relationships)
    - [8.1. Spatial hierarchy via `children`](#81-spatial-hierarchy-via-children)
    - [8.2. Space boundaries](#82-space-boundaries)
    - [8.3. Openings and voids](#83-openings-and-voids)
- [9. Properties, Materials, and Classification](#9-properties-materials-and-classification)
    - [9.1. Flat property keys](#91-flat-property-keys)
    - [9.2. Material node](#92-material-node)
    - [9.3. Material assignment via `inherits`](#93-material-assignment-via-inherits)
    - [9.4. External classification](#94-external-classification)
    - [9.5. Material performance data](#95-material-performance-data)
- [10. Presentation and Metadata](#10-presentation-and-metadata)
    - [10.1. Color and opacity](#101-color-and-opacity)
    - [10.2. STEP provenance traceability](#102-step-provenance-traceability)
- [11. Composition and Federation](#11-composition-and-federation)
    - [11.1. Layer federation](#111-layer-federation)
    - [11.2. Conflict resolution — last-writer-wins](#112-conflict-resolution--last-writer-wins)
    - [11.3. Null as deletion](#113-null-as-deletion)
    - [11.4. Composition expansion](#114-composition-expansion)
- [12. Open Decision Register](#12-open-decision-register)
    - [IFCY §12 — Provenance and Trust](#ifcy-12--provenance-and-trust)
    - [IFCY §13 — Pre-Resolved Views: `ifc:MaterialisedSnapshot`](#ifcy-13--pre-resolved-views-ifcmaterialisedsnapshot)

---

## 1. Guiding Principles

IFCX is a JSON-based scene graph exchange format for IFC5. Seven design principles govern every convention in this specification.

### 1.1. JSON as normative data substrate

All IFC5 data is encoded as JSON. STEP Physical File (SPF/ISO-10303-21) is not the exchange format. JSON native types (boolean, number, string, array, object, null) are the canonical scalar primitives. See [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) and [RFC-IFC5-006: Serialization and Encoding](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md).

<details>
<summary>IFCY delta</summary>

IFCY files describe a partial view of a building model. Absent components do not imply absence of reality — they indicate the component is out of scope for this package. Both formats use JSON as the data substrate; IFCY frames this explicitly as an open-world contract rather than a closed serialization. Consumers must tolerate missing data rather than failing on incomplete input.  
→ [RFC-IFC5-041: Open World vs. Closed World](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md)

</details>

---

### 1.2. Scene graph composition model

IFCX represents a model as a directed graph of nodes, each addressed by a path. Hierarchy, type composition, and override layering follow a scene graph composition model inspired by OpenUSD. This is explicitly not a flat ECS (Entity-Component-System) array. See [RFC-IFC5-007: Scene Graph vs. ECS vs. Hybrid Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md).

<details>
<summary>IFCY delta</summary>

Entities are bare UUIDs; all meaning is attached as typed components. There is no hierarchical scene graph baked into entity identity. Spatial trees are one named view among many, declared separately from identity. This is an explicit rejection of the IFCX scene graph approach in favour of a flat Entity-Component-System (ECS) architecture.  

</details>

---

### 1.3. Path-addressed node identity

Every node is identified by a `path` field. In the current alpha, path values are UUID-like strings derived from IFC GlobalIds. The path simultaneously serves as stable identity and as the graph address at which attribute opinions accumulate. ⚠ Whether path should be the sole identity or one of several identity channels (alongside a separate UUID and URI) is under active discussion. See [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) and [RFC-IFC5-004: Path Model and Addressing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md).

<details>
<summary>IFCY delta</summary>

Every entity is addressed by a UUID that is globally unique, persistent, and opaque. No path, line number, or sequence position is identity-bearing. UUIDs survive federation, copy, split, and re-export. IFCY separates identity from graph position entirely — the UUID does not double as a scene-graph address.  

</details>

---

### 1.4. Namespace-qualified attribute vocabulary

All semantic attributes use `::` double-colon delimiters to express namespace hierarchy (e.g. `bsi::ifc::class`, `usd::usdgeom::mesh`). This enables multi-vocabulary layering on a single node without key collision. See [RFC-IFC5-005: Namespaces](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md) and [RFC-IFC5-023: Attribute Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md).

<details>
<summary>IFCY delta</summary>

A component is a typed, schema-validated record attached to an entity. One entity carries many components; one component belongs to exactly one entity. The schema `type` field (e.g. `ifc:IfcWallIdentity`) determines what attributes are legal and what they mean. Multi-vocabulary layering is achieved by attaching multiple typed components rather than by namespace-prefixing keys within a single object.  
→ [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md)

</details>

---

### 1.5. Modular schema imports

Vocabulary schemas are not embedded in full; they are referenced by URI. An IFCX file declares which external schema bundles it relies on via an `imports` array. This enables multiple domain vocabularies (IFC, USD, NL-SfB, materials) to coexist in one file without conflicts. See [RFC-IFC5-012: Modular Schema Imports](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) and [RFC-IFC5-032: Extensibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md).

<details>
<summary>IFCY delta</summary>

Containment, type-instance links, voids, and material associations are expressed as typed relation components rather than as inline arrays or map keys. Every relationship is independently addressable, versionable, and overridable. Schema imports become namespace prefix declarations in the `schemas` map; no separate `imports` array is used.  
→ [RFC-IFC5-008: Relationship Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md)

</details>

---

### 1.6. Additive, layer-composable authoring

Multiple records in the `data` array may refer to the same `path`. Each such record contributes additional attributes, children, or inherits links. This additive-patching model supports layered authoring, federated model assembly, and incremental update without rewriting the full node. Null values signal deletion during composition. See [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) and [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md).

<details>
<summary>IFCY delta</summary>

Multiple IFCY packages may contribute components to the same entity UUID. There is no inherent conflict when packages add different-typed components to the same entity — each component type is an independent slot. Conflict arises only when two packages contribute components of the same type to the same entity; last-writer-wins in layer order applies then. The additive model operates at component granularity rather than at attribute-key granularity.  

</details>

---

### 1.7. USD alignment for geometry and composition

Geometry payloads and scene composition semantics are directly aligned with OpenUSD conventions (`usd::usdgeom::*`, `usd::xformop`, layer stacks, LIVRPS composition). IFCX is not a USD file but borrows USD's scene graph model to support broad tooling interoperability. See [RFC-IFC5-015: OpenUSD Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) and [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md).

<details>
<summary>IFCY delta</summary>

IFCY adopts the same USD geometry vocabulary (`usd:MeshGeometry`, `usd:CurveGeometry`, `usd:XformComponent`) as IFCX. However, IFCY does not adopt USD's scene graph composition model — layer stacks and LIVRPS composition are replaced by the ECS component-layer model. USD alignment in IFCY is scoped to geometry data shapes, not to scene composition semantics.  

</details>

<details>
<summary>IFCY delta</summary>

**1.8 — Provenance is a first-class attribute.** Every package carries a package-level provenance record. Individual components may carry their own provenance, overriding the package default. The `authority` field distinguishes design intent from as-built survey from AI inference. IFCX records provenance only for IFC4.x migration traceability (`customdata.originalStepInstance`); IFCY makes provenance a required top-level concern for all authoring contexts.  
→ [RFC-IFC5-037: Security and Trust](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-037-security-trust.md), [RFC-IFC5-031: Metadata and Custom Data](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md)

**1.9 — Three-state value semantics.** Scalar values are typed (`T`), explicitly unknown (`null`), or absent (key omitted). `null` is a meaningful assertion — "this property is known to be unknown." Absence means the property is out of scope for this package. IFCX does not define this distinction; absent and null are equivalent in IFCX attribute values.  
→ [RFC-IFC5-025: Collections and Cardinality](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-025-collections-cardinality.md)

**1.10 — UCUM units on every measured value.** Numeric quantities carry an explicit UCUM unit string (`{ "value": 3.0, "unit": "m" }`) rather than relying on file-level unit declarations. IFCX carries bare JSON numbers with an implied SI context and no per-value unit annotation.  
→ [RFC-IFC5-028: Units and Measures](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md)

</details>

---

## 2. Document Structure

### 2.1. Top-level file envelope

An IFCX file is a single JSON object with exactly four top-level keys: `header`, `imports`, `schemas`, and `data`. The key names are unprefixed at the top level (⚠ prefixed `ifcx::` variants have been proposed; the canonical form is TBD).

```json
{
  "header":  { ... },
  "imports": [ ... ],
  "schemas": { ... },
  "data":    [ ... ]
}
```

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md)

<details>
<summary>IFCY delta</summary>

A valid IFCY file is a JSON object with five required keys: `ifcPackage`, `id`, `provenance`, `schemas`, and `data`. There is no `header` object or `imports` array; namespace origins are declared inline in `schemas`. Provenance is required at the package level with no IFCX equivalent.

```json
{
  "ifcPackage": "1.0",
  "id": "b9f3e1a2-c847-4d56-9e23-f70a18c5d123",
  "provenance": {
    "assertedBy": "technical@buildingsmart.org",
    "assertedAt": "2026-07-31T00:00:00Z",
    "authority": "design-intent"
  },
  "schemas": {
    "ifc": { "uri": "https://standards.buildingsmart.org/ifc/v5", "description": "IFC5 component types" },
    "usd": { "uri": "https://openusd.org/ns", "description": "USD geometry primitives" }
  },
  "data": [ ... ]
}
```


</details>

---

### 2.2. Header

The `header` object carries file-level metadata. All four fields are required in the alpha schema.

```json
"header": {
  "id":           "ifc5.technical.buildingsmart.org/examples/Hello Wall/hello-wall.ifcx",
  "ifcxVersion":  "ifcx_alpha",
  "dataVersion":  "1.0.0",
  "author":       "technical@buildingsmart.org",
  "timestamp":    "time string"
}
```

`id` is a string identifier for the dataset (path or URI form). `ifcxVersion` declares the format version; currently always `"ifcx_alpha"`. `dataVersion` is a dataset-specific semantic version. ⚠ `timestamp` format should conform to ISO 8601 but is not enforced in the alpha.

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) · [RFC-IFC5-031: Metadata and Custom Data](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md) · [RFC-IFC5-022: Versioning and Schema Evolution](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-022-versioning-schema-evolution.md)

<details>
<summary>IFCY delta</summary>

IFCY replaces the `header` object with two separate top-level keys:

**`ifcPackage`** carries the format version string (currently `"1.0"`). Parsers use this to select the correct schema interpreter. ⚠ Versioning strategy for minor vs. breaking changes not yet defined.

**`id`** is a UUID identifying this package as an artifact — the addressable identity of the file itself, not of any entity within it. A re-exported or federated package receives a new `id`. There is no `dataVersion` or `author` field at the top level; authorship is carried in the `provenance` object (see 2.6).

→ [RFC-IFC5-022: Versioning and Schema Evolution](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-022-versioning-schema-evolution.md), [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md)

</details>

---

### 2.3. Imports

The `imports` array lists external schema bundles the file depends on. Each entry is an object with a required `uri` string and an optional `integrity` hash. Imports are ordered; the vocabulary scope of each URI applies to all attributes bearing that namespace prefix.

```json
"imports": [
  { "uri": "https://ifcx.dev/@standards.buildingsmart.org/ifc/core/ifc@v5a.ifcx" },
  { "uri": "https://ifcx.dev/@standards.buildingsmart.org/ifc/core/prop@v5a.ifcx" },
  { "uri": "https://ifcx.dev/@standards.buildingsmart.org/ifc/ifc-mat/ifc-mat@v1.0.0.ifcx" },
  { "uri": "https://ifcx.dev/@openusd.org/usd@v1.ifcx" },
  { "uri": "https://ifcx.dev/@nlsfb/nlsfb@v1.ifcx" }
]
```

► [RFC-IFC5-012: Modular Schema Imports](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) · [RFC-IFC5-032: Extensibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md)

<details>
<summary>IFCY delta</summary>

IFCY has no `imports` array. Instead, the `schemas` map declares namespace prefixes inline. Each entry maps a short prefix (e.g. `ifc`, `usd`, `nlsfb`) to a `{ uri, description }` object. These prefixes appear as the leading segment of every component `type` field. There is no integrity hash mechanism; namespace governance is implied by the URI.

```json
"schemas": {
  "ifc":   { "uri": "https://standards.buildingsmart.org/ifc/v5",  "description": "IFC5 component types" },
  "usd":   { "uri": "https://openusd.org/ns",                      "description": "USD geometry primitives" },
  "nlsfb": { "uri": "https://www.nlsfb.nl/ontology",               "description": "NL-SfB classification" }
}
```

→ [RFC-IFC5-005: Namespaces](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md), [RFC-IFC5-012: Modular Schema Imports](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md)

</details>

---

### 2.4. Schemas

The `schemas` object declares inline schema entries for attribute keys that are not fully covered by the imported bundles — primarily extension or custom namespaces. Each entry maps a key name to an `IfcxSchema` object containing a `value` field describing the allowed data type and its structure.

```json
"schemas": {
  "customdata": {
    "value": {
      "dataType": "Object",
      "objectRestrictions": {
        "values": {
          "originalStepInstance": { "dataType": "String" }
        }
      }
    }
  }
}
```

Valid `dataType` values: `"Real"`, `"Boolean"`, `"Integer"`, `"String"`, `"DateTime"`, `"Enum"`, `"Array"`, `"Object"`, `"Reference"`, `"Blob"`.

► [RFC-IFC5-032: Extensibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md) · [RFC-IFC5-024: Type System and Primitives](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-024-type-system-primitives.md) · [RFC-IFC5-025: Collections and Cardinality](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-025-collections-cardinality.md)

<details>
<summary>IFCY delta</summary>

In IFCY, `schemas` serves only as a namespace prefix registry — it maps short prefixes to URIs. It does not carry inline type definitions or dataType constraints. All attribute-level type validation is governed by the component's `type` field, which resolves to a schema at the URI registered under that prefix. Custom extension types use a third-party prefix namespace and require no inline declaration.

→ [RFC-IFC5-005: Namespaces](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md), [RFC-IFC5-032: Extensibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md)

</details>

---

### 2.5. Data array

`data` is an ordered JSON array of node records (`IfcxNode[]`). The array is the entire semantic payload of the file. Multiple records may share the same `path` value; they are composed additively in document order.

<details>
<summary>IFCY delta</summary>

IFCY adds a required `provenance` top-level key with no IFCX equivalent. It applies to all components in the package unless a component declares its own override. Fields: `assertedBy` (email or identifier), `assertedAt` (ISO 8601 timestamp), `authority` (enum — see section 12 for full enumeration).

```json
"provenance": {
  "assertedBy": "technical@buildingsmart.org",
  "assertedAt": "2026-07-31T00:00:00Z",
  "authority": "design-intent"
}
```

→ [RFC-IFC5-031: Metadata and Custom Data](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md), [RFC-IFC5-037: Security and Trust](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-037-security-trust.md)

</details>

---

## 3. Identity and Addressing

### 3.1. Path field as node identity

Every node record has exactly one `path` field. The path is the stable, globally unique identifier of the node. It is both the node's canonical name and the address at which attribute contributions accumulate across records and layers.

```json
{ "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b", ... }
```

► [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) · [RFC-IFC5-004: Path Model and Addressing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md)

<details>
<summary>IFCY delta</summary>

An entity is a UUID string. It has no attributes of its own. All meaning attached to an entity lives in components that reference it via the `entity` field. The `path` key does not exist in IFCY — the entity UUID appears only as a value inside component records, never as a top-level node key.

```json
"entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b"
```

The UUID is the same value IFCX uses as a path; the structural difference is that IFCX uses it as an addressable node key while IFCY uses it purely as an opaque reference.  
→ [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md), [RFC-IFC5-007: Scene Graph vs. ECS vs. Hybrid Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md)

</details>

---

### 3.2. UUID-valued paths

In `hello-wall.ifcx`, all path values are UUID-like strings (RFC 4122 format) derived deterministically from IFC GlobalIds via a GUID-expansion algorithm. STEP instance numbers (e.g. `#1222`) are not used as node addresses; they are preserved only as provenance metadata. ⚠ Whether IFC GlobalId, UUID v4/v5, URI, or a combination is the normative identity carrier is under active committee discussion.

```json
{ "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" }
```
*Derived from IFC GlobalId `2JUHrTM_j3UxZiBnyBfByx` (IfcWall).*

► [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) · [RFC-IFC5-001: Strategic Architecture Mode](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md)

<details>
<summary>IFCY delta</summary>

Entity UUIDs carry no parent-child meaning. Two entities are related only by explicit relation components. A consumer cannot infer spatial containment or type-instance membership from UUID values alone. IFCX paths can imply structural position through the `children` map (see 4.2); in IFCY no such inference is possible or intended.  
→ [RFC-IFC5-004: Path Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md)

</details>

---

### 3.3. Human-readable child edge labels

When a node references child nodes via the `children` map (see 4.2), the keys are human-readable label strings — not path values. Labels correspond to meaningful element names within the parent's scope. Duplicate labels are disambiguated with a `_001`, `_002` suffix convention.

```json
{
  "path": "44af358b-3160-4063-8a89-a868335ff3b5",
  "children": {
    "My_Space": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6",
    "Wall":     "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b"
  }
}
```

► [RFC-IFC5-004: Path Model and Addressing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md)

<details>
<summary>IFCY delta</summary>

All cross-entity references use a `{ "ref": "<uuid>" }` wrapper. An optional `pathLabel` field carries a human-readable annotation for display purposes; it has no semantic weight. Two refs with different `pathLabel` values but the same `ref` UUID resolve to the same entity. There is no IFCY equivalent of the `children` map key as a structural position label.

```json
"root": { "ref": "14adb22b-2f47-438a-a6f3-1e90b0b16d3a", "pathLabel": "My_Project" }
```

→ [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md), [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md)

</details>

---

## 4. Graph Primitives

### 4.1. Node record structure

Each entry in the `data` array is an `IfcxNode` with one required field (`path`) and three optional fields (`children`, `inherits`, `attributes`). All three optional fields may appear in the same record or across separate records for the same path.

```
IfcxNode {
  path:       string            // required
  children?:  { [label]: path | null }
  inherits?:  { [role]:  path | null }
  attributes?: { [nsKey]: value }
}
```

► [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) · [RFC-IFC5-007: Scene Graph vs. ECS vs. Hybrid Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md)

<details>
<summary>IFCY delta</summary>

Every item in the `data` array is a component with four required fields (`id`, `type`, `entity`, `attributes`) and one optional field (`provenance`). There are no `children`, `inherits`, or `path` fields. The `type` field discriminates the schema; the `entity` field points to the UUID the component belongs to; `id` makes the component itself independently addressable.

```json
{
  "id":       "c0000000-0000-0000-0000-000000000006",
  "type":     "ifc:IfcWallIdentity",
  "entity":   "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "name":        "Wall",
    "description": null,
    "taxonomy":    { "ref": "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWall" }
  }
}
```

→ [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md), [RFC-IFC5-023: Attribute Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md)

</details>

---

### 4.2. `children` — containment and aggregation

The `children` map encodes parent-child containment edges. Each entry maps a human-readable label to the child node's path. Children relationships replace the IFC4.x `IfcRelAggregates`, `IfcRelContainedInSpatialStructure`, and similar decomposition relations for purposes of hierarchy navigation.

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "children": {
    "Body":       "634f90c3-831e-5f29-a9b2-fa69b207821e",
    "Axis":       "8407e490-ceaa-56e5-96df-2351d9110668",
    "Directrix":  "9d1fce89-e179-5076-9a3b-1b40eef3524b",
    "Window":     "2c2d549f-f9fe-4e22-8590-562fda81a690",
    "Window_001": "592504dc-469a-44d6-9ae8-c801b591679b"
  }
}
```

► [RFC-IFC5-016: Spatial Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md) · [RFC-IFC5-008: Relationship Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md)

<details>
<summary>IFCY delta</summary>

IFCY expresses containment as explicit typed relation components rather than as map keys on a parent node.

**Spatial containment** (`ifc:IfcRelContainedInSpatialStructure`) — declares that a building element is physically contained within a spatial element:

```json
{
  "id":   "c0000000-0000-0000-0000-000000000015",
  "type": "ifc:IfcRelContainedInSpatialStructure",
  "entity": "a9f3c881-5f5c-4ef3-bb8e-8ef64c76c789",
  "attributes": {
    "relatingStructure": { "ref": "5b4f18da-0942-4c5c-b2a0-be3218b41a4a" },
    "relatedElements":   [{ "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" }]
  }
}
```

**Spatial decomposition** (`ifc:IfcRelAggregates`) — declares Project→Site→Building→Storey hierarchy:

```json
{
  "type": "ifc:IfcRelAggregates",
  "entity": "<relation-entity-uuid>",
  "attributes": {
    "relatingObject":  { "ref": "<building-uuid>" },
    "relatedObjects":  [{ "ref": "<storey-uuid>" }]
  }
}
```

Each relation is a separately addressable component with its own `id` UUID — it can be overridden or deleted in a federated layer without touching either party entity.  

</details>

---

### 4.3. `inherits` — type-occurrence composition

The `inherits` map encodes typed composition arcs. A node may inherit from one or more named sources. On composition expansion, the inheriting node receives all children, inherits, and attributes of the inherited node, with local values taking precedence. This mechanism replaces `IfcRelDefinesByType` for type-to-instance relationships and is analogous to USD class inheritance.

```json
{
  "path": "2c2d549f-f9fe-4e22-8590-562fda81a690",
  "inherits": {
    "windowType": "25503984-6605-43a1-8597-eae657ff5bea"
  }
}
```

*Window occurrence inherits geometry, properties, and class identity from window type node.*

► [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) · [RFC-IFC5-040: Archetypes, Templates, and Override Mechanisms](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) · [RFC-IFC5-009: Class and Type Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md)

<details>
<summary>IFCY delta</summary>

IFCY provides two explicit mechanisms for type-to-instance relationships, replacing the IFCX `inherits` map:

**`ifc:IfcRelDefinesByType`** — a relation component declaring that occurrences are instances of a type entity. Used for straightforward class-level property inheritance without slot templating.

**`ifc:IfcInstantiates`** — used with the `ifc:IfcTypical` template system. An occurrence entity declares its Typical via an `IfcInstantiates` component and carries only its overrides. The inheritance resolution algorithm expands the Typical's slots and applies instance overrides at read time.

```json
{
  "id":   "c0000000-0000-0000-0000-000000000041",
  "type": "ifc:IfcInstantiates",
  "entity": "2c2d549f-f9fe-4e22-8590-562fda81a690",
  "attributes": {
    "typical": { "ref": "25503984-6605-43a1-8597-eae657ff5bea" }
  }
}
```

The key difference from IFCX: the relationship is a first-class component with its own `id`, not an anonymous map key on the occurrence node.  

</details>

---

### 4.4. Additive patching — multiple records per path

Multiple records in `data` may share the same `path`. Each record contributes its `children`, `inherits`, and `attributes` content additively. This is the primary mechanism for separating concerns (geometry, classification, properties, provenance) across logical layers in a single file. ⚠ Whether this is the normative exchange model or whether one-record-per-path should be required is under committee review.

```json
{ "path": "93791d5d-...", "attributes": { "customdata": { "originalStepInstance": "..." } } },
{ "path": "93791d5d-...", "attributes": { "bsi::ifc::class": { "code": "IfcWall", ... } } },
{ "path": "93791d5d-...", "attributes": { "bsi::ifc::prop::IsExternal": true } },
{ "path": "93791d5d-...", "inherits": { "material": "7a187a90-..." } }
```

*Four separate records, all contributing to the same Wall node.*

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) · [RFC-IFC5-033: Change, Transactions, and Collaboration](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md)

<details>
<summary>IFCY delta</summary>

IFCY achieves the same separation of concerns through multiple components attached to the same entity UUID, each with its own `type`. The equivalent of the four IFCX records above becomes four separate component entries:

```json
{ "type": "ifc:IfcWallIdentity",    "entity": "93791d5d-...", "attributes": { "legacyStepRef": "#1222=IfcWall(...)" } },
{ "type": "ifc:IfcPropertySet",     "entity": "93791d5d-...", "attributes": { "psetName": "Pset_WallCommon", "properties": { "IsExternal": true } } },
{ "type": "ifc:IfcPresentationStyle","entity": "93791d5d-...", "attributes": { "diffuseColor": [0.5,0.5,0.5] } },
{ "type": "ifc:IfcRelAssociatesMaterial", "entity": "<rel-uuid>", "attributes": { "relatedObjects": [{"ref":"93791d5d-..."}], "relatingMaterial": {"ref":"7a187a90-..."} } }
```

Each component has its own `id` UUID, making it independently addressable and overridable across federated packages.  
→ [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md)

</details>

<details>
<summary>IFCY delta</summary>

IFCY defines additional typed relation components that have no direct IFCX key equivalent (IFCX handles these through implicit graph structure or attribute objects):

**4.5 — `ifc:IfcRelVoidsElement` and `ifc:IfcRelFillsElement`.** Openings that subtract volume from a host element are linked via `IfcRelVoidsElement`. A door or window filling an opening uses `IfcRelFillsElement`. Both replace IFCX's implicit void-geometry child structure.

```json
{
  "type": "ifc:IfcRelVoidsElement",
  "entity": "<void-rel-uuid>",
  "attributes": {
    "relatingBuildingElement": { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
    "relatedOpeningElement":   { "ref": "<opening-uuid>" }
  }
}
```

**4.6 — `ifc:IfcRelAssociatesMaterial`.** Links an element entity to a material entity. Replaces IFCX's `bsi::ifc::material` attribute key and `inherits: { material: ... }` map entry.

**4.7 — `ifc:IfcRelSpaceBoundary`.** Declares a thermal or acoustic boundary surface between a space and a bounding element. Replaces IFCX's `bsi::ifc::spaceBoundary` attribute object (see IFCX section 8.2).

→ [RFC-IFC5-026: Openings, Voids, and Fillings](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md), [RFC-IFC5-017: Material Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md), [RFC-IFC5-030: Space Boundaries and Topology](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-030-space-boundaries.md)

</details>

---

## 5. Type System and Class Identity

### 5.1. IFC class declaration

An IFC entity's class is declared via the `bsi::ifc::class` attribute as a structured object carrying both a short code (the IFC class name) and a resolvable URI pointing to the bSDD dictionary entry. Both fields should be present; the URI is the authoritative semantic identifier.

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "bsi::ifc::class": {
      "code": "IfcWall",
      "uri":  "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWall"
    }
  }
}
```

► [RFC-IFC5-009: Class and Type Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) · [RFC-IFC5-027: Classification and External Dictionaries](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md)

<details>
<summary>IFCY delta</summary>

An IFC entity's class is declared by attaching an `ifc:<Type>Identity` component — there is no `bsi::ifc::class` attribute key. The component carries `name`, `description`, and a `taxonomy.ref` bSDD URI as its core fields.

```json
{
  "type": "ifc:IfcWallIdentity",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "name": "Wall",
    "description": null,
    "taxonomy": { "ref": "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWall" }
  }
}
```

The class name (`IfcWall`) appears in the `type` field rather than as an attribute value. The `code` field is removed — it is derivable from the URI and not stored separately.  

</details>

---

### 5.2. Type node geometry sharing

When multiple occurrences share geometry (e.g. two identical windows), the geometry is placed once on a shared type node. Occurrence nodes inherit the type node via `inherits`, acquiring its geometry without duplication. Occurrences may carry a local `usd::xformop` to place themselves.

```json
{ "path": "25503984-...",  "children": { "Void": "...", "Frame": "...", "Glazing": "..." } },
{ "path": "2c2d549f-...", "inherits": { "windowType": "25503984-..." } },
{ "path": "592504dc-...", "inherits": { "windowType": "25503984-..." } }
```

*Type node `25503984-…` holds window sub-geometry. Both window occurrences inherit it.*

► [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) · [RFC-IFC5-040: Archetypes, Templates, and Override Mechanisms](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md)

<details>
<summary>IFCY delta</summary>

Shared geometry is declared in the `componentTemplates` array of an `ifc:IfcTypical` component on the type entity. Each geometry slot has `inheritable: true`. Occurrence entities link to the type via `ifc:IfcInstantiates` and carry only placement overrides.

```json
{
  "type": "ifc:IfcTypical",
  "entity": "25503984-6605-43a1-8597-eae657ff5bea",
  "attributes": {
    "name": "WT01",
    "componentTemplates": [
      { "slotName": "geometry/Frame",   "type": "usd:MeshGeometry", "inheritable": true, "attributes": { "mesh": { ... } } },
      { "slotName": "geometry/Glazing", "type": "usd:MeshGeometry", "inheritable": true, "attributes": { "mesh": { ... } } },
      { "slotName": "geometry/Void",    "type": "usd:MeshGeometry", "inheritable": true, "attributes": { "mesh": { ... } } }
    ]
  }
}
```

Each occurrence carries `ifc:IfcInstantiates → typical: { ref: "25503984-..." }` and a `usd:XformComponent` override for placement.  

</details>

---

### 5.3. Type-level named properties

Properties on a type node are inherited by all occurrence nodes unless overridden. Named properties such as `bsi::ifc::prop::TypeName` and dimensional values (`Height`, `Volume`) may be declared at the type level.

```json
{
  "path": "25503984-6605-43a1-8597-eae657ff5bea",
  "attributes": {
    "bsi::ifc::prop::TypeName": "WT01",
    "bsi::ifc::prop::Volume":   0.025999999592,
    "bsi::ifc::prop::Height":   1.2
  }
}
```

► [RFC-IFC5-013: Property Sets](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md) · [RFC-IFC5-009: Class and Type Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md)

<details>
<summary>IFCY delta</summary>

Type-level properties are declared as `ifc:IfcPropertySet` slots inside the `IfcTypical` component's `componentTemplates` array with `inheritable: true`. Properties use UCUM units for measured values.

```json
{
  "slotName": "properties",
  "type": "ifc:IfcPropertySet",
  "inheritable": true,
  "attributes": {
    "psetName": "Pset_WindowCommon",
    "properties": {
      "IsExternal": true,
      "Height": { "value": 1.2, "unit": "m" },
      "Width":  { "value": 0.75, "unit": "m" }
    }
  }
}
```


</details>

<details>
<summary>IFCY delta</summary>

**5.4 — `taxonomy.ref` as bSDD URI.** The `taxonomy` object within an identity component carries a `ref` URI as the authoritative class pointer. The short `code` field (e.g. `IfcWall`) is derivable from it and not stored separately.

**5.5 — `classifications` array for external systems.** Additional classification references (NL-SfB, UniClass, OmniClass, etc.) are listed in a `classifications` array on the identity component. Each entry: `{ "code", "uri", "system" }`. Replaces IFCX's `nlsfb::class` and similar namespace-keyed classification attributes.

```json
"classifications": [
  { "code": "21.21", "uri": "https://identifier.buildingsmart.org/uri/nlsfb/nlsfb/2020/class/21.21", "system": "NL-SfB" }
]
```

**5.6 — `legacyStepRef`.** When a component originates from IFC4.x STEP, the original STEP entity text is preserved in `legacyStepRef` as an informational string on the identity component. Replaces IFCX's `customdata.originalStepInstance`.

**5.7 — Slot inheritance flag.** Each `componentTemplate` slot carries `inheritable: true/false`. `false` means the slot is type-level only and not propagated to instances. ⚠ Semantics of partial attribute overrides within a slot are under discussion.

**5.8 — Slot naming convention.** Slot names are free strings; recommended convention uses `/` for hierarchy within a logical group (e.g. `geometry/Frame`, `geometry/Glazing`, `geometry/Void`). ⚠ Normative slot naming registry under discussion.

→ [RFC-IFC5-027](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md), [RFC-IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md), [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md)

</details>

---

## 6. Attribute Conventions

### 6.1. Namespace `::` syntax

Attribute keys use `::` as a namespace separator. The convention is `<registry>::<domain>::<subdomain>::<name>`. Known registered prefixes in hello-wall.ifcx: `bsi` (buildingSMART), `usd` (OpenUSD/Pixar), `nlsfb` (NL-SfB classification). ⚠ UpperCamelCase vs lowerCamelCase in the property name segment is not yet standardized.

```
bsi::ifc::class
bsi::ifc::prop::IsExternal
bsi::ifc::presentation::diffuseColor
bsi::ifc-mat::prop::MassDensity
usd::usdgeom::mesh
usd::xformop
nlsfb::class
```

► [RFC-IFC5-005: Namespaces](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md) · [RFC-IFC5-023: Attribute Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md)

<details>
<summary>IFCY delta</summary>

IFCY uses a single `:` colon as the namespace separator in the component `type` field: `<prefix>:<TypeName>` (e.g. `ifc:IfcWallIdentity`, `usd:MeshGeometry`). Attribute keys *within* a component's `attributes` object are unqualified names governed by the component's schema — there are no namespace-prefixed attribute keys inside a component. Multi-vocabulary layering is achieved by using multiple components, not by mixing namespace-prefixed keys on a single object.  

</details>

---

### 6.2. Scalar value encoding

Scalar values are encoded directly as JSON native types. IFC typed wrappers from STEP (e.g. `IfcBoolean`, `IfcReal`, `IfcLabel`) are not present in attribute values. Booleans are `true`/`false`, numerics are JSON numbers, strings are JSON strings.

```json
"bsi::ifc::prop::IsExternal": true,
"bsi::ifc::prop::Volume":     2.783999976,
"bsi::ifc::prop::Height":     3.0
```

► [RFC-IFC5-024: Type System and Primitives](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-024-type-system-primitives.md) · [RFC-IFC5-028: Units and Measures](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md)

---

### 6.3. Object-valued attributes

Attributes with structured values use a JSON object. The object shape is governed by the schema associated with the attribute key (imported or locally declared). There is no separate type-tag field inside the value object; the attribute key itself carries the type.

```json
"bsi::ifc::material": {
  "code": "CONCRETE",
  "uri":  "https://identifier.buildingsmart.org/uri/fish/midas-materials/26/class/CONCRETE"
}
```

► [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) · [RFC-IFC5-025: Collections and Cardinality](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-025-collections-cardinality.md)

---

### 6.4. Reference values

Cross-node references within attributes (e.g. in relationship objects) use a `{ "ref": "<path>" }` wrapper. This distinguishes a reference-to-node from an inline string value.

```json
"bsi::ifc::spaceBoundary": {
  "relatedelement": { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
  "relatingspace":  { "ref": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6" }
}
```

► [RFC-IFC5-023: Attribute Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md) · [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md)

<details>
<summary>IFCY delta</summary>

IFCY uses the same `{ "ref": "<uuid>" }` wrapper but always references entity UUIDs rather than path strings. An optional `pathLabel` field annotates the ref for display — it has no semantic weight. The `ref` value is a pure UUID; no path hierarchy is encoded in it.

```json
"relatingStructure": { "ref": "5b4f18da-0942-4c5c-b2a0-be3218b41a4a", "pathLabel": "My_Storey" }
```


</details>

<details>
<summary>IFCY delta</summary>

**6.5 — Three-state scalar semantics.** Every attribute value is one of: a typed value `T`, `null` (explicitly unknown — key present but value unknown), or absent (key omitted — no assertion made). IFCX does not define this distinction.

```json
"attributes": { "name": "Wall", "description": null }
```

`description: null` asserts "the description is known to be unset." Omitting `description` means this package makes no assertion about it.  
→ [RFC-IFC5-025: Collections and Cardinality](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-025-collections-cardinality.md)

**6.6 — UCUM units on measured values.** Numeric quantities with physical units use `{ "value": <number>, "unit": "<ucum-string>" }` rather than bare numbers. `"m"`, `"m2"`, `"m3"`, `"degC"` etc.

```json
"Volume": { "value": 2.783999976, "unit": "m3" },
"Height": { "value": 3.0,         "unit": "m" }
```

IFCX carries bare numbers (e.g. `"bsi::ifc::prop::Volume": 2.783999976`) with no per-value unit.  
→ [RFC-IFC5-028: Units and Measures](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md)

**6.7 — Bare scalars for dimensionless values.** Boolean, string, and integer values without physical units remain bare JSON primitives. No wrapper object is used unless the value is a measured quantity.

</details>

---

## 7. Geometry

### 7.1. USD geometry alignment

Geometry payloads are expressed using USD schema key conventions. IFCX does not define its own geometry vocabulary; it adopts `usd::usdgeom::*` attribute namespaces and the associated data shapes from OpenUSD. All geometry is currently tessellated to mesh and polyline primitives; parametric/BRep geometry is out of scope for the alpha.

► [RFC-IFC5-015: OpenUSD Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) · [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md)

---

### 7.2. Triangulated mesh

Body geometry is encoded as `usd::usdgeom::mesh` with `points` (vertex coordinates as `[x, y, z]` triples) and `faceVertexIndices` (flat integer index array, all faces triangulated). `faceVertexCounts` is implied (all triangles) and omitted.

```json
{
  "path": "634f90c3-831e-5f29-a9b2-fa69b207821e",
  "attributes": {
    "usd::usdgeom::mesh": {
      "faceVertexIndices": [3, 0, 1, 3, 1, 2, ...],
      "points": [[10, 0, 0], [10, 0.1, 0], [10, 0.1, 3], ...]
    }
  }
}
```

► [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md) · [RFC-IFC5-015: OpenUSD Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md)

<details>
<summary>IFCY delta</summary>

IFCY encodes mesh geometry as a standalone `usd:MeshGeometry` component. The mesh data moves from being a nested attribute value to being the `attributes` of an independent component attached to the entity. The `representationIdentifier` field (`"Body"`, `"Void"`, etc.) replaces the IFCX convention of using a `children` key name as the geometry role label.

```json
{
  "type": "usd:MeshGeometry",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "representationIdentifier": "Body",
    "mesh": {
      "faceVertexIndices": [0, 1, 2, 0, 2, 3, ...],
      "points": [0.0, 0.0, 0.0, 5.0, 0.0, 0.0, ...]
    }
  }
}
```


</details>

---

### 7.3. Basis curves

Linear curve geometry (e.g. wall axis and directrix) uses `usd::usdgeom::basiscurves` with a `points` array. This is used for centerline/reference-curve representations.

```json
{
  "path": "8407e490-ceaa-56e5-96df-2351d9110668",
  "attributes": {
    "usd::usdgeom::basiscurves": {
      "points": [[0, 0, 0], [10, 0, 0]]
    }
  }
}
```

► [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md)

<details>
<summary>IFCY delta</summary>

Linear axis and directrix curves are carried as `usd:CurveGeometry` components with `curve.points` (flat float XYZ array). The component is attached directly to the element entity with `representationIdentifier: "Axis"` rather than living on a child node.

```json
{
  "type": "usd:CurveGeometry",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "representationIdentifier": "Axis",
    "curve": { "points": [0.0, 0.0, 0.0, 5.0, 0.0, 0.0] }
  }
}
```


</details>

---

### 7.4. Transform (placement)

Placement is encoded as `usd::xformop` with a `transform` field holding a 4×4 column-major matrix as a 4-element array of 4-element row arrays. The last row encodes the translation. An identity matrix at world origin does not need to be stated.

```json
{
  "path": "2c2d549f-f9fe-4e22-8590-562fda81a690",
  "attributes": {
    "usd::xformop": {
      "transform": [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1.76767492294312, 0, 1, 1]
      ]
    }
  }
}
```

► [RFC-IFC5-015: OpenUSD Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) · [RFC-IFC5-016: Spatial Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md)

<details>
<summary>IFCY delta</summary>

Placement is a standalone `usd:XformComponent` component. The matrix format is identical; the difference is structural — placement is a component in its own right, not a nested attribute key. `representationIdentifier: "placement"` disambiguates it from other transform-type components.

```json
{
  "type": "usd:XformComponent",
  "entity": "2c2d549f-f9fe-4e22-8590-562fda81a690",
  "attributes": {
    "representationIdentifier": "placement",
    "transform": [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [1.76767492294312, 0, 1, 1]
    ]
  }
}
```


</details>

---

### 7.5. Visibility

Nodes whose geometry should not be rendered by default carry `usd::usdgeom::visibility` with `"visibility": "invisible"`. This is used for type-level geometry nodes that exist solely as composition sources.

```json
{
  "path": "8fada721-cff8-590b-8d0b-9300b5fe8e18",
  "attributes": {
    "usd::usdgeom::visibility": { "visibility": "invisible" }
  }
}
```

*Window Void geometry — present for composition, not rendered directly.*

► [RFC-IFC5-029: Presentation and Appearance](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md) · [RFC-IFC5-015: OpenUSD Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md)

<details>
<summary>IFCY delta</summary>

IFCY has no `usd::usdgeom::visibility` attribute equivalent. The visibility/role of a geometry component is conveyed by `representationIdentifier` (e.g. `"Void"`) and by the relationship type linking it to the element. Void geometry is linked via `ifc:IfcRelVoidsElement` (section 4.5), which makes its role and render-exclusion semantics explicit through the relationship rather than through a visibility flag.  
→ [RFC-IFC5-026: Openings, Voids, and Fillings](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md)

</details>

<details>
<summary>IFCY delta</summary>

**7.6 — `ifc:IfcShapeRepresentation`.** A shape representation component links an element entity to one or more geometry entity nodes. The `representationIdentifier` field (`Body`, `Axis`, `Void`, `Frame`, `Glazing`) indicates the geometric role. This replaces IFCX's use of `children` map keys to label geometry roles.

```json
{
  "type": "ifc:IfcShapeRepresentation",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "representations": [
      { "representationIdentifier": "Body", "geometry": { "ref": "<mesh-entity-uuid>" } }
    ]
  }
}
```

→ [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md), [RFC-IFC5-026: Openings, Voids, and Fillings](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md)

</details>

---

## 8. Spatial Structure and Relationships

### 8.1. Spatial hierarchy via `children`

The IFC spatial hierarchy (Project → Site → Building → Storey → Space/Element) is expressed entirely through `children` maps. Each spatial container node lists its contained elements by name. This replaces IFC4.x `IfcRelAggregates` and `IfcRelContainedInSpatialStructure` for tree navigation.

```json
{ "path": "ab143723-...", "children": { "My_Project":  "14adb22b-..." } },
{ "path": "14adb22b-...", "children": { "My_Site":     "e0834921-..." } },
{ "path": "e0834921-...", "children": { "My_Building": "e84dc79e-..." } },
{ "path": "e84dc79e-...", "children": { "My_Storey":   "44af358b-..." } },
{ "path": "44af358b-...", "children": { "My_Space": "e3035b71-...", "Wall": "93791d5d-..." } }
```

► [RFC-IFC5-016: Spatial Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md) · [RFC-IFC5-008: Relationship Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md)

<details>
<summary>IFCY delta</summary>

IFCY replaces the implicit spatial hierarchy encoded in `children` maps with an explicit `ifc:SpatialView` component. The view names a traversal of the entity graph by specifying a `root` entity and a `composedFrom` array listing which relation component types define parent-child edges in that view. Multiple named views may coexist (e.g. spatial and systems views).

```json
{
  "type": "ifc:SpatialView",
  "entity": "14adb22b-2f47-438a-a6f3-1e90b0b16d3a",
  "attributes": {
    "name": "spatial-default",
    "root": { "ref": "14adb22b-2f47-438a-a6f3-1e90b0b16d3a", "pathLabel": "My_Project" },
    "composedFrom": [
      "ifc:IfcRelAggregates",
      "ifc:IfcRelContainedInSpatialStructure"
    ]
  }
}
```

A consumer traverses the tree by following `IfcRelAggregates` and `IfcRelContainedInSpatialStructure` components starting from `root`. ⚠ Multi-view consistency rules (e.g. can the same element appear under two view roots?) are under discussion.  
→ [RFC-IFC5-016: Spatial Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md), [RFC-IFC5-004: Path Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md)

</details>

---

### 8.2. Space boundaries

Space boundary relationships (IFC4.x `IfcRelSpaceBoundary`) are objectified as dedicated boundary nodes. Each boundary node carries a `bsi::ifc::spaceBoundary` attribute with `relatedelement` and `relatingspace` ref objects. The boundary node's geometry (its `Body` child) is the face of the bounding surface.

```json
{
  "path": "c8ecbf4c-e37a-4489-9133-15163b8a904e",
  "children": { "Body": "911155b7-..." },
  "attributes": {
    "bsi::ifc::spaceBoundary": {
      "relatedelement": { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
      "relatingspace":  { "ref": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6" }
    }
  }
}
```

► [RFC-IFC5-030: Space Boundaries and Topology](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-030-space-boundaries.md) · [RFC-IFC5-008: Relationship Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md)

<details>
<summary>IFCY delta</summary>

IFCY expresses space boundaries as a typed relation component. The boundary geometry is a separate entity carrying a `usd:MeshGeometry` component; the relationship component links space, element, and boundary geometry entity.

```json
{
  "type": "ifc:IfcRelSpaceBoundary",
  "entity": "<boundary-rel-uuid>",
  "attributes": {
    "relatingSpace":   { "ref": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6" },
    "relatedElement":  { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
    "boundaryGeometry": { "ref": "<boundary-geometry-entity-uuid>" }
  }
}
```


</details>

---

### 8.3. Openings and voids

Void geometry (e.g. window openings within a wall) is represented as a dedicated child node carrying body mesh and a `usd::usdgeom::visibility: invisible` flag on the type-level source node. Filling elements (window frames, glazing) are separate children of the type node inherited by occurrences. ⚠ Normative rules for opening/void/filling relationships are under discussion.

► [RFC-IFC5-026: Openings, Voids, and Fillings](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md) · [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md)

<details>
<summary>IFCY delta</summary>

IFCY makes void/filling relationships explicit typed relation components. There is no implicit geometry structure or visibility flag — the relationship type conveys the semantics.

```json
{
  "type": "ifc:IfcRelVoidsElement",
  "entity": "<void-rel-uuid>",
  "attributes": {
    "relatingBuildingElement": { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
    "relatedOpeningElement":   { "ref": "<opening-entity-uuid>" }
  }
}
```

```json
{
  "type": "ifc:IfcRelFillsElement",
  "entity": "<fill-rel-uuid>",
  "attributes": {
    "relatingOpeningElement": { "ref": "<opening-entity-uuid>" },
    "relatedBuildingElement": { "ref": "2c2d549f-f9fe-4e22-8590-562fda81a690" }
  }
}
```


</details>

---

## 9. Properties, Materials, and Classification

### 9.1. Flat property keys

IFC property set values are expressed as flat namespaced attribute keys on the node, not as nested property set objects. The convention is `bsi::ifc::prop::<PropertyName>`. Multiple properties may appear in one attributes block or across separate records for the same path.

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "bsi::ifc::prop::IsExternal": true,
    "bsi::ifc::prop::Volume":     2.783999976,
    "bsi::ifc::prop::Height":     3.0
  }
}
```

► [RFC-IFC5-013: Property Sets](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md) · [RFC-IFC5-023: Attribute Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md)

<details>
<summary>IFCY delta</summary>

Property data is attached via `IfcPropertySet` components. Each carries a `psetName` string and a `properties` map. Values use bare scalars for dimensionless properties and `{ value, unit }` objects for measured quantities. An entity may carry any number of `IfcPropertySet` components with different `psetName` values, directly mirroring IFC4.x pset semantics.

```json
{
  "type": "ifc:IfcPropertySet",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "psetName": "Pset_WallCommon",
    "properties": {
      "IsExternal": true,
      "Volume": { "value": 2.783999976, "unit": "m3" },
      "Height":  { "value": 3.0,         "unit": "m" }
    }
  }
}
```

→ [RFC-IFC5-013: Property Sets](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md), [RFC-IFC5-028: Units and Measures](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md)

</details>

---

### 9.2. Material node

Material definitions are expressed as standalone nodes carrying `bsi::ifc::material` (semantic identification), `bsi::ifc::presentation::diffuseColor`, `bsi::ifc::presentation::opacity`, and optionally material performance properties (`bsi::ifc-mat::prop::*`). Material nodes are not children of any building element; elements reference them via `inherits`.

```json
{
  "path": "7a187a90-3dcf-58cc-b3a6-51a9a407c55a",
  "attributes": {
    "bsi::ifc::material": {
      "code": "CONCRETE",
      "uri":  "https://identifier.buildingsmart.org/uri/fish/midas-materials/26/class/CONCRETE"
    },
    "bsi::ifc::presentation::diffuseColor": [0.5, 0.5, 0.5],
    "bsi::ifc::presentation::opacity": 1
  }
}
```

► [RFC-IFC5-017: Material Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) · [RFC-IFC5-029: Presentation and Appearance](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md)

<details>
<summary>IFCY delta</summary>

IFCY has no material node — a material is a first-class entity with its own UUID carrying multiple components. A material entity typically has an `ifc:<Material>Identity` component for semantic identification, an `ifc:IfcPresentationStyle` component for colour/opacity, and one or more `ifc:IfcPropertySet` components for performance data. There is no single `bsi::ifc::material` attribute key.

```json
{ "type": "ifc:IfcMaterialIdentity",      "entity": "7a187a90-...", "attributes": { "name": "Concrete", "taxonomy": { "ref": "https://identifier.buildingsmart.org/uri/fish/midas-materials/26/class/CONCRETE" } } },
{ "type": "ifc:IfcPresentationStyle",     "entity": "7a187a90-...", "attributes": { "diffuseColor": [0.5,0.5,0.5], "opacity": 1.0 } },
{ "type": "ifc:IfcPropertySet",           "entity": "7a187a90-...", "attributes": { "psetName": "Pset_MaterialCommon", "properties": { "MassDensity": { "value": 2400, "unit": "kg/m3" } } } }
```


</details>

---

### 9.3. Material assignment via `inherits`

Building elements reference their material node via the `inherits` map using the role key `"material"`. This allows the element to compositionally acquire the material's color, opacity, and semantic attributes.

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "inherits": { "material": "7a187a90-3dcf-58cc-b3a6-51a9a407c55a" }
}
```

► [RFC-IFC5-017: Material Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) · [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md)

<details>
<summary>IFCY delta</summary>

Material assignment is an explicit typed relation component. No `inherits` map entry is used.

```json
{
  "type": "ifc:IfcRelAssociatesMaterial",
  "entity": "<rel-uuid>",
  "attributes": {
    "relatedObjects":   [{ "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" }],
    "relatingMaterial": { "ref": "7a187a90-3dcf-58cc-b3a6-51a9a407c55a" }
  }
}
```

The material association is independently addressable and overridable — a different federation layer can replace it without touching the element entity itself.  

</details>

---

### 9.4. External classification

Non-IFC classification systems are attached to element nodes as namespace-qualified attributes, following the same `<registry>::<domain>::class` pattern. Each carries a `code` and a resolvable `uri`.

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "nlsfb::class": {
      "code": "21.21",
      "uri":  "https://identifier.buildingsmart.org/uri/nlsfb/nlsfb2005/2.2/class/21.21"
    }
  }
}
```

► [RFC-IFC5-027: Classification and External Dictionaries](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md) · [RFC-IFC5-035: Web and Linked-Data Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md)

<details>
<summary>IFCY delta</summary>

External classification references are consolidated into a `classifications` array on the entity's `ifc:<Type>Identity` component. Each entry carries `code`, `uri`, and `system`. This replaces all namespace-keyed classification attributes (`nlsfb::class`, etc.) with a single structured array.

```json
"classifications": [
  { "code": "21.21", "uri": "https://identifier.buildingsmart.org/uri/nlsfb/nlsfb/2020/class/21.21", "system": "NL-SfB" },
  { "code": "Ss_20_10_30", "uri": "https://uniclass.thenbs.com/...", "system": "Uniclass" }
]
```


</details>

---

### 9.5. Material performance data

Material-domain properties (LCA environmental indicators, structural, hygrothermal) are carried as `bsi::ifc-mat::prop::*` attributes on the material node. Compound values (e.g. lifecycle stage breakdown) are JSON objects with stage-code keys.

```json
{
  "path": "4549bada-a37e-5044-bb70-456516cca5a8",
  "attributes": {
    "bsi::ifc-mat::prop::StrengthClass":    "C24",
    "bsi::ifc-mat::prop::MoistureContent":  0.56,
    "bsi::ifc-mat::prop::MassDensity":      529.0,
    "bsi::ifc-mat::prop::GWP": {
      "A1-A3": -629.4, "A4": 0, "A5": 0,
      "C2": 1.802, "C3": 863, "D": -274.8
    }
  }
}
```

► [RFC-IFC5-017: Material Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) · [RFC-IFC5-028: Units and Measures](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md) · [RFC-IFC5-042: Alignment with External Domain Data Standards](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-042-external-domain-data-standards.md)

<details>
<summary>IFCY delta</summary>

IFCY carries material performance data as `ifc:IfcPropertySet` components attached to the material entity. The `psetName` follows IFC4.x conventions (e.g. `Pset_MaterialEnergy`, `Pset_MaterialMechanical`). Measured values use UCUM units; compound values (e.g. GWP by lifecycle stage) are nested JSON objects within `properties`.

```json
{
  "type": "ifc:IfcPropertySet",
  "entity": "4549bada-a37e-5044-bb70-456516cca5a8",
  "attributes": {
    "psetName": "Pset_MaterialCommon",
    "properties": {
      "MassDensity":    { "value": 529.0, "unit": "kg/m3" },
      "StrengthClass":  "C24",
      "GWP": { "A1-A3": { "value": -629.4, "unit": "kgCO2eq" }, "C3": { "value": 863, "unit": "kgCO2eq" } }
    }
  }
}
```


</details>

---

## 10. Presentation and Metadata

### 10.1. Color and opacity

Visual presentation is encoded as `bsi::ifc::presentation::diffuseColor` (RGB triple, each value 0.0–1.0) and `bsi::ifc::presentation::opacity` (0.0–1.0, where 1.0 is fully opaque). These may appear on element nodes directly or on material nodes (inherited by elements). ⚠ The normative relationship between element-level and material-level presentation attributes is under discussion.

```json
{
  "path": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6",
  "attributes": {
    "bsi::ifc::presentation::diffuseColor": [0.6, 0.7, 0.8],
    "bsi::ifc::presentation::opacity":      0.3
  }
}
```

► [RFC-IFC5-029: Presentation and Appearance](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md)

<details>
<summary>IFCY delta</summary>

Visual rendering properties are carried as a standalone `IfcPresentationStyle` component, not as attribute keys on the element or material node. Because it is a component, it can be overridden in a federated layer without touching geometry or identity. A visualization-only package may contain only `IfcPresentationStyle` components.

```json
{
  "type": "ifc:IfcPresentationStyle",
  "entity": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6",
  "attributes": {
    "diffuseColor": [0.6, 0.7, 0.8],
    "opacity":      0.3
  }
}
```

→ [RFC-IFC5-029: Presentation and Appearance](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md), [RFC-IFC5-032: Extensibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md)

</details>

---

### 10.2. STEP provenance traceability

To support round-tripping and audit of IFC4.x-to-IFCX conversions, each node converted from a STEP entity carries the original STEP line text as `customdata.originalStepInstance`. This field is informational and not expected to be parsed by IFCX consumers. Its schema is declared locally in the file's `schemas` block.

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "customdata": {
      "originalStepInstance": "#1222=IfcWall('2JUHrTM_j3UxZiBnyBfByx',$,'Wall',$,$,#1235,#1230,$,$)"
    }
  }
}
```

► [RFC-IFC5-031: Metadata and Custom Data](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md) · [RFC-IFC5-018: Backward Compatibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md)

<details>
<summary>IFCY delta</summary>

IFCY preserves STEP provenance as `legacyStepRef` directly on the `ifc:<Type>Identity` component's `attributes`, not in a separate `customdata` namespace. It requires no `schemas` block declaration; the field is part of the identity component schema.

```json
{
  "type": "ifc:IfcWallIdentity",
  "entity": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "attributes": {
    "name": "Wall",
    "legacyStepRef": "#1222=IfcWall('2JUHrTM_j3UxZiBnyBfByx',$,'Wall',$,$,#1235,#1230,$,$)"
  }
}
```


</details>

---

## 11. Composition and Federation

### 11.1. Layer federation

Multiple IFCX files are federated by merging their `schemas` dictionaries (by key) and concatenating their `data` arrays in layer order. The resulting unified layer set is then composed using the rules below. Federation is the mechanism for multi-party model assembly (e.g. structural engineer adding data to architect's model).

► [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) · [RFC-IFC5-033: Change, Transactions, and Collaboration](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md)

<details>
<summary>IFCY delta</summary>

Multiple IFCY packages are federated by concatenating their `data` arrays in layer order and merging their `schemas` prefix maps. There is no inherent conflict when packages add different-typed components to the same entity — each component type is an independent slot. Conflict arises only for same-type/same-entity components; last-writer-wins applies then. A structural engineer's package contributing `ifc:IfcPropertySet` components to entities already defined in an architect's geometry package produces no conflict.  

</details>

---

### 11.2. Conflict resolution — last-writer-wins

When multiple records for the same `path` contribute conflicting attribute values, the last record in document/layer order wins. This is the current alpha behavior (aligned with USD LIVRPS "Local" and "Referenced" semantics). ⚠ Whether this should be the normative rule or whether conflicts should surface for explicit consumer resolution is a critical open question.

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) · [RFC-IFC5-041: Open World vs. Closed World](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md)

<details>
<summary>IFCY delta</summary>

IFCY applies last-writer-wins at component-type granularity rather than attribute-key granularity. When two packages contribute components of the same `type` to the same `entity`, the later package's component replaces the earlier one in full. There is no partial-attribute merge between two components of the same type. ⚠ Whether this should be the normative rule is a critical open question shared with IFCX.  
→ [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md), [RFC-IFC5-041: Open World vs. Closed World](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md)

</details>

---

### 11.3. Null as deletion

A `null` value for a `children`, `inherits`, or `attributes` entry in a later layer signals deletion of that entry from the composed result. This enables targeted removal of graph edges or attribute values across layers without re-emitting the full node.

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) · [RFC-IFC5-033: Change, Transactions, and Collaboration](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md)

<details>
<summary>IFCY delta</summary>

IFCY signals component deletion by contributing a component with all-null `attributes`, or via an explicit tombstone mechanism. ⚠ The precise tombstone convention is not yet standardized — whether a null-attributes component, a dedicated `deleted: true` field, or a separate deletion record is the normative form remains open.  
→ [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md)

</details>

---

### 11.4. Composition expansion

After federation, a consumer may perform full composition expansion: resolving `inherits` arcs recursively to flatten each node into its full set of inherited and local attributes, children, and inherits. The expanded (flat) form is used for display and query but is not the canonical exchange form. Cycle detection over `inherits`/`children` graphs is required before expansion; cycles are invalid.

► [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) · [RFC-IFC5-040: Archetypes, Templates, and Override Mechanisms](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md)

<details>
<summary>IFCY delta</summary>

IFCY's equivalent of composition expansion is template resolution: expanding `ifc:IfcTypical` slots with `ifc:IfcInstantiates` instance overrides. The expanded form (`ifc:MaterialisedSnapshot` — see section 13) is explicitly marked as derived data, not authoritative. For extensibility, third parties define new component types under their own namespace prefix (e.g. `acme:AcousticRating`); conformant parsers must not fail on unknown types under the open-world assumption.  
→ [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md), [RFC-IFC5-032: Extensibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md)

</details>

---

## 12. Open Decision Register

The following decisions visible in `hello-wall.ifcx` are flagged ⚠ above and remain pending committee resolution. Each links to its primary RFC.

| # | Decision | RFC |
|---|---|---|
| 12.1 | Top-level key naming: unprefixed vs `ifcx::` prefixed | [RFC-IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) |
| 12.2 | Path as sole identity vs UUID + URI dual identity | [RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) |
| 12.3 | One-record-per-path vs additive patching as normative form | [RFC-IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) |
| 12.4 | `children`/`inherits` as normative relations vs explicit `IfcRel*` objects | [RFC-IFC5-008](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md) |
| 12.5 | Property key case: `UpperCamel` vs `lowerCamel` in `bsi::ifc::prop::*` | [RFC-IFC5-023](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md) |
| 12.6 | Last-writer-wins vs explicit conflict surfacing for multi-party authorship | [RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md) |
| 12.7 | USD-native geometry as normative vs IFC-native representation with USD as derived | [RFC-IFC5-014](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md), [RFC-IFC5-015](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) |
| 12.8 | Transform composition rule when entity appears in multiple spatial views | [RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) |

<details>
<summary>IFCY delta</summary>

IFCY carries ten additional open decisions beyond those shared with IFCX:

| IFCY # | Decision | RFC |
|--------|----------|-----|
| 14.1 | Normative confirmation that IFCY supersedes IFCX or that both coexist as separate profiles | [RFC-IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md), [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) |
| 14.2 | Multi-view consistency rules — can one element appear under two `SpatialView` roots? | [RFC-IFC5-016](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md) |
| 14.3 | Partial attribute override semantics within a Typical slot (merge vs. replace) | [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) |
| 14.4 | Normative slot naming registry for `componentTemplates` | [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) |
| 14.5 | Explicit tombstone mechanism for component deletion during federation | [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) |
| 14.6 | Snapshot freshness rules — normative staleness detection for `MaterialisedSnapshot` | [RFC-IFC5-033](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md) |
| 14.7 | Material layer set and constituent modeling conventions | [RFC-IFC5-017](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) |
| 14.8 | Parametric geometry extension path | [RFC-IFC5-014](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md) |
| 14.9 | Versioning strategy for minor vs. breaking changes to `ifcPackage` version string | [RFC-IFC5-022](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-022-versioning-schema-evolution.md) |
| 14.10 | Formal validation schema (JSONSchema or TypeSpec) for all `ifc:` component types | [RFC-IFC5-019](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-019-validation-framework.md) |

</details>

<details>
<summary>IFCY delta</summary>

These two sections exist only in IFCY and have no IFCX counterpart.

---

### IFCY §12 — Provenance and Trust

**12.1 — Package-level provenance.** The top-level `provenance` object applies to all components unless overridden. Fields: `assertedBy`, `assertedAt` (ISO 8601), `authority` (enum).

**12.2 — Component-level provenance override.** Any component may carry its own `provenance` object, overriding the package default for that component only. Used for mixed-authority packages (e.g. a survey measurement inside a design-intent package).

```json
{
  "type": "ifc:MaterialisedSnapshot", "entity": "2c2d549f-...",
  "attributes": { ... },
  "provenance": { "authority": "materialized-from", "derivedFrom": ["25503984-...", "2c2d549f-..."] }
}
```

**12.3 — `authority` enumeration.** Legal values: `design-intent` | `as-built` | `survey` | `inferred` | `ai-generated` | `materialized-from` | `regulatory` | `sensor`.

**12.4 — `derivedFrom` source list.** When `authority` is `materialized-from` or `inferred`, `derivedFrom` lists UUIDs of the source entities or components. Enables audit chains and cache invalidation.

→ [RFC-IFC5-037: Security and Trust](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-037-security-trust.md), [RFC-IFC5-036: AI and Machine-Readability](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md)

---

### IFCY §13 — Pre-Resolved Views: `ifc:MaterialisedSnapshot`

**13.1 — Purpose.** A pre-computed flat view of a Typical + instance combination, generated for AI and query consumers that cannot perform template expansion at read time. Carries `authority: "materialized-from"` and a `derivedFrom` source list.

```json
{
  "type": "ifc:MaterialisedSnapshot", "entity": "2c2d549f-f9fe-4e22-8590-562fda81a690",
  "attributes": {
    "resolvedFrom": "WT01", "resolvedAt": "2026-07-31T00:00:00Z",
    "snapshot": {
      "taxonomy": { "ref": "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/IfcWindow" },
      "IsExternal": true,
      "Height": { "value": 1.2, "unit": "m" },
      "Width":  { "value": 0.75, "unit": "m" }
    }
  },
  "provenance": { "authority": "materialized-from", "derivedFrom": ["25503984-...", "2c2d549f-..."] }
}
```

**13.2 — Snapshot is not authoritative.** A `MaterialisedSnapshot` is derived data. Consumers should prefer expanding templates from source components when possible.

**13.3 — `resolvedAt` timestamp.** Records when the snapshot was computed. Used for cache freshness assessment. ⚠ Normative freshness rules are under discussion.

→ [RFC-IFC5-036: AI and Machine-Readability](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md), [RFC-IFC5-040: Archetypes and Override Mechanisms](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md)

</details>

---

*This specification is a first-pass descriptive draft derived from `hello-wall.ifcx`, the TypeSpec schema in `schema/ifcx.tsp`, and the buildingSMART IFC5-development documentation. It records what the current alpha format does, not what the final IFC5 standard will require. All decisions marked ⚠ require committee resolution before normative language can be written.*
