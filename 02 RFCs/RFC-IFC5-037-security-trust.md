
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-037](https://docs.google.com/forms/d/e/1FAIpQLSdeW1Q61ee060a_JKjT7KbrOTvlO5zIqMlHBmJjDFlMgNAxzQ/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-037-security-trust.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1CgbOv0ib8CfoosIcs7IUuwFpWWWTD2g6c828ku9xQgE/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-037">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-037+%E2%80%94+&labels=IFC5-037&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdeW1Q61ee060a_JKjT7KbrOTvlO5zIqMlHBmJjDFlMgNAxzQ/viewform">📋 Take the feedback form</a></td>
</tr></table>


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


---

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-037) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-037+%E2%80%94+&labels=IFC5-037&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optiona

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-037-security-trust.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1CgbOv0ib8CfoosIcs7IUuwFpWWWTD2g6c828ku9xQgE/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-037">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-037+%E2%80%94+&labels=IFC5-037&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdeW1Q61ee060a_JKjT7KbrOTvlO5zIqMlHBmJjDFlMgNAxzQ/viewform">📋 Take the feedback form</a></td>
</tr></table>
