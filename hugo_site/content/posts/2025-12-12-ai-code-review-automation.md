---
title: "AI 코드 리뷰 자동화: PR 올릴 때마다 AI가 리뷰해주는 세팅법"
date: 2025-12-12
description: "CodeRabbit, GitHub Copilot 코드 리뷰, Sourcery로 PR에 AI 코드 리뷰를 자동화하는 방법. GitHub Actions 연동, 설정 예시, 장단점 비교까지 실전 가이드."
categories: [개발]
tags: [AI 코드 리뷰, GitHub, CodeRabbit, PR 자동화, 코드 품질]
keywords: [AI 코드 리뷰 자동화, CodeRabbit 사용법, GitHub Copilot 코드 리뷰, PR 자동 리뷰, 코드 리뷰 봇]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: ai-code-review-automation-github-pr
---

코드 리뷰가 밀리는 건 모든 개발팀의 공통 고민이다. PR을 올려놓으면 리뷰어가 바빠서 2~3일씩 대기하고, 리뷰어도 여러 PR을 동시에 봐야 해서 꼼꼼히 못 보는 경우가 많다. 그래서 요즘은 AI가 1차 리뷰를 하고, 사람은 비즈니스 로직이나 설계 판단에 집중하는 방식이 점점 보편화되고 있다. 직접 팀 프로젝트에 적용해봤는데, 단순 실수(오타, 미사용 변수, 타입 불일치)를 AI가 잡아주니까 사람 리뷰어가 더 중요한 부분에 시간을 쓸 수 있게 됐다.

---

## 1. AI 코드 리뷰 도구 개요

요즘 쓸 만한 AI 코드 리뷰 도구는 크게 세 가지다.

### CodeRabbit

AI 코드 리뷰 전문 서비스로, GitHub/GitLab/Azure DevOps와 연동해서 PR이 올라올 때마다 자동으로 리뷰 코멘트를 달아준다. GPT-4o와 Claude Sonnet을 기반으로 동작하며, 단순 린트 수준이 아니라 로직 분석, 보안 취약점, 성능 이슈까지 짚어준다.

- 지원 플랫폼: GitHub, GitLab, Azure DevOps, Bitbucket
- AI 모델: GPT-4o, Claude Sonnet 4 (자동 선택)
- 주요 기능: 라인별 코멘트, PR 요약, 시퀀스 다이어그램 생성, 대화형 리뷰

### GitHub Copilot Code Review

GitHub가 자체적으로 제공하는 AI 코드 리뷰 기능이다. Copilot 구독에 포함되어 있어서 별도 설치 없이 쓸 수 있다. PR의 "Reviewers"에서 Copilot을 리뷰어로 추가하면 된다.

- 지원 플랫폼: GitHub (당연히)
- 통합 수준: GitHub 네이티브
- 주요 기능: 코드 리뷰 코멘트, 수정 제안(Suggested changes), 보안 취약점 감지

Copilot의 다른 기능이 궁금하다면 [GitHub Copilot 활용 팁]({{< relref "posts/2025-12-13-github-copilot-tips.md" >}})도 참고하자.

### Sourcery

Python/JavaScript/TypeScript 코드에 특화된 AI 코드 리뷰 도구다. 리팩토링 제안에 강점이 있고, 코드 품질 점수를 매겨준다.

- 지원 플랫폼: GitHub, GitLab
- 특화 언어: Python, JavaScript, TypeScript
- 주요 기능: 리팩토링 제안, 코드 품질 점수, 복잡도 분석, 자동 수정 커밋

---

## 2. CodeRabbit 세팅하기

### 설치

CodeRabbit은 GitHub App으로 설치한다. 5분이면 끝난다.

```
1. https://coderabbit.ai 접속
2. "Start for Free" 클릭
3. GitHub 계정으로 로그인
4. 리뷰할 저장소 선택 (전체 또는 특정 저장소)
5. 권한 승인
6. 끝. 다음 PR부터 자동 리뷰 시작
```

### 설정 파일 (.coderabbit.yaml)

저장소 루트에 `.coderabbit.yaml` 파일을 만들면 세부 설정을 커스터마이징할 수 있다.

```yaml
# .coderabbit.yaml
language: "ko"  # 리뷰 코멘트를 한국어로

reviews:
  # PR 요약 자동 생성
  auto_summary: true

  # 리뷰 프로필 설정
  profile: "assertive"  # chill, assertive, nitpicky 중 선택

  # 리뷰에서 무시할 파일 패턴
  path_filters:
    - "!**/*.lock"
    - "!**/node_modules/**"
    - "!**/*.min.js"
    - "!**/dist/**"
    - "!**/*.generated.*"

  # 리뷰 범위 설정
  scope:
    - bugs          # 버그 감지
    - security      # 보안 취약점
    - performance   # 성능 이슈
    - style         # 코드 스타일
    - documentation # 문서화 부족

  # 자동 리뷰 활성화
  auto_review:
    enabled: true
    # PR이 draft일 때는 리뷰 안 함
    drafts: false
    # 특정 라벨이 있는 PR만 리뷰
    # labels:
    #   - "needs-review"

chat:
  # PR 코멘트에서 CodeRabbit에게 대화 가능
  auto_reply: true
```

### 리뷰 언어를 한국어로 설정

`language: "ko"`를 설정하면 코드 리뷰 코멘트가 한국어로 나온다. 한국 개발팀이라면 한국어 리뷰가 훨씬 직관적이다.

```yaml
# 한국어 리뷰 예시 코멘트:
#
# 🐛 버그: `user_id`가 None일 때 NullPointerException이
# 발생할 수 있습니다. None 체크를 추가하는 것을 권장합니다.
#
# 🔒 보안: 사용자 입력을 SQL 쿼리에 직접 삽입하고 있습니다.
# SQL Injection 취약점이 있으므로 파라미터 바인딩을 사용하세요.
```

### 고급 설정: 커스텀 리뷰 지침

팀의 코딩 컨벤션에 맞게 리뷰 지침을 추가할 수 있다.

```yaml
reviews:
  instructions: |
    - 함수 길이가 50줄을 넘으면 분리를 제안할 것
    - 에러 처리가 없는 API 호출은 반드시 지적할 것
    - TypeScript에서 any 타입 사용은 경고할 것
    - 환경변수를 하드코딩하면 반드시 지적할 것
    - 테스트 코드가 없는 비즈니스 로직 변경은 지적할 것
```

---

## 3. GitHub Copilot Code Review 세팅하기

### 사전 조건

- GitHub Copilot 구독 (Individual $10/월 또는 Business $19/월/인)
- 조직 설정에서 Copilot Code Review 활성화

### 사용 방법

Copilot 코드 리뷰는 별도 설치가 필요 없다. PR을 만든 후 리뷰어 추가 방식으로 사용한다.

```
방법 1: 수동으로 리뷰 요청
1. PR 페이지에서 "Reviewers" 섹션 클릭
2. "Copilot" 선택
3. Copilot이 자동으로 리뷰 시작

방법 2: 자동 리뷰 설정 (Rulesets 활용)
1. 저장소 Settings → Rules → Rulesets
2. 새 규칙 생성
3. "Request pull request review from Copilot" 활성화
4. 적용 브랜치 설정 (예: main, develop)
```

### GitHub Actions로 자동 리뷰 요청

PR이 올라올 때마다 자동으로 Copilot 리뷰를 요청하는 워크플로우를 만들 수 있다.

```yaml
# .github/workflows/copilot-review.yml
name: Request Copilot Review

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  pull-requests: write

jobs:
  request-review:
    runs-on: ubuntu-latest
    steps:
      - name: Request Copilot Review
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            // PR이 draft가 아닐 때만 리뷰 요청
            const pr = context.payload.pull_request;
            if (!pr.draft) {
              await github.rest.pulls.requestReviewers({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: pr.number,
                reviewers: ['copilot-pull-request-reviewer']
              });
              console.log(`Copilot review requested for PR #${pr.number}`);
            }
```

### Copilot 리뷰 커스터마이징

저장소에 코딩 가이드라인 파일을 만들면 Copilot이 참고한다.

```markdown
<!-- .github/copilot-review-instructions.md -->
# 코드 리뷰 가이드라인

## 필수 확인 항목
- 모든 API 엔드포인트에 에러 핸들링이 있는지
- 환경변수가 하드코딩되어 있지 않은지
- TypeScript의 strict mode 위반이 없는지
- SQL 쿼리에 파라미터 바인딩을 사용하는지

## 코딩 컨벤션
- 변수명은 camelCase
- 함수명은 동사로 시작
- 매직 넘버 사용 금지 (상수로 정의)
```

---

## 4. Sourcery 세팅하기

### 설치

```
1. https://sourcery.ai 접속
2. GitHub 계정으로 로그인
3. GitHub App 설치 → 저장소 선택
4. 다음 PR부터 자동 리뷰 시작
```

### 설정 파일 (.sourcery.yaml)

```yaml
# .sourcery.yaml
refactor:
  # 리팩토링 제안 활성화
  enabled: true

  # 최소 품질 점수 (이 점수 이하면 리팩토링 제안)
  min_quality: 25

review:
  # AI 리뷰 코멘트 활성화
  enabled: true

  # 리뷰할 파일 패턴
  include:
    - "src/**/*.py"
    - "src/**/*.ts"
    - "src/**/*.js"

  # 리뷰 제외 파일
  exclude:
    - "**/*_test.py"
    - "**/test_*.py"
    - "**/*.spec.ts"

  # PR 요약 자동 생성
  auto_summary: true

  # 코드 품질 점수 표시
  quality_score: true

rules:
  # 커스텀 규칙
  - id: no-print-statements
    description: "print() 대신 logger를 사용하세요"
    pattern: "print(${args})"
    replacement: "logger.info(${args})"
    language: python
```

### Sourcery의 코드 품질 점수

Sourcery는 PR의 변경사항에 대해 4가지 축으로 품질 점수를 매긴다.

```
코드 품질 = (복잡도 + 가독성 + 스타일 + 테스트 커버리지) / 4

각 축 점수 범위: 0 ~ 100

예시 리뷰 코멘트:
┌─────────────────────────────────────┐
│  Code Quality Score: 72/100         │
│                                     │
│  Complexity:  ████████░░  78        │
│  Readability: ███████░░░  68        │
│  Style:       █████████░  85        │
│  Tests:       █████░░░░░  56        │
│                                     │
│  Suggestions: 3 improvements found  │
└─────────────────────────────────────┘
```

---

## 5. 세 도구 비교

### 기능 비교

| 기능 | CodeRabbit | Copilot Review | Sourcery |
|------|-----------|---------------|----------|
| 라인별 코멘트 | ★★★★★ | ★★★★ | ★★★★ |
| PR 요약 | ★★★★★ | ★★★ | ★★★★ |
| 버그 감지 | ★★★★★ | ★★★★ | ★★★ |
| 보안 분석 | ★★★★ | ★★★★ | ★★ |
| 리팩토링 제안 | ★★★ | ★★★ | ★★★★★ |
| 코드 품질 점수 | ★★★ | ★★ | ★★★★★ |
| 대화형 리뷰 | ★★★★★ | ★★★ | ★★ |
| 한국어 리뷰 | ★★★★★ | ★★★ | ★★ |
| 설정 유연성 | ★★★★★ | ★★★ | ★★★★ |
| 다이어그램 생성 | ★★★★ | ★ | ★ |

### 지원 플랫폼 비교

| 플랫폼 | CodeRabbit | Copilot Review | Sourcery |
|--------|-----------|---------------|----------|
| GitHub | O | O | O |
| GitLab | O | X | O |
| Bitbucket | O | X | X |
| Azure DevOps | O | X | X |

### 가격 비교

| 플랜 | CodeRabbit | Copilot Review | Sourcery |
|------|-----------|---------------|----------|
| 무료 | 오픈소스 무료 | X (Copilot 구독 필요) | 오픈소스 무료 |
| 개인 | $12/월 | $10/월 (Copilot 포함) | $14/월 |
| 팀 | $24/월/인 | $19/월/인 (Copilot Business) | 별도 문의 |

이미 Copilot을 쓰고 있다면 Copilot Review가 추가 비용 없이 가장 편하다. 전문적인 AI 리뷰가 필요하면 CodeRabbit이 가장 강력하고, Python 위주 프로젝트에서 리팩토링에 집중하고 싶으면 Sourcery가 적합하다.

---

## 6. 실전 적용: GitHub Actions 통합 워크플로우

세 도구를 조합해서 쓸 수도 있다. 아래는 PR이 올라오면 CodeRabbit + 기존 CI를 함께 돌리는 워크플로우 예시다.

```yaml
# .github/workflows/pr-review-pipeline.yml
name: PR Review Pipeline

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  # 1단계: 기본 코드 검사 (lint, type check)
  lint-and-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: ESLint
        run: npm run lint

      - name: Type Check
        run: npm run typecheck

  # 2단계: 테스트 실행
  test:
    runs-on: ubuntu-latest
    needs: lint-and-typecheck
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Run Tests
        run: npm test -- --coverage

      - name: Upload Coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  # 3단계: 보안 스캔
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  # CodeRabbit은 별도 워크플로우 필요 없음
  # GitHub App으로 설치하면 PR에 자동으로 리뷰 코멘트를 달아줌
  # .coderabbit.yaml 설정만 있으면 됨
```

### 리뷰 프로세스 플로우

```
PR 생성
  │
  ├── GitHub Actions 자동 실행
  │   ├── Lint + Type Check → 통과/실패
  │   ├── 테스트 → 통과/실패 + 커버리지 리포트
  │   └── 보안 스캔 → 취약점 리포트
  │
  ├── AI 코드 리뷰 자동 실행 (동시에)
  │   ├── CodeRabbit → 라인별 코멘트, PR 요약
  │   └── (옵션) Copilot → 추가 코멘트
  │
  ├── 개발자가 AI 리뷰 코멘트 확인
  │   ├── 동의 → 코드 수정 후 재푸시
  │   └── 반박 → 코멘트에 답글 (CodeRabbit과 대화)
  │
  └── 사람 리뷰어 확인
      ├── AI가 놓친 설계/비즈니스 로직 검토
      └── 최종 Approve
```

---

## 7. AI 코드 리뷰 활용 팁

### 팁 1: AI 리뷰와 사람 리뷰의 역할 분리

AI 리뷰를 도입한다고 사람 리뷰가 필요 없어지는 건 아니다. 역할을 명확히 분리하는 게 핵심이다.

```
AI 리뷰가 잘하는 것:
  ├── 문법/스타일 오류 (미사용 변수, 오타, 일관성)
  ├── 보안 취약점 (SQL Injection, XSS, 하드코딩된 시크릿)
  ├── 성능 이슈 (불필요한 루프, N+1 쿼리)
  ├── 에러 핸들링 누락
  └── 타입 불일치, null 체크 누락

사람 리뷰가 잘하는 것:
  ├── 비즈니스 로직 정합성 ("이 할인 로직이 기획 의도와 맞나?")
  ├── 아키텍처 적합성 ("이 로직이 여기 있는 게 맞나?")
  ├── 네이밍 적절성 ("이 변수명이 맥락에 맞나?")
  ├── 확장성 판단 ("나중에 요구사항 바뀌면 어떻게 되지?")
  └── 팀 컨벤션 준수 여부
```

### 팁 2: 노이즈 줄이기

AI 리뷰가 너무 많은 코멘트를 달면 오히려 리뷰를 안 보게 된다. 노이즈를 줄이는 설정이 중요하다.

```yaml
# CodeRabbit: 프로필을 chill로 설정하면 중요한 이슈만 코멘트
reviews:
  profile: "chill"

# 자동 생성 파일, 락 파일, 번들 파일 제외
  path_filters:
    - "!**/*.lock"
    - "!**/package-lock.json"
    - "!**/yarn.lock"
    - "!**/dist/**"
    - "!**/build/**"
    - "!**/*.min.*"
    - "!**/*.generated.*"
    - "!**/migrations/**"
```

### 팁 3: 대화형 리뷰 활용

CodeRabbit의 강점 중 하나는 리뷰 코멘트에 답글을 달면 AI가 응답한다는 것이다.

```
CodeRabbit: "이 함수의 시간 복잡도가 O(n²)입니다. 데이터가
커지면 성능 문제가 될 수 있습니다."

개발자: "@coderabbitai 이 데이터는 최대 100건이라
성능 이슈가 없습니다."

CodeRabbit: "이해했습니다. 데이터 크기가 제한적이라면 현재
구현이 적합합니다. 다만 향후 데이터 증가 가능성이 있다면
인덱스나 캐싱을 고려해보시는 것을 추천드립니다."
```

### 팁 4: PR 템플릿에 AI 리뷰 가이드 포함

```markdown
<!-- .github/pull_request_template.md -->
## 변경 사항
<!-- 어떤 변경을 했는지 설명 -->

## AI 리뷰 참고사항
<!-- AI 리뷰어에게 알려줄 맥락 (선택) -->
<!-- 예: "이 PR은 성능 개선이 목적이므로 가독성보다 성능 관점에서 리뷰 바람" -->

## 테스트
- [ ] 기존 테스트 통과 확인
- [ ] 새로운 테스트 추가 (필요시)
```

---

## 8. 주의사항과 한계

### AI 코드 리뷰가 놓칠 수 있는 것

- 비즈니스 요구사항과의 정합성 (AI는 기획서를 모른다)
- 시스템 전체 맥락 (해당 PR만 보기 때문에 다른 모듈과의 관계를 놓칠 수 있다)
- 팀 내부의 암묵적 컨벤션 (문서화되지 않은 규칙)
- 정치적/조직적 맥락 ("이건 PM이 이렇게 해달라고 해서...")

### 보안 고려사항

AI 코드 리뷰 도구에 코드를 보내는 건 외부 서비스에 코드를 노출하는 것이다.

```
보안 체크리스트:
□ 코드에 시크릿(API 키, 비밀번호)이 포함되어 있지 않은지 확인
□ AI 리뷰 서비스의 데이터 처리 정책 확인
□ SOC 2, GDPR 등 필요한 보안 인증 여부 확인
□ 엔터프라이즈 플랜에서 데이터 보존 기간 확인
□ 필요시 on-premise 옵션 검토 (CodeRabbit Enterprise)
```

### false positive 처리

AI가 잘못된 지적을 하는 경우 무시하거나 피드백을 주면 된다.

```
대처 방법:
1. 코멘트에 이유를 달아서 dismiss
2. .coderabbit.yaml에서 특정 패턴 제외
3. 코드에 // coderabbit:ignore 주석 추가
4. 반복되는 false positive는 커스텀 지침으로 해결
```

---

## 9. 도입 전략: 어떤 순서로 적용할까

한 번에 다 도입하기보다 단계적으로 접근하는 게 좋다.

```
1단계 (1주차): GitHub Copilot Code Review
  └── 이미 Copilot을 쓰고 있다면 추가 비용 없이 시작 가능
  └── 리뷰어에 Copilot 추가하는 것만으로 즉시 사용

2단계 (2~3주차): CodeRabbit 무료 체험
  └── 오픈소스 저장소라면 무료
  └── .coderabbit.yaml로 팀 컨벤션에 맞게 설정
  └── 한국어 리뷰 설정

3단계 (4주차~): 피드백 반영 및 최적화
  └── 노이즈가 많은 규칙 제거
  └── 팀에서 유용했던/불필요했던 코멘트 유형 정리
  └── 커스텀 리뷰 지침 추가

4단계: 파이프라인 통합
  └── CI/CD와 AI 리뷰를 하나의 파이프라인으로 통합
  └── 리뷰 통과 조건 설정 (예: 보안 이슈 0건이면 자동 머지)
```

---

## 한 줄로 정리하면

AI 코드 리뷰는 사람 리뷰를 대체하는 게 아니라, 사람이 더 가치 있는 리뷰에 집중할 수 있게 해주는 도구다. 이미 Copilot을 쓰고 있다면 리뷰어 추가 한 번으로 시작할 수 있고, 제대로 된 AI 리뷰를 원한다면 CodeRabbit의 한국어 리뷰 + 대화형 리뷰가 현재 가장 강력하다. 설정에 30분 투자하면 PR 리뷰 대기 시간이 확 줄어드니까, 안 해봤으면 이번 기회에 붙여보자.
