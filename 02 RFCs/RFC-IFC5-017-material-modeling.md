<!-- rfc-links -->
> **IFC5-017 — Material Modeling** · Tier 3 — Domain Modeling
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-017) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-017+%E2%80%94+&labels=IFC5-017)

# RFC-IFC5-017: Material Modeling

| Field | Value |
|---|---|
| **Decision ID** | IFC5-017 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-013 |
| **Prototype Required** | No |
| **Source Topics** | Topic 29 |

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

- Tied to property sets decision (IFC5-013)
- Shapes geometry-material binding in the OpenUSD context (IFC5-015)

## 10. References

- IFC4 IfcMaterialResource schema
- USD UsdShade material binding


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-017) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-017+%E2%80%94+&labels=IFC5-017)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
