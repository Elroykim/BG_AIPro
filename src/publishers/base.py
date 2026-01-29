"""퍼블리셔 공통 인터페이스."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import BlogPost, PublishResult


class Publisher(ABC):
    """모든 플랫폼 퍼블리셔가 구현해야 하는 인터페이스."""

    @abstractmethod
    async def publish(self, post: BlogPost) -> PublishResult:
        """블로그 글을 발행한다."""
        ...

    @abstractmethod
    async def update(self, post_id: str, post: BlogPost) -> PublishResult:
        """발행된 글을 수정한다."""
        ...

    @abstractmethod
    async def delete(self, post_id: str) -> bool:
        """발행된 글을 삭제한다."""
        ...
