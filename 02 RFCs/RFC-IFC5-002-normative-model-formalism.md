<!-- rfc-links -->
> **IFC5-002 — Normative Information Model Formalism** · Tier 1 — Foundational
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-002) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-002+%E2%80%94+&labels=IFC5-002)

# RFC-IFC5-002: Normative Information Model Formalism

| Field | Value |
|---|---|
| **Decision ID** | IFC5-002 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | IFC5-001 |
| **Prototype Required** | No |
| **Source Topics** | Topic 2 |

---

## 1. Problem Statement

What is the authoritative IFC5 model? In IFC4.x, EXPRESS is both the schema formalism and the normative specification language. In IFC5, multiple formalisms are under consideration, and it is unclear which will be normative and which will be derived artifacts.

This matters because validation, conformance testing, tooling, and legal certification all depend on a single authoritative model.

## 2. Background

IFCX files contain schema declarations, but these are expressed in an ad hoc JSON structure that has not been formally specified. The ECS proposal uses implicit typing via componentType strings. Neither currently has a normative schema language.

## 3. Existing IFC4.x Convention

EXPRESS is the normative formalism for IFC4.x. JSON and XML serializations are derived from the EXPRESS schema. Validators are generated from EXPRESS.

## 4. Proposed Approaches

### 4.1 IFCX-specific schema language (JSON-based)

A new schema language embedded in JSON, specific to IFC5. Schemas can be distributed as packages and imported by IFCX files. Flexible but requires a new toolchain.

### 4.2 JSON Schema

Standard JSON Schema (draft-07 or 2020-12) as the normative formalism. Wide tooling support; lacks some IFC-specific expressiveness (e.g., inverse constraints, dimensional analysis).

### 4.3 EXPRESS retained

EXPRESS remains the normative formalism; IFCX is a derived serialization with a mapping specification. Preserves IFC toolchain; requires maintaining two languages.

### 4.4 TypeScript / programmatic schema

TypeScript type definitions as the normative model. Strong tooling integration; less suitable for formal standardization.

### 4.5 RDF/OWL

An ontological formalism aligned with linked-data principles. Enables SPARQL queries and semantic web integration; high complexity for most implementers.

## 5. Tradeoffs

| Dimension | IFCX-native | JSON Schema | EXPRESS | TypeScript | RDF/OWL |
|---|---|---|---|---|---|
| IFC toolchain continuity | Low | Low | High | Low | Low |
| Linked-data compatibility | Low | Low | Low | Low | High |
| Implementer accessibility | Moderate | High | Moderate | High | Low |
| Constraint expressiveness | TBD | Moderate | High | Low | High |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must the normative formalism be processable by standard tooling, or may it be IFC-specific?

**Q2.** Can validation be split — structural validation in JSON Schema, semantic validation in a separate rule language?

**Q3.** Must IFCX files be self-describing (i.e., include their schema), or may schemas be externally resolved?

**Q4.** How should schema versioning interact with the normative model?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines the toolchain required for IFC5 validators (IFC5-019)
- Determines how schema imports are declared (IFC5-012)
- Determines whether EXPRESS WHERE rules survive in IFC5 (IFC5-019)

## 10. References

- JSON Schema: https://json-schema.org
- EXPRESS / ISO 10303-11


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-002) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-002+%E2%80%94+&labels=IFC5-002)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
