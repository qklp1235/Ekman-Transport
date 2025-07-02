# 에크만 수송 시각화 시스템 (Ekman Transport Visualization System)

## 📖 개요

이 프로젝트는 해양학의 핵심 개념인 **에크만 수송(Ekman Transport)**을 인터랙티브하게 시각화하는 웹 애플리케이션입니다. 바람에 의한 해수 표면의 마찰력과 지구 자전으로 인한 코리올리 힘의 상호작용을 2D 및 3D로 시각화하여 학습과 연구에 활용할 수 있습니다.

## 🌊 에크만 수송이란?

에크만 수송은 바람이 해수 표면에 작용할 때 발생하는 해류 현상입니다:

- **바람 응력**: 바람이 해수 표면에 미치는 마찰력
- **코리올리 힘**: 지구 자전으로 인해 발생하는 관성력
- **에크만 나선**: 깊이에 따라 변화하는 해류 방향과 속도
- **수송 벡터**: 바람 방향에 대해 90도 각도로 발생하는 해류

### 수학적 표현
```
Mx = -τy / (ρf)
My = τx / (ρf)
```
여기서:
- τ: 바람 응력
- ρ: 해수 밀도
- f: 코리올리 매개변수

## ✨ 주요 기능

### 🎛️ 인터랙티브 제어
- **바람 속도**: 0-30 m/s 범위 조절
- **바람 방향**: 0-360도 범위 조절
- **위도**: -90도~90도 범위 조절
- **깊이**: 10-1000m 범위 조절

### 📊 시각화 옵션
- **3D 시각화**: 실사적인 바다 표면과 에크만 나선
- **2D 분석**: 4개 패널로 구성된 상세 분석
  - 바람 응력과 에크만 수송 벡터
  - 에크만 나선
  - 깊이별 속도 프로파일
  - 수송 성분 분석

### 📈 실시간 계산 결과
- 바람 응력 (mN/m²)
- 에크만 수송 벡터 (X, Y 성분)
- 에크만 깊이
- 코리올리 매개변수
- 총 수송량

### 📄 PDF 보고서 생성
- **다국어 지원**: 한국어, 영어, 중국어, 일본어, 스페인어, 러시아어
- **완전한 보고서**: 입력 파라미터, 계산 결과, 그래프 이미지 포함
- **앱 폰트 지원**: Noto Sans 폰트 패밀리 사용
- **프로페셔널한 레이아웃**: 테이블, 섹션, 요약 포함

## 🚀 설치 및 실행

### 1. 환경 설정
```bash
# Python 3.8+ 필요
python --version

# 가상환경 생성 (선택사항)
python -m venv ekman_env
source ekman_env/bin/activate  # Linux/Mac
# 또는
ekman_env\Scripts\activate     # Windows
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

#### GUI 애플리케이션 (권장)
```bash
python gui_app.py
```

#### 웹 애플리케이션
```bash
python app.py
```

### 4. 웹 브라우저에서 접속 (웹 버전)
```
http://localhost:5000
```

## 🛠️ 기술 스택

### 백엔드
- **Flask**: 웹 프레임워크
- **NumPy**: 수치 계산
- **SciPy**: 과학 계산
- **Plotly**: 인터랙티브 시각화
- **ReportLab**: PDF 생성

### 프론트엔드
- **Tkinter**: GUI 애플리케이션
- **Bootstrap 5**: 웹 반응형 UI
- **Font Awesome**: 아이콘
- **JavaScript**: 동적 인터래이스
- **Plotly.js**: 클라이언트 사이드 시각화

### 시각화 라이브러리
- **Plotly**: 3D/2D 인터랙티브 그래프
- **Matplotlib**: 2D 정적 그래프
- **ReportLab**: PDF 문서 생성

## 📁 프로젝트 구조

```
Ekman_transport_v.2.8.9/
├── gui_app.py              # GUI 메인 애플리케이션
├── app.py                  # Flask 웹 애플리케이션
├── ekman_calculations.py   # 에크만 수송 계산 클래스
├── pdf_report.py           # PDF 보고서 생성 모듈
├── translations.py         # 다국어 번역
├── requirements.txt        # Python 의존성
├── README.md              # 프로젝트 문서
├── templates/
│   └── index.html         # 메인 HTML 템플릿
└── static/
    ├── css/
    │   └── style.css      # 커스텀 스타일
    ├── js/
    │   └── main.js        # JavaScript 기능
    └── fonts/             # 폰트 파일들
        ├── NotoSans-Regular.ttf
        ├── NotoSansCJKkr-Regular.otf
        ├── NotoSansCJKjp-Regular.otf
        └── NotoSansCJKsc-Regular.otf
```

## 🎯 사용법

### GUI 애플리케이션 사용법
1. `python gui_app.py` 실행
2. 왼쪽 패널에서 파라미터 조정:
   - 바람 속도와 방향 설정
   - 위도와 깊이 설정
   - 2D/3D 시각화 선택
3. "계산 및 시각화" 버튼 클릭
4. 결과 확인 및 분석
5. **"PDF 보고서 내보내기" 버튼으로 보고서 생성**

### 웹 애플리케이션 사용법
1. 웹 브라우저에서 `http://localhost:5000` 접속
2. 왼쪽 패널에서 파라미터 조정
3. "계산 및 시각화" 버튼 클릭
4. 결과 확인 및 분석

### PDF 보고서 기능
- **언어 선택**: 6개 언어 지원 (한국어, 영어, 중국어, 일본어, 스페인어, 러시아어)
- **완전한 보고서**: 입력 파라미터, 계산 결과, 그래프 이미지 포함
- **프로페셔널한 레이아웃**: 테이블 형식의 데이터 표시
- **앱 폰트 지원**: 각 언어에 맞는 Noto Sans 폰트 사용

### 고급 기능
- **키보드 단축키**:
  - `Ctrl+Enter`: 계산 실행
  - `ESC`: 로딩 취소
- **반응형 디자인**: 모바일/태블릿 지원
- **실시간 업데이트**: 파라미터 변경 시 즉시 반영
- **사전 설정**: 일반, 강풍, 태풍 시나리오
- **지역 선택**: 주요 해양 지역 사전 설정

## 🔬 과학적 배경

### 물리 상수
- 해수 밀도: 1025 kg/m³
- 공기 밀도: 1.225 kg/m³
- 항력 계수: 0.0013
- 지구 자전 각속도: 7.2921×10⁻⁵ rad/s

### 계산 과정
1. **코리올리 매개변수 계산**: `f = 2Ω sin(φ)`
2. **바람 응력 계산**: `τ = ρₐ × Cₐ × U²`
3. **에크만 수송 계산**: `M = τ / (ρₛ × f)`
4. **에크만 깊이 계산**: `D = π × √(2K/f)`

## 🎨 시각화 특징

### 3D 시각화
- 실사적인 바다 표면 (파도 효과)
- 에크만 나선의 3D 벡터 표현
- 바람 벡터 표시
- 인터랙티브 카메라 제어

### 2D 분석
- 4개 패널로 구성된 종합 분석
- 벡터 다이어그램
- 깊이별 속도 프로파일
- 수송 성분 비교

## 📄 PDF 보고서 특징

### 다국어 지원
- **한국어**: 완전한 한국어 지원
- **영어**: 영어 보고서 생성
- **중국어**: 중국어 보고서 생성
- **일본어**: 일본어 보고서 생성
- **스페인어**: 스페인어 보고서 생성
- **러시아어**: 러시아어 보고서 생성

### 보고서 구성
1. **제목 및 생성 날짜**
2. **입력 파라미터 테이블**
3. **계산 결과 테이블**
4. **시각화 그래프 이미지**
5. **요약 및 분석**

### 폰트 지원
- **Noto Sans**: 기본 폰트
- **Noto Sans CJK KR**: 한국어
- **Noto Sans CJK JP**: 일본어
- **Noto Sans CJK SC**: 중국어

## 🔧 개발 및 확장

### 새로운 기능 추가
1. `ekman_calculations.py`에 계산 함수 추가
2. `gui_app.py` 또는 `app.py`에 새로운 기능 추가
3. `translations.py`에 새로운 번역 추가
4. `pdf_report.py`에 새로운 보고서 형식 추가

### 시각화 개선
- 새로운 색상 팔레트 적용
- 애니메이션 효과 추가
- 추가적인 인터랙션 기능

## 📚 참고 자료

- Ekman, V.W. (1905). On the influence of the earth's rotation on ocean currents.
- Stewart, R.H. (2008). Introduction to Physical Oceanography.
- Pond, S. & Pickard, G.L. (1983). Introductory Dynamical Oceanography.

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해주세요.

---

**해양학과 물리학의 아름다운 조화를 시각화하는 프로젝트입니다! 🌊✨** 