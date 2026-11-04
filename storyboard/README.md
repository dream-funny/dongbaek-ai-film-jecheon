# 동백꽃 — 4분 Flow AI 콘티

현재 제작 기준은 **EDITED_SCREENPLAY.md / Flow 편집본 v1.1**입니다. 최초 시나리오의 사건 순서와 씬별 길이를 유지하며 사용자 수정 사항을 반영했습니다.

- 10개 씬, 35개 컷, 최종 편집 길이 240초.
- Flow에서 컷당 8초 생성 기준: 총 280초를 생성하고 컷별 앞 4~8초를 사용합니다. 실제 선택 모델의 지원 길이는 Flow에서 확인합니다.
- 어머니는 화면 밖 목소리만 등장합니다. 닭싸움 장면에 어머니가 없습니다.
- 고추장 장면은 ‘나’와 작은 수탉만 등장합니다. 점순이가 없습니다.
- 감자는 흰색 무명 허리 앞치마 아랫단으로 감쌉니다. 손은 천만 잡습니다. 감자는 세 알입니다.
- 키 이미지는 컷의 동작이 시작되기 직전의 첫 프레임입니다. 대표 이미지 하나를 여러 클립의 시작 프레임으로 재사용하지 않습니다.
- 인물은 사용자가 선택한 최초 얼굴·의상 기준을 참조합니다. 고름을 새로 디자인하지 않습니다.
- 배경음악·영상 화면 자막·설명 내레이션 없음. 필요한 한국어 육성 대사·환경음·효과음만 사용합니다.

## 열기

1. [작은 ZIP 다운로드](https://github.com/dream-funny/dongbaek-ai-film-jecheon/raw/refs/heads/main/downloads/DONGBAEK_LIGHT_PACKAGE.zip)를 누릅니다(약 22MB).
2. 압축을 풀고 **DONGBAEK_STORYBOARD_LIGHT.html**을 브라우저로 엽니다. 이미지와 데이터가 내장되어 다른 파일을 옮기지 않아도 됩니다.
3. images 폴더에는 Flow에 바로 첨부할 JPEG 35장이 있습니다. 원본 PNG가 필요하면 [씬별 ZIP](../downloads/README.md)을 받습니다.
4. GitHub에서 다운로드 없이 내용만 보려면 [이미지·프롬프트 보기](GALLERY.md)를 엽니다.

경량 HTML의 **현재 이미지 PNG 저장**은 압축 미리보기를 PNG로 변환합니다. 원본 PNG와 바이트가 같지는 않으며, 무손실 원본은 씬별 ZIP입니다. 압축 과정에서 얼굴·구도·픽셀 크기는 변경하지 않습니다.

## Flow에서 영상 만들기

1. 씬을 고른 뒤 그 안의 컷을 선택합니다.
2. 컷 번호와 시작 자세를 확인하고 **키 이미지 저장**을 누릅니다.
3. Flow에서 이미지로 영상 만들기의 첫 프레임으로 같은 번호의 PNG를 첨부합니다.
4. 해당 컷의 **한글 복사** 또는 **영어 복사**로 영상 프롬프트를 붙여넣습니다. 영어 프롬프트에서도 실제 발화는 한국어로 지정합니다.
5. 8초로 생성하고, 편집표에 적힌 앞 4~8초를 사용합니다. 영상 모델의 출력·대사 타이밍이 맞지 않으면 재생성하거나 편집합니다.
6. `FLOW_EDIT_LIST.csv` 순서대로 이어 붙이면 240초입니다. 오프닝·엔딩 카드는 이 240초에 포함하지 않았습니다.

HTML은 Flow에 자동 접속하거나 영상을 생성하지 않습니다. 시작 이미지와 프롬프트를 준비한 제작 도구입니다. 실제 영상 생성 성공이나 한국어 음성 정확도는 아직 검증하지 않았습니다.

## 다른 컴퓨터로 이동

페이지의 진행 상태·체크·메모는 해당 브라우저의 로컬 저장소에만 보관됩니다. **작업 상태 내보내기**로 JSON을 저장하고 다른 컴퓨터에서 **가져오기**를 누릅니다. GitHub나 ChatGPT 대화에 자동 동기화되지 않습니다.

## 파일

- `assets/S01-01.png` ~ `assets/S10-04.png`: 컷별 시작 이미지(씬마다 컷 수가 다름).
- `VIDEO_PROMPTS.md`: 모든 컷의 한글·영어 영상 프롬프트와 시작 이미지 프롬프트.
- `FLOW_EDIT_LIST.csv`: 생성 길이·실사용 길이·전체 타임코드.
- `EDITED_SCREENPLAY.md`: 현재 편집본.
- `storyboard.json`: 교환용 데이터.
- `data.js`: 별도 서버 없이 동작하는 HTML 데이터.

재생성: `python3 tools/revise_storyboard_flow.py` → 이미지 파일 확인 → `python3 tools/package_storyboard.py`.
브라우저 검증: `python3 tools/check_storyboard.py`(Playwright 및 Chromium 필요).

## 배포 파일과 Git 기록

`downloads/`에 경량 HTML·ZIP과 씬별 원본 PNG ZIP을 저장합니다. 모두 GitHub 파일당 제한 이내입니다. `exports/`의 이전 대용량 배포본은 기본 다운로드 경로에서 제외했습니다.

재생성: `python3 tools/package_light_storyboard.py`(ImageMagick 필요). 경량판 검증: `python3 tools/check_light_storyboard.py`.
