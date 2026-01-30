---
title: "Claude API 실전 가이드: Anthropic API로 AI 앱 만들기 (2026)"
date: 2026-01-30
description: "Claude API(Anthropic API)의 기본 사용법부터 Tool Use, 비전, 스트리밍, 프롬프트 캐싱까지. 실전 예제와 함께 정리합니다."
categories: [AI]
tags: [Claude API, Anthropic, LLM API, AI 개발, Python]
keywords: [Claude API 사용법, Anthropic API 가이드, Claude API Python, Claude Tool Use, Claude 비전 API]
draft: false
slug: claude-api-anthropic-guide-2026
---

Claude는 Anthropic이 만든 AI 모델로, GPT와 함께 가장 많이 사용되는 LLM입니다. 2026년 현재, Claude API는 텍스트 생성뿐 아니라 **비전, 도구 사용, 프롬프트 캐싱, 배치 처리** 등 강력한 기능을 제공합니다.

이 글에서는 Claude API의 모든 핵심 기능을 실전 코드와 함께 정리합니다.

---

## API 시작하기

### 설치 및 설정

```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### 첫 번째 API 호출

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Python에서 리스트 컴프리헨션을 설명해줘"}
    ],
)

print(message.content[0].text)
```

### 모델 선택 (2026)

| 모델 | 특징 | 용도 | 입력 비용 (1M 토큰) |
|------|------|------|---------------------|
| **Claude Opus 4** | 최고 성능 | 복잡한 분석, 코딩 | $15 |
| **Claude Sonnet 4** | 균형잡힌 성능 | 일반 업무, 코딩 | $3 |
| **Claude Haiku 3.5** | 빠르고 저렴 | 분류, 요약, 간단한 질문 | $0.80 |

---

## 시스템 프롬프트

시스템 프롬프트로 Claude의 행동을 제어합니다.

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="당신은 시니어 Python 개발자입니다. 코드 리뷰를 할 때 보안, 성능, 가독성 관점에서 피드백합니다. 한국어로 답변합니다.",
    messages=[
        {"role": "user", "content": "이 코드를 리뷰해줘:\nimport os\nos.system(f'rm -rf {user_input}')"},
    ],
)
```

---

## 멀티턴 대화

이전 대화를 `messages` 배열에 포함하면 맥락이 유지됩니다.

```python
messages = [
    {"role": "user", "content": "FastAPI란 뭐야?"},
    {"role": "assistant", "content": "FastAPI는 Python의 현대적인 웹 프레임워크입니다..."},
    {"role": "user", "content": "간단한 예제 코드를 보여줘"},
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages,
)
# Claude는 이전 대화를 기억하고 FastAPI 예제를 제공합니다
```

---

## 비전 (이미지 분석)

Claude는 이미지를 직접 분석할 수 있습니다.

```python
import base64

with open("screenshot.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data,
                },
            },
            {
                "type": "text",
                "text": "이 UI 스크린샷에서 개선할 점을 알려줘",
            },
        ],
    }],
)
```

### 비전 활용 사례

- UI/UX 리뷰 자동화
- 차트/그래프 데이터 추출
- OCR (문서 텍스트 인식)
- 다이어그램 분석 및 코드 생성

---

## Tool Use (도구 사용)

Claude가 외부 시스템과 상호작용할 수 있게 합니다.

```python
import json

tools = [
    {
        "name": "get_weather",
        "description": "특정 도시의 현재 날씨를 조회합니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "도시 이름 (예: 서울, 부산)",
                }
            },
            "required": ["city"],
        },
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "서울 날씨 어때?"}],
)

# Claude가 도구 호출을 결정하면
for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        # 실제 날씨 API 호출 후 결과를 다시 Claude에 전달
```

### Tool Use 패턴

1. **사용자 메시지** → Claude에 전달 (도구 정의 포함)
2. **Claude 판단** → 도구 호출이 필요한지 결정
3. **도구 실행** → 개발자가 실제 함수 실행
4. **결과 전달** → 도구 결과를 Claude에 다시 전달
5. **최종 응답** → Claude가 결과를 기반으로 자연어 응답 생성

---

## 스트리밍

실시간 응답 표시로 사용자 경험을 향상시킵니다.

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Python 비동기 프로그래밍을 설명해줘"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## 프롬프트 캐싱

동일한 시스템 프롬프트나 대량의 컨텍스트를 반복 사용할 때 비용을 90% 절감합니다.

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "당신은 한국 세법 전문가입니다. 다음 세법 문서를 기반으로 답변합니다...(대량 텍스트)",
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": "연말정산에서 공제받을 수 있는 항목은?"}],
)

# 첫 요청: 캐시 생성 (정상 비용)
# 이후 요청: 캐시 히트 시 입력 토큰 비용 90% 감소
```

---

## 배치 API

대량 처리 시 50% 비용 절감. 24시간 이내 결과 반환.

```python
# 배치 요청 생성
batch = client.batches.create(
    requests=[
        {
            "custom_id": "req-1",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "요약해줘: ..."}],
            },
        },
        # ... 수백~수천 개의 요청
    ]
)

# 결과 조회
result = client.batches.retrieve(batch.id)
```

---

## 에러 처리 및 베스트 프랙티스

```python
from anthropic import APIError, RateLimitError
import time

def call_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages,
            )
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except APIError as e:
            if e.status_code >= 500:
                time.sleep(2 ** attempt)
            else:
                raise
    raise Exception("최대 재시도 횟수 초과")
```

### 비용 관리 팁

1. **max_tokens 적절히 설정** — 필요한 만큼만
2. **Haiku 우선 사용** — 간단한 태스크에는 가장 저렴한 모델
3. **프롬프트 캐싱** — 반복 컨텍스트 시 필수
4. **배치 API** — 긴급하지 않은 대량 처리에 활용

---

## 마무리

Claude API는 단순한 텍스트 생성을 넘어, 비전, 도구 사용, 캐싱 등 실무에 필요한 모든 기능을 갖추고 있습니다. 시작은 간단한 `messages.create` 호출이지만, Tool Use와 프롬프트 캐싱을 조합하면 강력한 AI 애플리케이션을 만들 수 있습니다.
