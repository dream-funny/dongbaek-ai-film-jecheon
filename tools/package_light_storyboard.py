"""원본을 보존하고 오프라인 콘티·영상 앱 및 키 이미지 패키지를 만든다."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,base64,zipfile,hashlib,sys
ROOT=Path(__file__).resolve().parent.parent;P=ROOT/'storyboard';D=ROOT/'downloads';D.mkdir(exist_ok=True)
WORK=Path('/tmp/dongbaek-light-assets');WORK.mkdir(exist_ok=True)
data=json.loads((P/'storyboard.json').read_text());clips=[c for s in data['scenes'] for c in s['clips']]
needed=sorted({c['image'] for c in clips}|{'assets/characters.png','assets/locations.png','assets/props_animals.png'})
videos=sorted({c['video'] for c in clips if c.get('video')})
original={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in needed+videos}
def encode(f):
 out=WORK/(Path(f).stem+'.jpg')
 subprocess.run(['magick',str(P/f),'-strip','-sampling-factor','2x2','-quality','82',str(out)],check=True,capture_output=True)
 return f,out
with ThreadPoolExecutor(max_workers=4) as pool:jpgs=dict(pool.map(encode,needed))
images={f:'data:image/jpeg;base64,'+base64.b64encode(jpgs[f].read_bytes()).decode('ascii') for f in needed}
media={f:'data:video/mp4;base64,'+base64.b64encode((P/f).read_bytes()).decode('ascii') for f in videos}
source=(P/'index.html').read_text();mdurl='data:text/markdown;charset=utf-8;base64,'+base64.b64encode((P/'VIDEO_PROMPTS.md').read_bytes()).decode()
def make_html(embedded):
 inline='<script>window.EMBEDDED_ASSETS='+json.dumps(embedded,separators=(',',':'))+';</script>\n<script>'+(P/'data.js').read_text().replace('</script','<\\/script')+'</script>'
 html=source.replace('<script src="data.js"></script>',inline).replace('href="VIDEO_PROMPTS.md"','href="'+mdurl+'"')
 html=html.replace('소란스러운 봄, 서툰 마음.','소란스러운 봄, 서툰 마음. · 영상 '+str(len(videos))+'컷 등록')
 html=html.replace('키 이미지 저장 ↓','현재 이미지 PNG 저장 ↓')
 return html.replace('<footer>','<footer>이미지는 동일 크기 JPEG 압축 미리보기입니다. 원본 PNG는 씬별 ZIP, 등록 MP4는 업로드 원본 그대로입니다.<br>',1)
standalone=D/'DONGBAEK_STORYBOARD_LIGHT.html';standalone.write_text(make_html({**images,**media}))
app_html=make_html(images) # ZIP은 MP4를 별도 파일로 포함하여 base64 중복을 줄인다.
with zipfile.ZipFile(D/'DONGBAEK_LIGHT_PACKAGE.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr(standalone.name,app_html)
 for f in videos:z.write(P/f,f)
 for f in ['VIDEO_PROMPTS.md','FLOW_EDIT_LIST.csv','EDITED_SCREENPLAY.md','VIDEO_MANIFEST.json']:
  if (P/f).exists():z.write(P/f,f)
 z.writestr('시작하기.txt',('ZIP 전체를 압축 해제하고 DONGBAEK_STORYBOARD_LIGHT.html을 브라우저로 엽니다. videos 폴더를 HTML 옆에 보관하세요.\nS01-01~S01-04 영상 4개가 등록되어 있습니다. 컷별 영상 보기와 S01 25초 이어보기를 사용하세요.\n시작 이미지 35장은 HTML에 내장되어 있습니다. 별도 JPEG 파일은 keyframes-and-prompts.zip을 받으세요.\n단일 HTML만 다른 컴퓨터로 옮기려면 저장소의 영상 내장 HTML 파일을 내려받으세요.\n').encode('utf-8-sig'))
for s in data['scenes']:
 if '--media-only' in sys.argv and (D/(s['id']+'_ORIGINAL_PNG.zip')).exists():continue
 if '--scene' in sys.argv and s['id']!=sys.argv[sys.argv.index('--scene')+1] and (D/(s['id']+'_ORIGINAL_PNG.zip')).exists():continue
 with zipfile.ZipFile(D/(s['id']+'_ORIGINAL_PNG.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for c in s['clips']:z.write(P/c['image'],s['id']+'/'+c['id']+'.png')
  z.writestr(s['id']+'/PROMPTS.txt','\n\n'.join(c['ko']+'\n\n'+c['en'] for c in s['clips']))
with zipfile.ZipFile(D/'keyframes-and-prompts.zip','w',zipfile.ZIP_DEFLATED) as z:
 for c in clips:z.write(jpgs[c['image']],'images/'+c['id']+'.jpg')
 for f in ['VIDEO_PROMPTS.md','FLOW_EDIT_LIST.csv']:z.write(P/f,f)
 z.writestr('READ_ME.txt','images 폴더의 컷 번호와 VIDEO_PROMPTS.md의 같은 번호를 사용하세요. JPEG 35장, 한영 영상 프롬프트, 편집표가 들어 있습니다.\n'.encode('utf-8-sig'))
for f in needed+videos:assert hashlib.sha256((P/f).read_bytes()).hexdigest()==original[f]
for f in D.glob('*.zip'):
 with zipfile.ZipFile(f) as z:assert z.testzip() is None
sizes={f.name:round(f.stat().st_size/1024/1024,2) for f in D.iterdir() if f.is_file() and f.suffix in ['.zip','.html']}
assert all((D/f).stat().st_size<100*1024*1024 for f in sizes)
(D/'sizes.json').write_text(json.dumps(sizes,ensure_ascii=False,indent=2))
readme=['# 동백꽃 — 콘티·영상 다운로드\n','비공개 저장소에 접근 가능한 GitHub 계정으로 로그인하고, 파일 페이지의 **↓ Download raw file**을 누르세요.\n',f'1. **[영상 포함 콘티 앱 ZIP — {sizes["DONGBAEK_LIGHT_PACKAGE.zip"]}MB](DONGBAEK_LIGHT_PACKAGE.zip)**: 전체 압축 해제 후 HTML을 엽니다. `videos` 폴더를 함께 보관하세요.\n',f'2. **[이미지·영상 내장 HTML 하나만 받기 — {sizes[standalone.name]}MB]({standalone.name})**: 이 파일 하나만 복사해도 오프라인으로 작동합니다.\n',f'3. **[키 이미지 35장 + 영상 프롬프트만 받기 — {sizes["keyframes-and-prompts.zip"]}MB](keyframes-and-prompts.zip)**\n','S01 영상 4컷은 업로드한 원본을 그대로 포함했습니다. 개별 영상의 전체 재생과 편집 구간 재생을 선택할 수 있습니다. **S01 영상 이어보기**는 8+8+5+4초, 총 25초입니다. 등록과 검토 완료는 구분합니다.\n','이미지 경량 미리보기는 JPEG 압축이며, PNG 저장은 미리보기를 PNG로 변환합니다. 아래 원본 PNG는 그대로 유지합니다.\n','## 고화질 원본 PNG — 필요한 씬만 받기\n','|씬|내용|원본 PNG ZIP|\n|---|---|---|']
for s in data['scenes']:
 name=s['id']+'_ORIGINAL_PNG.zip';readme.append(f'|{s["id"]}|{s["title"]}|[{sizes[name]}MB 다운로드]({name})|')
readme.append('\n[이미지·프롬프트·등록 영상 보기](../storyboard/GALLERY.md) · [사용 방법](../storyboard/README.md)\n')
(D/'README.md').write_text('\n'.join(readme))
print(json.dumps(sizes,ensure_ascii=False,indent=2))
