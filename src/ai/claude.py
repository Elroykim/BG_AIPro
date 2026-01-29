"""Claude (Anthropic) AI 프로바이더."""

from __future__ import annotations

import json

import anthropic

from .base import AIProvider


class ClaudeProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model

    async def generate(self, prompt: str, system: str = "") -> str:
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system or "You are a professional blog writer.",
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    async def generate_structured(self, prompt: str, system: str = "", schema: dict | None = None) -> dict:
        system_msg = system or "You are a professional blog writer."
        system_msg += "\n\nRespond ONLY with valid JSON. No markdown, no explanation."

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_msg,
            messages=[{"role": "user", "content": prompt}],
        )
        return json.loads(message.content[0].text)
