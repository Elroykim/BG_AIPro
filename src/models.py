"""콘텐츠 데이터 모델."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ContentStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    FAILED = "failed"


class Platform(str, Enum):
    WORDPRESS = "wordpress"
    HUGO = "hugo"
    NAVER = "naver"
    TISTORY = "tistory"


class OutlineItem(BaseModel):
    heading: str
    subheadings: list[str] = []
    key_points: list[str] = []


class ContentOutline(BaseModel):
    title: str
    slug: str = ""
    topic: str
    keywords: list[str] = []
    outline: list[OutlineItem] = []
    meta_description: str = ""


class BlogPost(BaseModel):
    id: str = Field(default_factory=lambda: "")
    title: str
    slug: str = ""
    topic: str
    content_markdown: str = ""
    content_html: str = ""
    meta_description: str = ""
    keywords: list[str] = []
    tags: list[str] = []
    categories: list[str] = []
    featured_image: str = ""
    status: ContentStatus = ContentStatus.DRAFT
    platforms_published: dict[str, str] = {}  # platform -> url
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    scheduled_at: datetime | None = None


class PublishResult(BaseModel):
    platform: Platform
    success: bool
    url: str = ""
    post_id: str = ""
    error: str = ""
