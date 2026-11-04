# dongbaek-ai-film-jecheon
11/7 동백꽃 제천강의

## 콘티 보기 · 다운로드

### 키 이미지와 영상 프롬프트만 받기 — 10.48MB

**[keyframes-and-prompts.zip 파일 화면 열기](https://github.com/dream-funny/dongbaek-ai-film-jecheon/blob/main/downloads/keyframes-and-prompts.zip)**

파일 화면 오른쪽 위의 **↓ Download raw file(원본 파일 다운로드)**를 누르세요. 파일 미리보기가 지원되지 않는다는 안내가 나와도 다운로드할 수 있습니다.

이 ZIP에는 **키 이미지 JPEG 35장 + 한글·영어 영상 프롬프트 + 컷별 편집표**만 들어 있습니다. HTML은 포함하지 않았습니다.



### 작은 ZIP으로 받기 — 권장

**[콘티·이미지 35장·프롬프트 ZIP 다운로드 — 22.0MB](https://github.com/dream-funny/dongbaek-ai-film-jecheon/blob/main/downloads/DONGBAEK_LIGHT_PACKAGE.zip)**

압축을 풀고 **`DONGBAEK_STORYBOARD_LIGHT.html`**을 더블클릭하세요. 이미지·프롬프트·복사 버튼이 모두 들어 있으며 설치가 필요하지 않습니다.

- [다운로드 파일 목록과 고화질 원본 PNG](downloads/README.md): 원본은 씬별 약 7~11MB로 나눴습니다.
- [이미지 35장·컷별 프롬프트를 GitHub에서 바로 보기](storyboard/GALLERY.md)
- [실행·Flow 사용 방법](storyboard/README.md)

비공개 저장소 접근 권한이 있는 GitHub 계정으로 로그인하세요. 파일 페이지가 열리면 **Download raw file / 원본 파일 다운로드**를 누르세요. GitHub 파일 화면은 소스 보기이며 HTML 콘티 실행 화면이 아닙니다.

경량판은 이미지의 얼굴·구도·픽셀 크기를 바꾸지 않고 JPEG 압축만 적용했습니다. PNG 원본도 그대로 보관합니다.

## 제작 현황

2026년 11월 7일 제천 청년센터 AI 영화 제작 실습 · 강사 유양석

- [STEP 1 시나리오 초안](STEP_1_SCREENPLAY.md): 3막, 10개 씬, 4분. 사용자 승인 완료.
- [STEP 2 제작 브레이크다운](STEP_2_BREAKDOWN.md) 및 [엑셀용 CSV](STEP_2_BREAKDOWN.csv): 외형·미술 설정 제안 포함.
- [작업 기록](WORK_LOG.md)

## 열람 방법

현재 결과물은 Markdown 문서입니다. GitHub 또는 편집기에서 위 파일을 열어 확인합니다. 설치나 실행 명령은 필요하지 않습니다. HTML 콘티와 실행 방법은 해당 제작 단계에서 추가합니다.

클라우드 대화 기록과 GitHub 파일 기록은 별도로 관리합니다. 커밋과 푸시는 사용자 승인 후 수행합니다.

- [제작 브레이크다운 엑셀 통합문서](DONGBAEK_PRODUCTION_BREAKDOWN.xlsx): 개요·씬별 상세·캐릭터·장소·소품·체크리스트 6개 시트.

## 이미지 기준 자료

[제작 기준과 이미지 목록](IMAGE_REFERENCES.md) · [한글·영어 생성 프롬프트](IMAGE_PROMPTS.md)

인물·장소·소품·동물·의상 참고 보드 4장을 `assets/references/`에 저장했습니다. 제작 시안이며 최종 승인 전입니다. 이미지 모델 버전은 확인되지 않았습니다.

## 시나리오 분석 리스트

[씬·인물·소품·장소 리스트 통합 엑셀](DONGBAEK_PRODUCTION_LISTS.xlsx) · [문서 및 개별 CSV](production_lists/PRODUCTION_LISTS.md)

10씬·4명·소품 관리 11항목·장소 4묶음. `python3 tools/build_production_lists.py`로 재생성합니다(openpyxl, Pillow 필요).

## 캐릭터 설명과 시트

[캐릭터북 엑셀](DONGBAEK_CHARACTER_BOOK.xlsx) · [캐릭터 설명](CHARACTERS.md) · [사용자 선택 원본](assets/references/characters.png)

인물 4명 설명, 화면 등장 3명의 얼굴·전신은 사용자가 고른 최초 공통 보드를 기준으로 합니다. 후속 고름 수정본은 미채택입니다. 후면 확정 이미지는 없습니다. `python3 tools/build_character_book.py`로 재생성합니다(openpyxl, Pillow 필요).

## 통합 제작 엑셀

[동백꽃 통합 제작 마스터](DONGBAEK_PRODUCTION_MASTER.xlsx): 두 통합문서를 합친 9개 시트. 요약·씬·인물·소품·장소·캐릭터 설명·인물별 시트를 포함합니다. 기존 파일은 유지합니다. `python3 tools/merge_production_books.py`로 재생성합니다.

## 현재 Flow 제작 기준

10씬·35컷·240초. 컷당 8초 생성 후 앞 4~8초 사용. 어머니는 음성만, 고추장 장면은 나와 작은 수탉만, 감자는 흰 무명 앞치마로 감쌉니다.

[현재 편집본](storyboard/EDITED_SCREENPLAY.md) · [영상 프롬프트](storyboard/VIDEO_PROMPTS.md) · [35컷 편집표](storyboard/FLOW_EDIT_LIST.csv)

이전 시나리오와 엑셀은 이전 버전의 이력입니다. 현재 제작은 위 Flow 편집본을 기준으로 합니다. 기존 대용량 배포본 대신 `downloads/`의 경량 ZIP을 사용하세요. 제작 원본은 `storyboard/assets/`와 씬별 PNG ZIP에 보관합니다.
