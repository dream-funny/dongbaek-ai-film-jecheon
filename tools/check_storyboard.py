"""로컬 Chromium에서 콘티의 실제 상호작용을 검증한다."""
from pathlib import Path
import json,threading,sys
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'storyboard/storyboard.json').read_text());allow_missing='--allow-missing' in sys.argv
clips=[c for s in DATA['scenes'] for c in s['clips']]
assert len(clips)==35 and sum(c['duration'] for c in clips)==240
assert sum(c['generatedDuration'] for c in clips)==280
assert all(4<=c['duration']<=8 for c in clips)
assert '화면 밖 목소리만' in DATA['scenes'][2]['characters']
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'],accept_downloads=True)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 base=f'http://127.0.0.1:{server.server_port}/storyboard/'
 page.goto(base)
 assert page.locator('#sceneNav [data-scene]').count()==10
 assert 'S01-01' in page.locator('#clipTitle').inner_text()
 # 各컷을 순회하며 이미지와 복사 프롬프트의 번호가 일치하는지 확인한다.
 for s in DATA['scenes']:
  page.locator('#sceneNav [data-scene="'+s['id']+'"]').click()
  for idx,c in enumerate(s['clips']):
   page.locator('[data-clip="'+str(idx)+'"]').click()
   assert c['id'] in page.locator('#clipTitle').inner_text()
   assert page.locator('#keyImage').get_attribute('src')==c['image']
   assert c['id'] in page.locator('#promptText').inner_text()
   if not allow_missing:
    page.wait_for_function('document.getElementById("keyImage").complete && document.getElementById("keyImage").naturalWidth > 0')
 # 실제 브라우저 클립보드에 복사해 원문과 비교한다.
 page.locator('#copyKo').click();actual=page.evaluate('navigator.clipboard.readText()');assert actual==clips[-1]['ko']
 page.locator('#copyEn').click();assert page.evaluate('navigator.clipboard.readText()')==clips[-1]['en']
 page.locator('#enTab').click();assert 'Generate 8s' in page.locator('#promptText').inner_text()
 page.locator('#sceneStatus').select_option('완료');page.locator('#sceneNotes').fill('집→강의장 테스트 메모');page.locator('[data-check="0"]').check();page.reload()
 assert page.locator('#sceneStatus').input_value()=='완료';assert page.locator('#sceneNotes').input_value()=='집→강의장 테스트 메모'
 with page.expect_download() as d:page.locator('#exportState').click()
 exported=ROOT/'storyboard_progress_test.json';d.value.save_as(exported)
 saved=json.loads(exported.read_text());assert saved['state']['S10']['status']=='완료'
 context.clear_permissions()
 page.evaluate('localStorage.clear()');page.reload()
 page.locator('#stateFile').set_input_files(str(exported));page.wait_for_function('document.getElementById("sceneStatus").value==="완료"')
 exported.unlink()
 # 검색 / 막 필터 / 전체 씬 / 모달 / 프롬프트 다운로드.
 page.locator('#actFilter').select_option('3');assert page.locator('#sceneNav [data-scene]').count()==3
 page.locator('#search').fill('말하지');assert page.locator('#sceneNav [data-scene]').count()==1
 page.locator('#search').fill('해당없음');assert '검색 결과가 없습니다' in page.locator('#sceneNav').inner_text()
 page.locator('#search').fill('');page.locator('#actFilter').select_option('all');page.locator('#gridTab').click();assert page.locator('.card').count()==10
 page.locator('.card').first.click();assert page.locator('#detailView').is_visible()
 if page.locator('#showKey').count():page.locator('#showKey').click()
 page.locator('#openImage').click();assert page.locator('#imageDialog').is_visible();page.keyboard.press('Escape')
 page.locator('#compareFaces').click();assert page.locator('#faceDialog').is_visible();assert page.locator('#originalGirl').get_attribute('src')=='assets/characters.png';page.keyboard.press('Escape')
 page.locator('#references').click();page.locator('[data-ref="props_animals"]').click();assert page.locator('#referenceImage').get_attribute('src')=='assets/props_animals.png';page.keyboard.press('Escape')
 page.locator('#preview').click();assert 'S01-01' in page.locator('#slideTitle').inner_text();page.locator('#slideNext').click();assert 'S01-02' in page.locator('#slideTitle').inner_text();page.locator('#slidePlay').click();page.keyboard.press('Escape')
 with page.expect_download() as d:page.locator('#allPrompts').click()
 downloaded=ROOT/'storyboard_prompts_test.txt';d.value.save_as(downloaded);t=downloaded.read_text();assert 'S01-01' in t and 'S10-04' in t;downloaded.unlink()
 # ローカル 파일을 직접 열고 네트워크 없이 UI 동작 확인.
 if not allow_missing:page.screenshot(path=str(ROOT/'storyboard/PREVIEW_DESKTOP.png'),full_page=True)
 context.close()
 offline=browser.new_context(viewport={'width':390,'height':844})
 local=offline.new_page();local.on('pageerror',lambda e:errors.append(str(e)))
 requested=[];local.on('request',lambda r:requested.append(r.url))
 if not allow_missing:
  # 大きな独立HTMLはCDP経由のset_contentではなくHTTPでストリーム読込する。
  local.goto(f'http://127.0.0.1:{server.server_port}/exports/DONGBAEK_STORYBOARD_4MIN.html',wait_until='load',timeout=120000)
  offline.set_offline(True)
 else:
  html=(ROOT/'storyboard/index.html').read_text().replace('<script src="data.js"></script>','<script>'+(ROOT/'storyboard/data.js').read_text()+'</script>')
  local.set_content(html)
 assert local.locator('#clipTitle').is_visible()
 local.locator('[data-clip="1"]').click();assert 'S01-02' in local.locator('#clipTitle').inner_text()
 assert local.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
 local.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined});document.execCommand=()=>false;")
 local.locator('#copyKo').click();assert local.locator('#copyDialog').is_visible();assert 'S01-02' in local.locator('#manualCopy').input_value();local.keyboard.press('Escape')
 if not allow_missing:
  local.wait_for_function('document.getElementById("keyImage").complete && document.getElementById("keyImage").naturalWidth > 0')
  local.locator('#sceneNav [data-scene="S10"]').click()
  local.locator('[data-clip="3"]').click()
  local.wait_for_function('document.getElementById("keyImage").complete && document.getElementById("keyImage").naturalWidth > 0')
  assert local.locator('#keyImage').get_attribute('src').startswith('blob:')
  assert all(u.startswith(('blob:','data:',f'http://127.0.0.1:{server.server_port}/exports/DONGBAEK_STORYBOARD_4MIN.html')) for u in requested)
  local.locator('#sceneNav [data-scene="S01"]').click();local.locator('[data-clip="1"]').click()
  local.screenshot(path=str(ROOT/'storyboard/PREVIEW_MOBILE.png'),full_page=True)
 assert not errors,errors
 browser.close()
server.shutdown()
print('PASS: 35컷·240초·한영 클립보드·상태 저장/이동·검색·필터·미리보기·이미지 모달·전체 다운로드·오프라인·모바일')
if allow_missing:print('주의: 현재 실행은 이미지 로딩 검증 제외. 이미지 완료 후 전체 검증 필요.')
