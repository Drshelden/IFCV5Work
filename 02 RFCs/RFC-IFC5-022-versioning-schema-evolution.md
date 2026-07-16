<!-- rfc-links -->
> **IFC5-022 — Versioning and Schema Evolution** · Tier 4 — Governance
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-022) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-022+%E2%80%94+&labels=IFC5-022&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)

# RFC-IFC5-022: Versioning and Schema Evolution

| Field | Value |
|---|---|
| **Decision ID** | IFC5-022 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-012 |
| **Prototype Required** | No |
| **Source Topics** | Topic 44 |

---

## 1. Problem Statement

IFC5 must define how the file format version, the core schema version, and individual module versions are declared and resolved. It must also define which changes are breaking vs. non-breaking, how deprecated names are handled, and how long-term archival (50+ year) is supported.

## 2. Background

IFC4.x has a single schema version declared in the file header. There is no module versioning, no deprecation mechanism, and no formal compatibility policy. This has made IFC4.x → IFC4.3 migration difficult in practice.

## 3. Existing IFC4.x Convention

Single `ifcVersion` in the file header. No module versioning. Schema changes require a new major version.

## 4. Proposed Approaches

### 4.1 Semantic versioning for all components

File format, core schema, and each module follow semver (MAJOR.MINOR.PATCH). Breaking changes require a major version bump. Parsers declare which versions they support.

### 4.2 Single monotonic schema version

One version number for the entire IFC5 release. All modules advance together. Simpler governance; harder for incremental adoption.

### 4.3 Date-based versioning with stability windows

Schemas are versioned by release date. A defined stability window (e.g., 5 years) guarantees no breaking changes within a version. Suitable for long-lived archival files.

### 4.4 Immutable schema URIs + aliases

Once published, a schema URI is immutable. Aliases map deprecated names to their replacements. Old files are always valid against their original schema URI.

## 5. Tradeoffs

| Dimension | Semver | Monotonic | Date-based | Immutable URIs |
|---|---|---|---|---|
| Incremental adoption | High | Low | Moderate | High |
| Archival stability | Moderate | Low | High | High |
| Governance simplicity | Moderate | High | Moderate | Moderate |
| Mixed-version documents | Supported | Not supported | Constrained | Supported |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** What constitutes a breaking change in an IFC5 schema? (Adding a required attribute? Renaming a property? Removing a class?)

**Q2.** How long must deprecated schema URIs remain resolvable? (For archival purposes, potentially decades.)

**Q3.** Can a single IFC5 file contain data from multiple schema versions? (e.g., after a module is upgraded)

**Q4.** How does ISO standardization interact with semantic versioning? ISO versions are not continuous.

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines import URI stability (IFC5-012)
- Affects long-term archival conformance

## 10. References

- Semantic versioning: https://semver.org
- W3C versioning best practices
- ISO 10303 version history


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-022) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-022+%E2%80%94+&labels=IFC5-022&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
