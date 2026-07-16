#!/usr/bin/env bash
# create_github_labels.sh
# Creates all RFC labels and category labels for https://github.com/Drshelden/IFCV5Work
#
# Prerequisites:
#   gh CLI installed and authenticated (gh auth login)
#
# Usage:
#   bash create_github_labels.sh

REPO="Drshelden/IFCV5Work"

GH_BIN="$(command -v gh 2>/dev/null || command -v gh.exe 2>/dev/null || true)"
if [ -z "$GH_BIN" ]; then
	echo "gh CLI not found in PATH. Install GitHub CLI or ensure gh.exe is available." >&2
	exit 1
fi

gh() {
	"$GH_BIN" "$@"
}

# ── Tier labels ────────────────────────────────────────────────────────────────
gh label create "tier-1-foundational"       --repo $REPO --color "B60205" --description "Tier 1 — Foundational RFCs" --force
gh label create "tier-2-core-architecture"  --repo $REPO --color "D93F0B" --description "Tier 2 — Core Architecture RFCs" --force
gh label create "tier-3-domain-modeling"    --repo $REPO --color "E4E669" --description "Tier 3 — Domain Modeling RFCs" --force
gh label create "tier-4-governance"         --repo $REPO --color "0075CA" --description "Tier 4 — Process & Governance RFCs" --force

# ── Process labels ─────────────────────────────────────────────────────────────
gh label create "general-approach"    --repo $REPO --color "7057FF" --description "Feedback on the overall RFC process and approach" --force
gh label create "new-rfc-proposal"    --repo $REPO --color "008672" --description "Proposal for a new RFC not in the current list" --force
gh label create "rfc-priority-poll"   --repo $REPO --color "E99695" --description "RFC prioritization input" --force
gh label create "prototype"           --repo $REPO --color "F9D0C4" --description "Related to a prototype implementation" --force
gh label create "blocking-objection"  --repo $REPO --color "B60205" --description "Blocking objection — RFC cannot advance as written" --force

# ── RFC labels — Tier 1 ────────────────────────────────────────────────────────
gh label create "IFC5-001" --repo $REPO --color "B60205" --description "Strategic Architecture Mode" --force
gh label create "IFC5-002" --repo $REPO --color "B60205" --description "Normative Information Model Formalism" --force
gh label create "IFC5-003" --repo $REPO --color "B60205" --description "Identity Model" --force
gh label create "IFC5-004" --repo $REPO --color "B60205" --description "Path Model and Addressing" --force
gh label create "IFC5-005" --repo $REPO --color "B60205" --description "Namespace and Qualified Names" --force
gh label create "IFC5-006" --repo $REPO --color "B60205" --description "Serialization and Encoding" --force

# ── RFC labels — Tier 2 ────────────────────────────────────────────────────────
gh label create "IFC5-007" --repo $REPO --color "D93F0B" --description "Scene Graph vs. ECS vs. Hybrid Architecture" --force
gh label create "IFC5-008" --repo $REPO --color "D93F0B" --description "Relationship Modeling Strategy" --force
gh label create "IFC5-009" --repo $REPO --color "D93F0B" --description "Class and Type Representation" --force
gh label create "IFC5-010" --repo $REPO --color "D93F0B" --description "Composition, Inheritance, and Instancing" --force
gh label create "IFC5-011" --repo $REPO --color "D93F0B" --description "Document-Level Structure" --force
gh label create "IFC5-012" --repo $REPO --color "D93F0B" --description "Modular Schema Imports" --force
gh label create "IFC5-023" --repo $REPO --color "D93F0B" --description "Attribute Representation" --force
gh label create "IFC5-024" --repo $REPO --color "D93F0B" --description "Type System, Primitives, Enumerations, SELECTs" --force
gh label create "IFC5-025" --repo $REPO --color "D93F0B" --description "Collections and Cardinality" --force

# ── RFC labels — Tier 3 ────────────────────────────────────────────────────────
gh label create "IFC5-013" --repo $REPO --color "FBCA04" --description "Property Sets and Properties" --force
gh label create "IFC5-014" --repo $REPO --color "FBCA04" --description "Geometry Architecture" --force
gh label create "IFC5-015" --repo $REPO --color "FBCA04" --description "OpenUSD Alignment" --force
gh label create "IFC5-016" --repo $REPO --color "FBCA04" --description "Spatial Structure and Decomposition" --force
gh label create "IFC5-017" --repo $REPO --color "FBCA04" --description "Material Modeling" --force
gh label create "IFC5-026" --repo $REPO --color "FBCA04" --description "Openings, Voids, and Fillings" --force
gh label create "IFC5-027" --repo $REPO --color "FBCA04" --description "Classification and External Dictionaries" --force
gh label create "IFC5-028" --repo $REPO --color "FBCA04" --description "Units and Measures" --force
gh label create "IFC5-029" --repo $REPO --color "FBCA04" --description "Presentation and Appearance" --force
gh label create "IFC5-030" --repo $REPO --color "FBCA04" --description "Space Boundaries and Topology" --force
gh label create "IFC5-031" --repo $REPO --color "FBCA04" --description "Metadata and Custom Data" --force

# ── RFC labels — Tier 4 ────────────────────────────────────────────────────────
gh label create "IFC5-018" --repo $REPO --color "0075CA" --description "Backward Compatibility and Round-Tripping" --force
gh label create "IFC5-019" --repo $REPO --color "0075CA" --description "Validation Framework" --force
gh label create "IFC5-020" --repo $REPO --color "0075CA" --description "Model Views and Exchange Requirements" --force
gh label create "IFC5-021" --repo $REPO --color "0075CA" --description "Federation and External References" --force
gh label create "IFC5-022" --repo $REPO --color "0075CA" --description "Versioning and Schema Evolution" --force
gh label create "IFC5-032" --repo $REPO --color "0075CA" --description "Extensibility" --force
gh label create "IFC5-033" --repo $REPO --color "0075CA" --description "Change, Transactions, and Collaboration" --force
gh label create "IFC5-034" --repo $REPO --color "0075CA" --description "Performance, Scale, and Database Implications" --force
gh label create "IFC5-035" --repo $REPO --color "0075CA" --description "Web and Linked-Data Alignment" --force
gh label create "IFC5-036" --repo $REPO --color "0075CA" --description "AI and Machine-Readability" --force
gh label create "IFC5-037" --repo $REPO --color "0075CA" --description "Security and Trust" --force
gh label create "IFC5-038" --repo $REPO --color "0075CA" --description "Governance, Conformance, and Interoperability Testing" --force

echo ""
echo "✓ All labels created. View at: https://github.com/$REPO/labels"
