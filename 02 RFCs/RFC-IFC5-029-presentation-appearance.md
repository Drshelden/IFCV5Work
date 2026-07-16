<!-- rfc-links -->
> **IFC5-029 — Presentation and Appearance** · Tier 3 — Domain Modeling
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-029) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-029+%E2%80%94+&labels=IFC5-029)

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

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-029) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-029+%E2%80%94+&labels=IFC5-029)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
