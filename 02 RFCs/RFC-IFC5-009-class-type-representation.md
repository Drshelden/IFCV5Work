
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-009](https://docs.google.com/forms/d/e/1FAIpQLSeBGI1FYTPy5FytaQWIW-oWbOsSQaeoiJlaaTqNe_6QNV_jhw/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) · [📝 Google Doc](https://docs.google.com/document/d/1kQGtF_UA9mpYj_tIuPvnIBKEzmyxmJlNkmbztD-OMSo/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-009) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-009+%E2%80%94+&labels=IFC5-009&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeBGI1FYTPy5FytaQWIW-oWbOsSQaeoiJlaaTqNe_6QNV_jhw/viewform)


# RFC-IFC5-009: Class and Type Representation

| Field | Value |
|---|---|
| **Decision ID** | IFC5-009 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | [IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) |
| **Prototype Required** | No |

---

## 1. Problem Statement

In IFC4.x, the deep class inheritance hierarchy (IfcRoot → IfcObjectDefinition → IfcObject → IfcProduct → IfcElement → IfcBuildingElement → IfcWall) is normative and constrains valid property sets, relationships, and geometry. IFC5 proposals disagree on whether this hierarchy is retained, flattened, or replaced by component composition.

Related: how do IfcTypeObject and IfcElementType (type objects) map to IFC5 prototype/instancing mechanisms?

## 2. Background

In IFCX, `bsi::ifc::class` appears as a string attribute. In ECS, `componentType` carries the class name. Neither explicitly preserves the full IFC inheritance chain. The question is whether subtype polymorphism (a query for IfcBuildingElement must return IfcWall instances) is preserved.

## 3. Existing IFC4.x Convention

- Entity classes defined in EXPRESS with explicit supertypes
- Type objects (IfcWallType) associated with occurrences via IfcRelDefinesByType
- Predefined types encoded as PredefinedType attribute + USERDEFINED
- Deep hierarchy: 6–8 levels common

## 4. Proposed Approaches

### 4.1 Retain class hierarchy as schema types

IFC class hierarchy is expressed in the IFC5 schema formalism. Every object declares its class; validators can query supertypes. Highest fidelity; requires EXPRESS-like expressiveness in the schema language.

### 4.2 Class as a classification attribute

The IFC class is stored as a string or code/URI attribute (`bsi::ifc::class: "IfcWall"`). Hierarchy is implicit in the bSDD or schema metadata but not enforced at the file level. Simpler; loses compile-time subtype checking.

### 4.3 Classes become component sets (ECS)

An object's class is determined by which components are attached. An IfcWall is any entity that has a WallComponent. Class hierarchy is expressed as component inheritance or schema composition.

### 4.4 Hybrid: schema-typed class with attribute shorthand

Normative schema types define the hierarchy; an attribute shorthand (`bsi::ifc::class`) is generated for query convenience. Both are present; schema type is normative.

## 5. Tradeoffs

| Dimension | Schema types | Classification attribute | Component sets | Hybrid |
|---|---|---|---|---|
| Subtype polymorphism | Full | Metadata-only | By composition | Full |
| IFC4.x round-trip | High | Moderate | Low | High |
| Schema complexity | High | Low | Moderate | High |
| USD API schema alignment | Moderate | Low | High | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must subtype polymorphism be supported at the file format level? (Can a receiver query "give me all IfcBuildingElement instances" without knowing every subtype?)

**Q2.** How do predefined types (e.g., IfcWall.PredefinedType = SHEAR) map to IFC5?

**Q3.** How do type objects (IfcWallType) map? Are they USD prototypes, schema classes, or ordinary nodes?

**Q4.** Can multiple classes be applied to one object? (e.g., an object that is both a structural member and a wall)

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines how property applicability is validated ([IFC5-019](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-019-validation-framework.md))
- Shapes the inheritance/instancing decision ([IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md))
- Affects backward compatibility ([IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md))

## 10. References

- IFC4 ADD2 TC1 entity hierarchy
- bSDD: https://search.bsdd.buildingsmart.org


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) · [📝 Google Doc](https://docs.google.com/document/d/1kQGtF_UA9mpYj_tIuPvnIBKEzmyxmJlNkmbztD-OMSo/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-009) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-009+%E2%80%94+&labels=IFC5-009&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeBGI1FYTPy5FytaQWIW-oWbOsSQaeoiJlaaTqNe_6QNV_jhw/viewform)
