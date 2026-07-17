<!-- rfc-links -->
> **IFC5-005 — Namespace and Qualified Names** · Tier 1 — Foundational
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-005) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-005+%E2%80%94+&labels=IFC5-005&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-005](https://docs.google.com/forms/d/e/1FAIpQLSdYaCRFZulAgTeWYwEkjW2c3kUQjVF2KAlnccJTAGyz2WybyA/viewform)** — answer the open questions and leave comments directly.


# RFC-IFC5-005: Namespace and Qualified Names

| Field | Value |
|---|---|
| **Decision ID** | IFC5-005 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | IFC5-002 |
| **Prototype Required** | No |
| **Source Topics** | Topics 6, 7 |

---

## 1. Problem Statement

IFCX uses `::` as a delimiter in qualified names (e.g., `bsi::ifc::class`, `usd::usdgeom::mesh`, `nlsfb::class`). The formal semantics of this delimiter, the mapping between namespace segments and schema imports, and the rules for collision avoidance are not defined.

## 2. Background

In IFCX examples, qualified names appear to function as both semantic identifiers and schema-path references. It is unclear whether `bsi::ifc::class` means "the `class` attribute defined in the `bsi::ifc` schema" or "a semantic concept in the bsi/ifc vocabulary."

## 3. Existing IFC4.x Convention

No namespace concept. All attribute and entity names are globally unique within the EXPRESS schema.

## 4. Proposed Approaches

### 4.1 Namespace as schema-import alias

`::` segments map directly to import aliases declared in the file header. `bsi::ifc` resolves to the imported `bsi/ifc` package. Every qualified attribute must originate in an imported schema.

### 4.2 Namespace as URI prefix

`::` segments expand to URI prefixes (similar to JSON-LD `@context`). `bsi::ifc::class` expands to `https://standards.buildingsmart.org/ifc/class`. Enables linked-data compatibility.

### 4.3 Namespace as organizational convention only

`::` is a naming convention for human disambiguation. No formal parsing rules. Does not require import declarations.

## 5. Tradeoffs

| Dimension | Schema-import alias | URI prefix | Convention only |
|---|---|---|---|
| Formal validation support | High | High | Low |
| Linked-data compatibility | Low | High | None |
| Tooling simplicity | Moderate | Moderate | High |
| Offline operation | Depends on imports | Depends on URIs | High |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Are namespace segments case-sensitive?

**Q2.** Can local (unqualified) attribute names coexist with qualified names?

**Q3.** Must every attribute that appears in an IFCX file be traceable to an imported schema?

**Q4.** How are naming conventions standardized for: schemas, attributes, classes, properties, geometry fields, classification systems?

**Q5.** Does `bsi::ifc::prop::TypeName` mean the property named TypeName in the bsi::ifc::prop schema, or the property whose value is a TypeName?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Determines how schema packages are declared (IFC5-012)
- Affects property set encoding (IFC5-013)
- Affects classification integration (related to material and property RFCs)

## 10. References

- IFCX Hello Wall examples
- JSON-LD @context specification


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-005) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-005+%E2%80%94+&labels=IFC5-005&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
