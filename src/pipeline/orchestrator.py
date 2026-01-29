"""파이프라인 오케스트레이터 - 전체 흐름을 조율한다."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from src.ai.base import AIProvider
from src.config import TopicConfig
from src.models import BlogPost, ContentStatus, Platform, PublishResult
from src.publishers.base import Publisher

from .planner import generate_outline, research_keywords
from .reviewer import apply_improvements, auto_review
from .writer import write_post


@dataclass
class PipelineConfig:
    """파이프라인 실행 설정."""

    auto_approve: bool = True           # True면 검토 통과 시 자동 발행
    min_review_score: int = 70          # 자동 승인 최소 점수
    max_improvement_rounds: int = 2     # 최대 개선 반복 횟수


@dataclass
class PipelineResult:
    """파이프라인 실행 결과."""

    post: BlogPost
    review_score: int = 0
    publish_results: list[PublishResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class Orchestrator:
    def __init__(
        self,
        ai: AIProvider,
        publishers: dict[str, Publisher],
        config: PipelineConfig | None = None,
    ):
        self.ai = ai
        self.publishers = publishers
        self.config = config or PipelineConfig()

    async def run(self, topic: TopicConfig, keyword: str) -> PipelineResult:
        """단일 키워드에 대해 전체 파이프라인을 실행한다."""
        errors: list[str] = []

        # 1. 기획: 아웃라인 생성
        outline = await generate_outline(self.ai, topic, keyword)

        # 2. 작성: 본문 생성
        post = await write_post(self.ai, outline)

        # 3. 검토: 품질 검수 + 자동 개선
        review = await auto_review(self.ai, post)
        review_score = review.score

        for _ in range(self.config.max_improvement_rounds):
            if review.approved:
                break
            post = await apply_improvements(self.ai, post, review.improvements)
            review = await auto_review(self.ai, post)
            review_score = review.score

        if not review.approved:
            post.status = ContentStatus.REVIEW
            return PipelineResult(post=post, review_score=review_score, errors=["품질 기준 미달"])

        # 4. 발행
        post.status = ContentStatus.APPROVED
        publish_results: list[PublishResult] = []

        if self.config.auto_approve:
            for platform_name in topic.platforms:
                publisher = self.publishers.get(platform_name)
                if not publisher:
                    errors.append(f"퍼블리셔 없음: {platform_name}")
                    continue
                result = await publisher.publish(post)
                publish_results.append(result)
                if result.success:
                    post.platforms_published[platform_name] = result.url
                else:
                    errors.append(f"{platform_name} 발행 실패: {result.error}")

            post.status = ContentStatus.PUBLISHED if any(r.success for r in publish_results) else ContentStatus.FAILED

        return PipelineResult(
            post=post,
            review_score=review_score,
            publish_results=publish_results,
            errors=errors,
        )

    async def run_batch(self, topic: TopicConfig, keywords: list[str]) -> list[PipelineResult]:
        """여러 키워드에 대해 순차적으로 파이프라인을 실행한다."""
        results = []
        for kw in keywords:
            result = await self.run(topic, kw)
            results.append(result)
        return results
