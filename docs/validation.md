# Release validation

Candidate: **0.1.0-rc.1**, prepared 24 November 2026. Local validation used Python 3.9.6 with jsonschema 4.25.1 and the pinned upstream Node authoring toolchain. GitHub Actions is configured for Python 3.12; the workflow checks each public push; consult the repository Actions history for hosted results.

## Completed checks

- Pinned baseline and extended authoring dataset each pass all **577 upstream tests** (`node --test --test-concurrency=2 scripts/*.test.mjs`).
- Upstream alignment generation, graph validation and generated-artifact check pass. Final counts: **1,922 topics, 4,023 dependencies, 8,721 standards, 177 clusters, 1,922 canonical teaching records**.
- Standalone release checker validates JSON schemas, references, the prerequisite DAG, manifest checksums/counts, topic/schema bindings, historical source hashes and the public boundary.
- Nine regression checks cover the real graph and reject duplicate IDs, dangling prerequisites, cycles, missing activity citations, restricted curriculum wording, wrong counts, tampered files, unlisted files and product-only files.
- Semantic preservation verifies all 1,912 original topic and teaching records and original alignment/dependency arrays, plus exact agreement between the new authored delta and the complete dataset.
- The final archive is checked after extraction; its contents match the release inventory. Repeated archive generation is byte-identical.

## Interpretation and limits

The source review establishes bounded technical support and selected curriculum relationships. It does not validate learner efficacy, proposed ages, all inherited source flags, or every inherited curriculum association. No learner study is required for this release. The eight historical computing supplements retain their original evidence limits and are not active canonical records.

The distribution is a data/content release with original validation tools; upstream applications and authoring scripts are excluded. Local technical checks are complete. The subsequent license review identified an outstanding third-party trademark question; see [reuse and licensing](reuse-and-licensing.md). Public hosting, download links, and hosted CI remain publication actions.

## Next update: local validation scope

The approved update contains 1,927 topics, 4,046 dependencies and 1,927 teaching records. The earlier checks above describe the original candidate. Current validation reruns release schemas, graph integrity, pinned-claim preservation and the release regression suite. The dependency preservation check reconstructs the baseline using the explicit approved connection review; it rejects changes outside that delta. This does not establish learner efficacy or new formal standards coverage.

Local checks passed on 24 November 2026: release schema/inventory/binding/integrity checks; preservation of all original topic and teaching claims; release unit suite. Negative preservation checks rejected an unapproved inherited reason edit, a missing approved edge and a reverted approved reversal. The authoring explorer check also passed for full and subset graphs. No hosted CI or learner-efficacy testing was run before this repository update.
