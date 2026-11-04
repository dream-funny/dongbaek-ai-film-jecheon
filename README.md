# dongbaek-ai-film-jecheon
11/7 동백꽃 제천강의

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
