<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md) · [📝 Google Doc](https://docs.google.com/document/d/1WmZ7ZGeDiwNXk7_YFr08mykSF_GpFg8ceKRnY67a1hI/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-032) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-032+%E2%80%94+&labels=IFC5-032&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLScjuMYfcujlbgWbA3xjFnLt3abeJghAYC0GyH0CgoOeWBKyVg/viewform)


# RFC-IFC5-032: Extensibility

| Field | Value |
|---|---|
| **Decision ID** | IFC5-032 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-012, IFC5-022 |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFC5 must define how the standard is extended: adding new classes, components, attributes, relationships, geometry schemas, domain modules, national extensions, and private organizational schemas. Without clear rules, extensions will fragment the ecosystem — vendors will create incompatible extensions, and receivers will not know how to handle unknown content.

## 2. Background

IFC4.x is extensible only via custom property sets and IfcRelAssociates. There is no mechanism for adding new entity types or relationships without a schema revision. This rigidity has driven vendors to embed application-specific data in strings and custom properties.

IFCX's schema import mechanism provides a natural extension point, but the governance rules for what may be extended, how extensions are named, and what receivers must do with unknown extensions are not defined.

## 3. Existing IFC4.x Convention

- Custom property sets (Pset_* by vendors)
- Custom classification references
- IfcDocumentReference for linked data
- No new entity types without schema revision

## 4. Proposed Approaches

### 4.1 Schema-package extensions

Extensions are distributed as schema packages (IFC5-012). Receivers that do not import the extension schema must preserve unrecognized namespaced attributes verbatim (unknown-extension preservation). Named governance process for promoting extensions to core.

### 4.2 Strict no-extension policy

Only buildingSMART-defined schemas are valid. Vendors use property sets for application data. Extensions require formal proposal and committee vote.

### 4.3 Open extension with compatibility class declaration

Files declare the extension packages they use. Receivers that do not support an extension may still process the file if it declares that the extension is optional (non-normative). Extensions that are required for correct interpretation are declared as mandatory.

### 4.4 Extension namespaces with stability guarantees

Any organization may define extension packages under their registered namespace. buildingSMART provides a stability guarantee only for `bsi::ifc::*`. Extensions under other namespaces carry no buildingSMART endorsement.

## 5. Tradeoffs

| Dimension | Schema packages | No extensions | Compatibility classes | Open namespaces |
|---|---|---|---|---|
| Ecosystem flexibility | High | Low | High | High |
| Fragmentation risk | Moderate | Low | Moderate | High |
| Unknown-extension safety | Yes (preserve) | N/A | Yes (flag) | Receiver-defined |
| Governance complexity | Moderate | Low | High | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must receivers preserve unrecognized namespaced attributes when round-tripping a file?

**Q2.** What happens if two extensions define conflicting semantics for the same attribute name?

**Q3.** How is a widely-adopted vendor extension promoted to buildingSMART core?

**Q4.** Can extensions redefine or override existing `bsi::ifc::*` attributes?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines schema import governance (IFC5-012)
- Shapes versioning policy for extensions (IFC5-022)
- Affects validation (IFC5-019) — how unknown extensions are treated

## 10. References

- OpenUSD applied API schema extension model
- buildingSMART proposal process


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md) · [📝 Google Doc](https://docs.google.com/document/d/1WmZ7ZGeDiwNXk7_YFr08mykSF_GpFg8ceKRnY67a1hI/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-032) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-032+%E2%80%94+&labels=IFC5-032&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLScjuMYfcujlbgWbA3xjFnLt3abeJghAYC0GyH0CgoOeWBKyVg/viewform)
