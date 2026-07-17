<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1_omQbQt3gMyKGn8PJNoUU_k0YD6oasgNzmw9bCFWJb8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-033">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-033+%E2%80%94+&labels=IFC5-033&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSceA_5uPFIw55TVQHwCRtkMJjSmuyliVjQ_ooz9OyIfqSAjMw/viewform">📋 Take the feedback form</a></td>
</tr></table>


# RFC-IFC5-033: Change, Transactions, and Collaboration

| Field | Value |
|---|---|
| **Decision ID** | IFC5-033 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-003, IFC5-021 |
| **Prototype Required** | No |
| **Source Topics** | Topic 46 |

---

## 1. Problem Statement

Digital twin and collaborative BIM use cases require fine-grained change tracking: who changed what, when, at what level of granularity (object, attribute, component), and how conflicts between concurrent edits are resolved. IFC4.x has only OwnerHistory, which is coarse and widely ignored. IFC5 must decide how deeply change semantics are built into the format.

## 2. Background

In IFC4.x, OwnerHistory records the creating and modifying application and timestamp at the object level. There is no attribute-level change tracking, no merge semantics, and no conflict detection. Real-world collaborative BIM relies on proprietary platforms (Revit worksharing, BIM 360, etc.) for change management — not IFC.

If IFC5 adopts layered composition (IFC5-011), each layer naturally corresponds to a changeset. USD's layer stack model provides a precedent.

## 3. Existing IFC4.x Convention

- IfcOwnerHistory: creator, modifier, application, timestamps at object level
- No attribute-level change tracking
- No merge or conflict semantics

## 4. Proposed Approaches

### 4.1 OwnerHistory retained at object level

OwnerHistory-equivalent is preserved as a structured attribute on each object node. Coarse but backward compatible. No new change infrastructure.

### 4.2 Changeset layers (USD-inspired)

Each authored layer in the document stack is a named changeset with author, timestamp, and approval state. Changes are expressed as delta records in a layer. Merge is defined by layer ordering.

### 4.3 Attribute-level provenance metadata

Each attribute may carry optional provenance metadata (author, timestamp, source application). Fine-grained; verbose. Suitable for AI-generated or sensor-derived data.

### 4.4 No change semantics in core format

Change management is a platform concern. IFC5 files are snapshots. Change tracking systems (Git, CDE platforms) manage revisions externally.

## 5. Tradeoffs

| Dimension | OwnerHistory | Changeset layers | Attr provenance | No semantics |
|---|---|---|---|---|
| Collaborative authoring support | Low | High | High | None |
| USD layer compatibility | No | High | No | N/A |
| File verbosity | Low | Moderate | High | None |
| Platform independence | High | High | High | Full |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is attribute-level change tracking a core requirement, or is object-level sufficient?

**Q2.** Must IFC5 files be deterministically serializable (canonical output) to work with source control diffs?

**Q3.** How are deleted objects represented — tombstone records, omission, or explicit deletion flags?

**Q4.** How does the collaboration model interact with the federation model (IFC5-021)?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Ties to document structure (IFC5-011) if changeset layers are adopted
- Affects federation model (IFC5-021)
- Shapes serialization decisions (IFC5-006) — canonical/deterministic output

## 10. References

- USD layer stack and composition model
- IFC4 IfcOwnerHistory
- Git diff semantics for text-based formats


---

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-033) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-033+%E2%80%94+&labels=IFC5-033&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1_omQbQt3gMyKGn8PJNoUU_k0YD6oasgNzmw9bCFWJb8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-033">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-033+%E2%80%94+&labels=IFC5-033&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSceA_5uPFIw55TVQHwCRtkMJjSmuyliVjQ_ooz9OyIfqSAjMw/viewform">📋 Take the feedback form</a></td>
</tr></table>
