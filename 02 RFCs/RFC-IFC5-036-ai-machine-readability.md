# RFC-IFC5-036: AI and Machine-Readability

| Field | Value |
|---|---|
| **Decision ID** | IFC5-036 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-003, IFC5-007 |
| **Prototype Required** | No |
| **Source Topics** | Topic 50 |

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

IFC5 mandates named (not positional) attributes and explicit class declarations. This alone makes the format substantially more AI-readable without additional design work. This is a constraint on IFC5-007 and IFC5-023.

### 4.2 Explicit provenance and confidence metadata

IFC5 supports optional provenance fields (was this attribute authored, inferred, or machine-generated?) and confidence scores. Enables AI systems to distinguish authoritative from inferred data.

### 4.3 Normalized representation preferred over nested

Where format decisions are equivalent from an engineering standpoint, the normalized (flatter) representation is preferred because it is more consistent for training data and query systems.

### 4.4 AI readability as an explicit conformance profile

A named AI-readability profile defines which IFC5 features must be present for files intended for ML consumption: stable IDs, named attributes, semantic URIs, no embedding of binary blobs in semantic fields.

## 5. Tradeoffs

| Dimension | Named attrs baseline | Provenance metadata | Normalized pref | AI profile |
|---|---|---|---|---|
| Design effort | Low | Moderate | Low | Moderate |
| Authoring tool burden | Low | Optional | Low | Optional |
| AI system benefit | Foundational | High | High | High |
| File verbosity | None | Low–moderate | Low | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Should IFC5 explicitly distinguish machine-generated attributes (from AI tools, sensors, or simulation) from human-authored ones?

**Q2.** Are there specific IFC5 design choices — e.g., between scene graph and ECS, or between inline and external geometry — that make a material difference to AI use cases?

**Q3.** Is the graph extractability of IFC5 (for graph neural network use cases) a design constraint?

**Q4.** Should IFC5 include fields for semantic embeddings or ML model references, or is this out of scope?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Provides additional design guidance for IFC5-007 (scene graph vs. ECS)
- Shapes provenance metadata decisions (IFC5-031)
- May reinforce normalization preferences in IFC5-013 (property sets)

## 10. References

- buildingSMART AI in BIM working group
- Graph neural networks on heterogeneous building graphs (literature)
- IFC-LLM tool use benchmarks
