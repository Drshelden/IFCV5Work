<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) · [📝 Google Doc](https://docs.google.com/document/d/11FX6NmvQ6RGb-1AvCd7FYvY5K1tuVrp9FXS7gTYNvKQ/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-012) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-012+%E2%80%94+&labels=IFC5-012&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdtibGrV_oKyf3l6yyQSpe9le11LI0onIbNTAbqGPbb_db4jw/viewform)


# RFC-IFC5-012: Modular Schema Imports

| Field | Value |
|---|---|
| **Decision ID** | IFC5-012 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-005, IFC5-011 |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFCX supports imported schema packages, but the URI syntax, package naming conventions, registry governance, offline resolution, version locking, and transitive dependency rules are not defined. Whether validation can proceed without resolving remote imports is also open.

## 2. Background

IFCX examples reference packages like `bsi/ifc` and `usd/usdgeom`. These URIs are not resolvable today. It is unclear whether a valid IFCX file must be self-contained or may depend on network-resolvable schemas.

## 3. Existing IFC4.x Convention

IFC4.x is self-contained. The schema is embedded in the IFC release; files declare their schema version in the header but do not import external packages.

## 4. Proposed Approaches

### 4.1 URN-based package references with a central registry

Schemas are identified by URNs (e.g., `urn:buildingsmart:ifc:1.0.0`). A central registry resolves URNs to schema documents. Offline operation requires a local cache.

### 4.2 URL-based imports with version pinning

Schemas are identified by HTTPS URLs with version in the path. Implementers may cache and vendor schemas. Validation may proceed offline with a local copy.

### 4.3 Embedded schemas only

IFC5 files must embed all schema definitions they use. No remote imports. Files are self-contained; no registry dependency. Increases file size.

### 4.4 Core schema is always present; extensions may be imported

The core IFC5 schema is bundled with every conformant implementation. Additional schemas (national extensions, domain modules, USD schemas) may be imported. Hybrid approach.

## 5. Tradeoffs

| Dimension | Central registry | URL imports | Embedded | Core + imports |
|---|---|---|---|---|
| Offline operation | Cache required | Cache required | Full | Partial |
| File self-containment | Low | Low | High | Moderate |
| Extension ecosystem | Full | Full | None | Partial |
| Governance complexity | High | Moderate | None | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Can an IFCX file be validated without resolving its imports (structural validation only)?

**Q2.** Who governs the `bsi::ifc` namespace and package? Is it a buildingSMART publication?

**Q3.** How are transitive imports and cyclic imports handled?

**Q4.** How are deprecated or replaced schema packages handled in existing files?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines how third-party and national extensions are managed
- Affects offline and air-gapped implementation scenarios
- Shapes versioning policy (IFC5-022)

## 10. References

- npm semantic versioning conventions
- OpenUSD USD schema registry


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) · [📝 Google Doc](https://docs.google.com/document/d/11FX6NmvQ6RGb-1AvCd7FYvY5K1tuVrp9FXS7gTYNvKQ/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-012) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-012+%E2%80%94+&labels=IFC5-012&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdtibGrV_oKyf3l6yyQSpe9le11LI0onIbNTAbqGPbb_db4jw/viewform)
