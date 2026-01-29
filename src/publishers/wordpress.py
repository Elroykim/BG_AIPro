"""WordPress REST API 퍼블리셔."""

from __future__ import annotations

import base64

import httpx
import markdown

from src.models import BlogPost, Platform, PublishResult

from .base import Publisher


class WordPressPublisher(Publisher):
    def __init__(self, url: str, username: str, app_password: str):
        self.base_url = url.rstrip("/")
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        credentials = base64.b64encode(f"{username}:{app_password}".encode()).decode()
        self.headers = {"Authorization": f"Basic {credentials}"}

    async def publish(self, post: BlogPost) -> PublishResult:
        html = markdown.markdown(post.content_markdown, extensions=["extra", "codehilite"])
        payload = {
            "title": post.title,
            "slug": post.slug,
            "content": html,
            "status": "publish" if post.scheduled_at is None else "future",
            "excerpt": post.meta_description,
            "tags": [],  # 태그 ID 매핑 필요
        }
        if post.scheduled_at:
            payload["date"] = post.scheduled_at.isoformat()

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    f"{self.api_url}/posts",
                    json=payload,
                    headers=self.headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return PublishResult(
                    platform=Platform.WORDPRESS,
                    success=True,
                    url=data.get("link", ""),
                    post_id=str(data["id"]),
                )
        except Exception as e:
            return PublishResult(
                platform=Platform.WORDPRESS,
                success=False,
                error=str(e),
            )

    async def update(self, post_id: str, post: BlogPost) -> PublishResult:
        html = markdown.markdown(post.content_markdown, extensions=["extra", "codehilite"])
        payload = {
            "title": post.title,
            "content": html,
            "excerpt": post.meta_description,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    f"{self.api_url}/posts/{post_id}",
                    json=payload,
                    headers=self.headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return PublishResult(
                    platform=Platform.WORDPRESS,
                    success=True,
                    url=data.get("link", ""),
                    post_id=post_id,
                )
        except Exception as e:
            return PublishResult(
                platform=Platform.WORDPRESS,
                success=False,
                error=str(e),
            )

    async def delete(self, post_id: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.delete(
                    f"{self.api_url}/posts/{post_id}",
                    headers=self.headers,
                )
                return resp.status_code == 200
        except Exception:
            return False
