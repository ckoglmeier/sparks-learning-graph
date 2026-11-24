#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate release inventory, JSON schemas and graph invariants without network access."""
import collections
import hashlib
import json
import pathlib
import re
import sys
from jsonschema import Draft202012Validator
ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(root, name):
    return json.loads((root / name).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_inventory(root):
    manifest = load(root, 'RELEASE-MANIFEST.json')
    listed = {r['path']: r for r in manifest['files']}
    if len(listed) != len(manifest['files']):
        raise ValueError('Duplicate inventory path')
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
              and '.git' not in p.relative_to(root).parts
              and '__pycache__' not in p.relative_to(root).parts
              and str(p.relative_to(root)) != 'RELEASE-MANIFEST.json'}
    if actual != set(listed):
        raise ValueError(f'Inventory mismatch: extra={actual-set(listed)}, missing={set(listed)-actual}')
    for name, record in listed.items():
        path = root / name
        if pathlib.PurePosixPath(name).is_absolute() or '..' in pathlib.PurePosixPath(name).parts or path.is_symlink():
            raise ValueError('Unsafe inventory path: ' + name)
        data = path.read_bytes()
        if len(data) != record['bytes'] or sha(data) != record['sha256']:
            raise ValueError('Inventory checksum mismatch: ' + name)
    return manifest


def read_graph(root):
    return {p.stem: json.loads(p.read_text()) for p in (root / 'data').glob('*.json')}


def check_graph(g):
    topics = g['topics']['topics']
    ids = [t['id'] for t in topics]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate topic IDs')
    ids = set(ids)
    edges = g['dependencies']['dependencies']
    pairs = [(d['topicId'], d['prerequisiteId']) for d in edges]
    if len(pairs) != len(set(pairs)):
        raise ValueError('Duplicate dependency')
    graph = collections.defaultdict(list)
    indegree = {i: 0 for i in ids}
    for d in edges:
        a, b = d['topicId'], d['prerequisiteId']
        if a not in ids or b not in ids:
            raise ValueError('Dangling prerequisite')
        if d['strength'] not in ['hard', 'soft']:
            raise ValueError('Invalid dependency strength')
        graph[b].append(a)
        indegree[a] += 1
    queue = collections.deque(i for i, n in indegree.items() if n == 0)
    visited = 0
    while queue:
        i = queue.popleft(); visited += 1
        for child in graph[i]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if visited != len(ids):
        raise ValueError('Dependency cycle')
    standard_keys = set()
    catalog = g['curriculum-standards']
    for curriculum in catalog['curricula']:
        codes_only = curriculum['slug'] in catalog['codesOnlySources']
        if curriculum['textIncluded'] == codes_only:
            raise ValueError('Codes-only flag mismatch')
        for standard in curriculum['topics']:
            if codes_only and 'data' in standard:
                raise ValueError('Restricted curriculum text in codes-only record')
            if standard['key'] != curriculum['slug'] + ':' + standard['code'] or standard['key'] in standard_keys:
                raise ValueError('Invalid or duplicate standard key')
            standard_keys.add(standard['key'])
    for topic in topics:
        if not set(topic['standards']) <= standard_keys:
            raise ValueError('Dangling topic standard')
    for context in g['curriculum-alignments']['alignments']:
        if context['topicId'] not in ids or not set(context.get('standards', [])) <= standard_keys:
            raise ValueError('Dangling alignment')
    records = g['teaching-research']['records']
    rids = [r['topicId'] for r in records]
    if len(rids) != len(set(rids)) or set(rids) != ids:
        raise ValueError('Research coverage mismatch')
    for r in records:
        cites = [s['id'] for s in r['sources']]
        if len(cites) != len(set(cites)):
            raise ValueError('Duplicate citation IDs')
        for activity in r['learn']['activities']:
            if not set(activity['sourceIds']) <= set(cites):
                raise ValueError('Dangling activity source')
    counts = g['manifest']['counts']
    expected = {'topics':len(ids), 'dependencies':len(edges), 'teachingResearch':len(records),
                'curriculumStandards':len(standard_keys), 'curricula':len(catalog['curricula']),
                'curriculumAlignments':len(g['curriculum-alignments']['alignments']),
                'clusters':len(g['clusters']['clusters'])}
    for key, value in expected.items():
        if counts[key] != value:
            raise ValueError('Manifest count mismatch: ' + key)
    if dict(collections.Counter(t['subject'] for t in topics)) != counts['topicsBySubject']:
        raise ValueError('Subject inventory mismatch')
    if g['topics']['topicCount'] != len(ids) or g['dependencies']['edgeCount'] != len(edges):
        raise ValueError('Collection count mismatch')
    coverage = {'topicCount':len(ids), 'withResearch':len(records), 'withoutResearch':0,
                'bySubject':{s:{'topics':n,'withResearch':n,'withoutResearch':0}
                             for s,n in collections.Counter(t['subject'] for t in topics).items()},
                'missingTopicIds':[]}
    if g['teaching-research']['coverage'] != coverage:
        raise ValueError('Research coverage summary mismatch')
    if any(v != g['teaching-research'][k] for k,v in g['manifest']['teachingResearch'].items()):
        raise ValueError('Manifest research summary mismatch')
    return expected


def check_schemas(root, graph):
    for data, schema in [('topics','topics'), ('dependencies','dependencies'),
                         ('clusters','clusters'), ('curriculum-standards','curriculum-standards'),
                         ('curriculum-alignments','curriculum-alignments-v2')]:
        spec = load(root, 'schema/' + schema + '.schema.json')
        Draft202012Validator.check_schema(spec)
        Draft202012Validator(spec).validate(graph[data])
    spec = load(root, 'schema/canonical-teaching-research-v2.schema.json')
    Draft202012Validator.check_schema(spec)
    validator = Draft202012Validator(spec)
    for record in graph['teaching-research']['records']:
        validator.validate(record)


def check_boundary(root):
    # Product-only metadata and operational markers, not ordinary subject words.
    forbidden = re.compile(r'requiresExpansions|/Users/|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{30,}')
    for path in root.rglob('*'):
        if not path.is_file() or any(s in path.parts for s in ['.git','__pycache__']):
            continue
        rel = str(path.relative_to(root))
        if rel in ['tools/verify_release.py','tools/test_release.py']:
            continue
        if path.name in ['paths.json','BUILD-RECORD.md','SPARKS.md']:
            raise ValueError('Product-only file in public package: ' + rel)
        if path.suffix in ['.json','.md','.cff','.yml','.py']:
            if forbidden.search(path.read_text()):
                raise ValueError('Product or private marker in public package: ' + rel)
    additions = load(root, 'extensions/sparks/additions.json')
    for t in additions['topics']:
        if {'worlds','paths','world','level','pack','requiresExpansions'} & set(t):
            raise ValueError('Product metadata in graph topic')
    dispositions = load(root, 'docs/curriculum-alignment.json')['records']
    if {r['topicId'] for r in dispositions} != {t['id'] for t in additions['topics']}:
        raise ValueError('Missing curriculum disposition')
    if any(r['formalAssociationAuthored'] for r in dispositions):
        raise ValueError('Unexpected new formal alignment claim')
    for record in load(root, 'supplements/computing-2026-10-29/index.json'):
        data = (root/'supplements/computing-2026-10-29'/record['file']).read_bytes()
        if sha(data) != record['sha256']:
            raise ValueError('Historical supplement changed')


def verify(root=ROOT):
    inventory = check_inventory(root)
    graph = read_graph(root)
    check_schemas(root, graph)
    counts = check_graph(graph)
    for name, rec in graph['manifest']['files'].items():
        data = (root/'data'/name).read_bytes()
        if sha(data) != rec['sha256'] or len(data) != rec['bytes']:
            raise ValueError('Graph checksum mismatch: ' + name)
    research = graph['teaching-research']
    if research['topicFileSha256'] != sha((root/'data/topics.json').read_bytes()):
        raise ValueError('Research-topic binding mismatch')
    if research['canonicalSchemaSha256'] != sha((root/'schema/canonical-teaching-research-v2.schema.json').read_bytes()):
        raise ValueError('Canonical schema binding mismatch')
    check_boundary(root)
    print('PASS', inventory['version'], json.dumps(counts, sort_keys=True))
    return counts


if __name__ == '__main__':
    verify(pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT)
