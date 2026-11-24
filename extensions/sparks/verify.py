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
for kind,file in [('alignments','curriculum-alignments.json'),('dependencies','dependencies.json')]:
 old=[r for r in read('data/'+file)[kind] if r['topicId'] not in new]
 assert digest(old)==b[kind],kind+' original records changed'
for kind, records, key in [('topics', topics, 'id'), ('research', research, 'topicId')]:
 index = {r[key]: r for r in records}
 for record in a[kind]: assert index[record[key]] == record, ('delta mismatch', kind, record[key])
for kind, file in [('alignments','curriculum-alignments.json'), ('dependencies','dependencies.json')]:
 actual = [r for r in read('data/'+file)[kind] if r['topicId'] in new]
 assert sorted(map(digest,actual)) == sorted(map(digest,a[kind])), ('delta mismatch',kind)
for r in a['research']:
 citations={s['id'] for s in r['sources']}
 for activity in r['learn']['activities']:assert set(activity['sourceIds'])<=citations
 assert r['assess']['correctAnswer'] and r['learn']['constraints']
for c in a['alignments']:assert c['ageRangeEnd']<=12 and c['standards']==[] and c['scope']=='global'
print('PASS: original authored records preserved; all additions and sources resolve; primary authoring scope.')
