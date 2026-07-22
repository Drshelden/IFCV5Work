
# RFC-IFC5-042: Alignment with External Domain Data Standards

| Field | Value |
|---|---|
| **Decision ID** | IFC5-042 |
| **Status** | Idea |
| **Tier** | 4 — Process & Governance |
| **Owner** | TBD |
| **Dependencies** | [IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md), [IFC5-012](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md), [IFC5-020](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-020-model-views-exchange.md), [IFC5-027](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md), [IFC5-032](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md), [IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) |
| **Prototype Required** | No |

---

## 1. Problem Statement

Several established data standards from other bodies describe overlapping or adjacent aspects of the built environment: building automation and IoT systems (Brick Schema, Project Haystack, ASHRAE 223P), sensor observations (W3C Web of Things, OGC SensorThings), urban geometry (OGC CityGML / GeoBIM), energy analysis (gbXML), facilities management (COBie), and electrical infrastructure (IEC CIM). Many of these are evolving alongside IFC5 and are in active use in the industry.

IFC5's namespace system and schema import mechanism provide the *technical* means for data from these sources to coexist with IFC5 data. But the technical mechanism does not answer the architectural question: what normative position, if any, does IFC5 take on alignment with these standards?

Without a decision, each software vendor and national implementation will handle cross-standard data differently, producing incompatible approaches even where the underlying standards are compatible. The question is not whether these standards matter — they do — but whether IFC5 defines any normative interoperability story for them, and if so, what form that takes.

---

## 2. Background

### The landscape of overlapping standards

The following standards describe aspects of the built environment that IFC5 also covers or is adjacent to. This is not exhaustive but represents the most active sources of potential alignment:

**Building automation and IoT semantics**

- **Brick Schema** (brickschema.org) — An RDF-based building metadata schema covering HVAC, lighting, electrical, and plumbing systems. Models physical components and their relationships as a graph. Developed by a consortium including UC Berkeley, PNNL, and industry partners. Increasingly used for building analytics and controls interoperability. Aligns well with RDF-based IFC5 representations.
- **Project Haystack** (project-haystack.org) — A tag-based data model for building equipment and sensor data, widely adopted in BAS/BMS products. Version 4 introduced a more structured ontology (Trio/Zinc formats). Less formal than Brick but very broadly deployed.
- **ASHRAE 223P** — A normative ASHRAE standard (currently in public review as of 2025) providing a semantic data model for HVAC and building system connections. Written as an OWL ontology. Intended to work alongside Brick; more normatively rigorous and broader in scope. Directly relevant to MEP system modeling in IFC5.

**Sensor and observation data**

- **W3C Web of Things (WoT)** — A W3C standard for describing IoT devices and their capabilities via "Thing Descriptions" (JSON-LD). Defines semantic descriptions of sensors, actuators, and data streams. Directly relevant to how IFC5 objects refer to or embed live sensor data.
- **OGC SensorThings API** — OGC standard for observational data: sensors, observations, and datastreams. Provides REST/MQTT access patterns. The semantic model (based on OGC Observations & Measurements) is distinct from but compatible with WoT.

**Urban and geospatial**

- **OGC CityGML / GeoBIM** — OGC city-scale geometry and attribute standard, extensively used in urban planning, digital twin platforms, and national spatial data infrastructures. GeoBIM defines mappings between IFC and CityGML; these are informative today. CityGML 3.0 introduced greater semantic alignment with IFC.

**Energy and energy analysis**

- **gbXML** — Green Building XML; a file format for transferring building geometry and properties to energy simulation tools. No formal standards body; maintained by the Green Building Studio consortium. Widely supported in design tools. No formal alignment with IFC exists despite significant overlap.

**Facilities management**

- **COBie** (Construction Operations Building information exchange) — A buildingSMART deliverable (ISO 15686-4 aligned) for FM handover data: spaces, equipment, systems, documents, and spare parts. Currently implemented as a spreadsheet and IFC4 MVD. Whether IFC5 maintains a normative COBie definition is an open question.

**Electrical and energy infrastructure**

- **IEC CIM** (Common Information Model, IEC 61968/61970) — The dominant standard for electrical grid and distribution network data. Growing relevance for building-level electrification, grid-interactive buildings, and on-site generation. No formal IFC alignment exists today.

### IFC4.x and prior work

IFC4.x has no normative alignment with any of these standards. Alignment has been handled ad hoc:
- COBie was originally an MVD for IFC2x3 and IFC4; buildingSMART produces a COBie certification
- gbXML interoperability is via third-party conversion tools (no normative mapping)
- CityGML alignment is addressed in the GeoBIM research project (informative only)
- Brick, Haystack, ASHRAE 223P, WoT, SensorThings, and IEC CIM have no formal connection to IFC

The result is that building data frequently lives in silos: IFC files for geometry and construction data, Brick/Haystack models for BAS/analytics, WoT/SensorThings for sensor streams, and CityGML for urban context — all describing overlapping aspects of the same building with no normative path between them.

---

## 3. Existing IFC4.x Convention

- No normative alignment with external domain data standards
- COBie: implemented as an MVD (exchange constraint on IFC4); maintained by buildingSMART as a certification program
- gbXML: no formal alignment; interoperability via third-party conversion tools
- CityGML: no formal alignment; GeoBIM project provides informative mappings
- Haystack/Brick/ASHRAE 223P/WoT: entirely separate domains with no formal IFC connection
- Extension via custom property sets (Pset_*) is the only IFC4.x mechanism for carrying external vocabulary

---

## 4. Proposed Approaches

### 4.1 No normative position — extension namespaces only

IFC5 takes no position on alignment with external domain standards. Any organization that wishes to embed Brick, Haystack, ASHRAE 223P, WoT, or CityGML data in an IFC5 file may do so via the extension namespace mechanism ([IFC5-032](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md)). buildingSMART does not register, endorse, or maintain mappings for external schemas.

**Implication:** Interoperability with external standards is fully delegated to vendors, national bodies, and interest groups. Multiple incompatible conventions for the same external standard will likely emerge independently.

### 4.2 Recognized external namespace registry

buildingSMART maintains a registry of external standards that have been formally reviewed for namespace registration. Registration means: the external schema is assigned a stable IFC5 namespace prefix (e.g., `brick::`, `wot::`, `ashrae223p::`, `citygml::`) and buildingSMART publishes a brief alignment note documenting the scope and known conflicts. buildingSMART does not own or maintain the external schema; it only stabilizes the namespace reference.

**Implication:** Prevents namespace fragmentation. Does not require buildingSMART to produce or maintain mapping documents. Vendors know which prefix to use for a given external schema; receivers can identify the source reliably.

### 4.3 Normative companion alignment specifications

For a defined set of high-priority external standards, buildingSMART publishes normative alignment specifications as companion documents to IFC5. These are analogous to MVDs: they define how IFC5 and the external standard are used together, what data goes in each, and how to translate between representations. The alignment specification is buildingSMART-governed and carries the same normative weight as the core standard.

**Priority candidates for companion specifications:** COBie (continuity from IFC4), ASHRAE 223P (systems semantics), gbXML (energy analysis), and CityGML/GeoBIM (urban context).

**Implication:** High quality and consistency; high governance burden. Risk of misalignment if the external standard evolves faster than buildingSMART can update the companion spec.

### 4.4 Linked-data convergence as the interoperability surface

IFC5 treats the RDF/linked-data layer (from RFC-[IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md)) as the primary interoperability surface for external domain standards. External standards that have normative RDF representations (Brick, ASHRAE 223P, W3C WoT) are interoperable at the graph level without any IFC5-specific alignment work — they are simply additional named graphs that can be merged with or queried alongside an IFC5 graph. No IFC5-specific namespace registration or mapping specification is needed for standards that already have stable IRIs.

**Implication:** Elegant for RDF-native standards (Brick, ASHRAE 223P, WoT). Does not help for non-RDF standards (Haystack, gbXML, COBie, IEC CIM) without additional conversion work. Depends on RFC-[IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) decision.

### 4.5 Exchange profile alignment (profile per external standard)

IFC5 defines named exchange profiles (from RFC-[IFC5-020](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-020-model-views-exchange.md)) that explicitly incorporate requirements from specific external standards. A "BAS Integration Profile" would define which IFC5 objects carry Brick and/or ASHRAE 223P attributes, how sensor references are encoded, and what validation rules apply. A "GeoBIM Profile" would define how IFC5 relates to CityGML LoD. Profiles are buildingSMART-published and externally co-governed with the relevant standards body where possible.

**Implication:** Tightly couples external standard alignment to the IFC5 MVD/profile mechanism. Requires co-governance with external bodies. Most suitable for exchange scenarios with well-defined scope (e.g., handover to energy analysis, handover to BMS). Less suitable for open-ended alignment.

---

## 5. Tradeoffs

| Dimension | Extension namespaces only | Namespace registry | Companion specs | Linked-data convergence | Exchange profiles |
|---|---|---|---|---|---|
| Governance burden on buildingSMART | None | Low | High | Low | Moderate |
| Consistency across implementations | Low | Moderate | High | High (for RDF standards) | High (within profile scope) |
| Coverage of non-RDF standards | Full (unmanaged) | Full | Selective | Low | Selective |
| External body co-governance required | No | No | Desirable | No | Yes (for some) |
| Risk of vendor fragmentation | High | Moderate | Low | Low | Low |
| Dependency on [RFC-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) decision | None | None | None | High | None |
| Alignment with existing COBie investment | None | Partial | High | Low | High |

---

## 6. Recommendation

*To be filled in after committee discussion.*

The case for at minimum a **namespace registry (4.2)** is strong — it is low-cost, prevents fragmentation, and does not require buildingSMART to take substantive technical positions on external standards. It is compatible with any of the other approaches and can be adopted regardless of the [RFC-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) outcome.

The case for **companion alignment specifications (4.3)** for COBie specifically is also strong, given existing buildingSMART investment and the FM handover use case. Whether ASHRAE 223P, gbXML, and CityGML warrant companion specs is a prioritization question for the committee.

---

## 7. Open Questions

**Q1.** Is the namespace collision problem (multiple vendors using different prefixes for the same external standard) real enough to warrant a registry? Are there existing examples from IFC4x deployments?

**Q2.** Should COBie be treated as an IFC5 exchange profile rather than a separate deliverable? If so, is it a candidate for co-development with FM industry bodies?

**Q3.** Does ASHRAE 223P's OWL ontology align well enough with IFC5's data model that linked-data convergence (4.4) is genuinely sufficient, or are there structural mismatches that require an explicit mapping?

**Q4.** W3C WoT Thing Descriptions are JSON-LD documents. If IFC5 objects can carry `wot::` namespace attributes, can a conformant IFC5 receiver be expected to interpret WoT data — or is WoT interoperability purely a tooling concern outside the scope of IFC5 conformance?

**Q5.** Should buildingSMART seek formal liaison relationships with W3C (WoT), ASHRAE (223P), OGC (CityGML/SensorThings), and the Brick Consortium as part of IFC5 development? What is the governance model for co-produced alignment specifications?

**Q6.** IEC CIM is dominant in grid-interactive building use cases (demand response, on-site generation, grid services). Is this within the scope of IFC5 or explicitly out of scope?

**Q7.** Haystack 4 introduced a formal ontology (Trio format), but Haystack tag sets are also widely deployed in a much looser form. Which representation, if any, should a Haystack alignment target?

---

## 8. Prototype

- **Required:** No
- **Recommended:** A reference example showing an IFC5 object (e.g., an air handling unit) carrying both native IFC5 attributes and `brick::` and `ashrae223p::` attributes in the same document would concretely demonstrate the namespace coexistence question. This could extend the Hello Wall reference examples (03 Reference Examples/) to a simple MEP scenario.

---

## 9. Consequences

- Directly determines the scope and governance model for IFC5's relationship to the BAS/IoT standards landscape
- Constrains or enables how COBie is handled in IFC5 (replaces or informs a COBie-specific decision)
- Informs namespace registration governance in RFC-[IFC5-032](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md) (Extensibility)
- Depends on and may constrain the RFC-[IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) (Linked Data) decision
- May require buildingSMART to establish new liaison relationships with W3C, ASHRAE, OGC, and the Brick Consortium

---

## 10. References

- Brick Schema: https://brickschema.org/
- ASHRAE 223P (draft standard): https://www.ashrae.org/technical-resources/standards-and-guidelines/read-only-versions-of-ashrae-standards
- W3C Web of Things (WoT) Thing Description: https://www.w3.org/TR/wot-thing-description/
- Project Haystack: https://project-haystack.org/
- OGC SensorThings API: https://www.ogc.org/standards/sensorthings
- OGC CityGML 3.0: https://www.ogc.org/standards/citygml
- GeoBIM (IFC–CityGML alignment): https://www.geobim-benchmark.org/
- gbXML: https://gbxml.org/
- COBie (ISO 15686-4): https://www.buildingsmart.org/standards/bsi-standards/cobie/
- IEC CIM (IEC 61968/61970): https://www.iec.ch/
- ifcOWL (for context on prior linked-data work): https://technical.buildingsmart.org/resources/ifcowl/

---

*IFC5 Architecture Initiative · July 2026 · Status: Idea — not yet in Open Review*
