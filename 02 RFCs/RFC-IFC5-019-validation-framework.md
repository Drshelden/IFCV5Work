
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-019](https://docs.google.com/forms/d/e/1FAIpQLScqz5ytIrUPbTnGf85fLBtWs_SwBJt4VoF3GxYGTpaK7RBvLw/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-019-validation-framework.md) · [📝 Google Doc](https://docs.google.com/document/d/1EUrBgq8I_UOFmk4eP2chhFRwmHLbklNVAWkATi_z9Sk/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-019) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-019+%E2%80%94+&labels=IFC5-019&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLScqz5ytIrUPbTnGf85fLBtWs_SwBJt4VoF3GxYGTpaK7RBvLw/viewform)


# RFC-IFC5-019: Validation Framework

| Field | Value |
|---|---|
| **Decision ID** | IFC5-019 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-002, IFC5-012 |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFC4.x has a well-defined validation stack (EXPRESS WHERE rules, UNIQUE rules, cardinality constraints, geometric validity). IFC5 must define an equivalent stack. The question is how validation layers are defined, what tooling supports them, and how EXPRESS WHERE rules are migrated.

## 2. Background

In IFC4.x, WHERE rules are compiled from EXPRESS and executed by validators. They encode domain constraints (e.g., "a wall must have at least one representation if it is placed"). In JSON-based IFC5, these rules cannot be expressed in JSON Schema and require a separate rule language.

IDS (Information Delivery Specification) is a buildingSMART standard for exchange requirements. Its relationship to IFC5 validation is not defined.

## 3. Existing IFC4.x Convention

- EXPRESS WHERE rules: field-level and entity-level constraints
- UNIQUE rules: uniqueness constraints within instances
- Cardinality constraints: SET [1:?] OF etc.
- Geometric validity: implementer agreements
- IDS: exchange requirement profiles (newer, not fully integrated with IFC4.x)

## 4. Proposed Approaches

### 4.1 Layered validation: JSON Schema + domain rule language

JSON Schema handles structural validation. A separate rule language (SHACL, Schematron, or custom) handles domain constraints (migrated WHERE rules). IDS handles exchange requirements.

### 4.2 JSON Schema only

All constraints expressed in JSON Schema. WHERE rules that cannot be expressed in JSON Schema are dropped or converted to informative guidance. Simplest tooling; loss of some constraints.

### 4.3 EXPRESS retained for normative constraints

EXPRESS WHERE rules are retained in a companion file. JSON validators call an EXPRESS engine. Highest fidelity; requires EXPRESS runtime.

### 4.4 Validation profiles

Validation is defined in tiers: (1) structural, (2) schema, (3) IFC semantic, (4) exchange requirement. Each tier has separate tooling and conformance certificates.

## 5. Tradeoffs

| Dimension | Layered | JSON Schema only | EXPRESS retained | Profiles |
|---|---|---|---|---|
| WHERE rule fidelity | High | Low | High | Moderate |
| Tooling accessibility | Moderate | High | Low | Moderate |
| IDS integration | Natural | Partial | Manual | Natural |
| Offline operation | Full | Full | Full | Full |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Can a file be declared "structurally valid" without schema validation? What is the minimum conformance level?

**Q2.** Which IFC4.x WHERE rules are genuinely necessary vs. artifacts of EXPRESS limitations?

**Q3.** How does IDS integrate with the IFC5 validation stack?

**Q4.** What is the machine-readable format for validation reports?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines schema formalism requirements (feeds back to IFC5-002)
- Shapes model view and exchange requirements (IFC5-020)
- Affects conformance testing (Topic 53)

## 10. References

- SHACL: https://www.w3.org/TR/shacl/
- IDS: https://github.com/buildingSMART/IDS
- JSON Schema: https://json-schema.org


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-019-validation-framework.md) · [📝 Google Doc](https://docs.google.com/document/d/1EUrBgq8I_UOFmk4eP2chhFRwmHLbklNVAWkATi_z9Sk/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-019) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-019+%E2%80%94+&labels=IFC5-019&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLScqz5ytIrUPbTnGf85fLBtWs_SwBJt4VoF3GxYGTpaK7RBvLw/viewform)
