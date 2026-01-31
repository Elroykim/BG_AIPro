---
title: "Vercel AI SDK로 AI 챗봇 10분만에 배포하기: Next.js + 스트리밍"
date: 2026-01-03
description: "Vercel AI SDK와 Next.js를 사용해 스트리밍 AI 챗봇을 만들고 배포하는 과정. 멀티 프로바이더 지원, UI 컴포넌트, 프로덕션 배포까지 실전 코드로 설명합니다."
categories: [개발]
tags: [Vercel, AI SDK, Next.js, 챗봇 배포, 스트리밍]
keywords: [Vercel AI SDK, Next.js AI 챗봇, AI 스트리밍 배포, Vercel 챗봇 만들기, AI SDK 튜토리얼]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: vercel-ai-sdk-chatbot-nextjs-deploy
---

Streamlit으로 AI 앱 프로토타입을 만들다가 "이걸 제대로 된 웹으로 만들고 싶다"는 생각이 들었다. Next.js에 AI SDK를 붙여보니 스트리밍 응답이 기본으로 되고, 배포도 `git push` 한 번이면 끝나더라. ChatGPT처럼 글자가 한 글자씩 나타나는 그 효과가 SDK 내장 기능으로 바로 되는 게 좀 놀라웠다.

Vercel AI SDK로 Next.js 기반 AI 챗봇을 만들고 배포하는 전체 과정을 정리한다.

---

## Vercel AI SDK란?

Vercel에서 만든 오픈소스 라이브러리로, AI 모델을 웹앱에 통합하는 데 필요한 기능을 제공한다. 핵심 특징은 이렇다.

```
[Vercel AI SDK 핵심]
├── ai (Core)        → LLM 호출, 스트리밍, 도구 사용
├── @ai-sdk/openai   → OpenAI 프로바이더
├── @ai-sdk/anthropic → Anthropic 프로바이더
├── @ai-sdk/google   → Google AI 프로바이더
└── @ai-sdk/ui       → React/Svelte/Vue 훅
```

### 왜 AI SDK인가?

| 항목 | 직접 구현 | Vercel AI SDK |
|------|----------|---------------|
| 스트리밍 응답 | fetch + ReadableStream 수동 구현 | `streamText()` 한 줄 |
| UI 상태 관리 | useState, useEffect 조합 | `useChat()` 훅 |
| 프로바이더 전환 | API 코드 전면 수정 | 프로바이더만 교체 |
| 에러 처리 | 수동 구현 | 내장 |
| 도구 사용 | 직접 파싱 | 타입 안전 도구 정의 |
| 타입 안전성 | 별도 정의 | TypeScript 네이티브 |

---

## 프로젝트 세팅

### Next.js + AI SDK 초기화

```bash
# Next.js 프로젝트 생성
npx create-next-app@latest ai-chatbot --typescript --tailwind --app --src-dir
cd ai-chatbot

# AI SDK 설치
npm install ai @ai-sdk/openai @ai-sdk/anthropic
```

### 환경 변수

```bash
# .env.local
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 프로젝트 구조

```
ai-chatbot/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── chat/
│   │   │       └── route.ts    ← API 엔드포인트
│   │   ├── page.tsx            ← 메인 채팅 UI
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageBubble.tsx
│   │   └── ModelSelector.tsx
│   └── lib/
│       └── providers.ts        ← AI 프로바이더 설정
├── .env.local
├── next.config.js
└── package.json
```

---

## 기본 챗봇 구현

### Step 1: API 라우트

```typescript
// src/app/api/chat/route.ts
import { streamText } from 'ai'
import { openai } from '@ai-sdk/openai'

export const maxDuration = 30

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: openai('gpt-4o'),
    system: '당신은 친절한 한국어 AI 어시스턴트입니다. 개발 관련 질문에 특화되어 있습니다.',
    messages,
  })

  return result.toDataStreamResponse()
}
```

끝이다. 이게 스트리밍 API의 전부다. `streamText`가 모델 호출과 스트리밍을 다 처리해준다.

### Step 2: 채팅 UI

```tsx
// src/app/page.tsx
'use client'

import { useChat } from '@ai-sdk/react'

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } = useChat()

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">AI 챗봇</h1>

      {/* 메시지 목록 */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-2xl px-4 py-2 ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl px-4 py-2">
              <span className="animate-pulse">생각하는 중...</span>
            </div>
          </div>
        )}
      </div>

      {/* 에러 표시 */}
      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4">
          오류가 발생했습니다: {error.message}
        </div>
      )}

      {/* 입력 폼 */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="메시지를 입력하세요..."
          className="flex-1 border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="bg-blue-500 text-white px-6 py-3 rounded-xl hover:bg-blue-600 disabled:opacity-50 transition-colors"
        >
          전송
        </button>
      </form>
    </div>
  )
}
```

`useChat()` 훅이 메시지 상태, 입력 관리, 서버 통신, 스트리밍 수신을 다 처리한다. 직접 구현하면 코드가 3~4배는 더 많아졌을 것이다.

---

## 멀티 프로바이더 지원

AI SDK의 강점은 프로바이더 전환이 쉽다는 것이다. 코드 한 줄만 바꾸면 OpenAI에서 Anthropic으로, Google로 바꿀 수 있다.

### 프로바이더 설정

```typescript
// src/lib/providers.ts
import { openai } from '@ai-sdk/openai'
import { anthropic } from '@ai-sdk/anthropic'

export const models = {
  'gpt-4o': openai('gpt-4o'),
  'gpt-4o-mini': openai('gpt-4o-mini'),
  'claude-sonnet': anthropic('claude-sonnet-4-20250514'),
  'claude-haiku': anthropic('claude-haiku-4-20250514'),
} as const

export type ModelId = keyof typeof models
```

### 모델 선택 가능한 API 라우트

```typescript
// src/app/api/chat/route.ts
import { streamText } from 'ai'
import { models, type ModelId } from '@/lib/providers'

export const maxDuration = 30

export async function POST(req: Request) {
  const { messages, model: modelId = 'claude-sonnet' } = await req.json()

  const model = models[modelId as ModelId]

  if (!model) {
    return new Response(JSON.stringify({ error: '지원하지 않는 모델입니다' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  const result = streamText({
    model,
    system: '당신은 친절한 한국어 AI 어시스턴트입니다.',
    messages,
    temperature: 0.7,
    maxTokens: 2048,
  })

  return result.toDataStreamResponse()
}
```

### 모델 선택 UI

```tsx
// src/components/ModelSelector.tsx
'use client'

import { type ModelId } from '@/lib/providers'

const modelOptions: { id: ModelId; name: string; description: string }[] = [
  { id: 'gpt-4o', name: 'GPT-4o', description: '가장 스마트' },
  { id: 'gpt-4o-mini', name: 'GPT-4o Mini', description: '빠르고 저렴' },
  { id: 'claude-sonnet', name: 'Claude Sonnet', description: '균형 잡힌 성능' },
  { id: 'claude-haiku', name: 'Claude Haiku', description: '초고속 응답' },
]

interface Props {
  selected: ModelId
  onChange: (model: ModelId) => void
}

export function ModelSelector({ selected, onChange }: Props) {
  return (
    <div className="flex gap-2 flex-wrap">
      {modelOptions.map((model) => (
        <button
          key={model.id}
          onClick={() => onChange(model.id)}
          className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
            selected === model.id
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
          }`}
        >
          <span className="font-medium">{model.name}</span>
          <span className="text-xs ml-1 opacity-70">{model.description}</span>
        </button>
      ))}
    </div>
  )
}
```

### 메인 페이지에 모델 선택 추가

```tsx
// src/app/page.tsx (업데이트)
'use client'

import { useChat } from '@ai-sdk/react'
import { useState } from 'react'
import { ModelSelector } from '@/components/ModelSelector'
import { type ModelId } from '@/lib/providers'

export default function ChatPage() {
  const [selectedModel, setSelectedModel] = useState<ModelId>('claude-sonnet')

  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    body: {
      model: selectedModel,
    },
  })

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <div className="mb-4">
        <h1 className="text-2xl font-bold mb-2">AI 챗봇</h1>
        <ModelSelector selected={selectedModel} onChange={setSelectedModel} />
      </div>

      {/* ... 나머지 UI는 동일 */}
    </div>
  )
}
```

---

## 도구 사용 (Tool Use)

AI가 날씨를 조회하거나 계산을 하는 등의 "도구"를 사용할 수 있다.

```typescript
// src/app/api/chat/route.ts
import { streamText, tool } from 'ai'
import { anthropic } from '@ai-sdk/anthropic'
import { z } from 'zod'

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: anthropic('claude-sonnet-4-20250514'),
    system: '당신은 도구를 활용할 수 있는 AI 어시스턴트입니다.',
    messages,
    tools: {
      // 날씨 조회 도구
      getWeather: tool({
        description: '특정 도시의 현재 날씨를 조회합니다',
        parameters: z.object({
          city: z.string().describe('도시 이름 (예: 서울, 부산)'),
        }),
        execute: async ({ city }) => {
          // 실제로는 날씨 API 호출
          const mockWeather: Record<string, string> = {
            '서울': '맑음, 5°C',
            '부산': '흐림, 8°C',
            '제주': '비, 10°C',
          }
          return mockWeather[city] || `${city}의 날씨 정보를 찾을 수 없습니다`
        },
      }),

      // 계산 도구
      calculate: tool({
        description: '수학 계산을 수행합니다',
        parameters: z.object({
          expression: z.string().describe('계산식 (예: 2 + 3 * 4)'),
        }),
        execute: async ({ expression }) => {
          try {
            const result = Function(`'use strict'; return (${expression})`)()
            return `${expression} = ${result}`
          } catch {
            return '계산할 수 없는 수식입니다'
          }
        },
      }),

      // 웹 검색 도구 (예시)
      searchWeb: tool({
        description: '웹에서 정보를 검색합니다',
        parameters: z.object({
          query: z.string().describe('검색어'),
        }),
        execute: async ({ query }) => {
          // 실제로는 검색 API 호출
          return `"${query}" 검색 결과: 관련 정보를 찾았습니다.`
        },
      }),
    },
    maxSteps: 5,  // 도구 호출 최대 횟수
  })

  return result.toDataStreamResponse()
}
```

`zod`로 파라미터 스키마를 정의하니까 타입 안전하게 도구를 만들 수 있다.

---

## 스트리밍 응답 커스터마이징

### 마크다운 렌더링

AI 응답에 마크다운이 포함될 때 렌더링하려면 `react-markdown`을 쓴다.

```bash
npm install react-markdown remark-gfm
```

```tsx
// src/components/MessageBubble.tsx
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface Props {
  role: 'user' | 'assistant'
  content: string
}

export function MessageBubble({ role, content }: Props) {
  if (role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="bg-blue-500 text-white rounded-2xl px-4 py-2 max-w-[70%]">
          {content}
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="bg-gray-100 rounded-2xl px-4 py-2 max-w-[70%] prose prose-sm">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      </div>
    </div>
  )
}
```

### 코드 하이라이팅

```bash
npm install react-syntax-highlighter @types/react-syntax-highlighter
```

```tsx
// MessageBubble.tsx에 추가
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

// ReactMarkdown의 components prop에 코드 블록 커스텀
<ReactMarkdown
  remarkPlugins={[remarkGfm]}
  components={{
    code({ className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || '')
      const isInline = !match

      return isInline ? (
        <code className="bg-gray-200 px-1 rounded text-sm" {...props}>
          {children}
        </code>
      ) : (
        <SyntaxHighlighter
          style={oneDark}
          language={match[1]}
          PreTag="div"
          className="rounded-lg text-sm"
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      )
    },
  }}
>
  {content}
</ReactMarkdown>
```

---

## Vercel AI SDK vs Streamlit 비교

[Streamlit으로 AI 웹앱 만들기]({{< relref "posts/2025-12-29-streamlit-ai-webapp-tutorial.md" >}})와 비교해보면 각각의 장단점이 뚜렷하다.

| 항목 | Vercel AI SDK + Next.js | Streamlit |
|------|------------------------|-----------|
| 언어 | TypeScript/JavaScript | Python |
| 학습 곡선 | React 지식 필요 | Python만 알면 됨 |
| UI 자유도 | 무제한 (HTML/CSS) | 제한적 (위젯 기반) |
| 스트리밍 | 네이티브 지원 | `st.write_stream` |
| 성능 | 높음 (Edge Runtime) | 보통 |
| 배포 | Vercel (무료) | Streamlit Cloud (무료) |
| SEO | 가능 (SSR) | 불가 |
| 프로덕션 적합도 | 높음 | 보통 |
| 개발 속도 | 보통 | 매우 빠름 |

결론: 프로토타입은 Streamlit, 프로덕션은 Vercel AI SDK. 나는 내부 데모나 빠른 검증에는 Streamlit을 쓰고, 외부에 공개할 서비스는 Next.js + AI SDK로 만든다.

---

## Vercel에 배포하기

### Git 저장소 연결

```bash
# GitHub에 push
git init
git add .
git commit -m "Initial AI chatbot"
git remote add origin https://github.com/username/ai-chatbot.git
git push -u origin main
```

### Vercel 배포

1. [vercel.com](https://vercel.com) 접속
2. New Project > GitHub 저장소 선택
3. Environment Variables에 API 키 추가
4. Deploy 클릭

```
환경 변수 설정:
- OPENAI_API_KEY: sk-...
- ANTHROPIC_API_KEY: sk-ant-...
```

배포가 끝나면 `https://your-app.vercel.app` 주소가 생긴다. 이후에는 `git push`만 하면 자동 배포된다.

### 커스텀 도메인

```
Vercel Dashboard > Project > Settings > Domains
→ 커스텀 도메인 추가 (예: chat.mysite.com)
→ DNS 레코드 설정 안내 따르기
```

---

## 프로덕션 고려사항

### Rate Limiting

```typescript
// src/app/api/chat/route.ts
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'),  // 분당 10회
})

export async function POST(req: Request) {
  // IP 기반 rate limit
  const ip = req.headers.get('x-forwarded-for') ?? '127.0.0.1'
  const { success } = await ratelimit.limit(ip)

  if (!success) {
    return new Response(JSON.stringify({ error: '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.' }), {
      status: 429,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // ... 기존 챗봇 로직
}
```

### 에러 처리

```typescript
// src/app/api/chat/route.ts
export async function POST(req: Request) {
  try {
    const { messages, model: modelId } = await req.json()

    // 입력 검증
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return new Response(JSON.stringify({ error: '메시지가 비어있습니다' }), {
        status: 400,
      })
    }

    // 메시지 길이 제한
    const lastMessage = messages[messages.length - 1]
    if (lastMessage.content.length > 4000) {
      return new Response(JSON.stringify({ error: '메시지가 너무 깁니다 (4000자 이내)' }), {
        status: 400,
      })
    }

    const result = streamText({
      model: models[modelId as ModelId] || models['claude-sonnet'],
      messages,
      // ...
    })

    return result.toDataStreamResponse()
  } catch (error) {
    console.error('Chat API error:', error)
    return new Response(JSON.stringify({ error: '서버 오류가 발생했습니다' }), {
      status: 500,
    })
  }
}
```

### 비용 모니터링

```typescript
// 응답에서 토큰 사용량 추적
const result = streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages,
  onFinish: async ({ usage }) => {
    console.log(`입력 토큰: ${usage.promptTokens}`)
    console.log(`출력 토큰: ${usage.completionTokens}`)

    // DB에 사용량 저장 (Supabase, Prisma 등)
    // await saveUsage(userId, usage)
  },
})
```

---

## 전체 코드 요약

최소한의 파일로 동작하는 전체 코드를 정리한다.

```
필요한 파일:
1. src/app/api/chat/route.ts  → API 엔드포인트 (10줄)
2. src/app/page.tsx           → 채팅 UI (40줄)
3. src/lib/providers.ts       → 모델 설정 (10줄)
4. .env.local                 → API 키
```

총 코드량이 60줄 정도면 스트리밍 AI 챗봇이 완성된다. `useChat()` 훅이 상태 관리를 다 해주니까 boilerplate가 거의 없다.

---

## 다음 단계

기본 챗봇을 만든 후에 추가할 만한 기능들이다.

- 대화 저장: Supabase나 Prisma로 대화 히스토리 저장
- 파일 업로드: 이미지, PDF 등 멀티모달 입력 지원
- RAG: 문서 기반 질의응답 기능 추가
- 인증: NextAuth.js로 사용자 로그인 구현
- 분석: PostHog이나 Vercel Analytics로 사용 현황 추적

프로토타입에서 프로덕션까지, Vercel AI SDK + Next.js 조합이면 대부분의 AI 웹 서비스를 커버할 수 있다. 복잡한 셋업 없이 `git push`로 배포되는 경험은 한번 맛보면 돌아가기 어렵다.
