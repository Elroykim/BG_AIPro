"""로컬 LLM 프로바이더 (Ollama 등)."""

from __future__ import annotations

import json

import httpx

from .base import AIProvider


class LocalLLMProvider(AIProvider):
    """Ollama 호환 로컬 LLM 프로바이더."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(self, prompt: str, system: str = "") -> str:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system or "You are a professional blog writer.",
                    "stream": False,
                },
            )
            resp.raise_for_status()
            return resp.json()["response"]

    async def generate_structured(self, prompt: str, system: str = "", schema: dict | None = None) -> dict:
        system_msg = system or "You are a professional blog writer."
        system_msg += "\n\nRespond ONLY with valid JSON. No markdown, no explanation."

        text = await self.generate(prompt, system=system_msg)
        return json.loads(text)
