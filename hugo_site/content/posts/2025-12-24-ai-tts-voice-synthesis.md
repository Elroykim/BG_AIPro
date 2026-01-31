---
title: "AI 음성 합성(TTS) 써봤다: ElevenLabs vs OpenAI TTS vs 네이버 클로바"
date: 2025-12-24
description: "AI TTS 서비스를 실제로 한국어 텍스트로 테스트해본 비교 리뷰. ElevenLabs, OpenAI TTS, 네이버 클로바, Google Cloud TTS의 품질, 가격, API 사용법을 정리합니다."
categories: [AI]
tags: [AI TTS, 음성 합성, ElevenLabs, OpenAI TTS, 클로바]
keywords: [AI 음성 합성, TTS 비교, ElevenLabs 한국어, OpenAI TTS API, 네이버 클로바 보이스]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: ai-tts-voice-synthesis-comparison
---

유튜브 영상에 나레이션을 넣고 싶었는데, 직접 녹음하자니 목소리가 마음에 안 들고 방음도 안 되고. 그래서 AI TTS를 찾아보기 시작했다. 요즘 TTS 기술이 얼마나 좋아졌는지 궁금해서 주요 서비스를 다 테스트해봤는데, 결론부터 말하면 한국어는 아직 서비스마다 편차가 크다.

같은 한국어 텍스트로 ElevenLabs, OpenAI TTS, 네이버 클로바, Google Cloud TTS를 직접 비교해본 결과를 정리한다.

---

## AI TTS가 뭐가 달라졌나

예전 TTS를 기억하는 사람은 "로봇 목소리" 이미지가 강할 텐데, 지금은 상황이 완전히 다르다.

```
[기존 TTS]
텍스트 → 음소 분리 → 규칙 기반 발음 → 파형 합성
→ 로봇 같은 단조로운 목소리

[AI TTS (2025~)]
텍스트 → 딥러닝 모델 → 자연어 이해 → 뉴럴 음성 합성
→ 감정, 억양, 호흡까지 자연스러운 목소리
```

특히 최근에는 제로샷 음성 복제(voice cloning)까지 가능해져서, 몇 초 분량의 음성 샘플만 있으면 그 사람의 목소리로 TTS를 생성할 수 있다.

---

## 테스트 조건

공정한 비교를 위해 동일한 텍스트 3종으로 테스트했다.

```
[테스트 텍스트 1 - 뉴스 스타일]
"인공지능 기술의 발전으로 소프트웨어 개발 생산성이 크게 향상되고 있습니다.
특히 코드 생성과 자동 테스트 분야에서 눈에 띄는 성과를 보이고 있으며,
개발자들의 업무 방식이 빠르게 변화하고 있습니다."

[테스트 텍스트 2 - 대화 스타일]
"아, 그거 어제 해봤는데 진짜 대박이더라. 한번 써봐, 후회 안 할 거야.
근데 처음에 설정이 좀 귀찮긴 해. 같이 해볼까?"

[테스트 텍스트 3 - 기술 설명]
"FastAPI는 Python의 타입 힌트를 기반으로 자동 문서화와 데이터 검증을
제공하는 고성능 웹 프레임워크입니다. 비동기 처리를 기본으로 지원합니다."
```

평가 항목은 자연스러움, 한국어 발음 정확도, 감정 표현, 속도 조절 가능 여부, API 편의성, 가격이다.

---

## ElevenLabs

현재 AI TTS 분야에서 가장 주목받는 서비스다. 영어 품질이 압도적이고, 다국어 지원도 계속 개선되고 있다.

### API 사용법

```python
import requests
import os

ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]

def elevenlabs_tts(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
    """ElevenLabs TTS API 호출"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY,
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # 다국어 모델
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=data, headers=headers)

    with open("output_elevenlabs.mp3", "wb") as f:
        f.write(response.content)

    print("ElevenLabs TTS 생성 완료")
    return "output_elevenlabs.mp3"

# 사용
elevenlabs_tts("인공지능 기술의 발전으로 소프트웨어 개발 생산성이 크게 향상되고 있습니다.")
```

### 음성 복제 (Voice Cloning)

```python
def clone_voice(name: str, audio_files: list[str]):
    """음성 샘플로 커스텀 보이스 생성"""
    url = "https://api.elevenlabs.io/v1/voices/add"

    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    data = {"name": name}
    files = [
        ("files", (f"sample_{i}.mp3", open(f, "rb"), "audio/mpeg"))
        for i, f in enumerate(audio_files)
    ]

    response = requests.post(url, headers=headers, data=data, files=files)
    voice_id = response.json()["voice_id"]
    print(f"음성 복제 완료: {voice_id}")
    return voice_id

# 3초 이상의 음성 샘플 1~25개로 복제 가능
# voice_id = clone_voice("my-voice", ["sample1.mp3", "sample2.mp3"])
```

### 한국어 테스트 결과

- 뉴스 스타일: 자연스러움, 억양이 약간 영어 패턴
- 대화 스타일: "아, 그거" 같은 구어체 표현에서 어색함
- 기술 설명: "FastAPI"를 자연스럽게 읽음, 전체적으로 준수

총평: 영어는 압도적이지만, 한국어는 아직 네이티브 수준은 아니다. 한국어 전용 보이스가 추가되면 더 좋아질 듯하다.

---

## OpenAI TTS

ChatGPT를 만든 OpenAI의 TTS 서비스. API가 간결하고, 6종의 기본 음성을 제공한다.

### API 사용법

```python
from openai import OpenAI

client = OpenAI()

def openai_tts(text: str, voice: str = "alloy", model: str = "tts-1-hd"):
    """OpenAI TTS API 호출"""
    response = client.audio.speech.create(
        model=model,
        voice=voice,  # alloy, echo, fable, onyx, nova, shimmer
        input=text,
        speed=1.0,  # 0.25 ~ 4.0
    )

    output_path = "output_openai.mp3"
    response.stream_to_file(output_path)
    print(f"OpenAI TTS 생성 완료: {output_path}")
    return output_path

# 음성 종류별 테스트
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
for voice in voices:
    openai_tts("안녕하세요, 이것은 TTS 테스트입니다.", voice=voice)
```

### 스트리밍 TTS

```python
def openai_tts_stream(text: str, voice: str = "nova"):
    """실시간 스트리밍 TTS"""
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="pcm",
    )

    # 스트리밍으로 받아서 바로 재생 가능
    for chunk in response.iter_bytes(chunk_size=4096):
        # 오디오 플레이어로 전송
        yield chunk
```

### 모델 비교

| 항목 | tts-1 | tts-1-hd |
|------|-------|----------|
| 품질 | 보통 | 높음 |
| 지연시간 | 낮음 | 보통 |
| 가격 | $15/1M 글자 | $30/1M 글자 |
| 용도 | 실시간 앱 | 콘텐츠 제작 |

### 한국어 테스트 결과

- 뉴스 스타일: 깔끔하고 안정적, 약간 밋밋한 느낌
- 대화 스타일: 구어체 억양 재현이 약간 부자연스러움
- 기술 설명: 영어 기술 용어 발음이 자연스러움

총평: API가 심플하고 품질도 준수하다. 한국어 감정 표현은 조금 아쉽지만, 일반적인 나레이션 용도로는 충분하다. 직접 써보니 nova 음성이 한국어에서 가장 자연스러웠다.

---

## 네이버 클로바 보이스

한국어 TTS라면 네이버를 빼놓을 수 없다. 한국어에 최적화되어 있고, 다양한 한국어 음성을 제공한다.

### API 사용법

```python
import requests
import os

CLOVA_CLIENT_ID = os.environ["CLOVA_CLIENT_ID"]
CLOVA_CLIENT_SECRET = os.environ["CLOVA_CLIENT_SECRET"]

def clova_tts(text: str, speaker: str = "nara"):
    """네이버 클로바 보이스 TTS API 호출"""
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

    headers = {
        "X-NCP-APIGW-API-KEY-ID": CLOVA_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": CLOVA_CLIENT_SECRET,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "speaker": speaker,
        "text": text,
        "volume": 0,      # -5 ~ 5
        "speed": 0,        # -5 ~ 5
        "pitch": 0,        # -5 ~ 5
        "format": "mp3",
        "emotion": 0,      # 0: 기본, 1: 슬픔, 2: 기쁨, 3: 분노
        "emotion-strength": 1,  # 감정 강도 1~3
    }

    response = requests.post(url, headers=headers, data=data)

    with open("output_clova.mp3", "wb") as f:
        f.write(response.content)

    print("클로바 TTS 생성 완료")
    return "output_clova.mp3"

# 화자 목록 예시
speakers = {
    "nara": "여성 (나라, 차분한 목소리)",
    "clara": "여성 (클라라, 밝은 목소리)",
    "dara": "여성 (다라, 또렷한 목소리)",
    "matt": "남성 (매트, 낮은 목소리)",
    "shinji": "남성 (신지, 부드러운 목소리)",
}

for speaker, desc in speakers.items():
    print(f"테스트: {desc}")
    clova_tts("인공지능 기술의 발전으로 개발 생산성이 향상되고 있습니다.", speaker)
```

### 감정 표현 기능

클로바의 강점은 한국어 감정 표현이다. 같은 텍스트를 기쁜 톤, 슬픈 톤으로 변환할 수 있다.

```python
# 같은 텍스트, 다른 감정
emotions = {
    0: "기본",
    1: "슬픔",
    2: "기쁨",
    3: "분노",
}

text = "정말 그렇게 된 거예요? 믿을 수가 없네요."

for emotion_id, emotion_name in emotions.items():
    print(f"감정: {emotion_name}")
    data = {
        "speaker": "nara",
        "text": text,
        "emotion": emotion_id,
        "emotion-strength": 2,
    }
    # API 호출...
```

### 한국어 테스트 결과

- 뉴스 스타일: 발음과 억양이 가장 자연스러움, 아나운서 수준
- 대화 스타일: "아, 그거" 같은 구어체도 잘 처리
- 기술 설명: "FastAPI"를 "패스트에이피아이"로 읽는 경우 있음

총평: 한국어만 놓고 보면 클로바가 가장 자연스럽다. 감정 표현도 좋고, 화자 종류도 다양하다. 다만 영어 발음이 약하고 다국어 지원이 제한적이다.

---

## Google Cloud TTS

구글 클라우드의 TTS 서비스. WaveNet과 Neural2 모델을 제공하며, 다국어 지원이 폭넓다.

### API 사용법

```python
from google.cloud import texttospeech

def google_tts(text: str, language_code: str = "ko-KR",
               voice_name: str = "ko-KR-Neural2-A"):
    """Google Cloud TTS API 호출"""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,  # 0.25 ~ 4.0
        pitch=0.0,          # -20.0 ~ 20.0
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("output_google.mp3", "wb") as f:
        f.write(response.audio_content)

    print("Google TTS 생성 완료")
    return "output_google.mp3"

# 한국어 Neural2 음성
google_tts(
    "인공지능 기술의 발전으로 개발 생산성이 향상되고 있습니다.",
    voice_name="ko-KR-Neural2-C"
)
```

### SSML로 세밀한 제어

```python
def google_tts_ssml(ssml: str, voice_name: str = "ko-KR-Neural2-A"):
    """SSML 마크업으로 세밀한 음성 제어"""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("output_google_ssml.mp3", "wb") as f:
        f.write(response.audio_content)

    return "output_google_ssml.mp3"

# SSML 예시
ssml_text = """
<speak>
  인공지능 기술의 발전으로
  <break time="500ms"/>
  소프트웨어 개발 생산성이 <emphasis level="strong">크게</emphasis> 향상되고 있습니다.
  <break time="300ms"/>
  특히 <say-as interpret-as="spell-out">AI</say-as> 코드 생성 분야에서
  눈에 띄는 성과를 보이고 있습니다.
</speak>
"""

google_tts_ssml(ssml_text)
```

### 한국어 테스트 결과

- 뉴스 스타일: WaveNet보다 Neural2가 훨씬 자연스러움
- 대화 스타일: 구어체에서는 다소 딱딱한 느낌
- 기술 설명: SSML로 영어 발음을 제어할 수 있어서 기술 용어 처리에 유리

총평: 안정적이고 다국어 지원이 넓다. SSML 활용도가 높아서 세밀한 제어가 필요할 때 유용하다.

---

## 전체 비교표

| 항목 | ElevenLabs | OpenAI TTS | 클로바 보이스 | Google Cloud TTS |
|------|-----------|-----------|-------------|-----------------|
| 한국어 자연스러움 | B+ | B | A+ | B+ |
| 영어 자연스러움 | A+ | A | C | A |
| 감정 표현 | A | B | A | B (SSML) |
| 음성 복제 | 가능 | 불가 | 불가 | 불가 |
| 음성 종류 | 수천 개 + 커스텀 | 6종 | 약 20종 | 수십 종 |
| API 간결함 | 보통 | 매우 간결 | 보통 | 약간 복잡 |
| 스트리밍 | 지원 | 지원 | 미지원 | 지원 |
| SSML 지원 | 부분 | 미지원 | 미지원 | 완전 지원 |
| 무료 티어 | 월 1만자 | 없음 | 월 9만자 | 월 400만자 |
| 가격 (100만자) | ~$11 | $15~30 | ~$9 | $4~16 |

---

## 가격 비교 (상세)

유튜브 나레이션 기준으로 월 사용량을 계산해봤다. 10분짜리 영상의 스크립트가 약 2,000자라고 가정한다.

### 월 10개 영상 (2만 자) 기준

| 서비스 | 월 비용 | 비고 |
|--------|---------|------|
| ElevenLabs (Starter) | $5 | 3만자/월 |
| OpenAI TTS (tts-1) | $0.30 | 종량제 |
| OpenAI TTS (tts-1-hd) | $0.60 | 종량제 |
| 클로바 보이스 | 약 ₩2,000 | 9만자 무료 초과분 |
| Google Cloud (Neural2) | $0.32 | 400만자 무료 내 |

소량이면 Google Cloud 무료 티어가 가장 저렴하고, 품질을 중시하면 ElevenLabs Starter가 합리적이다.

---

## 실전 활용 사례

### 유튜브 나레이션 자동화

```python
def create_youtube_narration(script_path: str, service: str = "openai"):
    """유튜브 스크립트를 TTS로 변환"""
    with open(script_path, "r") as f:
        script = f.read()

    # 문단별로 분리
    paragraphs = [p.strip() for p in script.split("\n\n") if p.strip()]

    audio_files = []
    for i, para in enumerate(paragraphs):
        if service == "openai":
            output = openai_tts(para, voice="nova", model="tts-1-hd")
        elif service == "elevenlabs":
            output = elevenlabs_tts(para)
        elif service == "clova":
            output = clova_tts(para, speaker="nara")

        audio_files.append(output)
        print(f"[{i+1}/{len(paragraphs)}] 변환 완료")

    # pydub으로 합치기
    from pydub import AudioSegment

    combined = AudioSegment.empty()
    silence = AudioSegment.silent(duration=800)  # 문단 사이 0.8초 간격

    for audio_file in audio_files:
        segment = AudioSegment.from_mp3(audio_file)
        combined += segment + silence

    combined.export("final_narration.mp3", format="mp3")
    print("나레이션 생성 완료: final_narration.mp3")

# 사용
create_youtube_narration("script.txt", service="openai")
```

### 앱 음성 안내 시스템

```python
def generate_app_voice_pack(messages: dict, output_dir: str = "voice_pack"):
    """앱에서 쓸 음성 안내 파일 일괄 생성"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    for key, text in messages.items():
        output_path = f"{output_dir}/{key}.mp3"

        # 앱 안내는 짧고 명확해야 하므로 클로바 추천
        response = clova_tts(text, speaker="clara")
        os.rename(response, output_path)
        print(f"  {key}: {text}")

    print(f"\n음성팩 생성 완료: {output_dir}/")

# 앱 음성 안내 메시지
app_messages = {
    "welcome": "안녕하세요, AI 어시스턴트입니다.",
    "processing": "잠시만 기다려주세요. 분석 중입니다.",
    "complete": "분석이 완료되었습니다.",
    "error": "죄송합니다. 문제가 발생했습니다. 다시 시도해주세요.",
    "goodbye": "감사합니다. 좋은 하루 보내세요.",
}

generate_app_voice_pack(app_messages)
```

### 다국어 콘텐츠 제작

```python
def multilingual_tts(text_ko: str, text_en: str):
    """한국어/영어 동시 TTS 생성"""
    # 한국어: 클로바가 자연스러움
    ko_audio = clova_tts(text_ko, speaker="nara")

    # 영어: ElevenLabs가 자연스러움
    en_audio = elevenlabs_tts(text_en, voice_id="21m00Tcm4TlvDq8ikWAM")

    return {"ko": ko_audio, "en": en_audio}
```

---

## 서비스 선택 가이드

상황별로 어떤 TTS를 써야 할지 정리했다.

### 한국어 위주 콘텐츠

클로바 보이스를 추천한다. 한국어 발음과 억양이 가장 자연스럽고, 감정 표현도 지원하고, 가격도 합리적이다. 한국어 나레이션이나 앱 음성 안내에는 이게 제일 낫다.

### 영어 위주 또는 다국어

ElevenLabs가 독보적이다. 영어 품질이 최고이고, 음성 복제도 가능하다. 다만 가격이 좀 나가니까 분량이 많으면 예산 확인 필수.

### 빠른 프로토타입

OpenAI TTS가 좋다. API가 3줄이면 끝나고, 스트리밍도 되고, 품질도 준수하다. 이미 OpenAI API를 쓰고 있다면 추가 연동이 거의 없다.

### 세밀한 제어가 필요할 때

Google Cloud TTS + SSML 조합이 최선이다. 발음, 속도, 강조, 쉼표를 XML로 세밀하게 제어할 수 있다.

```
한국어 중심 → 클로바 보이스
영어/다국어 → ElevenLabs
빠른 개발 → OpenAI TTS
세밀한 제어 → Google Cloud TTS
음성 복제 → ElevenLabs
저비용 대량 → Google Cloud TTS
```

---

## 주의할 점

### 저작권과 윤리

- 음성 복제는 반드시 본인 동의를 받아야 한다
- 타인의 목소리를 무단으로 복제하면 법적 문제가 될 수 있다
- 상업용으로 쓸 때는 각 서비스의 이용 약관을 확인해야 한다
- AI 생성 음성임을 밝히는 것이 권장되는 추세

### 기술적 한계

- 긴 텍스트는 문단별로 나눠서 생성하는 게 품질이 더 좋다
- 특수 기호, 약어, 외래어는 서비스마다 처리 방식이 다르다
- 실시간 대화(예: 전화 상담 봇)에는 레이턴시를 반드시 테스트해야 한다

---

## 돌아보며

AI TTS를 직접 비교해보니 한 가지 확실한 건, 한국어와 영어의 품질 격차가 아직 크다는 것이다. 영어는 ElevenLabs가 사람과 구분이 안 될 정도인데, 한국어는 클로바가 가장 자연스럽지만 영어만큼의 수준에는 아직 미치지 못한다.

나는 주로 한국어 나레이션에는 클로바, 영어 컨텐츠에는 ElevenLabs, 빠른 테스트에는 OpenAI TTS를 쓰고 있다. 음성 외에 이미지, 영상까지 다루는 멀티모달 AI에 관심이 있다면 [멀티모달 AI 활용 가이드]({{< relref "posts/2026-01-22-multimodal-ai-guide.md" >}})도 참고해보자.

TTS 기술은 지금도 빠르게 발전하고 있어서, 6개월 뒤에는 순위가 바뀔 수 있다. 일단 무료 티어로 각 서비스를 직접 테스트해보고 자기 용도에 맞는 걸 고르는 게 가장 확실하다.
