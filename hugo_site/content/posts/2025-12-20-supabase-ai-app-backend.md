---
title: "Supabase로 AI 앱 백엔드 빠르게 만들기: 인증부터 벡터 검색까지"
date: 2025-12-20
description: "Supabase를 AI 앱 백엔드로 활용하는 방법. 인증, 데이터베이스, pgvector 임베딩 검색, Edge Functions까지 실전 프로젝트 구성을 다룹니다."
categories: [개발]
tags: [Supabase, AI 백엔드, pgvector, 인증, 데이터베이스]
keywords: [Supabase AI 앱, Supabase pgvector, AI 백엔드 구축, Supabase 인증, Supabase Edge Functions]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: supabase-ai-app-backend-guide
---

AI 사이드 프로젝트를 하다 보면 백엔드가 항상 발목을 잡는다. 인증 구현하고, DB 설계하고, API 서버 띄우고... 모델 연동은 아직 시작도 못했는데 벌써 일주일이 지나 있다. Supabase를 써보니까 이런 삽질이 거의 사라졌다. 특히 PostgreSQL 기반이라 pgvector 확장만 켜면 벡터 검색까지 한 곳에서 해결되는 게 좋았다.

Firebase에서 넘어온 사람도, 처음 백엔드를 잡는 사람도 참고할 수 있게 정리해봤다.

---

## Supabase가 AI 백엔드로 좋은 이유

요즘 AI 앱 백엔드에 필요한 것들을 정리하면 이렇다.

| 필요 기능 | 전통적 방식 | Supabase |
|-----------|-----------|----------|
| 사용자 인증 | Auth0, Firebase Auth, 직접 구현 | 내장 Auth |
| 데이터베이스 | PostgreSQL + 서버 운영 | 관리형 PostgreSQL |
| 벡터 검색 | Pinecone, Weaviate 별도 운영 | pgvector 확장 내장 |
| 파일 저장 | S3 + 별도 설정 | Storage 내장 |
| API 서버 | FastAPI, Express 등 직접 구현 | Edge Functions + PostgREST 자동 |
| 실시간 기능 | WebSocket 직접 구현 | Realtime 구독 내장 |

포인트는 이 모든 게 하나의 프로젝트 안에서 돌아간다는 것이다. 벡터 DB를 따로 운영하지 않아도 되고, 인증 서버를 별도로 세울 필요도 없다.

### Supabase vs Firebase

Firebase도 좋은 BaaS지만, AI 앱에서는 Supabase가 유리한 점이 많다.

| 비교 항목 | Supabase | Firebase |
|-----------|----------|----------|
| DB 종류 | PostgreSQL (관계형) | Firestore (NoSQL) |
| SQL 지원 | 네이티브 SQL | 불가 |
| 벡터 검색 | pgvector 확장 | 불가 (별도 서비스 필요) |
| 오픈소스 | 완전 오픈소스 | 비공개 |
| 셀프호스팅 | 가능 | 불가 |
| Edge Functions | Deno 기반 | Cloud Functions (Node.js) |
| 무료 티어 | 프로젝트 2개, 500MB DB | Spark 플랜 (제한적) |
| 가격 모델 | 예측 가능 | 읽기/쓰기 횟수 기반 |

Firebase는 NoSQL이라 복잡한 쿼리가 어렵고, 벡터 검색이 안 되니까 AI 앱에서는 결국 별도 서비스를 붙여야 한다. Supabase는 PostgreSQL이라 pgvector만 켜면 임베딩 저장과 유사도 검색이 바로 가능하다.

---

## 프로젝트 세팅

### Supabase 프로젝트 생성

1. [supabase.com](https://supabase.com)에서 계정 생성
2. New Project 클릭
3. 프로젝트 이름, DB 비밀번호, 리전(Northeast Asia - Tokyo 추천) 설정
4. 생성 완료 후 Settings > API에서 키 확인

```
필요한 키:
- Project URL: https://xxxx.supabase.co
- anon (public) key: eyJhbGci... (클라이언트 사이드)
- service_role key: eyJhbGci... (서버 사이드, 절대 노출 금지)
```

### Python 클라이언트 설치

```bash
pip install supabase python-dotenv
```

### 환경 변수 설정

```bash
# .env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
OPENAI_API_KEY=sk-...  # 임베딩 생성용
```

### 기본 클라이언트 초기화

```python
# supabase_client.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)
print("Supabase 클라이언트 초기화 완료")
```

JavaScript라면 이렇게 한다.

```javascript
// supabaseClient.js
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseKey)
```

---

## 인증 (Auth) 구현

AI 앱에서도 사용자 인증은 필수다. API 사용량을 사용자별로 추적하거나, 대화 기록을 저장하려면 유저 식별이 필요하니까.

### 이메일 회원가입/로그인

```python
# 회원가입
result = supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "secure-password-123"
})
print(f"User ID: {result.user.id}")

# 로그인
result = supabase.auth.sign_in_with_password({
    "email": "user@example.com",
    "password": "secure-password-123"
})
access_token = result.session.access_token
print(f"로그인 성공, 토큰: {access_token[:20]}...")
```

### OAuth 소셜 로그인 (Google, GitHub)

```python
# Google OAuth 시작 URL 생성
result = supabase.auth.sign_in_with_oauth({
    "provider": "google",
    "options": {
        "redirect_to": "http://localhost:3000/auth/callback"
    }
})
# 사용자를 result.url로 리다이렉트
```

JavaScript에서는 더 직관적이다.

```javascript
// Google 로그인
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'http://localhost:3000/auth/callback'
  }
})

// GitHub 로그인
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'github'
})
```

### Row Level Security (RLS) 설정

인증만으로는 부족하다. RLS를 걸어야 유저가 자기 데이터만 볼 수 있다.

```sql
-- conversations 테이블 생성
CREATE TABLE conversations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  title TEXT,
  messages JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- RLS 활성화
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- 정책: 유저는 자기 대화만 조회 가능
CREATE POLICY "Users can view own conversations"
  ON conversations FOR SELECT
  USING (auth.uid() = user_id);

-- 정책: 유저는 자기 대화만 생성 가능
CREATE POLICY "Users can insert own conversations"
  ON conversations FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- 정책: 유저는 자기 대화만 수정 가능
CREATE POLICY "Users can update own conversations"
  ON conversations FOR UPDATE
  USING (auth.uid() = user_id);
```

RLS를 처음 세팅하면서 좀 헤맸는데, 요점은 `auth.uid()` 함수로 현재 로그인한 유저의 ID를 가져와서 `user_id` 컬럼과 비교하는 것이다.

---

## 데이터베이스 설계

### AI 앱에서 흔히 필요한 테이블들

```sql
-- 유저 프로필 (auth.users 확장)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  username TEXT UNIQUE,
  avatar_url TEXT,
  api_usage INTEGER DEFAULT 0,
  plan TEXT DEFAULT 'free',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- AI 대화 세션
CREATE TABLE chat_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  model TEXT DEFAULT 'claude-sonnet-4-20250514',
  system_prompt TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 대화 메시지
CREATE TABLE messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
  role TEXT CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  tokens_used INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- API 사용량 추적
CREATE TABLE api_usage (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  model TEXT,
  input_tokens INTEGER,
  output_tokens INTEGER,
  cost DECIMAL(10, 6),
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 회원가입 시 자동 프로필 생성 (트리거)

```sql
-- 함수: 새 유저 가입 시 프로필 자동 생성
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'username');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 트리거 연결
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### Python에서 CRUD 하기

```python
# 대화 세션 생성
result = supabase.table("chat_sessions").insert({
    "user_id": user_id,
    "model": "claude-sonnet-4-20250514",
    "system_prompt": "너는 친절한 코딩 도우미야."
}).execute()
session_id = result.data[0]["id"]

# 메시지 저장
supabase.table("messages").insert({
    "session_id": session_id,
    "role": "user",
    "content": "Python으로 피보나치 함수 만들어줘",
    "tokens_used": 15
}).execute()

# 대화 히스토리 조회 (최근 20개)
messages = supabase.table("messages") \
    .select("*") \
    .eq("session_id", session_id) \
    .order("created_at") \
    .limit(20) \
    .execute()

for msg in messages.data:
    print(f"[{msg['role']}] {msg['content'][:50]}...")

# API 사용량 집계
usage = supabase.table("api_usage") \
    .select("model, input_tokens, output_tokens, cost") \
    .eq("user_id", user_id) \
    .execute()
```

---

## pgvector로 벡터 검색 구현

여기가 Supabase를 AI 백엔드로 쓸 때 가장 강력한 부분이다. 별도의 벡터 DB 없이도 PostgreSQL에서 바로 임베딩 저장과 유사도 검색을 할 수 있다.

### pgvector 활성화

Supabase 대시보드에서 SQL Editor를 열고 실행한다.

```sql
-- pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;
```

### 문서 테이블 생성

```sql
-- 문서 + 임베딩 저장 테이블
CREATE TABLE documents (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  title TEXT,
  content TEXT NOT NULL,
  embedding vector(1536),  -- OpenAI text-embedding-3-small 차원
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 벡터 인덱스 (IVFFlat) - 검색 속도 향상
CREATE INDEX ON documents
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

`vector(1536)`은 OpenAI의 text-embedding-3-small 모델 차원이다. 다른 임베딩 모델을 쓴다면 차원 수를 맞춰야 한다.

| 임베딩 모델 | 차원 | 용도 |
|-------------|------|------|
| text-embedding-3-small | 1536 | 범용, 비용 효율 |
| text-embedding-3-large | 3072 | 고정밀 검색 |
| Cohere embed-v3 | 1024 | 다국어 특화 |
| BGE-M3 (오픈소스) | 1024 | 셀프호스팅 가능 |

### 유사도 검색 함수

```sql
-- 코사인 유사도 기반 검색 함수
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_threshold FLOAT DEFAULT 0.7,
  match_count INT DEFAULT 5,
  filter_user_id UUID DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  title TEXT,
  content TEXT,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.title,
    documents.content,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE
    (filter_user_id IS NULL OR documents.user_id = filter_user_id)
    AND 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

`<=>` 연산자가 코사인 거리를 계산한다. `1 - 거리`를 하면 유사도가 된다.

### Python에서 임베딩 저장 + 검색

```python
import openai

openai_client = openai.OpenAI()

def get_embedding(text: str) -> list[float]:
    """텍스트를 임베딩 벡터로 변환"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# 문서 저장 (임베딩 포함)
def store_document(user_id: str, title: str, content: str):
    embedding = get_embedding(content)

    result = supabase.table("documents").insert({
        "user_id": user_id,
        "title": title,
        "content": content,
        "embedding": embedding,
        "metadata": {"source": "manual", "language": "ko"}
    }).execute()

    return result.data[0]

# 유사 문서 검색
def search_documents(query: str, user_id: str = None, top_k: int = 5):
    query_embedding = get_embedding(query)

    result = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_threshold": 0.7,
        "match_count": top_k,
        "filter_user_id": user_id
    }).execute()

    return result.data

# 사용 예시
store_document(
    user_id="user-uuid",
    title="Python 비동기 프로그래밍",
    content="asyncio는 Python에서 비동기 I/O를 처리하는 표준 라이브러리입니다..."
)

results = search_documents("파이썬에서 동시성 처리하는 방법")
for doc in results:
    print(f"[{doc['similarity']:.3f}] {doc['title']}")
    print(f"  {doc['content'][:100]}...")
```

직접 써보니 Pinecone이나 Weaviate 같은 전용 벡터 DB보다 초기 설정이 훨씬 간단하다. 다만 수백만 건 이상으로 스케일이 커지면 전용 벡터 DB가 더 나을 수 있다.

---

## Edge Functions로 AI API 프록시

클라이언트에서 직접 OpenAI나 Anthropic API를 호출하면 API 키가 노출된다. Edge Functions를 중간 프록시로 쓰면 키를 안전하게 서버에 둘 수 있다.

### Edge Function 생성

```bash
# Supabase CLI 설치
npm install -g supabase

# Edge Function 생성
supabase functions new ai-chat
```

### AI 챗 Edge Function

```typescript
// supabase/functions/ai-chat/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // 인증 확인
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    )

    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      return new Response(JSON.stringify({ error: '인증 필요' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // 요청 파싱
    const { messages, model = 'claude-sonnet-4-20250514' } = await req.json()

    // Claude API 호출
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': Deno.env.get('ANTHROPIC_API_KEY')!,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model,
        max_tokens: 1024,
        messages,
      }),
    })

    const aiResponse = await response.json()

    // 사용량 기록
    await supabase.from('api_usage').insert({
      user_id: user.id,
      model,
      input_tokens: aiResponse.usage?.input_tokens || 0,
      output_tokens: aiResponse.usage?.output_tokens || 0,
      cost: calculateCost(model, aiResponse.usage),
    })

    return new Response(JSON.stringify(aiResponse), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})

function calculateCost(model: string, usage: any): number {
  const pricing: Record<string, { input: number; output: number }> = {
    'claude-sonnet-4-20250514': { input: 3.0, output: 15.0 },
    'claude-haiku-4-20250514': { input: 0.80, output: 4.0 },
  }
  const p = pricing[model] || pricing['claude-sonnet-4-20250514']
  return (usage.input_tokens * p.input + usage.output_tokens * p.output) / 1_000_000
}
```

### Edge Function 배포

```bash
# 환경 변수 설정
supabase secrets set ANTHROPIC_API_KEY=sk-ant-...

# 배포
supabase functions deploy ai-chat

# 테스트
curl -X POST https://your-project.supabase.co/functions/v1/ai-chat \
  -H "Authorization: Bearer USER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "안녕하세요"}],
    "model": "claude-sonnet-4-20250514"
  }'
```

---

## RAG 시스템 구현 (전체 흐름)

지금까지 만든 것들을 합치면 Supabase 하나로 완전한 RAG 시스템을 만들 수 있다.

```
[사용자 질문]
     ↓
[Edge Function] ← 인증 확인
     ↓
[임베딩 생성] ← OpenAI Embedding API
     ↓
[pgvector 검색] ← match_documents() 호출
     ↓
[컨텍스트 + 질문 결합]
     ↓
[LLM 응답 생성] ← Claude API
     ↓
[결과 반환 + 사용량 기록]
```

### RAG Edge Function

```typescript
// supabase/functions/rag-query/index.ts
serve(async (req) => {
  // ... 인증 생략 (위와 동일)

  const { query } = await req.json()

  // 1. 쿼리 임베딩 생성
  const embeddingResponse = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'text-embedding-3-small',
      input: query,
    }),
  })
  const { data } = await embeddingResponse.json()
  const queryEmbedding = data[0].embedding

  // 2. 유사 문서 검색
  const { data: documents } = await supabase.rpc('match_documents', {
    query_embedding: queryEmbedding,
    match_threshold: 0.7,
    match_count: 5,
    filter_user_id: user.id,
  })

  // 3. 컨텍스트 구성
  const context = documents
    .map((doc: any) => `[${doc.title}]\n${doc.content}`)
    .join('\n\n---\n\n')

  // 4. LLM 응답 생성
  const aiResponse = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': Deno.env.get('ANTHROPIC_API_KEY')!,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      system: `다음 문서를 참고하여 질문에 답변하세요.\n\n${context}`,
      messages: [{ role: 'user', content: query }],
    }),
  })

  return new Response(JSON.stringify(await aiResponse.json()), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  })
})
```

---

## 실시간 기능 활용

Supabase Realtime으로 AI 응답을 실시간으로 받을 수 있다. 예를 들어, 한 유저가 질문하면 같은 채널의 다른 유저에게도 바로 보이게 할 수 있다.

```javascript
// 실시간 메시지 구독
const channel = supabase
  .channel('chat-room-1')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'messages',
      filter: `session_id=eq.${sessionId}`,
    },
    (payload) => {
      console.log('새 메시지:', payload.new)
      // UI 업데이트
      addMessageToUI(payload.new)
    }
  )
  .subscribe()

// 구독 해제
// channel.unsubscribe()
```

---

## 파일 저장소 (Storage) 활용

AI 앱에서 사용자가 업로드한 파일(PDF, 이미지 등)을 처리해야 할 때 Storage를 쓴다.

```python
# 버킷 생성 (대시보드에서도 가능)
supabase.storage.create_bucket("user-documents", {
    "public": False,
    "file_size_limit": 10485760,  # 10MB
    "allowed_mime_types": ["application/pdf", "text/plain", "image/*"]
})

# 파일 업로드
with open("report.pdf", "rb") as f:
    supabase.storage.from_("user-documents").upload(
        f"/{user_id}/report.pdf",
        f,
        {"content-type": "application/pdf"}
    )

# 파일 다운로드
data = supabase.storage.from_("user-documents").download(
    f"/{user_id}/report.pdf"
)
```

---

## 프로젝트 전체 구조

실제 AI 앱 프로젝트를 Supabase로 구성하면 이런 디렉터리 구조가 된다.

```
my-ai-app/
├── supabase/
│   ├── functions/
│   │   ├── ai-chat/
│   │   │   └── index.ts
│   │   └── rag-query/
│   │       └── index.ts
│   ├── migrations/
│   │   ├── 001_create_tables.sql
│   │   ├── 002_enable_pgvector.sql
│   │   ├── 003_create_documents.sql
│   │   └── 004_rls_policies.sql
│   └── config.toml
├── frontend/               # Next.js, React 등
│   ├── src/
│   │   ├── lib/
│   │   │   └── supabase.ts
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx
│   │   │   └── DocumentUploader.tsx
│   │   └── app/
│   │       ├── chat/
│   │       └── auth/
│   └── package.json
├── scripts/
│   ├── seed_documents.py   # 초기 문서 임베딩
│   └── migrate.py
├── .env.local
└── README.md
```

### 마이그레이션 관리

```bash
# 새 마이그레이션 생성
supabase migration new create_documents_table

# 로컬에서 마이그레이션 실행
supabase db reset

# 프로덕션에 적용
supabase db push
```

---

## 비용 및 한계

### 무료 티어로 어디까지?

| 항목 | 무료 (Free) | Pro ($25/월) |
|------|------------|-------------|
| DB 크기 | 500MB | 8GB |
| 스토리지 | 1GB | 100GB |
| Edge Function 호출 | 50만/월 | 200만/월 |
| Realtime 동시접속 | 200 | 500 |
| 프로젝트 수 | 2개 | 무제한 |

사이드 프로젝트나 프로토타입이라면 무료 티어로 충분하다. 나는 사이드 프로젝트 3개를 무료 티어로 운영하고 있는데, DB 용량만 주의하면 별문제 없었다.

### 한계점

pgvector가 편리하긴 한데 몇 가지 제약이 있다.

- 벡터 수가 100만 건 넘어가면 전용 벡터 DB 대비 검색 속도가 느려질 수 있음
- HNSW 인덱스를 쓰면 개선되지만, 메모리 사용량이 늘어남
- 멀티모달 검색(이미지 + 텍스트 동시 검색) 같은 고급 기능은 제한적

대규모 서비스라면 Supabase(인증/데이터) + Pinecone(벡터 검색) 조합도 고려해볼 만하다.

---

## 나가며

Supabase는 AI 앱 백엔드를 빠르게 구축하는 데 현재 가장 실용적인 선택이다. 인증, DB, 벡터 검색, 파일 저장, 실시간 기능, 서버리스 함수까지 하나의 플랫폼에서 해결되니까 초기 개발 속도가 확실히 빨라진다.

정리하면 이렇다.

1. 인증은 Supabase Auth로 소셜 로그인까지 빠르게 구현
2. PostgreSQL + RLS로 안전한 데이터 관리
3. pgvector로 벡터 검색까지 한 곳에서
4. Edge Functions로 API 키 보호 + 서버리스 로직
5. Realtime으로 실시간 기능 추가

AI 챗봇을 처음부터 만들어보고 싶다면 [AI 챗봇 만들기 가이드]({{< relref "posts/2025-12-31-ai-chatbot-build-guide.md" >}})를 먼저 보고, 거기에 Supabase 백엔드를 붙이는 식으로 진행하면 수월하다.

시작은 무료 티어로 프로토타입부터 만들어보자. PostgreSQL을 기반으로 하니까 나중에 마이그레이션하기도 쉽다.
