"""승인 시나리오 및 브레이크다운에서 제작 리스트를 생성한다. 외부 서비스 불필요."""
from pathlib import Path
from io import BytesIO
import csv,re
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'production_lists'; OUT.mkdir(exist_ok=True)
with (ROOT/'STEP_2_BREAKDOWN.csv').open(encoding='utf-8-sig',newline='') as f: scenes=list(csv.DictReader(f))
source=(ROOT/'STEP_1_SCREENPLAY.md').read_text()
source_scenes=re.findall(r'### 씬 (\d+)\. (.*?) — (\d+)초',source)
assert [(int(s['씬']),s['제목'],int(s['길이(초)'])) for s in scenes]==[(int(n),t,int(d)) for n,t,d in source_scenes]
assert len(scenes)==10 and sum(int(s['길이(초)']) for s in scenes)==240
fmt=lambda ns:', '.join(f'S{n:02}' for n in ns)
# 등장 유형을 구분한다: 화면 등장 / 음성 / 화면 밖에 남은 소품의 연속성.
chars=[
['C01','나','주인공 / 소작농의 아들',fmt(range(1,11)),'없음','청소년 소년; 마른 체격·짧은 검은 머리(외형 제안)','미색 저고리·회갈색 바지·짚신(제안)','호의 거절→닭 보호→분노→두려움→꽃밭에서 점순이를 바라봄','흙 묻은 손·무릎 / S09 눈물·젖은 소매 / S10 풀 부착','최상','인물 보드 왼쪽; 얼굴 시안 있음 / 고름·여밈 고증 보류'],
['C02','점순이','마름의 딸 / 갈등과 전환의 중심',fmt([1,2,5,7,8,9,10]),'S06: 멀리서 들리는 음성','청소년 소녀; 둥근 얼굴·검은 댕기머리(제안)','황토색 저고리·자주색 치마·고무신(제안)','감자 건넴→닭싸움→비밀 약속→꽃밭에서 함께 넘어짐','감자 3알 / 호드기 입→무릎 / 머리·의상 유지','최상','인물 보드 가운데; 얼굴 시안 있음 / 고름·여밈 고증 보류'],
['C03','나의 어머니','마름·소작 관계의 압박을 전달','S03','없음','중년 여성; 쪽진 머리(제안)','회백색 저고리·먹색 치마(제안)','수탉을 살피며 아들에게 경고','나의 손목을 내리는 손동작; 시선 연결','중','인물 보드 오른쪽; 시안 있음 / 복식 고증 보류'],
['C04','점순이 어머니','두 사람의 꽃밭 장면을 끝내는 호출','없음','S10: 멀리서 점순이를 부름','외형 설정 불필요','의상 이미지 불필요','화면 밖에서 “점순아!”라고 부름','먼 거리의 여성 음성; C03과 구분','중','음성만 필요 / 이미지 없음']]
props=[
['P02','핵심 소품','찐 감자 세 알','S01','없음','점순이의 호의와 나의 거절을 드러냄','3알','최상','흙빛 껍질·옅은 김; 승인 대본은 찐 감자다. 첨부 예시의 구운 감자로 변경하지 않음','소품 보드 1행 오른쪽'],
['A01','동물','나의 작은 수탉',fmt([2,3,4,5,7,8]),'S01·S06 닭소리: 개체 미지정','나를 대신하는 약한 존재; 보호·반격 동기','1마리','최상','황갈색 깃털·짧은 검은 꼬리 제안; S08 달아난 뒤 재등장 없음','소품 보드 4행 왼쪽'],
['A02','동물','점순이네 큰 수탉',fmt([2,5,7,8]),'S09: 정지한 몸의 배경 연속성(노출 선택)','갈등을 격화시키고 죽음으로 전환점을 만듦','1마리','최상','적갈색 몸·긴 녹흑색 꼬리 제안; A01보다 크게 고정; 타격 접촉·피 없음','소품 보드 4행 오른쪽'],
['D01','세트 미술','두 집 사이 낮은 나무 울타리',fmt([1,2,5]),'S03: 두 집 방향 연결 참고','두 집의 경계와 갈등 장소를 형성','연결 세트 1식','상','배치·재료·높이를 고정; 울타리 제작·파손 사건은 현 대본에 없음','장소 보드 왼쪽 위'],
['P08','자연물·핵심 모티프','노란 생강나무 꽃',fmt([7,8,9,10]),'S08·S09: 같은 장소의 배경 연속성','갈등과 결말의 공간; S10 소매의 꽃 한 송이','군락 1식 + 꽃 1송이','최상','Lindera obtusiloba; 붉은 동백 아님; 이른 봄·잎 적은 가지; S10 소매→손','소품 보드 3행 오른쪽 / 장소 보드 오른쪽 아래'],
['P01','농기구','괭이',fmt([1,2]),'없음','나의 밭일과 뛰어드는 행동을 연결','1개','상','낡은 나무 자루·무광 쇠날; S02 내려놓는 위치 고정','소품 보드 1행 왼쪽'],
['P03','생활 소품','고추장 종지와 고추장','S04','없음','수탉을 강하게 만들려는 시도를 보여줌','종지 1개 + 내용물','상','작은 갈색 질그릇; 실제 섭취 미노출; 손가락의 고추장 연결','소품 보드 2행 왼쪽'],
['P04','운반 도구','지게','S06','S07 이후: 산길에 내려놓은 상태','나무하는 일과 산길 동선 설정','1개','상','나무 지게·짚 끈; S06 내려놓음; 꽃밭에 갑자기 등장하지 않음','소품 보드 2행 오른쪽'],
['P05','생활 소품','땔감 묶음','S06','없음','지게에 얹는 노동 동작','1묶음','중','마른 가지; 묶음 양·끈 위치 유지','소품 보드 2행 오른쪽'],
['P06','악기·음향 소품','호드기','S07','S06 소리 / S08~S10 현장에 남은 상태','점순이의 존재를 소리로 알림','1개','상','짧고 곧은 나무껍질 관 제안; 담뱃대 형태 수정 완료; S07 입→무릎; 이후 회수는 미기재','소품 보드 3행 왼쪽 위'],
['P07','행동 소품','휘두르는 나뭇가지',fmt([7,8]),'S09: 바닥에 남은 가지','수탉의 죽음을 일으키는 행동 소품','1개','상','형태·길이 고정; S07 땅→손, S08 손→땅; 접촉은 화면 밖','소품 보드 3행 왼쪽 아래']]
locations=[
['L01','밭·두 집 사이 울타리·빈터','EXT',fmt([1,2,5]),'봄 낮 / S05는 며칠 뒤','감자 거절과 반복되는 닭싸움','밭고랑·흙길·낮은 울타리·멀리 초가 두 집','P01·P02·D01 / A01·A02','두 집 방향과 인물 좌우 고정; L02와 이어짐','최상','현대 시설 제외; 장소 보드 왼쪽 위 / 시안 있음'],
['L02','나의 집 마당·뒤꼍','EXT',fmt([3,4]),'S03 늦은 낮 / S04 며칠 뒤 낮','어머니 경고와 고추장 시도','초가·흙마당·처마·흙벽','P03 / A01','S03 마당과 S04 뒤꼍을 구분; L01 방향 연결','상','기본 가옥은 공통, 세부 공간 구분; 보드 오른쪽 위 / 시안 있음'],
['L03','산기슭 나무하는 길','EXT','S06','다음 날 늦은 낮','나무하기→호드기·닭소리→달려감','흙길·마른 가지·마을을 내려다보는 경사','P04·P05 / 화면 밖 P06 음향','지게를 놓은 지점 고정; L04까지의 동선 연결','상','꽃밭은 아래쪽으로 설정; 보드 왼쪽 아래 / 시안 있음'],
['L04','노란 꽃 군락 옆 빈터·풀밭','EXT',fmt([7,8,9,10]),'늦은 낮→해 질 무렵, 연속','최종 닭싸움·수탉의 죽음·약속·꽃밭 결말','노란 생강나무 군락·낮은 가지·풀밭·인접 흙바닥','P06·P07·P08 / A01·A02','꽃밭과 빈터는 한 지형; 가지·닭·호드기 위치 연결','최상','노란 꽃 유지; 조명 급변 방지; 보드 오른쪽 아래 / 시안 있음']]
scene_headers=['씬','막','제목','INT/EXT','장소 ID','장소','시간','길이(초)','화면 등장','음성만 등장','주요 행동','소품·동물·세트 ID','음향','연속성·제작 노트','영상 상태']
scene_rows=[]
for s in scenes:
 n=int(s['씬']); visible=['C01'];voice=[]
 for c in chars[1:]:
  if f'S{n:02}' in c[3].split(', '):visible.append(c[0])
 if n==6:voice=['C02']
 if n==10:voice=['C04']
 asset=s['소품·동물']
 extra={1:'D01',2:'D01',5:'D01',6:'P06(소리)',7:'P08(장소)',8:'P06·P08(배경)',9:'P08(배경)',10:''}.get(n,'')
 scene_rows.append([n,int(s['막']),s['제목'],s['INT/EXT'],s['장소ID'],s['장소'],s['시간'],int(s['길이(초)']),', '.join(visible),', '.join(voice) or '없음',s['주요 행동'],asset+(' / '+extra if extra else ''),s['음향'],s['연속성']+' / '+s['제작 유의사항'],'미착수'])
lists=[('1_씬리스트',scene_headers,scene_rows,None),('2_인물리스트',['ID','인물','역할','화면 등장 씬','음성만 등장','외형·나이 설정','의상 제안','극적 기능','연속성','우선순위','레퍼런스·제작 상태'],chars,'characters.png'),('3_소품리스트',['ID','분류','소품명','화면·장소 등장 씬','음향·잔존 연속성','용도·연출 의미','수량·비고','우선순위','제작·생성 노트','레퍼런스 위치'],props,'props_animals.png'),('4_장소리스트',['ID','장소명','INT/EXT','등장 씬','시간','극적 기능','필수 공간·미술','관련 소품·동물','연결·연속성','우선순위','레퍼런스·제작 상태'],locations,'locations.png')]
wb=Workbook();ov=wb.active;ov.title='0_요약'
for row in [('항목','내용'),('작품','동백꽃 — AI 단편영화 제작'),('기준','사용자 승인 STEP_1_SCREENPLAY.md v0.1 / 10씬 / 240초'),('인물','4명: 화면 3명 + 음성만 1명. 점순이는 S06에서 음성만 등장'),('소품 관리','11항목: 소품·자연물 8 + 동물 2 + 울타리 세트 1'),('장소','4개 장소 묶음. 마당·뒤꼍 및 빈터·꽃밭은 하위 공간 구분'),('첨부 표와 차이','첨부 예시는 표 구조만 참고. 11씬·구운 감자·울타리 제작 사건을 현 대본에 추가하지 않음'),('의상 검토','고름·여밈 위치는 고증 미완료. 기존 생성 이미지는 확정본이 아닌 시안'),('음향','배경음악 없음. 호드기는 장면 속 소리. 화면 자막·텍스트 없음'),('레퍼런스','외부 연결 없이 열리는 기존 이미지 보드를 각 리스트 오른쪽에 삽입. 행별로 해당 패널 위치 기재'),('상태','문서·참고 이미지 작성 / 씬별 영상 미착수 / 커밋·푸시 없음')]:ov.append(row)
for name,headers,rows,ref in lists:
 ws=wb.create_sheet(name);ws.append(headers)
 for row in rows:ws.append(row)
 with (OUT/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(rows)
 if ref:
  img=Image(ROOT/'assets/references'/ref)
  scale=min(420/img.width,600/img.height);img.width*=scale;img.height*=scale
  col=get_column_letter(len(headers)+2)
  ws[f'{col}1']='공통 레퍼런스 보드 · 행별 패널 위치 참조'
  ws.add_image(img,f'{col}2');ws.column_dimensions[col].width=62
  if name=='3_소품리스트':
   more=Image(ROOT/'assets/references/locations.png'); scale=420/more.width;more.width*=scale;more.height*=scale
   ws[f'{col}12']='울타리·꽃밭 참고: 장소 보드';ws.add_image(more,f'{col}13')
 # 표의 필터·인쇄 범위는 이미지 열과 분리한다.
 ws.auto_filter.ref=f'A1:{get_column_letter(len(headers))}{len(rows)+1}'
 ws.print_area=f'A1:{get_column_letter(len(headers))}{len(rows)+1}'
md=['# 동백꽃 — 시나리오 분석 제작 리스트\n','기준: 승인된 10씬 시나리오. 총 240초. 외형·의상은 제안이며 고름 고증은 미완료.\n']
for name,headers,rows,ref in lists:
 md.extend(['\n## '+name+'\n','| '+' | '.join(headers)+' |','|'+'---|'*len(headers)])
 for row in rows:md.append('| '+' | '.join(str(v).replace('|','/').replace('\n',' ') for v in row)+' |')
(OUT/'PRODUCTION_LISTS.md').write_text('\n'.join(md)+'\n')
for ws in wb:
 ws.freeze_panes='A2';ws.sheet_view.showGridLines=False
 maxcol=2 if ws==ov else len(next(x[1] for x in lists if x[0]==ws.title))
 for row in ws.iter_rows(max_col=maxcol):
  for c in row:
   c.font=Font(name='맑은 고딕',size=11,color='172B4D',bold=c.row==1)
   c.alignment=Alignment(vertical='top',wrap_text=True)
   c.fill=PatternFill('solid',fgColor='203B63' if c.row==1 else ('FFF2CC' if ws.title=='3_소품리스트' else ('F0F4F8' if c.row%2==0 else 'FFFFFF')))
   if c.row==1:c.font=Font(name='맑은 고딕',bold=True,color='FFFFFF',size=11)
   c.border=Border(bottom=Side(style='hair',color='CBD5E1'))
  ws.row_dimensions[row[0].row].height=32 if row[0].row==1 else (110 if ws.title=='1_씬리스트' else 82)
 for c in range(1,maxcol+1):ws.column_dimensions[get_column_letter(c)].width=24
 ws.column_dimensions['A'].width=12
 ws.sheet_properties.pageSetUpPr.fitToPage=True
 ws.page_setup.orientation='landscape';ws.page_setup.paperSize=ws.PAPERSIZE_A3;ws.page_setup.fitToWidth=1;ws.page_setup.fitToHeight=0
 ws.print_title_rows='1:1'
ov.column_dimensions['A'].width=23;ov.column_dimensions['B'].width=105
for sheet,cols in [('1_씬리스트',{'K':65,'L':40,'N':50,'H':12}),('2_인물리스트',{'F':40,'G':40,'H':45,'I':40,'K':42}),('3_소품리스트',{'E':38,'F':42,'I':65,'J':40}),('4_장소리스트',{'G':42,'I':48,'K':50})]:
 if sheet in wb:
  for col,width in cols.items():wb[sheet].column_dimensions[col].width=width
path=ROOT/'DONGBAEK_PRODUCTION_LISTS.xlsx';wb.save(path)
check=load_workbook(path)
assert check.sheetnames==['0_요약']+[x[0] for x in lists]
assert [check[n].max_row for n in ['1_씬리스트','2_인물리스트','3_소품리스트','4_장소리스트']]==[11,5,12,5]
assert sum(check['1_씬리스트'].cell(r,8).value for r in range(2,12))==240
assert sum(len(check[n]._images) for n in check.sheetnames)==4
for name,headers,rows,_ in lists:
 with (OUT/(name+'.csv')).open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f)))==len(rows)
print('검증 완료: 10씬·240초 / 인물 4명 / 소품 관리 11항목 / 장소 4묶음 / 내장 이미지 4개')
print(path)
