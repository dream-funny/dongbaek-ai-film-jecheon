"""키 이미지가 포함된 독립 HTML과 배포 ZIP을 만든다."""
from pathlib import Path
import base64,json,zipfile,re
ROOT=Path(__file__).resolve().parent.parent
P=ROOT/'storyboard'
data=json.loads((P/'storyboard.json').read_text())
needed={c['image'] for s in data['scenes'] for c in s['clips']}|{'assets/characters.png','assets/locations.png','assets/props_animals.png'}
missing=[f for f in sorted(needed) if not(P/f).is_file()]
if missing:raise SystemExit('시작 이미지 미완료: '+', '.join(missing))
assets={f:'data:image/png;base64,'+base64.b64encode((P/f).read_bytes()).decode('ascii') for f in sorted(needed)}
html=(P/'index.html').read_text()
inline='<script>window.EMBEDDED_ASSETS='+json.dumps(assets,separators=(',',':'))+';</script>\n<script>'+(P/'data.js').read_text().replace('</script','<\\/script')+'</script>'
standalone=html.replace('<script src="data.js"></script>',inline)
mdurl='data:text/markdown;charset=utf-8;base64,'+base64.b64encode((P/'VIDEO_PROMPTS.md').read_bytes()).decode()
standalone=standalone.replace('href="VIDEO_PROMPTS.md"','href="'+mdurl+'"')
exports=ROOT/'exports';exports.mkdir(exist_ok=True)
path=exports/'DONGBAEK_STORYBOARD_4MIN.html';path.write_text(standalone)
zip_path=exports/'DONGBAEK_STORYBOARD_FLOW.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for name in ['index.html','data.js','storyboard.json','VIDEO_PROMPTS.md','FLOW_EDIT_LIST.csv','EDITED_SCREENPLAY.md','README.md']:
  if (P/name).is_file():z.write(P/name,'dongbaek-storyboard/'+name)
 for name in sorted(needed):z.write(P/name,'dongbaek-storyboard/'+name)
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
assert 'src="data.js"' not in standalone
print('독립 HTML:',round(path.stat().st_size/1024/1024,1),'MiB')
print('Flow 제작 ZIP:',round(zip_path.stat().st_size/1024/1024,1),'MiB')
