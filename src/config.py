"""전역 설정 및 토픽별 설정 로딩."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """환경변수 기반 시크릿/글로벌 설정."""

    anthropic_api_key: str = ""

    # WordPress
    wp_url: str = ""
    wp_username: str = ""
    wp_app_password: str = ""

    # Hugo
    hugo_repo_path: str = ""
    github_token: str = ""

    # Naver
    naver_client_id: str = ""
    naver_client_secret: str = ""
    naver_blog_id: str = ""

    # Tistory
    tistory_access_token: str = ""
    tistory_blog_name: str = ""

    # Local LLM
    local_llm_url: str = "http://localhost:11434"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


class TopicConfig(BaseModel):
    """개별 주제(토픽) 설정."""

    name: str
    display_name: str = ""
    platforms: list[str] = ["wordpress", "hugo"]
    keywords_strategy: str = "long_tail"
    posting_frequency: str = "3/week"
    tone: str = "professional"
    language: str = "ko"
    categories: list[str] = []
    target_audience: str = ""


ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_DIR = ROOT_DIR / "topics"


def load_settings() -> Settings:
    return Settings()


def load_topic(topic_name: str) -> TopicConfig:
    config_path = TOPICS_DIR / topic_name / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"토픽 설정 없음: {config_path}")
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return TopicConfig(**data)


def list_topics() -> list[str]:
    if not TOPICS_DIR.exists():
        return []
    return [
        d.name for d in TOPICS_DIR.iterdir()
        if d.is_dir() and (d / "config.yaml").exists()
    ]
