---
title: "오픈소스 LLM 비교: Llama 3 vs Mistral vs DeepSeek, 뭘 골라야 할까"
date: 2025-12-02
description: "Llama 3.2, Mistral, DeepSeek-R1 세 오픈소스 LLM을 한국어 성능, 속도, 리소스 사용량, 용도별로 비교합니다. 로컬에서 돌려본 실사용 후기와 벤치마크 기반 추천."
categories: [AI]
tags: [오픈소스 LLM, Llama, Mistral, DeepSeek, 로컬 AI]
keywords: [오픈소스 LLM 비교, Llama 3 한국어, DeepSeek R1 로컬, Mistral 한국어 성능, 로컬 LLM 추천]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: open-source-llm-comparison-llama-mistral-deepseek
---

로컬에서 LLM을 돌려보겠다고 마음먹으면 첫 번째 관문이 "모델 뭘 쓰지?"다. ChatGPT나 Claude는 선택지가 정해져 있지만, 오픈소스 세계에 들어오면 Llama, Mistral, DeepSeek, Qwen, Phi, Gemma... 모델이 너무 많아서 오히려 혼란스럽다. 나도 처음에는 이것저것 깔아보면서 시간을 꽤 썼는데, 결국 중요한 건 내 용도와 하드웨어에 맞는 모델을 고르는 것이었다. 오늘은 요즘 가장 많이 쓰이는 Llama 3.2, Mistral, DeepSeek-R1 세 모델을 직접 돌려보면서 비교한 결과를 정리한다.

---

## 1. 주요 모델 소개: 각각 뭐가 다른가

### Llama 3.2 (Meta)

Meta가 오픈소스로 공개한 Llama 시리즈의 최신작이다. 1B, 3B 경량 모델부터 11B, 90B 비전 모델까지 다양한 크기를 제공한다. 커뮤니티에서 가장 많이 사용되는 만큼 생태계가 넓고, 파인튜닝된 파생 모델도 많다.

- 제공 크기: 1B, 3B, 11B (Vision), 90B (Vision)
- 라이선스: Llama 3.2 Community License (상업적 사용 가능, 월 7억 MAU 초과 시 별도 허가 필요)
- 컨텍스트 윈도우: 128K 토큰
- 특이사항: 1B/3B는 모바일 디바이스에서도 구동 가능, 11B/90B는 이미지 입력 지원

### Mistral (Mistral AI)

프랑스 스타트업 Mistral AI가 개발한 모델로, 모델 크기 대비 성능이 좋다는 평가를 받는다. Mixtral이라는 MoE(Mixture of Experts) 아키텍처 모델도 있어서, 파라미터 대비 추론 비용이 효율적이다.

- 주요 모델: Mistral 7B, Mistral Small (24B), Mistral Nemo (12B), Mixtral 8x7B
- 라이선스: Apache 2.0 (Mistral 7B, Nemo) / 상업용 라이선스 (Large, Small)
- 컨텍스트 윈도우: 최대 128K 토큰 (Mistral Small 기준)
- 특이사항: 유럽 기반이라 다국어에 상대적으로 강함, function calling 지원

### DeepSeek-R1 (DeepSeek)

중국 AI 스타트업 DeepSeek이 개발한 추론 특화 모델이다. 이름에 R1이 붙은 만큼 수학, 코딩, 논리적 추론에서 특히 강하다. 2025년 초 공개됐을 때 GPT-4o급 성능을 오픈소스로 풀었다는 점에서 큰 반향을 일으켰다.

- 제공 크기: 1.5B, 7B, 8B, 14B, 32B, 70B, 671B
- 라이선스: MIT License (완전 오픈소스, 상업적 사용 자유)
- 컨텍스트 윈도우: 64K~128K 토큰 (크기별 상이)
- 특이사항: Chain-of-Thought(사고 과정) 표시 기능, 추론 과정을 투명하게 보여줌

---

## 2. 벤치마크 비교: 숫자로 보는 성능

벤치마크 수치는 참고용이다. 실제 체감 성능은 벤치마크와 다를 수 있지만, 객관적인 비교의 출발점으로는 유용하다.

### 주요 벤치마크 (7~8B 모델 기준)

| 벤치마크 | Llama 3.1 8B | Mistral 7B v0.3 | DeepSeek-R1 8B | 측정 항목 |
|----------|-------------|-----------------|---------------|----------|
| MMLU | 69.4 | 62.5 | 67.8 | 일반 지식 |
| HumanEval | 72.6 | 56.1 | 71.3 | 코딩 능력 |
| GSM8K | 84.5 | 52.2 | 88.1 | 수학 추론 |
| ARC-C | 83.4 | 78.5 | 80.2 | 과학 추론 |
| HellaSwag | 82.0 | 81.3 | 79.5 | 상식 추론 |
| TruthfulQA | 51.7 | 58.2 | 53.4 | 사실 정확도 |
| Winogrande | 80.5 | 78.0 | 78.8 | 언어 이해 |

### 주요 벤치마크 (14B~24B 모델 기준)

| 벤치마크 | Llama 3.2 11B | Mistral Small 24B | DeepSeek-R1 14B | 측정 항목 |
|----------|-------------|-----------------|---------------|----------|
| MMLU | 73.2 | 77.3 | 76.8 | 일반 지식 |
| HumanEval | 76.8 | 74.4 | 80.5 | 코딩 능력 |
| GSM8K | 87.3 | 83.2 | 93.4 | 수학 추론 |
| ARC-C | 85.1 | 86.5 | 84.7 | 과학 추론 |
| MATH | 42.5 | 46.8 | 68.3 | 고급 수학 |

숫자만 놓고 보면 몇 가지 패턴이 보인다.

- 수학/추론: DeepSeek-R1이 압도적. GSM8K와 MATH에서 같은 크기 모델 대비 10점 이상 앞선다
- 코딩: Llama 3과 DeepSeek-R1이 비슷하게 강하고, Mistral은 약간 뒤처진다
- 일반 지식: 크기가 커지면 Mistral이 강해지는 경향. 24B 모델의 MMLU가 높다
- 사실 정확도: Mistral이 TruthfulQA에서 약간 앞선다

---

## 3. 한국어 성능 비교: 실제로 써보니

벤치마크 대부분은 영어 기반이라, 한국어 성능은 직접 테스트해봐야 정확하다. 7~8B 모델 기준으로 한국어 작업 4가지를 테스트해봤다.

### 테스트 1: 한국어 요약

원문: 약 500자 분량의 한국어 기술 뉴스 기사

```
[프롬프트]
다음 기사를 3줄로 요약해줘:
(기사 내용)
```

| 모델 | 요약 품질 | 한국어 자연스러움 | 핵심 포착 |
|------|----------|-----------------|----------|
| Llama 3.1 8B | 보통 | 간혹 어색한 표현 | 핵심 1~2개 놓침 |
| Mistral 7B | 보통 이하 | 번역투 느낌 강함 | 핵심 포착 부족 |
| DeepSeek-R1 8B | 양호 | 비교적 자연스러움 | 핵심 잘 잡음 |

**결과**: 7B급에서 한국어 요약은 DeepSeek-R1이 가장 낫다. 다만 세 모델 모두 GPT-4o나 Claude Sonnet 수준에는 미치지 못한다.

### 테스트 2: 한국어 코드 주석 작성

```python
# 프롬프트: 이 함수에 한국어 docstring을 작성해줘
def calculate_moving_average(data, window_size):
    if len(data) < window_size:
        return []
    result = []
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        result.append(sum(window) / window_size)
    return result
```

| 모델 | docstring 품질 | 파라미터 설명 | 자연스러움 |
|------|---------------|-------------|-----------|
| Llama 3.1 8B | 양호 | 영어 혼재 | 약간 어색 |
| Mistral 7B | 보통 | 간략함 | 번역투 |
| DeepSeek-R1 8B | 양호 | 상세함 | 자연스러움 |

### 테스트 3: 한국어 질의응답

```
[프롬프트]
한국의 공공데이터 포털에서 API 키를 발급받는 절차를 설명해줘.
```

이건 사실 한국 특화 지식이 필요한 질문이라 오픈소스 모델에게는 불리한 테스트다. 세 모델 모두 일반적인 API 발급 절차를 설명하는 수준이었고, 한국 공공데이터 포털의 구체적인 UI나 절차는 정확하게 알지 못했다. 그래도 DeepSeek-R1이 가장 구체적인 답변을 내놨고, Llama 3은 중간, Mistral은 가장 일반적인 답변을 했다.

### 테스트 4: 한영 번역

```
[프롬프트]
다음 문장을 영어로 번역해줘:
"이 프로젝트는 확장성을 고려하여 마이크로서비스 아키텍처로 설계했으며,
각 서비스 간 통신은 gRPC를 사용합니다."
```

| 모델 | 번역 정확도 | 기술 용어 처리 | 문장 자연스러움 |
|------|-----------|-------------|-------------|
| Llama 3.1 8B | 양호 | 정확 | 자연스러움 |
| Mistral 7B | 양호 | 정확 | 자연스러움 |
| DeepSeek-R1 8B | 양호 | 정확 | 자연스러움 |

기술 번역은 세 모델 모두 비슷하게 잘했다. 기술 용어가 영어 기반이라 한국어 모델 능력보다는 기본 언어 이해력만 있으면 되는 작업이기 때문이다.

### 한국어 종합 평가

| 항목 | Llama 3.1 8B | Mistral 7B | DeepSeek-R1 8B |
|------|-------------|-----------|---------------|
| 한국어 요약 | ★★★ | ★★ | ★★★★ |
| 한국어 대화 | ★★★ | ★★ | ★★★★ |
| 코드 + 한국어 | ★★★★ | ★★★ | ★★★★ |
| 한영 번역 | ★★★★ | ★★★ | ★★★★ |
| 한국 특화 지식 | ★★ | ★★ | ★★★ |

한국어 작업이 많다면 DeepSeek-R1을 추천한다. 학습 데이터에 중국어가 많이 포함되어 있는데, 그 덕분인지 한자 문화권 언어인 한국어에서도 상대적으로 좋은 성능을 보여준다.

---

## 4. 속도와 리소스 비교: 내 컴퓨터에서 잘 돌아갈까

### 추론 속도 (tokens/sec)

Ollama 기준으로 동일한 하드웨어에서 측정한 대략적인 수치다. 실제 속도는 하드웨어와 양자화 수준에 따라 달라질 수 있다. 로컬 LLM 세팅이 처음이라면 [Ollama 로컬 LLM 가이드]({{< relref "posts/2025-12-19-ollama-local-llm-guide.md" >}})를 먼저 읽어보는 걸 추천한다.

#### RTX 4070 (12GB VRAM) 기준

| 모델 | 크기 | 양자화 | 추론 속도 | 첫 응답 시간 |
|------|------|-------|----------|------------|
| Llama 3.1 8B | 4.7GB (Q4_K_M) | 4bit | ~42 tok/s | ~0.8초 |
| Mistral 7B | 4.1GB (Q4_K_M) | 4bit | ~48 tok/s | ~0.7초 |
| DeepSeek-R1 8B | 4.9GB (Q4_K_M) | 4bit | ~38 tok/s | ~1.2초 |
| DeepSeek-R1 14B | 8.9GB (Q4_K_M) | 4bit | ~22 tok/s | ~1.8초 |

#### Apple M3 Pro (18GB 통합 메모리) 기준

| 모델 | 크기 | 양자화 | 추론 속도 | 첫 응답 시간 |
|------|------|-------|----------|------------|
| Llama 3.1 8B | 4.7GB (Q4_K_M) | 4bit | ~35 tok/s | ~1.0초 |
| Mistral 7B | 4.1GB (Q4_K_M) | 4bit | ~40 tok/s | ~0.9초 |
| DeepSeek-R1 8B | 4.9GB (Q4_K_M) | 4bit | ~32 tok/s | ~1.5초 |
| DeepSeek-R1 14B | 8.9GB (Q4_K_M) | 4bit | ~18 tok/s | ~2.2초 |

#### CPU 전용 (32GB RAM, i7-13700K) 기준

| 모델 | 크기 | 양자화 | 추론 속도 | 첫 응답 시간 |
|------|------|-------|----------|------------|
| Llama 3.1 8B | 4.7GB (Q4_K_M) | 4bit | ~8 tok/s | ~3.5초 |
| Mistral 7B | 4.1GB (Q4_K_M) | 4bit | ~10 tok/s | ~3.0초 |
| DeepSeek-R1 8B | 4.9GB (Q4_K_M) | 4bit | ~7 tok/s | ~4.0초 |

속도만 보면 Mistral 7B가 가장 빠르다. 모델 크기가 상대적으로 작아서 메모리도 덜 쓰고, 아키텍처도 효율적이다. DeepSeek-R1은 추론 과정(Chain-of-Thought)을 내부적으로 거치기 때문에 첫 응답이 좀 느리지만, 그만큼 답변 품질이 높다.

### 메모리 사용량

| 모델 | RAM (CPU 모드) | VRAM (GPU 모드) | 비고 |
|------|--------------|----------------|------|
| Llama 3.1 8B (Q4) | ~8GB | ~5GB | 가장 무난 |
| Mistral 7B (Q4) | ~6GB | ~4.5GB | 가장 가벼움 |
| DeepSeek-R1 8B (Q4) | ~8GB | ~5.5GB | CoT로 인한 추가 메모리 |
| DeepSeek-R1 14B (Q4) | ~14GB | ~10GB | 16GB RAM이면 빠듯 |
| Llama 3.2 3B (Q4) | ~3GB | ~2.5GB | 가벼운 작업용 |
| Mistral Nemo 12B (Q4) | ~10GB | ~8GB | 중간급 |

---

## 5. 용도별 추천: 이럴 때 이 모델

### 코딩 보조

코딩 관련 작업이 주 목적이라면 DeepSeek-R1을 추천한다. HumanEval 벤치마크에서 높은 점수를 받았고, 실제로 써보면 코드 생성과 디버깅에서 확실히 강하다. 특히 14B 모델은 코딩 작업에서 상용 모델에 근접한 성능을 보여준다.

```
추천 모델:
1순위: DeepSeek-R1 14B (VRAM 12GB 이상)
2순위: DeepSeek-R1 8B (VRAM 8GB)
3순위: Llama 3.1 8B (가벼운 코딩 보조)
```

### 일반 대화 및 질의응답

범용 대화형 AI로 쓸 거라면 Llama 3.1 8B가 무난하다. 커뮤니티가 가장 크고, 파인튜닝된 변형 모델도 많아서 선택지가 넓다. 한국어 위주로 쓸 거라면 DeepSeek-R1 8B가 더 낫다.

```
추천 모델:
영어 위주: Llama 3.1 8B
한국어 위주: DeepSeek-R1 8B
가벼운 사용: Llama 3.2 3B
```

### 수학/논리적 추론

DeepSeek-R1 일택이다. GSM8K 88.1, MATH에서도 다른 모델을 크게 앞선다. 추론 과정을 투명하게 보여주기 때문에 틀렸을 때 어디서 잘못됐는지 확인하기도 좋다.

```
추천 모델:
1순위: DeepSeek-R1 14B 이상
2순위: DeepSeek-R1 8B
```

### 문서 요약 및 분석

긴 문서를 다뤄야 한다면 컨텍스트 윈도우가 넓은 모델이 유리하다. Llama 3은 128K 토큰을 지원하고, Mistral Small도 128K를 지원한다.

```
추천 모델:
긴 문서: Llama 3.1 8B (128K 컨텍스트)
짧은 문서: Mistral 7B (빠른 속도)
품질 우선: DeepSeek-R1 14B
```

### 멀티모달 (이미지 입력)

이미지를 입력으로 받아야 한다면 선택지가 좁아진다. Llama 3.2의 11B, 90B Vision 모델이 이미지 입력을 지원하고, LLaVA 같은 멀티모달 모델도 있다. Mistral과 DeepSeek-R1은 텍스트 전용이다.

```
추천 모델:
1순위: Llama 3.2 11B Vision (VRAM 12GB 이상)
2순위: LLaVA 13B
```

### 리소스 제한 환경 (8GB RAM 이하)

오래된 노트북이나 GPU 없는 환경이라면 3B 이하 모델을 써야 한다.

```
추천 모델:
1순위: Llama 3.2 3B
2순위: Phi-4-mini (3.8B)
3순위: Gemma 3 1B (최소 사양)
```

---

## 6. 모델 선택 플로우차트

용도와 환경에 따라 어떤 모델을 써야 할지 한눈에 정리하면 이렇다.

```
내 GPU VRAM은?
│
├── 없음 (CPU only, RAM 16GB 이하)
│   └── Llama 3.2 3B 또는 Phi-4-mini
│
├── 8GB (RTX 3060/4060 등)
│   ├── 코딩/추론 → DeepSeek-R1 8B
│   ├── 범용 대화 → Llama 3.1 8B
│   └── 속도 우선 → Mistral 7B
│
├── 12GB (RTX 4070 등)
│   ├── 코딩/추론 → DeepSeek-R1 14B ★ 추천
│   ├── 한국어 → DeepSeek-R1 14B
│   ├── 멀티모달 → Llama 3.2 11B Vision
│   └── 범용 → Mistral Nemo 12B
│
└── 24GB+ (RTX 4090, A6000 등)
    ├── 최고 성능 → DeepSeek-R1 32B
    ├── 범용 → Llama 3.1 70B (Q4 양자화)
    └── MoE → Mixtral 8x7B
```

---

## 7. 실전 세팅 팁

### Ollama로 각 모델 설치하기

```bash
# DeepSeek-R1 설치
ollama pull deepseek-r1:8b
ollama pull deepseek-r1:14b    # VRAM 12GB 이상

# Llama 3.1 설치
ollama pull llama3.1:8b

# Mistral 설치
ollama pull mistral:7b
ollama pull mistral-nemo:12b   # Nemo 버전

# 모델 실행
ollama run deepseek-r1:14b
```

### 양자화 선택 가이드

같은 모델이라도 양자화 수준에 따라 크기와 품질이 달라진다.

| 양자화 | 크기 비율 | 품질 손실 | 추천 상황 |
|--------|---------|----------|----------|
| Q8_0 | ~50% 원본 | 거의 없음 | VRAM 넉넉할 때 |
| Q6_K | ~40% 원본 | 미미 | 품질과 크기 균형 |
| Q4_K_M | ~30% 원본 | 약간 있음 | 가장 보편적 선택 |
| Q4_K_S | ~28% 원본 | 약간 있음 | 메모리 절약 필요 시 |
| Q3_K_M | ~25% 원본 | 체감됨 | 메모리 매우 부족 시 |
| Q2_K | ~20% 원본 | 상당함 | 비추천 |

내 경험상 Q4_K_M이 품질과 크기의 최적 균형점이다. Q8까지 올려도 체감 차이가 크지 않고, Q3 이하로 내리면 응답 품질이 눈에 띄게 떨어진다.

### 커스텀 Modelfile 활용

자주 쓰는 설정을 Modelfile로 만들어두면 편하다.

```dockerfile
# coding-assistant.modelfile
FROM deepseek-r1:14b

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 8192

SYSTEM """
당신은 시니어 소프트웨어 엔지니어입니다. 코드 리뷰, 디버깅, 구현을 도와주세요.
- 한국어로 설명하되 코드와 기술 용어는 영어를 사용
- 코드에는 반드시 주석을 포함
- 잠재적 버그나 개선점이 있으면 지적
"""
```

```bash
# 커스텀 모델 생성 및 실행
ollama create coding-assistant -f coding-assistant.modelfile
ollama run coding-assistant
```

### API 연동

Ollama는 OpenAI 호환 API를 제공하기 때문에, 기존에 OpenAI API를 쓰던 코드를 거의 그대로 쓸 수 있다.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # 아무 값이나 넣으면 됨
)

response = client.chat.completions.create(
    model="deepseek-r1:14b",
    messages=[
        {"role": "system", "content": "한국어로 답변하세요."},
        {"role": "user", "content": "FastAPI에서 미들웨어를 추가하는 방법을 알려줘"}
    ],
    temperature=0.3
)

print(response.choices[0].message.content)
```

---

## 8. 각 모델의 약점과 주의사항

어떤 모델이든 완벽하지는 않다. 써보면서 느낀 약점을 솔직하게 정리한다.

### Llama 3 시리즈

- 한국어 전용 학습 데이터가 부족해서, 한국 문화/제도에 대한 지식이 얕다
- 라이선스에 MAU 제한이 있어서 대규모 서비스에 적용할 때 확인 필요
- 8B 모델의 경우 복잡한 추론 작업에서 종종 논리 오류를 낸다

### Mistral 시리즈

- 한국어 성능이 세 모델 중 가장 약하다. 한국어 작업이 많다면 비추
- 최신 모델(Small, Large)은 Apache 라이선스가 아닌 상업용 라이선스로 전환됨
- 모델 업데이트 주기가 불규칙해서 생태계 예측이 어렵다

### DeepSeek-R1

- Chain-of-Thought 때문에 응답 시작이 느리다. 빠른 자동완성이 필요한 곳에는 부적합
- CoT 과정에서 토큰을 추가로 소모하기 때문에 실질 처리량이 줄어든다
- 중국 기업이라 데이터 프라이버시 관련 우려가 있을 수 있다 (로컬 실행이면 문제없음)
- 가끔 중국어가 섞여 나오는 현상이 있다

---

## 9. 세 모델 종합 비교표

| 항목 | Llama 3.1/3.2 | Mistral 7B/Nemo | DeepSeek-R1 |
|------|-------------|----------------|-------------|
| 코딩 | ★★★★ | ★★★ | ★★★★★ |
| 수학/추론 | ★★★ | ★★★ | ★★★★★ |
| 한국어 | ★★★ | ★★ | ★★★★ |
| 영어 | ★★★★ | ★★★★ | ★★★★ |
| 속도 | ★★★★ | ★★★★★ | ★★★ |
| 메모리 효율 | ★★★★ | ★★★★★ | ★★★ |
| 생태계/커뮤니티 | ★★★★★ | ★★★ | ★★★★ |
| 라이선스 자유도 | ★★★★ | ★★★ (모델마다 다름) | ★★★★★ |
| 멀티모달 | ★★★★ (Vision) | ★★ | ★★ |
| 문서/요약 | ★★★★ | ★★★ | ★★★★ |

---

## 한 줄 요약

내 결론은 이렇다. 코딩이나 추론 위주면 DeepSeek-R1 14B, 범용으로 쓸 거면 Llama 3.1 8B, 가볍고 빠른 게 필요하면 Mistral 7B. 세 모델 다 깔아보고 직접 비교해보는 게 사실 제일 좋은데, Ollama 덕분에 5분이면 설치할 수 있으니 부담 없이 써봐도 된다. 요즘 오픈소스 모델 발전 속도가 미친 수준이라, 3개월만 지나면 판이 또 바뀔 수 있다는 점도 참고하자.
