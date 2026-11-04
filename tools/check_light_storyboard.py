from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import threading,json
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
s=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start()
errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 ctx=b.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'],accept_downloads=True)
 page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{s.server_port}/downloads/DONGBAEK_STORYBOARD_LIGHT.html')
 ctx.set_offline(True)
 data=json.loads((ROOT/'storyboard/storyboard.json').read_text())
 for scene in data['scenes']:
  page.locator('#sceneNav [data-scene="'+scene['id']+'"]').click()
  for idx,c in enumerate(scene['clips']):
   page.locator('[data-clip="'+str(idx)+'"]').click()
   page.wait_for_function('document.getElementById("keyImage").complete && document.getElementById("keyImage").naturalWidth>0')
   assert c['id'] in page.locator('#clipTitle').inner_text()
   assert page.evaluate('fetch(document.getElementById("keyImage").src).then(r=>r.blob()).then(b=>b.type)')=='image/jpeg'
 last=data['scenes'][-1]['clips'][-1]
 page.locator('#copyKo').click();assert page.evaluate('navigator.clipboard.readText()')==last['ko']
 page.locator('#copyEn').click();assert page.evaluate('navigator.clipboard.readText()')==last['en']
 with page.expect_download() as d:page.locator('#downloadKey').click()
 tmp=ROOT/'downloads/_test.png';d.value.save_as(tmp)
 assert tmp.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
 with Image.open(tmp) as im:
  with Image.open(ROOT/'storyboard'/last['image']) as original:assert im.size==original.size
 tmp.unlink()
 page.locator('#preview').click();page.locator('#slidePlay').click();page.keyboard.press('Escape')
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 b.close()
s.shutdown()
print('PASS: 경량 HTML 오프라인 35장·JPEG MIME·한영 복사·실제 PNG 저장·해상도·모바일')
