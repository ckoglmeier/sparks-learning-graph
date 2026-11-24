# SPDX-License-Identifier: MIT
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parents[2]
def read(f):return json.loads((p/f).read_text())
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
b=read('extensions/sparks/baseline-authored-hashes.json');a=read('extensions/sparks/additions.json')
new={t['id'] for t in a['topics']};topics=read('data/topics.json')['topics'];research=read('data/teaching-research.json')['records']
for kind,records,key in [('topics',topics,'id'),('research',research,'topicId')]:
 index={r[key]:r for r in records}
 assert len(index)==len(records),kind+' duplicate IDs'
 for ident,h in b[kind].items():assert digest(index[ident])==h,(kind,ident,'changed original')
 assert set(index)-set(b[kind])==new,kind+' unexpected additions'
review=read('extensions/sparks/connection-review.json')
def bare(e):return {k:e[k] for k in ('topicId','prerequisiteId','strength','reason')}
# Reconstruct the pinned dependency array using only the explicitly approved delta.
edges=read('data/dependencies.json')['dependencies'][:]
for e in review['addedEdges']:
 record=bare(e)
 assert edges.count(record)==1,('missing or duplicate approved edge',record)
 edges.remove(record)
for rev in review['reversals']:
 assert edges.count(rev['after'])==1 and rev['before'] not in edges,('reversal mismatch',rev)
 edges[edges.index(rev['after'])]=rev['before']
assert digest([e for e in edges if e['topicId'] not in new])==b['dependencies'],'unreviewed inherited dependency change'
assert digest([r for r in read('data/curriculum-alignments.json')['alignments'] if r['topicId'] not in new])==b['alignments'],'original alignments changed'
for kind, records, key in [('topics', topics, 'id'), ('research', research, 'topicId')]:
 index = {r[key]: r for r in records}
 for record in a[kind]: assert index[record[key]] == record, ('delta mismatch', kind, record[key])
for kind, file in [('alignments','curriculum-alignments.json'), ('dependencies','dependencies.json')]:
 actual = ([r for r in read('data/'+file)[kind] if r['topicId'] in new] if kind == 'alignments' else [r for r in read('data/'+file)[kind] if r['topicId'] in new or r in [bare(e) for e in review['addedEdges']]])
 assert sorted(map(digest,actual)) == sorted(map(digest,a[kind])), ('delta mismatch',kind)
for r in a['research']:
 citations={s['id'] for s in r['sources']}
 for activity in r['learn']['activities']:assert set(activity['sourceIds'])<=citations
 assert r['assess']['correctAnswer'] and r['learn']['constraints']
for c in a['alignments']:assert c['ageRangeEnd']<=12 and c['standards']==[] and c['scope']=='global'
print('PASS: original topics and research preserved; only approved dependency changes; all additions and sources resolve; primary authoring scope.')
