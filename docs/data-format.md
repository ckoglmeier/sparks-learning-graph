# Data format

The upstream taxonomy namespace remains `v1`; `0.1.0-rc.1` identifies this derivative release, not a change to the taxonomy schema.

- `data/topics.json`: stable topic IDs, mastery claims, observable evidence, parent prompts and generated age/standard compatibility fields.
- `data/dependencies.json`: prerequisite edges; `topicId` depends on `prerequisiteId`, with hard/soft strength and rationale.
- `data/curriculum-alignments.json`: authoritative scoped associations and global age guidance.
- `data/curriculum-standards.json`: source catalogues with source-specific rights; some contain codes only.
- `data/teaching-research.json`: one canonical v2 record per active topic, activities, diagnostics, sources and authorship.
- `data/archived-teaching-research.json`: inherited upstream historical research archive.
- `data/clusters.json`: inherited subject/domain clusters. New topics reuse existing domains.
- `data/manifest.json`: graph inventory and file hashes. Its upstream generation timestamp is historical; RELEASE-MANIFEST.json dates this derivative.
- `schema/`: unchanged upstream declarative JSON schema definitions.
- `extensions/sparks/additions.json`: authored delta, with stable IDs and full records. `claim-rationale.json` explains reuse decisions.
- `docs/curriculum-alignment.json`: release-specific assessment of selected sources; it does not add standards links or extend the strict upstream schema.
- `supplements/computing-2026-10-29/`: original historical v1 records; not active canonical guidance.

Empty standard arrays on new topics mean no formal association has been authored. Read the curriculum relationship report before interpreting that absence. New `centrality: null` means uncomputed. Inherited centrality values were not recomputed.

## US educator companion

[US educator guide](us-educator-guide.md) and [versioned crosswalk](us-crosswalk.json) cover selected grades 3–5 and 6–8 connections. These editorial records do not add canonical standards associations or game paths.
