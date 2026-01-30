---
title: "AI 개발자를 위한 Docker 실전 가이드: 환경 구축부터 GPU 배포까지 (2026)"
date: 2026-01-30
description: "AI/ML 프로젝트에서 Docker를 활용하는 방법. 개발 환경 통일, GPU 컨테이너, 모델 서빙, Docker Compose까지 AI 개발자 관점에서 정리합니다."
categories: [AI]
tags: [Docker, AI 개발, GPU, 컨테이너, DevOps]
keywords: [Docker AI 개발, Docker GPU 설정, AI 모델 Docker 배포, Docker Compose ML, 컨테이너 머신러닝]
draft: false
slug: docker-for-ai-developers-guide-2026
---

"내 컴퓨터에서는 돌아가는데..." AI 개발에서 가장 흔한 문제입니다. Python 버전, CUDA 버전, 라이브러리 의존성이 조금만 달라도 모델이 작동하지 않습니다. **Docker**는 이 문제를 완전히 해결합니다.

---

## 왜 AI 개발에 Docker인가?

### AI 개발의 환경 문제

| 문제 | 원인 | Docker 해결 |
|------|------|------------|
| "내 PC에서만 작동" | Python/CUDA 버전 차이 | 동일한 컨테이너 이미지 |
| GPU 드라이버 충돌 | 여러 프로젝트가 다른 CUDA 요구 | 프로젝트별 컨테이너 |
| 배포 시 오류 | 로컬과 서버 환경 차이 | 동일 이미지로 배포 |
| 팀원 온보딩 지연 | 복잡한 환경 설정 | `docker compose up` 한 줄 |

---

## Docker 기초: AI 프로젝트용 Dockerfile

### 기본 Python ML 프로젝트

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# 시스템 의존성
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드
COPY . .

# 포트 노출
EXPOSE 8000

# 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### GPU 지원 PyTorch 프로젝트

```dockerfile
# GPU가 필요한 ML 프로젝트
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# Python 설치
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "train.py"]
```

### 빌드 및 실행

```bash
# 이미지 빌드
docker build -t my-ml-app .

# CPU로 실행
docker run -p 8000:8000 my-ml-app

# GPU로 실행 (NVIDIA Container Toolkit 필요)
docker run --gpus all -p 8000:8000 my-ml-app
```

---

## GPU Docker 설정

### NVIDIA Container Toolkit 설치

```bash
# Ubuntu
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### GPU 컨테이너 확인

```bash
docker run --gpus all nvidia/cuda:12.4.0-runtime-ubuntu22.04 nvidia-smi
```

### GPU 할당 옵션

```bash
# 모든 GPU 사용
docker run --gpus all my-app

# 특정 GPU만 사용
docker run --gpus '"device=0"' my-app

# GPU 2개 사용
docker run --gpus 2 my-app
```

---

## Docker Compose: 멀티 서비스 AI 시스템

실제 AI 서비스는 여러 컴포넌트로 구성됩니다.

```yaml
# docker-compose.yml
services:
  # AI 모델 서빙 API
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
      - redis

  # 벡터 데이터베이스 (RAG용)
  vectordb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma

  # 관계형 데이터베이스
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - pg_data:/var/lib/postgresql/data

  # 캐시
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  chroma_data:
  pg_data:
```

### 실행

```bash
# 전체 시스템 시작
docker compose up -d

# 로그 확인
docker compose logs -f api

# 중지
docker compose down
```

---

## AI 모델 서빙 컨테이너

### FastAPI + 모델 서빙

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 모델 파일 복사 (빌드 시 포함)
COPY models/ ./models/
COPY app.py .

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### 모델 파일 관리 팁

대용량 모델 파일은 Docker 이미지에 포함하면 이미지가 커집니다. 대안:

```dockerfile
# 방법 1: 런타임에 다운로드
CMD python download_model.py && uvicorn app:app --host 0.0.0.0

# 방법 2: 볼륨 마운트
# docker run -v ./models:/app/models my-app

# 방법 3: 멀티스테이지 빌드
FROM builder AS model-downloader
RUN python download_model.py

FROM python:3.12-slim
COPY --from=model-downloader /models /app/models
```

---

## Dockerfile 최적화

### 레이어 캐시 활용

```dockerfile
# 나쁜 예: 코드 변경 시 의존성도 다시 설치
COPY . .
RUN pip install -r requirements.txt

# 좋은 예: 의존성 캐시 활용
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### 이미지 크기 줄이기

```dockerfile
# slim 이미지 사용 (1GB → 200MB)
FROM python:3.12-slim

# 불필요한 파일 제외
# .dockerignore 파일:
# __pycache__/
# .git/
# .env
# *.pyc
# notebooks/
# data/raw/
```

---

## 실전 예제: LLM API 서비스

```yaml
# docker-compose.yml - 블로그 자동화 시스템
services:
  blog-api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  # Ollama 로컬 LLM (GPU)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]

volumes:
  ollama_data:
```

---

## 마무리

Docker는 AI 개발의 **재현성 문제를 근본적으로 해결**합니다. "내 PC에서는 돌아가는데"라는 말 대신, 동일한 Docker 이미지를 어디서든 실행할 수 있습니다.

**AI 개발자를 위한 Docker 시작 순서:**
1. 기본 Dockerfile 작성 → 로컬에서 컨테이너로 실행
2. docker-compose.yml → 멀티 서비스 구성
3. GPU Docker 설정 → 학습/추론 컨테이너화
4. CI/CD 연동 → 자동 빌드/배포

한 번 설정하면, 이후 모든 팀원과 서버에서 동일한 환경을 보장받을 수 있습니다.
