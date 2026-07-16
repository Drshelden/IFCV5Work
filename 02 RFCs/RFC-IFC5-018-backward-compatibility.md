<!-- rfc-links -->
> **IFC5-018 — Backward Compatibility and Round-Tripping** · Tier 4 — Governance
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-018) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-018+%E2%80%94+&labels=IFC5-018&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)

# RFC-IFC5-018: Backward Compatibility and Round-Tripping

| Field | Value |
|---|---|
| **Decision ID** | IFC5-018 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | IFC5-007, IFC5-008, IFC5-009 |
| **Prototype Required** | Yes |
| **Source Topics** | Topic 39 |

---

## 1. Problem Statement

What does IFC5 guarantee about IFC4.x migration? Must conversion be lossless, semantically equivalent, visually equivalent, or is intentional loss acceptable? This decision has direct implications for how existing IFC4.x software, data, and certification programs relate to IFC5.

## 2. Background

The three Hello Wall files show that the same building model can be expressed differently in each format. The IFCX and ECS versions appear to lose some IFC4.x constructs (relationship identities, property-set grouping, parametric geometry). Whether this loss is acceptable is a policy decision that must be made explicitly.

## 3. Existing IFC4.x Convention

IFC4.x files are authoritative. There is no notion of round-tripping within IFC4.x; files are exchanged as complete models.

## 4. Proposed Approaches

### 4.1 Lossless round-trip required

Every IFC4.x construct must be expressible in IFC5 and recoverable without data loss. The migration is a bijection. Strongest compatibility guarantee; most constraining on IFC5 design freedom.

### 4.2 Semantic equivalence required

All semantically meaningful IFC4.x data is preserved. STEP instance numbers, positional encoding, and derived attributes may be lost. Relationship GUIDs must be preserved.

### 4.3 Information equivalence with defined lossy transforms

A migration specification documents which IFC4.x constructs are transformed, which are dropped, and how receivers should interpret migrated data. Loss is acceptable if documented.

### 4.4 No backward compatibility guarantee

IFC5 is a new format. IFC4.x migration tools are out of scope for the standard. Third parties may develop converters.

## 5. Tradeoffs

| Dimension | Lossless | Semantic equiv | Defined lossy | No guarantee |
|---|---|---|---|---|
| Existing data protection | High | High | Moderate | None |
| IFC5 design freedom | Low | Moderate | High | Full |
| Certification continuity | Full | Partial | Partial | None |
| Migration tooling cost | High | Moderate | Moderate | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must IFC GlobalIds be preserved exactly in IFC5? If so, the identity model is constrained.

**Q2.** Must OwnerHistory be preserved? It carries audit trail information.

**Q3.** Must relationship GUIDs (for IfcRel* instances) be preserved?

**Q4.** What is the minimum IFC4.x subset that every IFC5 implementation must be able to migrate?

## 8. Prototype

- **Required:** Yes
- **Notes:** Convert Hello Wall IFC-SPF → IFCX → IFC-SPF. Document every attribute that is lost, transformed, or invented in the round-trip.

## 9. Consequences

- Constrains identity model (IFC5-003) if GlobalId preservation is required
- Constrains class representation (IFC5-009) if inheritance chain must be recoverable
- Constrains relationship model (IFC5-008) if relationship GUIDs must survive

## 10. References

- IFC4 ADD2 TC1 schema
- Hello Wall IFC-SPF: `03 Reference Examples/hello-wall.ifc`


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-018) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-018+%E2%80%94+&labels=IFC5-018&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
