<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) · [📝 Google Doc](https://docs.google.com/document/d/1MFAP9A0iSM86mPFfmqwRDrhyER-1KAll1ZwJrmMVIoY/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-035) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-035+%E2%80%94+&labels=IFC5-035&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSczGfwBSTl1sp_TmAi2VSJ_UFku9FiXQe4yKsGZBN7dj3QPaQ/viewform)


# RFC-IFC5-035: Web and Linked-Data Alignment

| Field | Value |
|---|---|
| **Decision ID** | IFC5-035 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-003, IFC5-005 |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFC4.x has no formal linked-data alignment. The IFC ontology (ifcOWL) exists as a community effort but is not normative. IFCX's `code`/`uri` pattern and namespace system open the possibility of linked-data-compatible IFC5. This RFC asks how far IFC5 should go: is it URI-aware, JSON-LD compatible, or explicitly a linked-data format?

## 2. Background

JSON-LD can make any JSON document linked-data-compatible by adding an `@context` that maps keys to URIs. IFC5's `::` namespace system bears structural similarity to JSON-LD prefixes. The bSDD URI pattern already provides persistent identifiers for IFC classes and properties. A small design commitment now could enable SPARQL queries over IFC5 data without a separate RDF conversion step.

## 3. Existing IFC4.x Convention

- No linked-data alignment in the standard
- ifcOWL: community-driven RDF mapping (not normative)
- IFC SPARQL queries require conversion via external tools

## 4. Proposed Approaches

### 4.1 URI-aware but not linked-data-native

IFC5 uses URIs as identifiers (code/URI pairs, namespace URIs) but is not a linked-data format. A separate, normative RDF mapping specification is published alongside IFC5.

### 4.2 JSON-LD compatible

IFC5 files include or reference a JSON-LD `@context` that maps IFC5 attributes to URIs. No changes to the core format needed; linked-data tooling works without conversion.

### 4.3 Explicit RDF representation as an alternative serialization

IFC5 defines a normative RDF/Turtle serialization alongside JSON. Both carry equivalent semantics. Implementers choose based on use case.

### 4.4 Full linked-data-first design

IFC5 is designed from the ground up as a linked-data format. Every object and attribute is a URI node in a graph. JSON is a serialization of the graph. Highest semantic web compatibility; highest complexity.

## 5. Tradeoffs

| Dimension | URI-aware | JSON-LD | RDF serialization | Linked-data-first |
|---|---|---|---|---|
| Semantic web integration | Low | High | High | Full |
| Implementation complexity | Low | Low | Moderate | High |
| File format simplicity | High | High | Moderate | Low |
| bSDD / vocabulary alignment | Partial | High | High | Full |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Can the `::` namespace system be mapped deterministically to IRIs without any additional design work?

**Q2.** Is JSON-LD `@context` compatibility a free benefit of the namespace system, or does it require explicit design choices?

**Q3.** Must the RDF mapping be normative (testable for conformance) or informative?

**Q4.** Are there use cases — web publishing, regulatory reporting, AI reasoning — that require linked-data compatibility as a hard requirement?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Tied to namespace and identity decisions (IFC5-003, IFC5-005)
- Informs classification encoding (IFC5-027)
- May constrain URI persistence requirements in versioning (IFC5-022)

## 10. References

- JSON-LD 1.1: https://www.w3.org/TR/json-ld11/
- ifcOWL: https://technical.buildingsmart.org/resources/ifcowl/
- bSDD URI patterns


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) · [📝 Google Doc](https://docs.google.com/document/d/1MFAP9A0iSM86mPFfmqwRDrhyER-1KAll1ZwJrmMVIoY/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-035) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-035+%E2%80%94+&labels=IFC5-035&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSczGfwBSTl1sp_TmAi2VSJ_UFku9FiXQe4yKsGZBN7dj3QPaQ/viewform)
