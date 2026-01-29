"""2단계: 콘텐츠 생성 - 아웃라인 기반 본문 작성."""

from __future__ import annotations

from slugify import slugify

from src.ai.base import AIProvider
from src.models import BlogPost, ContentOutline


async def write_post(ai: AIProvider, outline: ContentOutline) -> BlogPost:
    """아웃라인을 기반으로 블로그 본문을 작성한다."""
    outline_text = ""
    for item in outline.outline:
        outline_text += f"\n## {item.heading}\n"
        for sub in item.subheadings:
            outline_text += f"### {sub}\n"
        if item.key_points:
            outline_text += f"핵심: {', '.join(item.key_points)}\n"

    prompt = f"""다음 아웃라인을 기반으로 블로그 글을 작성해줘.

제목: {outline.title}
키워드: {', '.join(outline.keywords)}
메타 설명: {outline.meta_description}

아웃라인:
{outline_text}

작성 규칙:
1. Markdown 형식으로 작성
2. 자연스럽고 읽기 쉬운 한국어
3. SEO를 고려하여 키워드를 자연스럽게 배치
4. 각 섹션은 충분한 내용을 담되 불필요한 반복 없이
5. 도입부에서 독자의 관심을 끌 것
6. 결론에서 핵심 내용을 요약하고 행동을 유도할 것
7. 본문만 출력 (제목 제외, 본문은 ## 부터 시작)"""

    content = await ai.generate(prompt)

    return BlogPost(
        title=outline.title,
        slug=slugify(outline.title, allow_unicode=True),
        topic=outline.topic,
        content_markdown=content,
        meta_description=outline.meta_description,
        keywords=outline.keywords,
        tags=outline.keywords[:5],
    )
