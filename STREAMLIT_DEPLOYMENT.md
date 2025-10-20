# Streamlit 배포 가이드

## 🚀 Streamlit Cloud 배포 방법

### 1단계: GitHub 저장소 준비
1. 현재 프로젝트를 GitHub에 푸시
2. `app.py`와 `requirements.txt` 파일이 루트에 있는지 확인

### 2단계: Streamlit Cloud 배포
1. **https://share.streamlit.io** 접속
2. **Sign in with GitHub** 클릭
3. **New app** 클릭
4. 저장소 선택: `beeper9-source/esg`
5. **Main file path**: `app.py`
6. **App URL**: 원하는 URL 입력 (예: `samsung-sds-esg`)
7. **Deploy!** 클릭

### 3단계: 배포 확인
- 몇 분 후 배포 완료
- 제공된 URL로 접속하여 앱 확인

## 🔧 로컬 실행 방법

### 1단계: 의존성 설치
```bash
pip install -r requirements.txt
```

### 2단계: 앱 실행
```bash
streamlit run app.py
```

### 3단계: 브라우저에서 확인
- 자동으로 브라우저가 열림
- `http://localhost:8501`에서 앱 확인

## 📋 주요 기능

### ✅ 구현된 기능
- **대시보드**: KPI 메트릭, 차트 시각화
- **Scope 1**: 직접 배출량 관리 및 등록
- **Scope 2**: 간접 배출량 관리 및 등록
- **Scope 3**: 밸류체인 배출량 관리 및 등록
- **순환경제**: 폐기물 관리 및 재활용률 추적
- **임직원 아이디어**: 아이디어 제안 및 관리

### 🎨 UI/UX 특징
- **반응형 디자인**: 모든 화면 크기에 최적화
- **인터랙티브 차트**: Plotly를 활용한 동적 시각화
- **직관적 네비게이션**: 사이드바 메뉴
- **실시간 데이터**: 폼 입력 및 즉시 피드백

## 🌐 배포 URL
배포 완료 후: `https://samsung-sds-esg.streamlit.app`

## 🔄 업데이트 방법
1. 코드 수정 후 GitHub에 푸시
2. Streamlit Cloud에서 자동 재배포
3. 몇 분 후 변경사항 반영
