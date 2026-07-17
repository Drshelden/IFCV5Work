
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-031](https://docs.google.com/forms/d/e/1FAIpQLSekgF88F3gtZqPcW7pfhBchSdv203Gb1HpFRsWod7zNcKZGUg/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/10EzW4BT7lqSrIGS4c0iNMh1VqoIahPNvrFNhLmOJcd8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-031">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-031+%E2%80%94+&labels=IFC5-031&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSekgF88F3gtZqPcW7pfhBchSdv203Gb1HpFRsWod7zNcKZGUg/viewform">📋 Take the feedback form</a></td>
</tr></table>


# RFC-IFC5-031: Metadata and Custom Data

| Field | Value |
|---|---|
| **Decision ID** | IFC5-031 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-005, IFC5-011 |
| **Prototype Required** | No |
| **Source Topics** | Topic 38 |

---

## 1. Problem Statement

IFCX examples contain a `customdata` field used for application-specific metadata (e.g., `originalStepInstance`). The rules for custom data — whether it is schema-validated, whether it may affect semantics, namespace requirements, and what round-trip information it should carry — are not defined.

Without clear rules, custom data becomes a dumping ground that undermines interoperability.

## 2. Background

In IFCX Hello Wall, `customdata` carries the original SPF statement as a string. This is useful for lossless round-trip migration but raises questions: is this normative? Is it required? Can custom data be used for arbitrary application metadata? How large can it be?

## 3. Existing IFC4.x Convention

- No equivalent to custom data
- Application-specific data goes into custom property sets (Pset_*) or IfcPropertySet with user-defined names
- IfcDocumentReference for linked external documents
- OwnerHistory for authorship metadata

## 4. Proposed Approaches

### 4.1 Informative-only custom data, no semantic effect

`customdata` is explicitly non-normative. Validators ignore it. No namespace requirement. Applications may embed any data. Receivers may ignore it without loss of semantics.

### 4.2 Namespaced custom data with schema validation

Custom data must use a registered namespace. Schemas for custom data may be declared and imported. Validators may optionally check custom data against its schema.

### 4.3 Separate migration metadata section

A dedicated `migrationMetadata` section carries round-trip aids (original SPF statements, source IDs, conversion diagnostics). Distinct from application `customdata`. Both may coexist.

### 4.4 No custom data mechanism

Applications that need custom data use custom property sets (IFC5-013). No unstructured escape hatch. Cleaner but may force property set overhead for simple annotations.

## 5. Tradeoffs

| Dimension | Informative-only | Namespaced + schema | Separate migration | No custom data |
|---|---|---|---|---|
| Interoperability risk | Low (ignored) | Low (validated) | Low | None |
| Migration round-trip support | Partial | Partial | Full | None |
| File size risk | High | Moderate | Moderate | None |
| Application flexibility | Full | Constrained | Limited | None |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is the `originalStepInstance` pattern (embedding SPF source lines) recommended or merely permitted?

**Q2.** Must custom data namespaces be declared in the file imports?

**Q3.** Can custom data fields affect how a receiving application processes the object (i.e., have side effects)?

**Q4.** What are the privacy and security implications of embedding source application data in IFC5 files?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Affects backward compatibility migration strategy (IFC5-018)
- Shapes document structure conventions (IFC5-011)

## 10. References

- IFCX Hello Wall customdata examples
- USD customData namespace convention


---

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-031) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-031+%E2%80%94+&labels=IFC5-031&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/10EzW4BT7lqSrIGS4c0iNMh1VqoIahPNvrFNhLmOJcd8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-031">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-031+%E2%80%94+&labels=IFC5-031&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSekgF88F3gtZqPcW7pfhBchSdv203Gb1HpFRsWod7zNcKZGUg/viewform">📋 Take the feedback form</a></td>
</tr></table>
