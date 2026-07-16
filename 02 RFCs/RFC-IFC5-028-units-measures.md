<!-- rfc-links -->
> **IFC5-028 — Units and Measures** · Tier 3 — Domain Modeling
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-028) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-028+%E2%80%94+&labels=IFC5-028)

# RFC-IFC5-028: Units and Measures

| Field | Value |
|---|---|
| **Decision ID** | IFC5-028 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-011, IFC5-024 |
| **Prototype Required** | No |
| **Source Topics** | Topic 34 |

---

## 1. Problem Statement

IFC4.x encodes units in the IfcProject and allows per-attribute unit overrides. Measure types carry implicit dimensional semantics (IfcLengthMeasure, IfcAreaMeasure, IfcThermodynamicTemperatureMeasure). In IFC5, the rules for document-wide units, schema-defined units, per-attribute units, and dimensional analysis are not defined.

## 2. Background

In IFC4.x, the project declares SI or conversion-based units. Measure types carry dimensional semantics that can be validated against declared units. In practice, most IFC files use SI with millimetres as the length unit.

In IFCX, numeric values appear as plain JSON numbers. It is not clear whether receivers must consult the document header to interpret them, whether per-attribute unit declarations are supported, or how dimensional analysis is validated.

## 3. Existing IFC4.x Convention

- IfcUnitAssignment in IfcProject declares project-wide units
- IfcSIUnit, IfcConversionBasedUnit, IfcDerivedUnit
- Measure types in EXPRESS carry dimensional semantics
- Per-instance unit overrides via IfcMeasureWithUnit (rare)

## 4. Proposed Approaches

### 4.1 Document-wide units in header; numeric values unitless

All numeric values are interpreted against the document-declared unit system. Per-attribute unit overrides not supported (or are rare exceptions).

### 4.2 Per-attribute unit declarations

Each numeric attribute may carry an explicit unit declaration: `{"value": 3.5, "unit": "m"}`. Self-describing; allows mixed-unit models. Verbose.

### 4.3 Schema-defined canonical units per attribute type

Each schema-defined attribute type declares its canonical unit (e.g., length in metres, area in m²). Files store values in canonical units. No per-file unit declaration needed.

### 4.4 Dimensional metadata in schema, with document-level override

Schema declares the dimension of each attribute. The document header declares the project unit system, which overrides the canonical unit for display. Values stored in project units.

## 5. Tradeoffs

| Dimension | Doc-wide units | Per-attribute | Schema-canonical | Doc override |
|---|---|---|---|---|
| Compactness | High | Low | High | High |
| Mixed-unit models | No | Yes | No | No |
| Schema-free interpretation | No | Yes | No | No |
| Dimensional validation | Via schema | Via value | Via schema | Via schema |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Are IFC5 values stored in SI or in the project unit system? (SI is more interoperable; project units are more author-friendly.)

**Q2.** Are monetary units and currency dates in scope for IFC5 unit declarations?

**Q3.** How are dimensionless ratios (e.g., thermal resistance) distinguished from unitless values?

**Q4.** How are temperature values handled — absolute (Kelvin) vs. relative (°C)?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Affects property encoding (IFC5-013) — unit-bearing property values
- Shapes geometry precision and coordinate representation (IFC5-014)
- Tied to type system (IFC5-024) — measure type dimensional semantics

## 10. References

- IFC4 IfcMeasureResource schema
- SI Brochure (BIPM)


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-028) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-028+%E2%80%94+&labels=IFC5-028)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
