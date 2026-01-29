---
title: "내 컴퓨터에서 AI 돌리기: Ollama로 로컬 LLM 설치하고 활용하는 법 (2026)"
date: 2026-01-29
description: "Ollama를 이용해 내 컴퓨터에서 무료로 AI를 실행하는 방법. 설치부터 한국어 모델 추천, 실전 활용까지 완전 가이드."
categories: [AI]
tags: [Ollama, 로컬 LLM, AI 무료, DeepSeek, 오픈소스 AI]
keywords: [Ollama 설치 방법, 로컬 LLM, 로컬 AI 무료, Ollama 한국어 모델, Ollama vs ChatGPT]
draft: false
slug: ollama-local-llm-setup-guide-2026
---

ChatGPT, Claude, Gemini 같은 클라우드 AI 서비스를 매달 수만 원씩 내면서 쓰고 계신가요? 혹시 회사 기밀 데이터를 외부 AI에 넣는 게 불안하신 적 있나요? 그렇다면 **로컬 LLM**이 답입니다.

2026년 현재, 오픈소스 AI 모델의 성능은 놀라울 정도로 발전했습니다. DeepSeek-R1, Qwen 2.5, Llama 3 같은 모델들은 웬만한 작업에서 유료 AI 서비스에 뒤지지 않는 성능을 보여줍니다. 그리고 이 모든 걸 **내 컴퓨터에서 무료로** 실행할 수 있게 해주는 도구가 바로 **Ollama**입니다.

이 글에서는 Ollama 설치부터 한국어에 강한 모델 추천, 실전 활용법, API 연동, 그리고 클라우드 AI와의 비교까지 완전히 다룹니다. 프로그래밍 경험이 없어도 따라 할 수 있도록 단계별로 안내합니다.

---

## 1. 왜 로컬 LLM인가?

"ChatGPT 쓰면 되는데 굳이 내 컴퓨터에서 돌려야 하나?"라는 질문을 자주 받습니다. 로컬 LLM을 선택해야 하는 이유는 명확합니다.

### 완전 무료, 무제한 사용

ChatGPT Plus는 월 20달러(약 2만 7천 원), Claude Pro는 월 20달러입니다. 1년이면 약 32만 원이 나갑니다. 로컬 LLM은 한 번 설치하면 **전기세 외에는 추가 비용이 전혀 없습니다.** 하루에 1,000번을 질문해도, 10만 토큰짜리 문서를 분석해도 추가 과금이 없습니다.

API를 쓰는 개발자라면 비용 절감이 더 극적입니다. GPT-4o API는 입력 100만 토큰당 2.5달러, 출력 100만 토큰당 10달러인데, 로컬 LLM은 이 비용이 0원입니다.

### 데이터 프라이버시 보장

클라우드 AI에 입력한 데이터는 해당 기업의 서버를 거칩니다. 회사 코드, 고객 정보, 개인 일기, 의료 기록 등 민감한 데이터를 다룰 때 로컬 LLM은 **데이터가 내 컴퓨터 밖으로 나가지 않기 때문에** 완벽한 프라이버시를 보장합니다.

2025년부터 시행된 EU AI Act나 한국의 AI 기본법을 고려하면, 기업에서 로컬 LLM을 도입하는 건 규제 대응 차원에서도 현명한 선택입니다.

### 오프라인 사용 가능

비행기 안에서, 인터넷이 불안정한 카페에서, 보안 네트워크 내부에서도 AI를 쓸 수 있습니다. 모델을 한 번 다운로드하면 인터넷 연결 없이도 완벽하게 작동합니다.

### 완전한 커스터마이징

프롬프트 제한 없이 시스템 프롬프트를 자유롭게 설정할 수 있고, 모델을 파인튜닝하거나, RAG(검색증강생성) 파이프라인을 자유롭게 구성할 수 있습니다. 클라우드 AI의 안전 필터에 가로막힌 적이 있다면, 로컬 LLM의 자유도가 매력적으로 느껴질 것입니다.

---

## 2. Ollama란 무엇인가?

**Ollama**는 오픈소스 LLM을 로컬 환경에서 손쉽게 실행할 수 있도록 만들어진 도구입니다. Docker가 컨테이너 실행을 쉽게 만들어준 것처럼, Ollama는 AI 모델 실행을 쉽게 만들어줍니다.

### Ollama의 핵심 특징

- **원클릭 모델 다운로드 및 실행**: `ollama run llama3` 한 줄이면 모델 다운로드부터 실행까지 자동 처리
- **다양한 모델 지원**: DeepSeek, Llama, Qwen, Mistral, Gemma, Phi 등 100개 이상의 오픈소스 모델 지원
- **자동 GPU 가속**: NVIDIA, AMD, Apple Silicon GPU를 자동 감지하여 최적 성능 발휘
- **REST API 내장**: 별도 설정 없이 HTTP API를 통해 다른 프로그램과 연동 가능
- **크로스 플랫폼**: Windows, macOS, Linux 모두 지원
- **Modelfile 지원**: 커스텀 시스템 프롬프트, 파라미터를 설정한 나만의 모델 생성 가능

쉽게 말해, Ollama는 **"AI 모델의 패키지 매니저"**라고 생각하면 됩니다. npm이 JavaScript 패키지를 관리하듯, Ollama는 AI 모델을 관리합니다.

---

## 3. 하드웨어 요구사항

로컬 LLM은 모델 크기에 따라 필요한 하드웨어가 달라집니다. 아래 표를 참고해서 자신의 컴퓨터에 맞는 모델을 선택하세요.

### 모델 크기별 최소 사양

| 모델 크기 | RAM 최소 | VRAM(GPU) 권장 | 적합한 작업 | 대표 모델 |
|-----------|---------|---------------|------------|----------|
| 1B~3B | 8GB | 4GB | 간단한 분류, 요약 | Phi-4-mini, Gemma 3 1B |
| 7B~8B | 16GB | 8GB | 일반 대화, 코딩 보조, 번역 | Llama 3 8B, Qwen 2.5 7B |
| 14B | 16GB | 12GB | 고품질 한국어, 복잡한 코딩 | Qwen 2.5 14B, DeepSeek-R1 14B |
| 32B~34B | 32GB | 24GB | 전문 분석, 긴 문서 처리 | DeepSeek-R1 32B, Qwen 2.5 32B |
| 70B+ | 64GB+ | 48GB+ | 최고 성능 (서버급) | Llama 3 70B, DeepSeek-R1 70B |

### GPU별 실행 가능 모델 가이드

| GPU | VRAM | 최대 권장 모델 크기 | 예상 속도 (tok/s) |
|-----|------|-------------------|------------------|
| NVIDIA RTX 3060 | 12GB | 14B (Q4 양자화) | 15~25 |
| NVIDIA RTX 4060 Ti | 16GB | 14B (Q5) / 32B (Q4) | 20~35 |
| NVIDIA RTX 4070 Ti Super | 16GB | 14B (Q6) / 32B (Q4) | 30~45 |
| NVIDIA RTX 4080 | 16GB | 32B (Q4) | 35~50 |
| NVIDIA RTX 4090 | 24GB | 32B (Q6) / 70B (Q4) | 40~60 |
| Apple M2 Pro | 16GB (통합) | 14B (Q4) | 15~25 |
| Apple M3 Max | 36GB (통합) | 32B (Q5) / 70B (Q3) | 25~40 |
| Apple M4 Pro | 24GB (통합) | 32B (Q4) | 30~45 |
| AMD RX 7900 XTX | 24GB | 32B (Q6) / 70B (Q4) | 25~40 |

> **참고**: Q4, Q5, Q6은 양자화(Quantization) 수준입니다. 숫자가 클수록 품질이 좋지만 더 많은 메모리를 사용합니다. Q4는 원본 대비 약 95% 성능을 유지하면서 메모리를 크게 절약합니다.

### GPU가 없다면?

GPU가 없어도 CPU만으로 실행할 수 있습니다. 다만 속도가 느립니다.
- **7B 모델 CPU 실행**: 초당 약 3~8 토큰 (체감상 한 문장에 2~5초)
- **3B 이하 모델**: CPU에서도 쾌적하게 사용 가능

RAM이 16GB 이상이라면 7B 모델을 CPU로 돌려보는 것부터 시작하시는 걸 추천합니다.

---

## 4. 설치 방법 (OS별 완전 가이드)

### macOS 설치

macOS는 가장 간단합니다. Homebrew를 사용하거나 공식 사이트에서 다운로드하세요.

**방법 1: Homebrew (추천)**

```bash
# Homebrew가 없다면 먼저 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Ollama 설치
brew install ollama

# 설치 확인
ollama --version
```

**방법 2: 공식 다운로드**

[ollama.com](https://ollama.com) 에서 macOS 앱을 다운로드하여 설치합니다. 앱을 실행하면 메뉴바에 아이콘이 나타나며 백그라운드에서 서버가 실행됩니다.

### Windows 설치

```powershell
# 방법 1: 공식 설치 프로그램
# ollama.com 에서 Windows 설치 파일(.exe) 다운로드 후 실행

# 방법 2: winget 사용
winget install Ollama.Ollama

# 설치 확인 (새 터미널 창에서)
ollama --version
```

Windows에서는 설치 후 시스템 트레이에 Ollama 아이콘이 나타납니다. 이 아이콘이 보이면 서비스가 정상 실행 중입니다.

> **Windows 팁**: WSL2(Windows Subsystem for Linux)에서도 Linux 방식으로 설치 가능합니다. Docker 환경에 익숙하다면 WSL2를 추천합니다.

### Linux 설치

```bash
# 원라인 설치 스크립트 (Ubuntu, Debian, Fedora, Arch 등 지원)
curl -fsSL https://ollama.com/install.sh | sh

# 설치 확인
ollama --version

# 서비스 상태 확인
systemctl status ollama

# 부팅 시 자동 시작 설정
sudo systemctl enable ollama
```

### 첫 모델 다운로드 및 실행

설치가 완료되면, 터미널에서 바로 첫 모델을 실행해봅시다.

```bash
# Llama 3 8B 모델 다운로드 및 실행 (약 4.7GB)
ollama run llama3

# 실행되면 대화형 프롬프트가 나타납니다
>>> 안녕하세요! 한국어로 대화할 수 있나요?
```

첫 실행 시 모델 다운로드에 몇 분이 소요됩니다. 다운로드가 완료되면 이후에는 즉시 실행됩니다.

### 기본 명령어 정리

```bash
# 모델 목록 확인
ollama list

# 모델 다운로드만 (실행 없이)
ollama pull deepseek-r1:14b

# 모델 실행
ollama run deepseek-r1:14b

# 실행 중인 모델 확인
ollama ps

# 모델 삭제 (디스크 공간 확보)
ollama rm llama3

# 모델 상세 정보 확인
ollama show deepseek-r1:14b
```

---

## 5. 2026년 추천 모델 TOP 5 (한국어 성능 기준)

2026년 1월 기준, 한국어 성능이 뛰어난 로컬 실행 가능 모델 TOP 5를 소개합니다.

### 1위: DeepSeek-R1 (14B / 32B)

```bash
ollama run deepseek-r1:14b    # 14B 버전 (약 9GB)
ollama run deepseek-r1:32b    # 32B 버전 (약 20GB)
```

- **한국어 성능**: 매우 우수 (오픈소스 모델 중 최상위권)
- **특징**: Chain-of-Thought(사고 과정) 추론에 매우 강함. 수학, 코딩, 논리 문제에서 GPT-4 수준의 성능
- **장점**: 복잡한 추론 과제에서 압도적. 한국어 이해력과 생성 능력이 동급 최강
- **단점**: 추론 과정을 보여주기 때문에 응답 길이가 길어질 수 있음
- **추천 대상**: 코딩, 분석, 수학 문제 등 깊은 사고가 필요한 작업

### 2위: Qwen 2.5 (7B / 14B / 32B)

```bash
ollama run qwen2.5:7b     # 7B 버전 (약 4.4GB)
ollama run qwen2.5:14b    # 14B 버전 (약 9GB)
ollama run qwen2.5:32b    # 32B 버전 (약 20GB)
```

- **한국어 성능**: 우수 (CJK 언어 특화 학습)
- **특징**: Alibaba Cloud에서 개발. 다국어 성능이 뛰어나며 특히 아시아 언어에 강함
- **장점**: 한국어 자연스러움이 뛰어나고, 7B 모델도 한국어 품질이 높음
- **단점**: 일부 작업에서 DeepSeek-R1 대비 추론 깊이가 얕을 수 있음
- **추천 대상**: 일반 대화, 글쓰기, 번역 등 한국어 중심 작업

### 3위: Llama 3.3 (8B / 70B)

```bash
ollama run llama3.3       # 8B 버전 (약 4.7GB)
ollama run llama3.3:70b   # 70B 버전 (약 40GB)
```

- **한국어 성능**: 양호 (이전 버전 대비 크게 향상)
- **특징**: Meta에서 개발한 가장 대중적인 오픈소스 모델. 커뮤니티 생태계가 가장 넓음
- **장점**: 안정적인 성능, 풍부한 파인튜닝 모델, 최대 128K 컨텍스트 윈도우
- **단점**: 동일 파라미터 기준 한국어는 Qwen이나 DeepSeek에 약간 뒤처짐
- **추천 대상**: 영어 중심 작업, 범용 목적, 커뮤니티 모델 활용

### 4위: Mistral Small / Nemo (7B / 12B)

```bash
ollama run mistral         # 7B 버전 (약 4.1GB)
ollama run mistral-nemo    # 12B 버전 (약 7.1GB)
```

- **한국어 성능**: 보통 (유럽어 > 아시아어)
- **특징**: 프랑스 Mistral AI에서 개발. 모델 크기 대비 성능이 뛰어남
- **장점**: 가볍고 빠름. 코드 생성 능력 우수. 7B 모델의 효율성이 탁월
- **단점**: 한국어 전용 학습 데이터가 상대적으로 적음
- **추천 대상**: 빠른 응답이 필요한 작업, 코딩 보조, 영어 중심 작업

### 5위: Gemma 3 (4B / 12B / 27B)

```bash
ollama run gemma3:4b     # 4B 버전 (약 3.3GB)
ollama run gemma3:12b    # 12B 버전 (약 8GB)
ollama run gemma3:27b    # 27B 버전 (약 17GB)
```

- **한국어 성능**: 양호 (Google 다국어 데이터 활용)
- **특징**: Google DeepMind에서 개발. 멀티모달(이미지 이해) 지원이 특징
- **장점**: 이미지 입력 가능, 안정적인 성능, Google 생태계와 호환
- **단점**: 같은 크기 대비 추론 능력은 DeepSeek에 뒤처짐
- **추천 대상**: 이미지 분석이 필요한 작업, 가벼운 범용 작업

### 한국어 성능 비교 요약

| 모델 | 크기 | 한국어 자연스러움 | 한국어 이해력 | 추론 능력 | 속도 |
|------|------|-----------------|-------------|----------|------|
| DeepSeek-R1 14B | 14B | 9/10 | 9/10 | 10/10 | 보통 |
| Qwen 2.5 14B | 14B | 9/10 | 9/10 | 8/10 | 빠름 |
| Llama 3.3 8B | 8B | 7/10 | 7/10 | 7/10 | 빠름 |
| Mistral Nemo 12B | 12B | 6/10 | 6/10 | 7/10 | 매우 빠름 |
| Gemma 3 12B | 12B | 7/10 | 7/10 | 7/10 | 빠름 |

> **입문자 추천**: 16GB RAM이면 **Qwen 2.5 7B**로 시작하세요. 한국어 성능이 좋고 가볍습니다. 하드웨어가 여유 있다면 **DeepSeek-R1 14B**가 최고의 선택입니다.

---

## 6. 실전 활용 4가지

모델을 설치했으니, 이제 실제로 어떻게 활용하는지 알아봅시다.

### 활용 1: 코딩 어시스턴트

Ollama를 코딩 도우미로 쓰면 GitHub Copilot 구독료를 아낄 수 있습니다.

```bash
# DeepSeek-R1은 코딩에 특히 강합니다
ollama run deepseek-r1:14b
```

**프롬프트 예시:**

```
>>> Python으로 CSV 파일을 읽어서 월별 매출 합계를 계산하고,
    matplotlib로 막대 그래프를 그리는 코드를 작성해줘.
    CSV 컬럼은 date, product, amount 입니다.
```

**VS Code 연동:**

VS Code에서 **Continue** 확장 프로그램을 설치하면 Ollama를 코딩 어시스턴트로 바로 사용할 수 있습니다.

```json
// ~/.continue/config.json
{
  "models": [
    {
      "title": "DeepSeek-R1 14B (Local)",
      "provider": "ollama",
      "model": "deepseek-r1:14b"
    }
  ]
}
```

설정 후 VS Code에서 코드 선택 후 `Ctrl+L`(Mac: `Cmd+L`)을 누르면 AI에게 질문할 수 있습니다.

### 활용 2: 문서 Q&A (RAG)

회사 문서, PDF, 노트 등을 AI에게 읽히고 질문하는 RAG(Retrieval-Augmented Generation) 시스템을 구축할 수 있습니다.

**Open WebUI 사용 (가장 쉬운 방법):**

```bash
# Docker로 Open WebUI 설치
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

설치 후 `http://localhost:3000`에 접속하면 ChatGPT와 비슷한 웹 UI가 나타납니다. 여기서 문서를 업로드하고 질문할 수 있습니다.

**Python으로 간단한 RAG 구현:**

```python
# pip install langchain langchain-ollama chromadb
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. PDF 로드
loader = PyPDFLoader("회사규정.pdf")
documents = loader.load()

# 2. 텍스트 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 3. 벡터 DB 생성
embeddings = OllamaEmbeddings(model="qwen2.5:7b")
vectorstore = Chroma.from_documents(splits, embeddings)

# 4. Q&A 체인 생성
llm = OllamaLLM(model="qwen2.5:14b")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# 5. 질문하기
answer = qa_chain.invoke("연차 휴가는 며칠인가요?")
print(answer["result"])
```

### 활용 3: 번역기

Ollama를 전용 번역기로 설정하면, DeepL이나 Google 번역 대신 사용할 수 있습니다. 특히 기술 문서나 전문 용어가 많은 텍스트에서 맥락을 이해하는 번역이 가능합니다.

**Modelfile로 전용 번역 모델 만들기:**

```bash
# translator.Modelfile 생성
cat << 'EOF' > translator.Modelfile
FROM qwen2.5:14b
SYSTEM """당신은 전문 번역가입니다. 사용자가 입력하는 텍스트를 다음 규칙에 따라 번역합니다:
- 한국어 입력 → 영어로 번역
- 영어 입력 → 한국어로 번역
- 다른 언어 → 한국어로 번역
원문의 뉘앙스와 전문 용어를 최대한 살려서 자연스럽게 번역하세요.
번역문만 출력하고, 부가 설명은 하지 마세요."""
PARAMETER temperature 0.3
PARAMETER num_ctx 8192
EOF

# 커스텀 모델 생성
ollama create translator -f translator.Modelfile

# 번역 모델 실행
ollama run translator
```

```
>>> The transformer architecture has revolutionized natural language processing
    by enabling models to attend to all positions in the input sequence simultaneously.

트랜스포머 아키텍처는 모델이 입력 시퀀스의 모든 위치에 동시에 주의를 기울일 수
있게 함으로써 자연어 처리 분야에 혁명을 일으켰습니다.
```

### 활용 4: 개인 챗봇

나만의 성격과 지식을 가진 개인 비서 챗봇을 만들어봅시다.

```bash
# assistant.Modelfile 생성
cat << 'EOF' > assistant.Modelfile
FROM deepseek-r1:14b
SYSTEM """당신은 김서연이라는 이름의 한국어 AI 비서입니다.
성격은 친절하고 차분하며, 전문적이면서도 유머 감각이 있습니다.
사용자를 '선생님'이라고 부르며, 존댓말을 사용합니다.
가능하면 구체적인 예시와 함께 답변하고, 필요시 단계별로 설명합니다.
한국 문화와 트렌드에 대한 이해가 있으며, 한국어 관용 표현을 적절히 사용합니다."""
PARAMETER temperature 0.7
PARAMETER num_ctx 16384
PARAMETER top_p 0.9
EOF

# 비서 모델 생성 및 실행
ollama create my-assistant -f assistant.Modelfile
ollama run my-assistant
```

```
>>> 이번 주 금요일에 팀 회식이 있는데, 강남역 근처 추천 맛집 알려줘

선생님, 팀 회식 장소를 찾고 계시군요! 강남역 근처에 몇 곳 추천드리겠습니다.
인원수와 예산대에 따라 추천이 달라질 수 있는데, 대략적으로 알려주실 수 있을까요?

일단 일반적으로 인기 있는 유형별로 정리해 드리면...
```

---

## 7. Ollama API 활용법

Ollama는 기본적으로 **포트 11434**에서 REST API를 제공합니다. 이를 통해 모든 프로그래밍 언어에서 Ollama를 연동할 수 있습니다.

### 기본 API 사용법

```bash
# 서버 상태 확인
curl http://localhost:11434

# 텍스트 생성 (비스트리밍)
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:14b",
  "prompt": "한국의 수도는?",
  "stream": false
}'

# 채팅 API (대화 형식)
curl http://localhost:11434/api/chat -d '{
  "model": "deepseek-r1:14b",
  "messages": [
    {"role": "system", "content": "당신은 친절한 한국어 AI 비서입니다."},
    {"role": "user", "content": "Ollama가 뭔가요?"}
  ],
  "stream": false
}'
```

### Python에서 사용

```python
# pip install ollama
import ollama

# 간단한 텍스트 생성
response = ollama.generate(
    model='qwen2.5:14b',
    prompt='Python의 장점 3가지를 알려주세요.'
)
print(response['response'])

# 채팅 형식 (대화 이력 유지)
response = ollama.chat(
    model='deepseek-r1:14b',
    messages=[
        {'role': 'system', 'content': '당신은 시니어 파이썬 개발자입니다.'},
        {'role': 'user', 'content': 'FastAPI로 REST API를 만드는 기본 코드를 작성해줘.'}
    ]
)
print(response['message']['content'])

# 스트리밍 (실시간 출력)
stream = ollama.chat(
    model='qwen2.5:14b',
    messages=[{'role': 'user', 'content': '한국 역사에서 가장 중요한 사건 5가지는?'}],
    stream=True
)
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
```

### JavaScript/TypeScript에서 사용

```javascript
// npm install ollama
import { Ollama } from 'ollama';

const ollama = new Ollama({ host: 'http://localhost:11434' });

// 채팅 요청
const response = await ollama.chat({
  model: 'qwen2.5:14b',
  messages: [
    { role: 'user', content: '한국어로 인사해줘' }
  ]
});
console.log(response.message.content);

// 스트리밍
const stream = await ollama.chat({
  model: 'qwen2.5:14b',
  messages: [{ role: 'user', content: 'JavaScript의 async/await를 설명해줘' }],
  stream: true
});
for await (const chunk of stream) {
  process.stdout.write(chunk.message.content);
}
```

### OpenAI 호환 API

Ollama는 OpenAI API 형식도 지원합니다. 기존에 OpenAI API를 사용하는 코드를 최소한의 변경으로 Ollama로 전환할 수 있습니다.

```python
# pip install openai
from openai import OpenAI

# Ollama를 OpenAI 클라이언트로 사용
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'  # 아무 값이나 가능
)

response = client.chat.completions.create(
    model='deepseek-r1:14b',
    messages=[
        {'role': 'user', 'content': 'Ollama의 장점을 설명해줘'}
    ]
)
print(response.choices[0].message.content)
```

이 방법을 사용하면, 기존에 OpenAI API로 작성된 프로젝트를 **코드 한 줄 변경**으로 로컬 LLM으로 전환할 수 있어 매우 유용합니다.

---

## 8. Ollama vs ChatGPT/Claude 비교: 언제 어떤 걸 쓸까

솔직히 말하면, 로컬 LLM이 모든 면에서 클라우드 AI를 이기는 것은 아닙니다. 각각 장단점이 뚜렷하므로, 상황에 맞게 사용하는 게 현명합니다.

### 종합 비교표

| 항목 | Ollama (로컬) | ChatGPT Plus | Claude Pro |
|------|-------------|-------------|-----------|
| **월 비용** | 무료 (전기세만) | $20/월 | $20/월 |
| **API 비용** | 무료 | 토큰당 과금 | 토큰당 과금 |
| **프라이버시** | 완벽 (로컬 처리) | 서버 전송 | 서버 전송 |
| **오프라인 사용** | 가능 | 불가 | 불가 |
| **최고 성능 (최신 문제)** | 보통~좋음 | 매우 좋음 | 매우 좋음 |
| **한국어 품질** | 좋음 (모델에 따라) | 매우 좋음 | 매우 좋음 |
| **긴 문서 처리** | 좋음 (HW에 따라) | 매우 좋음 (128K) | 매우 좋음 (200K) |
| **이미지 이해** | 제한적 | 매우 좋음 | 매우 좋음 |
| **코드 생성** | 좋음~매우 좋음 | 매우 좋음 | 매우 좋음 |
| **커스터마이징** | 완전 자유 | 제한적 | 제한적 |
| **속도 (응답 시작)** | HW에 따라 다름 | 빠름 | 빠름 |
| **초기 설정** | 필요 | 불필요 | 불필요 |
| **최신 정보** | 학습 시점까지 | 웹 검색 가능 | 웹 검색 가능 |

### 이럴 때 Ollama를 쓰세요

- **민감한 데이터 처리**: 회사 코드, 고객 정보, 의료 기록 등을 다룰 때
- **대량 반복 작업**: 수백 개의 이메일 분류, 대량 번역, 데이터 처리 등 API 비용이 부담되는 작업
- **오프라인 환경**: 인터넷이 안 되는 환경에서 AI가 필요할 때
- **학습/실험 목적**: AI 모델의 동작을 이해하고, 프롬프트 엔지니어링을 연습할 때
- **개발 및 테스트**: AI 기능을 개발할 때 무제한으로 테스트하고 싶을 때
- **비용 절약**: 월 구독료 없이 AI를 자유롭게 쓰고 싶을 때

### 이럴 때 ChatGPT/Claude를 쓰세요

- **최고 품질이 필요한 작업**: 중요한 보고서, 논문 교정, 복잡한 분석 등
- **최신 정보가 필요할 때**: 웹 검색이 통합된 클라우드 AI가 유리
- **이미지 분석**: 복잡한 이미지 이해는 아직 클라우드 AI가 앞섬
- **매우 긴 대화**: 200K 토큰 컨텍스트가 필요한 경우
- **설정 없이 바로 사용**: 하드웨어 걱정 없이 즉시 사용하고 싶을 때

### 하이브리드 전략 (가장 추천)

가장 현명한 방법은 **두 가지를 병행**하는 것입니다.

1. **일상적인 질문, 코딩 보조, 번역** → Ollama (무료)
2. **중요한 작업, 최신 정보 필요** → ChatGPT 또는 Claude (유료)
3. **민감한 데이터** → 무조건 Ollama

이렇게 하면 클라우드 AI의 무료 티어만으로도 충분하거나, 유료 구독의 사용량을 크게 줄일 수 있습니다.

---

## 9. 트러블슈팅 FAQ

### Q1: "Error: model not found" 에러가 나요

```bash
# 사용 가능한 모델 목록 확인
ollama list

# 모델 이름을 정확히 입력했는지 확인 (대소문자 구분)
# 잘못된 예: ollama run DeepSeek-R1
# 올바른 예: ollama run deepseek-r1:14b

# 모델을 먼저 다운로드
ollama pull deepseek-r1:14b
```

### Q2: GPU를 인식하지 못해요 (CPU로만 실행돼요)

**NVIDIA GPU:**

```bash
# NVIDIA 드라이버 확인
nvidia-smi

# CUDA 버전 확인 (11.7 이상 필요)
nvcc --version

# 드라이버가 없거나 오래되었다면 업데이트
# Ubuntu:
sudo apt update && sudo apt install nvidia-driver-550

# Ollama 재시작
sudo systemctl restart ollama
```

**AMD GPU:**

```bash
# ROCm이 설치되어 있는지 확인
rocminfo

# ROCm이 없다면 설치 (Ubuntu)
# https://rocm.docs.amd.com 참고
```

**Apple Silicon (M1/M2/M3/M4):**

Metal GPU 가속이 자동으로 활성화됩니다. 인식 안 될 경우 Ollama를 최신 버전으로 업데이트하세요.

### Q3: 메모리(RAM/VRAM) 부족 에러가 나요

```bash
# 현재 실행 중인 모델 확인 및 종료
ollama ps
ollama stop <model_name>

# 더 작은 모델 사용
# 14B 대신 7B, 7B 대신 3B

# 양자화 수준이 낮은 버전 사용
ollama run qwen2.5:7b-q4_0    # Q4 양자화 (메모리 절약)

# GPU 메모리 할당 조정 (일부만 GPU 사용)
OLLAMA_NUM_GPU=20 ollama run deepseek-r1:14b
# 20개 레이어만 GPU에 할당, 나머지는 CPU
```

### Q4: 응답 속도가 너무 느려요

```bash
# 1. 더 작은 모델 사용
ollama run qwen2.5:7b    # 14B 대신 7B

# 2. 컨텍스트 길이 줄이기 (기본값은 모델마다 다름)
ollama run qwen2.5:7b --num-ctx 2048

# 3. GPU 사용 확인
ollama ps    # GPU 열에 값이 있는지 확인

# 4. 다른 프로그램의 GPU 사용량 확인
nvidia-smi   # NVIDIA GPU
```

### Q5: Ollama 서버에 외부에서 접속하고 싶어요

```bash
# 기본적으로 localhost(127.0.0.1)만 허용
# 외부 접속 허용하려면 환경 변수 설정

# Linux (systemd)
sudo systemctl edit ollama
# 아래 내용 추가:
# [Service]
# Environment="OLLAMA_HOST=0.0.0.0"

sudo systemctl restart ollama

# Mac/Windows
# 환경 변수 OLLAMA_HOST=0.0.0.0 설정 후 재시작
```

> **보안 주의**: 외부 접속을 허용할 때는 반드시 방화벽을 설정하거나 VPN을 통해서만 접속하도록 하세요.

### Q6: 한국어 응답이 깨지거나 이상해요

```bash
# 1. 한국어에 강한 모델 선택
ollama run qwen2.5:14b       # 한국어 최적
ollama run deepseek-r1:14b   # 한국어 우수

# 2. 시스템 프롬프트에서 한국어 지시
ollama run qwen2.5:14b --system "당신은 한국어만 사용하는 AI 비서입니다.
모든 응답을 자연스러운 한국어로 해주세요."

# 3. temperature 조절 (낮을수록 일관적)
# Modelfile에서 PARAMETER temperature 0.5 설정
```

### Q7: 모델이 너무 많은 디스크 공간을 차지해요

```bash
# 모델별 크기 확인
ollama list

# 사용하지 않는 모델 삭제
ollama rm llama3
ollama rm mistral

# 모델 저장 경로 확인
# Linux: ~/.ollama/models
# Mac: ~/.ollama/models
# Windows: C:\Users\<사용자>\.ollama\models

# 저장 경로 변경 (필요시)
# 환경 변수: OLLAMA_MODELS=/path/to/models
```

---

## 마무리: 지금 바로 시작하세요

2026년은 로컬 LLM의 황금기라고 해도 과언이 아닙니다. DeepSeek-R1이 증명했듯이, 오픈소스 모델도 충분히 실용적인 수준에 도달했습니다. Ollama 덕분에 복잡한 설정 없이도 누구나 AI를 내 컴퓨터에서 실행할 수 있게 되었습니다.

지금 당장 시작하는 방법은 간단합니다.

```bash
# 1. Ollama 설치 (30초)
curl -fsSL https://ollama.com/install.sh | sh

# 2. 첫 모델 실행 (다운로드 포함 5분)
ollama run qwen2.5:7b

# 3. 한국어로 대화 시작
>>> 안녕하세요! 무엇을 도와드릴까요?
```

**세 줄의 명령어**만 입력하면, 여러분의 컴퓨터에서 AI가 돌아갑니다. 무료로, 프라이버시를 지키면서, 무제한으로 말이죠.

로컬 LLM의 세계에 오신 것을 환영합니다.
