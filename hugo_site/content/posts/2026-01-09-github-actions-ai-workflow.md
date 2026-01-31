---
title: "GitHub Actions로 AI 자동화 파이프라인 만들기: PR 요약, 번역, 테스트"
date: 2026-01-09
description: "GitHub Actions에 AI를 연동하여 PR 자동 요약, 문서 자동 번역, AI 기반 테스트 생성 등의 자동화 파이프라인을 구축하는 방법을 실전 YAML 예제와 함께 설명합니다."
categories: [개발]
tags: [GitHub Actions, AI 자동화, CI/CD, PR 자동화, DevOps]
keywords: [GitHub Actions AI, PR 자동 요약, AI 번역 자동화, GitHub Actions 워크플로우, CI/CD AI 파이프라인]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: github-actions-ai-automation-workflow
---

PR을 올리면 리뷰어가 "이 PR이 뭘 하는 건지 요약 좀 써줘" 하고, 문서를 수정하면 "영어 버전도 업데이트해야 되는데" 하고. 이런 반복 작업이 쌓이다가 GitHub Actions에 AI를 붙여봤다. PR 올리면 자동으로 요약이 달리고, 한국어 문서를 수정하면 영어 번역이 자동으로 커밋되더라.

직접 세팅해보면서 알게 된 패턴과 워크플로우 YAML을 정리해봤다.

---

## 왜 GitHub Actions + AI인가

개발 워크플로우에서 AI가 잘 맞는 부분은 따로 있다. 코드를 짜는 것보다는, 코드에 대해 설명하거나 변환하는 작업에 AI가 강하다.

```
[AI가 잘하는 GitHub 작업]
├── PR 변경사항 요약 → 리뷰 시간 단축
├── 코드 리뷰 보조 → 잠재적 버그 탐지
├── 문서 번역 → 다국어 문서 유지
├── 커밋 메시지 정리 → 일관된 형식
├── 테스트 코드 제안 → 커버리지 향상
└── 릴리스 노트 자동 생성 → 변경 이력 정리
```

이런 작업들을 수동으로 하면 시간도 걸리고 빼먹기도 쉬운데, GitHub Actions에 연결해두면 자동으로 돌아간다.

### n8n과의 비교

| 항목 | GitHub Actions | n8n |
|------|---------------|-----|
| 트리거 | GitHub 이벤트 (PR, push 등) | HTTP, 스케줄, 다양한 서비스 |
| 환경 | GitHub 호스팅 러너 | 셀프호스팅 or 클라우드 |
| 코드 중심 | YAML + 스크립트 | 비주얼 워크플로우 |
| GitHub 통합 | 네이티브 | API 연동 필요 |
| 가격 | 퍼블릭 리포 무료, 프라이빗 월 2000분 | 셀프호스팅 무료 |
| 적합한 용도 | 개발 파이프라인 | 범용 업무 자동화 |

개발 관련 자동화는 GitHub Actions가 적합하고, 비개발 업무 자동화는 n8n이 적합하다. 두 가지를 조합해서 쓰는 것도 좋다.

---

## 사전 준비

### API 키를 GitHub Secrets에 등록

```
GitHub 리포지토리 > Settings > Secrets and variables > Actions
→ New repository secret

추가할 시크릿:
- OPENAI_API_KEY: sk-...
- ANTHROPIC_API_KEY: sk-ant-...
```

### 공통 스크립트 구조

```
.github/
├── workflows/
│   ├── pr-summary.yml
│   ├── auto-translate.yml
│   ├── ai-test-gen.yml
│   └── release-notes.yml
├── scripts/
│   ├── pr_summary.py
│   ├── translate.py
│   └── generate_tests.py
└── prompts/
    ├── pr_summary.txt
    └── code_review.txt
```

---

## 워크플로우 1: PR 자동 요약

PR을 열면 AI가 변경사항을 분석해서 요약 코멘트를 자동으로 달아준다.

### 워크플로우 YAML

```yaml
# .github/workflows/pr-summary.yml
name: AI PR Summary

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  pull-requests: write
  contents: read

jobs:
  summarize:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install anthropic PyGithub

      - name: Get PR diff
        id: diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > pr_diff.txt
          echo "diff_size=$(wc -c < pr_diff.txt)" >> $GITHUB_OUTPUT

      - name: Generate PR summary
        if: steps.diff.outputs.diff_size != '0'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO_NAME: ${{ github.repository }}
        run: python .github/scripts/pr_summary.py
```

### PR 요약 스크립트

```python
# .github/scripts/pr_summary.py
import os
import anthropic
from github import Github

def get_diff():
    with open("pr_diff.txt", "r") as f:
        diff = f.read()
    # 너무 길면 잘라내기 (토큰 절약)
    if len(diff) > 15000:
        diff = diff[:15000] + "\n\n... (diff truncated)"
    return diff

def generate_summary(diff: str) -> str:
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-haiku-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""다음 Git diff를 분석하여 PR 요약을 작성해주세요.

형식:
## 요약
(2-3문장으로 이 PR이 무엇을 하는지)

## 주요 변경사항
- (변경 1)
- (변경 2)
- ...

## 리뷰 포인트
- (리뷰어가 특히 살펴봐야 할 부분)

---

{diff}"""
        }]
    )

    return response.content[0].text

def post_comment(summary: str):
    gh = Github(os.environ["GITHUB_TOKEN"])
    repo = gh.get_repo(os.environ["REPO_NAME"])
    pr = repo.get_pull(int(os.environ["PR_NUMBER"]))

    comment_body = f"""🤖 **AI PR 요약** (자동 생성)

{summary}

---
*이 요약은 AI가 자동 생성했습니다. 참고용으로만 활용해주세요.*
"""

    # 기존 AI 코멘트가 있으면 업데이트
    for comment in pr.get_issue_comments():
        if "AI PR 요약" in comment.body:
            comment.edit(comment_body)
            print("기존 코멘트 업데이트")
            return

    pr.create_issue_comment(comment_body)
    print("새 코멘트 작성")

if __name__ == "__main__":
    diff = get_diff()
    summary = generate_summary(diff)
    post_comment(summary)
    print("PR 요약 완료")
```

써보니 Haiku 모델이면 PR 요약에 충분하고, 비용도 거의 안 든다. PR 하나당 0.001달러도 안 나온다.

---

## 워크플로우 2: 문서 자동 번역

한국어 문서(`docs/ko/`)를 수정하면 영어 버전(`docs/en/`)을 자동으로 번역해서 커밋하는 워크플로우다.

### 워크플로우 YAML

```yaml
# .github/workflows/auto-translate.yml
name: AI Document Translation

on:
  push:
    branches: [main]
    paths:
      - 'docs/ko/**'

permissions:
  contents: write
  pull-requests: write

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install anthropic

      - name: Get changed files
        id: changed
        run: |
          CHANGED=$(git diff --name-only HEAD~1 HEAD -- 'docs/ko/' | tr '\n' ',')
          echo "files=$CHANGED" >> $GITHUB_OUTPUT

      - name: Translate documents
        if: steps.changed.outputs.files != ''
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          CHANGED_FILES: ${{ steps.changed.outputs.files }}
        run: python .github/scripts/translate.py

      - name: Create PR with translations
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: "docs: auto-translate Korean docs to English"
          title: "[Auto] 문서 영어 번역 업데이트"
          body: |
            AI가 자동 번역한 문서입니다.
            번역 품질을 확인해주세요.

            변경된 한국어 문서: ${{ steps.changed.outputs.files }}
          branch: auto-translate
          base: main
```

### 번역 스크립트

```python
# .github/scripts/translate.py
import os
import anthropic

client = anthropic.Anthropic()

def translate_file(ko_path: str) -> str:
    """한국어 문서를 영어로 번역"""
    with open(ko_path, "r", encoding="utf-8") as f:
        content = f.read()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""다음 한국어 기술 문서를 영어로 번역해주세요.

규칙:
1. 마크다운 형식을 그대로 유지
2. 코드 블록 내용은 번역하지 않음 (주석만 번역)
3. 기술 용어는 영어 원문 유지
4. 자연스러운 영어로 (직역 X)
5. 제목과 링크 구조 유지

---

{content}"""
        }]
    )

    return response.content[0].text

def main():
    changed_files = os.environ.get("CHANGED_FILES", "").strip(",").split(",")

    for ko_file in changed_files:
        if not ko_file.strip():
            continue

        # docs/ko/guide.md → docs/en/guide.md
        en_file = ko_file.replace("docs/ko/", "docs/en/")

        # 디렉토리 생성
        os.makedirs(os.path.dirname(en_file), exist_ok=True)

        print(f"번역 중: {ko_file} → {en_file}")
        translated = translate_file(ko_file)

        with open(en_file, "w", encoding="utf-8") as f:
            f.write(translated)

        print(f"번역 완료: {en_file}")

if __name__ == "__main__":
    main()
```

번역 결과를 바로 main에 커밋하지 않고 PR로 만드는 게 포인트다. 사람이 확인하고 머지하는 단계를 두는 것이 안전하다.

---

## 워크플로우 3: AI 코드 리뷰

PR의 코드를 AI가 리뷰해서 잠재적 문제점을 코멘트로 달아준다.

### 워크플로우 YAML

```yaml
# .github/workflows/ai-code-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  pull-requests: write
  contents: read

jobs:
  review:
    runs-on: ubuntu-latest
    if: github.event.pull_request.draft == false
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install anthropic PyGithub

      - name: Run AI code review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO_NAME: ${{ github.repository }}
        run: python .github/scripts/code_review.py
```

### 코드 리뷰 스크립트

```python
# .github/scripts/code_review.py
import os
import subprocess
import anthropic
from github import Github

client = anthropic.Anthropic()

def get_changed_files():
    """변경된 파일 목록과 diff 가져오기"""
    result = subprocess.run(
        ["git", "diff", "--name-only", f"origin/{os.environ.get('GITHUB_BASE_REF', 'main')}...HEAD"],
        capture_output=True, text=True
    )
    files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]

    # 리뷰 대상 필터링 (코드 파일만)
    code_extensions = {'.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs'}
    return [f for f in files if any(f.endswith(ext) for ext in code_extensions)]

def get_file_diff(filepath: str) -> str:
    result = subprocess.run(
        ["git", "diff", f"origin/{os.environ.get('GITHUB_BASE_REF', 'main')}...HEAD", "--", filepath],
        capture_output=True, text=True
    )
    return result.stdout

def review_file(filepath: str, diff: str) -> str:
    response = client.messages.create(
        model="claude-haiku-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""다음 코드 변경사항을 리뷰해주세요.

파일: {filepath}

리뷰 관점:
1. 버그 가능성
2. 보안 취약점
3. 성능 문제
4. 가독성/유지보수성

중요한 이슈만 간결하게 지적해주세요. 문제가 없으면 "이슈 없음"이라고만 답해주세요.

```diff
{diff[:8000]}
```"""
        }]
    )
    return response.content[0].text

def main():
    files = get_changed_files()
    if not files:
        print("리뷰할 코드 파일 없음")
        return

    reviews = []
    for filepath in files[:10]:  # 최대 10개 파일
        diff = get_file_diff(filepath)
        if not diff:
            continue

        print(f"리뷰 중: {filepath}")
        review = review_file(filepath, diff)

        if "이슈 없음" not in review:
            reviews.append(f"### `{filepath}`\n\n{review}")

    if not reviews:
        print("리뷰 이슈 없음")
        return

    # PR에 코멘트 작성
    gh = Github(os.environ["GITHUB_TOKEN"])
    repo = gh.get_repo(os.environ["REPO_NAME"])
    pr = repo.get_pull(int(os.environ["PR_NUMBER"]))

    comment_body = f"""🔍 **AI 코드 리뷰**

{chr(10).join(reviews)}

---
*AI 자동 리뷰입니다. 참고용으로 활용해주세요.*
"""

    pr.create_issue_comment(comment_body)
    print(f"코드 리뷰 코멘트 작성 완료 ({len(reviews)}개 파일)")

if __name__ == "__main__":
    main()
```

---

## 워크플로우 4: 릴리스 노트 자동 생성

태그를 푸시하면 최근 커밋들을 분석해서 릴리스 노트를 자동으로 만든다.

### 워크플로우 YAML

```yaml
# .github/workflows/release-notes.yml
name: AI Release Notes

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install anthropic

      - name: Get commits since last tag
        id: commits
        run: |
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -z "$PREV_TAG" ]; then
            COMMITS=$(git log --oneline --no-merges)
          else
            COMMITS=$(git log --oneline --no-merges ${PREV_TAG}..HEAD)
          fi
          echo "$COMMITS" > commits.txt
          echo "count=$(wc -l < commits.txt)" >> $GITHUB_OUTPUT

      - name: Generate release notes
        if: steps.commits.outputs.count != '0'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python .github/scripts/release_notes.py

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body_path: release_notes.md
          generate_release_notes: false
```

### 릴리스 노트 스크립트

```python
# .github/scripts/release_notes.py
import anthropic

client = anthropic.Anthropic()

def generate_release_notes():
    with open("commits.txt", "r") as f:
        commits = f.read()

    response = client.messages.create(
        model="claude-haiku-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""다음 커밋 목록으로 릴리스 노트를 작성해주세요.

형식:
## 새로운 기능
- ...

## 개선사항
- ...

## 버그 수정
- ...

## 기타
- ...

카테고리에 해당하는 커밋이 없으면 그 섹션은 생략하세요.
각 항목은 사용자 관점에서 이해하기 쉽게 작성하세요.

커밋 목록:
{commits}"""
        }]
    )

    notes = response.content[0].text

    with open("release_notes.md", "w") as f:
        f.write(notes)

    print("릴리스 노트 생성 완료")

if __name__ == "__main__":
    generate_release_notes()
```

---

## 워크플로우 5: AI 테스트 코드 제안

새로운 코드가 push되면 AI가 해당 코드에 대한 테스트 코드를 제안한다.

```yaml
# .github/workflows/ai-test-suggestion.yml
name: AI Test Suggestion

on:
  pull_request:
    types: [opened]
    paths:
      - 'src/**/*.py'
      - '!src/**/*test*.py'

permissions:
  pull-requests: write
  contents: read

jobs:
  suggest-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install anthropic PyGithub

      - name: Generate test suggestions
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO_NAME: ${{ github.repository }}
        run: |
          python -c "
          import os, subprocess, anthropic
          from github import Github

          client = anthropic.Anthropic()

          result = subprocess.run(
              ['git', 'diff', '--name-only', '--diff-filter=AM',
               'origin/main...HEAD', '--', 'src/'],
              capture_output=True, text=True
          )
          new_files = [f for f in result.stdout.strip().split('\n')
                       if f.endswith('.py') and 'test' not in f]

          if not new_files:
              print('테스트 제안할 파일 없음')
              exit(0)

          suggestions = []
          for filepath in new_files[:5]:
              with open(filepath, 'r') as f:
                  code = f.read()

              response = client.messages.create(
                  model='claude-haiku-4-20250514',
                  max_tokens=2048,
                  messages=[{
                      'role': 'user',
                      'content': f'''다음 Python 코드에 대한 pytest 테스트 코드를 작성해주세요.

          파일: {filepath}

          \`\`\`python
          {code[:6000]}
          \`\`\`

          요구사항:
          1. 핵심 함수별로 최소 2개 테스트
          2. 엣지 케이스 포함
          3. pytest 스타일
          4. 한국어 주석'''
                  }]
              )
              suggestions.append(f'### \`{filepath}\`\n\n{response.content[0].text}')

          if suggestions:
              gh = Github(os.environ['GITHUB_TOKEN'])
              repo = gh.get_repo(os.environ['REPO_NAME'])
              pr = repo.get_pull(int(os.environ['PR_NUMBER']))

              body = '🧪 **AI 테스트 코드 제안**\n\n'
              body += '\n\n---\n\n'.join(suggestions)
              body += '\n\n---\n*AI가 제안한 테스트 코드입니다. 필요에 맞게 수정해서 사용하세요.*'

              pr.create_issue_comment(body)
              print(f'테스트 제안 완료 ({len(suggestions)}개 파일)')
          "
```

---

## 비용 관리

AI API 호출 비용이 쌓일 수 있으니 관리가 필요하다.

### 비용 추정

| 워크플로우 | 모델 | PR당 비용 (대략) | 월 50 PR 기준 |
|-----------|------|----------------|--------------|
| PR 요약 | Haiku | $0.001 | $0.05 |
| 코드 리뷰 | Haiku | $0.005 | $0.25 |
| 문서 번역 | Sonnet | $0.01 | $0.50 |
| 릴리스 노트 | Haiku | $0.001 | 월 1~2회 |
| 테스트 제안 | Haiku | $0.003 | $0.15 |

전부 합쳐도 월 1달러 이하다. Haiku 모델을 기본으로 쓰면 비용이 거의 무시할 수 있는 수준이다.

### 비용 절감 팁

```yaml
# 1. diff 크기가 작을 때만 실행
- name: Check diff size
  id: check
  run: |
    SIZE=$(git diff --stat origin/main...HEAD | tail -1 | awk '{print $4}')
    echo "changes=$SIZE" >> $GITHUB_OUTPUT

- name: Run AI review
  if: steps.check.outputs.changes < 1000  # 변경 줄 수 제한

# 2. 특정 라벨이 있을 때만 실행
- name: AI Review
  if: contains(github.event.pull_request.labels.*.name, 'ai-review')

# 3. draft PR은 건너뛰기
- name: AI Summary
  if: github.event.pull_request.draft == false
```

---

## 실전 팁

### 프롬프트를 파일로 관리

프롬프트를 코드에 하드코딩하지 말고 파일로 분리하면 수정이 편하다.

```
.github/prompts/
├── pr_summary.txt
├── code_review.txt
├── translation.txt
└── test_suggestion.txt
```

```python
# 프롬프트 로드
def load_prompt(name: str) -> str:
    with open(f".github/prompts/{name}.txt", "r") as f:
        return f.read()

prompt = load_prompt("pr_summary")
```

### 워크플로우 디버깅

```yaml
# 디버그 모드
- name: Debug info
  if: runner.debug == '1'
  run: |
    echo "Changed files: ${{ steps.changed.outputs.files }}"
    echo "Diff size: $(wc -c < pr_diff.txt)"
    cat pr_diff.txt | head -50
```

### 동시 실행 제어

같은 PR에서 여러 번 push하면 워크플로우가 중복 실행될 수 있다. `concurrency`로 제어한다.

```yaml
concurrency:
  group: ai-review-${{ github.event.pull_request.number }}
  cancel-in-progress: true  # 이전 실행 취소
```

---

## Docker 환경에서 실행

복잡한 의존성이 필요한 스크립트는 Docker 컨테이너에서 실행하는 게 안정적이다. [Docker 가이드]({{< relref "posts/2026-01-14-docker-for-ai-developers.md" >}})에서 다뤘던 내용을 여기에도 적용할 수 있다.

```yaml
jobs:
  ai-review:
    runs-on: ubuntu-latest
    container:
      image: python:3.12-slim
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install anthropic PyGithub

      - name: Run review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python .github/scripts/code_review.py
```

---

## 보안 주의사항

### API 키 보호

- 절대 워크플로우 YAML에 API 키를 직접 넣지 않는다
- GitHub Secrets를 통해서만 전달한다
- fork된 리포에서는 시크릿이 전달되지 않으니 주의한다

```yaml
# fork에서 실행 방지
jobs:
  review:
    if: github.event.pull_request.head.repo.full_name == github.repository
```

### AI 생성 결과물 검증

- AI가 자동 커밋하는 워크플로우(번역 등)는 PR로 만들어서 사람이 확인하는 단계를 반드시 둬야 한다
- AI 코드 리뷰는 참고용이지, 사람 리뷰를 대체하는 게 아니다
- 자동 생성된 테스트는 반드시 수동 검증 후 적용해야 한다

---

## 되짚어보기

GitHub Actions에 AI를 붙이면 개발 워크플로우의 반복적인 부분을 많이 줄일 수 있다. 나는 PR 요약이 가장 효과가 좋았는데, 리뷰어가 PR 맥락을 빠르게 파악해서 리뷰 시간이 체감상 절반 정도로 줄었다.

핵심을 정리하면 이렇다.

1. PR 요약은 Haiku 모델로도 충분하고, 비용도 거의 제로
2. 문서 번역은 자동 커밋 대신 PR로 만들어서 사람이 확인
3. 코드 리뷰는 보조 수단이지 대체는 아님
4. 프롬프트는 파일로 분리해서 관리
5. concurrency 설정으로 중복 실행 방지

월 1달러도 안 되는 비용으로 개발 워크플로우 전체에 AI를 붙일 수 있으니, 쓰지 않을 이유가 없다. 가장 쉬운 PR 요약부터 시작해서 점차 확장해보는 걸 추천한다.
