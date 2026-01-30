---
title: "나만의 AI 챗봇 만들기: Python으로 처음부터 배포까지 (2026)"
date: 2026-01-30
description: "Python과 LLM API를 활용해 나만의 AI 챗봇을 만드는 방법. 설계부터 대화 관리, 메모리 구현, 웹 배포까지 단계별로 설명합니다."
categories: [AI]
tags: [AI 챗봇, Python, LLM, Claude API, 챗봇 개발]
keywords: [AI 챗봇 만들기, Python 챗봇 개발, LLM 챗봇 구축, Claude 챗봇 만들기, AI 챗봇 튜토리얼]
draft: true
slug: ai-chatbot-build-guide-python-2026
---

ChatGPT와 Claude를 써보면서 "나도 이런 챗봇을 만들 수 있을까?"라고 생각해본 적 있으신가요? 2026년 현재, LLM API를 활용하면 **몇 시간 만에** 자신만의 AI 챗봇을 만들 수 있습니다.

이 글에서는 Python으로 AI 챗봇을 처음부터 만들고, 대화 기록 관리, 시스템 프롬프트 설정, 웹 인터페이스 구축까지 실전 과정을 안내합니다.

---

## 왜 나만의 챗봇인가?

상용 AI 서비스를 그대로 쓰면 되지 않냐고요? 나만의 챗봇이 필요한 이유는 명확합니다.

| 상용 서비스 | 나만의 챗봇 |
|------------|-----------|
| 범용 응답 | 도메인 특화 응답 |
| 데이터 외부 전송 | 내부 서버에서 처리 가능 |
| 커스터마이징 제한 | 완전한 제어 |
| 월정액 구독 | 사용량 기반 비용 |
| 기능 제한적 | 외부 시스템 연동 자유 |

회사 내부 FAQ 봇, 고객 상담 봇, 학습 도우미, 개인 비서 등 **특정 목적에 최적화된 챗봇**은 직접 만들어야 합니다.

---

## Step 1: 기본 챗봇 구조

### 프로젝트 설정

```bash
mkdir my-chatbot && cd my-chatbot
pip install anthropic fastapi uvicorn jinja2
```

### 핵심 챗봇 클래스

```python
# chatbot.py
from anthropic import Anthropic

class ChatBot:
    def __init__(self, system_prompt: str = ""):
        self.client = Anthropic()
        self.system_prompt = system_prompt
        self.conversation_history: list[dict] = []

    def chat(self, user_message: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
        })

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history,
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message,
        })

        return assistant_message

    def reset(self):
        self.conversation_history = []
```

이 구조의 핵심은 `conversation_history`입니다. 매번 대화 전체를 API에 전달하여 **맥락을 유지**합니다.

---

## Step 2: 시스템 프롬프트 설계

시스템 프롬프트는 챗봇의 **성격, 역할, 규칙**을 정의합니다. 잘 설계된 시스템 프롬프트가 챗봇 품질의 80%를 결정합니다.

### 예시: 고객 상담 챗봇

```python
SYSTEM_PROMPT = """당신은 'AI김비서'라는 이름의 온라인 쇼핑몰 고객 상담 챗봇입니다.

## 역할
- 고객의 주문, 배송, 반품, 교환 관련 질문에 답변합니다.
- 친절하고 전문적인 톤을 유지합니다.
- 한국어로 응답합니다.

## 규칙
- 답변은 3문장 이내로 간결하게 합니다.
- 확실하지 않은 정보는 "확인 후 안내드리겠습니다"라고 답합니다.
- 개인정보(주민번호, 카드번호 등)는 절대 요청하지 않습니다.
- 환불/교환은 7일 이내, 배송은 2-3일 소요로 안내합니다.

## 응답 형식
인사 → 답변 → 추가 도움 여부 확인
"""

bot = ChatBot(system_prompt=SYSTEM_PROMPT)
```

### 시스템 프롬프트 설계 팁

1. **역할을 명확히** — "당신은 ~입니다"로 시작
2. **규칙을 구체적으로** — 하지 말아야 할 것도 명시
3. **응답 형식 지정** — 일관된 출력 유도
4. **예외 처리** — 모르는 질문에 대한 대응 방법 명시

---

## Step 3: 대화 메모리 관리

대화가 길어지면 토큰 제한에 걸립니다. 효율적인 메모리 관리가 필요합니다.

### 슬라이딩 윈도우 방식

```python
class ChatBotWithMemory(ChatBot):
    def __init__(self, system_prompt: str = "", max_turns: int = 20):
        super().__init__(system_prompt)
        self.max_turns = max_turns

    def chat(self, user_message: str) -> str:
        # 오래된 대화 제거 (최근 N턴만 유지)
        if len(self.conversation_history) > self.max_turns * 2:
            self.conversation_history = self.conversation_history[-(self.max_turns * 2):]

        return super().chat(user_message)
```

### 요약 기반 메모리

```python
def summarize_history(self) -> str:
    """오래된 대화를 요약하여 압축한다."""
    if len(self.conversation_history) <= 10:
        return

    old_messages = self.conversation_history[:-10]
    summary_response = self.client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"다음 대화를 3줄로 요약해줘:\n{old_messages}",
        }],
    )

    summary = summary_response.content[0].text
    self.conversation_history = [
        {"role": "user", "content": f"[이전 대화 요약: {summary}]"},
        {"role": "assistant", "content": "네, 이전 대화 내용을 기억하고 있습니다."},
    ] + self.conversation_history[-10:]
```

---

## Step 4: 웹 인터페이스 구축

### FastAPI + HTML 템플릿

```python
# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
bot = ChatBot(system_prompt="당신은 친절한 AI 비서입니다. 한국어로 답합니다.")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    reply = bot.chat(req.message)
    return ChatResponse(reply=reply)


@app.post("/reset")
async def reset_endpoint():
    bot.reset()
    return {"status": "ok"}
```

### 프론트엔드 (templates/chat.html)

간단한 채팅 UI를 HTML/CSS/JavaScript로 구성하고, `/chat` 엔드포인트에 POST 요청을 보내면 됩니다.

---

## Step 5: 고급 기능 추가

### 도구 사용 (Tool Use)

챗봇이 외부 시스템과 상호작용하도록 도구를 정의할 수 있습니다.

```python
tools = [
    {
        "name": "check_order_status",
        "description": "주문번호로 배송 상태를 조회합니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "주문번호 (예: ORD-20260130-001)",
                }
            },
            "required": ["order_id"],
        },
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)
```

### 스트리밍 응답

실시간으로 응답을 표시하면 사용자 경험이 크게 향상됩니다.

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## 비용 최적화

| 전략 | 효과 |
|------|------|
| 시스템 프롬프트 간결하게 | 매 요청마다 토큰 절약 |
| 슬라이딩 윈도우 메모리 | 긴 대화 시 토큰 폭증 방지 |
| Haiku 모델 (간단한 질문) | 비용 1/10 절감 |
| 캐싱 (자주 묻는 질문) | API 호출 자체 감소 |
| 프롬프트 캐싱 활용 | 시스템 프롬프트 비용 90% 절감 |

---

## 마무리

AI 챗봇 개발은 더 이상 어렵지 않습니다. LLM API 하나면 핵심 로직은 완성되고, 나머지는 비즈니스 로직과 사용자 경험에 집중하면 됩니다.

**시작하기 좋은 순서:**
1. 기본 ChatBot 클래스로 CLI 챗봇 만들기
2. 시스템 프롬프트 설계 및 테스트
3. 웹 인터페이스 추가
4. 도구 사용, 메모리 관리 등 고급 기능 추가
5. 배포 (Railway, Fly.io 등)

가장 중요한 것은 **시스템 프롬프트 설계**입니다. 코드는 단순하지만, 프롬프트가 챗봇의 품질을 결정합니다.
