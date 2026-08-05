# IFCX Format Specification — Alpha Draft

**Version:** Alpha (ifcx_alpha)  
**Date:** 2026-08-05  
**Source repository:** [buildingSMART/IFC5-development](https://github.com/buildingSMART/IFC5-development)  
**Reference example:** `examples/Hello Wall/hello-wall.ifcx`  
**Schema:** `schema/ifcx.tsp` (TypeSpec) → `schema/out/ts/ifcx.d.ts` (generated TypeScript)  
**RFC repository:** [Drshelden/IFCV5Work](https://github.com/Drshelden/IFCV5Work/tree/master/02%20RFCs)
**Cross-reference:** [GitHub](https://github.com/Drshelden/IFCV5Work/blob/master/05%20Normative%20Specification/IFCX-Specification-v3clean.md) · Google Docs *(link generated on first `sync_and_push` — see `scripts/drive_index.json`)*  
**Companion (with IFCY deltas):** [GitHub](https://github.com/Drshelden/IFCV5Work/blob/master/05%20Normative%20Specification/IFCX-Specification-v3.md) · [Google Docs](https://docs.google.com/document/d/1VSnRbWFbItd6-dblo_by6QsI6HpOzylGQjFhQutD5Tc)  

> **Status note.** IFCX is in active architectural development. Decisions marked ⚠ are under active committee discussion; the behavior described reflects the current `hello-wall.ifcx` example and buildingSMART alpha conventions, not a finalized normative standard.

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

---

## 1. Guiding Principles

IFCX is a JSON-based scene graph exchange format for IFC5. Seven design principles govern every convention in this specification.

### 1.1. JSON as normative data substrate

<sub>💬 [Discuss §1.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A71.1%5D%20JSON%20as%20normative%20data%20substrate&body=%2A%2ASection%3A%2A%2A%20%C2%A71.1%20%E2%80%94%20JSON%20as%20normative%20data%20substrate%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

All IFC5 data is encoded as JSON. STEP Physical File (SPF/ISO-10303-21) is not the exchange format. JSON native types (boolean, number, string, array, object, null) are the canonical scalar primitives. See [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) and [RFC-IFC5-006: Serialization and Encoding](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md).

---

### 1.2. Scene graph composition model

<sub>💬 [Discuss §1.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A71.2%5D%20Scene%20graph%20composition%20model&body=%2A%2ASection%3A%2A%2A%20%C2%A71.2%20%E2%80%94%20Scene%20graph%20composition%20model%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

IFCX represents a model as a directed graph of nodes, each addressed by a path. Hierarchy, type composition, and override layering follow a scene graph composition model inspired by OpenUSD. This is explicitly not a flat ECS (Entity-Component-System) array. See [RFC-IFC5-007: Scene Graph vs. ECS vs. Hybrid Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md).

---

### 1.3. Path-addressed node identity

<sub>💬 [Discuss §1.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A71.3%5D%20Path-addressed%20node%20identity&body=%2A%2ASection%3A%2A%2A%20%C2%A71.3%20%E2%80%94%20Path-addressed%20node%20identity%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Every node is identified by a `path` field. In the current alpha, path values are UUID-like strings derived from IFC GlobalIds. The path simultaneously serves as stable identity and as the graph address at which attribute opinions accumulate. ⚠ Whether path should be the sole identity or one of several identity channels (alongside a separate UUID and URI) is under active discussion. See [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) and [RFC-IFC5-004: Path Model and Addressing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md).

---

### 1.4. Namespace-qualified attribute vocabulary

<sub>💬 [Discuss §1.4](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A71.4%5D%20Namespace-qualified%20attribute%20vocabulary&body=%2A%2ASection%3A%2A%2A%20%C2%A71.4%20%E2%80%94%20Namespace-qualified%20attribute%20vocabulary%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

All semantic attributes use `::` double-colon delimiters to express namespace hierarchy (e.g. `bsi::ifc::class`, `usd::usdgeom::mesh`). This enables multi-vocabulary layering on a single node without key collision. See [RFC-IFC5-005: Namespaces](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md) and [RFC-IFC5-023: Attribute Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md).

---

### 1.5. Modular schema imports

<sub>💬 [Discuss §1.5](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A71.5%5D%20Modular%20schema%20imports&body=%2A%2ASection%3A%2A%2A%20%C2%A71.5%20%E2%80%94%20Modular%20schema%20imports%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Vocabulary schemas are not embedded in full; they are referenced by URI. An IFCX file declares which external schema bundles it relies on via an `imports` array. This enables multiple domain vocabularies (IFC, USD, NL-SfB, materials) to coexist in one file without conflicts. See [RFC-IFC5-012: Modular Schema Imports](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) and [RFC-IFC5-032: Extensibility](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md).

---

### 1.6. Additive, layer-composable authoring

<sub>💬 [Discuss §1.6](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A71.6%5D%20Additive%2C%20layer-composable%20authoring&body=%2A%2ASection%3A%2A%2A%20%C2%A71.6%20%E2%80%94%20Additive%2C%20layer-composable%20authoring%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Multiple records in the `data` array may refer to the same `path`. Each such record contributes additional attributes, children, or inherits links. This additive-patching model supports layered authoring, federated model assembly, and incremental update without rewriting the full node. Null values signal deletion during composition. See [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) and [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md).

---

### 1.7. USD alignment for geometry and composition

<sub>💬 [Discuss §1.7](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A71.7%5D%20USD%20alignment%20for%20geometry%20and%20composition&body=%2A%2ASection%3A%2A%2A%20%C2%A71.7%20%E2%80%94%20USD%20alignment%20for%20geometry%20and%20composition%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Geometry payloads and scene composition semantics are directly aligned with OpenUSD conventions (`usd::usdgeom::*`, `usd::xformop`, layer stacks, LIVRPS composition). IFCX is not a USD file but borrows USD's scene graph model to support broad tooling interoperability. See [RFC-IFC5-015: OpenUSD Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) and [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md).

---

## 2. Document Structure

### 2.1. Top-level file envelope

<sub>💬 [Discuss §2.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A72.1%5D%20Top-level%20file%20envelope&body=%2A%2ASection%3A%2A%2A%20%C2%A72.1%20%E2%80%94%20Top-level%20file%20envelope%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 2.2. Header

<sub>💬 [Discuss §2.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A72.2%5D%20Header&body=%2A%2ASection%3A%2A%2A%20%C2%A72.2%20%E2%80%94%20Header%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 2.3. Imports

<sub>💬 [Discuss §2.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A72.3%5D%20Imports&body=%2A%2ASection%3A%2A%2A%20%C2%A72.3%20%E2%80%94%20Imports%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 2.4. Schemas

<sub>💬 [Discuss §2.4](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A72.4%5D%20Schemas&body=%2A%2ASection%3A%2A%2A%20%C2%A72.4%20%E2%80%94%20Schemas%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 2.5. Data array

<sub>💬 [Discuss §2.5](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A72.5%5D%20Data%20array&body=%2A%2ASection%3A%2A%2A%20%C2%A72.5%20%E2%80%94%20Data%20array%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

`data` is an ordered JSON array of node records (`IfcxNode[]`). The array is the entire semantic payload of the file. Multiple records may share the same `path` value; they are composed additively in document order.

---

## 3. Identity and Addressing

### 3.1. Path field as node identity

<sub>💬 [Discuss §3.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A73.1%5D%20Path%20field%20as%20node%20identity&body=%2A%2ASection%3A%2A%2A%20%C2%A73.1%20%E2%80%94%20Path%20field%20as%20node%20identity%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Every node record has exactly one `path` field. The path is the stable, globally unique identifier of the node. It is both the node's canonical name and the address at which attribute contributions accumulate across records and layers.

```json
{ "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b", ... }
```

► [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) · [RFC-IFC5-004: Path Model and Addressing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md)

---

### 3.2. UUID-valued paths

<sub>💬 [Discuss §3.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A73.2%5D%20UUID-valued%20paths&body=%2A%2ASection%3A%2A%2A%20%C2%A73.2%20%E2%80%94%20UUID-valued%20paths%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

In `hello-wall.ifcx`, all path values are UUID-like strings (RFC 4122 format) derived deterministically from IFC GlobalIds via a GUID-expansion algorithm. STEP instance numbers (e.g. `#1222`) are not used as node addresses; they are preserved only as provenance metadata. ⚠ Whether IFC GlobalId, UUID v4/v5, URI, or a combination is the normative identity carrier is under active committee discussion.

```json
{ "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" }
```
*Derived from IFC GlobalId `2JUHrTM_j3UxZiBnyBfByx` (IfcWall).*

► [RFC-IFC5-003: Identity Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) · [RFC-IFC5-001: Strategic Architecture Mode](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md)

---

### 3.3. Human-readable child edge labels

<sub>💬 [Discuss §3.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A73.3%5D%20Human-readable%20child%20edge%20labels&body=%2A%2ASection%3A%2A%2A%20%C2%A73.3%20%E2%80%94%20Human-readable%20child%20edge%20labels%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

## 4. Graph Primitives

### 4.1. Node record structure

<sub>💬 [Discuss §4.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A74.1%5D%20Node%20record%20structure&body=%2A%2ASection%3A%2A%2A%20%C2%A74.1%20%E2%80%94%20Node%20record%20structure%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 4.2. `children` — containment and aggregation

<sub>💬 [Discuss §4.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A74.2%5D%20%60children%60%20%E2%80%94%20containment%20and%20aggregation&body=%2A%2ASection%3A%2A%2A%20%C2%A74.2%20%E2%80%94%20%60children%60%20%E2%80%94%20containment%20and%20aggregation%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 4.3. `inherits` — type-occurrence composition

<sub>💬 [Discuss §4.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A74.3%5D%20%60inherits%60%20%E2%80%94%20type-occurrence%20composition&body=%2A%2ASection%3A%2A%2A%20%C2%A74.3%20%E2%80%94%20%60inherits%60%20%E2%80%94%20type-occurrence%20composition%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 4.4. Additive patching — multiple records per path

<sub>💬 [Discuss §4.4](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A74.4%5D%20Additive%20patching%20%E2%80%94%20multiple%20records%20per%20path&body=%2A%2ASection%3A%2A%2A%20%C2%A74.4%20%E2%80%94%20Additive%20patching%20%E2%80%94%20multiple%20records%20per%20path%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Multiple records in `data` may share the same `path`. Each record contributes its `children`, `inherits`, and `attributes` content additively. This is the primary mechanism for separating concerns (geometry, classification, properties, provenance) across logical layers in a single file. ⚠ Whether this is the normative exchange model or whether one-record-per-path should be required is under committee review.

```json
{ "path": "93791d5d-...", "attributes": { "customdata": { "originalStepInstance": "..." } } },
{ "path": "93791d5d-...", "attributes": { "bsi::ifc::class": { "code": "IfcWall", ... } } },
{ "path": "93791d5d-...", "attributes": { "bsi::ifc::prop::IsExternal": true } },
{ "path": "93791d5d-...", "inherits": { "material": "7a187a90-..." } }
```

*Four separate records, all contributing to the same Wall node.*

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) · [RFC-IFC5-033: Change, Transactions, and Collaboration](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md)

---

## 5. Type System and Class Identity

### 5.1. IFC class declaration

<sub>💬 [Discuss §5.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A75.1%5D%20IFC%20class%20declaration&body=%2A%2ASection%3A%2A%2A%20%C2%A75.1%20%E2%80%94%20IFC%20class%20declaration%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 5.2. Type node geometry sharing

<sub>💬 [Discuss §5.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A75.2%5D%20Type%20node%20geometry%20sharing&body=%2A%2ASection%3A%2A%2A%20%C2%A75.2%20%E2%80%94%20Type%20node%20geometry%20sharing%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

When multiple occurrences share geometry (e.g. two identical windows), the geometry is placed once on a shared type node. Occurrence nodes inherit the type node via `inherits`, acquiring its geometry without duplication. Occurrences may carry a local `usd::xformop` to place themselves.

```json
{ "path": "25503984-...",  "children": { "Void": "...", "Frame": "...", "Glazing": "..." } },
{ "path": "2c2d549f-...", "inherits": { "windowType": "25503984-..." } },
{ "path": "592504dc-...", "inherits": { "windowType": "25503984-..." } }
```

*Type node `25503984-…` holds window sub-geometry. Both window occurrences inherit it.*

► [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) · [RFC-IFC5-040: Archetypes, Templates, and Override Mechanisms](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md)

---

### 5.3. Type-level named properties

<sub>💬 [Discuss §5.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A75.3%5D%20Type-level%20named%20properties&body=%2A%2ASection%3A%2A%2A%20%C2%A75.3%20%E2%80%94%20Type-level%20named%20properties%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

## 6. Attribute Conventions

### 6.1. Namespace `::` syntax

<sub>💬 [Discuss §6.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A76.1%5D%20Namespace%20%60%3A%3A%60%20syntax&body=%2A%2ASection%3A%2A%2A%20%C2%A76.1%20%E2%80%94%20Namespace%20%60%3A%3A%60%20syntax%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 6.2. Scalar value encoding

<sub>💬 [Discuss §6.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A76.2%5D%20Scalar%20value%20encoding&body=%2A%2ASection%3A%2A%2A%20%C2%A76.2%20%E2%80%94%20Scalar%20value%20encoding%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Scalar values are encoded directly as JSON native types. IFC typed wrappers from STEP (e.g. `IfcBoolean`, `IfcReal`, `IfcLabel`) are not present in attribute values. Booleans are `true`/`false`, numerics are JSON numbers, strings are JSON strings.

```json
"bsi::ifc::prop::IsExternal": true,
"bsi::ifc::prop::Volume":     2.783999976,
"bsi::ifc::prop::Height":     3.0
```

► [RFC-IFC5-024: Type System and Primitives](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-024-type-system-primitives.md) · [RFC-IFC5-028: Units and Measures](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md)

---

### 6.3. Object-valued attributes

<sub>💬 [Discuss §6.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A76.3%5D%20Object-valued%20attributes&body=%2A%2ASection%3A%2A%2A%20%C2%A76.3%20%E2%80%94%20Object-valued%20attributes%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

<sub>💬 [Discuss §6.4](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A76.4%5D%20Reference%20values&body=%2A%2ASection%3A%2A%2A%20%C2%A76.4%20%E2%80%94%20Reference%20values%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Cross-node references within attributes (e.g. in relationship objects) use a `{ "ref": "<path>" }` wrapper. This distinguishes a reference-to-node from an inline string value.

```json
"bsi::ifc::spaceBoundary": {
  "relatedelement": { "ref": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b" },
  "relatingspace":  { "ref": "e3035b71-bd9f-4cdc-86fd-b56e2f4605b6" }
}
```

► [RFC-IFC5-023: Attribute Representation](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md) · [RFC-IFC5-039: Foundational JSON Data Model](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md)

---

## 7. Geometry

### 7.1. USD geometry alignment

<sub>💬 [Discuss §7.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A77.1%5D%20USD%20geometry%20alignment&body=%2A%2ASection%3A%2A%2A%20%C2%A77.1%20%E2%80%94%20USD%20geometry%20alignment%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Geometry payloads are expressed using USD schema key conventions. IFCX does not define its own geometry vocabulary; it adopts `usd::usdgeom::*` attribute namespaces and the associated data shapes from OpenUSD. All geometry is currently tessellated to mesh and polyline primitives; parametric/BRep geometry is out of scope for the alpha.

► [RFC-IFC5-015: OpenUSD Alignment](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) · [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md)

---

### 7.2. Triangulated mesh

<sub>💬 [Discuss §7.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A77.2%5D%20Triangulated%20mesh&body=%2A%2ASection%3A%2A%2A%20%C2%A77.2%20%E2%80%94%20Triangulated%20mesh%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 7.3. Basis curves

<sub>💬 [Discuss §7.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A77.3%5D%20Basis%20curves&body=%2A%2ASection%3A%2A%2A%20%C2%A77.3%20%E2%80%94%20Basis%20curves%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 7.4. Transform (placement)

<sub>💬 [Discuss §7.4](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A77.4%5D%20Transform%20%28placement%29&body=%2A%2ASection%3A%2A%2A%20%C2%A77.4%20%E2%80%94%20Transform%20%28placement%29%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 7.5. Visibility

<sub>💬 [Discuss §7.5](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A77.5%5D%20Visibility&body=%2A%2ASection%3A%2A%2A%20%C2%A77.5%20%E2%80%94%20Visibility%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

## 8. Spatial Structure and Relationships

### 8.1. Spatial hierarchy via `children`

<sub>💬 [Discuss §8.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A78.1%5D%20Spatial%20hierarchy%20via%20%60children%60&body=%2A%2ASection%3A%2A%2A%20%C2%A78.1%20%E2%80%94%20Spatial%20hierarchy%20via%20%60children%60%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

The IFC spatial hierarchy (Project → Site → Building → Storey → Space/Element) is expressed entirely through `children` maps. Each spatial container node lists its contained elements by name. This replaces IFC4.x `IfcRelAggregates` and `IfcRelContainedInSpatialStructure` for tree navigation.

```json
{ "path": "ab143723-...", "children": { "My_Project":  "14adb22b-..." } },
{ "path": "14adb22b-...", "children": { "My_Site":     "e0834921-..." } },
{ "path": "e0834921-...", "children": { "My_Building": "e84dc79e-..." } },
{ "path": "e84dc79e-...", "children": { "My_Storey":   "44af358b-..." } },
{ "path": "44af358b-...", "children": { "My_Space": "e3035b71-...", "Wall": "93791d5d-..." } }
```

► [RFC-IFC5-016: Spatial Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md) · [RFC-IFC5-008: Relationship Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md)

---

### 8.2. Space boundaries

<sub>💬 [Discuss §8.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A78.2%5D%20Space%20boundaries&body=%2A%2ASection%3A%2A%2A%20%C2%A78.2%20%E2%80%94%20Space%20boundaries%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 8.3. Openings and voids

<sub>💬 [Discuss §8.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A78.3%5D%20Openings%20and%20voids&body=%2A%2ASection%3A%2A%2A%20%C2%A78.3%20%E2%80%94%20Openings%20and%20voids%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Void geometry (e.g. window openings within a wall) is represented as a dedicated child node carrying body mesh and a `usd::usdgeom::visibility: invisible` flag on the type-level source node. Filling elements (window frames, glazing) are separate children of the type node inherited by occurrences. ⚠ Normative rules for opening/void/filling relationships are under discussion.

► [RFC-IFC5-026: Openings, Voids, and Fillings](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md) · [RFC-IFC5-014: Geometry Architecture](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md)

---

## 9. Properties, Materials, and Classification

### 9.1. Flat property keys

<sub>💬 [Discuss §9.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A79.1%5D%20Flat%20property%20keys&body=%2A%2ASection%3A%2A%2A%20%C2%A79.1%20%E2%80%94%20Flat%20property%20keys%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 9.2. Material node

<sub>💬 [Discuss §9.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A79.2%5D%20Material%20node&body=%2A%2ASection%3A%2A%2A%20%C2%A79.2%20%E2%80%94%20Material%20node%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 9.3. Material assignment via `inherits`

<sub>💬 [Discuss §9.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A79.3%5D%20Material%20assignment%20via%20%60inherits%60&body=%2A%2ASection%3A%2A%2A%20%C2%A79.3%20%E2%80%94%20Material%20assignment%20via%20%60inherits%60%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Building elements reference their material node via the `inherits` map using the role key `"material"`. This allows the element to compositionally acquire the material's color, opacity, and semantic attributes.

```json
{
  "path": "93791d5d-5beb-437b-b8ec-2f1f0ba4bf3b",
  "inherits": { "material": "7a187a90-3dcf-58cc-b3a6-51a9a407c55a" }
}
```

► [RFC-IFC5-017: Material Modeling](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) · [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md)

---

### 9.4. External classification

<sub>💬 [Discuss §9.4](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A79.4%5D%20External%20classification&body=%2A%2ASection%3A%2A%2A%20%C2%A79.4%20%E2%80%94%20External%20classification%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 9.5. Material performance data

<sub>💬 [Discuss §9.5](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A79.5%5D%20Material%20performance%20data&body=%2A%2ASection%3A%2A%2A%20%C2%A79.5%20%E2%80%94%20Material%20performance%20data%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

## 10. Presentation and Metadata

### 10.1. Color and opacity

<sub>💬 [Discuss §10.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A710.1%5D%20Color%20and%20opacity&body=%2A%2ASection%3A%2A%2A%20%C2%A710.1%20%E2%80%94%20Color%20and%20opacity%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

### 10.2. STEP provenance traceability

<sub>💬 [Discuss §10.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A710.2%5D%20STEP%20provenance%20traceability&body=%2A%2ASection%3A%2A%2A%20%C2%A710.2%20%E2%80%94%20STEP%20provenance%20traceability%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

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

---

## 11. Composition and Federation

### 11.1. Layer federation

<sub>💬 [Discuss §11.1](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A711.1%5D%20Layer%20federation&body=%2A%2ASection%3A%2A%2A%20%C2%A711.1%20%E2%80%94%20Layer%20federation%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

Multiple IFCX files are federated by merging their `schemas` dictionaries (by key) and concatenating their `data` arrays in layer order. The resulting unified layer set is then composed using the rules below. Federation is the mechanism for multi-party model assembly (e.g. structural engineer adding data to architect's model).

► [RFC-IFC5-021: Federation and External References](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) · [RFC-IFC5-033: Change, Transactions, and Collaboration](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md)

---

### 11.2. Conflict resolution — last-writer-wins

<sub>💬 [Discuss §11.2](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A711.2%5D%20Conflict%20resolution%20%E2%80%94%20last-writer-wins&body=%2A%2ASection%3A%2A%2A%20%C2%A711.2%20%E2%80%94%20Conflict%20resolution%20%E2%80%94%20last-writer-wins%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

When multiple records for the same `path` contribute conflicting attribute values, the last record in document/layer order wins. This is the current alpha behavior (aligned with USD LIVRPS "Local" and "Referenced" semantics). ⚠ Whether this should be the normative rule or whether conflicts should surface for explicit consumer resolution is a critical open question.

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) · [RFC-IFC5-041: Open World vs. Closed World](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md)

---

### 11.3. Null as deletion

<sub>💬 [Discuss §11.3](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A711.3%5D%20Null%20as%20deletion&body=%2A%2ASection%3A%2A%2A%20%C2%A711.3%20%E2%80%94%20Null%20as%20deletion%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

A `null` value for a `children`, `inherits`, or `attributes` entry in a later layer signals deletion of that entry from the composed result. This enables targeted removal of graph edges or attribute values across layers without re-emitting the full node.

► [RFC-IFC5-011: Document-Level Structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) · [RFC-IFC5-033: Change, Transactions, and Collaboration](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md)

---

### 11.4. Composition expansion

<sub>💬 [Discuss §11.4](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BSpec%20%C2%A711.4%5D%20Composition%20expansion&body=%2A%2ASection%3A%2A%2A%20%C2%A711.4%20%E2%80%94%20Composition%20expansion%0A%0A%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20spec%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)</sub>

After federation, a consumer may perform full composition expansion: resolving `inherits` arcs recursively to flatten each node into its full set of inherited and local attributes, children, and inherits. The expanded (flat) form is used for display and query but is not the canonical exchange form. Cycle detection over `inherits`/`children` graphs is required before expansion; cycles are invalid.

► [RFC-IFC5-010: Composition, Inheritance, and Instancing](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) · [RFC-IFC5-040: Archetypes, Templates, and Override Mechanisms](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md)

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

---

*This specification is a first-pass descriptive draft derived from `hello-wall.ifcx`, the TypeSpec schema in `schema/ifcx.tsp`, and the buildingSMART IFC5-development documentation. It records what the current alpha format does, not what the final IFC5 standard will require. All decisions marked ⚠ require committee resolution before normative language can be written.*
