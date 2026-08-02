/**
 * ifc5-schema.ts
 * TypeScript schema for the IFC5 Package format.
 *
 * Proposed in: "Toward a Component-Based, Open-World Architecture for IFC5"
 * Architecture layers:
 *   Layer 1   — JSON/JS data primitives
 *   Layer 1.5 — Component primitive + Package envelope + Provenance
 *   Layer 2   — IFC4X business logic as typed components (identity, psets, relations)
 *   Layer 3   — Views, Typicals, Instances, Materialised Snapshots
 */

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 1  —  Primitive type aliases
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/** UUID v4 — canonical, stable entity identity. Never repurposed. */
export type UUID = string;

/** URI / IRI string */
export type URI = string;

/** ISO 8601 datetime, e.g. "2026-07-31T00:00:00Z" */
export type ISO8601DateTime = string;

/**
 * 4×4 column-major transform matrix (OpenUSD convention).
 * Row 3 carries translation: [[r0],[r1],[r2],[tx,ty,tz,1]]
 */
export type Matrix4x4 = [
  [number, number, number, number],
  [number, number, number, number],
  [number, number, number, number],
  [number, number, number, number]
];

/** RGB colour triple, each channel in [0, 1] */
export type RGB = [number, number, number];

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Three-state attribute semantics
//
//   T value  = known
//   null     = explicitly unknown / intentionally absent
//   key absent = out of scope for this package / not asserted
//
// TypeScript cannot enforce the absent case in object types; use `undefined`
// as a stand-in when constructing objects programmatically.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

export type ThreeState<T> = T | null | undefined;

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 1.5 — Core reference and value types
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/** Local entity reference — points to an entity in this package by UUID */
export interface LocalRef {
  ref: UUID;
  /**
   * Optional path segment label for use in spatial view reconstruction.
   * Present on `relatedObjects`/`relatedElements` entries of containment IfcRels
   * (IfcRelAggregates, IfcRelContainedInSpatialStructure) and on the `root` ref
   * of an ifc:SpatialView descriptor.
   * When absent, the related entity's own `name` attribute is used as fallback.
   * See RFC-IFC5-004 and IFC5-Path-Model-Architecture-Discussion.md.
   */
  pathLabel?: string;
}

/** External URI reference — points to a resource outside this package */
export interface ExternalRef {
  ref: URI;
  /** When the external resource was last fetched (for cache-busting / audit) */
  fetchedAt: ISO8601DateTime;
  version?: string;
}

export type Ref = LocalRef | ExternalRef;

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Quantity and taxonomy helpers
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * Quantity with an explicit UCUM unit code.
 * Replaces the proprietary IFC4X measure types (IfcLengthMeasure, etc.).
 * Examples: { value: 3.0, unit: "m" }  { value: 529, unit: "kg/m3" }
 */
export interface UcumValue {
  value: number;
  /**
   * UCUM unit code — see https://ucum.org/ucum
   * Common codes: "m", "m2", "m3", "kg", "kg/m3", "Pa", "1" (dimensionless),
   *   "kg{CO2e}/m3", "W/(m.K)", "K"
   */
  unit: string;
}

/** bSDD / external taxonomy reference used for class membership */
export interface TaxonomyRef {
  /** bSDD concept URI — used for subtype polymorphism via bSDD hierarchy */
  ref: URI;
  version?: string;
}

/** Entry in an external classification system (NL-SfB, OmniClass, etc.) */
export interface ClassificationEntry {
  code: string;
  uri: URI;
  /** Human-readable system name, e.g. "NL-SfB", "OmniClass", "Uniclass" */
  system: string;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 1.5 — Provenance
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * Epistemic authority levels.
 * Controls which assertions override others when packages are federated.
 * Order (strongest → weakest): survey > as-built > design-intent > inferred
 */
export type ProvenanceAuthority =
  | 'design-intent'       // authored by a designer
  | 'as-built'            // confirmed on site after construction
  | 'survey'              // measured from reality (laser scan, IoT, etc.)
  | 'inferred'            // derived by reasoning, not directly asserted
  | 'ai-generated'        // produced by an AI model
  | 'sensor'              // streamed from a live sensor
  | 'regulatory'          // mandated by code / authority having jurisdiction
  | 'materialized-from'   // resolved/flattened snapshot (derived data)
  | string;               // extensible

export interface Provenance {
  /** URI identifying the asserting party — person, organisation, tool, or service */
  assertedBy: URI;
  /** When this assertion was made */
  assertedAt: ISO8601DateTime;
  authority: ProvenanceAuthority;
  /**
   * For 'materialized-from': UUIDs of the source entities/components from which
   * this assertion was derived. Enables traceability back to authoritative data.
   */
  derivedFrom?: UUID[];
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 1.5 — Component primitive
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * The fundamental semantic unit of IFC5.
 *
 * Each component is an atomic assertion: "entity E has type-T attributes A,
 * asserted by provenance P."
 *
 * Entities can have many components of different types; components of the
 * same type from different packages are federated additively (open world).
 */
export interface IFC5Component {
  /**
   * Component's own stable UUID — optional but recommended.
   * Enables targeted update, versioning, and federation conflict resolution.
   */
  id?: UUID;

  /**
   * Namespaced component type — drives interpretation and schema validation.
   * Format: "<namespace>:<TypeName>"
   * Examples: "ifc:IfcWallIdentity", "usd:MeshGeometry", "nlsfb:Classification"
   */
  type: string;

  /**
   * UUID of the entity this component describes.
   * Absent only for package-level components (e.g. SpatialView on the package itself).
   */
  entity?: UUID;

  /** Type-specific attribute payload */
  attributes: Record<string, unknown>;

  /**
   * Component-level provenance — overrides package-level provenance.
   * Absent = inherit package provenance.
   */
  provenance?: Provenance;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 1.5 — Package envelope
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

export interface SchemaImport {
  /** Canonical URI for this namespace */
  uri: URI;
  description?: string;
}

/**
 * IFC5Package — the top-level transmission unit.
 *
 * A package carries a provenance block that is inherited by every component
 * in data[] that does not declare its own provenance. This makes the common
 * case (single-author, single-authority file) concise while still supporting
 * mixed-authority packages where individual components carry their own provenance.
 */
export interface IFC5Package {
  /** Format version sentinel */
  ifcPackage: '1.0';
  /** This package's canonical UUID */
  id: UUID;
  /** Default provenance, inherited by all components without their own block */
  provenance: Provenance;
  /** Namespace prefix → schema URI mapping */
  schemas: Record<string, SchemaImport>;
  /**
   * Flat, unordered array of all component assertions.
   * Order carries no semantic meaning — consumers should group by entity UUID.
   */
  data: IFC5Component[];
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 2 — Identity components
//
// Each IFC4X entity class becomes a typed identity component.
// The component asserts class membership and carries the bSDD taxonomy URI,
// enabling subtype polymorphism queries without a closed class hierarchy.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

export interface IfcEntityIdentityAttributes {
  name: string | null;
  description?: ThreeState<string>;
  /** bSDD concept URI — drives taxonomy queries and subtype polymorphism */
  taxonomy: TaxonomyRef;
  /** Zero or more external classification system entries */
  classifications?: ClassificationEntry[];
  /**
   * Original IFC-SPF STEP line — enables lossless round-trip to IFC4X (R18).
   * Absent when the entity was not derived from IFC4X source.
   */
  legacyStepRef?: string;
}

export interface IfcProjectIdentityAttributes       extends IfcEntityIdentityAttributes {}
export interface IfcSiteIdentityAttributes           extends IfcEntityIdentityAttributes {}
export interface IfcBuildingIdentityAttributes       extends IfcEntityIdentityAttributes {}
export interface IfcBuildingStoreyIdentityAttributes extends IfcEntityIdentityAttributes {
  elevation?: ThreeState<UcumValue>;
}
export interface IfcSpaceIdentityAttributes          extends IfcEntityIdentityAttributes {
  predefinedType?: ThreeState<string>;
}
export interface IfcWallIdentityAttributes           extends IfcEntityIdentityAttributes {}
export interface IfcWallTypeIdentityAttributes       extends IfcEntityIdentityAttributes {
  predefinedType?: ThreeState<string>;
}
export interface IfcWindowIdentityAttributes         extends IfcEntityIdentityAttributes {
  predefinedType?: ThreeState<string>;
}
export interface IfcWindowTypeIdentityAttributes     extends IfcEntityIdentityAttributes {
  predefinedType?: ThreeState<string>;
  partitioningType?: ThreeState<string>;
}
export interface IfcOpeningElementIdentityAttributes extends IfcEntityIdentityAttributes {
  predefinedType?: ThreeState<string>;
}

export interface IfcMaterialIdentityAttributes {
  name: string;
  taxonomy: TaxonomyRef;
  diffuseColor?: RGB;
  /** Opacity 0–1. null = unknown. absent = not specified. */
  opacity?: ThreeState<number>;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 2 — Property set component
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/** Scalar property value types */
export type PropertyScalar = boolean | number | string;

/** A property value: scalar, UCUM quantity, reference, or three-state unknown/absent */
export type PropertyValue = ThreeState<PropertyScalar | UcumValue | Ref>;

/**
 * Property set — maps an entity to a named group of typed properties.
 * Uses UCUM quantities for all numeric values with physical dimensions.
 */
export interface IfcPropertySetAttributes {
  /** psetName matches the IFC4X Pset name, e.g. "Pset_WallCommon" */
  psetName: string;
  properties: Record<string, PropertyValue>;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 2 — Relation components
//
// Design rules:
//   1:many  → component on the "relating" (1) entity; array of refs to the many
//   1:1     → component on the dependent entity; single ref to the relating
//   M:N     → dedicated relation entity with identity component; both sides ref it
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/** IfcRelAggregates — on the aggregate, lists its decomposed parts */
export interface IfcRelAggregatesAttributes {
  name?: string;
  /**
   * Each ref may carry an optional `pathLabel` — the path segment name for
   * this child in any SpatialView that includes ifc:IfcRelAggregates.
   * When absent, the related entity's own `name` attribute is used as fallback.
   */
  relatedObjects: LocalRef[];
}

/** IfcRelContainedInSpatialStructure — on the containing structure */
export interface IfcRelContainedInSpatialStructureAttributes {
  name?: string;
  /**
   * Each ref may carry an optional `pathLabel` — the path segment name for
   * this element in any SpatialView that includes ifc:IfcRelContainedInSpatialStructure.
   * When absent, the related entity's own `name` attribute is used as fallback.
   */
  relatedElements: LocalRef[];
}

/** IfcRelDefinesByType — on the type entity, lists instances of this type */
export interface IfcRelDefinesByTypeAttributes {
  name?: string;
  relatedObjects: LocalRef[];
}

/** IfcRelDefinesByProperties — on the element being defined */
export interface IfcRelDefinesByPropertiesAttributes {
  name?: string;
  /** Reference to a pset name string, or an inline property set definition */
  relatingPropertyDefinition: string | IfcPropertySetAttributes;
}

/** IfcRelVoidsElement — on the voided element, lists its openings (1:many) */
export interface IfcRelVoidsElementAttributes {
  name?: string;
  relatedOpeningElements: LocalRef[];
}

/**
 * IfcRelFillsElement — on the filling element (1:1 to its opening).
 * Pattern: component on the dependent (window), pointing to its opening.
 */
export interface IfcRelFillsElementAttributes {
  name?: string;
  relatingOpeningElement: LocalRef;
}

/** IfcRelAssociatesMaterial — on the material entity, listing associated elements */
export interface IfcRelAssociatesMaterialAttributes {
  name?: string;
  /** Semantic role, e.g. "wall-body", "window-frame", "window-glazing" */
  materialRole?: string;
  relatedObjects: LocalRef[];
}

export type SpaceBoundaryType = 'PHYSICAL' | 'VIRTUAL' | 'NOTDEFINED';
export type SpaceBoundaryExternal =
  | 'INTERNAL' | 'EXTERNAL' | 'EXTERNAL_EARTH'
  | 'EXTERNAL_WATER' | 'EXTERNAL_FIRE' | 'NOTDEFINED';

/** IfcRelSpaceBoundary — on the relating space, one component per bounded surface */
export interface IfcRelSpaceBoundaryAttributes {
  name?: string;
  physicalOrVirtualBoundary: SpaceBoundaryType;
  internalOrExternalBoundary: SpaceBoundaryExternal;
  /** null = virtual boundary with no physical element */
  relatedBuildingElement: LocalRef | null;
  /** Reference to a geometry entity describing the boundary surface */
  connectionGeometryBody?: LocalRef;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 3 — Spatial view component
//
// Paths are navigational views — they do NOT define entity identity.
// Entity identity is always the UUID. Multiple views can coexist.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * IfcSpatialView — a named, navigational organisation of entities.
 *
 * Acts as a lightweight descriptor: it names the view, anchors its root,
 * and declares which relation types constitute the view graph. The actual
 * parent-child topology is carried by the referenced IfcRel components
 * (e.g. IfcRelAggregates, IfcRelContainedInSpatialStructure), not duplicated here.
 *
 * For custom views with no matching IfcRel type, `children` provides a fallback
 * explicit path→UUID map.
 *
 * Multiple SpatialView components may coexist — one per named organisational view
 * (spatial, structural, phase, cost breakdown, etc.).
 *
 * See RFC-IFC5-004 and IFC5-Path-Model-Architecture-Discussion.md for the full
 * alternatives analysis and directionality tradeoffs.
 */
export interface IfcSpatialViewAttributes {
  /** Machine-readable view name, unique within the package */
  name: string;
  description?: string;
  /**
   * The root entity of this view.
   * The optional `pathLabel` on this ref is the path segment name for the root
   * entity (e.g. "My_Project"). When absent, the entity's `name` attribute is used.
   */
  root: LocalRef;
  /**
   * Declares which IfcRel component types constitute the view graph.
   * The view is the subgraph of all components of these types, traversed
   * from `root` following `relatedObjects`/`relatedElements` refs.
   *
   * For the default IFC spatial view:
   *   ["ifc:IfcRelAggregates", "ifc:IfcRelContainedInSpatialStructure"]
   *
   * Mutually exclusive with `children` — use one or the other.
   */
  composedFrom?: string[];
  /**
   * Explicit path → UUID map. Fallback for custom organisational views
   * where no IfcRel type covers the required hierarchy.
   * Paths use '/' as separator; must be unique within the map.
   *
   * Mutually exclusive with `composedFrom` — use one or the other.
   */
  children?: Record<string, UUID>;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 3 — Typical and instance components
//
// IfcTypical replaces both IfcTypeObject (IFC4X) and the `inherits` arc (IFCX).
// Instances declare themselves via IfcInstantiates and carry only overrides.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * A named slot in an IfcTypical that instances may inherit or override.
 */
export interface ComponentTemplate {
  /** Slot identifier — unique within this Typical */
  slotName: string;
  /** Component type this slot instantiates, e.g. "ifc:IfcPropertySet" */
  type: string;
  /**
   * true  = instances get this component automatically (no need to re-declare)
   * false = instances must explicitly opt in
   */
  inheritable: boolean;
  /** Default attribute values; instances may override individual keys */
  attributes: Record<string, unknown>;
  /**
   * true (default) = instance can override individual attribute keys.
   * false          = slot is frozen; instances cannot override it.
   */
  overridable?: boolean;
}

/**
 * IfcTypical — a parametric template for a family of instances.
 *
 * The Typical entity carries the "type-level" components once.
 * Instances reference it via IfcInstantiates and only declare
 * what differs (typically just the placement transform).
 *
 * This resolves three IFCX issues:
 *   1. `inherits` is ambiguous (prototype vs. aggregation)
 *   2. Closed-world: the singular scene graph bakes type resolution into paths
 *   3. AI cannot consume the data without resolving the arc first (→ use MaterialisedSnapshot)
 */
export interface IfcTypicalAttributes {
  name: string;
  description?: ThreeState<string>;
  taxonomy?: TaxonomyRef;
  componentTemplates: ComponentTemplate[];
}

/**
 * IfcInstantiates — declares that this entity is an instance of a Typical.
 * The entity only carries components that differ from the Typical's templates.
 * All inheritable templates are implicitly present on the instance.
 */
export interface IfcInstantiatesAttributes {
  /** The Typical this entity instantiates */
  typical: LocalRef;
  description?: string;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// GEOMETRY COMPONENTS (USD carry-through)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/** USD-compatible triangulated mesh */
export interface UsdMesh {
  faceVertexIndices: number[];
  /** Vertex positions [x, y, z] in metres */
  points: [number, number, number][];
}

/** USD-compatible basis curve */
export interface UsdCurve {
  points: [number, number, number][];
}

export interface MeshGeometryAttributes {
  mesh: UsdMesh;
  representationIdentifier?: string;
  visibility?: 'visible' | 'invisible';
  /** Material entity for this geometry node */
  material?: LocalRef;
}

export interface CurveGeometryAttributes {
  curve: UsdCurve;
  representationIdentifier?: string;
}

/**
 * IfcShapeRepresentation — links an IFC element to its geometry entity nodes.
 * One component per representation context (Body, Axis, Directrix, Basis, Void…)
 */
export interface IfcShapeRepresentationAttributes {
  /** IFC representation identifier, e.g. "Body", "Axis", "Void", "Basis" */
  representationIdentifier: string;
  /** IFC representation type, e.g. "SolidModel", "Curve2D", "Surface" */
  representationType: string;
  items: LocalRef[];
}

/** USD transform — 4×4 column-major matrix; translation in row 3 */
export interface XformComponentAttributes {
  representationIdentifier?: string;
  transform: Matrix4x4;
}

/** Presentation style (colour + opacity) for a geometry entity */
export interface IfcPresentationStyleAttributes {
  diffuseColor?: RGB;
  /** Opacity 0–1. null = unknown. absent = opaque assumed. */
  opacity?: ThreeState<number>;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// LAYER 3 — Materialised snapshot component
//
// Pre-resolved, fully flattened read-model of a Typical instance.
// For AI consumption and query engines that cannot evaluate composition arcs.
// MUST carry provenance.authority = 'materialized-from' with derivedFrom set.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

export interface MaterialisedSnapshotAttributes {
  /** Name of the Typical from which this snapshot was resolved */
  resolvedFrom: string;
  /** Timestamp of resolution */
  resolvedAt: ISO8601DateTime;
  /**
   * Fully flattened attribute map — Typical templates + instance overrides merged.
   * Keys match the attribute names in the underlying component types.
   * This is the authoritative flat view for AI and query engines.
   */
  snapshot: Record<string, unknown>;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Discriminated union over all known component types
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

type Base = { id?: UUID; entity?: UUID; provenance?: Provenance };

export type IFC5TypedComponent =
  // Layer 2: Identity
  | (Base & { type: 'ifc:IfcProjectIdentity';          attributes: IfcProjectIdentityAttributes })
  | (Base & { type: 'ifc:IfcSiteIdentity';             attributes: IfcSiteIdentityAttributes })
  | (Base & { type: 'ifc:IfcBuildingIdentity';         attributes: IfcBuildingIdentityAttributes })
  | (Base & { type: 'ifc:IfcBuildingStoreyIdentity';   attributes: IfcBuildingStoreyIdentityAttributes })
  | (Base & { type: 'ifc:IfcSpaceIdentity';            attributes: IfcSpaceIdentityAttributes })
  | (Base & { type: 'ifc:IfcWallIdentity';             attributes: IfcWallIdentityAttributes })
  | (Base & { type: 'ifc:IfcWallTypeIdentity';         attributes: IfcWallTypeIdentityAttributes })
  | (Base & { type: 'ifc:IfcWindowIdentity';           attributes: IfcWindowIdentityAttributes })
  | (Base & { type: 'ifc:IfcWindowTypeIdentity';       attributes: IfcWindowTypeIdentityAttributes })
  | (Base & { type: 'ifc:IfcOpeningElementIdentity';   attributes: IfcOpeningElementIdentityAttributes })
  | (Base & { type: 'ifc:IfcMaterialIdentity';         attributes: IfcMaterialIdentityAttributes })
  | (Base & { type: 'ifc:IfcMaterialProperties';       attributes: IfcPropertySetAttributes })
  // Layer 2: Properties
  | (Base & { type: 'ifc:IfcPropertySet';              attributes: IfcPropertySetAttributes })
  // Layer 2: Relations
  | (Base & { type: 'ifc:IfcRelAggregates';                        attributes: IfcRelAggregatesAttributes })
  | (Base & { type: 'ifc:IfcRelContainedInSpatialStructure';        attributes: IfcRelContainedInSpatialStructureAttributes })
  | (Base & { type: 'ifc:IfcRelDefinesByType';                      attributes: IfcRelDefinesByTypeAttributes })
  | (Base & { type: 'ifc:IfcRelDefinesByProperties';                attributes: IfcRelDefinesByPropertiesAttributes })
  | (Base & { type: 'ifc:IfcRelVoidsElement';                       attributes: IfcRelVoidsElementAttributes })
  | (Base & { type: 'ifc:IfcRelFillsElement';                       attributes: IfcRelFillsElementAttributes })
  | (Base & { type: 'ifc:IfcRelAssociatesMaterial';                 attributes: IfcRelAssociatesMaterialAttributes })
  | (Base & { type: 'ifc:IfcRelSpaceBoundary';                      attributes: IfcRelSpaceBoundaryAttributes })
  // Layer 3: Views
  | (Base & { type: 'ifc:SpatialView';                 attributes: IfcSpatialViewAttributes })
  // Layer 3: Typicals
  | (Base & { type: 'ifc:IfcTypical';                  attributes: IfcTypicalAttributes })
  | (Base & { type: 'ifc:IfcInstantiates';             attributes: IfcInstantiatesAttributes })
  // Geometry
  | (Base & { type: 'ifc:IfcShapeRepresentation';      attributes: IfcShapeRepresentationAttributes })
  | (Base & { type: 'ifc:IfcPresentationStyle';        attributes: IfcPresentationStyleAttributes })
  | (Base & { type: 'usd:MeshGeometry';                attributes: MeshGeometryAttributes })
  | (Base & { type: 'usd:CurveGeometry';               attributes: CurveGeometryAttributes })
  | (Base & { type: 'usd:XformComponent';              attributes: XformComponentAttributes })
  // Layer 3: Snapshots
  | (Base & { type: 'ifc:MaterialisedSnapshot';        attributes: MaterialisedSnapshotAttributes })
  // Open extension — any schema can add types; the format is not closed
  | (Base & { type: string;                            attributes: Record<string, unknown> });

/** Typed package — same as IFC5Package but with the discriminated component union */
export interface IFC5TypedPackage extends Omit<IFC5Package, 'data'> {
  data: IFC5TypedComponent[];
}
