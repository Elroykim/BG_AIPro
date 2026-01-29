#!/bin/bash
# ============================================================
# BG_AIPro -> AiKim 배포 스크립트 (Linux/Mac)
#
# hugo_site/의 콘텐츠를 AiKim 레포에 복사하고 push한다.
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_PATH="$(dirname "$SCRIPT_DIR")"
HUGO_SRC="$PROJECT_PATH/hugo_site"
DEPLOY_PATH="$(dirname "$PROJECT_PATH")/AiKim"

echo "============================================================"
echo " BG_AIPro -> AiKim 배포"
echo "============================================================"
echo ""

# 1. 경로 확인
if [ ! -f "$HUGO_SRC/hugo.yaml" ]; then
    echo "[ERROR] Hugo 사이트 없음: $HUGO_SRC"
    exit 1
fi
if [ ! -d "$DEPLOY_PATH/.git" ]; then
    echo "[ERROR] AiKim 레포 없음: $DEPLOY_PATH"
    echo "AiKim 레포를 먼저 클론하세요."
    exit 1
fi

# 2. AiKim 최신화
echo "[1/4] AiKim 레포 최신화..."
cd "$DEPLOY_PATH"
git pull origin main 2>/dev/null || true
echo ""

# 3. 동기화
echo "[2/4] 콘텐츠 동기화..."
rsync -av --delete --exclude='.git' --exclude='public' --exclude='resources' --exclude='.hugo_build.lock' "$HUGO_SRC/" "$DEPLOY_PATH/"
echo ""

# 4. 커밋 및 푸시
echo "[3/4] 커밋..."
cd "$DEPLOY_PATH"
git add -A
if ! git diff --cached --quiet; then
    git commit -m "deploy: 콘텐츠 업데이트 $(date '+%Y-%m-%d %H:%M')"
    echo ""
    echo "[4/4] 푸시..."
    git push origin main
    echo ""
    echo "============================================================"
    echo " 배포 완료! https://elroykim.github.io/AiKim/"
    echo "============================================================"
else
    echo "     변경사항 없음. 배포 건너뜀."
fi
