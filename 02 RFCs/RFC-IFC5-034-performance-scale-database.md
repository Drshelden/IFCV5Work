
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-034](https://docs.google.com/forms/d/e/1FAIpQLSdkwm4Zs0qXR5ceM9BQXvO4QcyUwy8UzZMoNjIVObIQFbMClA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-034-performance-scale-database.md) · [📝 Google Doc](https://docs.google.com/document/d/1h4VJRhfV_2vTEmLn870Abdwozyzu1rO9E0wYg0nMXos/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-034) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-034+%E2%80%94+&labels=IFC5-034&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdkwm4Zs0qXR5ceM9BQXvO4QcyUwy8UzZMoNjIVObIQFbMClA/viewform)


# RFC-IFC5-034: Performance, Scale, and Database Implications

| Field | Value |
|---|---|
| **Decision ID** | IFC5-034 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-006, IFC5-007 |
| **Prototype Required** | Yes |

---

## 1. Problem Statement

IFC5 is expected to support building-scale, city-scale, and infrastructure-scale models — potentially billions of objects. The physical encoding and structural organization of IFC5 files have direct implications for parsing performance, memory use, indexing strategies, streaming, and database ingestion. These requirements must inform (not be deferred after) the core format decisions.

## 2. Background

Large IFC4.x files (500MB+) are a known pain point. JSON is typically 3–5x larger than SPF for equivalent data, and slower to parse. ECS flat arrays are database-friendly; scene graphs require tree traversal. Neither IFCX nor ECS has been tested at city scale.

## 3. Existing IFC4.x Convention

- Single-file STEP Physical File; no streaming
- No pagination or chunked loading
- No database-native format

## 4. Proposed Approaches

### 4.1 Streaming-first design with chunked JSON

The data array in IFCX is designed for streaming: records are independent and may be loaded incrementally. Path-indexed lookup is possible without loading the full file. Requires that records not depend on forward references within the stream.

### 4.2 Binary container with semantic JSON index

A binary container (like glTF) holds large geometry arrays in binary form alongside a compact JSON semantic index. Reduces file size and parse time for large models.

### 4.3 Database projection as a first-class output

IFC5 schema design explicitly considers database ingestion: every object has a stable key, every attribute is addressable, and the schema supports efficient component-type indexing. The flat ECS model is preferred for this reason.

### 4.4 Explicit scale profiles

IFC5 defines scale profiles: a building profile (current IFCX approach), a city/infrastructure profile (with spatial indexing), and a streaming/partial-load profile (for web delivery). Each has defined format constraints.

## 5. Tradeoffs

| Dimension | Streaming JSON | Binary container | DB projection | Scale profiles |
|---|---|---|---|---|
| Human readability | High | None | N/A | Mixed |
| Parse performance | Moderate | High | High | Mixed |
| Large geometry | Poor | Good | N/A | Mixed |
| Tooling complexity | Low | High | High | High |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** What is the target scale for IFC5 core? Building? Campus? City? Infrastructure corridor?

**Q2.** Is random access (load only the objects needed for a spatial query) a core requirement?

**Q3.** Must IFC5 support incremental updates (delta records) for live digital twin feeds?

**Q4.** What is the expected ratio of geometry data to semantic data in a typical IFC5 file, and does this justify a binary geometry container?

## 8. Prototype

- **Required:** Yes
- **Notes:** Benchmark JSON parsing of a large IFC4.x file converted to IFCX vs. a binary container approach. Report file size, parse time, and memory use.

## 9. Consequences

- Directly influences serialization choices (IFC5-006)
- Shapes ECS vs. scene-graph decision (IFC5-007) — ECS is more DB-friendly
- Informs geometry encoding (IFC5-014)

## 10. References

- glTF binary buffer benchmark data
- IFC4 large file performance studies
- ECS component indexing literature


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-034-performance-scale-database.md) · [📝 Google Doc](https://docs.google.com/document/d/1h4VJRhfV_2vTEmLn870Abdwozyzu1rO9E0wYg0nMXos/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-034) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-034+%E2%80%94+&labels=IFC5-034&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdkwm4Zs0qXR5ceM9BQXvO4QcyUwy8UzZMoNjIVObIQFbMClA/viewform)
