"""Hugo 퍼블리셔 로컬 통합 테스트.

실행: python scripts/test_hugo_publish.py
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import BlogPost
from src.publishers.hugo import HugoPublisher

HUGO_SITE_PATH = Path(__file__).resolve().parent.parent / "hugo_site"


def create_sample_post() -> BlogPost:
    """테스트용 샘플 블로그 포스트를 생성한다."""
    return BlogPost(
        title="2026년 개인 블로그 시작하기: 플랫폼 선택부터 첫 글 발행까지",
        slug="2026-start-personal-blog",
        topic="tech",
        content_markdown="""## 왜 2026년에도 블로그인가?

소셜 미디어가 넘쳐나는 시대에 블로그는 여전히 강력한 도구입니다. 짧은 콘텐츠의 홍수 속에서, 깊이 있는 글은 오히려 차별화된 가치를 제공합니다.

### 블로그의 장점

- **소유권**: 플랫폼에 종속되지 않는 내 콘텐츠
- **SEO 자산**: 검색 엔진을 통한 지속적인 유입
- **전문성 구축**: 특정 분야의 전문가로 포지셔닝
- **수익화 가능성**: 애드센스, 제휴 마케팅, 디지털 제품

## 플랫폼 선택 가이드

### 무료로 시작하기: Hugo + GitHub Pages

기술적 역량이 있다면 가장 추천하는 조합입니다.

```bash
# Hugo 설치 (macOS)
brew install hugo

# 새 사이트 생성
hugo new site my-blog
cd my-blog

# 테마 설치
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke themes/ananke

# 첫 글 작성
hugo new posts/my-first-post.md

# 로컬 서버 실행
hugo server -D
```

**장점**: 무료, 빠른 빌드, Git 버전 관리, 자동 배포
**단점**: 초기 설정에 기술적 지식 필요

### 편의성 중심: WordPress.com

글쓰기에만 집중하고 싶다면 WordPress.com 호스팅형을 선택하세요.

- 무료 플랜으로 시작 가능
- 드래그 앤 드롭 에디터
- 수천 개의 테마와 플러그인

### 한국 시장 공략: 네이버 블로그

한국 검색 트래픽의 과반을 네이버가 차지합니다. 한국어 콘텐츠로 국내 독자를 타겟팅한다면 네이버 블로그는 필수입니다.

## 첫 글 작성 팁

### 주제 선정

1. **자신이 잘 아는 분야**에서 시작
2. **검색 수요**가 있는 키워드 선택
3. **구체적인 문제 해결**에 초점

### 글 구조

좋은 블로그 글의 기본 구조:

1. **도입**: 독자의 문제/관심사를 명시
2. **본문**: 해결책을 단계별로 제시
3. **결론**: 핵심 요약 + 행동 유도

### SEO 기본기

- 제목에 메인 키워드 포함
- 메타 디스크립션 160자 이내로 작성
- H2, H3 태그로 구조화
- 이미지에 alt 텍스트 추가

## 마치며

완벽한 첫 글을 쓰려고 하지 마세요. 가장 중요한 것은 **시작하는 것**입니다. 글을 쓰면서 자연스럽게 실력이 향상되고, 독자의 피드백을 통해 방향을 잡아갈 수 있습니다.

오늘 바로 블로그를 개설하고 첫 글을 발행해보세요.""",
        meta_description="2026년 블로그 시작 가이드. Hugo, WordPress, 네이버 블로그 중 최적의 플랫폼을 선택하고 첫 글을 발행하는 방법을 알려드립니다.",
        keywords=["블로그 시작하기", "Hugo 블로그", "개인 블로그", "블로그 플랫폼"],
        tags=["블로그", "Hugo", "SEO", "콘텐츠"],
        categories=["기술"],
        created_at=datetime(2026, 1, 29),
    )


async def main():
    print("=" * 60)
    print("Hugo 퍼블리셔 로컬 통합 테스트")
    print("=" * 60)

    # 1. 퍼블리셔 초기화
    publisher = HugoPublisher(repo_path=str(HUGO_SITE_PATH))
    print(f"\n[1] Hugo 사이트 경로: {HUGO_SITE_PATH}")
    print(f"    콘텐츠 디렉토리: {publisher.content_dir}")

    # 2. 샘플 포스트 생성
    post = create_sample_post()
    print(f"\n[2] 샘플 포스트 생성 완료")
    print(f"    제목: {post.title}")
    print(f"    슬러그: {post.slug}")
    print(f"    키워드: {', '.join(post.keywords)}")

    # 3. Hugo에 로컬 발행 (git push 없이)
    print(f"\n[3] Hugo 로컬 발행 중...")
    result = await publisher.publish_local(post)

    print(f"\n[4] 발행 결과:")
    print(f"    성공: {result.success}")
    print(f"    URL: {result.url}")
    print(f"    Post ID: {result.post_id}")
    if result.error:
        print(f"    오류: {result.error}")

    # 4. 빌드 결과 확인
    public_dir = HUGO_SITE_PATH / "public"
    if public_dir.exists():
        html_files = list(public_dir.rglob("*.html"))
        print(f"\n[5] 빌드 결과:")
        print(f"    생성된 HTML 파일 수: {len(html_files)}")
        for f in sorted(html_files)[:10]:
            print(f"    - {f.relative_to(public_dir)}")
        if len(html_files) > 10:
            print(f"    ... 외 {len(html_files) - 10}개")
    else:
        print("\n[5] public/ 디렉토리 없음 (빌드 실패)")

    # 5. 생성된 마크다운 파일 확인
    md_files = list(publisher.content_dir.glob("*.md"))
    print(f"\n[6] 콘텐츠 파일:")
    for f in md_files:
        print(f"    - {f.name} ({f.stat().st_size} bytes)")

    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
