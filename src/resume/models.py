"""이력서 데이터 모델."""

from __future__ import annotations

from pydantic import BaseModel


class ContactInfo(BaseModel):
    """연락처 정보."""

    email: str = ""
    phone: str = ""
    location: str = ""
    website: str = ""
    github: str = ""
    linkedin: str = ""


class Experience(BaseModel):
    """경력 사항."""

    company: str
    position: str
    start_date: str
    end_date: str = "현재"
    description: str = ""
    highlights: list[str] = []


class Education(BaseModel):
    """학력 사항."""

    institution: str
    degree: str
    field: str = ""
    start_date: str = ""
    end_date: str = ""
    gpa: str = ""
    highlights: list[str] = []


class Skill(BaseModel):
    """기술 스택."""

    category: str
    items: list[str] = []


class Project(BaseModel):
    """프로젝트."""

    name: str
    description: str = ""
    tech_stack: list[str] = []
    url: str = ""
    highlights: list[str] = []


class Certification(BaseModel):
    """자격증 및 인증."""

    name: str
    issuer: str = ""
    date: str = ""
    url: str = ""


class Resume(BaseModel):
    """전체 이력서."""

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
