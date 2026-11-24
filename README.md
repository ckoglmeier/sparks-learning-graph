# Sparks Learning Graph

A reusable map of learning concepts, the knowledge they depend on, and ways to teach and assess them.

We built this while developing Sparks & Sprockets, a game about building machines and understanding how they work. We started with [Marble Skill Taxonomy](https://github.com/withmarbleapp/os-taxonomy) and extended it where practical engineering called for a more explicit concept.

The graph can be used independently of the game by educators, researchers, and developers.

**Release candidate: 0.1.0-rc.1.** This public edition provides curriculum identifiers and source links, with [source-rights disclosures](docs/reuse-and-licensing.md).

## What is included

The complete dataset contains **1,922 topics, 4,023 prerequisite relationships, and 1,922 teaching records**. Each topic describes what a learner should be able to explain or do. Teaching records include activities, assessment guidance, sources, and limitations.

Our contribution adds ten concepts covering:

- Density, displacement, buoyancy, and water pressure.
- Sensors, controllers, actuators, and feedback.
- Force and travel in simple machines, load placement and tipping, contact pressure, and solar-panel orientation.

We also preserve eight earlier computing teaching guides as historical supplements. The original Marble topic IDs and authored records remain intact.

## How the concepts relate to curricula

Practical engineering often connects ideas that appear in different subjects or at different ages. We document those relationships explicitly.

Some additions contribute to existing primary requirements. Others introduce a later concept qualitatively or provide enrichment without an exact standards mapping. An absent mapping does not mean that every curriculum omits a concept.

The [curriculum relationship notes](docs/curriculum-alignment.md) identify the sources reviewed, what each concept contributes, and which requirements remain outside its scope. Proposed activities and age ranges are teaching guidance, not evidence of measured learning outcomes.

## Explore the graph

- [Added concepts](docs/concepts.md): definitions, examples, sources, and reasons for each addition.
- [Curriculum relationships](docs/curriculum-alignment.md): partial coverage, enrichment, and assessment boundaries.
- [Earlier work](docs/reconciliation.md): reused concepts and preserved computing guidance.
- [Data format](docs/data-format.md), [validation](docs/validation.md), and [contributing](CONTRIBUTING.md).

## Download and use

The `data/` folder is the complete machine-readable database, not just a patch. `extensions/sparks/additions.json` also supplies the complete authored additions, and `UPSTREAM.json` pins the source. `RELEASE-MANIFEST.json` lists distributed file hashes. Download the packaged candidate from [GitHub Releases](https://github.com/ckoglmeier/sparks-learning-graph/releases).

To verify an extracted copy with Python 3.9 or later:

```sh
python3 -m pip install -r requirements-dev.txt
python3 tools/verify_release.py
python3 -m unittest discover -s tools -p 'test_*.py'
python3 extensions/sparks/verify.py
```

Dependencies are for release checks only; consumers can read the JSON without them. `python3 tools/build_archive.py /path/to/output.zip` creates a deterministic archive after validating the package.

## Reuse and credit

The database is licensed under [ODbL 1.0](LICENSE). Marble-authored and Sparks-authored learning content is licensed under [CC BY-SA 4.0](LICENSE-CONTENT). Our original verification tools use [MIT](LICENSE-CODE).

Those licenses permit reuse, including commercial reuse, subject to their terms. **Third-party curriculum material has separate terms.** All standard-text payloads are omitted from the curriculum catalogue. Inherited teaching research may retain limited quotations or paraphrases, which remain subject to their source terms. No special publisher permission or endorsement is claimed. Consult [PROVENANCE.md](PROVENANCE.md) and [reuse and licensing](docs/reuse-and-licensing.md) before redistributing source material.

Retain attribution, identify changes, and comply with the applicable share-alike terms. This release includes the complete machine-readable database so it can be inspected and reused.

Marble Skill Taxonomy (v1) · © Generative Spark, Inc. (Marble) · https://withmarble.com · licensed under ODbL 1.0 (database) and CC BY-SA 4.0 (content).

This derivative is maintained by Sparks & Sprockets. It is not endorsed by Marble or the curriculum publishers. Full notices and authorship details are in [ATTRIBUTION.md](ATTRIBUTION.md).

## US educator companion

[US educator guide](docs/us-educator-guide.md) and [versioned crosswalk](docs/us-crosswalk.json) cover selected grades 3–5 and 6–8 connections. These editorial records do not add canonical standards associations or game paths.
