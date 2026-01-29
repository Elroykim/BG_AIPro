"""1단계: 콘텐츠 기획 - 키워드 리서치 및 아웃라인 생성."""

from __future__ import annotations

from src.ai.base import AIProvider
from src.config import TopicConfig
from src.models import ContentOutline, OutlineItem


async def research_keywords(ai: AIProvider, topic: TopicConfig) -> list[str]:
    """주제에 맞는 블로그 키워드를 리서치한다."""
    prompt = f"""다음 블로그 주제에 대해 SEO에 효과적인 롱테일 키워드 10개를 제안해줘.

주제: {topic.display_name}
카테고리: {', '.join(topic.categories)}
대상 독자: {topic.target_audience}
언어: {topic.language}

JSON 배열로 응답해줘. 예: ["키워드1", "키워드2", ...]"""

    result = await ai.generate_structured(prompt)
    return result if isinstance(result, list) else result.get("keywords", [])


async def generate_outline(ai: AIProvider, topic: TopicConfig, keyword: str) -> ContentOutline:
    """키워드 기반으로 블로그 글 아웃라인을 생성한다."""
    prompt = f"""다음 키워드로 블로그 글 아웃라인을 만들어줘.

키워드: {keyword}
주제 분야: {topic.display_name}
톤: {topic.tone}
언어: {topic.language}

다음 JSON 형식으로 응답해줘:
{{
  "title": "글 제목",
  "meta_description": "160자 이내 메타 설명",
  "keywords": ["메인키워드", "관련키워드1", "관련키워드2"],
  "outline": [
    {{
      "heading": "H2 제목",
      "subheadings": ["H3 소제목1", "H3 소제목2"],
      "key_points": ["핵심 포인트1", "핵심 포인트2"]
    }}
  ]
}}"""

    data = await ai.generate_structured(prompt)
    return ContentOutline(
        title=data["title"],
        topic=topic.name,
        keywords=data.get("keywords", [keyword]),
        meta_description=data.get("meta_description", ""),
        outline=[OutlineItem(**item) for item in data.get("outline", [])],
    )
