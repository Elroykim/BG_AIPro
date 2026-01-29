"""네이버 블로그 크로스포스팅 퍼블리셔."""

from __future__ import annotations

import httpx
import markdown

from src.models import BlogPost, Platform, PublishResult

from .base import Publisher


class NaverPublisher(Publisher):
    """네이버 블로그 API (생성 전용, 수정/삭제 미지원)."""

    WRITE_API = "https://openapi.naver.com/blog/writePost.json"

    def __init__(self, client_id: str, client_secret: str, blog_id: str, access_token: str = ""):
        self.blog_id = blog_id
        self.access_token = access_token
        self.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }
        if access_token:
            self.headers["Authorization"] = f"Bearer {access_token}"

    async def publish(self, post: BlogPost) -> PublishResult:
        html = markdown.markdown(post.content_markdown, extensions=["extra"])
        # 원본 출처 링크 추가
        if post.platforms_published.get("wordpress"):
            html += f'\n<p>원본: <a href="{post.platforms_published["wordpress"]}">원문 보기</a></p>'

        payload = {
            "title": post.title,
            "contents": html,
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    self.WRITE_API,
                    data=payload,
                    headers=self.headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return PublishResult(
                    platform=Platform.NAVER,
                    success=True,
                    url=data.get("url", f"https://blog.naver.com/{self.blog_id}"),
                    post_id=str(data.get("postId", "")),
                )
        except Exception as e:
            return PublishResult(
                platform=Platform.NAVER,
                success=False,
                error=str(e),
            )

    async def update(self, post_id: str, post: BlogPost) -> PublishResult:
        """네이버는 수정 API가 없어 재발행으로 대체."""
        return PublishResult(
            platform=Platform.NAVER,
            success=False,
            error="네이버 블로그는 API를 통한 수정을 지원하지 않습니다.",
        )

    async def delete(self, post_id: str) -> bool:
        """네이버는 삭제 API를 지원하지 않음."""
        return False
