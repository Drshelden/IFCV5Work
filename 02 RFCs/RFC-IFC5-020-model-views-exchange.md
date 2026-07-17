
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-020](https://docs.google.com/forms/d/e/1FAIpQLSetCodkSRz0KLo7lwOBCVfgvFqG48GPZrVgfZG5KsKbe-v2oA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-020-model-views-exchange.md) · [📝 Google Doc](https://docs.google.com/document/d/1edUVoBse15mZfrUwG7WRrNSGzNLUudh7gcIPWMABYuU/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-020) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-020+%E2%80%94+&labels=IFC5-020&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSetCodkSRz0KLo7lwOBCVfgvFqG48GPZrVgfZG5KsKbe-v2oA/viewform)


# RFC-IFC5-020: Model Views and Exchange Requirements

| Field | Value |
|---|---|
| **Decision ID** | IFC5-020 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-019 |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFC4.x uses Model View Definitions (MVDs) to define subsets of the schema required for specific exchange use cases. IDS provides a newer, more accessible mechanism for the same purpose. IFC5 must decide whether MVDs continue, how IDS integrates, and whether IFC5 files declare their conformance profile.

## 2. Background

MVDs have been widely criticized for being overly complex to define and difficult to test. IDS is simpler and more accessible but less expressive. Neither fully addresses the challenge of discipline-specific profiles (structural, MEP, architectural) or lightweight visualization profiles.

## 3. Existing IFC4.x Convention

- MVDs defined by buildingSMART or certified implementers
- Validators test files against a specific MVD
- Certification is MVD-specific (e.g., IFC4 Reference View, IFC4 Design Transfer View)

## 4. Proposed Approaches

### 4.1 MVDs replaced by IDS + schema subsets

IDS becomes the primary mechanism for exchange requirements. Schema subsets define which modules are required for a profile. MVDs are not continued.

### 4.2 MVDs retained with IFC5 tooling

MVDs continue in IFC5 with modernized tooling. IDS is integrated as a machine-readable layer. Certification programs continue.

### 4.3 Profiles declared in files

IFC5 files declare their conformance profile in the header. Validators select the appropriate rule set based on the declared profile.

### 4.4 No formal profiles

Profiles are a deployment concern, not a format standard. Any IFC5 file is equally valid; exchange requirements are negotiated separately.

## 5. Tradeoffs

| Dimension | IDS replaces | MVDs retained | Profile declarations | No profiles |
|---|---|---|---|---|
| Certification continuity | Low | High | Moderate | None |
| Accessibility | High | Low | Moderate | High |
| Exchange requirement expressiveness | Moderate | High | TBD | None |
| Tooling complexity | Low | High | Moderate | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** What is the future of MVDs? Should IFC5 invest in modernizing them or replacing them?

**Q2.** How does an IFC5 file communicate which exchange requirements it satisfies?

**Q3.** Are discipline-specific profiles (structural, MEP, architectural, GIS) normatively defined in IFC5?

**Q4.** What is the minimum subset every IFC5 implementation must support?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines certification program continuity
- Shapes validation framework tooling requirements (IFC5-019)

## 10. References

- buildingSMART IDS: https://github.com/buildingSMART/IDS
- MVD database: https://mvdxml.org


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-020-model-views-exchange.md) · [📝 Google Doc](https://docs.google.com/document/d/1edUVoBse15mZfrUwG7WRrNSGzNLUudh7gcIPWMABYuU/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-020) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-020+%E2%80%94+&labels=IFC5-020&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSetCodkSRz0KLo7lwOBCVfgvFqG48GPZrVgfZG5KsKbe-v2oA/viewform)
