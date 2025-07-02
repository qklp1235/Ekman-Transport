#!/bin/bash

# 🚀 GitHub 자동 업로드 스크립트
# 사용법: ./auto_push.sh "커밋 메시지"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌊 Ekman Transport Visualizer - GitHub 자동 업로드${NC}"
echo "=================================================="

# 커밋 메시지 설정
if [ -z "$1" ]; then
    COMMIT_MSG="others"
    echo -e "${YELLOW}⚠️  커밋 메시지가 없습니다. 기본값 'others'를 사용합니다.${NC}"
else
    COMMIT_MSG="$1"
fi

echo -e "${BLUE}📝 커밋 메시지: ${GREEN}$COMMIT_MSG${NC}"

# Git 상태 확인
echo -e "\n${BLUE}📊 Git 상태 확인 중...${NC}"
git status --porcelain

# Git add
echo -e "\n${BLUE}📁 파일 추가 중...${NC}"
git add .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ git add 완료${NC}"
else
    echo -e "${RED}❌ git add 실패${NC}"
    exit 1
fi

# Git commit
echo -e "\n${BLUE}💾 커밋 중...${NC}"
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ git commit 완료${NC}"
else
    echo -e "${YELLOW}⚠️  커밋할 변경사항이 없거나 커밋에 실패했습니다.${NC}"
fi

# Git push
echo -e "\n${BLUE}🚀 GitHub에 업로드 중...${NC}"
git push origin main

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}🎉 GitHub 업로드 완료!${NC}"
    echo -e "${GREEN}✨ 모든 변경사항이 성공적으로 업로드되었습니다.${NC}"
else
    echo -e "\n${RED}❌ GitHub 업로드 실패${NC}"
    echo -e "${YELLOW}💡 GitHub 레포지토리가 연결되어 있는지 확인해주세요.${NC}"
    echo -e "${YELLOW}   git remote -v 명령어로 확인 가능합니다.${NC}"
    exit 1
fi

echo -e "\n${BLUE}=================================================="
echo -e "🔗 GitHub 레포지토리에서 확인해보세요!${NC}" 