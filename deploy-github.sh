#!/bin/bash
# GitHub Pages 자동 배포 스크립트

set -e

DASHBOARD_DIR="/Users/zoelumos/.openclaw/workspace/dashboard"
DEPLOY_DIR="/tmp/zoe-dashboard"
REPO_URL="https://github.com/schul92/zoe-dashboard.git"

echo "🚀 Starting dashboard deployment..."

# 1. Python 스크립트 실행 (최신 데이터 생성)
cd "$DASHBOARD_DIR"
echo "📊 Generating AWS architecture diagram..."
python3 aws-diagram.py 2>/dev/null || echo "⚠️ AWS diagram failed (not critical)"

echo "📊 Generating workflow diagram..."
python3 workflow-diagram.py 2>/dev/null || echo "⚠️ Workflow diagram failed (not critical)"

# 2. Deploy 디렉토리 준비
if [ ! -d "$DEPLOY_DIR/.git" ]; then
    echo "📦 Cloning repo for first time..."
    rm -rf "$DEPLOY_DIR"
    git clone "$REPO_URL" "$DEPLOY_DIR"
fi

# 3. 최신 변경사항 가져오기
cd "$DEPLOY_DIR"
git pull origin main

# 4. 파일 동기화
echo "🔄 Syncing files..."
rsync -av --delete \
    --exclude='.git' \
    --exclude='deploy-github.sh' \
    --exclude='seo/data.json' \
    "$DASHBOARD_DIR/" "$DEPLOY_DIR/"

# 5. Git 커밋 & 푸시
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing changes..."
    git add .
    git commit -m "🔄 Auto-update dashboard - $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo "⬆️ Pushing to GitHub..."
    git push origin main
    
    echo "✅ Deployment complete!"
    echo "🌐 Live at: https://schul92.github.io/zoe-dashboard/"
else
    echo "✅ No changes to deploy"
fi
