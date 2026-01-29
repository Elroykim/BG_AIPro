"""SEO 리서치 모듈 — 주제별 블로그 토픽 도출 및 키워드 분석."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TopicIdea:
    """SEO 리서치로 도출된 블로그 토픽 아이디어."""

    rank: int
    title: str
    slug: str
    main_keyword: str
    long_tail_keywords: list[str]
    search_intent: str  # informational, commercial, transactional, navigational
    competition: str  # low, medium, high
    target_audience: str
    content_angle: str
    estimated_word_count: int = 2000
    priority: str = "normal"  # high, normal, low


@dataclass
class SEOResearchResult:
    """SEO 리서치 전체 결과."""

    topic_category: str
    research_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    ideas: list[TopicIdea] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "topic_category": self.topic_category,
            "research_date": self.research_date,
            "total_ideas": len(self.ideas),
            "ideas": [
                {
                    "rank": i.rank,
                    "title": i.title,
                    "slug": i.slug,
                    "main_keyword": i.main_keyword,
                    "long_tail_keywords": i.long_tail_keywords,
                    "search_intent": i.search_intent,
                    "competition": i.competition,
                    "target_audience": i.target_audience,
                    "content_angle": i.content_angle,
                    "estimated_word_count": i.estimated_word_count,
                    "priority": i.priority,
                }
                for i in self.ideas
            ],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
