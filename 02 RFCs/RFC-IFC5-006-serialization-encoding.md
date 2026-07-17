
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-006](https://docs.google.com/forms/d/e/1FAIpQLSfNrJ2Rr1UxpaInpvpmB7uR3FikmwaDGpr5CAm6vyhZqgzbKw/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) · [📝 Google Doc](https://docs.google.com/document/d/1cpLHKgds-9VXgaxqZCOqKd0-_BBy3wIh6f3HNe73Xrg/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-006) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-006+%E2%80%94+&labels=IFC5-006&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfNrJ2Rr1UxpaInpvpmB7uR3FikmwaDGpr5CAm6vyhZqgzbKw/viewform)


# RFC-IFC5-006: Serialization and Encoding

| Field | Value |
|---|---|
| **Decision ID** | IFC5-006 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | IFC5-001 |
| **Prototype Required** | No |
| **Absorbs** | Topics 55 (IFCX fine-grained syntax), 56 (ECS fine-grained syntax), 57 (IFC-SPF fine-grained syntax) |

---

## 1. Problem Statement

IFC5 examples use JSON as the physical encoding. Many downstream decisions depend on the encoding model: whether binary alternatives are permitted, how large geometry arrays are handled, whether files may span multiple documents, and whether deterministic serialization is required for source control and content hashing.

## 2. Background

IFC4.x uses STEP Physical File (SPF), a compact text format. IFCX uses JSON. JSON is human-readable but verbose for large geometry arrays; binary JSON (BSON, MessagePack, CBOR) alternatives exist. OpenUSD uses both text (.usda) and binary (.usdc) encodings of the same model.

## 3. Existing IFC4.x Convention

Single-file STEP Physical File. ASCII with controlled character escaping. No streaming or binary geometry.

## 4. Proposed Approaches

### 4.1 JSON only

A single normative JSON encoding. Binary geometry may be embedded as Base64 or referenced by URI. Simple; no need for multiple parsers.

### 4.2 JSON + binary container

JSON for semantic data; binary format (e.g., glTF-style buffer) for large geometry arrays. Reduces file size. Requires a container format specification.

### 4.3 JSON text + binary JSON alternatives

JSON is the normative encoding; binary JSON alternatives (CBOR, MessagePack) are permitted for equivalent-semantic files. Requires a canonicalization rule.

### 4.4 Multi-file model

A logical IFC5 model may span multiple files (semantic data, geometry, type libraries). Requires federation and reference semantics (see IFC5-021).

## 5. Tradeoffs

| Dimension | JSON only | JSON + binary container | Binary JSON alternatives | Multi-file |
|---|---|---|---|---|
| Human readability | High | Partial | Low | Partial |
| File size | Large | Moderate | Small | Depends |
| Tooling complexity | Low | Moderate | High | High |
| Source control diff | Good | Poor | None | Good |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is deterministic/canonical JSON serialization required? (Needed for content hashing and source control.)

**Q2.** How should large numeric arrays (geometry vertex buffers) be handled in JSON?

**Q3.** Is `.ifcx` a single JSON file or may it be a package/container?

**Q4.** Are external geometry assets (e.g., a separate mesh file referenced by URI) normatively supported?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Affects geometry encoding decisions (IFC5-014)
- Affects streaming and performance considerations (related to scale topics)
- Determines document structure options (IFC5-011)

## 11. Absorbed Topics: Fine-Grained Syntax Decisions (Topics 55, 56, 57)

Topics 55, 56, and 57 of the source inventory enumerate detailed syntax questions for IFCX, ECS, and IFC-SPF respectively. These are not architectural decisions in their own right — they are the *implementation consequences* of decisions made in this RFC and in IFC5-007 (Scene Graph vs. ECS). Once the top-level encoding and structural decisions are resolved, the fine-grained syntax questions below become specification-writing work rather than committee decisions.

Key questions that remain open and should be resolved as part of this RFC's acceptance:

**IFCX syntax (Topic 55):**
- Why is `data` an array rather than an object indexed by path? (Affects streaming; see Q3 above)
- Are multiple entries for one path intentional (layered authoring) or an error?
- Must child-map values be paths, or may they be inline objects?
- May qualified attribute names contain `::` as nested keys?

**ECS syntax (Topic 56):**
- Is `entityType` redundant with `componentType` suffix conventions?
- Why do relationship components use string GUID references rather than typed references?
- Why do inline nested components require (or not require) GUIDs?

**IFC-SPF syntax (Topic 57):**
These are reference questions for backward compatibility analysis and are fully addressed in IFC5-018. No new decisions needed here.

## 10. References

- glTF binary buffer specification
- CBOR: RFC 8949
- JSON Canonicalization Scheme: RFC 8785


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) · [📝 Google Doc](https://docs.google.com/document/d/1cpLHKgds-9VXgaxqZCOqKd0-_BBy3wIh6f3HNe73Xrg/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-006) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-006+%E2%80%94+&labels=IFC5-006&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfNrJ2Rr1UxpaInpvpmB7uR3FikmwaDGpr5CAm6vyhZqgzbKw/viewform)
