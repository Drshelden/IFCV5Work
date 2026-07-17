<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1p8W1b0jPkaYfeuCQ2o6SEc5JgRFUkFafGEujorUrytY/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-029">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-029+%E2%80%94+&labels=IFC5-029&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSfyW5GdJbrXpWXv2IWIga2Dt0wUQLETFyG0eAbit0S5NEh5EQ/viewform">📋 Take the feedback form</a></td>
</tr></table>


# RFC-IFC5-029: Presentation and Appearance

| Field | Value |
|---|---|
| **Decision ID** | IFC5-029 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-015, IFC5-017 |
| **Prototype Required** | No |
| **Source Topics** | Topic 35 |

---

## 1. Problem Statement

IFC4.x has a rich presentation model: IfcSurfaceStyle, IfcCurveStyle, IfcTextStyle, IfcPresentationLayerAssignment, and color/opacity/texture definitions. IFCX examples use USD-derived presentation attributes (`bsi::ifc::presentation::diffuseColor`). Whether IFC5 adopts USD's UsdShade model, retains IFC4.x presentation objects, or defines a hybrid is not specified.

The distinction between engineering materials (thermal, structural properties) and render materials (visualization) must also be clarified.

## 2. Background

In IFCX examples, presentation data appears as namespaced color attributes inline on element nodes. In IFC4.x, presentation is a separate resource layer (IfcPresentationResource) attached to geometry representations, not directly to semantic objects. The two approaches have different inheritance and override models.

## 3. Existing IFC4.x Convention

- IfcSurfaceStyle: diffuse/specular/transmission colors, textures
- IfcCurveStyle: line thickness, color, dash pattern
- IfcPresentationLayerAssignment: CAD layer assignment
- Presentation attached to IfcRepresentationItem, not to products directly
- Style inheritance through geometry hierarchy

## 4. Proposed Approaches

### 4.1 USD UsdShade material binding

Render materials use USD's UsdShade schema. Material prims are bound to geometry nodes. IFC4.x surface styles are migrated to UsdPreviewSurface or MaterialX. Full USD tooling compatibility.

### 4.2 Inline presentation attributes on elements

Presentation properties (diffuseColor, opacity) are namespaced attributes on the element node. No separate material nodes. Simple; loses geometry-level override capability.

### 4.3 IFC4.x presentation objects retained

IfcSurfaceStyle and related objects are preserved as named nodes attached to geometry representations. Maximum IFC4.x fidelity; least USD alignment.

### 4.4 Hybrid: engineering materials as objects, render as inline

Engineering material definitions (fire rating, thermal conductivity) use structured property objects (IFC5-017). Render/visualization properties are inline attributes or USD material bindings. Separates concerns cleanly.

## 5. Tradeoffs

| Dimension | USD UsdShade | Inline attrs | IFC4.x objects | Hybrid |
|---|---|---|---|---|
| USD tooling compatibility | High | Low | None | Moderate |
| IFC4.x round-trip | Low | Low | High | Moderate |
| Layer assignment support | Via USD purpose | Limited | Full | Limited |
| Geometry-level override | Full | None | Full | Partial |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is CAD layer assignment (IfcPresentationLayerAssignment) in scope for IFC5?

**Q2.** How are discipline-specific display states (e.g., different colors for structural vs. architectural view) represented?

**Q3.** How does type-level style inheritance work — does an element inherit presentation from its type object?

**Q4.** Is PBR (Physically Based Rendering) material support required for IFC5?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Tied to OpenUSD alignment decisions (IFC5-015)
- Tied to material modeling (IFC5-017)
- Affects geometry architecture (IFC5-014) — geometry-level style attachment

## 10. References

- IFC4 IfcPresentationResource schema
- USD UsdShade and UsdPreviewSurface documentation
- MaterialX specification


---

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-029) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-029+%E2%80%94+&labels=IFC5-029&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Option

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1p8W1b0jPkaYfeuCQ2o6SEc5JgRFUkFafGEujorUrytY/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-029">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-029+%E2%80%94+&labels=IFC5-029&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSfyW5GdJbrXpWXv2IWIga2Dt0wUQLETFyG0eAbit0S5NEh5EQ/viewform">📋 Take the feedback form</a></td>
</tr></table>
