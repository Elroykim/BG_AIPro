"""3단계: 품질 검토 - AI 기반 자동 검수 + 선택적 사람 승인."""

from __future__ import annotations

import json

from src.ai.base import AIProvider
from src.models import BlogPost, ContentStatus


class ReviewResult:
    def __init__(self, approved: bool, score: int, feedback: str, improvements: list[str]):
        self.approved = approved
        self.score = score
        self.feedback = feedback
        self.improvements = improvements


async def auto_review(ai: AIProvider, post: BlogPost) -> ReviewResult:
    """AI가 블로그 글의 품질을 자동 검토한다."""
    prompt = f"""다음 블로그 글의 품질을 검토해줘.

제목: {post.title}
키워드: {', '.join(post.keywords)}
메타 설명: {post.meta_description}

본문:
{post.content_markdown}

다음 기준으로 평가하고 JSON으로 응답해줘:
{{
  "score": 0-100,
  "approved": true/false (70점 이상이면 true),
  "feedback": "전체적인 평가 한 줄",
  "checks": {{
    "seo_keyword_usage": 0-10,
    "readability": 0-10,
    "structure": 0-10,
    "originality": 0-10,
    "completeness": 0-10
  }},
  "improvements": ["개선사항1", "개선사항2"]
}}"""

    data = await ai.generate_structured(prompt)
    return ReviewResult(
        approved=data.get("approved", False),
        score=data.get("score", 0),
        feedback=data.get("feedback", ""),
        improvements=data.get("improvements", []),
    )


async def apply_improvements(ai: AIProvider, post: BlogPost, improvements: list[str]) -> BlogPost:
    """검토 피드백을 반영하여 글을 개선한다."""
    prompt = f"""다음 블로그 글을 개선사항에 따라 수정해줘.

제목: {post.title}

현재 본문:
{post.content_markdown}

개선사항:
{chr(10).join(f'- {imp}' for imp in improvements)}

수정된 본문만 Markdown으로 출력해줘."""

    improved_content = await ai.generate(prompt)
    post.content_markdown = improved_content
    return post
