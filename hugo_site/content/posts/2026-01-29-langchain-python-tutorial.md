---
title: "LangChain 입문 가이드: Python으로 AI 앱 만들기 (2026 최신판)"
date: 2026-01-29
description: "LangChain의 핵심 개념과 구성 요소를 이해하고, Python으로 실용적인 AI 애플리케이션을 만드는 입문 가이드입니다. 챗봇, 문서 요약, 에이전트까지 실전 예제를 포함합니다."
categories: [AI]
tags: [LangChain, Python, LLM, AI 개발, 에이전트]
keywords: [LangChain 사용법, LangChain 입문, LangChain Python 튜토리얼, AI 앱 만들기, LangChain 에이전트]
draft: true
slug: langchain-python-beginner-guide-2026
---

ChatGPT API를 직접 호출하여 간단한 챗봇을 만드는 것은 어렵지 않습니다. 하지만 "회사 내부 문서를 검색하여 답변하는 챗봇", "여러 도구를 조합하여 복잡한 작업을 수행하는 에이전트"를 만들려면 어떻게 해야 할까요? 이때 필요한 것이 **LangChain**입니다.

LangChain은 LLM을 활용한 애플리케이션을 쉽게 만들 수 있는 **Python 프레임워크**입니다. 2026년 현재 AI 앱 개발의 사실상 표준으로 자리잡았으며, 수많은 기업과 개발자가 프로덕션에서 사용하고 있습니다.

---

## LangChain이란?

LangChain은 **LLM(대규모 언어 모델)을 중심으로 다양한 구성 요소를 연결(Chain)하여 AI 애플리케이션을 구축하는 프레임워크**입니다.

### 왜 LangChain이 필요한가?

LLM API만으로는 다음과 같은 한계가 있습니다.

```
[LLM API만 사용하는 경우]

사용자 → LLM API → 응답
         ↑
    학습 데이터만 사용
    (최신 정보 없음, 내부 문서 접근 불가)

[LangChain을 사용하는 경우]

사용자 → LangChain → LLM API → 응답
              ↕           ↕
         벡터 DB      외부 도구
         웹 검색      데이터베이스
         문서 로더    API 호출
```

LangChain은 LLM과 외부 데이터/도구를 연결하는 **접착제** 역할을 합니다.

### LangChain 생태계 구성

```
┌─────────────────────────────────────────┐
│              LangChain 생태계             │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │langchain │  │langchain │  │  Lang  │ │
│  │  (core)  │  │community │  │ Smith  │ │
│  │          │  │          │  │        │ │
│  │ 핵심 추상화│  │ 서드파티  │  │ 모니터링│ │
│  │ 체인, 에이전│  │ 통합     │  │ 디버깅  │ │
│  └──────────┘  └──────────┘  └────────┘ │
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │ LangGraph│  │ LangServe│             │
│  │          │  │          │             │
│  │ 복잡한    │  │ API 서빙 │             │
│  │ 워크플로우 │  │          │             │
│  └──────────┘  └──────────┘             │
└─────────────────────────────────────────┘
```

---

## 환경 설정

### 패키지 설치

```bash
pip install langchain langchain-anthropic langchain-community \
            langchain-chroma faiss-cpu \
            python-dotenv
```

### 환경 변수 설정

```bash
# .env 파일
ANTHROPIC_API_KEY=your-api-key-here
```

```python
# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()
```

---

## 핵심 개념 1: 모델 (LLM / Chat Model)

LangChain에서 LLM을 사용하는 가장 기본적인 방법입니다.

```python
from langchain_anthropic import ChatAnthropic

# Claude 모델 초기화
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0.7,
    max_tokens=1024,
)

# 기본 호출
response = llm.invoke("파이썬의 장점 3가지를 간단히 알려줘")
print(response.content)
```

### 메시지 타입

Chat Model은 메시지 기반으로 동작합니다.

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="당신은 친절한 한국어 AI 어시스턴트입니다."),
    HumanMessage(content="Docker란 무엇인가요?"),
]

response = llm.invoke(messages)
print(response.content)
```

| 메시지 타입 | 역할 | 설명 |
|------------|------|------|
| SystemMessage | 시스템 | AI의 동작 방식을 설정 |
| HumanMessage | 사용자 | 사용자의 입력 |
| AIMessage | AI | AI의 응답 (대화 히스토리용) |

---

## 핵심 개념 2: 프롬프트 템플릿

하드코딩된 프롬프트 대신, 변수를 포함한 템플릿을 사용합니다.

```python
from langchain_core.prompts import ChatPromptTemplate

# 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 {specialty} 전문가입니다. 한국어로 답변하세요."),
    ("human", "{question}"),
])

# 변수를 채워서 사용
chain = prompt | llm
response = chain.invoke({
    "specialty": "Python 백엔드 개발",
    "question": "FastAPI와 Django의 차이점을 알려줘"
})
print(response.content)
```

### LCEL (LangChain Expression Language)

위 예시에서 사용한 `|` 연산자가 바로 **LCEL**입니다. 파이프라인처럼 구성 요소를 연결합니다.

```python
from langchain_core.output_parsers import StrOutputParser

# LCEL로 체인 구성: 프롬프트 → LLM → 출력 파서
chain = prompt | llm | StrOutputParser()

# 이제 결과가 문자열로 반환됩니다
result = chain.invoke({
    "specialty": "데이터 엔지니어링",
    "question": "ETL과 ELT의 차이점은?"
})
print(result)  # 문자열
```

---

## 핵심 개념 3: 출력 파서

LLM의 출력을 원하는 형식으로 변환합니다.

### JSON 출력 파서

```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 원하는 출력 구조 정의
class BookReview(BaseModel):
    title: str = Field(description="책 제목")
    author: str = Field(description="저자")
    rating: int = Field(description="평점 (1-5)")
    summary: str = Field(description="한줄 요약")
    recommended: bool = Field(description="추천 여부")

parser = JsonOutputParser(pydantic_object=BookReview)

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 도서 리뷰어입니다. {format_instructions}"),
    ("human", "'{book_title}' 책을 리뷰해줘"),
])

chain = prompt | llm | parser
result = chain.invoke({
    "book_title": "클린 코드",
    "format_instructions": parser.get_format_instructions()
})
print(result)
# {'title': '클린 코드', 'author': '로버트 C. 마틴', 'rating': 5, ...}
```

---

## 핵심 개념 4: 체인 (Chain)

여러 구성 요소를 연결하여 복잡한 워크플로우를 만듭니다.

### Sequential Chain: 순차 실행

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1단계: 주제에서 개요 생성
outline_prompt = ChatPromptTemplate.from_messages([
    ("system", "블로그 글의 개요를 작성하는 전문가입니다."),
    ("human", "'{topic}'에 대한 블로그 글 개요를 작성해줘. 3개의 섹션으로."),
])

# 2단계: 개요에서 본문 생성
content_prompt = ChatPromptTemplate.from_messages([
    ("system", "블로그 글을 작성하는 전문 작가입니다."),
    ("human", "다음 개요를 바탕으로 블로그 글을 작성해줘:\n\n{outline}"),
])

# 체인 연결
outline_chain = outline_prompt | llm | StrOutputParser()
content_chain = content_prompt | llm | StrOutputParser()

# 순차 실행
outline = outline_chain.invoke({"topic": "AI 시대의 개발자 역할"})
content = content_chain.invoke({"outline": outline})
print(content)
```

### RunnablePassthrough: 데이터 전달

```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# 병렬 실행: 같은 입력으로 여러 체인 동시 실행
parallel_chain = RunnableParallel(
    pros=ChatPromptTemplate.from_template("{topic}의 장점 3가지") | llm | StrOutputParser(),
    cons=ChatPromptTemplate.from_template("{topic}의 단점 3가지") | llm | StrOutputParser(),
)

result = parallel_chain.invoke({"topic": "마이크로서비스 아키텍처"})
print("장점:", result["pros"])
print("단점:", result["cons"])
```

---

## 핵심 개념 5: 메모리 (대화 히스토리)

챗봇을 만들려면 이전 대화를 기억해야 합니다.

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 세션별 대화 히스토리 저장소
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 프롬프트에 대화 히스토리 포함
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 AI 어시스턴트입니다."),
    ("placeholder", "{history}"),
    ("human", "{input}"),
])

chain = prompt | llm

# 메모리를 연결한 체인
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 대화 테스트
config = {"configurable": {"session_id": "user-001"}}

r1 = chain_with_history.invoke(
    {"input": "내 이름은 철수야"},
    config=config,
)
print(r1.content)

r2 = chain_with_history.invoke(
    {"input": "내 이름이 뭐라고 했지?"},
    config=config,
)
print(r2.content)  # "철수"라고 기억합니다
```

---

## 핵심 개념 6: 도구 (Tools) & 에이전트 (Agent)

에이전트는 LLM이 **스스로 판단하여 도구를 선택하고 실행**하는 시스템입니다.

### 도구 정의

```python
from langchain_core.tools import tool

@tool
def search_weather(city: str) -> str:
    """주어진 도시의 현재 날씨를 검색합니다."""
    # 실제로는 날씨 API를 호출
    weather_data = {
        "서울": "맑음, 기온 5°C",
        "부산": "흐림, 기온 8°C",
        "제주": "비, 기온 10°C",
    }
    return weather_data.get(city, f"{city}의 날씨 정보를 찾을 수 없습니다.")

@tool
def calculate(expression: str) -> str:
    """수학 계산을 수행합니다. 예: '2 + 3 * 4'"""
    try:
        result = eval(expression)  # 프로덕션에서는 안전한 파서 사용
        return str(result)
    except Exception as e:
        return f"계산 오류: {e}"
```

### 에이전트 구성

```python
from langgraph.prebuilt import create_react_agent

# 도구 목록
tools = [search_weather, calculate]

# 에이전트 생성
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="당신은 날씨 정보와 계산을 도와주는 AI 어시스턴트입니다."
)

# 에이전트 실행
result = agent.invoke({
    "messages": [("human", "서울 날씨 알려주고, 15 * 24가 뭔지도 계산해줘")]
})
print(result["messages"][-1].content)
```

에이전트의 동작 과정:

```
사용자: "서울 날씨 알려주고, 15 * 24가 뭔지도 계산해줘"

에이전트 사고:
  → 두 가지 작업이 필요하다
  → 1) search_weather("서울") 호출
  → 결과: "맑음, 기온 5°C"
  → 2) calculate("15 * 24") 호출
  → 결과: "360"
  → 두 결과를 종합하여 답변 생성

에이전트 응답:
  "서울의 현재 날씨는 맑음이고 기온은 5°C입니다.
   그리고 15 × 24 = 360입니다."
```

---

## 실전 프로젝트: FAQ 챗봇 만들기

LangChain으로 회사 FAQ 문서를 기반으로 답변하는 챗봇을 만들어 봅니다.

```python
"""
FAQ 챗봇 - LangChain + ChromaDB + Claude
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. FAQ 데이터 준비
faq_data = [
    "Q: 연차 휴가는 며칠인가요?\nA: 1년 이상 근속 시 15일의 유급 연차가 부여됩니다.",
    "Q: 재택근무 신청은 어떻게 하나요?\nA: HR 시스템에서 3일 전까지 신청하면 됩니다.",
    "Q: 야근 수당은 어떻게 계산되나요?\nA: 통상 시급의 1.5배가 적용됩니다.",
    "Q: 교육비 지원이 있나요?\nA: 연간 100만원의 자기개발비를 지원합니다.",
]

# 2. 텍스트 분할 & 벡터 DB 생성
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=20
)
docs = text_splitter.create_documents(faq_data)

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large"
)
vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 3. RAG 체인 구성
prompt = ChatPromptTemplate.from_template("""
다음 FAQ 정보를 기반으로 질문에 답변하세요.
FAQ에 없는 정보는 "해당 정보를 찾을 수 없습니다"라고 답하세요.

FAQ 정보:
{context}

질문: {question}
답변:""")

llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 4. 실행
answer = chain.invoke("연차가 며칠이에요?")
print(answer)
```

---

## 자주 하는 실수와 해결법

| 실수 | 해결법 |
|------|--------|
| API 키를 코드에 직접 작성 | `.env` 파일 + `python-dotenv` 사용 |
| 토큰 한도 초과 | `max_tokens` 설정, 입력 텍스트 길이 관리 |
| 체인에서 변수명 불일치 | 프롬프트의 변수명과 invoke 딕셔너리 키 일치 확인 |
| 느린 응답 속도 | 스트리밍 사용: `chain.stream()` |
| 에이전트 무한 루프 | `max_iterations` 파라미터로 제한 |

---

## 마무리

LangChain은 LLM 기반 애플리케이션을 빠르게 프로토타이핑하고 프로덕션까지 가져갈 수 있는 프레임워크입니다. 이 글에서 다룬 핵심 개념만 이해하면 대부분의 AI 앱을 만들 수 있습니다.

학습 순서를 정리하면:

```
1. 모델 + 프롬프트 → 기본 호출
2. LCEL → 체인 구성
3. 출력 파서 → 구조화된 결과
4. 메모리 → 대화 챗봇
5. RAG → 문서 기반 QA
6. 에이전트 → 자율 행동 AI
```

다음 글에서는 AI 이미지 생성 도구 비교를 다루겠습니다.
