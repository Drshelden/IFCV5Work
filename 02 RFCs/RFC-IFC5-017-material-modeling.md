
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-017](https://docs.google.com/forms/d/e/1FAIpQLSdph7XZZjeLBeK2onnWMpCcy7ZVz5PaHHJTPInaMP0GwOK8mQ/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) · [📝 Google Doc](https://docs.google.com/document/d/13bVfx5TR0ZLYvaMvSM6ZDyYNObfzKFGkAzuuNeqyre4/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-017) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-017+%E2%80%94+&labels=IFC5-017&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdph7XZZjeLBeK2onnWMpCcy7ZVz5PaHHJTPInaMP0GwOK8mQ/viewform)


# RFC-IFC5-017: Material Modeling

| Field | Value |
|---|---|
| **Decision ID** | IFC5-017 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | [IFC5-013](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md) |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFC4.x has a rich material modeling system: IfcMaterial, IfcMaterialLayerSet, IfcMaterialConstituentSet, IfcMaterialProfileSet, with physical, environmental, and presentation properties. IFC5 examples contain inline material data in a simplified form. How IFC material semantics map to IFC5 — and whether materials become scene-graph nodes — is not defined.

## 2. Background

In IFCX Hello Wall, materials appear as inline attributes under the wall node (e.g., `bsi::ifc::presentation::diffuseColor`). In ECS, a material component is a separate entity. In IFC4.x, materials are independent objects associated via IfcRelAssociatesMaterial, enabling sharing across many elements.

## 3. Existing IFC4.x Convention

- IfcMaterial: named material with optional classification and category
- IfcMaterialLayerSet: ordered layers with thickness and offset
- IfcMaterialConstituentSet: named constituents for composite elements
- IfcMaterialProfileSet: profile-based (structural sections)
- Associated via IfcRelAssociatesMaterial to elements or types
- Physical properties via IfcMaterialProperties

## 4. Proposed Approaches

### 4.1 Materials as scene-graph nodes

Materials are nodes in the scene graph, referenceable by path. Elements reference material nodes. Aligns with USD UsdShade material binding.

### 4.2 Materials inline as attributes

Material data is expressed as namespaced attributes on the element node. No separate material identity. Simple; loses sharing and reuse.

### 4.3 Materials retained as first-class semantic objects

IfcMaterialLayerSet and equivalents are preserved as named objects. Association via relationship (IFC5 equivalent of IfcRelAssociatesMaterial). Highest fidelity.

### 4.4 Hybrid: presentation materials inline; engineering materials as objects

Render/visualization materials (diffuseColor, PBR) are inline. Engineering material definitions (thermal conductivity, fire rating) are named objects with full property sets.

## 5. Tradeoffs

| Dimension | Scene nodes | Inline attrs | First-class objects | Hybrid |
|---|---|---|---|---|
| Engineering property preservation | Low | Low | High | High |
| USD render material alignment | High | Low | Low | Moderate |
| Sharing across elements | High | None | High | Partial |
| File verbosity | Low | Low | High | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is sharing of material definitions across elements required in IFC5?

**Q2.** How do IfcMaterialLayerSet and IfcMaterialConstituentSet map to IFC5?

**Q3.** Should presentation materials (render) and engineering materials (physical properties) use the same representation?

**Q4.** Can a material reference a bSDD or external material vocabulary entry?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Tied to property sets decision ([IFC5-013](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md))
- Shapes geometry-material binding in the OpenUSD context ([IFC5-015](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md))

## 10. References

- IFC4 IfcMaterialResource schema
- USD UsdShade material binding


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) · [📝 Google Doc](https://docs.google.com/document/d/13bVfx5TR0ZLYvaMvSM6ZDyYNObfzKFGkAzuuNeqyre4/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-017) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-017+%E2%80%94+&labels=IFC5-017&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdph7XZZjeLBeK2onnWMpCcy7ZVz5PaHHJTPInaMP0GwOK8mQ/viewform)
