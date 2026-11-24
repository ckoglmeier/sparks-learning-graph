#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Refresh the inventory after deliberately reviewed changes."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
ALLOWED_DIRS={'data','schema','extensions','supplements','docs','tools','.github'}
ALLOWED_ROOT={'README.md','CHANGELOG.md','CONTRIBUTING.md','ATTRIBUTION.md','PROVENANCE.md','CITATION.cff','UPSTREAM.json','LICENSE','LICENSE-CONTENT','LICENSE-CODE','requirements-dev.txt','.gitignore'}

def refresh(root=ROOT):
    records=[]
    for path in sorted(root.rglob('*')):
        rel=path.relative_to(root)
        if not path.is_file() or any(s in rel.parts for s in ['.git','__pycache__']):continue
        if str(rel)=='RELEASE-MANIFEST.json':continue
        if path.is_symlink() or (len(rel.parts)==1 and str(rel) not in ALLOWED_ROOT) or (len(rel.parts)>1 and rel.parts[0] not in ALLOWED_DIRS):
            raise ValueError('Not in release allowlist: '+str(rel))
        data=path.read_bytes()
        records.append({'path':str(rel),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    manifest={'version':'0.1.0-rc.1','preparedAt':'2026-11-24','upstreamCommit':'acac33d2a23bef7d60c462da2cd8ef124c7faa2a','inventoryExcludes':['RELEASE-MANIFEST.json (self)','local .git metadata','Python __pycache__'],'files':records}
    (root/'RELEASE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Inventoried',len(records),'files')
if __name__=='__main__':refresh()
