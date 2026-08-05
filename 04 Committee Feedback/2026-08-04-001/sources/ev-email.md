# Committee Discussion Summary
**Author:** Ev
**Date:** 2026-08-04
**Source:** Email summary

## A. Paths and hierarchy (probably not a problem)

As TK mentions, nothing stops the same entity from appearing under two different trees at once. The path is "not its identity, but an address." The paper's statement that IFCX creates a closed-world assumption isn't a missing feature — it's a missing example. **Action:** Publish a Hello Wall variant with two simultaneous hierarchies pointing at the same UUID.

## B. Conflict resolution (the real gotcha)

Everyone agrees "one opinion silently winning" will never be the modus operandi of IFCX. However, the schema defines `ProvenanceAuthority` as literally setting an override order: survey beats as-built beats design-intent beats inferred. That's a precedence rule living in the same document that says there isn't one. If building toward a conformance suite, "what's the height of wall W?" needs one defined, testable answer. **Action:** Decide — retain every opinion + who asserted it, define one normative default for plain queries, let consumers declare a different policy if needed.

## C. Relationships (genuinely unresolved)

Some believe IfcRel* shouldn't come back — components with identity and provenance already provide the modularity IfcRels used to provide. Others want them explicitly for lossless coverage of the 30+ IfcRel* families, especially many-to-many cases: material associations, groupings, interference checks. **Action:** Side-by-side comparison of 2-3 concrete many-to-many relationships, both approaches.

## D. Transform bug (new bug, good acid test)

In the paper's IFCY Hello Wall example, windows get moved to be children of the storey instead of the wall, but keep their original transform matrices. This only works because the wall has an identity transform. If the wall were rotated, the windows would render in the wrong place. **Action:** Any spatial-view design must show it working on a Hello Wall variant with a non-identity wall transform.

## E. Component id/versioning

Every component carries an `id`, none ever referenced — no way to mark one component as superseding another. Louis's fix: hash canonical content (JCS + SHA-256) so derived/cached components report fresh/stale/unknown. **Action:** Take a decision and log it.

## Other loose ends

- Spatial structure vs. physical position not always the same (infrastructure) — needs its own test case
- Minimal mesh representation independent of USD — decide the group's position

## Next steps

1. Accept/Reject Louis's three-part resolution proposal
2. Side-by-side comparison of 2-3 IfcRel* many-to-many cases
3. Decide on component content hashing
4. Run reference examples against their schema before debates — new standing habit
