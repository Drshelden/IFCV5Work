
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-013](https://docs.google.com/forms/d/e/1FAIpQLSdZtGeaXPoC8s3-JOESbdAlI3AKl3RgqWd-tEul12t_tWAL9w/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1PQGu24WhHJ7XFW--1t_EHn8kXPtZI1lGL0mnnNMLkF8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-013">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-013+%E2%80%94+&labels=IFC5-013&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdZtGeaXPoC8s3-JOESbdAlI3AKl3RgqWd-tEul12t_tWAL9w/viewform">📋 Take the feedback form</a></td>
</tr></table>


# RFC-IFC5-013: Property Sets and Properties

| Field | Value |
|---|---|
| **Decision ID** | IFC5-013 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-009 |
| **Prototype Required** | Yes |
| **Source Topics** | Topic 27 |

---

## 1. Problem Statement

IFC4.x uses IfcPropertySet objects, associated via IfcRelDefinesByProperties, to attach typed properties to objects. IFCX examples suggest properties may become namespaced attributes (e.g., `bsi::ifc::prop::IsExternal`). These two representations are fundamentally different: the first preserves property-set grouping and identity; the second does not.

The question is: how are IFC properties represented in IFC5, and what information is preserved?

## 2. Background

In IFC4.x, `Pset_WallCommon.IsExternal` is an IfcPropertySingleValue named `IsExternal` inside an IfcPropertySet named `Pset_WallCommon`, associated to a wall via IfcRelDefinesByProperties. The property-set name, the relationship identity, and the property type are all distinct pieces of information.

In IFCX examples, this might appear as `"bsi::ifc::prop::IsExternal": true`. The property-set name `Pset_WallCommon` may be lost.

## 3. Existing IFC4.x Convention

- IfcPropertySet with name and set of IfcProperty
- IfcRelDefinesByProperties links set to one or more objects
- Properties have names, values, units, and optional descriptions
- QuantitySet variants with measure semantics

## 4. Proposed Approaches

### 4.1 Properties become namespaced attributes

Properties are expressed as qualified attributes directly on the object node. Property-set grouping is encoded in the namespace prefix. `Pset_WallCommon.IsExternal` → `bsi::ifc::Pset_WallCommon::IsExternal`.

### 4.2 Property sets retained as sub-objects

Each property set remains a named child node or attribute group. Properties are sub-attributes. Property-set identity is preserved.

### 4.3 IfcPropertySet retained as first-class objects

Property sets remain explicit named objects associated via IfcRelDefinesByProperties (or its IFC5 equivalent). Highest fidelity; most verbose.

### 4.4 Hybrid: schema-defined sets become attributes; custom sets remain objects

Standard buildingSMART property sets (Pset_WallCommon, etc.) become namespaced attributes. Custom or unknown property sets remain explicit objects.

## 5. Tradeoffs

| Dimension | Namespaced attrs | Sub-objects | First-class objects | Hybrid |
|---|---|---|---|---|
| IFC4.x round-trip | Low (Pset name lost) | Moderate | High | High |
| Query simplicity | High | Moderate | Low | Moderate |
| bSDD linkage | Via namespace | Via name | Via relationship | Mixed |
| File verbosity | Low | Moderate | High | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is the property-set name (e.g., `Pset_WallCommon`) normatively required in IFC5, or may it be lost in translation?

**Q2.** How are complex properties (bounded values, enumerated values, table values) encoded?

**Q3.** How are custom (non-buildingSMART) property sets handled?

**Q4.** How does bSDD property validation work if properties are namespaced attributes?

## 8. Prototype

- **Required:** Yes
- **Notes:** Show Pset_WallCommon.IsExternal in both IFCX and ECS representations, with round-trip back to IFC4.x.

## 9. Consequences

- Affects material modeling (IFC5-017)
- Affects validation framework (IFC5-019)

## 10. References

- buildingSMART Property Sets: https://github.com/buildingSMART/IFC4.3-html
- bSDD: https://search.bsdd.buildingsmart.org


---

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-013) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-013+%E2%80%94+&labels=IFC5-013&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Option

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1PQGu24WhHJ7XFW--1t_EHn8kXPtZI1lGL0mnnNMLkF8/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-013">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-013+%E2%80%94+&labels=IFC5-013&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdZtGeaXPoC8s3-JOESbdAlI3AKl3RgqWd-tEul12t_tWAL9w/viewform">📋 Take the feedback form</a></td>
</tr></table>
