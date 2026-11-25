"""Run with Python 3 after adding local audio assets: python extras/rebuild_assets.py.
This refreshes the local inventory and cache version. It does NOT approve animal recording rights.
Review recordings separately and add eligible real-animal IDs to REVIEW_CALLS or VERIFIED_CALLS in index.html.
"""
from pathlib import Path
import re,json,hashlib
root=Path(__file__).resolve().parent.parent
index=root/'index.html'; sw=root/'sw.js'
audio=sorted(p.relative_to(root).as_posix() for p in root.glob('audio/**/*.mp3'))
html=index.read_text(encoding='utf-8'); html,n=re.subn(r'const INCLUDED_AUDIO=new Set\([^\n]+\);','const INCLUDED_AUDIO=new Set('+json.dumps(audio)+');',html,count=1);assert n==1
index.write_text(html,encoding='utf-8')
assets=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png']+['./'+p for p in audio]+['./'+p.relative_to(root).as_posix() for p in sorted(root.glob('art/colouring/*.png'))]
h=hashlib.sha256()
for path in assets[1:]:
 h.update(path.encode());h.update((root/path).read_bytes())
text=sw.read_text(encoding='utf-8');text=re.sub(r"const VERSION='[^']+';", "const VERSION='uaaf-"+h.hexdigest()[:16]+"';",text,count=1);text=re.sub(r'const ASSETS=\[[^\n]*\];','const ASSETS='+json.dumps(assets)+';',text,count=1);sw.write_text(text,encoding='utf-8')
print('Asset inventory refreshed:',len(audio),'MP3s.')
