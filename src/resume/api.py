"""Resume API 엔드포인트."""

from __future__ import annotations

from pathlib import Path

import yaml
from fastapi import FastAPI, HTTPException

from src.resume.models import Resume

app = FastAPI(
    title="BG_AIPro Resume API",
    description="이력서 데이터를 제공하는 REST API",
    version="1.0.0",
)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RESUME_PATH = DATA_DIR / "resume.yaml"


def _load_resume() -> Resume:
    """YAML 파일에서 이력서 데이터를 로드한다."""
    if not RESUME_PATH.exists():
        raise HTTPException(status_code=404, detail="이력서 데이터 파일이 없습니다.")
    with open(RESUME_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Resume(**data)


@app.get("/api/resume", response_model=Resume, summary="전체 이력서 조회")
async def get_resume():
    """전체 이력서 데이터를 반환한다."""
    return _load_resume()


@app.get("/api/resume/contact", summary="연락처 조회")
async def get_contact():
    """연락처 정보를 반환한다."""
    resume = _load_resume()
    return {"name": resume.name, "title": resume.title, "contact": resume.contact}


@app.get("/api/resume/experience", summary="경력 조회")
async def get_experience():
    """경력 사항 목록을 반환한다."""
    resume = _load_resume()
    return {"experience": resume.experience}


@app.get("/api/resume/education", summary="학력 조회")
async def get_education():
    """학력 사항 목록을 반환한다."""
    resume = _load_resume()
    return {"education": resume.education}


@app.get("/api/resume/skills", summary="기술 스택 조회")
async def get_skills():
    """기술 스택 목록을 반환한다."""
    resume = _load_resume()
    return {"skills": resume.skills}


@app.get("/api/resume/projects", summary="프로젝트 조회")
async def get_projects():
    """프로젝트 목록을 반환한다."""
    resume = _load_resume()
    return {"projects": resume.projects}


@app.get("/api/resume/certifications", summary="자격증 조회")
async def get_certifications():
    """자격증 및 인증 목록을 반환한다."""
    resume = _load_resume()
    return {"certifications": resume.certifications}


@app.get("/health", summary="헬스 체크")
async def health_check():
    """서버 상태를 확인한다."""
    return {"status": "ok"}
