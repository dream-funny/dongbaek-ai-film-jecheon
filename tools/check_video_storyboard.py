"""업로드 동영상의 실제 재생·편집 구간·오프라인 패키지를 검증한다."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import threading,json,hashlib,zipfile,tempfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/';errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 ctx=b.new_context(viewport={'width':1440,'height':1050},accept_downloads=True)
 page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'storyboard/index.html')
 assert page.locator('#videoCount').inner_text()=='4 / 35'
 for i in range(4):
  page.locator('[data-clip="'+str(i)+'"]').click()
  page.wait_for_function('document.getElementById("clipVideo").readyState>=1')
  assert page.locator('#videoStage').is_visible()
  assert page.evaluate('document.getElementById("clipVideo").videoWidth')==1280
  assert 8<=page.evaluate('document.getElementById("clipVideo").duration')<8.1
  page.evaluate('document.getElementById("clipVideo").play()')
  page.wait_for_function('document.getElementById("clipVideo").currentTime>0.15')
  page.evaluate('document.getElementById("clipVideo").pause()')
 # S01-03은 편집 5초에서 멈추지만, 체크 해제 시 8초 원본을 볼 수 있다.
 page.locator('[data-clip="2"]').click();page.wait_for_function('document.getElementById("clipVideo").readyState>=1')
 page.locator('#trimClip').uncheck();page.evaluate('document.getElementById("clipVideo").currentTime=4.8;document.getElementById("clipVideo").play()')
 page.wait_for_function('document.getElementById("clipVideo").currentTime>5.15');assert not page.evaluate('document.getElementById("clipVideo").paused')
 page.evaluate('document.getElementById("clipVideo").pause()');page.locator('#trimClip').check();page.evaluate('document.getElementById("clipVideo").currentTime=4.8;document.getElementById("clipVideo").play()')
 page.wait_for_function('document.getElementById("clipVideo").paused && Math.abs(document.getElementById("clipVideo").currentTime-5)<0.03')
 page.locator('#showKey').click();assert page.locator('#imageStage').is_visible();assert page.locator('#videoStage').is_hidden();page.locator('#showVideo').click()
 # 연결 미리보기는 실제 영상을 재생하며 8+8+5+4초 구간을 차례로 사용한다.
 page.locator('#sceneVideoPreview').click();assert page.locator('#slideProgress').get_attribute('max')=='25'
 for i,end in enumerate([8,8,5,4]):
  page.wait_for_function('(id)=>document.getElementById("slideTitle").textContent.includes(id)',arg=f'S01-{i+1:02}')
  page.wait_for_function('document.getElementById("slideVideo").currentTime>0.1')
  assert page.locator('#slideVideoStage').is_visible()
  page.evaluate('(end)=>document.getElementById("slideVideo").currentTime=end-0.08',end)
  if i<3:page.wait_for_function('(id)=>document.getElementById("slideTitle").textContent.includes(id)',arg=f'S01-{i+2:02}')
 page.wait_for_function('document.getElementById("slidePlay").textContent==="재생" && document.getElementById("slideProgress").value===25')
 page.keyboard.press('Escape');assert page.evaluate('Array.from(document.querySelectorAll("video")).every(v=>v.paused)')
 page.locator('#sceneNav [data-scene="S02"]').click();assert page.locator('#videoStage').is_hidden();assert page.locator('#imageStage').is_visible();assert '미등록' in page.locator('#mediaControls').inner_text()
 page.locator('#preview').click();assert page.locator('#slideImageStage').is_visible();page.locator('#slidePrev').click();page.wait_for_function('document.getElementById("slideVideo").currentTime>0.1');page.keyboard.press('Escape')
 ctx.close();print('PASS: 4개 실제 H264/AAC 재생, 원본/편집 구간 전환, 25초 연결·영상/이미지 혼합 미리보기',flush=True)
 # 단일 HTML은 네트워크를 끊어도 MP4 원본이 재생·저장된다.
 ctx=b.new_context(viewport={'width':390,'height':844},accept_downloads=True);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'downloads/DONGBAEK_STORYBOARD_LIGHT.html',timeout=120000);ctx.set_offline(True)
 for i in range(4):
  page.locator('[data-clip="'+str(i)+'"]').click();page.wait_for_function('document.getElementById("clipVideo").readyState>=1')
  assert page.locator('#clipVideo').get_attribute('src').startswith('blob:')
  page.evaluate('document.getElementById("clipVideo").play()');page.wait_for_function('document.getElementById("clipVideo").currentTime>0.1');page.evaluate('document.getElementById("clipVideo").pause()')
 with page.expect_download() as d:page.locator('#downloadVideo').click()
 tmp=ROOT/'downloads/_video_test.mp4';d.value.save_as(tmp)
 assert hashlib.sha256(tmp.read_bytes()).digest()==hashlib.sha256((ROOT/'storyboard/videos/S01/S01-04.mp4').read_bytes()).digest();tmp.unlink()
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.locator('[data-clip="0"]').click();page.screenshot(path=str(ROOT/'storyboard/PREVIEW_VIDEO_MOBILE.png'),full_page=True)
 ctx.close()
 # ZIP을 풀어 HTML에서 상대 경로 MP4 4개가 실제로 재생되는지도 확인한다.
 with tempfile.TemporaryDirectory(dir=ROOT/'downloads',prefix='_app_verify_') as tmpdir:
  with zipfile.ZipFile(ROOT/'downloads/DONGBAEK_LIGHT_PACKAGE.zip') as z:z.extractall(tmpdir)
  relative=Path(tmpdir).relative_to(ROOT).as_posix()
  zipctx=b.new_context();zippage=zipctx.new_page();zippage.on('pageerror',lambda e:errors.append(str(e)))
  zippage.goto(base+relative+'/DONGBAEK_STORYBOARD_LIGHT.html')
  for i in range(4):
   zippage.locator('[data-clip="'+str(i)+'"]').click();zippage.wait_for_function('document.getElementById("clipVideo").readyState>=1')
   zippage.evaluate('document.getElementById("clipVideo").play()');zippage.wait_for_function('document.getElementById("clipVideo").currentTime>0.1');zippage.evaluate('document.getElementById("clipVideo").pause()')
  zipctx.close()
 assert not errors,errors
 b.close()
server.shutdown()
with zipfile.ZipFile(ROOT/'downloads/DONGBAEK_LIGHT_PACKAGE.zip') as z:
 assert z.testzip() is None
 for i in range(1,5):
  f=f'videos/S01/S01-{i:02}.mp4';assert z.read(f)==(ROOT/'storyboard'/f).read_bytes()
 assert len([f for f in z.namelist() if f.endswith('.mp4')])==4
print('PASS: 단일 HTML 오프라인 MP4 4개·원본 바이트 다운로드·모바일·ZIP 원본 4개 일치',flush=True)
