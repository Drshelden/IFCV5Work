<!-- rfc-links -->
> **IFC5-012 — Modular Schema Imports** · Tier 2 — Core Architecture
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-012) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-012+%E2%80%94+&labels=IFC5-012)

# RFC-IFC5-012: Modular Schema Imports

| Field | Value |
|---|---|
| **Decision ID** | IFC5-012 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-005, IFC5-011 |
| **Prototype Required** | No |
| **Source Topics** | Topic 6 |

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

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-012) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-012+%E2%80%94+&labels=IFC5-012)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
