"""CLI 진입점."""

from __future__ import annotations

import asyncio
import sys

from rich.console import Console
from rich.table import Table

from src.ai.claude import ClaudeProvider
from src.config import list_topics, load_settings, load_topic
from src.pipeline.orchestrator import Orchestrator, PipelineConfig
from src.pipeline.planner import research_keywords
from src.publishers.hugo import HugoPublisher
from src.publishers.wordpress import WordPressPublisher

console = Console()


def build_publishers(settings) -> dict:
    """설정에서 사용 가능한 퍼블리셔를 생성한다."""
    publishers = {}
    if settings.wp_url and settings.wp_username:
        publishers["wordpress"] = WordPressPublisher(
            url=settings.wp_url,
            username=settings.wp_username,
            app_password=settings.wp_app_password,
        )
    if settings.hugo_repo_path:
        publishers["hugo"] = HugoPublisher(repo_path=settings.hugo_repo_path)
    return publishers


async def cmd_topics():
    """등록된 토픽 목록을 출력한다."""
    topics = list_topics()
    if not topics:
        console.print("[yellow]등록된 토픽이 없습니다. topics/ 디렉토리에 토픽을 추가하세요.[/yellow]")
        return
    table = Table(title="등록된 토픽")
    table.add_column("이름", style="cyan")
    table.add_column("표시명")
    table.add_column("플랫폼")
    table.add_column("빈도")
    for name in topics:
        tc = load_topic(name)
        table.add_row(name, tc.display_name, ", ".join(tc.platforms), tc.posting_frequency)
    console.print(table)


async def cmd_run(topic_name: str, keyword: str | None = None):
    """파이프라인을 실행한다."""
    settings = load_settings()
    if not settings.anthropic_api_key:
        console.print("[red]ANTHROPIC_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.[/red]")
        return

    ai = ClaudeProvider(api_key=settings.anthropic_api_key)
    publishers = build_publishers(settings)
    topic = load_topic(topic_name)

    console.print(f"[bold green]파이프라인 시작:[/bold green] {topic.display_name}")

    if not keyword:
        console.print("[cyan]키워드 리서치 중...[/cyan]")
        keywords = await research_keywords(ai, topic)
        console.print(f"추천 키워드: {keywords}")
        keyword = keywords[0] if keywords else topic.display_name

    orchestrator = Orchestrator(ai=ai, publishers=publishers)
    result = await orchestrator.run(topic, keyword)

    console.print(f"\n[bold]결과:[/bold]")
    console.print(f"  제목: {result.post.title}")
    console.print(f"  상태: {result.post.status.value}")
    console.print(f"  검토 점수: {result.review_score}")
    for pr in result.publish_results:
        status = "[green]성공[/green]" if pr.success else f"[red]실패: {pr.error}[/red]"
        console.print(f"  {pr.platform.value}: {status} {pr.url}")
    if result.errors:
        for err in result.errors:
            console.print(f"  [red]오류: {err}[/red]")


def cmd_serve(host: str = "0.0.0.0", port: int = 8000):
    """Resume API 서버를 시작한다."""
    import uvicorn

    console.print(f"[bold green]Resume API 서버 시작:[/bold green] http://{host}:{port}")
    console.print("[cyan]API 문서: http://{host}:{port}/docs[/cyan]")
    uvicorn.run("src.resume.api:app", host=host, port=port, reload=True)


def main():
    if len(sys.argv) < 2:
        console.print("[bold]BG_AIPro[/bold] - 블로그 자동화 시스템")
        console.print("\n사용법:")
        console.print("  bgai topics           등록된 토픽 목록")
        console.print("  bgai run <토픽>       파이프라인 실행")
        console.print("  bgai run <토픽> <키워드>  특정 키워드로 실행")
        console.print("  bgai serve            Resume API 서버 시작")
        console.print("  bgai serve <포트>     지정 포트로 서버 시작")
        return

    command = sys.argv[1]

    if command == "topics":
        asyncio.run(cmd_topics())
    elif command == "run":
        topic_name = sys.argv[2] if len(sys.argv) > 2 else None
        keyword = sys.argv[3] if len(sys.argv) > 3 else None
        if not topic_name:
            console.print("[red]토픽 이름을 지정하세요.[/red]")
            return
        asyncio.run(cmd_run(topic_name, keyword))
    elif command == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        cmd_serve(port=port)
    else:
        console.print(f"[red]알 수 없는 명령: {command}[/red]")


if __name__ == "__main__":
    main()
