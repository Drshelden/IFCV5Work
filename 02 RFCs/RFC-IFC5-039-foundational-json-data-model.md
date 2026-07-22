<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-039](https://docs.google.com/forms/d/e/1FAIpQLSdvcExxicOiWRRstyh3M4EthJP9mHM66R0T80qtgMLRl-zsTA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1UeUZC7WUz--oi0GdDxXH7_XTtAnqv1J6DoGvMeAeGXI/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-039) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-039+%E2%80%94+&labels=IFC5-039&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdvcExxicOiWRRstyh3M4EthJP9mHM66R0T80qtgMLRl-zsTA/viewform)


# RFC-IFC5-039: Foundational JSON Data Model — Primitives, Value vs. Reference, and the Component Primitive

| Field | Value |
|---|---|
| **Decision ID** | IFC5-039 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | [IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) |
| **Prototype Required** | No |
| **Logical position** | Tier 1 — between [IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) and [IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) |

---

## 1. Problem Statement

Both IFCX and IFC-ECS share a set of data-model assumptions that are treated as implicit rather than specified: JSON as the encoding substrate, nested combinations of arrays and dictionaries as the universal data primitive, a mechanism for encoding object references inline (by value) or by identifier (by reference), and a notion of a "component" as a fundamental dictionary that carries semantic data about an entity. These assumptions are not currently stated anywhere as normative constraints.

Leaving them implicit creates ambiguity: future serialization formats, binary encodings, or query languages may violate these assumptions without realizing it. It also prevents the committee from asking whether these assumptions are correct or whether alternatives exist.

This RFC proposes to make the foundational JSON data model explicit, declare what is normative and what is a default choice, and identify where international standards apply.

---

## 2. Background

Both current IFC5 proposals use JSON:

**IFCX** (from the buildingSMART IFC5-development repository):
```json
{
  "path": "/IfcProject/Site/Building/BuildingStorey/Wall",
  "attributes": {
    "ifc:Name": { "type": "IfcLabel", "value": "Wall-001" }
  },
  "children": { ... }
}
```

**IFC-ECS** (from the IFC-ECS repository):
```json
{
  "entityGuid": "14adb22b-d474-48a2-8e8f-6d4c067c1953",
  "componentGuid": "5e3f2a1c-...",
  "componentType": "IfcWallGeometry",
  "attributes": { ... }
}
```

Both use nested dicts and arrays. Both support pass-by-reference via `{"ref": "14adb22b-..."}` or path strings. Both treat a "component" as a dict with at least one identifying field and an `attributes` dict.

**JSON as a data model** (not just a syntax): JSON defines exactly five data types — null, boolean, number, string, array, and object (dictionary). All structured data in both proposals is built from these primitives. This is not an accident; it is a design choice with consequences for tooling, interoperability, and AI readability.

**International standards in this space:**
- **JSON Schema** (IETF draft): schema definition language for JSON documents
- **JSON-LD** (W3C): linked-data framing over JSON; adds `@context`, `@id`, `@type`
- **OData** (OASIS): REST-based data query and manipulation over JSON
- **JSON:API** (community standard): conventions for resource relationships in JSON APIs
- **CBOR** (RFC 7049): binary-compatible superset of JSON, same data model

None of these are currently referenced by either IFC5 proposal.

---

## 3. Existing IFC4.x Convention

IFC4.x uses STEP Physical File (SPF) encoding, which is not JSON-based. Its data primitives are:
- Positional attribute lists on entity instances
- Explicit EXPRESS typing
- `#N` instance references (opaque numeric handles)
- No native notion of a "component" — all semantics are carried by entity type hierarchies and explicit relationship instances

The shift to JSON represents a fundamental break from this convention, one that both current proposals make without explicitly justifying it.

---

## 4. Proposed Approaches

### 4.1 JSON as a normative baseline (default encoding)

IFC5 declares JSON as the normative baseline encoding. The data model is built from JSON primitives (null, boolean, number, string, array, object). Other encodings (CBOR, binary, Protobuf) are permitted as optional profiles but must preserve the JSON data model semantics and support lossless round-tripping to JSON.

This is consistent with both IFCX and IFC-ECS as currently proposed.

### 4.2 JSON as one of several co-equal encodings

IFC5 defines an abstract data model and provides normative bindings for JSON, CBOR, and IFC-SPF, each with equivalent status. No encoding is privileged. This preserves backward compatibility paths and future binary encoding options.

### 4.3 JSON-LD alignment

IFC5 adopts JSON-LD as the baseline, gaining `@context`-based namespace resolution, `@id`-based identity, and compatibility with RDF and the W3C Linked Data ecosystem. All IFC5 documents are valid JSON-LD. This strengthens the linked-data story (IFC5-035) and AI readability (IFC5-036) at the cost of mandatory `@context` declarations.

### 4.4 Abstract data model with JSON as the reference implementation

IFC5 defines an abstract object model (types, attributes, relationships, references) and provides a normative JSON serialization as the reference implementation. Conformance is tested against the abstract model, not the serialization. This is the most flexible approach but the most complex to specify.

---

## 5. Value vs. Reference Encoding

Both current proposals support two ways of including another object's data:

**Pass by value** — the full object dictionary is embedded inline:
```json
{
  "material": {
    "componentType": "IfcMaterial",
    "attributes": { "Name": "Concrete" }
  }
}
```

**Pass by reference** — a reference handle points to an object defined elsewhere:
```json
{
  "material": { "ref": "14adb22b-d474-48a2-8e8f-6d4c067c1953" }
}
```

The reference syntax (`{"ref": "..."}`) is not currently standardized. JSON-LD uses `{"@id": "..."}`. OData uses `{"@odata.id": "..."}`. The choice of reference syntax is a normative decision with interoperability implications.

**Questions for this section:**
- Should `{"ref": "..."}` be the normative reference syntax, or should IFC5 align with `{"@id": "..."}` (JSON-LD)?
- Is the reference handle always a GUID, or may it also be a path string (IFCX convention)?
- Must both pass-by-value and pass-by-reference be supported in all IFC5 profiles?

---

## 6. The Component Primitive

Both proposals converge on a notion of a "component" that is a dictionary containing:
1. An entity reference (GUID or path) — identifying which entity the component belongs to
2. Semantic attributes — the actual data payload
3. Optionally: a component identity (component-level GUID) and a component type

This convergence suggests the component is a foundational primitive, not an incidental implementation detail. Making it explicit would:
- Allow cross-profile component exchange
- Define minimum required fields for a valid component
- Allow tooling to process components without knowing the full architectural profile

**IFCX component structure (implicit):**
```json
{
  "path": "/Project/Site/Building/Wall",   ← entity reference (path-based)
  "attributes": { ... }                    ← semantic payload
}
```

**IFC-ECS component structure (explicit):**
```json
{
  "entityGuid": "14adb22b-...",            ← entity reference (GUID-based)
  "componentGuid": "5e3f2a1c-...",         ← component identity
  "componentType": "IfcWallGeometry",      ← component type
  "attributes": { ... }                    ← semantic payload
}
```

The structural fields differ. Whether a minimum common structure can be defined — while allowing both path-based and GUID-based entity references — is a key question for this RFC.

---

## 7. Tradeoffs

| Dimension | JSON normative baseline | JSON as one encoding | JSON-LD | Abstract model |
|---|---|---|---|---|
| Tooling simplicity | High | Low | Moderate | Low |
| Linked-data / AI alignment | Low | Low | High | High |
| Binary encoding path | Via CBOR | Direct | Via CBOR | Direct |
| IFC4.x community friction | Moderate | Low | High | Low |
| Specification effort | Low | High | Moderate | High |

---

## 8. Recommendation

*To be filled in after committee discussion.*

---

## 9. Open Questions

**Q1.** Should JSON (or a JSON-compatible data model) be declared as a normative baseline for IFC5, or should it be one of several equally valid encodings?

**Q2.** Should the pass-by-reference mechanism — e.g., `{"ref": "uuid"}` — be normatively defined at the foundational level, including the key name and the permitted types of reference handle (GUID, path, URI)?

**Q3.** Is the "component as a dictionary with at least one entity reference field and an attributes payload" a foundational architectural assumption that should be specified normatively, or is it an implementation pattern specific to one approach?

**Q4.** Are there international standards (JSON Schema, JSON-LD, OData, JSON:API, CBOR) that IFC5 should formally align with at the data primitive level? If so, which, and to what extent?

**Q5.** Should the foundational data model require that every component or data object be uniquely identifiable — by GUID, path, or URI — as a hard constraint? Or may anonymous inline structures exist?

**Q6.** Should a minimum required field set be defined for the "component primitive" — the shared structural concept present in both IFCX and IFC-ECS — so that cross-profile tools can process components without knowing the full architectural mode?

---

## 10. Prototype

- **Required:** No
- **Notes:** This is a definitional RFC. The relevant prototypes exist in the Hello Wall examples (03 Reference Examples/), which already demonstrate both component conventions. A prototype showing cross-profile component exchange would be valuable but is not required before committee discussion.

---

## 11. Consequences

This RFC, if adopted, directly shapes:
- Identity model (IFC5-003) — GUID vs path vs URI as canonical identifier
- Path model (IFC5-004) — whether path is an entity reference or a structural address
- Serialization (IFC5-006) — what JSON encoding is normative
- Scene graph vs. ECS (IFC5-007) — both share the component primitive; explicit definition enables cross-profile tooling
- Attribute representation (IFC5-023) — named attributes in JSON dicts
- Web and linked-data alignment (IFC5-035) — JSON-LD option
- AI readability (IFC5-036) — JSON data model is foundational for AI tooling

---

## 12. References

- IFCX Hello Wall: `03 Reference Examples/`
- IFC-ECS Hello Wall: `03 Reference Examples/`
- IETF JSON Schema: https://json-schema.org/
- W3C JSON-LD: https://www.w3.org/TR/json-ld/
- IETF CBOR (RFC 7049): https://datatracker.ietf.org/doc/html/rfc7049
- JSON:API: https://jsonapi.org/
- buildingSMART IFC5-development: https://github.com/buildingSMART/IFC5-development
- IFC-ECS: https://github.com/Drshelden/IFC-ECS


---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1UeUZC7WUz--oi0GdDxXH7_XTtAnqv1J6DoGvMeAeGXI/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-039) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-039+%E2%80%94+&labels=IFC5-039&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdvcExxicOiWRRstyh3M4EthJP9mHM66R0T80qtgMLRl-zsTA/viewform)
