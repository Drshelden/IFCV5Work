<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md) · [📝 Google Doc](https://docs.google.com/document/d/1iYD6pizVQUI4ZDDUWvfJE5waVV2m2Le_gXabpW6dt04/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-026) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-026+%E2%80%94+&labels=IFC5-026&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeE0p-ic000wKBiTR15HoycvbH2O39h6cWbYZNh62qyArQX5w/viewform)


# RFC-IFC5-026: Openings, Voids, and Fillings

| Field | Value |
|---|---|
| **Decision ID** | IFC5-026 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-008, IFC5-016 |
| **Prototype Required** | Yes |

---

## 1. Problem Statement

The opening/void/filling pattern — a wall hosts an opening, which is filled by a window — is one of the most common and semantically significant constructs in building models. IFC4.x represents this with IfcOpeningElement, IfcRelVoidsElement, and IfcRelFillsElement as distinct objects. IFC5 proposals suggest collapsing this into host-child hierarchy. Whether the semantic distinctions are preserved is a key decision.

## 2. Background

In IFC4.x:
- IfcOpeningElement is a product with its own identity, geometry, placement, and GlobalId
- IfcRelVoidsElement links the host (wall) to the opening
- IfcRelFillsElement links the opening to the filling element (window)
- The void geometry drives boolean subtraction from the host geometry

In IFCX examples, windows appear as children of walls. Whether this implies voiding and filling semantics is not declared.

## 3. Existing IFC4.x Convention

- IfcOpeningElement: independent semantic object with placement and geometry
- IfcRelVoidsElement: void relationship (one opening per relationship)
- IfcRelFillsElement: filling relationship (one filling per relationship, multiple allowed per opening)
- Host geometry is constructed by boolean subtraction; opening geometry defines the cut

## 4. Proposed Approaches

### 4.1 Scene hierarchy implies void/fill

A window that is a `child` of a wall implicitly means the wall has an opening voided by the window geometry. IfcOpeningElement no longer exists as an independent object. Simple; loses opening identity and geometry.

### 4.2 Explicit opening nodes retained

IfcOpeningElement is preserved as a named scene node, child of the host. IfcRelVoidsElement and IfcRelFillsElement become attributes or child relationships of the opening node. Opening identity and geometry are preserved.

### 4.3 Relationship attributes on host

The host wall carries a `voids` attribute listing opening descriptors, each with its geometry and optional filling reference. Openings do not exist as independent nodes. Compact; loses round-trip to IfcOpeningElement GlobalId.

### 4.4 Full IFC4.x objects preserved

IfcOpeningElement, IfcRelVoidsElement, and IfcRelFillsElement are fully preserved as named nodes, with the same structure as IFC4.x. Maximum fidelity; most verbose.

## 5. Tradeoffs

| Dimension | Hierarchy implies | Explicit nodes | Rel attributes | Full objects |
|---|---|---|---|---|
| File simplicity | High | Moderate | Moderate | Low |
| Opening identity preserved | No | Yes | No | Yes |
| Round-trip to IFC4.x | Low | High | Moderate | High |
| Boolean subtraction semantics | Implicit | Explicit | Explicit | Explicit |
| Multiple fillings per opening | Unclear | Yes | Yes | Yes |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must IfcOpeningElement preserve its own GlobalId in IFC5? (It is referenced by MEP and structural analysis tools.)

**Q2.** When a window is a child of a wall in the scene graph, does that unambiguously imply a void relationship?

**Q3.** How is the opening geometry (the cut shape) expressed if IfcOpeningElement no longer exists?

**Q4.** How are unfilled openings (no window) represented in the child-of-wall approach?

## 8. Prototype

- **Required:** Yes
- **Notes:** Show Hello Wall with wall, opening, and window in all three formats. Verify that void geometry and filling identity round-trip correctly.

## 9. Consequences

- Tied to relationship modeling strategy (IFC5-008)
- Affects geometry architecture (IFC5-014) — boolean subtraction semantics
- Affects backward compatibility (IFC5-018) — opening GlobalIds

## 10. References

- IFC4 IfcOpeningElement, IfcRelVoidsElement, IfcRelFillsElement
- Hello Wall IFC-SPF: `03 Reference Examples/hello-wall.ifc`


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md) · [📝 Google Doc](https://docs.google.com/document/d/1iYD6pizVQUI4ZDDUWvfJE5waVV2m2Le_gXabpW6dt04/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-026) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-026+%E2%80%94+&labels=IFC5-026&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeE0p-ic000wKBiTR15HoycvbH2O39h6cWbYZNh62qyArQX5w/viewform)
