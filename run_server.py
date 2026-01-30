"""Resume API 서버 실행 스크립트."""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Resume API 서버 시작: http://localhost:{port}")
    print(f"API 문서: http://localhost:{port}/docs")
    uvicorn.run("src.resume.api:app", host="0.0.0.0", port=port, reload=True)
