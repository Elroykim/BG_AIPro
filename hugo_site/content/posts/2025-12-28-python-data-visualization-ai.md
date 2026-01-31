---
title: "Python 데이터 시각화에 AI 붙여보기: ChatGPT로 차트 자동 생성"
date: 2025-12-28
description: "ChatGPT와 Claude를 활용해 Python 데이터 시각화를 자동화하는 방법. CSV 데이터에서 matplotlib, plotly 차트를 AI로 생성하고 수동 코딩과 비교합니다."
categories: [개발]
tags: [Python, 데이터 시각화, matplotlib, ChatGPT, AI 분석]
keywords: [Python 데이터 시각화, ChatGPT 차트 생성, matplotlib AI, plotly 자동화, AI 데이터 분석]
draft: true
cover:
  image: ""
  alt: ""
  hidden: false
slug: python-data-visualization-ai-chart-generation
---

데이터 분석 결과를 차트로 만들어야 하는데, matplotlib 문법이 자꾸 헷갈린다. 색상은 어떻게 바꾸더라, 범례 위치는... 매번 Stack Overflow를 뒤지다가 시간이 훌쩍 갔었는데, ChatGPT한테 "이 데이터로 차트 그려줘" 하니까 30초 만에 코드가 나온다.

직접 써보니 AI가 시각화 코드를 생성하는 건 확실히 빠르다. 대신 원하는 스타일로 다듬으려면 프롬프트 기술이 필요하다. 실제 데이터로 테스트한 결과와 팁을 정리해봤다.

---

## 기존 방식 vs AI 방식

matplotlib으로 차트를 그리는 기존 워크플로우와 AI를 활용한 워크플로우를 비교해보자.

```
[기존 방식]
데이터 준비 → matplotlib 문서 검색 → 코드 작성 → 실행 → 에러 수정
→ 스타일 조정 → Stack Overflow 검색 → 반복...
소요 시간: 30분 ~ 1시간

[AI 방식]
데이터 준비 → AI에 데이터 + 요구사항 전달 → 코드 생성 → 실행
→ 피드백으로 수정 요청 → 완성
소요 시간: 5분 ~ 15분
```

단순한 차트일수록 AI의 이득이 크고, 복잡한 커스텀 차트는 AI가 뼈대를 잡아주면 내가 미세 조정하는 식이 효율적이었다.

---

## 실습 데이터 준비

실습용 CSV 데이터를 먼저 만들어보자. 가상의 SaaS 스타트업 월별 매출 데이터다.

```python
import pandas as pd
import numpy as np

# 샘플 데이터 생성
np.random.seed(42)

months = pd.date_range('2025-01', periods=12, freq='M')
data = {
    '월': months.strftime('%Y-%m'),
    '매출': [1200, 1350, 1580, 1720, 1890, 2100,
             2350, 2580, 2450, 2780, 3100, 3500],
    '사용자수': [500, 620, 780, 920, 1050, 1230,
                1400, 1580, 1520, 1750, 2000, 2300],
    '이탈률': [8.2, 7.5, 6.8, 6.2, 5.8, 5.5,
              5.2, 4.8, 5.1, 4.5, 4.2, 3.8],
    '서비스': ['Basic']*4 + ['Pro']*4 + ['Enterprise']*4,
}

df = pd.DataFrame(data)
df.to_csv('startup_metrics.csv', index=False)
print(df.head())
```

```
        월    매출  사용자수  이탈률      서비스
0  2025-01  1200      500   8.2     Basic
1  2025-02  1350      620   7.5     Basic
2  2025-03  1580      780   6.8     Basic
3  2025-04  1720      920   6.2     Basic
4  2025-05  1890     1050   5.8       Pro
```

---

## ChatGPT에 차트 요청하기

### 기본 프롬프트

ChatGPT(또는 Claude)에 데이터를 보여주고 차트를 요청하는 기본 패턴이다.

```
[프롬프트]
다음 CSV 데이터로 월별 매출 추이 차트를 matplotlib으로 그려줘.
한국어 레이블, 깔끔한 스타일로.

월,매출,사용자수,이탈률
2025-01,1200,500,8.2
2025-02,1350,620,7.5
...
```

### AI가 생성한 코드

```python
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

# 한국어 폰트 설정
matplotlib.rcParams['font.family'] = 'NanumGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('startup_metrics.csv')

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df['월'], df['매출'], marker='o', color='#2196F3',
        linewidth=2, markersize=6, label='매출(만원)')

ax.fill_between(range(len(df)), df['매출'], alpha=0.1, color='#2196F3')

ax.set_title('월별 매출 추이', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('월', fontsize=12)
ax.set_ylabel('매출 (만원)', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('revenue_trend.png', dpi=150, bbox_inches='tight')
plt.show()
```

간단한 차트는 이렇게 한번에 나온다. 문제는 디테일이다.

---

## 프롬프트 잘 쓰는 법

AI에게 시각화를 요청할 때 프롬프트의 구체성에 따라 결과물 퀄리티가 확 달라진다.

### 나쁜 프롬프트

```
이 데이터로 그래프 그려줘.
```

이러면 AI가 알아서 차트 타입을 고르는데, 내가 원하는 것과 다를 확률이 높다.

### 좋은 프롬프트

```
다음 데이터로 matplotlib 차트를 그려줘.

요구사항:
1. 차트 타입: 이중 Y축 (좌: 매출 막대그래프, 우: 이탈률 꺾은선)
2. 색상: 매출은 #4CAF50 계열, 이탈률은 #FF5722
3. 스타일: 격자선 연하게, 배경 흰색
4. 한국어 레이블 (NanumGothic 폰트)
5. 범례는 우측 상단
6. 해상도: dpi=150, figsize=(14, 7)
7. 각 막대 위에 값 표시

데이터:
월,매출,이탈률
2025-01,1200,8.2
...
```

### AI 프롬프트 템플릿

내가 자주 쓰는 프롬프트 템플릿을 정리하면 이렇다.

```
[시각화 프롬프트 템플릿]

데이터: {데이터 또는 CSV 경로}
차트 타입: {bar/line/scatter/pie/heatmap/이중축/서브플롯}
라이브러리: {matplotlib/plotly/seaborn}
스타일:
  - 색상 팔레트: {구체적 색상 코드 or 팔레트명}
  - 폰트: {NanumGothic, 크기}
  - 사이즈: {figsize 또는 width x height}
  - 배경: {흰색/투명/다크}
추가 요소:
  - 값 레이블: {표시 여부, 위치}
  - 범례: {위치}
  - 제목/축 레이블: {구체적 텍스트}
  - 추세선: {필요 여부}
출력: {png/svg/html(plotly)}
```

---

## 실전 예제: 다양한 차트 생성

### 예제 1: 이중 Y축 차트

```
[프롬프트]
월별 매출(막대)과 이탈률(꺾은선)을 이중 Y축으로 그려줘.
매출은 파란 계열 막대, 이탈률은 빨간 꺾은선.
막대 위에 값 표시, 이탈률 포인트에도 값 표시.
```

AI가 생성한 코드를 실행하면 이런 결과가 나온다.

```python
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

matplotlib.rcParams['font.family'] = 'NanumGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('startup_metrics.csv')

fig, ax1 = plt.subplots(figsize=(14, 7))

# 매출 막대그래프 (좌측 Y축)
bars = ax1.bar(df['월'], df['매출'], color='#42A5F5', alpha=0.8,
               width=0.6, label='매출(만원)')
ax1.set_ylabel('매출 (만원)', fontsize=12, color='#1565C0')
ax1.tick_params(axis='y', labelcolor='#1565C0')

# 막대 위에 값 표시
for bar, val in zip(bars, df['매출']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
             f'{val:,}', ha='center', va='bottom', fontsize=9)

# 이탈률 꺾은선 (우측 Y축)
ax2 = ax1.twinx()
line = ax2.plot(df['월'], df['이탈률'], color='#EF5350', marker='s',
                linewidth=2, markersize=7, label='이탈률(%)')
ax2.set_ylabel('이탈률 (%)', fontsize=12, color='#C62828')
ax2.tick_params(axis='y', labelcolor='#C62828')

# 이탈률 값 표시
for x, y in zip(df['월'], df['이탈률']):
    ax2.annotate(f'{y}%', (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center', fontsize=9, color='#C62828')

ax1.set_title('월별 매출 vs 이탈률 추이', fontsize=16, fontweight='bold', pad=15)
ax1.set_xlabel('월', fontsize=12)

# 범례 합치기
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

ax1.grid(True, alpha=0.2)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('dual_axis_chart.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 예제 2: 인터랙티브 대시보드 (Plotly)

```
[프롬프트]
plotly로 인터랙티브 대시보드를 만들어줘.
서브플롯 4개: 매출 추이, 사용자수 추이, 이탈률 추이, 서비스별 매출 파이차트.
다크 테마, 호버 시 상세 정보 표시.
```

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

df = pd.read_csv('startup_metrics.csv')

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('매출 추이', '사용자수 추이', '이탈률 추이', '서비스별 매출'),
    specs=[[{"type": "scatter"}, {"type": "scatter"}],
           [{"type": "scatter"}, {"type": "pie"}]]
)

# 매출 추이
fig.add_trace(
    go.Scatter(x=df['월'], y=df['매출'], mode='lines+markers',
               name='매출', line=dict(color='#4FC3F7', width=2),
               hovertemplate='%{x}<br>매출: %{y:,}만원'),
    row=1, col=1
)

# 사용자수 추이
fig.add_trace(
    go.Scatter(x=df['월'], y=df['사용자수'], mode='lines+markers',
               name='사용자수', line=dict(color='#81C784', width=2),
               hovertemplate='%{x}<br>사용자: %{y:,}명'),
    row=1, col=2
)

# 이탈률 추이
fig.add_trace(
    go.Scatter(x=df['월'], y=df['이탈률'], mode='lines+markers',
               name='이탈률', line=dict(color='#FF8A65', width=2),
               fill='tozeroy', fillcolor='rgba(255,138,101,0.1)',
               hovertemplate='%{x}<br>이탈률: %{y}%'),
    row=2, col=1
)

# 서비스별 매출 파이차트
service_revenue = df.groupby('서비스')['매출'].sum()
fig.add_trace(
    go.Pie(labels=service_revenue.index, values=service_revenue.values,
           marker_colors=['#4FC3F7', '#81C784', '#FFB74D'],
           textinfo='label+percent'),
    row=2, col=2
)

fig.update_layout(
    template='plotly_dark',
    title='SaaS 스타트업 대시보드',
    height=800,
    showlegend=True,
    font=dict(size=12),
)

fig.write_html('dashboard.html')
fig.show()
```

plotly는 인터랙티브하게 동작해서 마우스 호버, 줌, 패닝이 다 되니까 발표 자료나 웹 대시보드에 좋다.

### 예제 3: 상관관계 히트맵 (Seaborn)

```
[프롬프트]
매출, 사용자수, 이탈률 간의 상관관계를 seaborn 히트맵으로 그려줘.
값 표시, 색상은 coolwarm, 한국어 레이블.
```

```python
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'NanumGothic'

df = pd.read_csv('startup_metrics.csv')
numeric_cols = ['매출', '사용자수', '이탈률']
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm',
            center=0, vmin=-1, vmax=1,
            square=True, linewidths=1, ax=ax,
            annot_kws={'size': 14})

ax.set_title('지표 간 상관관계', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## Code Interpreter 활용 팁

ChatGPT Plus의 Code Interpreter(Advanced Data Analysis)를 쓰면 CSV 파일을 직접 업로드하고 차트를 바로 실행할 수 있다.

### 효과적인 사용 방법

```
[Step 1] CSV 파일 업로드

[Step 2] 프롬프트
"이 데이터를 탐색해서 주요 인사이트 3가지를 찾고,
각 인사이트에 맞는 차트를 그려줘.
차트는 matplotlib 기반, 한국어, 깔끔한 스타일로."

[Step 3] 결과 확인 후 수정 요청
"두 번째 차트의 색상을 파스텔 톤으로 바꾸고,
추세선을 추가해줘."
```

### Code Interpreter vs 로컬 코딩

| 항목 | Code Interpreter | 로컬 Python |
|------|-----------------|------------|
| 환경 설정 | 불필요 | pip install 필요 |
| 파일 접근 | 업로드 필요 | 직접 접근 |
| 라이브러리 | 주요 라이브러리 사전 설치 | 자유롭게 설치 |
| 실행 속도 | 클라우드 (보통) | 로컬 하드웨어 의존 |
| 대용량 데이터 | 제한 있음 (~100MB) | 메모리 한도까지 |
| 자동화 | 수동 반복 | 스크립트 자동화 가능 |
| 비용 | ChatGPT Plus 구독 | API 비용 또는 무료 |

결론적으로 탐색적 분석(EDA)에는 Code Interpreter가 빠르고, 반복적인 리포트 생성에는 로컬 스크립트가 적합하다.

---

## AI로 생성한 코드 수정하기

AI가 생성한 차트 코드가 100% 완벽한 경우는 드물다. 보통 아래 같은 수정이 필요하다.

### 흔한 수정 사항

```python
# 1. 한국어 폰트가 깨질 때
import matplotlib
matplotlib.rcParams['font.family'] = 'NanumGothic'  # macOS: AppleGothic
matplotlib.rcParams['axes.unicode_minus'] = False

# 2. 날짜 축이 겹칠 때
plt.xticks(rotation=45, ha='right')
fig.autofmt_xdate()

# 3. 범례가 차트를 가릴 때
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# 4. 여백이 잘릴 때
plt.tight_layout()
plt.savefig('chart.png', dpi=150, bbox_inches='tight')

# 5. 색상이 구린 경우
# AI한테 "색상을 Material Design 팔레트로 바꿔줘" 하면 된다
colors = ['#1976D2', '#388E3C', '#F57C00', '#7B1FA2']
```

### AI에게 수정을 요청하는 팁

```
[비효율적]
"이거 좀 예쁘게 만들어줘"

[효율적]
"다음 수정을 해줘:
1. 배경색을 #FAFAFA로
2. 격자선을 점선으로 변경
3. 폰트 크기를 제목 18, 축 레이블 13, 눈금 11로
4. 범례를 차트 아래에 가로로 배치
5. Y축에 천 단위 콤마 포맷 적용"
```

수정 요청도 프롬프트처럼 구체적으로 해야 원하는 결과가 나온다.

---

## 수동 코딩 vs AI 생성 비교

실제로 같은 차트를 수동으로 코딩하는 것과 AI로 생성하는 것을 비교해봤다.

### 단순 꺾은선 그래프

| 항목 | 수동 코딩 | AI 생성 |
|------|----------|---------|
| 소요 시간 | 5분 | 1분 |
| 코드 품질 | 작성자 수준 의존 | 일관되게 깔끔 |
| 커스터마이징 | 자유로움 | 프롬프트 반복 필요 |
| 학습 효과 | 높음 | 낮음 |

### 복잡한 다중 서브플롯 대시보드

| 항목 | 수동 코딩 | AI 생성 |
|------|----------|---------|
| 소요 시간 | 30분~1시간 | 5~10분 |
| 코드 품질 | 경험에 따라 다름 | 대체로 중상 |
| 디버깅 | 본인이 직접 | AI에게 에러 메시지 전달 |
| 최종 품질 | 높음 (충분한 시간 투자 시) | 중상 (미세 조정 필요) |

내 경험으로는 AI가 80% 정도의 완성도를 빠르게 뽑아주고, 나머지 20%는 직접 손보는 게 가장 효율적이다.

---

## 자동화 워크플로우

주기적인 데이터 리포트를 자동으로 생성하고 싶다면 이런 파이프라인을 만들 수 있다.

```python
import anthropic
import pandas as pd
import subprocess
import os

client = anthropic.Anthropic()

def auto_generate_chart(csv_path: str, requirements: str):
    """AI에게 CSV 데이터와 요구사항을 전달하여 차트 코드 자동 생성"""

    df = pd.read_csv(csv_path)
    data_sample = df.head(5).to_string()
    data_info = f"컬럼: {list(df.columns)}\n행 수: {len(df)}\n데이터 타입:\n{df.dtypes.to_string()}"

    prompt = f"""다음 데이터로 Python matplotlib 차트를 그리는 코드를 작성해줘.

데이터 정보:
{data_info}

데이터 샘플:
{data_sample}

요구사항:
{requirements}

코드만 출력해줘. 설명 없이 ```python ``` 블록 안에 완성된 코드만.
파일 경로는 '{csv_path}'로 읽어야 해.
저장 경로는 'generated_chart.png'으로.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    # 코드 추출
    code = response.content[0].text
    code = code.split("```python")[1].split("```")[0].strip()

    # 코드 저장 및 실행
    with open("temp_chart.py", "w") as f:
        f.write(code)

    result = subprocess.run(["python", "temp_chart.py"], capture_output=True, text=True)

    if result.returncode == 0:
        print("차트 생성 성공: generated_chart.png")
    else:
        print(f"에러 발생:\n{result.stderr}")

    os.remove("temp_chart.py")
    return result.returncode == 0

# 사용 예시
auto_generate_chart(
    "startup_metrics.csv",
    """
    - 이중 Y축: 좌측에 매출 막대, 우측에 이탈률 꺾은선
    - 서비스 구간별로 배경색을 다르게 (Basic: 파랑, Pro: 초록, Enterprise: 주황)
    - 한국어 레이블, NanumGothic 폰트
    - 제목: '2025년 SaaS 성장 지표'
    - 깔끔한 흰색 배경, 격자선은 점선
    """
)
```

---

## Plotly vs Matplotlib: 언제 뭘 쓸까

| 상황 | 추천 라이브러리 |
|------|---------------|
| 논문/보고서 정적 이미지 | matplotlib |
| 웹 대시보드 | plotly |
| 탐색적 분석 | plotly (인터랙티브) |
| 자동화 스크립트 | matplotlib |
| 프레젠테이션 | plotly 또는 matplotlib |
| Jupyter 노트북 | 둘 다 OK |

matplotlib은 정적 이미지 품질이 높고 커스터마이징이 세밀해서 논문이나 보고서에 적합하고, plotly는 인터랙티브 기능이 강력해서 웹 기반 대시보드에 적합하다.

---

## 추천 프롬프트 모음

자주 쓰는 차트별 프롬프트를 정리해뒀다. 복사해서 데이터만 바꿔 쓰면 된다.

### 시계열 차트

```
{데이터}를 시계열 꺾은선 그래프로 그려줘.
이동평균(7일) 추세선 추가, 주말은 회색 배경으로 표시.
Y축은 천 단위 콤마 포맷.
```

### 비교 막대 차트

```
{데이터}를 그룹별 가로 막대 차트로 그려줘.
내림차순 정렬, 각 막대 끝에 값 표시.
색상은 카테고리별로 다르게.
```

### 분포 차트

```
{데이터}의 분포를 히스토그램 + KDE 곡선으로 그려줘.
평균과 중앙값을 점선으로 표시.
통계 요약 텍스트박스 추가.
```

### 비율 차트

```
{데이터}를 도넛 차트로 그려줘.
중앙에 총합 표시, 각 조각에 레이블 + 퍼센트 표시.
파스텔 색상 팔레트.
```

---

## 요점 정리

AI를 데이터 시각화에 활용하면 생산성이 확실히 올라간다. 특히 matplotlib 문법을 자주 잊어버리는 사람(나 포함)에게는 구원 같은 도구다.

핵심 포인트를 정리하면 이렇다.

1. 프롬프트를 구체적으로 쓰자 -- 차트 타입, 색상, 크기, 폰트까지 명시
2. AI가 80% 만들고 내가 20% 다듬는 게 최적의 워크플로우
3. 탐색적 분석은 Code Interpreter, 자동화는 로컬 스크립트
4. plotly는 인터랙티브, matplotlib은 정적 이미지에 각각 강점
5. 자주 쓰는 프롬프트는 템플릿으로 저장해두면 편하다

데이터 분석을 좀 더 체계적으로 해보고 싶다면 [AI 데이터 분석 입문 가이드]({{< relref "posts/2026-01-20-ai-data-analysis-beginners.md" >}})도 같이 읽어보면 도움이 된다.

matplotlib 코드를 처음부터 외울 필요는 없다. AI한테 뼈대를 뽑아달라고 하고, 내가 원하는 방향으로 다듬는 습관을 들이면 데이터 시각화가 훨씬 빨라진다.
