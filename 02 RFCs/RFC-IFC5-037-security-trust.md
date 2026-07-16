# RFC-IFC5-037: Security and Trust

| Field | Value |
|---|---|
| **Decision ID** | IFC5-037 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-012, IFC5-021 |
| **Prototype Required** | No |
| **Source Topics** | Topic 51 |

---

## 1. Problem Statement

IFC5's schema import mechanism introduces remote network dependencies. Malicious or tampered schema packages, URI spoofing, recursive imports, and oversized arrays are attack vectors that do not exist in self-contained IFC4.x files. Security considerations must inform — not just follow — the design of schema imports, federation, and custom data.

Critical infrastructure (hospitals, transportation, utilities) is a primary IFC domain. Security is not optional.

## 2. Background

If an IFC5 file imports schemas from remote URIs, a receiving validator must either trust those URIs or refuse to process the file. A compromised schema registry could cause all validators globally to interpret files incorrectly. Additionally, if IFC5 supports procedural or executable schema constructs, these could be used as vectors for arbitrary code execution in validation engines.

## 3. Existing IFC4.x Convention

- Self-contained; no remote imports
- No executable constructs
- No digital signature mechanism
- No formal security threat model

## 4. Proposed Approaches

### 4.1 Schema integrity via content hashing

Schema imports include a content hash. Validators verify the hash before using a schema. A schema registry tamper is detectable immediately.

### 4.2 Trusted schema allowlist

Validators maintain a local allowlist of trusted schema URIs and their hashes. Files that import unlisted schemas require explicit user approval. Sandboxed validation by default.

### 4.3 Digital signatures on files and schemas

IFC5 files and schema packages support optional digital signatures. Signed files carry authorship provenance. Chain of custody is verifiable. Requires a PKI infrastructure.

### 4.4 No remote imports in core; extensions are local packages

Core IFC5 schema is always bundled with the validator. Extensions are distributed as signed local packages, not resolved at runtime from remote URIs. Eliminates the remote-import attack surface.

## 5. Tradeoffs

| Dimension | Content hashing | Allowlist | Digital signatures | No remote imports |
|---|---|---|---|---|
| Attack surface | Reduced | Low | Low | Eliminated |
| Extension ecosystem flexibility | Full | Limited | Full | Low |
| Infrastructure requirement | Registry | Local cache | PKI | None |
| Implementer complexity | Low | Low | High | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must IFC5 validators sandbox schema evaluation to prevent execution of malicious constructs?

**Q2.** Is digital signature support normative or optional?

**Q3.** How should classified or sensitive model data (government, defense, critical infrastructure) be handled?

**Q4.** Who is responsible for maintaining the integrity of the buildingSMART schema registry?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Directly shapes schema import design (IFC5-012)
- Informs federation security (IFC5-021)
- May constrain extensibility (IFC5-032)

## 10. References

- OWASP: Remote code execution via deserialization
- W3C Content Security Policy
- npm package integrity (lock files, signatures)
