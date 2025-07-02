# 🚀 GitHub 자동 업로드 시스템

이 프로젝트에는 간단한 명령어로 GitHub에 자동 업로드할 수 있는 시스템이 구축되어 있습니다.

## 📋 목차
- [초기 설정](#-초기-설정)
- [사용법](#-사용법)
- [문제 해결](#-문제-해결)

## 🛠 초기 설정

### 1. GitHub 레포지토리 생성
1. [GitHub](https://github.com)에 로그인
2. 새 레포지토리 생성 (Repository name: `ekman-transport-visualizer` 추천)
3. **Public** 또는 **Private** 선택
4. **"Add a README file"** 체크 **해제** (이미 파일들이 있으므로)
5. **Create repository** 클릭

### 2. 자동 설정 스크립트 실행
```bash
./setup_github.sh
```

이 스크립트는 다음을 수행합니다:
- GitHub 레포지토리 URL 입력 받기
- 원격 저장소 연결
- 초기 파일 업로드
- 편리한 별칭 설정

### 3. 수동 설정 (선택사항)
자동 설정이 안될 경우 수동으로 설정:

```bash
# GitHub 레포지토리 연결
git remote add origin https://github.com/사용자명/레포지토리명.git

# 초기 업로드
git add .
git commit -m "🎉 Initial commit: Ekman Transport Visualizer"
git branch -M main
git push -u origin main
```

## 🚀 사용법

### 기본 사용 (현재 디렉토리에서)
```bash
# 기본 커밋 메시지 ("others")로 업로드
./auto_push.sh

# 커스텀 커밋 메시지로 업로드
./auto_push.sh "다크모드 추가 및 UI 개선"
```

### 별칭 사용 (터미널 어디서든)
별칭이 설정되어 있다면:
```bash
# 어느 디렉토리에서든 사용 가능
auto_push
auto_push "새로운 기능 추가"
```

### 스크립트가 수행하는 작업
1. `git add .` - 모든 변경된 파일 스테이징
2. `git commit -m "메시지"` - 커밋 생성
3. `git push origin main` - GitHub에 업로드

## ⚡ 빠른 사용 예시

```bash
# 1. 파일 수정 후
vim index_tkinter_style.html

# 2. 한 번에 업로드
./auto_push.sh "시각화 개선"

# 또는 별칭 사용
auto_push "시각화 개선"
```

## 🔧 문제 해결

### "permission denied" 오류
```bash
chmod +x auto_push.sh
chmod +x setup_github.sh
```

### GitHub 인증 문제
1. **Personal Access Token** 사용:
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - repo 권한 선택
   - 생성된 토큰을 비밀번호로 사용

2. **SSH 키** 사용:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   cat ~/.ssh/id_rsa.pub
   # 출력된 키를 GitHub → Settings → SSH keys에 추가
   ```

### 원격 저장소 확인
```bash
git remote -v
```

### 브랜치 확인
```bash
git branch -a
```

## 📁 생성된 파일들

| 파일 | 설명 |
|------|------|
| `auto_push.sh` | 자동 업로드 스크립트 |
| `setup_github.sh` | GitHub 연결 설정 도우미 |
| `.gitignore` | Git 무시 파일 목록 |
| `GITHUB_SETUP_GUIDE.md` | 이 가이드 파일 |

## 🎯 추천 워크플로우

1. **개발 작업** → 파일 수정
2. **테스트** → 브라우저에서 확인
3. **업로드** → `auto_push "수정 내용"` 실행
4. **확인** → GitHub 레포지토리에서 변경사항 확인

## 💡 팁

- 커밋 메시지는 구체적으로 작성하는 것이 좋습니다
- 큰 변경사항 전에는 백업을 권장합니다
- 정기적으로 GitHub에서 변경사항을 확인하세요

---

## 🌊 Ekman Transport Visualizer 특징

- ✨ **다크/라이트 모드 자동 전환**
- 📊 **인터랙티브 2D/3D 시각화**
- 🎛 **직관적인 Tkinter 스타일 UI**
- 📱 **반응형 웹 디자인**
- 🚀 **GitHub 자동 업로드 시스템**

프로젝트가 성공적으로 업로드되었다면, GitHub 레포지토리에서 확인해보세요! 🎉 