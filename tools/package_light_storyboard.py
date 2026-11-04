"""원본 PNG를 유지하고 JPEG 기반 소용량 HTML 및 씬별 PNG ZIP을 만든다."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,base64,zipfile,hashlib,sys
ROOT=Path(__file__).resolve().parent.parent;P=ROOT/'storyboard';D=ROOT/'downloads';D.mkdir(exist_ok=True)
WORK=Path('/tmp/dongbaek-light-assets');WORK.mkdir(exist_ok=True)
data=json.loads((P/'storyboard.json').read_text())
clips=[c for s in data['scenes'] for c in s['clips']]
needed=sorted({c['image'] for c in clips}|{'assets/characters.png','assets/locations.png','assets/props_animals.png'})
original={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in needed}
def encode(f):
 out=WORK/(Path(f).stem+'.jpg')
 subprocess.run(['magick',str(P/f),'-strip','-sampling-factor','2x2','-quality','82',str(out)],check=True,capture_output=True)
 return f,out
with ThreadPoolExecutor(max_workers=4) as pool:jpgs=dict(pool.map(encode,needed))
embedded={f:'data:image/jpeg;base64,'+base64.b64encode(jpgs[f].read_bytes()).decode('ascii') for f in needed}
html=(P/'index.html').read_text();inline='<script>window.EMBEDDED_ASSETS='+json.dumps(embedded,separators=(',',':'))+';</script>\n<script>'+(P/'data.js').read_text().replace('</script','<\\/script')+'</script>'
html=html.replace('<script src="data.js"></script>',inline)
mdurl='data:text/markdown;charset=utf-8;base64,'+base64.b64encode((P/'VIDEO_PROMPTS.md').read_bytes()).decode();html=html.replace('href="VIDEO_PROMPTS.md"','href="'+mdurl+'"')
html=html.replace('SCENES</span>','SCENES</span>',1)
html=html.replace('소란스러운 봄, 서툰 마음.','소란스러운 봄, 서툰 마음. · 경량판')
html=html.replace('키 이미지 저장 ↓','현재 이미지 PNG 저장 ↓')
html=html.replace('<footer>','<footer>경량판은 동일 크기의 JPEG 압축 미리보기를 사용합니다. PNG 저장은 이 미리보기를 PNG로 변환하며, 원본 PNG는 씬별 ZIP에 있습니다.<br>',1)
standalone=D/'DONGBAEK_STORYBOARD_LIGHT.html';standalone.write_text(html)
with zipfile.ZipFile(D/'DONGBAEK_LIGHT_PACKAGE.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(standalone,standalone.name)
 for c in clips:z.write(jpgs[c['image']],'images/'+c['id']+'.jpg')
 for f in ['VIDEO_PROMPTS.md','FLOW_EDIT_LIST.csv','EDITED_SCREENPLAY.md']:z.write(P/f,f)
 z.writestr('시작하기.txt','DONGBAEK_STORYBOARD_LIGHT.html을 브라우저로 엽니다. 이미지와 프롬프트가 모두 들어 있습니다.\nimages 폴더 JPEG는 Flow 첫 프레임으로 쓸 수 있습니다. 원본 PNG는 저장소 downloads의 씬별 ZIP을 받으세요.\n이미지의 인물·구도·해상도는 원본 기준이며 파일 용량을 줄이기 위한 JPEG 압축만 적용했습니다.\n')
for s in data['scenes']:
 if '--scene' in sys.argv and s['id']!=sys.argv[sys.argv.index('--scene')+1] and (D/(s['id']+'_ORIGINAL_PNG.zip')).exists():continue
 with zipfile.ZipFile(D/(s['id']+'_ORIGINAL_PNG.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for c in s['clips']:z.write(P/c['image'],s['id']+'/'+c['id']+'.png')
  z.writestr(s['id']+'/PROMPTS.txt','\n\n'.join(c['ko']+'\n\n'+c['en'] for c in s['clips']))
with zipfile.ZipFile(D/'keyframes-and-prompts.zip','w',zipfile.ZIP_DEFLATED) as z:
 for c in clips:z.write(jpgs[c['image']],'images/'+c['id']+'.jpg')
 for f in ['VIDEO_PROMPTS.md','FLOW_EDIT_LIST.csv']:z.write(P/f,f)
 z.writestr('READ_ME.txt','images 폴더의 컷 번호와 VIDEO_PROMPTS.md의 같은 번호를 사용하세요. JPEG 35장, 한영 영상 프롬프트, 편집표가 들어 있습니다.\n'.encode('utf-8-sig'))
for f in needed:assert hashlib.sha256((P/f).read_bytes()).hexdigest()==original[f]
for f in D.glob('*.zip'):
 with zipfile.ZipFile(f) as z:assert z.testzip() is None
sizes={f.name:round(f.stat().st_size/1024/1024,2) for f in D.iterdir() if f.is_file() and f.suffix in ['.zip','.html']}
assert all((D/f).stat().st_size<100*1024*1024 for f in sizes)
(D/'sizes.json').write_text(json.dumps(sizes,ensure_ascii=False,indent=2))
readme=['# 동백꽃 — 소용량 다운로드\n','비공개 저장소에 접근 가능한 GitHub 계정으로 로그인하세요. 파일을 열고 **Download raw file / 원본 파일 다운로드**를 누르면 됩니다.\n',f'1. **[HTML 하나만 받기 — {sizes[standalone.name]}MB]({standalone.name})**: 이미지 35장·영상 프롬프트·복사 버튼 포함. 내려받아 브라우저로 엽니다.\n',f'2. **[콘티 + 이미지 35장 + 프롬프트 ZIP — {sizes["DONGBAEK_LIGHT_PACKAGE.zip"]}MB](DONGBAEK_LIGHT_PACKAGE.zip)**: 압축 해제 후 HTML을 엽니다. 이미지 JPEG도 별도로 들어 있습니다.\n','이미지 다시 생성이나 얼굴·구도 변경 없이 JPEG 압축만 적용했습니다. 픽셀 크기도 유지합니다. 경량 HTML의 PNG 저장은 압축 미리보기를 PNG로 변환합니다. 아래 원본 PNG는 손실 없이 그대로 보관했습니다.\n','## 고화질 원본 PNG — 필요한 씬만 받기\n','|씬|내용|원본 PNG ZIP|\n|---|---|---|']
for s in data['scenes']:
 name=s['id']+'_ORIGINAL_PNG.zip';readme.append(f'|{s["id"]}|{s["title"]}|[{sizes[name]}MB 다운로드]({name})|')
readme.insert(2,f'**[키 이미지 35장 + 영상 프롬프트만 받기 — {sizes["keyframes-and-prompts.zip"]}MB](keyframes-and-prompts.zip)**\n')
readme.append('\n[이미지·프롬프트 바로 보기](../storyboard/GALLERY.md) · [사용 방법](../storyboard/README.md)\n')
i=next(i for i,v in enumerate(readme) if v.startswith('1. **'));j=next(i for i,v in enumerate(readme) if v.startswith('2. **'));readme[i],readme[j]=readme[j].replace('2. **','1. **',1),readme[i].replace('1. **','2. **',1)
(D/'README.md').write_text('\n'.join(readme))
print(json.dumps(sizes,ensure_ascii=False,indent=2))
