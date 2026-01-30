"""Resume API 단독 실행 서버.

사용법:
    pip install fastapi uvicorn pyyaml
    python resume_server.py
"""

import sys
from pathlib import Path
from typing import Optional

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ── 데이터 모델 ──────────────────────────────────────────────

class ContactInfo(BaseModel):
    email: str = ""
    phone: str = ""
    location: str = ""
    website: str = ""
    github: str = ""
    linkedin: str = ""


class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: str = "현재"
    description: str = ""
    highlights: list[str] = []


class Education(BaseModel):
    institution: str
    degree: str
    field: str = ""
    start_date: str = ""
    end_date: str = ""
    gpa: str = ""
    highlights: list[str] = []


class Skill(BaseModel):
    category: str
    items: list[str] = []


class Project(BaseModel):
    name: str
    description: str = ""
    tech_stack: list[str] = []
    url: str = ""
    highlights: list[str] = []


class Certification(BaseModel):
    name: str
    issuer: str = ""
    date: str = ""
    url: str = ""


class Resume(BaseModel):
    name: str
    title: str = ""
    summary: str = ""
    contact: ContactInfo = ContactInfo()
    experience: list[Experience] = []
    education: list[Education] = []
    skills: list[Skill] = []
    projects: list[Project] = []
    certifications: list[Certification] = []
    languages: list[str] = []


# ── YAML 로드 ────────────────────────────────────────────────

RESUME_PATH = Path(__file__).resolve().parent / "data" / "resume.yaml"


def _load_resume() -> Resume:
    if not RESUME_PATH.exists():
        raise HTTPException(status_code=404, detail="data/resume.yaml 파일이 없습니다.")
    with open(RESUME_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Resume(**data)


# ── FastAPI 앱 ────────────────────────────────────────────────

app = FastAPI(
    title="BG_AIPro Resume API",
    description="이력서 데이터를 제공하는 REST API",
    version="1.0.0",
)


@app.get("/api/resume", response_model=Resume, summary="전체 이력서 조회")
async def get_resume():
    return _load_resume()


@app.get("/api/resume/contact", summary="연락처 조회")
async def get_contact():
    r = _load_resume()
    return {"name": r.name, "title": r.title, "contact": r.contact}


@app.get("/api/resume/experience", summary="경력 조회")
async def get_experience():
    return {"experience": _load_resume().experience}


@app.get("/api/resume/education", summary="학력 조회")
async def get_education():
    return {"education": _load_resume().education}


@app.get("/api/resume/skills", summary="기술 스택 조회")
async def get_skills():
    return {"skills": _load_resume().skills}


@app.get("/api/resume/projects", summary="프로젝트 조회")
async def get_projects():
    return {"projects": _load_resume().projects}


@app.get("/api/resume/certifications", summary="자격증 조회")
async def get_certifications():
    return {"certifications": _load_resume().certifications}


@app.get("/health", summary="헬스 체크")
async def health_check():
    return {"status": "ok"}


# ── 메인 ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Resume API 서버: http://localhost:{port}")
    print(f"API 문서:        http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)
