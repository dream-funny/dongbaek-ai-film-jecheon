from pathlib import Path
import json,threading
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent;P=ROOT/'storyboard'
clips=[c for s in json.loads((P/'storyboard.json').read_text())['scenes'] for c in s['clips'] if (P/c['image']).exists()]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(P)));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as x:
 b=x.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1000})
 for n in range(0,len(clips),12):
  html='<html><meta charset="utf-8"><body style="background:#ddd;font:14px sans-serif;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">'
  for c in clips[n:n+12]:html+=f'<div>{c["id"]} · {c["startTitle"]}<img src="{c["image"]}" style="display:block;width:100%;aspect-ratio:16/9;object-fit:contain"></div>'
  (P/'qa.html').write_text(html+'</body></html>');page.goto(f'http://127.0.0.1:{server.server_port}/qa.html?page={n}');page.screenshot(path=f'/tmp/dongbaek-review-{n//12+1}.png',full_page=True)
  print(f'/tmp/dongbaek-review-{n//12+1}.png')
 b.close()
server.shutdown();(P/'qa.html').unlink(missing_ok=True)
