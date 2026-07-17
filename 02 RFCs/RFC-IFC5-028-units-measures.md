<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1opW4ky0z3ll0bTgQT6dpRdQSmXEbWxh6I61g9HY5fb8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-028">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-028+%E2%80%94+&labels=IFC5-028&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSddABPiY6olZQ4k4vv2hMDwmiMrGMoxVt_j5SuoL_nxn4bgZQ/viewform">📋 Take the feedback form</a></td>
</tr></table>


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

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-028) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-028+%E2%80%94+&labels=IFC5-028&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1opW4ky0z3ll0bTgQT6dpRdQSmXEbWxh6I61g9HY5fb8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-028">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-028+%E2%80%94+&labels=IFC5-028&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSddABPiY6olZQ4k4vv2hMDwmiMrGMoxVt_j5SuoL_nxn4bgZQ/viewform">📋 Take the feedback form</a></td>
</tr></table>
