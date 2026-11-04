"""외부 라이브러리 없이 콘티 데이터·한영 영상 프롬프트를 빌드한다."""
from pathlib import Path
import csv,json,re
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'storyboard'
with (ROOT/'STEP_2_BREAKDOWN.csv').open(encoding='utf-8-sig',newline='') as f: source=list(csv.DictReader(f))
# 각 항목: 한글 동작, 영어 동작, 카메라(한/영), 대사, 소리(한/영).
A=[
[
('나가 괭이로 흙을 고른다.','The boy works the earth with his hoe.','와이드·눈높이·고정 / Wide, eye level, locked off','', '흙을 긁는 쇠날, 먼 닭소리 / Hoe scraping soil, distant rooster'),
('점순이가 감자 세 알을 내민다.','Jeomsun extends exactly three steaming potatoes.','미디엄 투숏·35mm·느린 전진 / Medium two-shot, 35mm, slow push in','점순이: 느 집엔 이런 거 없지? 뜨거울 때 먹어.','바람, 옷자락 / Breeze, cloth rustle'),
('나가 내민 감자를 흘끗 본다.','The boy glances at the offered potatoes.','얼굴 클로즈업·65mm·고정 / Face close-up, 65mm, locked off','', '멀리 우는 닭 / Distant rooster'),
('나가 고개를 돌린다.','The boy turns his face away.','미디엄·50mm·고정 / Medium, 50mm, locked off','나: 안 먹어. 너나 먹어.','바람, 숨 / Breeze, breath'),
('점순이가 내민 손을 거둔다.','Jeomsun withdraws her offered hands.','손에서 얼굴로 느린 틸트 / Slow tilt from hands to face','', '옷자락, 짧은 바람 / Cloth, brief breeze')],
[
('점순이가 큰 수탉을 울타리 밖에 내려놓는다.','Jeomsun sets the larger rooster down outside the fence.','미디엄·낮은 눈높이·고정 / Medium, low eye level, locked off','', '가벼운 날갯짓 / Light wingbeats'),
('큰 수탉이 작은 수탉 쪽으로 다가간다.','The larger rooster approaches the smaller rooster without contact.','로우 앵글·닭 눈높이·고정 / Low angle at rooster eye level, locked off','', '닭 울음, 흙 발소리 / Crowing, feet on dirt'),
('나가 괭이를 내려놓고 두 닭 사이로 뛰어든다.','The boy lowers his hoe and steps quickly between the two roosters.','미디엄 와이드·짧은 팬 / Medium wide, short pan','나: 야! 닭 좀 치워!','빠른 발소리, 날갯짓 / Quick footsteps, flapping'),
('점순이가 팔짱을 낀다.','Jeomsun folds her arms.','미디엄 클로즈업·50mm·고정 / Medium close-up, 50mm, locked off','점순이: 왜? 느 집 닭도 덤비잖아.','옷자락, 닭소리 / Cloth, rooster sounds')],
[
('나가 작은 수탉을 품에 안는다.','The boy holds his small rooster against his chest.','미디엄 투숏·50mm·고정 / Medium two-shot, 50mm, locked off','나: 점순이가 또 싸움 붙였어.','낮은 닭소리 / Soft rooster clucking'),
('어머니가 흐트러진 깃털을 살핀다.','Mother examines the rooster’s ruffled, uninjured feathers.','손과 닭 인서트·65mm·고정 / Hands and feathers insert, 65mm, locked off','', '깃털, 처마 밑 바람 / Feathers, breeze under eaves'),
('어머니가 나의 가리키는 손목을 내린다.','Mother lowers the boy’s pointing wrist.','미디엄 투숏·50mm·고정 / Medium two-shot, 50mm, locked off','어머니: 그 집은 마름이야. 밉보이면 밭도 못 부쳐.','옷자락 / Cloth rustle'),
('나가 입을 다문다.','The boy falls silent.','얼굴 클로즈업·65mm·느린 전진 / Face close-up, 65mm, slow push in','', '낮은 닭소리, 바람 / Soft clucking, breeze')],
[
('나가 고추장 종지를 땅에 놓는다.','The boy places the gochujang bowl on the earth.','종지 인서트·50mm·고정 / Bowl insert, 50mm, locked off','', '질그릇이 흙에 닿는 소리 / Earthenware on dirt'),
('나가 손가락 끝에 고추장을 묻힌다.','The boy dabs a tiny amount of gochujang on his fingertip.','손 클로즈업·65mm·고정 / Hand close-up, 65mm, locked off','', '종지 스침 / Soft touch against bowl'),
('나가 닭의 부리와 떨어진 곳에 손가락을 내민다.','The boy offers his fingertip well away from the rooster’s beak; no feeding.','로우 미디엄·50mm·고정 / Low medium, 50mm, locked off','나: 이거 먹으면 기운 난댔어. 이번엔 지지 마.','가벼운 푸드덕거림 / Light flapping'),
('작은 수탉이 뒤로 물러나자 나가 손을 멈춘다.','The small rooster steps back and the boy stops his hand.','같은 로우 미디엄·고정 / Same low medium, locked off','', '닭 발소리 / Rooster feet on dirt')],
[
('두 수탉이 서로를 향해 목을 세운다.','The two roosters raise their necks toward each other without contact.','로우 앵글·고정 / Low angle, locked off','', '닭 울음 / Rooster calls'),
('큰 수탉이 날개를 펼치자 작은 수탉이 물러난다.','The larger rooster spreads its wings as the smaller one retreats; no contact.','닭 눈높이·짧은 팬 / Rooster eye level, short pan','', '날갯짓 / Wingbeats'),
('나가 작은 수탉 앞에 몸을 낮춘다.','The boy lowers himself protectively in front of the smaller rooster.','미디엄 와이드·35mm·고정 / Medium wide, 35mm, locked off','', '옷자락, 발소리 / Cloth, footsteps'),
('점순이가 입가에 손을 댄다.','Jeomsun brings her fingertips to her faint teasing smile.','미디엄 클로즈업·50mm·고정 / Medium close-up, 50mm, locked off','점순이: 그것 봐. 또 졌네.','짧은 웃음 / Brief laugh'),
('나가 점순이를 올려다본다.','The crouching boy looks up sharply at Jeomsun.','나의 얼굴 클로즈업·65mm·고정 / Boy’s close-up, 65mm, locked off','나: 싸움 붙이지 말랬잖아!','닭소리, 거친 숨 / Roosters, tense breath')],
[
('나가 지게에 마른 나뭇가지를 얹는다.','The boy lays dry firewood on his wooden jige carrier.','와이드·35mm·고정 / Wide, 35mm, locked off','', '마른 가지 마찰음 / Dry twigs rubbing'),
('호드기 소리를 들은 나가 고개를 든다.','The boy lifts his head at the distant bark-whistle sound.','미디엄·50mm·느린 전진 / Medium, 50mm, slow push in','점순이(화면 밖 멀리서): 아이고, 또 밀리네.','멀리 호드기 다음 닭 울음 / Distant bark whistle followed by rooster call'),
('나가 지게를 내려놓는다.','The boy sets the jige and firewood on the trail.','미디엄 와이드·고정 / Medium wide, locked off','', '나무가 흙에 닿음 / Wood touching dirt'),
('나가 소리가 나는 쪽으로 달린다.','The boy runs downhill toward the offscreen sound, leaving the jige behind.','와이드·짧은 추적 팬 / Wide, brief tracking pan','', '달리는 발소리 / Running footsteps')],
[
('점순이가 호드기를 입에서 뗀다.','Jeomsun removes the straight bark whistle from her lips.','미디엄·50mm·고정 / Medium, 50mm, locked off','', '호드기 소리가 멎음 / Bark-whistle sound stops'),
('작은 수탉이 큰 수탉 앞에 웅크린다.','The small rooster crouches before the larger rooster, without contact.','로우 미디엄·고정 / Low medium, locked off','', '닭 울음 / Rooster calls'),
('나가 빈터로 뛰어들어 점순이 앞에 멈춘다.','The boy runs into the clearing and stops before Jeomsun.','미디엄 와이드·35mm·짧은 팬 / Medium wide, 35mm, short pan','나: 내 닭 죽겠잖아!','빠른 발소리, 거친 숨 / Quick feet, tense breath'),
('점순이가 호드기를 무릎에 내려놓는다.','Jeomsun lowers the straight bark whistle to her lap.','미디엄 클로즈업·50mm·고정 / Medium close-up, 50mm, locked off','점순이: 그럼 내 말 좀 듣든가.','옷자락, 바람 / Cloth, breeze'),
('큰 수탉이 고개를 내린다. 접촉 직전에 반응 컷으로 넘긴다.','The larger rooster lowers its head; cut away before any contact.','닭 인서트·낮은 앵글·고정 / Rooster insert, low angle, locked off','', '날갯짓 / Wingbeats'),
('나가 땅의 나뭇가지를 움켜쥔다.','The boy grips the single rough branch on the ground.','손 클로즈업·65mm·고정 / Hand close-up, 65mm, locked off','', '손과 나무의 마찰 / Hand gripping rough wood')],
[
('나가 나뭇가지를 휘두른다. 닭은 프레임 밖에 둔다.','The boy swings the branch; all animals remain outside the frame.','허리 위 미디엄·고정 / Waist-up medium, locked off','', '옷자락과 공기 가르는 소리 / Cloth, branch whoosh'),
('점순이의 얼굴이 굳는다. 화면 밖에서 둔탁한 소리가 한 번 난다.','Jeomsun’s face becomes still; one dull sound occurs offscreen, no impact shown.','점순이 클로즈업·65mm·고정 / Jeomsun close-up, 65mm, locked off','점순이: 너, 우리 닭 죽였지?','화면 밖 둔탁한 소리 한 번 / One dull offscreen sound'),
('정지한 큰 수탉을 멀리 두고 작은 수탉이 빈터 밖으로 달아난다.','A distant unobtrusive large rooster is motionless; the small rooster leaves the clearing. No wounds or blood.','빈터 와이드·35mm·고정 / Clearing wide, 35mm, locked off','', '작은 닭 발소리 / Small rooster’s feet'),
('나가 손에서 나뭇가지를 놓친다.','The boy releases the branch onto the earth.','손과 바닥 인서트·고정 / Hand and ground insert, locked off','', '가지 낙하음 / Branch dropping')],
[
('나가 점순이를 올려다본다.','The boy looks up at Jeomsun.','나의 얼굴 클로즈업·65mm·고정 / Boy’s close-up, 65mm, locked off','', '떨리는 숨 / Trembling breath'),
('나의 눈에 눈물이 흐른다.','Tears run down the boy’s face.','같은 얼굴 클로즈업·고정 / Same face close-up, locked off','나: 너희 집에서 우리 밭 뺏으면… 우린 어떡해.','훌쩍임 / Sniffling'),
('나가 소매로 눈을 문지른다.','The boy wipes his eyes with his ivory sleeve.','미디엄 클로즈업·50mm·고정 / Medium close-up, 50mm, locked off','', '소매 스침 / Sleeve brushing skin'),
('점순이가 다가와 몸을 낮춘다.','Jeomsun steps closer and lowers herself to his eye level.','미디엄 투숏·50mm·고정 / Medium two-shot, 50mm, locked off','점순이: 다시는 안 그럴 거지?','옷자락, 낮은 바람 / Cloth, soft breeze'),
('나가 고개를 끄덕인다.','The boy nods.','나의 클로즈업·65mm·고정 / Boy’s close-up, 65mm, locked off','나: 응.','짧은 숨 / Short breath'),
('점순이가 나의 눈을 바라본다.','Jeomsun holds the boy’s gaze.','점순이 클로즈업·65mm·느린 전진 / Jeomsun close-up, 65mm, slow push in','점순이: 그럼 나도 말 안 해.','바람 / Breeze')],
[
('점순이가 나의 어깨를 가볍게 민다.','Jeomsun lightly nudges the boy’s shoulder.','미디엄 투숏·35mm·고정 / Medium two-shot, 35mm, locked off','', '옷자락 / Cloth rustle'),
('점순이가 균형을 잃는 나의 소매를 잡는다.','Jeomsun catches the boy’s sleeve as he loses balance.','손과 소매 인서트·50mm·고정 / Hands and sleeve insert, 50mm, locked off','', '옷자락 스침 / Fabric movement'),
('두 사람이 풀밭에 나란히 내려앉는다.','Both settle gently side by side into the soft grass.','조금 높은 미디엄 와이드·35mm·고정 / Slightly high medium wide, 35mm, locked off','', '풀밭에 닿는 몸 / Soft bodies on grass'),
('꽃가지 아래에서 두 사람이 서로를 바라본다.','Under swaying yellow flowering twigs, they look at each other with a restrained innocent smile.','눈높이 투숏·50mm·느린 전진 / Eye-level two-shot, 50mm, slow push in','', '두 사람의 숨, 꽃가지 바람 / Breathing, breeze in twigs'),
('멀리서 부르는 소리에 점순이가 일어나 달려간다.','At a distant call, Jeomsun gets up and runs between the shrubs.','와이드·35mm·짧은 팬 / Wide, 35mm, short pan','점순이 어머니(화면 밖 멀리서): 점순아! / 점순이(작게): 먼저 가.','멀어지는 발소리 / Receding footsteps'),
('나가 소매에 붙은 노란 꽃 한 송이를 집는다.','The boy picks one tiny yellow spicebush blossom from his ivory sleeve.','손과 꽃 클로즈업·65mm·고정 / Hand and blossom close-up, 65mm, locked off','', '낮은 바람 / Soft breeze')]
]
KO='1930년대 강원 농촌의 이른 봄. 16:9 시네마틱 실사, 자연광, 절제된 흙빛 색감, 자연스러운 피부와 낡은 무명. 선택 원본 characters.png의 얼굴·체형·머리·의상·고름 형태를 그대로 유지한다. 나: 짧은 검은 머리, 미색 저고리, 회갈색 바지, 짚신. 점순이: 검은 댕기머리, 황토색 저고리, 짙은 자주색 치마, 검은 고무신. 어머니: 쪽머리, 회백색 저고리, 먹색 치마. 인물·소품이 늘어나거나 옷이 바뀌지 않는다. 작은 황갈색 수탉과 큰 적갈색 수탉을 구별한다. 노란 꽃은 생강나무 꽃이다. 현대 물건, 화면 글자, 자막, 캡션, 워터마크, 배경음악, 설명 내레이션 없음. 닭 타격 접촉·피·상처는 보여주지 않는다.'
EN='Early spring in a 1930s farming village in Gangwon, Korea. Cinematic photoreal live action, 16:9, natural light, muted earthy palette, real skin and worn cotton. Preserve the exact identities, bodies, hair, original clothing and original goreum designs from approved characters.png. Boy: short black hair, ivory jeogori, grey-brown baji, straw sandals. Jeomsun: black braid and dark ribbon, ochre jeogori, dark plum chima, black rubber shoes. Mother: low bun, grey-white jeogori, charcoal chima. Do not add characters, change costumes or duplicate props. Distinguish the small golden-brown and larger chestnut roosters. Yellow blossoms are Lindera obtusiloba spicebush. No modern objects, on-screen text, subtitles, captions, watermark, background music or narration. No animal impact, blood or wounds.'
conditions=[
'감자 정확히 3알. 나 왼쪽·점순이 오른쪽. 괭이 1개. 낮.',
'동일 울타리·좌우 위치. 괭이는 내려놓음. 닭 2마리 크기 차이. 낮.',
'나와 어머니만 화면 등장. 작은 닭은 품에 안김. 늦은 낮.',
'나와 작은 닭만 등장. 종지 1개. 고추장을 실제로 먹이지 않음. 며칠 뒤 낮.',
'같은 울타리 빈터. 나 왼쪽·점순이 오른쪽. 작은 닭 깃털 흐트러짐. 낮.',
'화면에는 나만 등장. 점순이는 멀리 음성만. 지게는 산길에 남음. 늦은 낮.',
'노란 꽃 군락 옆 빈터. 나 왼쪽·점순이 오른쪽. 호드기는 곧은 관. 지게 없음. 늦은 낮.',
'같은 빈터·같은 빛. 타격은 프레임 밖. 작은 닭 퇴장, 가지 바닥. 상처·피 없음.',
'같은 꽃밭. 가지 바닥·호드기 원래 자리. 작은 닭 없음. 나의 눈물·젖은 소매.',
'같은 노란 꽃 군락, 해질녘으로 서서히. 청소년 두 사람의 소박한 시선. 꽃 한 송이 소매→손. 어머니는 음성만.']
conditions_en=[
'Exactly three potatoes and one hoe; boy frame left, girl frame right; noon.',
'Same fence and screen positions; hoe lowered; two roosters of different sizes; noon.',
'Only boy and mother visible; small rooster in his arms; late afternoon.',
'Only boy and small rooster; one earthen bowl; no ingestion; a few days later, noon.',
'Same fence clearing; boy left, girl right; ruffled small rooster; noon.',
'Only boy visible; Jeomsun distant offscreen voice only; jige stays on trail; late afternoon.',
'Yellow spicebush clearing; boy left, girl right; whistle is a straight bark tube; no jige; late afternoon.',
'Same clearing and light; impact offscreen; small rooster leaves; branch on earth; no blood or injuries.',
'Same grove; branch on ground, whistle at original sitting place; small rooster absent; tears and wet ivory sleeve.',
'Same yellow grove, gradual sunset light; innocent restrained adolescent interaction; one blossom sleeve to hand; mother offscreen voice only.']
scenes=[];cursor=0
for i,(s,clips) in enumerate(zip(source,A)):
 assert len(clips)*5==int(s['길이(초)'])
 obj={'id':f'S{i+1:02}','number':i+1,'act':int(s['막']),'title':s['제목'],'location':s['장소'],'locationId':s['장소ID'],'time':s['시간'],'duration':int(s['길이(초)']),'start':cursor,'end':cursor+int(s['길이(초)']),'image':f'assets/S{i+1:02}.png','characters':s['등장인물'],'props':s['소품·동물'],'action':s['주요 행동'],'dialogue':s['대사'],'sound':s['음향'],'continuity':s['연속성'],'notes':s['제작 유의사항'],'imageType':'씬 대표 키프레임 · AI 생성 시안','clips':[]}
 for j,(ko,en,cam,dialogue,sound) in enumerate(clips):
  camerako,cameraen=cam.split(' / ',1);soundko,sounden=sound.split(' / ',1)
  audio_ko=('육성 대사(한국어 그대로): '+dialogue if dialogue else '대사 없음.')+' 환경음·효과음: '+soundko+'. 배경음악 없음.'
  audio_en=('Spoken dialogue in ORIGINAL KOREAN, never translate the speech: '+dialogue if dialogue else 'No spoken dialogue.')+' Diegetic sound: '+sounden+'. No background music.'
  ko_prompt=f'{obj["id"]}-{j+1:02} | 편집 목표 5초 | {s["장소"]} / {s["시간"]}\n{KO}\n연속성: {conditions[i]}\n이번 클립의 행동: {ko}\n카메라: {camerako}. 한 클립 안에서 임의의 컷 전환 없음.\n{audio_ko}\n참조: 이 씬의 대표 키프레임으로 얼굴·장소·조명을 맞춘다. 시작 자세와 앵글이 다르면 이 클립에 맞는 시작 프레임을 먼저 준비한다. 모델이 5초를 지원하지 않으면 지원 길이로 생성 후 편집에서 5초를 사용한다.'
  en_prompt=f'{obj["id"]}-{j+1:02} | Edit target: 5 seconds | {s["장소"]}\n{EN}\nContinuity: {conditions_en[i]}\nAction in THIS clip: {en}\nCamera: {cameraen}. One continuous shot with no spontaneous cuts.\n{audio_en}\nUse the scene keyframe as visual identity, location and lighting reference. If pose or camera differs, prepare a matching start frame first. If the model does not offer 5-second generation, generate a supported length and use 5 seconds in the edit.'
  obj['clips'].append({'id':f'{obj["id"]}-{j+1:02}','duration':5,'start':j*5,'actionKo':ko,'actionEn':en,'cameraKo':camerako,'cameraEn':cameraen,'dialogue':dialogue,'soundKo':soundko,'soundEn':sounden,'ko':ko_prompt,'en':en_prompt})
 scenes.append(obj);cursor+=obj['duration']
assert cursor==240 and sum(len(x['clips']) for x in scenes)==48
payload={'title':'동백꽃','version':'콘티 v1.0','duration':240,'scenes':scenes,'notes':'10개 대표 키프레임, 48개 5초 편집 구간. 실제 영상은 아직 생성하지 않았음.'}
(OUT/'storyboard.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
(OUT/'data.js').write_text('window.STORYBOARD = '+json.dumps(payload,ensure_ascii=False,indent=2)+';\n')
md=['# 동백꽃 — Flow용 영상 프롬프트\n','10씬 / 240초 / 48개 클립. 각 5초는 편집 목표다. Flow에서 선택한 모델이 제공하는 생성 길이를 사용한 뒤 편집한다. 한국어 음성이 지원되지 않거나 불명확하면 대사를 별도 녹음·합성하여 편집한다. 영상은 아직 생성하지 않았다.\n','씬별 대표 키프레임 1장씩 총 10장이다. 모든 클립의 첫 프레임이 준비된 것은 아니다. 다른 앵글·자세는 해당 클립 시작 이미지를 추가 준비하거나 이전 영상의 마지막 프레임을 사용한다.\n']
for s in scenes:
 md.append(f'\n## {s["id"]}. {s["title"]} — {s["duration"]}초\n')
 for c in s['clips']:
  md.append(f'\n### {c["id"]}\n\n#### 한글\n\n```text\n{c["ko"]}\n```\n\n#### English\n\n```text\n{c["en"]}\n```\n')
(OUT/'VIDEO_PROMPTS.md').write_text('\n'.join(md))
# JSON은 교환용. HTML은 file://에서도 작동하도록 data.js 대신 인라인 데이터 사용.
print('생성 완료: 10씬 / 240초 / 한영 프롬프트 48쌍')
