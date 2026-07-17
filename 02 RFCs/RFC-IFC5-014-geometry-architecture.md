<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md) · [📝 Google Doc](https://docs.google.com/document/d/1YE7j_Z49EOi39vUzFKulc5Q2daaaqepDLzkvXXrZTDI/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-014) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-014+%E2%80%94+&labels=IFC5-014&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfp2QEmiEmeOhQp7SXXnpGt8bqGi2ho49zudsclXGGjntkOEg/viewform)


# RFC-IFC5-014: Geometry Architecture

| Field | Value |
|---|---|
| **Decision ID** | IFC5-014 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-007, IFC5-010 |
| **Prototype Required** | Yes |

---

## 1. Problem Statement

IFC4.x supports rich parametric geometry (B-rep, swept solids, CSG, profiles). IFCX examples show tessellated meshes. It is unclear whether IFC5 retains parametric geometry representations, treats tessellation as the normative exchange geometry, or supports both.

This question has downstream consequences for quantity takeoff accuracy, round-trip fidelity, and the relationship between semantic objects and their geometric representation.

## 2. Background

In IFCX Hello Wall examples, geometry appears as `usd::usdgeom::mesh` nodes with explicit vertex arrays. The parametric geometry construction history (extrusion profile, depth, axis) is not present. In ECS examples, geometry is an OBJ string embedded in a component. Neither preserves the parametric intent of the original IFC-SPF wall.

## 3. Existing IFC4.x Convention

- IfcProductDefinitionShape contains IfcShapeRepresentation
- Representations use parametric geometry (IfcExtrudedAreaSolid, etc.) or tessellation
- Multiple representations may coexist (Body, Axis, etc.) for different purposes
- Shared geometry via IfcMappedItem / IfcRepresentationMap

## 4. Proposed Approaches

### 4.1 Tessellation-only (mesh-first)

IFC5 normalizes on tessellated mesh geometry. Parametric geometry may be stored in `customdata` as a migration aid but is not normative.

### 4.2 Parametric geometry retained as schema types

IFC5 includes schema definitions for parametric geometry (extrusions, profiles, B-rep). Tessellation is a derived output, not the authoritative representation.

### 4.3 Dual representation: parametric + mesh

Objects may carry both a parametric representation (authoritative, schema-validated) and a tessellated representation (for visualization). Receivers declare which they consume.

### 4.4 External geometry assets

Geometry is not embedded in IFCX files. It is referenced by URI to external assets (glTF, OBJ, USDC). IFCX carries semantic data only; geometry is separately managed.

## 5. Tradeoffs

| Dimension | Mesh-first | Parametric | Dual | External |
|---|---|---|---|---|
| Round-trip to IFC4.x | Loss of parametric | Full | Full | Partial |
| USD geometry alignment | High | Low | Moderate | Moderate |
| Quantity accuracy | From mesh | From parametric | From parametric | Depends |
| File size | Large (meshes) | Small | Large | Small |
| BIM authoring support | Low | High | High | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Are the mesh geometries in IFCX examples authoritative, or derived outputs of parametric construction?

**Q2.** Must receivers be able to distinguish design-intent geometry from visualization geometry?

**Q3.** How is geometry shared between multiple semantic objects (mapped representations)?

**Q4.** How is the relationship between a semantic product node and its geometry node expressed?

## 8. Prototype

- **Required:** Yes
- **Notes:** Show Hello Wall with both parametric (extrusion) and tessellated representations. Demonstrate round-trip to IFC4.x.

## 9. Consequences

- Shapes OpenUSD geometry mapping decisions (IFC5-015)
- Affects placement and transforms (Topic 33)
- Determines quantity takeoff accuracy

## 10. References

- IFC4 geometry schema (IfcGeometricModelResource)
- OpenUSD UsdGeomMesh schema
- glTF 2.0 specification


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md) · [📝 Google Doc](https://docs.google.com/document/d/1YE7j_Z49EOi39vUzFKulc5Q2daaaqepDLzkvXXrZTDI/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-014) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-014+%E2%80%94+&labels=IFC5-014&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfp2QEmiEmeOhQp7SXXnpGt8bqGi2ho49zudsclXGGjntkOEg/viewform)
