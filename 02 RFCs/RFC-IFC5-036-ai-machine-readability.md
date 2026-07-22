
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-036](https://docs.google.com/forms/d/e/1FAIpQLSdphGuPq8vyYNvh1YLuejkorRr4Bxs88coC-rsUSxJMJ-ifUA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md) · [📝 Google Doc](https://docs.google.com/document/d/1I7atBaHdbrheIUDJTehVsFAZe9lEmCUhkMstT1oWiVo/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-036) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-036+%E2%80%94+&labels=IFC5-036&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdphGuPq8vyYNvh1YLuejkorRr4Bxs88coC-rsUSxJMJ-ifUA/viewform)


# RFC-IFC5-036: AI and Machine-Readability

| Field | Value |
|---|---|
| **Decision ID** | IFC5-036 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | [IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md), [IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFC5 is being designed at a time when AI systems — language models, graph neural networks, scene understanding models — are becoming significant consumers of building data. Design choices that are neutral for human-authored tooling may meaningfully affect AI usability: explicit named attributes vs. positional, normalized vs. nested, stable identities, semantic URIs, and graph extractability all affect how easily AI systems can learn from and reason over IFC5 data.

This RFC asks the committee to explicitly consider AI readability as a design constraint, not an afterthought.

## 2. Background

IFC4.x's positional attributes, opaque STEP instance numbers, and deep inheritance hierarchy make it difficult for AI systems to extract consistent training data. IFCX's named attributes, namespaced semantics, and path-based identities are friendlier to machine learning. The ECS flat array is friendly to component-type queries. Neither has been designed with AI use cases as an explicit goal.

## 3. Existing IFC4.x Convention

- No AI considerations; format predates modern ML
- Positional attributes make schema-free interpretation impossible
- STEP instance numbers are opaque identifiers with no semantic content

## 4. Proposed Approaches

### 4.1 Named and typed attributes as a baseline requirement

IFC5 mandates named (not positional) attributes and explicit class declarations. This alone makes the format substantially more AI-readable without additional design work. This is a constraint on [IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) and [IFC5-023](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md).

### 4.2 Explicit provenance and confidence metadata

IFC5 supports optional provenance fields (was this attribute authored, inferred, or machine-generated?) and confidence scores. Enables AI systems to distinguish authoritative from inferred data.

### 4.3 Normalized representation preferred over nested

Where format decisions are equivalent from an engineering standpoint, the normalized (flatter) representation is preferred because it is more consistent for training data and query systems.

### 4.4 AI readability as an explicit conformance profile

A named AI-readability profile defines which IFC5 features must be present for files intended for ML consumption: stable IDs, named attributes, semantic URIs, no embedding of binary blobs in semantic fields.

### 4.5 Atomic data standard as the AI readability foundation

AI readability is most reliably achieved not through a separate profile, but through a foundational requirement on the data primitive itself: every object in IFC5 must be a **typed, named, uniquely identified dictionary**. Specifically:

- Every semantic object has a declared type (not inferred from position or context)
- Every attribute is named (not positional)
- Every object is uniquely identifiable by a stable ID (GUID, path, or URI) that is stable across exports
- Object relationships are expressed as references to those stable IDs, not by embedding

This is the "atomic data standard" concept described in [IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) and [IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md). From an AI perspective, this atomic standard means:
- Any IFC5 document can be parsed into a consistent `{id, type, attributes, references}` structure without schema knowledge
- Training datasets are consistent across different authors and tools
- Graph construction (for graph neural networks) requires only the reference links, not schema traversal

This approach argues that AI readability is not a profile to be layered on top — it is a consequence of correctly specifying the data model at the foundational level.

## 5. Tradeoffs

| Dimension | Named attrs baseline | Provenance metadata | Normalized pref | AI profile | Atomic data standard |
|---|---|---|---|---|---|
| Design effort | Low | Moderate | Low | Moderate | Low (if foundational) |
| Authoring tool burden | Low | Optional | Low | Optional | Low |
| AI system benefit | Foundational | High | High | High | Very high |
| File verbosity | None | Low–moderate | Low | Low | None |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Should IFC5 explicitly distinguish machine-generated attributes (from AI tools, sensors, or simulation) from human-authored ones?

**Q2.** Are there specific IFC5 design choices — e.g., between scene graph and ECS, or between inline and external geometry — that make a material difference to AI use cases? In particular: is a flat, normalized, component-oriented representation (ECS-style) intrinsically more AI-readable than a hierarchical scene graph?

**Q3.** Is the graph extractability of IFC5 (for graph neural network use cases) a design constraint?

**Q4.** Should IFC5 include fields for semantic embeddings or ML model references, or is this out of scope?

**Q5.** Should IFC5 specify a **minimal atomic data unit** — a typed, identified, reference-capable dictionary — as a requirement for the AI-readability conformance profile? Or is the atomic data standard ([IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md)) sufficient on its own, without a named AI profile?

**Q6.** If AI readability is achieved through the foundational data model (approach 4.5), what additional requirements — if any — does this RFC need to add beyond what [IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) and [IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) already specify? Is a separate AI-readability RFC necessary, or should its requirements be merged into the foundational RFCs?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Provides additional design guidance for [IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) (scene graph vs. ECS)
- Shapes provenance metadata decisions ([IFC5-031](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md))
- May reinforce normalization preferences in [IFC5-013](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md) (property sets)
- Closely linked to [IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) (foundational JSON data model) and [IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) (atomic data architecture requirement)

## 10. References

- buildingSMART AI in BIM working group
- Graph neural networks on heterogeneous building graphs (literature)
- IFC-LLM tool use benchmarks


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md) · [📝 Google Doc](https://docs.google.com/document/d/1I7atBaHdbrheIUDJTehVsFAZe9lEmCUhkMstT1oWiVo/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-036) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-036+%E2%80%94+&labels=IFC5-036&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdphGuPq8vyYNvh1YLuejkorRr4Bxs88coC-rsUSxJMJ-ifUA/viewform)
