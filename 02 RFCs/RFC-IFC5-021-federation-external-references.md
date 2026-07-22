
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-021](https://docs.google.com/forms/d/e/1FAIpQLSdFyH2DrLOlwTSqEqykXdQqSaoSBwNcfeSktvRsrPhvAGJAUQ/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) · [📝 Google Doc](https://docs.google.com/document/d/1ZMMBhS7-DWYhPxSYiTpZjN3b-rGOjyJLKbiurIyFFGc/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-021) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-021+%E2%80%94+&labels=IFC5-021&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdFyH2DrLOlwTSqEqykXdQqSaoSBwNcfeSktvRsrPhvAGJAUQ/viewform)


# RFC-IFC5-021: Federation and External References

| Field | Value |
|---|---|
| **Decision ID** | IFC5-021 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | [IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md), [IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) |
| **Prototype Required** | No |

---

## 1. Problem Statement

Large building projects require federated models: multiple IFC5 files contributed by different disciplines, combined into a single logical model. This requires defined URI schemes for cross-file references, identity reconciliation rules, and handling of unresolvable references. The federation model is not currently specified.

## 2. Background

IFC4.x has limited federation support (IfcExternalReference, coordination views). Real-world federation is typically achieved by model merge tools or proprietary platforms. IFCX's path model could enable USD-like layer composition for federation, but this is not specified.

## 3. Existing IFC4.x Convention

- IfcExternalReference: reference to an external source by location, name, and identifier
- No normative model federation mechanism
- Coordination views are MVD-specific conventions

## 4. Proposed Approaches

### 4.1 URI-based cross-file references

Objects in other files are referenced by URI (file path, URL, or URN) plus a path fragment. Receiving files may lazy-load or cache referenced files. Similar to USD references.

### 4.2 Global UUID references

Cross-file references use the target object's UUID. Receivers must index all available files to resolve. No file path coupling.

### 4.3 Federated layers (USD-style)

A root IFC5 file defines a layer stack. Each layer (file) contributes data to the merged model via USD-like composition semantics. Federation is a first-class document concept.

### 4.4 No normative federation

Federation is a deployment and tooling concern. IFC5 files are self-contained. Cross-file references are informative only.

## 5. Tradeoffs

| Dimension | URI references | UUID references | Federated layers | No federation |
|---|---|---|---|---|
| USD alignment | Moderate | Low | High | None |
| File location coupling | High | None | Moderate | N/A |
| Circular reference risk | Low | Moderate | High | None |
| Implementer complexity | Low | Moderate | High | None |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must federation be a normative IFC5 concept, or is it sufficient to define it in a companion specification?

**Q2.** How are identity conflicts resolved when two files define data for the same path or GUID?

**Q3.** How are federated inverse relationships (e.g., finding all spaces that reference a wall from another file) resolved?

**Q4.** What happens when a referenced file is unavailable? Is partial validation defined?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Depends on identity model decisions ([IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md), [IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md))
- Shapes document structure rules ([IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md))

## 10. References

- OpenUSD references and payloads documentation
- IFC4 IfcExternalReference


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) · [📝 Google Doc](https://docs.google.com/document/d/1ZMMBhS7-DWYhPxSYiTpZjN3b-rGOjyJLKbiurIyFFGc/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-021) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-021+%E2%80%94+&labels=IFC5-021&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdFyH2DrLOlwTSqEqykXdQqSaoSBwNcfeSktvRsrPhvAGJAUQ/viewform)
