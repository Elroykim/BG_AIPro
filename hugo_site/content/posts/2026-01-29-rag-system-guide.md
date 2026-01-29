---
title: "RAG 시스템 구축 입문: 나만의 AI 지식 베이스 만들기 (Python 실전 가이드)"
date: 2026-01-29
description: "RAG(검색 증강 생성)의 원리를 이해하고, Python으로 한국어 문서 기반 AI 지식 베이스를 직접 구축하는 실전 가이드입니다."
categories: [AI]
tags: [RAG, 벡터 데이터베이스, LangChain, 임베딩, AI 개발]
keywords: [RAG 시스템 구축, RAG 구현 방법, LangChain RAG 한국어, 벡터 데이터베이스 사용법, RAG 한국어 임베딩]
draft: false
slug: rag-system-build-guide-python-2026
---

ChatGPT에게 "우리 회사 내부 문서에서 답을 찾아줘"라고 부탁하면 어떻게 될까요? 아마 그럴듯하지만 **완전히 틀린 답**을 자신 있게 내놓을 것입니다. 이것이 바로 LLM(대규모 언어 모델)의 고질적 문제인 **환각(Hallucination)**입니다. RAG(Retrieval-Augmented Generation)는 이 문제를 정면으로 해결하는 기술이며, 2026년 현재 기업용 AI 애플리케이션의 사실상 표준 아키텍처가 되었습니다.

이 글에서는 RAG의 원리부터 시작해 Python으로 한국어 문서 기반 AI 지식 베이스를 처음부터 끝까지 직접 구축하는 방법을 다룹니다. 복사-붙여넣기로 바로 실행할 수 있는 전체 코드를 포함하고 있으니, 끝까지 따라오시면 여러분만의 RAG 시스템을 완성할 수 있습니다.

---

## RAG란 무엇인가?

**RAG(Retrieval-Augmented Generation, 검색 증강 생성)**는 LLM이 답변을 생성하기 전에, 외부 지식 저장소에서 관련 정보를 먼저 검색(Retrieve)한 뒤 그 정보를 컨텍스트로 활용하여 응답을 생성(Generate)하는 기술입니다.

### LLM의 환각 문제

일반적인 LLM은 학습 데이터에 포함된 정보만을 기반으로 답변합니다. 이로 인해 다음과 같은 문제가 발생합니다.

- **정보의 시점 제한**: 학습 데이터 이후의 정보를 알 수 없습니다.
- **조직 내부 정보 부재**: 회사 내부 문서, 사내 규정 등을 전혀 모릅니다.
- **환각(Hallucination)**: 모르는 내용도 그럴듯하게 지어내서 답변합니다.
- **출처 불분명**: 어디서 그 정보를 가져왔는지 확인할 수 없습니다.

### RAG가 해결하는 방식

RAG는 "오픈북 시험"과 같습니다. 학생(LLM)이 시험을 볼 때, 기억에만 의존하는 것이 아니라 **교과서(외부 문서)를 참고하면서** 답을 작성하는 것입니다. 이를 통해 다음을 달성합니다.

- **사실 기반 답변**: 실제 문서에 근거한 정확한 답변을 생성합니다.
- **최신 정보 반영**: 문서를 업데이트하면 즉시 반영됩니다.
- **출처 제공**: 어떤 문서의 어느 부분을 참고했는지 명시할 수 있습니다.
- **비용 효율성**: 전체 모델을 파인튜닝하는 것보다 훨씬 저렴합니다.

---

## RAG 아키텍처 이해하기

RAG 시스템은 크게 두 단계로 나뉩니다. 문서를 미리 처리해두는 **인덱싱(Indexing) 단계**와, 사용자 질문에 답변하는 **질의(Query) 단계**입니다.

### 전체 파이프라인 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                    [1] 인덱싱 단계 (오프라인)                      │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────┐  │
│  │ 문서 로딩  │──▶│  청킹     │──▶│  임베딩   │──▶│ 벡터DB 저장  │  │
│  │ (PDF 등) │   │ (분할)    │   │ (벡터화)  │   │ (ChromaDB)  │  │
│  └──────────┘   └──────────┘   └──────────┘   └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    [2] 질의 단계 (온라인)                         │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────┐  │
│  │ 사용자    │──▶│ 질문 임베딩│──▶│ 유사도   │──▶│  관련 문서   │  │
│  │ 질문 입력 │   │ (벡터화)  │   │ 검색     │   │  Top-K 반환  │  │
│  └──────────┘   └──────────┘   └──────────┘   └──────┬──────┘  │
│                                                       │         │
│  ┌──────────┐   ┌───────────────────────────────┐     │         │
│  │ 최종 답변 │◀──│ LLM (질문 + 검색된 문서 컨텍스트) │◀────┘         │
│  │ 출력     │   │ → 답변 생성                    │              │
│  └──────────┘   └───────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### 각 단계 상세 설명

**1단계 - 문서 로딩(Document Loading)**: PDF, Word, 텍스트 파일, 웹 페이지 등 다양한 형식의 원본 문서를 텍스트로 변환합니다. LangChain의 Document Loader를 사용하면 수십 가지 포맷을 손쉽게 처리할 수 있습니다.

**2단계 - 청킹(Chunking)**: 로딩된 문서를 일정 크기의 텍스트 조각(청크)으로 분할합니다. LLM의 컨텍스트 윈도우 제한과 검색 정밀도를 고려하여 적절한 크기로 나누는 것이 핵심입니다.

**3단계 - 임베딩(Embedding)**: 각 청크를 고차원 벡터(숫자 배열)로 변환합니다. 의미적으로 유사한 텍스트는 벡터 공간에서 가까운 위치에 놓이게 됩니다.

**4단계 - 벡터DB 저장**: 생성된 벡터들을 벡터 데이터베이스에 저장합니다. ChromaDB, Pinecone, Weaviate, Milvus 등 다양한 옵션이 있습니다.

**5단계 - 유사도 검색(Retrieval)**: 사용자 질문도 동일한 임베딩 모델로 벡터화한 후, 벡터DB에서 코사인 유사도 등을 기준으로 가장 관련성 높은 청크를 찾습니다.

**6단계 - LLM 응답 생성(Generation)**: 검색된 청크들을 프롬프트에 포함시켜 LLM에 전달하면, LLM이 해당 정보를 기반으로 답변을 생성합니다.

---

## 한국어 RAG의 특수성

한국어로 RAG 시스템을 구축할 때는 영어와는 다른 고려 사항이 존재합니다. 한국어의 언어적 특성을 이해하고 이에 맞는 전략을 선택하는 것이 성능에 큰 영향을 미칩니다.

### 한국어 청킹의 어려움

영어는 단어 사이에 공백이 명확하고, 문장 구조가 비교적 단순합니다. 반면 한국어는 다음과 같은 특성이 있습니다.

- **교착어**: "먹었습니다", "먹겠습니다", "먹히다" 등 하나의 어근에 여러 접사가 붙어 의미가 변합니다.
- **조사 결합**: "사과를", "사과가", "사과에서" 등 조사에 따라 같은 단어도 다르게 인식될 수 있습니다.
- **띄어쓰기 불규칙**: 한국어 문서에서는 띄어쓰기 오류가 빈번하며, 이는 단순 공백 기반 분할의 품질을 떨어뜨립니다.

### 형태소 기반 청킹 전략

한국어 텍스트를 더 효과적으로 분할하려면 형태소 분석기를 활용하는 것이 좋습니다.

```python
from konlpy.tag import Mecab

mecab = Mecab()

text = "인공지능 기술이 빠르게 발전하고 있습니다."
morphs = mecab.morphs(text)
print(morphs)
# ['인공', '지능', '기술', '이', '빠르', '게', '발전', '하', '고', '있', '습니다', '.']
```

하지만 실무에서는 형태소 단위까지 분할할 필요는 없습니다. 대부분의 경우 `RecursiveCharacterTextSplitter`에 적절한 구분자를 설정하는 것으로 충분합니다. 한국어에 적합한 구분자 우선순위는 다음과 같습니다.

```python
korean_separators = ["\n\n", "\n", ".", "。", "!", "?", ";", ",", " "]
```

### 한국어 임베딩 모델의 중요성

영어 전용 임베딩 모델을 한국어에 사용하면 의미 파악 성능이 크게 떨어집니다. 반드시 한국어를 지원하는 다국어(multilingual) 모델 또는 한국어 특화 모델을 선택해야 합니다. 이에 대해서는 아래 임베딩 모델 비교 섹션에서 자세히 다룹니다.

---

## 실전: Python으로 RAG 시스템 만들기

이제 실제로 동작하는 RAG 시스템을 구축해 보겠습니다. LangChain, ChromaDB, 그리고 Claude API를 사용합니다.

### 환경 설정

먼저 필요한 패키지를 설치합니다.

```bash
pip install langchain langchain-community langchain-anthropic \
            chromadb sentence-transformers \
            pypdf tiktoken
```

환경 변수에 Anthropic API 키를 설정합니다.

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 전체 RAG 시스템 코드

아래는 PDF 문서를 로딩하여 ChromaDB에 저장하고, 사용자 질문에 답변하는 전체 코드입니다.

```python
"""
RAG 시스템 구축 - 한국어 문서 기반 AI 지식 베이스
LangChain + ChromaDB + Claude API
"""

import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


# ──────────────────────────────────────────────
# 1. 문서 로딩
# ──────────────────────────────────────────────
def load_documents(pdf_directory: str):
    """지정된 디렉토리에서 PDF 문서를 로딩합니다."""
    loader = DirectoryLoader(
        pdf_directory,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )
    documents = loader.load()
    print(f"총 {len(documents)}개의 페이지를 로딩했습니다.")
    return documents


# ──────────────────────────────────────────────
# 2. 텍스트 분할 (청킹)
# ──────────────────────────────────────────────
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """문서를 한국어에 적합한 방식으로 청크 단위로 분할합니다."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "。", "!", "?", ";", ",", " ", ""],
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"총 {len(chunks)}개의 청크로 분할했습니다.")
    return chunks


# ──────────────────────────────────────────────
# 3. 임베딩 모델 초기화
# ──────────────────────────────────────────────
def get_embedding_model(model_name="intfloat/multilingual-e5-large"):
    """한국어를 지원하는 임베딩 모델을 초기화합니다."""
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},  # GPU 사용 시 "cuda"
        encode_kwargs={"normalize_embeddings": True},
    )
    print(f"임베딩 모델 로드 완료: {model_name}")
    return embeddings


# ──────────────────────────────────────────────
# 4. 벡터 데이터베이스 생성 및 저장
# ──────────────────────────────────────────────
def create_vectorstore(chunks, embeddings, persist_directory="./chroma_db"):
    """청크를 벡터화하여 ChromaDB에 저장합니다."""
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="korean_docs",
    )
    print(f"벡터 DB 저장 완료: {persist_directory}")
    return vectorstore


def load_vectorstore(embeddings, persist_directory="./chroma_db"):
    """기존에 저장된 벡터 DB를 로드합니다."""
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="korean_docs",
    )
    print("기존 벡터 DB를 로드했습니다.")
    return vectorstore


# ──────────────────────────────────────────────
# 5. RAG 체인 구성
# ──────────────────────────────────────────────
def create_rag_chain(vectorstore):
    """검색 + LLM 응답 생성 체인을 구성합니다."""

    # Claude LLM 초기화
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0,
        max_tokens=2048,
    )

    # 한국어 전용 프롬프트 템플릿
    prompt_template = """당신은 주어진 문서를 기반으로 질문에 정확하게 답변하는 AI 어시스턴트입니다.
아래 제공된 컨텍스트(context)만을 사용하여 질문에 답변하세요.

규칙:
1. 컨텍스트에 없는 정보는 절대 지어내지 마세요.
2. 답변할 수 없는 경우 "제공된 문서에서 해당 정보를 찾을 수 없습니다."라고 답하세요.
3. 답변 시 관련 문서의 내용을 인용하여 근거를 제시하세요.
4. 한국어로 답변하세요.

컨텍스트:
{context}

질문: {question}

답변:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    # RetrievalQA 체인 구성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4},  # 상위 4개 문서 검색
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )

    return qa_chain


# ──────────────────────────────────────────────
# 6. 메인 실행
# ──────────────────────────────────────────────
def main():
    # 설정
    PDF_DIR = "./documents"       # PDF 파일이 있는 디렉토리
    DB_DIR = "./chroma_db"        # 벡터 DB 저장 경로
    EMBEDDING_MODEL = "intfloat/multilingual-e5-large"

    # 임베딩 모델 로드
    embeddings = get_embedding_model(EMBEDDING_MODEL)

    # 벡터 DB가 이미 존재하면 로드, 없으면 새로 생성
    if os.path.exists(DB_DIR):
        vectorstore = load_vectorstore(embeddings, DB_DIR)
    else:
        documents = load_documents(PDF_DIR)
        chunks = split_documents(documents, chunk_size=500, chunk_overlap=50)
        vectorstore = create_vectorstore(chunks, embeddings, DB_DIR)

    # RAG 체인 구성
    qa_chain = create_rag_chain(vectorstore)

    # 대화형 질의응답 루프
    print("\n" + "=" * 50)
    print("RAG 시스템이 준비되었습니다. 질문을 입력하세요.")
    print("종료하려면 'quit'를 입력하세요.")
    print("=" * 50 + "\n")

    while True:
        question = input("질문: ").strip()
        if question.lower() in ["quit", "exit", "종료"]:
            print("시스템을 종료합니다.")
            break
        if not question:
            continue

        # 질문 처리
        result = qa_chain.invoke({"query": question})

        # 답변 출력
        print(f"\n답변: {result['result']}\n")

        # 참고 문서 출력
        print("--- 참고 문서 ---")
        for i, doc in enumerate(result["source_documents"], 1):
            source = doc.metadata.get("source", "알 수 없음")
            page = doc.metadata.get("page", "N/A")
            print(f"[{i}] 출처: {source} (페이지: {page})")
            print(f"    내용: {doc.page_content[:150]}...\n")


if __name__ == "__main__":
    main()
```

### 코드 실행 결과 예시

```
총 45개의 페이지를 로딩했습니다.
총 128개의 청크로 분할했습니다.
임베딩 모델 로드 완료: intfloat/multilingual-e5-large
벡터 DB 저장 완료: ./chroma_db

==================================================
RAG 시스템이 준비되었습니다. 질문을 입력하세요.
종료하려면 'quit'를 입력하세요.
==================================================

질문: 연차 휴가는 며칠인가요?

답변: 제공된 문서에 따르면, 1년 이상 근속한 직원에게는 연간 15일의
유급 연차 휴가가 부여됩니다. 3년 이상 근속 시 매 2년마다 1일이
추가되며, 최대 25일까지 부여됩니다.

--- 참고 문서 ---
[1] 출처: documents/취업규칙.pdf (페이지: 12)
    내용: 제20조 (연차 유급휴가) ① 1년간 80퍼센트 이상 출근한 근로자에게
    15일의 유급휴가를 부여한다...
```

---

## 한국어 임베딩 모델 비교

RAG 시스템의 검색 품질은 임베딩 모델의 성능에 직접적으로 좌우됩니다. 한국어를 지원하는 주요 임베딩 모델을 비교합니다.

### 주요 모델 비교표

| 모델명 | 개발사 | 차원 수 | 한국어 성능 | 최대 토큰 | 특징 |
|--------|--------|---------|------------|----------|------|
| `intfloat/multilingual-e5-large` | Microsoft | 1024 | 우수 | 512 | 다국어 범용, 안정적 성능 |
| `BAAI/bge-m3` | BAAI | 1024 | 매우 우수 | 8192 | 긴 문서 처리 가능, Dense+Sparse+ColBERT |
| `BM-K/KoSimCSE-roberta` | 한국 연구팀 | 768 | 우수 | 512 | 한국어 특화 학습, 경량 |
| `jhgan/ko-sroberta-multitask` | 한국 연구팀 | 768 | 양호 | 512 | 다양한 한국어 태스크 학습 |
| `Upstage/solar-embedding-1-large` | Upstage | 4096 | 매우 우수 | 4096 | 상용 API, 최상급 한국어 성능 |
| `openai/text-embedding-3-large` | OpenAI | 3072 | 우수 | 8191 | 상용 API, 안정적 |

### 모델 선택 가이드

**무료 + 로컬 실행이 필요한 경우**:
- 일반적 용도라면 `intfloat/multilingual-e5-large`를 추천합니다. 한국어 성능이 안정적이고 커뮤니티 지원이 풍부합니다.
- 긴 문서를 처리해야 한다면 `BAAI/bge-m3`이 최선입니다. 최대 8192 토큰을 지원하여 긴 청크도 처리할 수 있습니다.

**한국어 성능 최우선인 경우**:
- `BM-K/KoSimCSE-roberta`는 한국어 문장 유사도 태스크에서 뛰어난 성능을 보입니다.

**상용 서비스 구축 시**:
- `Upstage/solar-embedding-1-large`는 2026년 현재 한국어 임베딩 벤치마크에서 최상위권 성능을 기록하고 있습니다. API 비용이 발생하지만 품질이 우수합니다.

### 임베딩 모델 교체 방법

위 코드에서 임베딩 모델을 교체하는 것은 매우 간단합니다.

```python
# multilingual-e5-large (기본)
embeddings = get_embedding_model("intfloat/multilingual-e5-large")

# BGE-M3로 교체
embeddings = get_embedding_model("BAAI/bge-m3")

# 한국어 특화 KoSimCSE로 교체
embeddings = get_embedding_model("BM-K/KoSimCSE-roberta")
```

> **주의**: 임베딩 모델을 변경하면 기존 벡터 DB와 호환되지 않습니다. 모델을 변경할 경우 반드시 벡터 DB를 새로 생성해야 합니다.

---

## RAG 성능 개선 팁

기본적인 RAG 파이프라인을 구축했다면, 이제 성능을 끌어올릴 차례입니다. 아래는 실무에서 검증된 성능 개선 기법들입니다.

### 1. 청크 크기와 오버랩 최적화

청크 크기는 RAG 성능에 가장 직접적인 영향을 미치는 하이퍼파라미터입니다.

```
청크가 너무 작을 때 (100자):
┌─────────────────────┐
│ 문맥이 부족하여       │ → 검색은 정확하지만 LLM이
│ 의미 파악 어려움       │   답변을 구성하기 어려움
└─────────────────────┘

청크가 너무 클 때 (2000자):
┌─────────────────────┐
│ 불필요한 정보가        │ → 검색 정밀도가 떨어지고
│ 너무 많이 포함됨       │   노이즈가 증가함
└─────────────────────┘

적절한 청크 크기 (300~800자):
┌─────────────────────┐
│ 하나의 개념/단락을     │ → 검색 정밀도와 문맥 보존
│ 포함하는 적절한 크기    │   사이의 균형
└─────────────────────┘
```

**실전 권장값 (한국어 기준)**:

| 문서 유형 | 청크 크기 | 오버랩 | 이유 |
|----------|----------|--------|------|
| 기술 문서 | 500~800자 | 50~100자 | 개념별로 충분한 문맥 포함 |
| 법률/규정 | 300~500자 | 80~100자 | 조항별 정밀한 검색 필요 |
| 일반 문서 | 400~600자 | 50자 | 단락 단위의 자연스러운 분할 |
| FAQ | 200~400자 | 30자 | 질문-답변 쌍이 하나의 청크 |

오버랩(overlap)은 인접 청크 사이에 겹치는 부분을 두어 문맥이 끊기는 것을 방지합니다. 일반적으로 청크 크기의 10~20% 정도가 적절합니다.

### 2. 리랭킹(Re-ranking)

초기 벡터 검색으로 후보 문서를 넓게 가져온 후, 더 정교한 모델로 관련성을 재평가하는 기법입니다.

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker

# Cross-encoder 리랭커 설정
cross_encoder = HuggingFaceCrossEncoder(
    model_name="BAAI/bge-reranker-v2-m3"
)
reranker = CrossEncoderReranker(
    model=cross_encoder,
    top_n=3  # 리랭킹 후 상위 3개만 사용
)

# 압축 리트리버: 먼저 10개 검색 → 리랭킹 → 상위 3개 반환
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=vectorstore.as_retriever(
        search_kwargs={"k": 10}
    ),
)
```

리랭킹은 검색 정밀도를 크게 향상시킵니다. 특히 한국어처럼 동음이의어가 많고 문맥에 따라 의미가 달라지는 언어에서 효과가 큽니다.

### 3. HyDE (Hypothetical Document Embeddings)

사용자의 짧은 질문만으로는 관련 문서를 정확히 검색하기 어려울 수 있습니다. HyDE는 LLM에게 먼저 **가상의 답변 문서**를 생성하게 한 후, 그 가상 문서를 임베딩하여 검색하는 기법입니다.

```python
from langchain.chains import HypotheticalDocumentEmbedder, LLMChain
from langchain.prompts import PromptTemplate

# HyDE 프롬프트
hyde_prompt = PromptTemplate(
    input_variables=["question"],
    template="""다음 질문에 대해 전문적인 한국어 문서에서 발췌한 것처럼
상세한 답변 문단을 작성하세요.

질문: {question}

답변 문단:""",
)

# HyDE 임베딩 생성
hyde_embeddings = HypotheticalDocumentEmbedder.from_llm(
    llm=ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0),
    base_embeddings=embeddings,
    prompt_key="question",
)
```

HyDE의 효과를 시각적으로 표현하면 다음과 같습니다.

```
[일반 검색]
  "연차 며칠?" ──(임베딩)──▶ 짧은 질문 벡터 ──(검색)──▶ 관련도 중간

[HyDE 검색]
  "연차 며칠?" ──(LLM)──▶ "근로기준법에 따르면 1년 이상
   근속한 근로자에게는 15일의 유급 연차 휴가가 부여되며..."
   ──(임베딩)──▶ 풍부한 문맥의 벡터 ──(검색)──▶ 관련도 높음
```

### 4. 메타데이터 필터링

벡터 검색만으로는 부족할 수 있습니다. 문서에 메타데이터(출처, 날짜, 부서, 카테고리 등)를 태깅하고, 검색 시 필터링을 적용하면 정밀도가 향상됩니다.

```python
# 문서 로딩 시 메타데이터 추가
for doc in documents:
    doc.metadata["department"] = "인사팀"
    doc.metadata["doc_type"] = "규정"
    doc.metadata["year"] = 2026

# 검색 시 메타데이터 필터링
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {"department": "인사팀"},  # 인사팀 문서만 검색
    }
)
```

### 5. 멀티 쿼리 리트리버

하나의 질문을 여러 관점에서 재구성하여 검색 범위를 넓히는 기법입니다.

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    llm=ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.3),
)

# "연차 휴가 며칠?" 이라는 질문이 자동으로 다음처럼 확장됩니다:
# → "연차 유급 휴가 일수는 얼마인가요?"
# → "직원의 연간 휴가 일수 규정은 무엇인가요?"
# → "근로자 연차 휴가 부여 기준은 어떻게 되나요?"
```

---

## 흔한 실패 패턴과 해결법

RAG 시스템을 구축하다 보면 반복적으로 마주치는 문제들이 있습니다. 미리 알아두면 디버깅 시간을 크게 줄일 수 있습니다.

### 실패 패턴 1: "답을 찾을 수 없다"고 하는데 문서에는 답이 있는 경우

**증상**: 분명히 관련 문서가 있는데 "해당 정보를 찾을 수 없습니다"라고 답변합니다.

**원인과 해결법**:

```
원인 1: 질문과 문서의 표현 차이
┌──────────────────────────────────────────────┐
│ 질문: "월급날이 언제예요?"                       │
│ 문서: "임금은 매월 25일에 지급한다"               │
│ → "월급"과 "임금"이 다른 벡터로 매핑됨             │
│                                              │
│ 해결: HyDE 또는 멀티 쿼리 리트리버 적용           │
└──────────────────────────────────────────────┘

원인 2: 청크 크기가 너무 작아 문맥 소실
┌──────────────────────────────────────────────┐
│ 원본: "제15조 (임금) ① 임금은 매월 25일에        │
│        지급한다. ② 25일이 휴일인 경우 전일..."    │
│ 청크1: "제15조 (임금) ① 임금은"                 │
│ 청크2: "매월 25일에 지급한다."                   │
│ → 핵심 정보가 분리됨                            │
│                                              │
│ 해결: 청크 크기 증가 또는 오버랩 확대              │
└──────────────────────────────────────────────┘

원인 3: 검색 결과 개수(k)가 너무 적음
┌──────────────────────────────────────────────┐
│ k=2로 설정했는데, 관련 문서가 3번째에 위치         │
│                                              │
│ 해결: k 값을 늘리고 리랭킹 적용                   │
└──────────────────────────────────────────────┘
```

### 실패 패턴 2: 엉뚱한 문서를 검색하는 경우

**증상**: 질문과 전혀 관련 없는 문서가 검색됩니다.

**원인과 해결법**:

- **임베딩 모델 품질 부족**: 영어 전용 모델을 사용하고 있지 않은지 확인하세요. 한국어 지원 모델로 교체해야 합니다.
- **문서 전처리 부족**: 머리글/바닥글, 목차, 페이지 번호 등이 노이즈로 작용할 수 있습니다. 로딩 후 불필요한 텍스트를 정리하세요.
- **도메인 불일치**: 범용 임베딩 모델이 특정 도메인(의학, 법률 등)에서 약할 수 있습니다. 도메인 특화 파인튜닝을 고려하세요.

```python
# 문서 전처리: 노이즈 제거
import re

def clean_document(text: str) -> str:
    """문서 텍스트에서 노이즈를 제거합니다."""
    # 페이지 번호 제거
    text = re.sub(r'\n\s*-?\s*\d+\s*-?\s*\n', '\n', text)
    # 반복되는 머리글/바닥글 패턴 제거
    text = re.sub(r'(주식회사 ○○○|기밀문서)\s*\n', '', text)
    # 과도한 공백 정리
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()
```

### 실패 패턴 3: LLM이 검색된 문서를 무시하고 자체 지식으로 답변

**증상**: 검색된 문서에 명확한 답이 있는데도, LLM이 자체 학습 데이터를 기반으로 다른 답변을 생성합니다.

**해결법**: 프롬프트를 강화하여 LLM이 반드시 주어진 컨텍스트만 사용하도록 유도합니다.

```python
strict_prompt = """당신은 제공된 문서만을 기반으로 답변하는 AI입니다.

절대적 규칙:
- 아래 '컨텍스트'에 포함된 정보만 사용하세요.
- 컨텍스트에 없는 내용은 "문서에서 찾을 수 없습니다"라고 답하세요.
- 당신의 사전 학습 지식을 사용하지 마세요.
- 답변 시 반드시 근거가 되는 문서 내용을 인용하세요.

컨텍스트:
{context}

질문: {question}

답변 (반드시 컨텍스트 기반으로):"""
```

### 실패 패턴 4: 응답 속도가 너무 느린 경우

**증상**: 질문에서 답변까지 10초 이상 걸립니다.

**해결법 체크리스트**:

| 병목 지점 | 확인 방법 | 해결법 |
|----------|----------|--------|
| 임베딩 계산 | 질문 임베딩 시간 측정 | GPU 사용 또는 경량 모델 교체 |
| 벡터 검색 | 검색 시간 측정 | 인덱스 최적화(HNSW), k 값 조정 |
| LLM 응답 | API 호출 시간 측정 | 스트리밍 응답, 경량 모델 사용 |
| 문서 로딩 | 초기 로딩 시간 | 벡터 DB 사전 구축 후 로드만 수행 |

```python
import time

# 각 단계별 소요 시간 측정
start = time.time()
query_embedding = embeddings.embed_query(question)
print(f"임베딩 시간: {time.time() - start:.2f}초")

start = time.time()
docs = vectorstore.similarity_search(question, k=4)
print(f"검색 시간: {time.time() - start:.2f}초")

start = time.time()
result = qa_chain.invoke({"query": question})
print(f"LLM 응답 시간: {time.time() - start:.2f}초")
```

### 실패 패턴 5: 한국어 PDF 인코딩 문제

**증상**: PDF에서 추출한 텍스트가 깨져서 나옵니다.

**해결법**: PyPDFLoader 대신 다른 로더를 시도하세요.

```python
# 방법 1: PyMuPDFLoader (더 나은 한국어 지원)
from langchain_community.document_loaders import PyMuPDFLoader
loader = PyMuPDFLoader("document.pdf")

# 방법 2: OCR 기반 (스캔 문서의 경우)
# pip install unstructured pdf2image pytesseract
from langchain_community.document_loaders import UnstructuredPDFLoader
loader = UnstructuredPDFLoader(
    "scanned_document.pdf",
    mode="elements",
    strategy="ocr_only",
    ocr_languages="kor",
)
```

---

## 마무리: RAG 시스템 구축 체크리스트

RAG 시스템을 구축할 때 다음 체크리스트를 참고하세요.

```
☐ 1. 문서 준비
   ├── 소스 문서 형식 확인 (PDF, TXT, DOCX 등)
   ├── 한국어 인코딩 검증
   └── 불필요한 노이즈(머리글, 바닥글) 정리 계획

☐ 2. 청킹 전략 결정
   ├── 문서 유형에 맞는 청크 크기 선택
   ├── 오버랩 비율 설정 (10~20%)
   └── 한국어 구분자 우선순위 설정

☐ 3. 임베딩 모델 선택
   ├── 한국어 지원 여부 확인
   ├── 로컬 실행 vs API 사용 결정
   └── 벤치마크 성능 비교

☐ 4. 벡터 DB 선택
   ├── 데이터 규모에 맞는 DB 선택
   ├── 메타데이터 필터링 필요 여부
   └── 영속성(persistence) 요구사항

☐ 5. 검색 최적화
   ├── 기본 유사도 검색으로 시작
   ├── 필요시 리랭킹 추가
   └── HyDE, 멀티 쿼리 등 고급 기법 검토

☐ 6. 프롬프트 엔지니어링
   ├── 컨텍스트 기반 답변 유도
   ├── 출처 인용 요구
   └── 답변 불가 시 처리 방법 명시

☐ 7. 평가 및 모니터링
   ├── 테스트 질문 세트 구축
   ├── 검색 정밀도/재현율 측정
   └── 답변 품질 정성 평가
```

RAG는 LLM을 실무에 적용하는 가장 실용적인 방법입니다. 이 글에서 제공한 코드를 기반으로 여러분의 데이터에 맞게 커스터마이징하며 경험을 쌓아 보시기 바랍니다. 작은 규모의 프로토타입부터 시작하여, 청킹 전략과 임베딩 모델을 실험하며 최적의 구성을 찾아가는 과정 자체가 RAG 엔지니어링의 핵심입니다.

다음 글에서는 프로덕션 환경에서의 RAG 운영 전략과 평가 프레임워크(RAGAS 등)에 대해 다루겠습니다.
