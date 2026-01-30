---
title: "Streamlit으로 AI 웹앱 만들기: Python만으로 완성하는 LLM 챗봇 UI (실전 튜토리얼)"
date: 2025-12-29
description: "Streamlit을 활용하여 Python만으로 AI 챗봇 웹 애플리케이션을 만드는 실전 튜토리얼입니다. Claude API 연동, 대화 히스토리, 파일 업로드까지 단계별로 구현합니다."
categories: [AI]
tags: [Streamlit, Python, AI 챗봇, 웹앱, LLM]
keywords: [Streamlit 사용법, Streamlit AI 챗봇, Python 웹앱 만들기, Streamlit 튜토리얼, LLM 웹앱]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: streamlit-ai-webapp-tutorial-2026
---

AI 모델을 만들어놓고 "이걸 어떻게 보여주지?" 하는 순간이 꼭 온다. React 배우자니 한세월이고, Flask로 짜면 UI가 너무 구리고. Streamlit을 쓰면 Python만으로 그럴듯한 웹앱을 뚝딱 만들 수 있는데, 처음 써봤을 때 솔직히 좀 감동이었다.

Streamlit 기초부터 Claude API 연동 챗봇까지, 실전에서 바로 써먹을 수 있게 정리해봤다.

---

## Streamlit이란?

Streamlit은 **데이터 과학자와 AI 개발자를 위한 Python 웹 프레임워크**입니다. HTML, CSS, JavaScript를 전혀 몰라도 Python 스크립트 하나로 인터랙티브한 웹앱을 만들 수 있습니다.

### 왜 Streamlit인가?

```
[기존 방식]
AI 모델 → REST API (FastAPI) → 프론트엔드 (React) → 배포
                                   ↑
                            HTML/CSS/JS 필요
                            별도 학습 비용 높음

[Streamlit 방식]
AI 모델 → Streamlit 앱 (Python만) → 배포
              ↑
         Python만 알면 OK
         UI 컴포넌트 내장
```

---

## 시작하기

### 설치

```bash
pip install streamlit
```

### Hello World

```python
# app.py
import streamlit as st

st.title("Hello Streamlit!")
st.write("Python으로 만든 첫 번째 웹앱입니다.")

# 실행: streamlit run app.py
```

```bash
streamlit run app.py
# → http://localhost:8501 에서 앱 확인
```

---

## 핵심 UI 컴포넌트

### 텍스트 출력

```python
import streamlit as st

st.title("제목")
st.header("헤더")
st.subheader("서브헤더")
st.write("일반 텍스트. **마크다운**도 지원합니다.")
st.markdown("### 마크다운 헤더")
st.code("print('Hello World')", language="python")
st.latex(r"E = mc^2")
```

### 입력 위젯

```python
# 텍스트 입력
name = st.text_input("이름을 입력하세요")
message = st.text_area("메시지를 입력하세요", height=150)

# 숫자
age = st.number_input("나이", min_value=0, max_value=150, value=25)
temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)

# 선택
model = st.selectbox("모델 선택", ["Claude Sonnet", "GPT-4o", "Gemini"])
options = st.multiselect("태그", ["Python", "AI", "Web", "Data"])

# 토글
use_stream = st.toggle("스트리밍 모드", value=True)

# 파일 업로드
uploaded_file = st.file_uploader("파일 업로드", type=["pdf", "txt", "csv"])

# 버튼
if st.button("실행"):
    st.write("버튼이 클릭되었습니다!")
```

### 레이아웃

```python
# 컬럼 레이아웃
col1, col2 = st.columns(2)
with col1:
    st.write("왼쪽 컬럼")
with col2:
    st.write("오른쪽 컬럼")

# 사이드바
with st.sidebar:
    st.title("설정")
    api_key = st.text_input("API Key", type="password")
    model = st.selectbox("모델", ["Claude", "GPT-4o"])

# 탭
tab1, tab2 = st.tabs(["채팅", "설정"])
with tab1:
    st.write("채팅 탭")
with tab2:
    st.write("설정 탭")

# 확장 패널
with st.expander("상세 정보"):
    st.write("접었다 펼칠 수 있는 영역입니다.")
```

---

## 실전 프로젝트: AI 챗봇 만들기

### 기본 챗봇 (Claude API 연동)

```python
"""
Streamlit AI 챗봇 - Claude API 연동
실행: streamlit run chatbot.py
"""

import streamlit as st
import anthropic

# 페이지 설정
st.set_page_config(
    page_title="AI 챗봇",
    page_icon="🤖",
    layout="centered",
)

st.title("AI 챗봇")
st.caption("Claude API 기반 대화형 AI 어시스턴트")

# 사이드바 설정
with st.sidebar:
    api_key = st.text_input("Anthropic API Key", type="password")
    model = st.selectbox("모델", [
        "claude-sonnet-4-20250514",
        "claude-haiku-4-20250414",
    ])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    system_prompt = st.text_area(
        "시스템 프롬프트",
        value="당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 답변합니다.",
        height=100,
    )

# 대화 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    if not api_key:
        st.error("사이드바에서 API Key를 입력해주세요.")
        st.stop()

    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        client = anthropic.Anthropic(api_key=api_key)

        # 스트리밍 응답
        with st.spinner("생각 중..."):
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

        assistant_message = response.content[0].text
        st.markdown(assistant_message)

    # 대화 히스토리에 추가
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message,
    })
```

### 스트리밍 응답 추가

```python
# 위 코드의 AI 응답 생성 부분을 다음으로 교체:

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    with client.messages.stream(
        model=model,
        max_tokens=2048,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
    ) as stream:
        for text in stream.text_stream:
            full_response += text
            message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)
    assistant_message = full_response
```

### 파일 업로드 기능 추가

```python
# 사이드바에 추가
with st.sidebar:
    st.divider()
    st.subheader("문서 업로드")
    uploaded_file = st.file_uploader(
        "PDF 또는 텍스트 파일",
        type=["pdf", "txt"],
    )

    if uploaded_file:
        if uploaded_file.type == "text/plain":
            file_content = uploaded_file.read().decode("utf-8")
        else:
            # PDF 처리 (PyPDF2 필요)
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            file_content = ""
            for page in reader.pages:
                file_content += page.extract_text()

        st.session_state.document = file_content
        st.success(f"파일 업로드 완료: {len(file_content)}자")

# 시스템 프롬프트에 문서 포함
if "document" in st.session_state:
    system_prompt += f"\n\n참고 문서:\n{st.session_state.document[:5000]}"
```

---

## 배포하기

### Streamlit Community Cloud (무료)

가장 간단한 배포 방법입니다.

```
1. GitHub에 프로젝트를 push
2. share.streamlit.io 에 접속
3. GitHub 저장소 연결
4. Deploy 클릭
```

**필요한 파일:**

```
프로젝트/
├── app.py              # 메인 앱
├── requirements.txt    # 의존성
└── .streamlit/
    └── config.toml     # 설정 (선택)
```

```
# requirements.txt
streamlit>=1.40.0
anthropic>=0.40.0
```

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"
```

---

## 유용한 팁 모음

### 성능 최적화: @st.cache

```python
@st.cache_data  # 데이터 캐싱
def load_data(file_path):
    """데이터를 로드하고 캐시합니다."""
    import pandas as pd
    return pd.read_csv(file_path)

@st.cache_resource  # 리소스 캐싱 (ML 모델 등)
def load_model():
    """ML 모델을 로드하고 캐시합니다."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("intfloat/multilingual-e5-large")
```

### Session State 활용

```python
# 페이지 리로드 시에도 데이터 유지
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("카운트 증가"):
    st.session_state.counter += 1

st.write(f"현재 카운트: {st.session_state.counter}")
```

### 프로그레스 바

```python
import time

progress_bar = st.progress(0)
status_text = st.empty()

for i in range(100):
    progress_bar.progress(i + 1)
    status_text.text(f"처리 중... {i + 1}%")
    time.sleep(0.01)

status_text.text("완료!")
```

---

## Streamlit vs 대안 비교

| 항목 | Streamlit | Gradio | Panel | FastAPI + React |
|------|-----------|--------|-------|----------------|
| 학습 난이도 | 매우 쉬움 | 쉬움 | 보통 | 어려움 |
| UI 커스터마이징 | 보통 | 제한적 | 높음 | 무제한 |
| AI/ML 특화 | 우수 | 매우 우수 | 보통 | 보통 |
| 프로덕션 적합도 | 보통 | 보통 | 높음 | 매우 높음 |
| 배포 용이성 | 매우 쉬움 | 쉬움 | 보통 | 어려움 |
| 실시간 업데이트 | 보통 | 우수 | 우수 | 우수 |

**Streamlit 추천 상황:**
- AI/ML 데모 및 프로토타입
- 내부 도구 및 대시보드
- 데이터 분석 리포트
- 소규모 AI 웹 서비스

나는 사내 데모나 빠른 프로토타입에는 항상 Streamlit을 먼저 쓰는데, 프로덕션 수준이 필요해지면 그때 FastAPI + React로 넘어가는 식으로 운영하고 있다.

---

## 마치며

Streamlit은 Python 개발자가 가장 빠르게 AI 웹앱을 만들 수 있는 도구입니다. 프론트엔드 기술 없이도 깔끔한 UI를 구성할 수 있고, Claude나 GPT API와의 연동도 간단합니다. AI 앱의 백엔드 로직을 더 체계적으로 구성하고 싶다면 [LangChain 입문 가이드]({{< relref "posts/2025-12-27-langchain-python-tutorial.md" >}})도 함께 참고해 보세요.

AI 모델을 만들었다면, Streamlit으로 웹앱을 만들어 동료나 고객에게 바로 보여주세요. 프로토타입부터 시작하여 피드백을 받고 개선하는 것이 가장 효율적인 방법입니다.
