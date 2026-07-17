
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-038](https://docs.google.com/forms/d/e/1FAIpQLSeQHDg8LRnUDxVzXeugPq7ER1T_i1tw3yqIuC_L2b409SXD1Q/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-038-governance-conformance.md) · [📝 Google Doc](https://docs.google.com/document/d/1GY-1oDXFIXhUoY1-3NbeZU4kiW6nXJDPy63wkjypZOw/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-038) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-038+%E2%80%94+&labels=IFC5-038&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeQHDg8LRnUDxVzXeugPq7ER1T_i1tw3yqIuC_L2b409SXD1Q/viewform)


# RFC-IFC5-038: Governance, Conformance, and Interoperability Testing

| Field | Value |
|---|---|
| **Decision ID** | IFC5-038 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-019, IFC5-020, IFC5-022 |
| **Prototype Required** | No |

---

## 1. Problem Statement

Who owns the IFC5 core namespaces? How are new modules approved? How does buildingSMART's governance interact with OpenUSD governance and bSDD governance? How is conformance tested and certified? These are not purely technical questions — they determine the long-term sustainability of the standard.

## 2. Background

IFC4.x governance is managed by buildingSMART through ISO 16739. Conformance testing is via certified software and MVD-specific validation. The buildingSMART certification program has been a key driver of IFC adoption. IFC5 introduces new complexity: schema imports, USD alignment, bSDD dependency, and a potential modular structure where different governance bodies may own different modules.

## 3. Existing IFC4.x Convention

- buildingSMART International owns the IFC standard
- ISO 16739 is the normative publication vehicle
- Certification program for software products
- MVD-specific conformance testing

## 4. Proposed Approaches

### 4.1 Centralized buildingSMART governance

buildingSMART governs all `bsi::*` namespaces and the core schema. Other namespaces (USD, national bodies) have their own governance. Cross-governance coordination via liaison agreements.

### 4.2 Modular governance with delegation

Core IFC5 (bsi::ifc::*) is buildingSMART-governed. USD schemas (usd::*) are ASWF/Pixar-governed. National body namespaces are nationally governed. A governance coordination council resolves conflicts.

### 4.3 Community governance (open source model)

IFC5 schemas are managed on GitHub with open contribution, version-tagged releases, and a technical steering committee. ISO normative publication is based on stable releases.

### 4.4 Conformance profiles replace certification

Instead of software certification, conformance is per-file: IFC5 files are validated against defined profiles (IFC5-020) and a conformance report is attached. No product certification required. Simpler; reduces buildingSMART gatekeeping role.

## 5. Tradeoffs

| Dimension | Centralized | Modular | Community | Profile conformance |
|---|---|---|---|---|
| Governance agility | Low | Moderate | High | High |
| Accountability | High | Distributed | Distributed | File-level |
| USD coordination complexity | High | Low | Low | N/A |
| ISO process compatibility | High | Moderate | Moderate | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** How does buildingSMART govern a standard that deliberately incorporates non-buildingSMART schemas (USD, bSDD)?

**Q2.** Can a software product be certified as "IFC5 conformant" when IFC5 has modular, optionally-imported schemas?

**Q3.** What is the minimum conformance test that every IFC5 implementation must pass — regardless of which modules it supports?

**Q4.** How does IFC5 conformance testing relate to the Hello Wall benchmark files?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Shapes how the buildingSMART IFC5 program is structured
- Determines who controls schema URI persistence (IFC5-022)
- Informs extensibility governance (IFC5-032)
- Shapes conformance test suite design (referenced in IFC5-019, IFC5-020)

## 10. References

- buildingSMART certification program
- ISO 16739 (IFC standard)
- ASWF governance model
- OpenUSD governance documentation


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-038-governance-conformance.md) · [📝 Google Doc](https://docs.google.com/document/d/1GY-1oDXFIXhUoY1-3NbeZU4kiW6nXJDPy63wkjypZOw/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-038) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-038+%E2%80%94+&labels=IFC5-038&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeQHDg8LRnUDxVzXeugPq7ER1T_i1tw3yqIuC_L2b409SXD1Q/viewform)
