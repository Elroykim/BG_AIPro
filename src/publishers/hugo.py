"""Hugo + GitHub Pages 퍼블리셔."""

from __future__ import annotations

import subprocess
from pathlib import Path

import frontmatter

from src.models import BlogPost, Platform, PublishResult

from .base import Publisher


class HugoPublisher(Publisher):
    def __init__(self, repo_path: str, branch: str = "main", hugo_bin: str = "hugo"):
        self.repo_path = Path(repo_path)
        self.content_dir = self.repo_path / "content" / "posts"
        self.branch = branch
        self.hugo_bin = hugo_bin

    def _build_frontmatter(self, post: BlogPost) -> dict:
        return {
            "title": post.title,
            "date": post.created_at.isoformat(),
            "draft": False,
            "slug": post.slug,
            "description": post.meta_description,
            "tags": post.tags,
            "categories": post.categories,
            "keywords": post.keywords,
        }

    def _write_post_file(self, post: BlogPost) -> Path:
        self.content_dir.mkdir(parents=True, exist_ok=True)
        date_prefix = post.created_at.strftime("%Y-%m-%d")
        file_path = self.content_dir / f"{date_prefix}-{post.slug}.md"
        fm = frontmatter.Post(post.content_markdown, **self._build_frontmatter(post))
        file_path.write_text(frontmatter.dumps(fm), encoding="utf-8")
        return file_path

    def build(self) -> subprocess.CompletedProcess:
        """Hugo 사이트를 빌드한다."""
        return subprocess.run(
            [self.hugo_bin, "--gc", "--minify"],
            cwd=self.repo_path,
            check=True,
            capture_output=True,
            text=True,
        )

    def _git_push(self, message: str) -> None:
        cmds = [
            ["git", "add", "."],
            ["git", "commit", "-m", message],
            ["git", "push", "origin", self.branch],
        ]
        for cmd in cmds:
            subprocess.run(cmd, cwd=self.repo_path, check=True, capture_output=True)

    async def publish(self, post: BlogPost) -> PublishResult:
        try:
            file_path = self._write_post_file(post)
            self.build()
            self._git_push(f"post: {post.title}")
            slug = post.slug
            return PublishResult(
                platform=Platform.HUGO,
                success=True,
                url=f"/posts/{file_path.stem}/",
                post_id=slug,
            )
        except Exception as e:
            return PublishResult(
                platform=Platform.HUGO,
                success=False,
                error=str(e),
            )

    async def publish_local(self, post: BlogPost) -> PublishResult:
        """git push 없이 로컬에 파일만 쓰고 빌드한다 (테스트용)."""
        try:
            file_path = self._write_post_file(post)
            result = self.build()
            return PublishResult(
                platform=Platform.HUGO,
                success=True,
                url=f"/posts/{file_path.stem}/",
                post_id=post.slug,
            )
        except Exception as e:
            return PublishResult(
                platform=Platform.HUGO,
                success=False,
                error=str(e),
            )

    async def update(self, post_id: str, post: BlogPost) -> PublishResult:
        try:
            self._write_post_file(post)
            self.build()
            self._git_push(f"update: {post.title}")
            return PublishResult(
                platform=Platform.HUGO,
                success=True,
                url=f"/{post.slug}/",
                post_id=post_id,
            )
        except Exception as e:
            return PublishResult(
                platform=Platform.HUGO,
                success=False,
                error=str(e),
            )

    async def delete(self, post_id: str) -> bool:
        try:
            file_path = self.content_dir / f"{post_id}.md"
            if file_path.exists():
                file_path.unlink()
                self.build()
                self._git_push(f"delete: {post_id}")
                return True
            return False
        except Exception:
            return False
