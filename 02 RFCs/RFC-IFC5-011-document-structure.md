<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1LM9cJnGC5qzvMQp0CFyo3IHYC0Z7-dj9klj731rZr1c/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-011">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-011+%E2%80%94+&labels=IFC5-011&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSfMUZKudBZic01L7R1DZq8uZul7KRUu2O8kA-gyNyhZLXVwSQ/viewform">📋 Take the feedback form</a></td>
</tr></table>


# RFC-IFC5-011: Document-Level Structure

| Field | Value |
|---|---|
| **Decision ID** | IFC5-011 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-006 |
| **Prototype Required** | No |
| **Source Topics** | Topic 5 |

---

## 1. Problem Statement

The required and optional sections of an IFCX file — header, imports, schemas, data — are not formally specified. Key questions include what the header must contain, what sections are required, whether duplicate path records in the data array are additive or erroneous, and what ordering rules apply.

## 2. Background

IFCX examples contain a `data` array where multiple records may refer to the same path. Whether this is intentional (layered authoring) or a file error is not defined. In OpenUSD, multiple layers can contribute to the same prim via composition arcs — this may be analogous or may be a different mechanism.

## 3. Existing IFC4.x Convention

SPF has a fixed header (FILE_DESCRIPTION, FILE_NAME, FILE_SCHEMA) followed by DATA; section. There is no concept of layering or incremental contribution.

## 4. Proposed Approaches

### 4.1 Strict single-record-per-path

Each path may appear at most once in the data array. Duplicate paths are a validation error. Simple; clear.

### 4.2 Additive layering (USD-like)

Multiple records for the same path contribute additively. Later records override earlier ones for conflicting attributes. Enables incremental authoring, federation deltas, and discipline overlays.

### 4.3 Named layers with explicit merge semantics

Records belong to named layers (e.g., `{"layer": "structural", "path": "...", ...}`). Merge semantics are defined per layer. Most expressive; most complex.

## 5. Tradeoffs

| Dimension | Single record | Additive | Named layers |
|---|---|---|---|
| Simplicity | High | Moderate | Low |
| Federated authoring | No | Partial | Full |
| USD compatibility | No | Partial | High |
| Validation complexity | Low | Moderate | High |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** What is the minimum required header content for a valid IFCX file?

**Q2.** Are `imports`, `schemas`, and `data` all required sections, or may some be absent?

**Q3.** If multiple records contribute to one path, which attribute wins when there is a conflict?

**Q4.** Is the ordering of records within the data array semantically significant?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Affects how federation overlays are expressed (IFC5-021)
- Shapes schema import declarations (IFC5-012)

## 10. References

- OpenUSD layer specification
- IFCX Hello Wall example header structure


---

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-011) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-011+%E2%80%94+&labels=IFC5-011&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20link

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1LM9cJnGC5qzvMQp0CFyo3IHYC0Z7-dj9klj731rZr1c/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-011">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-011+%E2%80%94+&labels=IFC5-011&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSfMUZKudBZic01L7R1DZq8uZul7KRUu2O8kA-gyNyhZLXVwSQ/viewform">📋 Take the feedback form</a></td>
</tr></table>
