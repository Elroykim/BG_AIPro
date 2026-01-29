---
title: "AI 에이전트 직접 만들기: Python으로 시작하는 2026 실전 튜토리얼"
date: 2026-01-29
description: "AI 에이전트의 작동 원리를 이해하고, Python으로 직접 만들어보는 실전 튜토리얼. ReAct 패턴부터 도구 호출까지 단계별로 구현합니다."
categories: [AI]
tags: [AI 에이전트, Python, ReAct, Tool Use, LLM 개발]
keywords: [AI 에이전트 만들기, Python AI 에이전트, AI 에이전트 구축, 에이전트 AI 예제 코드, AI 에이전트 개발 입문]
draft: false
slug: build-ai-agent-python-tutorial-2026
---

"AI 에이전트"라는 말이 2026년 기술 업계에서 가장 많이 등장하는 키워드가 되었습니다. OpenAI, Anthropic, Google 모두 에이전트 시대를 선언했고, 실제로 코드를 작성하고 파일을 관리하며 웹을 검색하는 AI가 일상이 되었습니다. 그런데 AI 에이전트는 정확히 어떻게 작동하는 걸까요? 그리고 직접 만들 수 있을까요?

이 글에서는 AI 에이전트의 핵심 원리를 처음부터 설명하고, Python으로 실제 동작하는 리서치 에이전트를 단계별로 구현합니다. ReAct 패턴, 도구 호출 메커니즘, 메모리 관리까지 에이전트 개발의 모든 것을 다룹니다. 프로그래밍 기초가 있다면 누구나 따라할 수 있습니다.

---

## AI 에이전트란 무엇인가

### 정의: 자율적으로 판단하고 행동하는 AI 시스템

AI 에이전트(AI Agent)는 **주어진 목표를 달성하기 위해 스스로 판단하고, 도구를 사용하며, 반복적으로 행동하는 AI 시스템**입니다. 단순히 질문에 답하는 것이 아니라, 목표를 분석하고 필요한 단계를 계획한 다음 실제 행동을 수행합니다.

핵심은 세 가지 능력에 있습니다.

1. **추론(Reasoning)** -- 주어진 상황을 분석하고 다음에 무엇을 해야 하는지 판단합니다.
2. **행동(Acting)** -- 도구를 호출하거나 외부 시스템과 상호작용합니다.
3. **관찰(Observing)** -- 행동의 결과를 확인하고, 그 결과를 바탕으로 다음 판단을 내립니다.

일상적인 예를 들어보겠습니다. "다음 주 서울 날씨를 확인하고, 비가 오는 날을 찾아서 실내 데이트 코스를 추천해줘"라는 요청을 받으면, 에이전트는 다음과 같이 동작합니다.

```
[에이전트 사고 과정]

1단계(추론): "날씨 정보가 필요하다 → 날씨 API를 호출하자"
2단계(행동): 날씨 API 호출 → 서울 다음 주 예보 조회
3단계(관찰): "수요일과 금요일에 비 예보가 있다"
4단계(추론): "비 오는 날의 실내 코스를 찾아야 한다 → 검색해보자"
5단계(행동): 웹 검색 → "서울 실내 데이트 코스 추천"
6단계(관찰): 검색 결과에서 장소 목록 확보
7단계(추론): "충분한 정보를 얻었다 → 최종 답변을 구성하자"
8단계(행동): 사용자에게 정리된 추천 결과 전달
```

이 과정에서 에이전트는 사람의 개입 없이 스스로 "다음에 무엇을 해야 하는지"를 판단합니다. 바로 이 **자율성**이 에이전트의 핵심입니다.

### 에이전트의 3가지 구성 요소

AI 에이전트를 구축하려면 세 가지 요소가 필요합니다.

```
┌─────────────────────────────────────────────┐
│              AI 에이전트 구조                 │
│                                             │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │  두뇌    │  │  도구     │  │  메모리    │  │
│  │ (LLM)   │  │ (Tools)  │  │ (Memory)  │  │
│  │         │  │          │  │           │  │
│  │ 추론과   │  │ 검색, API │  │ 대화 기록  │  │
│  │ 판단 수행 │  │ DB 접근 등│  │ 상태 유지  │  │
│  └─────────┘  └──────────┘  └───────────┘  │
│       │             │             │         │
│       └─────────────┼─────────────┘         │
│                     │                       │
│            ┌────────┴────────┐              │
│            │   에이전트 루프   │              │
│            │ (추론→행동→관찰)  │              │
│            └─────────────────┘              │
└─────────────────────────────────────────────┘
```

- **두뇌(LLM)**: Claude, GPT 등 대규모 언어 모델이 판단의 핵심을 담당합니다.
- **도구(Tools)**: 웹 검색, 파일 읽기, API 호출 등 외부 세계와 상호작용하는 수단입니다.
- **메모리(Memory)**: 이전 대화, 행동 결과 등을 기억해서 일관된 판단을 내립니다.

---

## 에이전트 vs 챗봇: 무엇이 다른가

AI 에이전트와 챗봇은 겉보기에 비슷하지만 근본적으로 다른 시스템입니다. 아래 표로 핵심 차이를 비교합니다.

| 구분 | 일반 챗봇 | AI 에이전트 |
|------|----------|------------|
| **작동 방식** | 입력 → 출력 (1회) | 입력 → 추론 → 행동 → 관찰 (반복 루프) |
| **자율성** | 없음. 매번 사용자 입력 필요 | 높음. 스스로 다음 단계 결정 |
| **도구 사용** | 불가능 또는 제한적 | 다양한 외부 도구 호출 가능 |
| **상태 관리** | 단순 대화 히스토리 | 목표, 계획, 중간 결과 관리 |
| **에러 처리** | 사용자가 재요청 | 스스로 재시도 또는 대안 탐색 |
| **복잡한 작업** | 단일 턴 응답만 가능 | 다단계 작업을 순서대로 수행 |
| **대표 예시** | 고객 FAQ 봇 | Claude Code, Devin, AutoGPT |

한 문장으로 요약하면, **챗봇은 대화를 하고 에이전트는 일을 합니다**. 챗봇에게 "서울에서 부산까지 KTX 예매해줘"라고 하면 예매 방법을 알려주지만, 에이전트에게 같은 요청을 하면 실제로 예매 사이트에 접속해서 좌석을 선택하고 결제를 시도합니다.

---

## ReAct 패턴: 에이전트의 사고 방식

### ReAct란

현재 대부분의 AI 에이전트가 사용하는 핵심 패턴이 **ReAct**(Reasoning + Acting)입니다. 2022년 프린스턴 대학교와 Google이 공동으로 발표한 논문에서 제안된 이 패턴은, LLM이 **추론과 행동을 번갈아 수행**하도록 합니다.

이름에서 알 수 있듯이 ReAct는 두 가지를 결합합니다.

- **Re**(Reasoning): 현재 상황을 분석하고 다음 행동을 계획
- **Act**(Acting): 실제로 도구를 호출하거나 행동을 수행

여기에 행동 결과를 확인하는 **Observe** 단계가 추가되어 하나의 완전한 루프를 형성합니다.

### ReAct 루프의 동작 흐름

```
              ┌──────────────┐
              │   사용자 요청  │
              └──────┬───────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Reason (추론)         │
        │   "무엇을 해야 하는가?"  │
        │   - 상황 분석            │
        │   - 다음 행동 계획       │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Act (행동)            │
        │   "실행하자"            │
        │   - 도구 호출            │
        │   - API 요청            │
        │   - 데이터 조회          │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Observe (관찰)        │
        │   "결과가 어떤가?"       │
        │   - 도구 실행 결과 확인   │
        │   - 목표 달성 여부 판단   │
        └────────────┬───────────┘
                     │
              ┌──────┴──────┐
              │             │
         목표 미달성     목표 달성
              │             │
              ▼             ▼
        Reason으로     ┌──────────┐
        돌아감         │ 최종 응답  │
                      └──────────┘
```

### 구체적 예시: "2026년 한국 AI 시장 규모를 조사해줘"

```
[Reason 1]
"2026년 한국 AI 시장 규모에 대한 최신 데이터가 필요하다.
웹 검색으로 관련 보고서나 기사를 찾아보자."

[Act 1]
도구: web_search("2026년 한국 AI 시장 규모 보고서")

[Observe 1]
검색 결과: "IDC 보고서에 따르면 2026년 한국 AI 시장은..."
→ 일부 데이터 확보, 하지만 정부 공식 수치도 필요

[Reason 2]
"IDC 수치는 확보했으나, 과학기술정보통신부의 공식 발표도
확인하면 더 신뢰성 있는 답변이 가능하다."

[Act 2]
도구: web_search("과학기술정보통신부 2026 AI 산업 현황")

[Observe 2]
검색 결과: "과기정통부 발표에 따르면..."
→ 공식 수치 확보 완료

[Reason 3]
"두 출처의 데이터를 모두 확보했다. 이제 정리해서 답변하자."

[Act 3]
최종 답변 생성: 수치, 출처, 분석을 포함한 종합 답변
```

ReAct의 핵심은 LLM이 **"왜 이 행동을 하는지" 스스로 설명**한다는 점입니다. 단순히 도구를 호출하는 것이 아니라, 추론 과정을 명시적으로 거치기 때문에 결과의 정확성과 설명력이 높아집니다.

---

## 도구(Tool) 정의와 호출 메커니즘

### 도구란 무엇인가

AI 에이전트에서 **도구(Tool)**는 LLM이 외부 세계와 상호작용할 수 있게 해주는 함수입니다. LLM은 자체적으로 인터넷을 검색하거나 파일을 읽을 수 없습니다. 도구가 그 다리 역할을 합니다.

도구는 보통 다음 세 가지 요소로 정의됩니다.

1. **이름(name)**: 도구를 식별하는 고유한 이름 (예: `web_search`)
2. **설명(description)**: 이 도구가 무엇을 하는지에 대한 자연어 설명. LLM이 이 설명을 읽고 언제 사용할지 판단합니다.
3. **입력 스키마(input_schema)**: 도구에 전달해야 하는 매개변수 정의. JSON Schema 형식을 주로 사용합니다.

### 도구 호출의 전체 흐름

Claude API의 tool_use 기능을 기준으로 도구 호출이 어떻게 이루어지는지 살펴보겠습니다.

```
┌─────────┐         ┌──────────┐         ┌──────────┐
│  개발자   │         │  Claude  │         │  도구     │
│ (코드)   │         │  (LLM)   │         │ (함수)    │
└────┬────┘         └────┬─────┘         └────┬─────┘
     │                   │                    │
     │  1. 메시지 + 도구  │                    │
     │   목록 전송        │                    │
     │──────────────────>│                    │
     │                   │                    │
     │  2. tool_use 응답  │                    │
     │   (도구명 + 인자)  │                    │
     │<──────────────────│                    │
     │                   │                    │
     │  3. 도구 실행                           │
     │────────────────────────────────────────>│
     │                                        │
     │  4. 실행 결과 반환                       │
     │<────────────────────────────────────────│
     │                   │                    │
     │  5. tool_result   │                    │
     │   메시지로 전송    │                    │
     │──────────────────>│                    │
     │                   │                    │
     │  6. 최종 응답      │                    │
     │   (또는 추가 도구  │                    │
     │    호출 요청)      │                    │
     │<──────────────────│                    │
     │                   │                    │
```

핵심 포인트는 **LLM이 직접 도구를 실행하지 않는다**는 것입니다. LLM은 "이 도구를 이 인자로 호출해달라"는 요청을 보내고, 개발자의 코드가 실제 실행을 담당합니다. 이 구조가 안전성과 유연성을 보장합니다.

### Anthropic Claude의 도구 정의 형식

Claude API에서 도구는 다음과 같이 정의합니다.

```python
tools = [
    {
        "name": "web_search",
        "description": "주어진 검색어로 웹을 검색하여 관련 결과를 반환합니다. 최신 정보가 필요할 때 사용하세요.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색할 내용"
                }
            },
            "required": ["query"]
        }
    }
]
```

`description`이 특히 중요합니다. LLM은 이 설명을 읽고 **언제 이 도구를 사용할지** 판단하기 때문입니다. 설명이 모호하면 LLM이 적절한 시점에 도구를 호출하지 못할 수 있습니다.

---

## 실전 구현: Python으로 리서치 에이전트 만들기

이제 이론을 코드로 옮깁니다. Anthropic Claude API의 tool_use 기능과 httpx를 사용하여, 웹 검색을 수행하는 리서치 에이전트를 Python으로 구현하겠습니다.

### 환경 준비

먼저 필요한 패키지를 설치합니다.

```bash
pip install anthropic httpx
```

Anthropic API 키가 필요합니다. [Anthropic 콘솔](https://console.anthropic.com/)에서 발급받아 환경 변수로 설정하세요.

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 1단계: 도구 정의

에이전트가 사용할 도구를 정의합니다. 여기서는 두 가지 도구를 만듭니다.

```python
import httpx
import json

# --- 도구 실행 함수 ---

def web_search(query: str) -> str:
    """DuckDuckGo Instant Answer API를 사용한 간단한 웹 검색"""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1,
    }
    try:
        response = httpx.get(url, params=params, timeout=10.0)
        data = response.json()

        results = []
        # Abstract (요약 정보)
        if data.get("AbstractText"):
            results.append(f"요약: {data['AbstractText']}")
            results.append(f"출처: {data.get('AbstractSource', 'N/A')}")

        # Related Topics (관련 항목)
        for topic in data.get("RelatedTopics", [])[:5]:
            if "Text" in topic:
                results.append(f"- {topic['Text']}")

        if results:
            return "\n".join(results)
        return f"'{query}'에 대한 직접적인 검색 결과가 없습니다. 다른 검색어를 시도해보세요."

    except Exception as e:
        return f"검색 중 오류 발생: {str(e)}"


def calculate(expression: str) -> str:
    """수학 계산을 수행합니다."""
    try:
        # 안전한 수학 연산만 허용
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names, {})
        return f"계산 결과: {expression} = {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"
```

### 2단계: Claude API용 도구 스키마 정의

Claude API에 전달할 도구 목록을 정의합니다. 이 스키마를 보고 LLM이 어떤 도구를 언제 사용할지 결정합니다.

```python
# --- Claude API용 도구 스키마 ---

TOOLS = [
    {
        "name": "web_search",
        "description": (
            "웹에서 정보를 검색합니다. "
            "최신 뉴스, 사실 확인, 특정 주제에 대한 정보가 "
            "필요할 때 사용하세요."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색할 내용 (한국어 또는 영어)",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "calculate",
        "description": (
            "수학 계산을 수행합니다. "
            "숫자 연산, 비율 계산, 단위 변환 등이 "
            "필요할 때 사용하세요."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "계산할 수학 표현식 (예: '100 * 1.15')",
                }
            },
            "required": ["expression"],
        },
    },
]
```

### 3단계: 도구 실행 핸들러

LLM이 도구 호출을 요청하면 실제로 실행할 디스패처 함수를 만듭니다.

```python
# --- 도구 실행 디스패처 ---

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """도구 이름에 따라 적절한 함수를 실행합니다."""
    if tool_name == "web_search":
        return web_search(tool_input["query"])
    elif tool_name == "calculate":
        return calculate(tool_input["expression"])
    else:
        return f"알 수 없는 도구: {tool_name}"
```

### 4단계: 에이전트 루프 구현

이 부분이 에이전트의 핵심입니다. ReAct 패턴에 따라 "추론 → 행동 → 관찰"을 반복하는 루프를 구현합니다.

```python
import anthropic

# --- 에이전트 루프 ---

def run_agent(user_query: str, max_iterations: int = 10) -> str:
    """
    리서치 에이전트를 실행합니다.

    Args:
        user_query: 사용자의 질문 또는 요청
        max_iterations: 최대 반복 횟수 (무한 루프 방지)

    Returns:
        에이전트의 최종 답변
    """
    client = anthropic.Anthropic()

    # 시스템 프롬프트: 에이전트의 역할과 행동 규칙 정의
    system_prompt = """당신은 리서치 에이전트입니다. 사용자의 질문에 답하기 위해
도구를 활용하여 정보를 수집하고 분석합니다.

규칙:
1. 답을 모를 때는 반드시 도구를 사용하여 정보를 검색하세요.
2. 여러 출처의 정보를 종합하여 정확한 답변을 제공하세요.
3. 검색 결과가 불충분하면 다른 검색어로 재시도하세요.
4. 충분한 정보를 수집했다면 종합적인 답변을 작성하세요.
5. 수치 계산이 필요하면 calculate 도구를 사용하세요."""

    # 대화 히스토리 초기화
    messages = [
        {"role": "user", "content": user_query}
    ]

    print(f"\n{'='*60}")
    print(f"질문: {user_query}")
    print(f"{'='*60}")

    for i in range(max_iterations):
        print(f"\n--- 반복 {i + 1} ---")

        # Claude API 호출
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            tools=TOOLS,
            messages=messages,
        )

        # 응답에서 텍스트와 도구 호출 분리
        assistant_content = response.content
        messages.append({"role": "assistant", "content": assistant_content})

        # stop_reason 확인
        if response.stop_reason == "end_turn":
            # 도구 호출 없이 최종 답변 생성 완료
            final_text = ""
            for block in assistant_content:
                if hasattr(block, "text"):
                    final_text += block.text
            print(f"\n[최종 답변 생성 완료]")
            return final_text

        elif response.stop_reason == "tool_use":
            # 도구 호출 처리
            tool_results = []
            for block in assistant_content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id

                    print(f"  도구 호출: {tool_name}({json.dumps(tool_input, ensure_ascii=False)})")

                    # 도구 실행
                    result = execute_tool(tool_name, tool_input)
                    print(f"  결과: {result[:200]}...")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result,
                    })

            # 도구 실행 결과를 대화에 추가
            messages.append({"role": "user", "content": tool_results})

    return "최대 반복 횟수에 도달했습니다. 더 구체적인 질문을 시도해주세요."
```

### 5단계: 실행

이제 에이전트를 실행합니다.

```python
# --- 메인 실행 ---

if __name__ == "__main__":
    # 예시 질문
    result = run_agent(
        "Python과 Rust의 성능 차이를 비교하고, "
        "각 언어가 적합한 사용 사례를 알려줘."
    )

    print(f"\n{'='*60}")
    print("최종 답변:")
    print(f"{'='*60}")
    print(result)
```

### 전체 코드 통합

위의 모든 코드를 하나의 파일(`research_agent.py`)로 합치면 바로 실행 가능한 에이전트가 됩니다. 전체 코드를 한 번에 보겠습니다.

```python
"""
research_agent.py
Python으로 만드는 리서치 에이전트 - 전체 실행 가능 코드
"""

import json
import httpx
import anthropic


# ============================================================
# 1. 도구 함수 정의
# ============================================================

def web_search(query: str) -> str:
    """DuckDuckGo Instant Answer API를 사용한 간단한 웹 검색"""
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
    try:
        resp = httpx.get(url, params=params, timeout=10.0)
        data = resp.json()
        results = []
        if data.get("AbstractText"):
            results.append(f"요약: {data['AbstractText']}")
            results.append(f"출처: {data.get('AbstractSource', 'N/A')}")
        for topic in data.get("RelatedTopics", [])[:5]:
            if "Text" in topic:
                results.append(f"- {topic['Text']}")
        return "\n".join(results) if results else f"'{query}' 관련 결과 없음"
    except Exception as e:
        return f"검색 오류: {e}"


def calculate(expression: str) -> str:
    """안전한 수학 계산"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"계산 오류: {e}"


# ============================================================
# 2. Claude API용 도구 스키마
# ============================================================

TOOLS = [
    {
        "name": "web_search",
        "description": "웹 검색으로 최신 정보를 조회합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색어"
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "calculate",
        "description": "수학 계산을 수행합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "수학 표현식"
                }
            },
            "required": ["expression"],
        },
    },
]


# ============================================================
# 3. 도구 디스패처
# ============================================================

def execute_tool(name: str, inputs: dict) -> str:
    dispatch = {
        "web_search": lambda: web_search(inputs["query"]),
        "calculate": lambda: calculate(inputs["expression"]),
    }
    return dispatch.get(name, lambda: f"알 수 없는 도구: {name}")()


# ============================================================
# 4. 에이전트 루프
# ============================================================

def run_agent(query: str, max_turns: int = 10) -> str:
    client = anthropic.Anthropic()
    system = (
        "당신은 리서치 에이전트입니다. 도구를 사용해 정보를 수집하고 "
        "종합적인 답변을 작성하세요. 충분한 정보가 모이면 최종 답변을 "
        "생성하세요."
    )
    messages = [{"role": "user", "content": query}]

    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({
            "role": "assistant",
            "content": response.content,
        })

        # 최종 답변이면 반환
        if response.stop_reason == "end_turn":
            return "".join(
                b.text for b in response.content if hasattr(b, "text")
            )

        # 도구 호출 처리
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    print(f"[도구] {block.name}: {result[:100]}...")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})

    return "최대 반복 횟수 초과"


# ============================================================
# 5. 실행
# ============================================================

if __name__ == "__main__":
    answer = run_agent("AI 에이전트의 2026년 최신 동향을 조사해줘")
    print(answer)
```

실행 결과는 대략 다음과 같은 흐름을 보입니다.

```
[도구] web_search: 요약: An intelligent agent is an agent acting...
[도구] web_search: 요약: AI agents in 2026 are increasingly...
[도구] web_search: - Multi-agent systems are becoming standard...

(최종 답변이 출력됨)
```

에이전트가 스스로 여러 번 검색을 수행하고, 충분한 정보가 모이면 종합 답변을 생성합니다.

---

## 코드 핵심 분석: 왜 이렇게 동작하는가

위 코드에서 가장 중요한 부분을 짚어보겠습니다.

### stop_reason의 역할

```python
if response.stop_reason == "end_turn":
    # LLM이 더 이상 도구가 필요 없다고 판단 → 최종 답변
    return final_text

elif response.stop_reason == "tool_use":
    # LLM이 도구 호출을 요청 → 실행 후 결과를 다시 전달
    ...
```

Claude API는 응답의 `stop_reason`으로 두 가지 상태를 알려줍니다.

- **`end_turn`**: LLM이 답변을 완료했습니다. 도구 호출 없이 텍스트만 반환합니다.
- **`tool_use`**: LLM이 도구를 사용하고 싶다고 요청합니다. 개발자가 도구를 실행하고 결과를 돌려줘야 합니다.

이 두 상태를 기반으로 루프를 제어하는 것이 에이전트의 핵심 메커니즘입니다.

### 대화 히스토리의 누적

```python
messages.append({"role": "assistant", "content": response.content})
# ...
messages.append({"role": "user", "content": tool_results})
```

매 턴마다 어시스턴트의 응답과 도구 실행 결과가 `messages` 리스트에 누적됩니다. 이를 통해 LLM은 이전에 어떤 도구를 호출했고 어떤 결과를 받았는지 기억하며, 중복 검색을 피하고 점진적으로 정보를 축적할 수 있습니다.

### max_turns로 무한 루프 방지

에이전트가 목표를 달성하지 못하고 무한히 도구를 호출하는 것을 방지하기 위해 `max_turns` 제한을 둡니다. 실제 프로덕션 환경에서는 비용 제한(토큰 사용량), 시간 제한도 함께 적용하는 것이 일반적입니다.

---

## 메모리 관리: 에이전트의 기억력

### 문제: 컨텍스트 윈도우의 한계

LLM에는 한 번에 처리할 수 있는 토큰의 양, 즉 **컨텍스트 윈도우** 제한이 있습니다. Claude의 경우 200K 토큰까지 지원하지만, 에이전트가 많은 도구를 호출하면서 대화 히스토리가 빠르게 길어집니다.

```
[메모리 문제 시나리오]

턴 1: 사용자 질문 (100 토큰)
턴 2: 검색 결과 A (2,000 토큰)
턴 3: 검색 결과 B (3,000 토큰)
턴 4: 검색 결과 C (2,500 토큰)
...
턴 20: 누적 50,000 토큰 → 비용 증가 + 응답 속도 저하
```

### 해결 전략 1: 대화 요약(Summarization)

일정 턴 수마다 이전 대화를 요약하여 토큰을 절약합니다.

```python
def summarize_history(client, messages, keep_recent=4):
    """오래된 대화를 요약하여 메모리를 절약합니다."""
    if len(messages) <= keep_recent:
        return messages

    # 오래된 메시지를 분리
    old_messages = messages[:-keep_recent]
    recent_messages = messages[-keep_recent:]

    # 오래된 대화를 요약 요청
    summary_request = (
        "다음 대화 내용을 핵심 정보만 간결하게 요약해주세요:\n\n"
    )
    for msg in old_messages:
        if isinstance(msg["content"], str):
            summary_request += f"{msg['role']}: {msg['content'][:500]}\n"

    summary_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": summary_request}],
    )

    summary_text = summary_response.content[0].text

    # 요약 + 최근 메시지로 재구성
    compressed = [
        {"role": "user", "content": f"[이전 대화 요약]\n{summary_text}"},
        {"role": "assistant", "content": "네, 이전 대화 내용을 이해했습니다."},
    ]
    compressed.extend(recent_messages)

    return compressed
```

### 해결 전략 2: 슬라이딩 윈도우

가장 간단한 방법으로, 최근 N개의 메시지만 유지합니다.

```python
def sliding_window(messages, window_size=20):
    """최근 N개의 메시지만 유지합니다."""
    if len(messages) > window_size:
        return messages[-window_size:]
    return messages
```

### 해결 전략 3: 도구 결과 압축

도구 실행 결과가 지나치게 길 경우, 핵심 내용만 추출합니다.

```python
def compress_tool_result(result: str, max_length: int = 1000) -> str:
    """도구 결과를 최대 길이로 자르고 요약합니다."""
    if len(result) <= max_length:
        return result
    return result[:max_length] + "\n...(결과가 잘렸습니다. 핵심 내용을 기반으로 판단하세요.)"
```

실전에서는 이 세 가지 전략을 상황에 맞게 조합합니다. 대부분의 프로덕션 에이전트는 요약 + 슬라이딩 윈도우를 기본으로 사용합니다.

---

## 확장: 멀티 에이전트 시스템 개요

하나의 에이전트도 강력하지만, 여러 에이전트가 협력하면 더 복잡한 작업을 처리할 수 있습니다. 이것이 **멀티 에이전트 시스템**입니다.

### 멀티 에이전트의 기본 구조

```
                ┌──────────────────┐
                │  오케스트레이터    │
                │  (Orchestrator)  │
                │  작업 분배 + 통합  │
                └───────┬──────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
   ┌────────────┐ ┌──────────┐ ┌──────────────┐
   │ 리서치 에이전트│ │ 코딩 에이전트│ │ 리뷰 에이전트  │
   │ 정보 수집   │ │ 코드 작성  │ │ 품질 검증     │
   └────────────┘ └──────────┘ └──────────────┘
```

### 주요 패턴

| 패턴 | 설명 | 예시 |
|------|------|------|
| **오케스트레이터-워커** | 중앙 에이전트가 작업을 분배하고 결과를 통합 | PM이 개발자에게 업무 배분 |
| **파이프라인** | 에이전트가 순차적으로 작업을 처리 | 조사 → 작성 → 검토 → 발행 |
| **토론(Debate)** | 여러 에이전트가 같은 문제에 대해 다른 관점에서 논의 | 찬성 측 vs 반대 측 토론 |
| **투표(Voting)** | 여러 에이전트가 독립적으로 답변 후 다수결로 결정 | 3개 에이전트 중 2개 이상 동의하면 채택 |

### 간단한 멀티 에이전트 예시

```python
def multi_agent_research(topic: str) -> str:
    """
    두 에이전트가 협력하는 간단한 멀티 에이전트 시스템
    1. 리서치 에이전트: 정보 수집
    2. 라이터 에이전트: 보고서 작성
    """
    # 1단계: 리서치 에이전트가 정보 수집
    research_result = run_agent(
        f"다음 주제에 대한 핵심 사실과 최신 데이터를 조사해줘: {topic}"
    )

    # 2단계: 라이터 에이전트가 보고서 작성
    client = anthropic.Anthropic()
    report = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="당신은 전문 리포트 작성자입니다. 주어진 조사 결과를 바탕으로 구조화된 보고서를 작성하세요.",
        messages=[{
            "role": "user",
            "content": f"다음 조사 결과를 바탕으로 '{topic}'에 대한 보고서를 작성해주세요:\n\n{research_result}"
        }],
    )

    return report.content[0].text
```

멀티 에이전트 시스템은 2026년 현재 가장 활발히 연구되는 분야입니다. Anthropic의 Claude는 **MCP(Model Context Protocol)**를 통해 에이전트 간 통신을 표준화하고 있습니다. MCP에 대한 자세한 내용은 [MCP 완전 가이드: AI 에이전트의 USB-C, 개념부터 서버 구축까지](/posts/mcp-model-context-protocol-guide-2026/)에서 다루고 있습니다.

---

## 에이전트 개발 시 주의사항

실전에서 에이전트를 개발할 때 반드시 고려해야 할 사항들입니다.

### 안전성

```python
# 나쁜 예: 임의의 코드 실행 허용
def dangerous_tool(code: str):
    exec(code)  # 절대 이렇게 하지 마세요!

# 좋은 예: 허용된 작업만 수행
def safe_tool(action: str, params: dict):
    ALLOWED_ACTIONS = {"search", "calculate", "read_file"}
    if action not in ALLOWED_ACTIONS:
        return "허용되지 않은 작업입니다"
    # 허용된 작업만 실행
```

에이전트에게 주는 도구의 권한을 최소화하세요. 파일 삭제, 코드 실행, 결제 처리 등 위험한 작업은 사람의 확인 단계를 추가하는 것이 좋습니다.

### 비용 관리

| 항목 | 관리 방법 |
|------|----------|
| API 호출 횟수 | `max_turns` 제한 설정 |
| 토큰 사용량 | 메모리 압축, 도구 결과 길이 제한 |
| 시간 | 전체 에이전트 실행에 타임아웃 설정 |
| 실패 대응 | 재시도 횟수 제한, 폴백(fallback) 전략 |

### 디버깅과 로깅

에이전트는 여러 단계를 거치기 때문에 어디서 문제가 발생했는지 파악하기 어렵습니다. 충분한 로깅이 필수입니다.

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent")

def run_agent_with_logging(query: str):
    logger.info(f"에이전트 시작: {query}")

    for turn in range(max_turns):
        logger.info(f"턴 {turn + 1}")
        # ... API 호출 ...
        logger.info(f"stop_reason: {response.stop_reason}")

        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    logger.info(f"도구 호출: {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    logger.info(f"도구 결과: {result[:200]}")
```

---

## 바이브 코딩으로 에이전트 만들기

프로그래밍에 익숙하지 않다면 [바이브 코딩](/posts/vibe-coding-guide-2026/)이라는 접근 방법도 있습니다. AI 코딩 도구(Cursor, Claude Code 등)에게 자연어로 "웹 검색 기능이 있는 AI 에이전트를 만들어줘"라고 요청하면, 위에서 다룬 코드와 유사한 결과물을 자동으로 생성해줍니다.

에이전트의 원리를 이해한 상태에서 바이브 코딩을 활용하면, AI가 생성한 코드를 검증하고 필요한 부분을 수정할 수 있어 훨씬 효과적입니다. 원리를 모르고 바이브 코딩만 하면 에러가 발생했을 때 대처하기 어렵기 때문입니다.

---

## 다음 단계: 어디서부터 학습할 것인가

이 튜토리얼을 완료했다면 다음 단계로 진행해보세요.

### 초급 → 중급

1. **도구 추가하기**: 날씨 API, 뉴스 API, 데이터베이스 조회 등 새로운 도구를 에이전트에 추가해보세요.
2. **프롬프트 엔지니어링**: 시스템 프롬프트를 개선하여 에이전트의 판단력을 높이세요.
3. **에러 처리 강화**: 네트워크 실패, API 오류 등 예외 상황에 대응하는 코드를 추가하세요.

### 중급 → 고급

4. **스트리밍 응답 구현**: 사용자가 에이전트의 사고 과정을 실시간으로 볼 수 있게 구현하세요.
5. **MCP 서버 구축**: 에이전트의 도구를 MCP 프로토콜로 표준화하세요. [MCP 완전 가이드](/posts/mcp-model-context-protocol-guide-2026/)를 참고하면 됩니다.
6. **멀티 에이전트**: 여러 에이전트가 협력하는 시스템을 설계하고 구현하세요.
7. **평가(Evaluation)**: 에이전트의 성능을 자동으로 측정하는 테스트 프레임워크를 구축하세요.

### 추천 학습 리소스

| 리소스 | 유형 | 설명 |
|--------|------|------|
| [Anthropic Docs - Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) | 공식 문서 | Claude tool_use 기능의 공식 가이드 |
| [Anthropic Docs - Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) | 공식 문서 | 에이전트 구축에 관한 Anthropic의 공식 권장 사항 |
| [ReAct 논문](https://arxiv.org/abs/2210.03629) | 논문 | ReAct 패턴의 원본 연구 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 프레임워크 | 복잡한 에이전트 워크플로우 구축 프레임워크 |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 프레임워크 | 멀티 에이전트 시스템 구축 프레임워크 |

---

## 마무리

AI 에이전트는 더 이상 연구실의 개념이 아닙니다. 이 글에서 다룬 수십 줄의 Python 코드만으로도 스스로 판단하고 도구를 사용하는 에이전트를 만들 수 있습니다.

핵심을 정리하면 다음과 같습니다.

- **에이전트 = LLM + 도구 + 루프**입니다. LLM이 추론하고, 도구가 실행하며, 루프가 이를 반복합니다.
- **ReAct 패턴**은 추론과 행동을 번갈아 수행하여 복잡한 작업을 단계적으로 해결합니다.
- **Claude API의 tool_use**는 도구 호출을 구조화된 방식으로 지원하여 안정적인 에이전트를 구축할 수 있게 합니다.
- **메모리 관리**는 에이전트가 장기간 동작할 때 필수적인 요소입니다.

2026년은 에이전트의 해입니다. 지금 직접 만들어보면서 이 기술의 가능성을 체험해보세요. 작은 리서치 에이전트에서 시작해서, MCP 연동, 멀티 에이전트까지 점진적으로 확장해 나가면 됩니다.
