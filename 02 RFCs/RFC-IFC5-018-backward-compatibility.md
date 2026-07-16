<!-- rfc-links -->
> **IFC5-018 — Backward Compatibility and Round-Tripping** · Tier 4 — Governance
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-018) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-018+%E2%80%94+&labels=IFC5-018)

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
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-018) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-4-governance&title=%5BRFC+Feedback%5D+IFC5-018+%E2%80%94+&labels=IFC5-018)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
