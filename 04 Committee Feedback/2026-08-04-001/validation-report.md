# Validation Report — Batch 2026-08-04-001

**Generated:** 2026-08-05 00:52 UTC  

**Examples validated:** 1


### Example: `hello-wall-ifcy`

**JSON file:** `/sessions/focused-magical-knuth/mnt/IFCV5/repo/03 Reference Examples/Hello-Wall/hello-wall-ifcy.json`  
**Schema:** `/sessions/focused-magical-knuth/mnt/IFCV5/ifc5-layered-schema.ts`

*Schema interfaces found: 43; type aliases: 13*

| Check | Status | Detail |
|-------|--------|--------|
| Namespace prefix check | ✅ PASS | All CURIE prefixes declared in package.schemas ({'usd', 'ifc', 'nlsfb'}) |
| Entity reference check | ✅ PASS | All ref values match known component ids (65 checked) |
| SpatialView mutual exclusion | ✅ PASS | No SpatialView mutual-exclusion violations found |
| pathLabel location check | ✅ PASS | pathLabel fields only appear in allowed relationship types |
| UUID format check | ✅ PASS | All id/ref fields match UUID pattern |
| Component id uniqueness | ✅ PASS | All 64 component ids are unique |
| Root ref check | ✅ PASS | All SpatialView root.ref values match known component ids |

**Overall result:** ✅ PASS