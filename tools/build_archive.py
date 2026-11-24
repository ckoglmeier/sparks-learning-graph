#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Create a deterministic ZIP from the verified explicit release inventory."""
import pathlib,sys,zipfile,json
from verify_release import verify,ROOT

def build(output,root=ROOT):
    output=pathlib.Path(output).resolve()
    if output==root or root in output.parents:raise ValueError('Archive must be outside the source package')
    verify(root)
    names=[r['path'] for r in json.loads((root/'RELEASE-MANIFEST.json').read_text())['files']]+['RELEASE-MANIFEST.json']
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in sorted(names):
            info=zipfile.ZipInfo('sparks-learning-graph-0.1.0-rc.1/'+name,date_time=(2026,11,24,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            archive.writestr(info,(root/name).read_bytes(),compresslevel=9)
    print(output)
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python3 tools/build_archive.py OUTPUT.zip')
    build(sys.argv[1])
