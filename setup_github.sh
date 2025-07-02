#!/bin/bash

# 🔧 GitHub 연결 설정 도우미 스크립트

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🔧 GitHub 연결 설정 도우미${NC}"
echo "========================================="

# 1. GitHub 레포지토리 URL 입력받기
echo -e "\n${BLUE}📝 GitHub 레포지토리 정보를 입력해주세요:${NC}"
echo -e "${YELLOW}예시: https://github.com/사용자명/레포지토리명.git${NC}"
read -p "GitHub 레포지토리 URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo -e "${RED}❌ 레포지토리 URL이 필요합니다.${NC}"
    exit 1
fi

# 2. 원격 저장소 연결
echo -e "\n${BLUE}🔗 GitHub 레포지토리 연결 중...${NC}"
git remote add origin "$REPO_URL"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ GitHub 레포지토리 연결 완료${NC}"
else
    echo -e "${YELLOW}⚠️  이미 연결되어 있거나 오류가 발생했습니다.${NC}"
    echo -e "${BLUE}현재 연결된 원격 저장소:${NC}"
    git remote -v
fi

# 3. 초기 커밋 및 업로드
echo -e "\n${BLUE}📤 초기 파일 업로드 중...${NC}"
git add .
git commit -m "🎉 Initial commit: Ekman Transport Visualizer with Dark/Light mode"

# 메인 브랜치 설정
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}🎉 초기 업로드 완료!${NC}"
else
    echo -e "${RED}❌ 업로드 실패. GitHub 인증을 확인해주세요.${NC}"
fi

# 4. 별칭 설정 안내
echo -e "\n${PURPLE}⚡ 편리한 사용을 위한 별칭 설정${NC}"
echo "======================================"

# 사용자의 shell 확인
SHELL_NAME=$(basename "$SHELL")
CONFIG_FILE=""

case $SHELL_NAME in
    "zsh")
        CONFIG_FILE="$HOME/.zshrc"
        ;;
    "bash")
        CONFIG_FILE="$HOME/.bashrc"
        ;;
    *)
        CONFIG_FILE="$HOME/.bashrc"
        ;;
esac

echo -e "${BLUE}🔍 감지된 Shell: ${GREEN}$SHELL_NAME${NC}"
echo -e "${BLUE}📝 설정 파일: ${GREEN}$CONFIG_FILE${NC}"

# 별칭 추가
ALIAS_LINE="alias auto_push='cd \"$(pwd)\" && ./auto_push.sh'"

echo -e "\n${YELLOW}다음 별칭을 $CONFIG_FILE에 추가하시겠습니까?${NC}"
echo -e "${GREEN}$ALIAS_LINE${NC}"
echo -e "\n${BLUE}이렇게 하면 터미널 어디서든 ${GREEN}'auto_push'${BLUE} 명령어로 업로드할 수 있습니다!${NC}"

read -p "별칭을 추가하시겠습니까? (y/n): " ADD_ALIAS

if [[ $ADD_ALIAS =~ ^[Yy]$ ]]; then
    echo "" >> "$CONFIG_FILE"
    echo "# Ekman Transport Visualizer - GitHub 자동 업로드" >> "$CONFIG_FILE"
    echo "$ALIAS_LINE" >> "$CONFIG_FILE"
    
    echo -e "${GREEN}✅ 별칭이 추가되었습니다!${NC}"
    echo -e "${YELLOW}⚠️  새 터미널을 열거나 다음 명령어를 실행해주세요:${NC}"
    echo -e "${BLUE}source $CONFIG_FILE${NC}"
else
    echo -e "${BLUE}별칭을 수동으로 추가하려면 다음을 복사해서 사용하세요:${NC}"
    echo -e "${GREEN}$ALIAS_LINE${NC}"
fi

echo -e "\n${PURPLE}========================================="
echo -e "🎉 설정 완료!${NC}"
echo -e "\n${BLUE}사용법:${NC}"
echo -e "${GREEN}1. 현재 디렉토리에서: ${YELLOW}./auto_push.sh \"커밋메시지\"${NC}"
echo -e "${GREEN}2. 별칭 사용 (설정 후): ${YELLOW}auto_push \"커밋메시지\"${NC}"
echo -e "${GREEN}3. 기본 메시지로: ${YELLOW}auto_push${NC}"
echo -e "\n${BLUE}🔗 GitHub 레포지토리: ${GREEN}$REPO_URL${NC}" 