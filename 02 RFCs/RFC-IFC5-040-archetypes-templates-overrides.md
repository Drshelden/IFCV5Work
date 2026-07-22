<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-040](https://docs.google.com/forms/d/e/1FAIpQLSeUzq6dz0OlETzYhZIgeFc8lEbb0kR1lh0cSDAPYOWAeq2zEg/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) · [📝 Google Doc](https://docs.google.com/document/d/15FBR8_JsY504a8fAH_vg5av5kkZH8FNeb2ce_0tPyAg/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-040) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-040+%E2%80%94+&labels=IFC5-040&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeUzq6dz0OlETzYhZIgeFc8lEbb0kR1lh0cSDAPYOWAeq2zEg/viewform)


# RFC-IFC5-040: Archetypes, Type Templates, and Override Mechanisms

| Field | Value |
|---|---|
| **Decision ID** | IFC5-040 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | [IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md), [IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md), [IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md), [IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md), [IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md), [IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md) |
| **Prototype Required** | Yes |
| **Logical position** | Tier 2 — extends [IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) (Class and Type Representation) and [IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) (Composition, Inheritance, Instancing) |

---

## 1. Problem Statement

IFC4.x has a concept of "type objects" (e.g., `IfcWallType`) that define shared properties for all instances of that type. IFCX, following USD, has a more powerful concept of **archetypes**: templates that define a default entity structure — including children, components, and attribute values — which can be **instantiated** multiple times and **selectively overridden** on each instance. IFC-ECS has a `componentType` field but no architecture for defining a typed template, instantiating it, or overriding specific attributes per instance.

This gap is significant:
- Without archetypes, every wall in a model must redundantly carry all of its component data. With archetypes, instances carry only their differences from the template.
- Without override semantics, composition (inheriting from a base type while customizing it) requires copying data, not referencing and patching it.
- The path model ([IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md)) is tightly coupled to USD-style override semantics: paths allow overrides to target sub-nodes precisely. It is an open question whether GUID-based ECS can support equivalent override behavior without paths.

This RFC asks: Should IFC5 define a normative archetype/template mechanism? If so, what are its semantics, and does it require a path hierarchy?

---

## 2. Background

### 2.1 USD Archetypes (the IFCX model)

USD uses the term "prototype" or "class" for reusable template prims. The mechanism works as follows:

1. Define a template prim at a well-known path (e.g., `/Templates/StandardWall`)
2. Reference it from instances using `inherits` or `references`:
   ```json
   {
     "path": "/Building/Wall001",
     "inherits": "/Templates/StandardWall",
     "attributes": {
       "ifc:Name": { "value": "Wall-001" }
     }
   }
   ```
3. Attributes on the instance **override** the template's values. Attributes not mentioned on the instance **inherit** from the template.
4. USD distinguishes **opinion strength**: "stronger" opinions (closer to the instance) override "weaker" ones (from the template or inherited prims). This allows layered composition without destroying the original.

The path structure is load-bearing here: overrides target sub-nodes by path, enabling precise attribute-level and sub-component-level overrides in deep hierarchies.

### 2.2 IFC4.x Type Objects

IFC4.x has `IfcTypeObject` (and subtypes like `IfcWallType`). Instances are linked via `IfcRelDefinesByType`. This provides:
- Shared property sets on the type
- A defined type name and occurrence-level overrides via `IfcRelDefinesByProperties`

What IFC4.x does **not** support:
- Partial attribute overrides (you either use the type's value or replace it entirely)
- Nested component/sub-object inheritance with selective override
- Layered composition (multiple levels of template inheritance with defined precedence)

### 2.3 IFC-ECS: Component Types Without Templates

IFC-ECS has a `componentType` field on each component. This allows grouping and querying components by type. However:
- There is no mechanism to define a **component template** — a default set of attributes that all components of that type inherit
- There is no mechanism to **instantiate** a typed entity template and selectively override specific components or attributes
- The flat array model means there is no path structure to address sub-components for override

### 2.4 JSONSchema and TypeScript as Template Languages

An alternative approach to USD-style archetype paths is to use an existing schema language to define component templates:

**JSON Schema:**
```json
{
  "$id": "IfcWallType",
  "type": "object",
  "properties": {
    "Name": { "type": "string" },
    "IsExternal": { "type": "boolean", "default": false },
    "LoadBearing": { "type": "boolean", "default": false }
  }
}
```

**TypeScript-style:**
```typescript
interface IfcWallType {
  Name: string;
  IsExternal: boolean;    // default: false
  LoadBearing: boolean;   // default: false
}
```

Both provide type safety and default values but do not natively support the override-composition semantics USD provides. Extensions would be required.

---

## 3. Existing IFC4.x Convention

`IfcTypeObject` → linked to instances via `IfcRelDefinesByType`. Shared property sets via `IfcPropertySetTemplate`. No structural inheritance, no layered overrides. The mechanism is explicit relationship-based, not prototype-based.

---

## 4. Proposed Approaches

### 4.1 USD-style archetypes with path-based overrides (IFCX)

IFC5 adopts USD's archetype/prototype model directly. Templates are defined at canonical paths. Instances reference templates via `inherits`. Overrides are expressed as attributes and sub-node modifications on the instance prim. The path hierarchy is required to address override targets.

This is the most powerful mechanism but requires the path hierarchy (IFC5-004) as a prerequisite.

### 4.2 GUID-based component templates with override records

IFC5 defines a component template mechanism that works with GUID-addressed entities, without requiring a path hierarchy. A template is a named component-set definition. Instances reference a template by ID. Overrides are explicit records:
```json
{
  "entityGuid": "14adb22b-...",
  "templateId": "StandardWall",
  "overrides": {
    "IfcWallGeometry.Height": 3200,
    "IfcWallMaterial.Name": "Brick"
  }
}
```

This approach preserves ECS-style flat addressing while supporting archetype behavior. It does not require USD-style path traversal. The override syntax is more explicit but less composable than USD's layered model.

### 4.3 JSONSchema / TypeScript as the template definition language

Component templates are defined using JSON Schema (or TypeScript interfaces). Default values are specified in the schema. Instances omit attributes that match the default, reducing redundancy. Override semantics are simple: instance attribute values replace schema defaults. No inheritance chain is required.

This approach is well-tooled, widely understood, and integrates naturally with JSON-native workflows. It does not support multi-level composition (a template inheriting from another template with override).

### 4.4 Explicit archetype RFC as a first-class IFC5 construct

IFC5 defines a dedicated `IfcArchetype` (or `IfcTemplate`) entity with explicit composition semantics: base template, layers of override, and defined opinion strength (strong vs. weak). This is a new IFC construct that borrows USD semantics but does not require USD paths. Components declare which archetype they participate in. Override precedence is explicit.

### 4.5 No normative archetype mechanism — defer to schema conventions

IFC5 does not specify an archetype or template system. Schema authors define types using JSON Schema. Instance data is always fully materialized (no implicit inheritance). Tooling is responsible for managing template libraries. This is the lowest complexity option but sacrifices the data-economy and composition benefits of archetypes.

---

## 5. Tradeoffs

| Dimension | USD archetypes | GUID-based overrides | JSONSchema templates | Explicit archetype construct | No mechanism |
|---|---|---|---|---|---|
| USD / IFCX alignment | High | Low | Low | Moderate | None |
| ECS compatibility | Low | High | High | Moderate | High |
| Override expressiveness | High | Moderate | Low | High | None |
| Tooling complexity | High | Moderate | Low | High | Low |
| Prototype required | Yes | Yes | No | Yes | No |
| File size benefit | High | High | Moderate | High | None |
| Path hierarchy dependency | Required | None | None | Optional | None |

---

## 6. Recommendation

*To be filled in after committee discussion.*

---

## 7. Open Questions

**Q1.** Should IFC5 define a normative archetype/template mechanism, or leave type instantiation to schema-level conventions (JSON Schema defaults)?

**Q2.** Is the USD-style path hierarchy a **requirement** for supporting practical override semantics, or can a GUID-based component model support equivalent behavior? If GUID-based overrides are possible, what additions to the ECS model are required?

**Q3.** Should the template definition language for IFC5 archetypes be based on an existing standard (JSON Schema, TypeScript, OWL) or a custom IFC5 construct? What are the tradeoffs in terms of tooling, expressiveness, and long-term maintenance?

**Q4.** How should **partial overrides** work: should an instance be able to override a single attribute within a component, an entire component, or an entire entity template? What is the minimum granularity required for practical BIM use cases?

**Q5.** Can IFC-ECS's flat component model be extended to support archetype definition and instantiation without requiring a path hierarchy? If a prototype is built to demonstrate this, what does it reveal about the limitations of the approach?

**Q6.** Should IFC5 adopt USD's distinction between **strong opinions** (always win) and **weak opinions** (can be overridden by later composition)? Is this level of complexity necessary for building model use cases, or is a simpler "instance always overrides template" rule sufficient?

**Q7.** Should archetypes/templates be versioned independently of the instances that reference them? What happens to existing instances when a template is updated?

---

## 8. Prototype

- **Required:** Yes
- **Notes:** Demonstrate archetype instantiation and override using the Hello Wall example. Show at minimum: (1) a wall type template with default geometry and material components, (2) ten instances that override only their names and positions, (3) one instance that overrides the material. Compare file size and query behavior against a fully materialized (no-template) version. Demonstrate this in both IFCX (USD-style paths) and IFC-ECS (GUID-based) to test approach 4.2.

---

## 9. Consequences

- **IFC5-004 (Path Model):** If approach 4.1 is adopted, path addressing is load-bearing for override semantics, not just navigation. This significantly raises the stakes of the path model decision.
- **IFC5-007 (Scene Graph vs. ECS):** Archetype behavior via overrides is native to the scene graph model; ECS requires additional design to match it. This RFC may reveal a fundamental asymmetry between the two architectures.
- **IFC5-009 (Class and Type Representation):** The relationship between `IfcTypeObject` and the new archetype mechanism must be defined. Are they the same thing, or are archetypes a more powerful replacement?
- **IFC5-010 (Composition, Inheritance, Instancing):** Archetypes are the primary use case for composition and inheritance. This RFC provides the concrete mechanism that RFC-IFC5-010 must describe abstractly.
- **IFC5-034 (Performance, Scale, Database):** Archetype instantiation with selective overrides has significant implications for how models are stored and queried. Database designs differ significantly between fully materialized and reference-plus-override approaches.

---

## 10. References

- USD Composition Arcs: https://openusd.org/dev/api/pcp_page_front.html
- USD Prototype / Instancing: https://openusd.org/release/api/class_usd_prim.html#prototype
- IFC4.x IfcTypeObject: https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2/HTML/schema/ifckernel/lexical/ifctypeobject.htm
- IFCX Hello Wall: `03 Reference Examples/`
- IFC-ECS Hello Wall: `03 Reference Examples/`
- JSON Schema (for approach 4.3): https://json-schema.org/
- buildingSMART IFC5-development: https://github.com/buildingSMART/IFC5-development


---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) · [📝 Google Doc](https://docs.google.com/document/d/15FBR8_JsY504a8fAH_vg5av5kkZH8FNeb2ce_0tPyAg/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-040) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-040+%E2%80%94+&labels=IFC5-040&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeUzq6dz0OlETzYhZIgeFc8lEbb0kR1lh0cSDAPYOWAeq2zEg/viewform)
