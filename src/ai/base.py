"""AI 프로바이더 공통 인터페이스."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """모든 AI 프로바이더가 구현해야 하는 인터페이스."""

    @abstractmethod
    async def generate(self, prompt: str, system: str = "") -> str:
        """프롬프트를 받아 텍스트를 생성한다."""
        ...

    @abstractmethod
    async def generate_structured(self, prompt: str, system: str = "", schema: dict | None = None) -> dict:
        """구조화된 JSON 응답을 생성한다."""
        ...
