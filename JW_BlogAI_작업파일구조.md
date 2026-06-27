---
type: project_file_structure
project: JW_BlogAI
created: "2026-06-27"
updated: "2026-06-27"
---

# JW_BlogAI 작업파일 구조

## 1. 루트 필수 파일

| 파일 | 역할 |
|---|---|
| `_INDEX.md` | 프로젝트 루트 색인/라우팅/문서·RDF 인덱스 |
| `JW_BlogAI_프로젝트개요.md` | 프로젝트 기본정보 SSOT |
| `JW_BlogAI_프로젝트로그.md` | 변경/결정/진행 이력 |
| `JW_BlogAI_프로젝트지침.md` | 작업 규칙/주의사항 |
| `JW_BlogAI_작업파일구조.md` | 파일 구조와 작업 단위 |

## 2. 표준 폴더

| 폴더 | 역할 |
|---|---|
| `01.JW_BlogAI_RP(보고)/` | 성과품/보고서/제안서 등 외부 제출 산출물 |
| `02.JW_BlogAI_RA(검토및분석)/` | 검토·분석·작업 산출물 |
| `03.JW_BlogAI_AD(행정)/` | 예산·인력·고객사·계약·입찰·정산 등 행정/사업관리 |
| `04.JW_BlogAI_RM(자료)/` | 원본/참고/회의/입찰 자료의 경량 인덱스 및 요약 |
| `05.JW_BlogAI_MT(관리)/` | 프로젝트 관리 문서, 로그, 지침, 작업구조 |
| `06.JW_BlogAI_SC(Scripts)/` | 자동화/분석 스크립트 |

## 3. 원본 및 메타데이터 연결

- GDrive 원본: 프로젝트별 GDrive 폴더
- RDFIndex: `00.System/RDFIndex/by_project/JW_BlogAI/`
- 대용량/바이너리 원본은 Git repo에 직접 넣지 않는다.
- 루트 `_INDEX.md`는 Markdown 문서와 RDF/GDrive 원본 인덱스를 집계한다.
