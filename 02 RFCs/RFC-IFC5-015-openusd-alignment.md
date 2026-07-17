
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-015](https://docs.google.com/forms/d/e/1FAIpQLSfeT1hP68vz2wS0j9TRb6ceWd7UXQr__kn95Vu0J5LGANV3FQ/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1p0GsubNCCqZvrdIvLClrfdAVGKIRoxtLa3wkpHxLbrg/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-015">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-015+%E2%80%94+&labels=IFC5-015&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSfeT1hP68vz2wS0j9TRb6ceWd7UXQr__kn95Vu0J5LGANV3FQ/viewform">📋 Take the feedback form</a></td>
</tr></table>


# RFC-IFC5-015: OpenUSD Alignment

| Field | Value |
|---|---|
| **Decision ID** | IFC5-015 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-007, IFC5-014 |
| **Prototype Required** | Yes |
| **Source Topics** | Topics 31, 33 |

---

## 1. Problem Statement

IFCX uses USD-derived concepts (prim-like nodes, usd::usdgeom::mesh, usd::xformop, inherits arcs). The degree of alignment is not defined: is USD compatibility syntactic (IFCX uses USD schema names), semantic (IFCX data can be processed by a USD runtime), or merely conceptual (IFCX borrows USD ideas but is not USD-compatible)?

The answer determines whether IFC5 files can be losslessly converted to .usda/.usdc, and whether USD tooling (Hydra, usdview) can be used with IFC5 data.

## 2. Background

OpenUSD is a rich scene description framework developed by Pixar and now an ASWF standard. It has schema definitions, composition arcs, time samples, variants, and an extensive geometry and material schema library. IFCX uses some USD schema names (usd::usdgeom::mesh) but the semantics of USD composition arcs in an IFC context are not fully specified.

## 3. Existing IFC4.x Convention

No USD alignment. IFC4.x predates USD's open-source release as an industry format.

## 4. Proposed Approaches

### 4.1 Conceptual alignment only

IFCX borrows USD vocabulary (prim paths, schemas, inherits) but is not a valid USD file. No guarantee that USD tooling can process IFCX files.

### 4.2 USD-compatible subset

IFCX files, when generated with a USD-compatible profile, are valid USD files. USD composition arcs follow USD semantics. IFC semantics are authored as USD Applied API Schemas.

### 4.3 Bidirectional lossless conversion

A normative specification defines lossless conversion between IFCX and USD. Not all IFC concepts need a USD equivalent, but the conversion is defined and reversible.

### 4.4 USD as the physical format

IFCX is abandoned; IFC5 uses native USD (.usda/.usdc) with IFC semantics expressed as Applied API Schemas. Maximum USD compatibility; potentially loses IFC-specific expressiveness.

## 5. Tradeoffs

| Dimension | Conceptual | USD subset | Bidirectional | USD native |
|---|---|---|---|---|
| USD tooling usability | None | High | Moderate | Full |
| IFC expressiveness | Full | Constrained | Full | Constrained |
| Governance independence | Full | Partial | Partial | None (tied to USD) |
| Implementer complexity | Low | High | High | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Which USD concepts does IFC5 commit to adopting normatively: prims, schemas, inherits, references, payloads, variantSets, time samples?

**Q2.** If IFCX uses `usd::usdgeom::mesh`, must the attributes follow UsdGeomMesh semantics exactly?

**Q3.** Can an IFCX file with full IFC semantics be opened in usdview or processed by a USD runtime?

**Q4.** How does IFC5 governance relate to USD governance? Who controls schema evolution when both standards evolve?

## 8. Prototype

- **Required:** Yes
- **Notes:** Take Hello Wall IFCX and attempt to open it in usdview. Document what works, what fails, and what is lost.

## 9. Consequences

- Determines feasibility of USD-based visualization tools for IFC5
- Affects geometry encoding choices (IFC5-014)
- Shapes composition and inheritance semantics (IFC5-010)

## 10. References

- OpenUSD documentation: https://openusd.org
- ASWF OpenUSD Working Group
- USD Applied API Schemas documentation


---

💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-015) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-015+%E2%80%94+&labels=IFC5-015&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%

---

<!-- rfc-nav -->
<table><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md">📄 GitHub MD</a></td>
<td><a href="https://docs.google.com/document/d/1p0GsubNCCqZvrdIvLClrfdAVGKIRoxtLa3wkpHxLbrg/edit">📝 Google Doc</a></td>
</tr><tr>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-015">💬 View all discussions</a></td>
<td><a href="https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-015+%E2%80%94+&labels=IFC5-015&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A">+ New discussion</a></td>
</tr><tr>
<td colspan="2" align="center"><a href="https://docs.google.com/forms/d/e/1FAIpQLSfeT1hP68vz2wS0j9TRb6ceWd7UXQr__kn95Vu0J5LGANV3FQ/viewform">📋 Take the feedback form</a></td>
</tr></table>
