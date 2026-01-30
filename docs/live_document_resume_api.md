# Live Document: Resume API 엔드포인트 구축

> 브랜치: `claude/build-resume-endpoint-XFRW5`
> 작업일: 2026-01-30
> 상태: **진행 중**

---

## 1. 작업 목표

BG_AIPro 프로젝트에 **이력서(Resume) 데이터를 REST API로 제공**하는 엔드포인트를 구축한다.

---

## 2. 프로젝트 현황 (작업 전)

- Python 3.11+ 기반 AI 블로그 자동화 시스템
- CLI 전용 (`bgai` 명령어) — 웹 서버 없음
- Hugo 정적 사이트 + GitHub Pages 배포
- 기존 API 엔드포인트 없음, Resume 관련 파일 없음

---

## 3. 구현 내용

### 3.1 추가/수정된 파일

| 파일 | 설명 | 상태 |
|------|------|------|
| `pyproject.toml` | `fastapi`, `uvicorn` 의존성 추가 | 수정 |
| `src/resume/__init__.py` | Resume 모듈 패키지 초기화 | 신규 |
| `src/resume/models.py` | Pydantic 데이터 모델 (Resume, Experience 등) | 신규 |
| `src/resume/api.py` | FastAPI 라우터 및 엔드포인트 | 신규 |
| `data/resume.yaml` | 샘플 이력서 YAML 데이터 | 신규 |
| `src/cli.py` | `bgai serve` 명령어 추가 | 수정 |
| `run_server.py` | 모듈 경로 문제 해결용 실행 스크립트 | 신규 |
| `resume_server.py` | **단독 실행 가능한 올인원 서버 스크립트** | 신규 |

### 3.2 API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/resume` | 전체 이력서 조회 |
| GET | `/api/resume/contact` | 연락처 정보 |
| GET | `/api/resume/experience` | 경력 사항 |
| GET | `/api/resume/education` | 학력 사항 |
| GET | `/api/resume/skills` | 기술 스택 |
| GET | `/api/resume/projects` | 프로젝트 목록 |
| GET | `/api/resume/certifications` | 자격증 목록 |
| GET | `/health` | 헬스 체크 |

### 3.3 데이터 모델

```
Resume
├── name, title, summary
├── contact: ContactInfo (email, phone, location, website, github, linkedin)
├── experience: list[Experience] (company, position, dates, highlights)
├── education: list[Education] (institution, degree, field, highlights)
├── skills: list[Skill] (category, items)
├── projects: list[Project] (name, description, tech_stack, highlights)
├── certifications: list[Certification] (name, issuer, date)
└── languages: list[str]
```

---

## 4. 커밋 이력

| 커밋 | 메시지 |
|------|--------|
| `dfab9af` | `feat: Resume API 엔드포인트 구축 (FastAPI)` |
| `2b8ba99` | `fix: 모듈 경로 문제 해결을 위한 서버 실행 스크립트 추가` |
| `2cafbaf` | `feat: 단독 실행 가능한 Resume API 서버 스크립트 추가` |

---

## 5. 발생한 이슈 및 해결

### 이슈 1: localhost 접속 불가 (`ERR_CONNECTION_REFUSED`)
- **원인:** 서버가 원격 작업 환경에서만 실행되고, 사용자 로컬 PC에서는 실행되지 않음
- **해결:** 사용자가 로컬에서 직접 서버를 실행해야 함

### 이슈 2: `ModuleNotFoundError: No module named 'src.resume'`
- **원인:** Windows 환경에서 `python -m uvicorn src.resume.api:app` 실행 시 Python 모듈 경로를 찾지 못함
- **해결 1:** `run_server.py` — `sys.path`에 프로젝트 루트를 추가하는 실행 스크립트 생성
- **해결 2:** `resume_server.py` — 모듈 import 없이 모든 코드를 단일 파일에 포함한 독립 실행 스크립트 생성

### 이슈 3: `git pull` 실패 (`couldn't find remote ref`)
- **원인:** 원격 작업 환경의 git 서버와 사용자의 GitHub 원격 저장소가 다름
- **상태:** 사용자가 로컬에서 직접 파일을 생성해야 함

---

## 6. 실행 방법

### 의존성 설치
```bash
pip install fastapi uvicorn pyyaml
```

### 서버 실행 (권장: 단독 실행 스크립트)
```bash
cd BG_AIPro
python resume_server.py
```

### 서버 실행 (대안: 모듈 방식)
```bash
python run_server.py
```

### 접속
- API: `http://localhost:8000/api/resume`
- Swagger 문서: `http://localhost:8000/docs`

---

## 7. 남은 작업

- [ ] 사용자 로컬 환경에서 `resume_server.py` 실행 확인
- [ ] `data/resume.yaml`을 실제 이력서 데이터로 수정
- [ ] (선택) 외부 접속을 위한 클라우드 배포 (Railway, Render 등)
- [ ] (선택) CORS 설정 추가 (프론트엔드 연동 시)
- [ ] (선택) 이력서 PDF 다운로드 엔드포인트 추가
