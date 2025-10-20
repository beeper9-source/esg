import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="삼성SDS ESG Re:source",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1e3a8a;
    }
    .sidebar .sidebar-content {
        background-color: #1e3a8a;
    }
    /* 사이드바 왼쪽 정렬 강화 */
    .sidebar .sidebar-content .element-container {
        text-align: left !important;
    }
    .sidebar .sidebar-content h1, 
    .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3 {
        text-align: left !important;
    }
    .sidebar .sidebar-content p {
        text-align: left !important;
    }
    /* 모든 텍스트 요소 왼쪽 정렬 */
    .sidebar * {
        text-align: left !important;
    }
    .sidebar .stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
    }
    .sidebar .stMarkdown {
        text-align: left !important;
    }
    .sidebar div {
        text-align: left !important;
    }
    
    /* 선택된 메뉴 항목 스타일 */
    .selected-menu-item {
        background-color: #e8f5e8 !important;
        border: 2px solid #2e7d32 !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin: 2px 0 !important;
        font-weight: bold !important;
        color: #1b5e20 !important;
    }
    
    .selected-category {
        background-color: #e8f5e8 !important;
        border: 2px solid #2e7d32 !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin: 5px 0 !important;
        font-weight: bold !important;
        color: #1b5e20 !important;
    }
    
    /* Re:source 깜박임 애니메이션 */
    @keyframes blink {
        0%, 50% {
            opacity: 1;
        }
        51%, 100% {
            opacity: 0.3;
        }
    }
    
    .blink-text {
        animation: blink 2s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바 네비게이션
st.sidebar.markdown("""
<div style="padding: 1rem; text-align: left;">
    <h2 style="color: white; margin: 0; text-align: left !important;">🌱 삼성SDS ESG</h2>
    <p class="blink-text" style="color: #e0e0e0; margin: 0; text-align: left !important;">Re:source</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# 메뉴 항목들 (2단계 구조)
st.sidebar.markdown("### 📊 메뉴")

# Level 1 메뉴
level1_menus = {
    "E : 환경": {
        "계단 오르기": "계단 오르기",
        "일회용품 ZERO 챌린지": "일회용품 ZERO 챌린지", 
        "페이퍼리스 데이": "페이퍼리스 데이",
        "소등·절전 챌린지": "소등·절전 챌린지",
        "플로깅 데이": "플로깅 데이",
        "탄소 발자국 챌린지": "탄소 발자국 챌린지"
    },
    "S : 사회": {
        "사무실 미니 플리마켓": "사무실 미니 플리마켓",
        "ESG 아이디어 공모전": "임직원 아이디어",
        "그린리본 인증 캠페인": "그린리본 인증 캠페인",
        "지역 사회 연계 봉사": "지역 사회 연계 봉사"
    },
    "G : 운영정책": {
        "ESG 성과 공개 플랫폼": "ESG 성과 공개 플랫폼",
        "ESG 교육 및 퀴즈데이": "ESG 교육 및 퀴즈데이",
        "디지털 다이어트 캠페인": "디지털 다이어트 캠페인"
    }
}

# Level 1 선택
if 'selected_level1' not in st.session_state:
    st.session_state.selected_level1 = "E : 환경"

# 기본 메뉴 선택
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "계단 오르기"

menu = st.session_state.selected_menu

# 모든 카테고리 메뉴 표시 (모두 펼쳐진 상태)
for level1_name, level2_items in level1_menus.items():
    # 카테고리 제목
    if level1_name == st.session_state.selected_level1:
        st.sidebar.markdown(f"""
        <div class="selected-category">
            <strong>🔽 {level1_name}</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f"**📁 {level1_name}**")
    
    # 모든 하위 메뉴 표시 (항상 펼쳐진 상태)
    for level2_name, level2_value in level2_items.items():
        if level2_value == st.session_state.selected_menu:
            # 선택된 메뉴 항목
            st.sidebar.markdown(f"""
            <div class="selected-menu-item">
                📋 {level2_name}
            </div>
            """, unsafe_allow_html=True)
        else:
            # 일반 메뉴 항목
            if st.sidebar.button(f"  📋 {level2_name}", key=f"level2_{level2_value}", use_container_width=True):
                st.session_state.selected_level1 = level1_name
                st.session_state.selected_menu = level2_value
                st.rerun()
    
    st.sidebar.markdown("")  # 카테고리 간 간격

st.sidebar.markdown("---")

# 계단 오르기 페이지
if menu == "계단 오르기":
    st.title("🏢 계단 오르기 캠페인")
    st.write("삼성SDS 5개 사옥에서 진행하는 친환경 계단 오르기 캠페인을 관리합니다.")

    # 사옥 정보
    buildings = {
        "잠실": {
            "name": "잠실 사옥",
            "image": "🏢",
            "participants": 0
        },
        "판교IT": {
            "name": "판교 IT 사옥", 
            "image": "🏢",
            "participants": 0
        },
        "판교물류": {
            "name": "판교 물류 사옥",
            "image": "🏢", 
            "participants": 0
        },
        "상암": {
            "name": "상암 사옥",
            "image": "🏢",
            "participants": 0
        },
        "수원": {
            "name": "수원 사옥",
            "image": "🏢",
            "participants": 0
        }
    }

    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'stair_climbing_data' not in st.session_state:
        # 샘플 데이터 생성
        sample_buildings = {
            "잠실": {
                "name": "잠실 사옥",
                "image": "🏢",
                "participants": np.random.randint(15, 35)  # 15-35명 사이 랜덤
            },
            "판교IT": {
                "name": "판교 IT 사옥", 
                "image": "🏢",
                "participants": np.random.randint(20, 40)  # 20-40명 사이 랜덤
            },
            "판교물류": {
                "name": "판교 물류 사옥",
                "image": "🏢", 
                "participants": np.random.randint(10, 25)  # 10-25명 사이 랜덤
            },
            "상암": {
                "name": "상암 사옥",
                "image": "🏢",
                "participants": np.random.randint(12, 30)  # 12-30명 사이 랜덤
            },
            "수원": {
                "name": "수원 사옥",
                "image": "🏢",
                "participants": np.random.randint(8, 20)   # 8-20명 사이 랜덤
            }
        }
        st.session_state.stair_climbing_data = sample_buildings

    st.markdown("---")

    # 오늘 날짜 표시
    today = datetime.now().strftime("%Y년 %m월 %d일")
    st.subheader(f"📅 {today} 계단 오르기 현황")

    # 사옥별 카드 레이아웃
    cols = st.columns(5)
    
    for i, (building_key, building_info) in enumerate(st.session_state.stair_climbing_data.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                margin-bottom: 10px;
            ">
                <h3 style="margin: 0; color: #1e3a8a;">{building_info['image']}</h3>
                <h4 style="margin: 10px 0; color: #333;">{building_info['name']}</h4>
                <p style="margin: 5px 0; font-size: 18px; font-weight: bold; color: #28a745;">
                    참여자: {building_info['participants']}명
                </p>
                <p style="margin: 5px 0; font-size: 14px; font-weight: bold; color: #dc3545;">
                    예상감축량: {building_info['participants'] * 0.3:.1f}kg CO₂eq
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 등록 버튼
            if st.button(f"등록하기", key=f"register_{building_key}", use_container_width=True):
                st.session_state.stair_climbing_data[building_key]['participants'] += 1
                st.success(f"{building_info['name']}에 계단 오르기 등록 완료!")
                st.rerun()

    st.markdown("---")

    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_participants = sum(building['participants'] for building in st.session_state.stair_climbing_data.values())
    
    with col1:
        st.metric(
            label="총 참여자",
            value=f"{total_participants}명",
            delta=f"+{total_participants}명"
        )
    
    with col2:
        st.metric(
            label="참여 사옥",
            value="5개",
            delta="100%"
        )
    
    with col3:
        st.metric(
            label="평균 참여율",
            value=f"{total_participants/5:.1f}명",
            delta="사옥당"
        )
    
    with col4:
        st.metric(
            label="예상감축량",
            value=f"{total_participants * 0.3:.1f}kg",
            delta="CO₂eq"
        )

    st.markdown("---")

    # 사옥별 참여 현황 차트
    st.subheader("🏢 사옥별 참여 현황")
    
    building_names = list(st.session_state.stair_climbing_data.keys())
    participants_count = [building['participants'] for building in st.session_state.stair_climbing_data.values()]
    
    fig_stairs = px.bar(
        x=building_names,
        y=participants_count,
        title='사옥별 계단 오르기 참여자 수',
        labels={'x': '사옥', 'y': '참여자 수'},
        color=participants_count,
        color_continuous_scale='Greens'
    )
    fig_stairs.update_layout(
        xaxis_title="사옥",
        yaxis_title="참여자 수 (명)"
    )
    st.plotly_chart(fig_stairs, use_container_width=True)

    # 사옥별 예상감축량 차트
    st.subheader("🌱 사옥별 예상감축량")
    
    building_names = list(st.session_state.stair_climbing_data.keys())
    reduction_amounts = [building['participants'] * 0.3 for building in st.session_state.stair_climbing_data.values()]
    
    fig_reduction = px.bar(
        x=building_names,
        y=reduction_amounts,
        title='사옥별 예상감축량 (kg CO₂eq)',
        labels={'x': '사옥', 'y': '예상감축량 (kg CO₂eq)'},
        color=reduction_amounts,
        color_continuous_scale='Reds'
    )
    fig_reduction.update_layout(
        xaxis_title="사옥",
        yaxis_title="예상감축량 (kg CO₂eq)"
    )
    st.plotly_chart(fig_reduction, use_container_width=True)

    st.markdown("---")

    # 지표 산식 설명
    st.subheader("📊 예상감축량 지표 산식")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🌱 탄소 감축량 계산 공식**
        
        ```
        예상감축량 = 참여자 수 × 0.3kg CO₂eq
        ```
        
        **📋 계산 기준**
        - 계단 이용 1회당: 0.3kg CO₂eq
        - 엘리베이터 대신 계단 이용 시 절약되는 탄소량
        - 국제 탄소 배출 계수 기준 적용
        """)
    
    with col2:
        st.success("""
        **🎯 환경 효과**
        
        • **에너지 절약**: 엘리베이터 사용량 감소
        • **건강 증진**: 계단 오르기로 체력 향상
        • **탄소 감축**: 직접적인 CO₂ 배출량 감소
        • **친환경 문화**: 지속가능한 생활습관 형성
        """)
    
    # 실시간 계산 예시
    st.markdown("---")
    st.subheader("🧮 실시간 계산 예시")
    
    example_participants = total_participants
    example_reduction = example_participants * 0.3
    
    st.markdown(f"""
    <div style="
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #d4edda;
        margin-bottom: 10px;
    ">
        <h3 style="margin: 0; color: #155724;">📈 현재 상황</h3>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>총 참여자:</strong> {example_participants}명
        </p>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>계산식:</strong> {example_participants}명 × 0.3kg CO₂eq
        </p>
        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #155724;">
            <strong>= {example_reduction:.1f}kg CO₂eq</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 리셋 버튼
    st.subheader("🔄 데이터 관리")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 데이터 초기화", use_container_width=True):
            # 샘플 데이터로 리셋
            sample_buildings = {
                "잠실": {
                    "name": "잠실 사옥",
                    "image": "🏢",
                    "participants": np.random.randint(15, 35)
                },
                "판교IT": {
                    "name": "판교 IT 사옥", 
                    "image": "🏢",
                    "participants": np.random.randint(20, 40)
                },
                "판교물류": {
                    "name": "판교 물류 사옥",
                    "image": "🏢", 
                    "participants": np.random.randint(10, 25)
                },
                "상암": {
                    "name": "상암 사옥",
                    "image": "🏢",
                    "participants": np.random.randint(12, 30)
                },
                "수원": {
                    "name": "수원 사옥",
                    "image": "🏢",
                    "participants": np.random.randint(8, 20)
                }
            }
            st.session_state.stair_climbing_data = sample_buildings
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 보기", use_container_width=True):
            st.info("통계 데이터를 새로고침했습니다!")

# 일회용품 ZERO 챌린지 페이지
elif menu == "일회용품 ZERO 챌린지":
    st.title("♻️ 일회용품 ZERO 챌린지")
    st.write("제로컵 위크 캠페인을 통해 개인 컵, 텀블러, 도시락 사용을 장려합니다.")

    # 챌린지 정보
    challenge_info = {
        "name": "제로컵 위크",
        "description": "일회용 컵·용기 사용을 줄이고 개인 컵, 텀블러, 도시락 사용을 장려하는 캠페인",
        "duration": "2024년 10월 20일 ~ 10월 27일",
        "goal": "일회용품 사용률 50% 감소"
    }

    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'zero_challenge_data' not in st.session_state:
        # 샘플 데이터 생성
        personal_cups = np.random.randint(25, 50)
        tumblers = np.random.randint(30, 60)
        lunchboxes = np.random.randint(15, 35)
        total_participants = personal_cups + tumblers + lunchboxes
        single_use_reduction = personal_cups + tumblers + (lunchboxes * 2)  # 도시락은 2개 절약
        
        # 시간대별 샘플 등록 데이터 생성
        sample_registrations = []
        for i in range(np.random.randint(20, 40)):  # 20-40개의 샘플 등록
            hour = np.random.randint(8, 18)  # 8시-18시 사이
            minute = np.random.randint(0, 60)
            usage_type = np.random.choice(['개인 컵', '텀블러', '도시락'])
            sample_registrations.append({
                'type': usage_type,
                'timestamp': f"{hour:02d}:{minute:02d}",
                'date': datetime.now().strftime("%Y-%m-%d")
            })
        
        # 탄소감축량 계산을 위한 변수들
        A_single = 0.15  # 일회용품 1개당 탄소배출량 (kg CO₂eq)
        A_multi = 0.02  # 다회용품 1개당 탄소배출량 (kg CO₂eq)
        N = single_use_reduction  # 절약된 일회용품 수
        
        # 순환이용률 계산을 위한 변수들
        R = personal_cups + tumblers  # 재사용 용기 수
        C = lunchboxes  # 순환용기 수 (도시락)
        W = np.random.randint(50, 100)  # 폐기물 수 (샘플)
        
        st.session_state.zero_challenge_data = {
            "participants": total_participants,
            "personal_cups": personal_cups,
            "tumblers": tumblers,
            "lunchboxes": lunchboxes,
            "single_use_reduction": single_use_reduction,
            "daily_registrations": sample_registrations,
            # 탄소감축량 관련
            "A_single": A_single,
            "A_multi": A_multi,
            "N": N,
            "carbon_reduction": (A_single - A_multi) * N,
            # 순환이용률 관련
            "R": R,
            "C": C,
            "W": W,
            "circular_rate": ((R + C) / (W + C)) * 100
        }

    st.markdown("---")

    # 챌린지 정보 카드
    st.subheader("📋 챌린지 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **🎯 챌린지명**: {challenge_info['name']}
        
        **📅 기간**: {challenge_info['duration']}
        
        **🎯 목표**: {challenge_info['goal']}
        """)
    
    with col2:
        st.success(f"""
        **📝 설명**: {challenge_info['description']}
        
        **🌱 환경효과**: 일회용품 사용 감소로 탄소발자국 줄이기
        """)

    st.markdown("---")

    # 참여 등록 섹션
    st.subheader("🎮 참여 등록")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #f8f9fa;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #1e3a8a;">☕</h3>
            <h4 style="margin: 10px 0; color: #333;">개인 컵 사용</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #28a745;">
                참여자: {personal_cups}명
            </p>
        </div>
        """.format(personal_cups=st.session_state.zero_challenge_data['personal_cups']), unsafe_allow_html=True)
        
        if st.button("개인 컵 등록", key="personal_cup", use_container_width=True):
            st.session_state.zero_challenge_data['personal_cups'] += 1
            st.session_state.zero_challenge_data['participants'] += 1
            st.session_state.zero_challenge_data['single_use_reduction'] += 1
            st.session_state.zero_challenge_data['N'] += 1
            st.session_state.zero_challenge_data['R'] += 1
            # 지표 재계산
            st.session_state.zero_challenge_data['carbon_reduction'] = (st.session_state.zero_challenge_data['A_single'] - st.session_state.zero_challenge_data['A_multi']) * st.session_state.zero_challenge_data['N']
            st.session_state.zero_challenge_data['circular_rate'] = ((st.session_state.zero_challenge_data['R'] + st.session_state.zero_challenge_data['C']) / (st.session_state.zero_challenge_data['W'] + st.session_state.zero_challenge_data['C'])) * 100
            st.session_state.zero_challenge_data['daily_registrations'].append({
                'type': '개인 컵',
                'timestamp': datetime.now().strftime("%H:%M"),
                'date': datetime.now().strftime("%Y-%m-%d")
            })
            st.success("개인 컵 사용 등록 완료! 🌱")
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #f8f9fa;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #1e3a8a;">🍵</h3>
            <h4 style="margin: 10px 0; color: #333;">텀블러 사용</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #28a745;">
                참여자: {tumblers}명
            </p>
        </div>
        """.format(tumblers=st.session_state.zero_challenge_data['tumblers']), unsafe_allow_html=True)
        
        if st.button("텀블러 등록", key="tumbler", use_container_width=True):
            st.session_state.zero_challenge_data['tumblers'] += 1
            st.session_state.zero_challenge_data['participants'] += 1
            st.session_state.zero_challenge_data['single_use_reduction'] += 1
            st.session_state.zero_challenge_data['N'] += 1
            st.session_state.zero_challenge_data['R'] += 1
            # 지표 재계산
            st.session_state.zero_challenge_data['carbon_reduction'] = (st.session_state.zero_challenge_data['A_single'] - st.session_state.zero_challenge_data['A_multi']) * st.session_state.zero_challenge_data['N']
            st.session_state.zero_challenge_data['circular_rate'] = ((st.session_state.zero_challenge_data['R'] + st.session_state.zero_challenge_data['C']) / (st.session_state.zero_challenge_data['W'] + st.session_state.zero_challenge_data['C'])) * 100
            st.session_state.zero_challenge_data['daily_registrations'].append({
                'type': '텀블러',
                'timestamp': datetime.now().strftime("%H:%M"),
                'date': datetime.now().strftime("%Y-%m-%d")
            })
            st.success("텀블러 사용 등록 완료! 🌱")
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #f8f9fa;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #1e3a8a;">🍱</h3>
            <h4 style="margin: 10px 0; color: #333;">도시락 사용</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #28a745;">
                참여자: {lunchboxes}명
            </p>
        </div>
        """.format(lunchboxes=st.session_state.zero_challenge_data['lunchboxes']), unsafe_allow_html=True)
        
        if st.button("도시락 등록", key="lunchbox", use_container_width=True):
            st.session_state.zero_challenge_data['lunchboxes'] += 1
            st.session_state.zero_challenge_data['participants'] += 1
            st.session_state.zero_challenge_data['single_use_reduction'] += 2  # 도시락은 용기 2개 절약
            st.session_state.zero_challenge_data['N'] += 2
            st.session_state.zero_challenge_data['C'] += 1
            # 지표 재계산
            st.session_state.zero_challenge_data['carbon_reduction'] = (st.session_state.zero_challenge_data['A_single'] - st.session_state.zero_challenge_data['A_multi']) * st.session_state.zero_challenge_data['N']
            st.session_state.zero_challenge_data['circular_rate'] = ((st.session_state.zero_challenge_data['R'] + st.session_state.zero_challenge_data['C']) / (st.session_state.zero_challenge_data['W'] + st.session_state.zero_challenge_data['C'])) * 100
            st.session_state.zero_challenge_data['daily_registrations'].append({
                'type': '도시락',
                'timestamp': datetime.now().strftime("%H:%M"),
                'date': datetime.now().strftime("%Y-%m-%d")
            })
            st.success("도시락 사용 등록 완료! 🌱")
            st.rerun()

    st.markdown("---")

    # 실시간 통계
    st.subheader("📊 실시간 통계")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            label="총 참여자",
            value=f"{st.session_state.zero_challenge_data['participants']}명",
            delta=f"+{st.session_state.zero_challenge_data['participants']}명"
        )
    
    with col2:
        st.metric(
            label="일회용품 감소",
            value=f"{st.session_state.zero_challenge_data['single_use_reduction']}개",
            delta=f"-{st.session_state.zero_challenge_data['single_use_reduction']}개"
        )
    
    with col3:
        st.metric(
            label="감소율",
            value=f"{(st.session_state.zero_challenge_data['single_use_reduction']/max(st.session_state.zero_challenge_data['participants'], 1)*100):.1f}%",
            delta="목표 대비"
        )
    
    with col4:
        st.metric(
            label="탄소감축량",
            value=f"{st.session_state.zero_challenge_data['carbon_reduction']:.2f}kg",
            delta="CO₂eq"
        )
    
    with col5:
        st.metric(
            label="순환이용률",
            value=f"{st.session_state.zero_challenge_data['circular_rate']:.1f}%",
            delta="환경효과"
        )
    
    with col6:
        st.metric(
            label="재사용 용기",
            value=f"{st.session_state.zero_challenge_data['R']}개",
            delta="R+C"
        )

    st.markdown("---")

    # 사용 유형별 현황 차트
    st.subheader("📈 사용 유형별 현황")
    
    usage_types = ['개인 컵', '텀블러', '도시락']
    usage_counts = [
        st.session_state.zero_challenge_data['personal_cups'],
        st.session_state.zero_challenge_data['tumblers'],
        st.session_state.zero_challenge_data['lunchboxes']
    ]
    
    fig_usage = px.pie(
        values=usage_counts,
        names=usage_types,
        title='친환경 용기 사용 유형별 비율',
        color_discrete_sequence=['#82ca9d', '#8884d8', '#ffc658']
    )
    fig_usage.update_layout(height=400)
    st.plotly_chart(fig_usage, use_container_width=True)

    st.markdown("---")

    # 지표 산식 설명
    st.subheader("📊 지표 산식 설명")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🌱 탄소감축량 계산 공식**
        
        ```
        탄소감축량 = (A_single − A_multi) × N
        ```
        
        **📋 변수 설명**
        - **A_single**: 일회용품 1개당 탄소배출량 (0.15kg CO₂eq)
        - **A_multi**: 다회용품 1개당 탄소배출량 (0.02kg CO₂eq)
        - **N**: 절약된 일회용품 수 (개)
        
        **🎯 계산 예시**
        - 절약된 일회용품: 100개
        - 탄소감축량: (0.15 - 0.02) × 100 = 13.0kg CO₂eq
        """)
    
    with col2:
        st.success("""
        **♻️ 순환이용률 계산 공식**
        
        ```
        순환이용률 = (R + C) / (W + C) × 100
        ```
        
        **📋 변수 설명**
        - **R**: 재사용 용기 수 (개인 컵 + 텀블러)
        - **C**: 순환용기 수 (도시락)
        - **W**: 폐기물 수 (일회용품)
        
        **🎯 계산 예시**
        - 재사용 용기: 80개, 순환용기: 20개, 폐기물: 50개
        - 순환이용률: (80 + 20) / (50 + 20) × 100 = 142.9%
        """)
    
    # 실시간 계산 예시
    st.markdown("---")
    st.subheader("🧮 실시간 계산 예시")
    
    current_data = st.session_state.zero_challenge_data
    carbon_example = (current_data['A_single'] - current_data['A_multi']) * current_data['N']
    circular_example = ((current_data['R'] + current_data['C']) / (current_data['W'] + current_data['C'])) * 100
    
    st.markdown(f"""
    <div style="
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #d4edda;
        margin-bottom: 10px;
    ">
        <h3 style="margin: 0; color: #155724;">📈 현재 상황</h3>
        <div style="display: flex; justify-content: space-around; margin: 20px 0;">
            <div>
                <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                    <strong>탄소감축량:</strong><br>
                    ({current_data['A_single']} - {current_data['A_multi']}) × {current_data['N']}<br>
                    = <strong>{carbon_example:.2f}kg CO₂eq</strong>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                    <strong>순환이용률:</strong><br>
                    ({current_data['R']} + {current_data['C']}) / ({current_data['W']} + {current_data['C']}) × 100<br>
                    = <strong>{circular_example:.1f}%</strong>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 시간대별 등록 현황
    st.subheader("⏰ 시간대별 등록 현황")
    
    if st.session_state.zero_challenge_data['daily_registrations']:
        # 오늘 등록된 데이터만 필터링
        today_registrations = [
            reg for reg in st.session_state.zero_challenge_data['daily_registrations']
            if reg['date'] == datetime.now().strftime("%Y-%m-%d")
        ]
        
        if today_registrations:
            # 시간대별 집계
            hourly_data = {}
            for reg in today_registrations:
                hour = reg['timestamp'].split(':')[0]
                if hour not in hourly_data:
                    hourly_data[hour] = 0
                hourly_data[hour] += 1
            
            hours = list(hourly_data.keys())
            counts = list(hourly_data.values())
            
            fig_hourly = px.bar(
                x=hours,
                y=counts,
                title='오늘 시간대별 등록 현황',
                labels={'x': '시간', 'y': '등록 수'},
                color=counts,
                color_continuous_scale='Blues'
            )
            fig_hourly.update_layout(
                xaxis_title="시간 (시)",
                yaxis_title="등록 수"
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
        else:
            st.info("오늘 아직 등록된 데이터가 없습니다.")
    else:
        st.info("등록된 데이터가 없습니다.")

    st.markdown("---")

    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", use_container_width=True):
            # 샘플 데이터로 리셋
            personal_cups = np.random.randint(25, 50)
            tumblers = np.random.randint(30, 60)
            lunchboxes = np.random.randint(15, 35)
            total_participants = personal_cups + tumblers + lunchboxes
            single_use_reduction = personal_cups + tumblers + (lunchboxes * 2)
            
            # 시간대별 샘플 등록 데이터 생성
            sample_registrations = []
            for i in range(np.random.randint(20, 40)):
                hour = np.random.randint(8, 18)
                minute = np.random.randint(0, 60)
                usage_type = np.random.choice(['개인 컵', '텀블러', '도시락'])
                sample_registrations.append({
                    'type': usage_type,
                    'timestamp': f"{hour:02d}:{minute:02d}",
                    'date': datetime.now().strftime("%Y-%m-%d")
                })
            
            # 탄소감축량 계산을 위한 변수들
            A_single = 0.15  # 일회용품 1개당 탄소배출량 (kg CO₂eq)
            A_multi = 0.02  # 다회용품 1개당 탄소배출량 (kg CO₂eq)
            N = single_use_reduction  # 절약된 일회용품 수
            
            # 순환이용률 계산을 위한 변수들
            R = personal_cups + tumblers  # 재사용 용기 수
            C = lunchboxes  # 순환용기 수 (도시락)
            W = np.random.randint(50, 100)  # 폐기물 수 (샘플)
            
            st.session_state.zero_challenge_data = {
                "participants": total_participants,
                "personal_cups": personal_cups,
                "tumblers": tumblers,
                "lunchboxes": lunchboxes,
                "single_use_reduction": single_use_reduction,
                "daily_registrations": sample_registrations,
                # 탄소감축량 관련
                "A_single": A_single,
                "A_multi": A_multi,
                "N": N,
                "carbon_reduction": (A_single - A_multi) * N,
                # 순환이용률 관련
                "R": R,
                "C": C,
                "W": W,
                "circular_rate": ((R + C) / (W + C)) * 100
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", use_container_width=True):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 등록 내역 보기", use_container_width=True):
            if st.session_state.zero_challenge_data['daily_registrations']:
                st.write("**최근 등록 내역:**")
                for reg in st.session_state.zero_challenge_data['daily_registrations'][-10:]:
                    st.write(f"- {reg['type']}: {reg['date']} {reg['timestamp']}")
            else:
                st.info("등록된 내역이 없습니다.")

# 페이퍼리스 데이 페이지
elif menu == "페이퍼리스 데이":
    st.title("📄 페이퍼리스 데이")
    st.write("매주 특정 요일에 종이 없는 업무일을 지정하여 디지털 업무 환경을 구축합니다.")

    # 페이퍼리스 데이 정보
    paperless_info = {
        "name": "페이퍼리스 데이",
        "description": "매주 수요일을 종이 없는 업무일로 지정하여 전자결재, PDF 회의, 디지털 메모 사용을 장려",
        "target_day": "매주 수요일",
        "goal": "인쇄 건수 30% 감소, 종이 구매량 25% 감소"
    }

    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'paperless_data' not in st.session_state:
        # 샘플 데이터 생성
        base_prints = np.random.randint(200, 400)  # 기본 인쇄 건수
        base_paper_purchase = np.random.randint(50, 100)  # 기본 종이 구매량 (리터)
        
        # 페이퍼리스 데이 효과 (30% 감소)
        paperless_day_prints = int(base_prints * 0.7)
        paperless_day_paper = int(base_paper_purchase * 0.75)
        
        # 주간 데이터 생성
        weekly_data = []
        days = ['월', '화', '수', '목', '금']
        for i, day in enumerate(days):
            if day == '수':  # 수요일은 페이퍼리스 데이
                weekly_data.append({
                    'day': day,
                    'prints': np.random.randint(paperless_day_prints-20, paperless_day_prints+20),
                    'paper_purchase': np.random.randint(paperless_day_paper-5, paperless_day_paper+5),
                    'digital_usage': np.random.randint(80, 95),  # 디지털 사용률
                    'is_paperless': True
                })
            else:
                weekly_data.append({
                    'day': day,
                    'prints': np.random.randint(base_prints-30, base_prints+30),
                    'paper_purchase': np.random.randint(base_paper_purchase-10, base_paper_purchase+10),
                    'digital_usage': np.random.randint(40, 60),
                    'is_paperless': False
                })
        
        # 탄소감축량 계산을 위한 변수들
        N = np.random.randint(5000, 15000)  # 줄인 종이 사용 장수 (장)
        Ep = 0.00288  # A4 1장당 배출계수 (kg CO₂eq/장)
        carbon_reduction = N * Ep  # 탄소감축량 계산
        
        st.session_state.paperless_data = {
            "weekly_data": weekly_data,
            "total_prints": sum(day['prints'] for day in weekly_data),
            "total_paper_purchase": sum(day['paper_purchase'] for day in weekly_data),
            "digital_adoption_rate": np.random.randint(65, 80),
            "paper_savings": np.random.randint(20, 35),
            "cost_savings": np.random.randint(500, 800),  # 천원 단위
            # 탄소감축량 관련
            "N": N,
            "Ep": Ep,
            "carbon_reduction": carbon_reduction
        }

    st.markdown("---")

    # 페이퍼리스 데이 정보 카드
    st.subheader("📋 페이퍼리스 데이 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 지정 요일**: {paperless_info['target_day']}
        
        **🎯 목표**: {paperless_info['goal']}
        
        **📝 설명**: {paperless_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **🌱 환경효과**: 종이 사용 감소로 산림 보호
        
        **💰 경제효과**: 인쇄 비용 및 종이 구매비 절약
        
        **⚡ 효율성**: 디지털 업무 환경 구축
        """)

    st.markdown("---")

    # 주간 현황
    st.subheader("📊 주간 현황")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="총 인쇄 건수",
            value=f"{st.session_state.paperless_data['total_prints']}건",
            delta=f"-{st.session_state.paperless_data['paper_savings']}%"
        )
    
    with col2:
        st.metric(
            label="종이 구매량",
            value=f"{st.session_state.paperless_data['total_paper_purchase']}L",
            delta=f"-{st.session_state.paperless_data['paper_savings']-5}%"
        )
    
    with col3:
        st.metric(
            label="디지털 채택률",
            value=f"{st.session_state.paperless_data['digital_adoption_rate']}%",
            delta=f"+{np.random.randint(5, 15)}%"
        )
    
    with col4:
        st.metric(
            label="비용 절약",
            value=f"{st.session_state.paperless_data['cost_savings']}천원",
            delta=f"+{np.random.randint(50, 100)}천원"
        )
    
    with col5:
        st.metric(
            label="탄소감축량",
            value=f"{st.session_state.paperless_data['carbon_reduction']:.2f}kg",
            delta="CO₂eq"
        )

    st.markdown("---")

    # 요일별 상세 현황
    st.subheader("📅 요일별 상세 현황")
    
    # 요일별 데이터 테이블
    weekly_df = pd.DataFrame(st.session_state.paperless_data['weekly_data'])
    
    # 페이퍼리스 데이 강조를 위한 스타일링
    def highlight_paperless(row):
        if row['is_paperless']:
            return ['background-color: #d4edda'] * len(row)
        return [''] * len(row)
    
    styled_df = weekly_df.style.apply(highlight_paperless, axis=1)
    st.dataframe(styled_df, use_container_width=True)

    st.markdown("---")

    # 요일별 인쇄 건수 차트
    st.subheader("📈 요일별 인쇄 건수 비교")
    
    fig_prints = px.bar(
        weekly_df,
        x='day',
        y='prints',
        title='요일별 인쇄 건수 (수요일: 페이퍼리스 데이)',
        color='is_paperless',
        color_discrete_map={True: '#28a745', False: '#6c757d'},
        labels={'prints': '인쇄 건수', 'day': '요일'}
    )
    fig_prints.update_layout(
        xaxis_title="요일",
        yaxis_title="인쇄 건수"
    )
    st.plotly_chart(fig_prints, use_container_width=True)

    st.markdown("---")

    # 디지털 사용률 차트
    st.subheader("💻 요일별 디지털 사용률")
    
    fig_digital = px.line(
        weekly_df,
        x='day',
        y='digital_usage',
        title='요일별 디지털 사용률',
        markers=True,
        labels={'digital_usage': '디지털 사용률 (%)', 'day': '요일'},
        color_discrete_sequence=['#007bff']
    )
    fig_digital.update_layout(
        xaxis_title="요일",
        yaxis_title="디지털 사용률 (%)",
        yaxis=dict(range=[0, 100])
    )
    st.plotly_chart(fig_digital, use_container_width=True)

    st.markdown("---")

    # 페이퍼리스 데이 참여 현황
    st.subheader("🎯 페이퍼리스 데이 참여 현황")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #d4edda;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #155724;">📄</h3>
            <h4 style="margin: 10px 0; color: #155724;">페이퍼리스 데이</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                참여 부서: {departments}개
            </p>
            <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                참여 직원: {employees}명
            </p>
        </div>
        """.format(
            departments=np.random.randint(8, 15),
            employees=np.random.randint(120, 200)
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            border: 2px solid #007bff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #cce7ff;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #004085;">💻</h3>
            <h4 style="margin: 10px 0; color: #004085;">디지털 도구 사용</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #004085;">
                Knox meeting: {knox_meeting}%
            </p>
            <p style="margin: 5px 0; font-size: 16px; color: #004085;">
                PDF 회의: {pdf_meeting}%
            </p>
        </div>
        """.format(
            knox_meeting=np.random.randint(85, 95),
            pdf_meeting=np.random.randint(70, 85)
        ), unsafe_allow_html=True)

    st.markdown("---")

    # 탄소감축량 지표 산식 설명
    st.subheader("📊 탄소감축량 지표 산식")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🌱 탄소감축량 계산 공식**
        
        ```
        감축량(kg CO₂eq) = N × Ep
        ```
        
        **📋 변수 정의**
        - **N**: 줄인 종이 사용 장수 (장)
        - **Ep**: A4 1장당 배출계수 (0.00288 kg CO₂eq/장)
        
        **🎯 계산 기준**
        - A4 용지 1장당 탄소배출량: 0.00288 kg CO₂eq
        - 국제 탄소 배출 계수 기준 적용
        - 종이 생산 과정의 탄소발자국 고려
        """)
    
    with col2:
        st.success("""
        **📄 예시 계산**
        
        연간 10,000장을 절약했다면:
        
        ```
        10,000 × 0.00288 = 28.8 kg CO₂eq
        ```
        
        **🌍 환경 효과**
        • **산림 보호**: 종이 사용 감소로 나무 보존
        • **탄소 감축**: 직접적인 CO₂ 배출량 감소
        • **에너지 절약**: 종이 생산 과정 에너지 절약
        • **폐기물 감소**: 종이 폐기물 발생량 감소
        """)
    
    # 실시간 계산 예시
    st.markdown("---")
    st.subheader("🧮 실시간 계산 예시")
    
    current_data = st.session_state.paperless_data
    carbon_example = current_data['N'] * current_data['Ep']
    
    st.markdown(f"""
    <div style="
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #d4edda;
        margin-bottom: 10px;
    ">
        <h3 style="margin: 0; color: #155724;">📈 현재 상황</h3>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>줄인 종이 사용량:</strong> {current_data['N']:,}장
        </p>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>계산식:</strong> {current_data['N']:,}장 × {current_data['Ep']}kg CO₂eq/장
        </p>
        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #155724;">
            <strong>= {carbon_example:.2f}kg CO₂eq</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 환경 효과 및 절약 효과
    st.subheader("🌱 환경 효과 및 절약 효과")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="절약된 종이",
            value=f"{st.session_state.paperless_data['total_paper_purchase'] * 0.3:.1f}L",
            delta="주간 절약"
        )
    
    with col2:
        st.metric(
            label="CO2 절약",
            value=f"{st.session_state.paperless_data['total_paper_purchase'] * 0.3 * 0.5:.1f}kg",
            delta="주간 절약"
        )
    
    with col3:
        st.metric(
            label="나무 보호",
            value=f"{st.session_state.paperless_data['total_paper_purchase'] * 0.3 * 0.02:.1f}그루",
            delta="주간 절약"
        )

    st.markdown("---")

    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", use_container_width=True):
            # 새로운 샘플 데이터 생성
            base_prints = np.random.randint(200, 400)
            base_paper_purchase = np.random.randint(50, 100)
            paperless_day_prints = int(base_prints * 0.7)
            paperless_day_paper = int(base_paper_purchase * 0.75)
            
            weekly_data = []
            days = ['월', '화', '수', '목', '금']
            for i, day in enumerate(days):
                if day == '수':
                    weekly_data.append({
                        'day': day,
                        'prints': np.random.randint(paperless_day_prints-20, paperless_day_prints+20),
                        'paper_purchase': np.random.randint(paperless_day_paper-5, paperless_day_paper+5),
                        'digital_usage': np.random.randint(80, 95),
                        'is_paperless': True
                    })
                else:
                    weekly_data.append({
                        'day': day,
                        'prints': np.random.randint(base_prints-30, base_prints+30),
                        'paper_purchase': np.random.randint(base_paper_purchase-10, base_paper_purchase+10),
                        'digital_usage': np.random.randint(40, 60),
                        'is_paperless': False
                    })
            
            # 탄소감축량 계산을 위한 변수들
            N = np.random.randint(5000, 15000)  # 줄인 종이 사용 장수 (장)
            Ep = 0.00288  # A4 1장당 배출계수 (kg CO₂eq/장)
            carbon_reduction = N * Ep  # 탄소감축량 계산
            
            st.session_state.paperless_data = {
                "weekly_data": weekly_data,
                "total_prints": sum(day['prints'] for day in weekly_data),
                "total_paper_purchase": sum(day['paper_purchase'] for day in weekly_data),
                "digital_adoption_rate": np.random.randint(65, 80),
                "paper_savings": np.random.randint(20, 35),
                "cost_savings": np.random.randint(500, 800),
                # 탄소감축량 관련
                "N": N,
                "Ep": Ep,
                "carbon_reduction": carbon_reduction
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", use_container_width=True):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 상세 리포트", use_container_width=True):
            st.info("상세 리포트를 생성했습니다!")

# 소등·절전 챌린지 페이지
elif menu == "소등·절전 챌린지":
    st.title("💡 소등·절전 챌린지")
    st.write("삼성SDS 5개 사옥에서 퇴근 후 불필요한 조명·모니터 끄기와 점심시간 조명 절반 소등을 통해 전력 사용량을 줄입니다.")

    # 사옥 정보
    buildings = {
        "잠실": {
            "name": "잠실 사옥",
            "image": "🏢",
            "participants": 0,
            "power_saved": 0,
            "lights_off_rate": 0,
            "monitors_off_rate": 0
        },
        "판교IT": {
            "name": "판교 IT 사옥", 
            "image": "🏢",
            "participants": 0,
            "power_saved": 0,
            "lights_off_rate": 0,
            "monitors_off_rate": 0
        },
        "판교물류": {
            "name": "판교 물류 사옥",
            "image": "🏢", 
            "participants": 0,
            "power_saved": 0,
            "lights_off_rate": 0,
            "monitors_off_rate": 0
        },
        "상암": {
            "name": "상암 사옥",
            "image": "🏢",
            "participants": 0,
            "power_saved": 0,
            "lights_off_rate": 0,
            "monitors_off_rate": 0
        },
        "수원": {
            "name": "수원 사옥",
            "image": "🏢",
            "participants": 0,
            "power_saved": 0,
            "lights_off_rate": 0,
            "monitors_off_rate": 0
        }
    }

    # 소등·절전 챌린지 정보
    power_saving_info = {
        "name": "소등·절전 챌린지",
        "description": "퇴근 후 불필요한 조명·모니터 끄기, 점심시간 조명 절반 소등을 통한 전력 절약",
        "target_time": "퇴근 후 (18:00~), 점심시간 (12:00~13:00)",
        "goal": "월별 전력 사용량 20% 감소, 전기요금 절약"
    }

    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'power_saving_data' not in st.session_state:
        # 샘플 데이터 생성
        sample_buildings = {
            "잠실": {
                "name": "잠실 사옥",
                "image": "🏢",
                "participants": np.random.randint(25, 45),
                "power_saved": np.random.randint(150, 250),  # kWh
                "lights_off_rate": np.random.randint(80, 95),
                "monitors_off_rate": np.random.randint(70, 90)
            },
            "판교IT": {
                "name": "판교 IT 사옥", 
                "image": "🏢",
                "participants": np.random.randint(30, 50),
                "power_saved": np.random.randint(180, 280),
                "lights_off_rate": np.random.randint(85, 95),
                "monitors_off_rate": np.random.randint(75, 90)
            },
            "판교물류": {
                "name": "판교 물류 사옥",
                "image": "🏢", 
                "participants": np.random.randint(20, 35),
                "power_saved": np.random.randint(120, 200),
                "lights_off_rate": np.random.randint(75, 90),
                "monitors_off_rate": np.random.randint(65, 85)
            },
            "상암": {
                "name": "상암 사옥",
                "image": "🏢",
                "participants": np.random.randint(22, 40),
                "power_saved": np.random.randint(140, 220),
                "lights_off_rate": np.random.randint(80, 95),
                "monitors_off_rate": np.random.randint(70, 90)
            },
            "수원": {
                "name": "수원 사옥",
                "image": "🏢",
                "participants": np.random.randint(18, 30),
                "power_saved": np.random.randint(100, 180),
                "lights_off_rate": np.random.randint(75, 90),
                "monitors_off_rate": np.random.randint(65, 85)
            }
        }
        
        # 전체 통계 계산
        total_participants = sum(building['participants'] for building in sample_buildings.values())
        total_power_saved = sum(building['power_saved'] for building in sample_buildings.values())
        total_bill_saved = total_power_saved * 120  # kWh당 120원
        
        # 탄소감축량 계산을 위한 변수들
        P = 0.05  # 조명 1개의 소비전력 (kW)
        H = np.random.randint(2, 6)  # 소등 시간 (시간 단위, hr)
        N = np.random.randint(100, 200)  # 조명 개수
        EF = 0.459  # 전력 배출계수 (kgCO₂eq/kWh, 한국전력 기준)
        carbon_reduction = P * H * N * EF  # 탄소감축량 계산
        
        st.session_state.power_saving_data = {
            "buildings": sample_buildings,
            "total_participants": total_participants,
            "total_power_saved": total_power_saved,
            "total_bill_saved": total_bill_saved,
            "participation_rate": np.random.randint(85, 95),
            "average_daily_saving": total_power_saved // 30,
            # 탄소감축량 관련
            "P": P,
            "H": H,
            "N": N,
            "EF": EF,
            "carbon_reduction": carbon_reduction
        }

    st.markdown("---")

    # 소등·절전 챌린지 정보 카드
    st.subheader("📋 소등·절전 챌린지 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **⏰ 대상 시간**: {power_saving_info['target_time']}
        
        **🎯 목표**: {power_saving_info['goal']}
        
        **📝 설명**: {power_saving_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **🌱 환경효과**: 전력 사용량 감소로 탄소 배출 줄이기
        
        **💰 경제효과**: 전기요금 절약으로 운영비용 감소
        
        **⚡ 효율성**: 에너지 효율적인 업무 환경 구축
        """)

    st.markdown("---")

    # 오늘 날짜 표시
    today = datetime.now().strftime("%Y년 %m월 %d일")
    st.subheader(f"📅 {today} 소등·절전 챌린지 현황")

    # 사옥별 카드 레이아웃
    cols = st.columns(5)
    
    for i, (building_key, building_info) in enumerate(st.session_state.power_saving_data['buildings'].items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                margin-bottom: 10px;
            ">
                <h3 style="margin: 0; color: #1e3a8a;">{building_info['image']}</h3>
                <h4 style="margin: 10px 0; color: #333;">{building_info['name']}</h4>
                <p style="margin: 5px 0; font-size: 16px; font-weight: bold; color: #28a745;">
                    참여자: {building_info['participants']}명
                </p>
                <p style="margin: 5px 0; font-size: 14px; color: #007bff;">
                    절약량: {building_info['power_saved']}kWh
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                    조명소등: {building_info['lights_off_rate']}%
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                    모니터소등: {building_info['monitors_off_rate']}%
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 등록 버튼
            if st.button(f"절전 등록", key=f"power_register_{building_key}", use_container_width=True):
                st.session_state.power_saving_data['buildings'][building_key]['participants'] += 1
                additional_power = np.random.randint(5, 15)
                st.session_state.power_saving_data['buildings'][building_key]['power_saved'] += additional_power
                st.session_state.power_saving_data['total_participants'] += 1
                st.session_state.power_saving_data['total_power_saved'] += additional_power
                st.session_state.power_saving_data['total_bill_saved'] += additional_power * 120
                st.success(f"{building_info['name']}에 절전 등록 완료! 💡")
                st.rerun()

    st.markdown("---")

    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="총 참여자",
            value=f"{st.session_state.power_saving_data['total_participants']}명",
            delta=f"+{np.random.randint(5, 15)}명"
        )
    
    with col2:
        st.metric(
            label="총 전력 절약",
            value=f"{st.session_state.power_saving_data['total_power_saved']}kWh",
            delta=f"+{np.random.randint(20, 50)}kWh"
        )
    
    with col3:
        st.metric(
            label="전기요금 절약",
            value=f"{st.session_state.power_saving_data['total_bill_saved']:,}원",
            delta=f"+{np.random.randint(2000, 6000):,}원"
        )
    
    with col4:
        st.metric(
            label="참여율",
            value=f"{st.session_state.power_saving_data['participation_rate']}%",
            delta=f"+{np.random.randint(3, 8)}%"
        )
    
    with col5:
        st.metric(
            label="탄소감축량",
            value=f"{st.session_state.power_saving_data['carbon_reduction']:.2f}kg",
            delta="CO₂eq"
        )

    st.markdown("---")

    # 사옥별 전력 절약 현황 차트
    st.subheader("🏢 사옥별 전력 절약 현황")
    
    building_names = list(st.session_state.power_saving_data['buildings'].keys())
    power_saved_amounts = [building['power_saved'] for building in st.session_state.power_saving_data['buildings'].values()]
    
    fig_power = px.bar(
        x=building_names,
        y=power_saved_amounts,
        title='사옥별 전력 절약량',
        labels={'x': '사옥', 'y': '절약량 (kWh)'},
        color=power_saved_amounts,
        color_continuous_scale='Greens'
    )
    fig_power.update_layout(
        xaxis_title="사옥",
        yaxis_title="절약량 (kWh)"
    )
    st.plotly_chart(fig_power, use_container_width=True)

    st.markdown("---")

    # 사옥별 참여자 수 차트
    st.subheader("👥 사옥별 참여자 수")
    
    participants_counts = [building['participants'] for building in st.session_state.power_saving_data['buildings'].values()]
    
    fig_participants = px.bar(
        x=building_names,
        y=participants_counts,
        title='사옥별 참여자 수',
        labels={'x': '사옥', 'y': '참여자 수'},
        color=participants_counts,
        color_continuous_scale='Blues'
    )
    fig_participants.update_layout(
        xaxis_title="사옥",
        yaxis_title="참여자 수"
    )
    st.plotly_chart(fig_participants, use_container_width=True)

    st.markdown("---")

    # 탄소감축량 지표 산식
    st.subheader("📊 탄소감축량 지표 산식")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🌱 탄소감축량 계산 공식**
        ```
        감축량(kgCO₂eq) = P × H × N × EF
        ```
        **📋 변수 정의**
        - **P**: 조명 1개의 소비전력 (kW)
        - **H**: 소등 시간 (시간 단위, hr)
        - **N**: 조명 개수
        - **EF**: 전력 배출계수 (0.459 kgCO₂eq/kWh, 한국전력 기준)
        **🎯 계산 기준**
        - 조명 1개당 소비전력: 0.05kW
        - 소등 시간: 2-6시간 (평균 4시간)
        - 조명 개수: 100-200개
        - 한국전력 배출계수: 0.459 kgCO₂eq/kWh
        """)
    
    with col2:
        st.success("""
        **⚡ 전력 배출계수 정보**
        ```
        EF = 0.459 kgCO₂eq/kWh
        ```
        **📋 배출계수 기준**
        - **대한민국 공식 계수**: 0.459 kgCO₂eq/kWh
        - **동일 계수**: 0.459 tCO₂eq/MWh
        - **국가별 차이**: 국가에 따라 달라짐
        - **한국전력 기준**: 공식 인증 계수 사용
        **🌍 환경 효과**
        • **탄소 감축**: 직접적인 CO₂ 배출량 감소
        • **에너지 절약**: 전력 사용량 감소
        • **친환경 문화**: 지속가능한 에너지 사용
        • **경제 효과**: 전기요금 절약
        """)
    
    st.subheader("🧮 실시간 계산 예시")
    current_data = st.session_state.power_saving_data
    carbon_example = current_data['P'] * current_data['H'] * current_data['N'] * current_data['EF']
    st.markdown(f"""
    <div style="
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #d4edda;
        margin-bottom: 10px;
    ">
        <h3 style="margin: 0; color: #155724;">📈 현재 상황</h3>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>조명 소비전력:</strong> {current_data['P']}kW
        </p>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>소등 시간:</strong> {current_data['H']}시간
        </p>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>조명 개수:</strong> {current_data['N']}개
        </p>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>배출계수:</strong> {current_data['EF']} kgCO₂eq/kWh
        </p>
        <p style="margin: 10px 0; font-size: 18px; color: #155724;">
            <strong>계산식:</strong> {current_data['P']} × {current_data['H']} × {current_data['N']} × {current_data['EF']}
        </p>
        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #155724;">
            <strong>= {carbon_example:.2f}kg CO₂eq</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 환경 효과
    st.subheader("🌱 환경 효과")
    
    col1, col2, col3 = st.columns(3)
    
    total_saved = st.session_state.power_saving_data['total_power_saved']
    
    with col1:
        st.metric(
            label="CO2 절약",
            value=f"{total_saved * 0.4:.1f}kg",
            delta="월간 절약"
        )
    
    with col2:
        st.metric(
            label="나무 보호",
            value=f"{total_saved * 0.01:.1f}그루",
            delta="월간 보호"
        )
    
    with col3:
        st.metric(
            label="환경등가",
            value=f"{total_saved * 0.05:.1f}L",
            delta="휘발유 절약"
        )

    st.markdown("---")

    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            sample_buildings = {
                "잠실": {
                    "name": "잠실 사옥",
                    "image": "🏢",
                    "participants": np.random.randint(25, 45),
                    "power_saved": np.random.randint(150, 250),
                    "lights_off_rate": np.random.randint(80, 95),
                    "monitors_off_rate": np.random.randint(70, 90)
                },
                "판교IT": {
                    "name": "판교 IT 사옥", 
                    "image": "🏢",
                    "participants": np.random.randint(30, 50),
                    "power_saved": np.random.randint(180, 280),
                    "lights_off_rate": np.random.randint(85, 95),
                    "monitors_off_rate": np.random.randint(75, 90)
                },
                "판교물류": {
                    "name": "판교 물류 사옥",
                    "image": "🏢", 
                    "participants": np.random.randint(20, 35),
                    "power_saved": np.random.randint(120, 200),
                    "lights_off_rate": np.random.randint(75, 90),
                    "monitors_off_rate": np.random.randint(65, 85)
                },
                "상암": {
                    "name": "상암 사옥",
                    "image": "🏢",
                    "participants": np.random.randint(22, 40),
                    "power_saved": np.random.randint(140, 220),
                    "lights_off_rate": np.random.randint(80, 95),
                    "monitors_off_rate": np.random.randint(70, 90)
                },
                "수원": {
                    "name": "수원 사옥",
                    "image": "🏢",
                    "participants": np.random.randint(18, 30),
                    "power_saved": np.random.randint(100, 180),
                    "lights_off_rate": np.random.randint(75, 90),
                    "monitors_off_rate": np.random.randint(65, 85)
                }
            }
            
            # 전체 통계 재계산
            total_participants = sum(building['participants'] for building in sample_buildings.values())
            total_power_saved = sum(building['power_saved'] for building in sample_buildings.values())
            total_bill_saved = total_power_saved * 120
            
            # 탄소감축량 계산을 위한 변수들
            P = 0.05  # 조명 1개의 소비전력 (kW)
            H = np.random.randint(2, 6)  # 소등 시간 (시간 단위, hr)
            N = np.random.randint(100, 200)  # 조명 개수
            EF = 0.459  # 전력 배출계수 (kgCO₂eq/kWh, 한국전력 기준)
            carbon_reduction = P * H * N * EF  # 탄소감축량 계산
            
            st.session_state.power_saving_data = {
                "buildings": sample_buildings,
                "total_participants": total_participants,
                "total_power_saved": total_power_saved,
                "total_bill_saved": total_bill_saved,
                "participation_rate": np.random.randint(85, 95),
                "average_daily_saving": total_power_saved // 30,
                # 탄소감축량 관련
                "P": P,
                "H": H,
                "N": N,
                "EF": EF,
                "carbon_reduction": carbon_reduction
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 절전 리포트", width='stretch'):
            st.info("절전 리포트를 생성했습니다!")

# 플로깅 데이 페이지
elif menu == "플로깅 데이":
    st.title("🚮 플로깅 데이 (Plogging Day)")
    st.write("점심시간에 사무실 주변 쓰레기 줍기 산책을 통해 환경정화 활동을 실시합니다.")

    # 플로깅 데이 정보
    plogging_info = {
        "name": "플로깅 데이",
        "description": "점심시간에 사무실 주변 쓰레기 줍기 산책 실시",
        "schedule": "매주 화요일, 목요일 점심시간 (12:00~13:00)",
        "goal": "분리 배출 쓰레기 총량 감소, 참여 직원 수 증가"
    }

    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'plogging_data' not in st.session_state:
        # 샘플 데이터 생성
        total_participants = np.random.randint(45, 80)
        total_waste_collected = np.random.randint(120, 200)  # kg
        plastic_bottles = np.random.randint(30, 60)
        cans = np.random.randint(20, 40)
        paper_waste = np.random.randint(15, 30)
        other_waste = np.random.randint(55, 70)
        
        # 순환율 계산을 위한 변수들 (톤 단위)
        R = np.random.randint(15, 25)  # 실질 재활용량 (톤)
        C = np.random.randint(8, 15)   # 자원순환으로 인정된 물량 (톤)
        W = np.random.randint(40, 60)  # 폐기물 총 발생량 (톤)
        
        # 기존 순환율 계산
        original_circular_rate = ((R + C) / (W + C)) * 100
        
        # 플로깅 활동으로 인한 개선량
        delta_R = np.random.randint(2, 5)  # 재활용량 증가 (톤)
        delta_C = np.random.randint(1, 3)  # 자원순환량 증가 (톤)
        
        # 개선된 순환율 계산
        improved_circular_rate = (((R + delta_R) + (C + delta_C)) / (W + C + delta_C)) * 100
        
        # 순환율 개선 정도
        circular_rate_improvement = improved_circular_rate - original_circular_rate
        
        # 주간 데이터 생성
        weekly_data = []
        days = ['월', '화', '수', '목', '금']
        for i, day in enumerate(days):
            if day in ['화', '목']:  # 플로깅 데이
                weekly_data.append({
                    'day': day,
                    'participants': np.random.randint(8, 15),
                    'waste_collected': np.random.randint(20, 35),
                    'is_plogging_day': True
                })
            else:
                weekly_data.append({
                    'day': day,
                    'participants': 0,
                    'waste_collected': 0,
                    'is_plogging_day': False
                })
        
        st.session_state.plogging_data = {
            "total_participants": total_participants,
            "total_waste_collected": total_waste_collected,
            "plastic_bottles": plastic_bottles,
            "cans": cans,
            "paper_waste": paper_waste,
            "other_waste": other_waste,
            "weekly_data": weekly_data,
            "participation_rate": np.random.randint(75, 90),
            # 순환율 관련
            "R": R,
            "C": C,
            "W": W,
            "delta_R": delta_R,
            "delta_C": delta_C,
            "original_circular_rate": original_circular_rate,
            "improved_circular_rate": improved_circular_rate,
            "circular_rate_improvement": circular_rate_improvement
        }

    st.markdown("---")

    # 플로깅 데이 정보 카드
    st.subheader("📋 플로깅 데이 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 일정**: {plogging_info['schedule']}
        
        **🎯 목표**: {plogging_info['goal']}
        
        **📝 설명**: {plogging_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **🌱 환경효과**: 쓰레기 수거로 지역 환경 정화
        
        **🏃 건강효과**: 산책을 통한 건강 증진
        
        **🤝 사회효과**: 지역사회 환경 보호 기여
        """)

    st.markdown("---")

    # 참여 등록 섹션
    st.subheader("🎮 참여 등록")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #d4edda;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #155724;">🚮</h3>
            <h4 style="margin: 10px 0; color: #155724;">플로깅 참여</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                참여자: {participants}명
            </p>
        </div>
        """.format(participants=st.session_state.plogging_data['total_participants']), unsafe_allow_html=True)
        
        if st.button("플로깅 참여", key="plogging_participate", use_container_width=True):
            st.session_state.plogging_data['total_participants'] += 1
            st.success("플로깅 데이 참여 등록 완료! 🌱")
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="
            border: 2px solid #17a2b8;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #d1ecf1;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #0c5460;">♻️</h3>
            <h4 style="margin: 10px 0; color: #0c5460;">쓰레기 수거</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #0c5460;">
                수거량: {waste}kg
            </p>
        </div>
        """.format(waste=st.session_state.plogging_data['total_waste_collected']), unsafe_allow_html=True)
        
        if st.button("쓰레기 수거 등록", key="waste_collect", use_container_width=True):
            additional_waste = np.random.randint(5, 15)
            st.session_state.plogging_data['total_waste_collected'] += additional_waste
            st.success(f"쓰레기 {additional_waste}kg 수거 등록 완료! ♻️")
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #fff3cd;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #856404;">📊</h3>
            <h4 style="margin: 10px 0; color: #856404;">참여율</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #856404;">
                참여율: {rate}%
            </p>
        </div>
        """.format(rate=st.session_state.plogging_data['participation_rate']), unsafe_allow_html=True)
        
        if st.button("통계 새로고침", key="refresh_stats", use_container_width=True):
            st.info("통계 데이터를 새로고침했습니다!")

    st.markdown("---")

    # 주간 현황
    st.subheader("📊 주간 현황")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="총 참여자",
            value=f"{st.session_state.plogging_data['total_participants']}명",
            delta=f"+{np.random.randint(2, 8)}명"
        )
    
    with col2:
        st.metric(
            label="쓰레기 수거량",
            value=f"{st.session_state.plogging_data['total_waste_collected']}kg",
            delta=f"+{np.random.randint(5, 15)}kg"
        )
    
    with col3:
        st.metric(
            label="참여율",
            value=f"{st.session_state.plogging_data['participation_rate']}%",
            delta=f"+{np.random.randint(3, 8)}%"
        )
    
    with col4:
        st.metric(
            label="환경 점수",
            value=f"{st.session_state.plogging_data['total_waste_collected'] * 2}점",
            delta=f"+{np.random.randint(10, 30)}점"
        )
    
    with col5:
        st.metric(
            label="순환율 개선",
            value=f"{st.session_state.plogging_data['circular_rate_improvement']:.1f}%p",
            delta="개선"
        )

    st.markdown("---")

    # 요일별 참여 현황
    st.subheader("📅 요일별 참여 현황")
    
    weekly_df = pd.DataFrame(st.session_state.plogging_data['weekly_data'])
    
    fig_weekly = px.bar(
        weekly_df,
        x='day',
        y='participants',
        title='요일별 플로깅 참여자 수',
        color='is_plogging_day',
        color_discrete_map={True: '#28a745', False: '#6c757d'},
        labels={'participants': '참여자 수', 'day': '요일'}
    )
    fig_weekly.update_layout(
        xaxis_title="요일",
        yaxis_title="참여자 수"
    )
    st.plotly_chart(fig_weekly, use_container_width=True)

    st.markdown("---")

    # 쓰레기 유형별 수거 현황
    st.subheader("♻️ 쓰레기 유형별 수거 현황")
    
    waste_types = ['플라스틱 병', '캔', '종이류', '기타']
    waste_amounts = [
        st.session_state.plogging_data['plastic_bottles'],
        st.session_state.plogging_data['cans'],
        st.session_state.plogging_data['paper_waste'],
        st.session_state.plogging_data['other_waste']
    ]
    
    fig_waste = px.pie(
        values=waste_amounts,
        names=waste_types,
        title='쓰레기 유형별 수거 비율',
        color_discrete_sequence=['#82ca9d', '#8884d8', '#ffc658', '#ff7300']
    )
    fig_waste.update_layout(height=400)
    st.plotly_chart(fig_waste, use_container_width=True)

    st.markdown("---")

    # 순환율 개선 지표 산식
    st.subheader("📊 순환율 개선 지표 산식")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **♻️ 기본 순환율 산정식**
        ```
        순환율(%) = (R + C) / (W + C) × 100
        ```
        **📋 변수 정의**
        - **R**: 실질 재활용량 (톤 단위)
        - **C**: 자원순환으로 인정된 물량 (재사용, 에너지회수량 등, 톤)
        - **W**: 폐기물 총 발생량 (톤 단위)
        **🎯 계산 기준**
        - 재활용과 자원순환 인정분을 폐기물 총량과 합산한 분모에 대비해 비율 산출
        - 플로깅 활동으로 수거된 쓰레기의 재활용 및 자원순환 효과 반영
        """)
    
    with col2:
        st.success("""
        **📈 순환율 개선 계산**
        ```
        개선 순환율 = ((R+ΔR) + (C+ΔC)) / (W + C + ΔC) × 100
        ```
        **📋 개선 변수**
        - **ΔR**: 재활용량 증가분 (톤)
        - **ΔC**: 자원순환량 증가분 (톤)
        **🎯 개선 정도**
        ```
        Δ순환율 = 개선 순환율 - 기존 순환율
        ```
        **🌍 환경 효과**
        • **재활용률 향상**: 쓰레기 수거로 재활용 가능 물질 증가
        • **자원순환 증대**: 에너지 회수 및 재사용 물량 증가
        • **폐기물 감소**: 총 발생량 대비 순환 이용률 향상
        """)
    
    st.subheader("🧮 실시간 계산 예시")
    current_data = st.session_state.plogging_data
    original_rate = current_data['original_circular_rate']
    improved_rate = current_data['improved_circular_rate']
    improvement = current_data['circular_rate_improvement']
    
    st.markdown(f"""
    <div style="
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #d4edda;
        margin-bottom: 10px;
    ">
        <h3 style="margin: 0; color: #155724;">📈 현재 상황</h3>
        <div style="display: flex; justify-content: space-around; margin: 20px 0;">
            <div>
                <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                    <strong>기존 순환율:</strong><br>
                    ({current_data['R']} + {current_data['C']}) / ({current_data['W']} + {current_data['C']}) × 100<br>
                    = <strong>{original_rate:.1f}%</strong>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                    <strong>개선 순환율:</strong><br>
                    (({current_data['R']}+{current_data['delta_R']}) + ({current_data['C']}+{current_data['delta_C']})) / ({current_data['W']} + {current_data['C']} + {current_data['delta_C']}) × 100<br>
                    = <strong>{improved_rate:.1f}%</strong>
                </p>
            </div>
        </div>
        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #155724;">
            <strong>순환율 개선: +{improvement:.1f}%p</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 환경 효과
    st.subheader("🌱 환경 효과")
    
    col1, col2, col3 = st.columns(3)
    
    total_waste = st.session_state.plogging_data['total_waste_collected']
    
    with col1:
        st.metric(
            label="CO2 절약",
            value=f"{total_waste * 0.3:.1f}kg",
            delta="월간 절약"
        )
    
    with col2:
        st.metric(
            label="재활용률",
            value=f"{(total_waste * 0.7):.1f}kg",
            delta="재활용 가능"
        )
    
    with col3:
        st.metric(
            label="환경 점수",
            value=f"{total_waste * 2}점",
            delta="누적 점수"
        )

    st.markdown("---")

    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            total_participants = np.random.randint(45, 80)
            total_waste_collected = np.random.randint(120, 200)
            plastic_bottles = np.random.randint(30, 60)
            cans = np.random.randint(20, 40)
            paper_waste = np.random.randint(15, 30)
            other_waste = np.random.randint(55, 70)
            
            # 순환율 계산을 위한 변수들 (톤 단위)
            R = np.random.randint(15, 25)  # 실질 재활용량 (톤)
            C = np.random.randint(8, 15)   # 자원순환으로 인정된 물량 (톤)
            W = np.random.randint(40, 60)  # 폐기물 총 발생량 (톤)
            
            # 기존 순환율 계산
            original_circular_rate = ((R + C) / (W + C)) * 100
            
            # 플로깅 활동으로 인한 개선량
            delta_R = np.random.randint(2, 5)  # 재활용량 증가 (톤)
            delta_C = np.random.randint(1, 3)  # 자원순환량 증가 (톤)
            
            # 개선된 순환율 계산
            improved_circular_rate = (((R + delta_R) + (C + delta_C)) / (W + C + delta_C)) * 100
            
            # 순환율 개선 정도
            circular_rate_improvement = improved_circular_rate - original_circular_rate
            
            weekly_data = []
            days = ['월', '화', '수', '목', '금']
            for i, day in enumerate(days):
                if day in ['화', '목']:
                    weekly_data.append({
                        'day': day,
                        'participants': np.random.randint(8, 15),
                        'waste_collected': np.random.randint(20, 35),
                        'is_plogging_day': True
                    })
                else:
                    weekly_data.append({
                        'day': day,
                        'participants': 0,
                        'waste_collected': 0,
                        'is_plogging_day': False
                    })
            
            st.session_state.plogging_data = {
                "total_participants": total_participants,
                "total_waste_collected": total_waste_collected,
                "plastic_bottles": plastic_bottles,
                "cans": cans,
                "paper_waste": paper_waste,
                "other_waste": other_waste,
                "weekly_data": weekly_data,
                "participation_rate": np.random.randint(75, 90),
                # 순환율 관련
                "R": R,
                "C": C,
                "W": W,
                "delta_R": delta_R,
                "delta_C": delta_C,
                "original_circular_rate": original_circular_rate,
                "improved_circular_rate": improved_circular_rate,
                "circular_rate_improvement": circular_rate_improvement
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 플로깅 리포트", width='stretch'):
            st.info("플로깅 리포트를 생성했습니다!")

# 탄소 발자국 챌린지 페이지
elif menu == "탄소 발자국 챌린지":
    st.title("👣 탄소 발자국 챌린지")
    st.write("엘리베이터 대신 계단 이용, 대중교통 출근, 자전거 이용을 독려하여 탄소 감축을 실현합니다.")

    # 탄소 발자국 챌린지 정보
    carbon_footprint_info = {
        "name": "탄소 발자국 챌린지",
        "description": "엘리베이터 대신 계단 이용, 대중교통 출근, 자전거 이용 독려",
        "target": "일상생활에서의 탄소 감축 실천",
        "goal": "참여 건수 증가, 출퇴근 교통수단별 탄소감축량 계산"
    }

    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'carbon_footprint_data' not in st.session_state:
        # 샘플 데이터 생성
        total_participations = np.random.randint(200, 350)
        stairs_usage = np.random.randint(80, 120)
        public_transport = np.random.randint(60, 100)
        bicycle_usage = np.random.randint(40, 80)
        
        # 탄소감축량 계산을 위한 변수들
        P_elevator = 0.05  # 엘리베이터 1회 이용 시 소비 전력 (kWh)
        EF = 0.459  # 전력 배출계수 (kgCO₂eq/kWh)
        E_car = 2.2  # 자가용 1회 평균 배출량 (kgCO₂eq)
        E_transit = 0.6  # 대중교통 1회 평균 배출량 (kgCO₂eq)
        
        # 각 항목별 탄소감축량 계산
        C_stairs = stairs_usage * P_elevator * EF  # 계단 이용에 의한 감축량
        C_transit = public_transport * (E_car - E_transit)  # 대중교통 이용에 의한 감축량
        C_bike = bicycle_usage * E_car  # 자전거 이용에 의한 감축량
        
        # 총 탄소감축량
        total_carbon_reduction = C_stairs + C_transit + C_bike
        
        # 교통수단별 탄소 감축량 (kg CO2)
        carbon_savings = {
            'stairs': C_stairs,
            'public_transport': C_transit,
            'bicycle': C_bike
        }
        
        # 일별 데이터 생성 (최근 30일)
        daily_data = []
        for i in range(30):
            day = (datetime.now() - timedelta(days=29-i)).strftime("%m/%d")
            weekday = (datetime.now() - timedelta(days=29-i)).weekday()
            
            if weekday < 5:  # 평일
                daily_participations = np.random.randint(8, 15)
                daily_carbon_saved = daily_participations * np.random.uniform(0.1, 0.3)
            else:  # 주말
                daily_participations = np.random.randint(3, 8)
                daily_carbon_saved = daily_participations * np.random.uniform(0.1, 0.2)
            
            daily_data.append({
                'date': day,
                'participations': daily_participations,
                'carbon_saved': daily_carbon_saved,
                'is_weekday': weekday < 5
            })
        
        st.session_state.carbon_footprint_data = {
            "total_participations": total_participations,
            "stairs_usage": stairs_usage,
            "public_transport": public_transport,
            "bicycle_usage": bicycle_usage,
            "carbon_savings": carbon_savings,
            "daily_data": daily_data,
            "participation_rate": np.random.randint(70, 85),
            # 탄소감축량 관련
            "P_elevator": P_elevator,
            "EF": EF,
            "E_car": E_car,
            "E_transit": E_transit,
            "C_stairs": C_stairs,
            "C_transit": C_transit,
            "C_bike": C_bike,
            "total_carbon_reduction": total_carbon_reduction
        }

    st.markdown("---")

    # 탄소 발자국 챌린지 정보 카드
    st.subheader("📋 탄소 발자국 챌린지 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **🎯 목표**: {carbon_footprint_info['target']}
        
        **📊 지표**: {carbon_footprint_info['goal']}
        
        **📝 설명**: {carbon_footprint_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **🌱 환경효과**: 일상생활에서의 탄소 감축 실천
        
        **🏃 건강효과**: 계단 이용, 자전거 타기로 건강 증진
        
        **💰 경제효과**: 교통비 절약, 에너지 비용 절감
        """)

    st.markdown("---")

    # 참여 등록 섹션
    st.subheader("🎮 참여 등록")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #d4edda;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #155724;">🪜</h3>
            <h4 style="margin: 10px 0; color: #155724;">계단 이용</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                참여: {stairs}회
            </p>
        </div>
        """.format(stairs=st.session_state.carbon_footprint_data['stairs_usage']), unsafe_allow_html=True)
        
        if st.button("계단 이용 등록", key="stairs_usage", use_container_width=True):
            st.session_state.carbon_footprint_data['stairs_usage'] += 1
            st.session_state.carbon_footprint_data['total_participations'] += 1
            st.session_state.carbon_footprint_data['carbon_savings']['stairs'] += 0.05
            st.success("계단 이용 등록 완료! 🪜")
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="
            border: 2px solid #007bff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #cce7ff;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #004085;">🚌</h3>
            <h4 style="margin: 10px 0; color: #004085;">대중교통 이용</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #004085;">
                참여: {transport}회
            </p>
        </div>
        """.format(transport=st.session_state.carbon_footprint_data['public_transport']), unsafe_allow_html=True)
        
        if st.button("대중교통 이용 등록", key="public_transport", use_container_width=True):
            st.session_state.carbon_footprint_data['public_transport'] += 1
            st.session_state.carbon_footprint_data['total_participations'] += 1
            st.session_state.carbon_footprint_data['carbon_savings']['public_transport'] += 0.3
            st.success("대중교통 이용 등록 완료! 🚌")
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #fff3cd;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #856404;">🚲</h3>
            <h4 style="margin: 10px 0; color: #856404;">자전거 이용</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #856404;">
                참여: {bicycle}회
            </p>
        </div>
        """.format(bicycle=st.session_state.carbon_footprint_data['bicycle_usage']), unsafe_allow_html=True)
        
        if st.button("자전거 이용 등록", key="bicycle_usage", use_container_width=True):
            st.session_state.carbon_footprint_data['bicycle_usage'] += 1
            st.session_state.carbon_footprint_data['total_participations'] += 1
            st.session_state.carbon_footprint_data['carbon_savings']['bicycle'] += 0.2
            st.success("자전거 이용 등록 완료! 🚲")
            st.rerun()

    st.markdown("---")

    # 전체 현황
    st.subheader("📊 전체 현황")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="총 참여 건수",
            value=f"{st.session_state.carbon_footprint_data['total_participations']}회",
            delta=f"+{np.random.randint(5, 15)}회"
        )
    
    with col2:
        total_carbon_saved = sum(st.session_state.carbon_footprint_data['carbon_savings'].values())
        st.metric(
            label="총 탄소 절약",
            value=f"{total_carbon_saved:.1f}kg",
            delta=f"+{np.random.uniform(1, 3):.1f}kg"
        )
    
    with col3:
        st.metric(
            label="참여율",
            value=f"{st.session_state.carbon_footprint_data['participation_rate']}%",
            delta=f"+{np.random.randint(2, 8)}%"
        )
    
    with col4:
        st.metric(
            label="환경 점수",
            value=f"{int(total_carbon_saved * 10)}점",
            delta=f"+{np.random.randint(10, 30)}점"
        )
    
    with col5:
        st.metric(
            label="총 탄소감축량",
            value=f"{st.session_state.carbon_footprint_data['total_carbon_reduction']:.2f}kg",
            delta="CO₂eq"
        )

    st.markdown("---")

    # 교통수단별 탄소 절약량
    st.subheader("🚗 교통수단별 탄소 절약량")
    
    transport_types = ['계단 이용', '대중교통', '자전거']
    carbon_amounts = [
        st.session_state.carbon_footprint_data['carbon_savings']['stairs'],
        st.session_state.carbon_footprint_data['carbon_savings']['public_transport'],
        st.session_state.carbon_footprint_data['carbon_savings']['bicycle']
    ]
    
    fig_carbon = px.bar(
        x=transport_types,
        y=carbon_amounts,
        title='교통수단별 탄소 절약량',
        labels={'x': '교통수단', 'y': '탄소 절약량 (kg CO2)'},
        color=carbon_amounts,
        color_continuous_scale='Greens'
    )
    fig_carbon.update_layout(
        xaxis_title="교통수단",
        yaxis_title="탄소 절약량 (kg CO2)"
    )
    st.plotly_chart(fig_carbon, use_container_width=True)

    st.markdown("---")

    # 일별 참여 현황
    st.subheader("📅 일별 참여 현황")
    
    daily_df = pd.DataFrame(st.session_state.carbon_footprint_data['daily_data'])
    
    fig_daily = px.line(
        daily_df,
        x='date',
        y='participations',
        title='일별 참여 건수 추이',
        markers=True,
        labels={'participations': '참여 건수', 'date': '날짜'},
        color_discrete_sequence=['#28a745']
    )
    fig_daily.update_layout(
        xaxis_title="날짜",
        yaxis_title="참여 건수",
        xaxis_tickangle=45
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown("---")

    # 탄소감축량 지표 산식
    st.subheader("📊 탄소감축량 지표 산식")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **👣 기본 산식 구조**
        ```
        총 감축량(kgCO₂eq) = C_stairs + C_transit + C_bike
        ```
        **📋 각 항목 산정식**
        
        **🪜 계단 이용에 의한 감축량**
        ```
        C_stairs = N_stairs × P_elevator × EF
        ```
        - **N_stairs**: 계단 이용 횟수
        - **P_elevator**: 엘리베이터 1회 이용 시 소비 전력 (kWh)
        - **EF**: 전력 배출계수 (kgCO₂eq/kWh)
        
        **🚌 대중교통 이용에 의한 감축량**
        ```
        C_transit = N_transit × (E_car - E_transit)
        ```
        - **N_transit**: 대중교통 이용 횟수
        - **E_car**: 자가용 1회 평균 배출량 (kgCO₂eq)
        - **E_transit**: 대중교통 1회 평균 배출량 (kgCO₂eq)
        """)
    
    with col2:
        st.success("""
        **🚲 자전거 이용에 의한 감축량**
        ```
        C_bike = N_bike × E_car
        ```
        - **N_bike**: 자전거 이용 횟수
        - **E_car**: 자가용 1회 배출량 (kgCO₂eq)
        
        **🎯 최종 통합 산식**
        ```
        총 감축량 = N_stairs × P_elevator × EF
                  + N_transit × (E_car - E_transit)
                  + N_bike × E_car
        ```
        **📊 예시값**
        - **P_elevator**: 0.05 kWh/회
        - **EF**: 0.459 kgCO₂eq/kWh
        - **E_car**: 2.2 kgCO₂eq/회
        - **E_transit**: 0.6 kgCO₂eq/회
        """)
    
    st.subheader("🧮 실시간 계산 예시")
    current_data = st.session_state.carbon_footprint_data
    
    st.markdown(f"""
    <div style="
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #d4edda;
        margin-bottom: 10px;
    ">
        <h3 style="margin: 0; color: #155724;">📈 현재 상황</h3>
        <div style="display: flex; justify-content: space-around; margin: 20px 0;">
            <div>
                <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                    <strong>계단 이용:</strong><br>
                    {current_data['stairs_usage']} × {current_data['P_elevator']} × {current_data['EF']}<br>
                    = <strong>{current_data['C_stairs']:.2f}kg CO₂eq</strong>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                    <strong>대중교통:</strong><br>
                    {current_data['public_transport']} × ({current_data['E_car']} - {current_data['E_transit']})<br>
                    = <strong>{current_data['C_transit']:.2f}kg CO₂eq</strong>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; font-size: 16px; color: #155724;">
                    <strong>자전거:</strong><br>
                    {current_data['bicycle_usage']} × {current_data['E_car']}<br>
                    = <strong>{current_data['C_bike']:.2f}kg CO₂eq</strong>
                </p>
            </div>
        </div>
        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #155724;">
            <strong>총 탄소감축량: {current_data['total_carbon_reduction']:.2f}kg CO₂eq</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 환경 효과
    st.subheader("🌱 환경 효과")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="CO2 절약",
            value=f"{total_carbon_saved:.1f}kg",
            delta="월간 절약"
        )
    
    with col2:
        st.metric(
            label="나무 보호",
            value=f"{total_carbon_saved * 0.02:.1f}그루",
            delta="월간 보호"
        )
    
    with col3:
        st.metric(
            label="환경등가",
            value=f"{total_carbon_saved * 0.1:.1f}L",
            delta="휘발유 절약"
        )

    st.markdown("---")

    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            total_participations = np.random.randint(200, 350)
            stairs_usage = np.random.randint(80, 120)
            public_transport = np.random.randint(60, 100)
            bicycle_usage = np.random.randint(40, 80)
            
            # 탄소감축량 계산을 위한 변수들
            P_elevator = 0.05  # 엘리베이터 1회 이용 시 소비 전력 (kWh)
            EF = 0.459  # 전력 배출계수 (kgCO₂eq/kWh)
            E_car = 2.2  # 자가용 1회 평균 배출량 (kgCO₂eq)
            E_transit = 0.6  # 대중교통 1회 평균 배출량 (kgCO₂eq)
            
            # 각 항목별 탄소감축량 계산
            C_stairs = stairs_usage * P_elevator * EF  # 계단 이용에 의한 감축량
            C_transit = public_transport * (E_car - E_transit)  # 대중교통 이용에 의한 감축량
            C_bike = bicycle_usage * E_car  # 자전거 이용에 의한 감축량
            
            # 총 탄소감축량
            total_carbon_reduction = C_stairs + C_transit + C_bike
            
            carbon_savings = {
                'stairs': C_stairs,
                'public_transport': C_transit,
                'bicycle': C_bike
            }
            
            daily_data = []
            for i in range(30):
                day = (datetime.now() - timedelta(days=29-i)).strftime("%m/%d")
                weekday = (datetime.now() - timedelta(days=29-i)).weekday()
                
                if weekday < 5:
                    daily_participations = np.random.randint(8, 15)
                    daily_carbon_saved = daily_participations * np.random.uniform(0.1, 0.3)
                else:
                    daily_participations = np.random.randint(3, 8)
                    daily_carbon_saved = daily_participations * np.random.uniform(0.1, 0.2)
                
                daily_data.append({
                    'date': day,
                    'participations': daily_participations,
                    'carbon_saved': daily_carbon_saved,
                    'is_weekday': weekday < 5
                })
            
            st.session_state.carbon_footprint_data = {
                "total_participations": total_participations,
                "stairs_usage": stairs_usage,
                "public_transport": public_transport,
                "bicycle_usage": bicycle_usage,
                "carbon_savings": carbon_savings,
                "daily_data": daily_data,
                "participation_rate": np.random.randint(70, 85),
                # 탄소감축량 관련
                "P_elevator": P_elevator,
                "EF": EF,
                "E_car": E_car,
                "E_transit": E_transit,
                "C_stairs": C_stairs,
                "C_transit": C_transit,
                "C_bike": C_bike,
                "total_carbon_reduction": total_carbon_reduction
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 탄소 리포트", width='stretch'):
            st.info("탄소 발자국 리포트를 생성했습니다!")

# 사무실 미니 플리마켓 페이지
elif menu == "사무실 미니 플리마켓":
    st.title("🛍️ 사무실 미니 플리마켓")
    st.write("직원 간 중고 물품·책 교환·판매행사를 통해 자원 재활용과 사회적 가치를 창출합니다.")

    # 미니 플리마켓 정보
    flea_market_info = {
        "name": "사무실 미니 플리마켓",
        "description": "직원 간 중고 물품·책 교환·판매행사 개최",
        "schedule": "매월 둘째 주 금요일 (14:00~17:00)",
        "goal": "재활용 물품 개수 증가, 모금액을 통한 기부 연결"
    }

    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'flea_market_data' not in st.session_state:
        # 샘플 물품 데이터 (사진 포함)
        sample_items = [
            {
                "id": 1,
                "name": "MacBook Pro 13인치",
                "category": "전자제품",
                "price": 800000,
                "seller": "김개발",
                "description": "2020년 모델, 상태 양호",
                "image": "💻",
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 2,
                "name": "해리포터 시리즈 전집",
                "category": "도서",
                "price": 50000,
                "seller": "이책사",
                "description": "1-7권 완전판, 새책 수준",
                "image": "📚",
                "image_url": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 3,
                "name": "나이키 운동화",
                "category": "의류/신발",
                "price": 80000,
                "seller": "박운동",
                "description": "사이즈 270, 몇 번만 착용",
                "image": "👟",
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 4,
                "name": "무지 후드티",
                "category": "의류/신발",
                "price": 15000,
                "seller": "최패션",
                "description": "L사이즈, 깨끗한 상태",
                "image": "👕",
                "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 5,
                "name": "아이폰 12 케이스",
                "category": "전자제품",
                "price": 10000,
                "seller": "정폰케이스",
                "description": "투명 케이스, 스크래치 없음",
                "image": "📱",
                "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 6,
                "name": "커피머신",
                "category": "생활용품",
                "price": 120000,
                "seller": "한커피",
                "description": "네스프레소 캡슐 머신",
                "image": "☕",
                "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 7,
                "name": "헤드폰",
                "category": "전자제품",
                "price": 60000,
                "seller": "음악사랑",
                "description": "소니 무선 헤드폰",
                "image": "🎧",
                "image_url": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 8,
                "name": "가방",
                "category": "의류/신발",
                "price": 40000,
                "seller": "백백백",
                "description": "브랜드 백팩, 내구성 좋음",
                "image": "🎒",
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 9,
                "name": "시계",
                "category": "액세서리",
                "price": 200000,
                "seller": "타임키퍼",
                "description": "스위스 시계, 정품",
                "image": "⌚",
                "image_url": "https://images.unsplash.com/photo-1594534475808-b18fc33b045e?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 10,
                "name": "자전거",
                "category": "운동용품",
                "price": 300000,
                "seller": "바이크러버",
                "description": "로드바이크, 잘 관리됨",
                "image": "🚲",
                "image_url": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 11,
                "name": "캠핑용품 세트",
                "category": "생활용품",
                "price": 150000,
                "seller": "캠핑러",
                "description": "텐트, 매트, 랜턴 포함",
                "image": "⛺",
                "image_url": "https://images.unsplash.com/photo-1487730116645-74489c95b41b?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            },
            {
                "id": 12,
                "name": "게임기",
                "category": "전자제품",
                "price": 400000,
                "seller": "게이머",
                "description": "플레이스테이션 5, 게임 3개 포함",
                "image": "🎮",
                "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=300&h=200&fit=crop",
                "status": "판매중",
                "donation_amount": 0
            }
        ]
        
        # 통계 데이터
        total_items = len(sample_items)
        total_value = sum(item['price'] for item in sample_items)
        sold_items = np.random.randint(3, 8)
        total_donations = np.random.randint(50000, 150000)
        
        st.session_state.flea_market_data = {
            "items": sample_items,
            "total_items": total_items,
            "total_value": total_value,
            "sold_items": sold_items,
            "total_donations": total_donations,
            "participants": np.random.randint(25, 45),
            "recycling_rate": np.random.randint(85, 95)
        }

    st.markdown("---")

    # 미니 플리마켓 정보 카드
    st.subheader("📋 미니 플리마켓 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 일정**: {flea_market_info['schedule']}
        
        **🎯 목표**: {flea_market_info['goal']}
        
        **📝 설명**: {flea_market_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **♻️ 환경효과**: 중고 물품 재활용으로 자원 절약
        
        **🤝 사회효과**: 직원 간 소통과 나눔 문화 조성
        
        **💰 경제효과**: 모금액을 통한 사회적 기여
        """)

    st.markdown("---")

    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="등록된 물품",
            value=f"{st.session_state.flea_market_data['total_items']}개",
            delta=f"+{np.random.randint(2, 8)}개"
        )
    
    with col2:
        st.metric(
            label="총 물품 가치",
            value=f"{st.session_state.flea_market_data['total_value']:,}원",
            delta=f"+{np.random.randint(100000, 300000):,}원"
        )
    
    with col3:
        st.metric(
            label="판매 완료",
            value=f"{st.session_state.flea_market_data['sold_items']}개",
            delta=f"+{np.random.randint(1, 4)}개"
        )
    
    with col4:
        st.metric(
            label="모금액",
            value=f"{st.session_state.flea_market_data['total_donations']:,}원",
            delta=f"+{np.random.randint(10000, 30000):,}원"
        )

    st.markdown("---")

    # 물품 등록 섹션
    st.subheader("🛒 새 물품 등록")
    
    with st.form("item_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            item_name = st.text_input("물품명", placeholder="예: MacBook Pro")
            category = st.selectbox("카테고리", ["전자제품", "도서", "의류/신발", "생활용품", "액세서리", "운동용품", "기타"])
            price = st.number_input("가격 (원)", min_value=0, value=0, step=1000)
        
        with col2:
            seller_name = st.text_input("판매자명", placeholder="예: 홍길동")
            description = st.text_area("물품 설명", placeholder="물품 상태, 특징 등을 입력하세요")
            donation_rate = st.slider("기부 비율 (%)", 0, 100, 10)
        
        submitted = st.form_submit_button("물품 등록")
        if submitted:
            if item_name and seller_name and price > 0:
                new_item = {
                    "id": len(st.session_state.flea_market_data['items']) + 1,
                    "name": item_name,
                    "category": category,
                    "price": price,
                    "seller": seller_name,
                    "description": description,
                    "image": "📦",  # 기본 아이콘
                    "image_url": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=300&h=200&fit=crop",  # 기본 이미지
                    "status": "판매중",
                    "donation_amount": int(price * donation_rate / 100)
                }
                st.session_state.flea_market_data['items'].append(new_item)
                st.session_state.flea_market_data['total_items'] += 1
                st.session_state.flea_market_data['total_value'] += price
                st.success(f"{item_name}이(가) 성공적으로 등록되었습니다! 🛍️")
                st.rerun()
            else:
                st.error("모든 필수 항목을 입력해주세요!")

    st.markdown("---")

    # 물품 목록
    st.subheader("🛍️ 등록된 물품 목록")
    
    # 카테고리 필터
    categories = ["전체"] + list(set(item['category'] for item in st.session_state.flea_market_data['items']))
    selected_category = st.selectbox("카테고리 필터", categories)
    
    # 필터링된 물품 목록
    filtered_items = st.session_state.flea_market_data['items']
    if selected_category != "전체":
        filtered_items = [item for item in filtered_items if item['category'] == selected_category]
    
    # 물품 카드 표시
    for i in range(0, len(filtered_items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_items):
                item = filtered_items[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div style="
                        border: 2px solid #e0e0e0;
                        border-radius: 10px;
                        padding: 15px;
                        text-align: center;
                        background-color: #f8f9fa;
                        margin-bottom: 10px;
                    ">
                        <img src="{item['image_url']}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px;">
                        <h4 style="margin: 10px 0; color: #333;">{item['name']}</h4>
                        <p style="margin: 5px 0; font-size: 16px; font-weight: bold; color: #28a745;">
                            {item['price']:,}원
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            {item['category']} | 판매자: {item['seller']}
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            {item['description'][:30]}...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 구매 버튼
                    if st.button(f"구매하기", key=f"buy_{item['id']}", use_container_width=True):
                        # 구매 처리
                        st.session_state.flea_market_data['sold_items'] += 1
                        st.session_state.flea_market_data['total_donations'] += item['donation_amount']
                        st.session_state.flea_market_data['items'].remove(item)
                        st.session_state.flea_market_data['total_items'] -= 1
                        st.session_state.flea_market_data['total_value'] -= item['price']
                        st.success(f"{item['name']} 구매 완료! 기부금 {item['donation_amount']:,}원이 추가되었습니다! 🎉")
                        st.rerun()

    st.markdown("---")

    # 카테고리별 통계
    st.subheader("📊 카테고리별 통계")
    
    category_stats = {}
    for item in st.session_state.flea_market_data['items']:
        if item['category'] not in category_stats:
            category_stats[item['category']] = {'count': 0, 'total_value': 0}
        category_stats[item['category']]['count'] += 1
        category_stats[item['category']]['total_value'] += item['price']
    
    if category_stats:
        categories = list(category_stats.keys())
        counts = [category_stats[cat]['count'] for cat in categories]
        values = [category_stats[cat]['total_value'] for cat in categories]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_count = px.bar(
                x=categories,
                y=counts,
                title='카테고리별 물품 수',
                labels={'x': '카테고리', 'y': '물품 수'},
                color=counts,
                color_continuous_scale='Blues'
            )
            fig_count.update_layout(xaxis_title="카테고리", yaxis_title="물품 수")
            st.plotly_chart(fig_count, use_container_width=True)
        
        with col2:
            fig_value = px.bar(
                x=categories,
                y=values,
                title='카테고리별 총 가치',
                labels={'x': '카테고리', 'y': '총 가치 (원)'},
                color=values,
                color_continuous_scale='Greens'
            )
            fig_value.update_layout(xaxis_title="카테고리", yaxis_title="총 가치 (원)")
            st.plotly_chart(fig_value, use_container_width=True)

    st.markdown("---")

    # 기부 현황
    st.subheader("💝 기부 현황")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="총 모금액",
            value=f"{st.session_state.flea_market_data['total_donations']:,}원",
            delta=f"+{np.random.randint(10000, 30000):,}원"
        )
    
    with col2:
        st.metric(
            label="참여자 수",
            value=f"{st.session_state.flea_market_data['participants']}명",
            delta=f"+{np.random.randint(2, 8)}명"
        )
    
    with col3:
        st.metric(
            label="재활용률",
            value=f"{st.session_state.flea_market_data['recycling_rate']}%",
            delta=f"+{np.random.randint(2, 5)}%"
        )

    st.markdown("---")

    # 기부 연결 정보
    st.subheader("🤝 기부 연결 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🎯 기부 대상**
        - 지역 아동센터
        - 환경보호 단체
        - 사회적 기업 지원
        - 재해 구호 기금
        """)
    
    with col2:
        st.success("""
        **📈 기부 효과**
        - 사회적 가치 창출
        - ESG 경영 실현
        - 직원 참여도 향상
        - 브랜드 이미지 개선
        """)

    st.markdown("---")

    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            sample_items = [
                {
                    "id": 1,
                    "name": "MacBook Pro 13인치",
                    "category": "전자제품",
                    "price": 800000,
                    "seller": "김개발",
                    "description": "2020년 모델, 상태 양호",
                    "image": "💻",
                    "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 2,
                    "name": "해리포터 시리즈 전집",
                    "category": "도서",
                    "price": 50000,
                    "seller": "이책사",
                    "description": "1-7권 완전판, 새책 수준",
                    "image": "📚",
                    "image_url": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 3,
                    "name": "나이키 운동화",
                    "category": "의류/신발",
                    "price": 80000,
                    "seller": "박운동",
                    "description": "사이즈 270, 몇 번만 착용",
                    "image": "👟",
                    "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 4,
                    "name": "무지 후드티",
                    "category": "의류/신발",
                    "price": 15000,
                    "seller": "최패션",
                    "description": "L사이즈, 깨끗한 상태",
                    "image": "👕",
                    "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 5,
                    "name": "아이폰 12 케이스",
                    "category": "전자제품",
                    "price": 10000,
                    "seller": "정폰케이스",
                    "description": "투명 케이스, 스크래치 없음",
                    "image": "📱",
                    "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 6,
                    "name": "커피머신",
                    "category": "생활용품",
                    "price": 120000,
                    "seller": "한커피",
                    "description": "네스프레소 캡슐 머신",
                    "image": "☕",
                    "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 7,
                    "name": "헤드폰",
                    "category": "전자제품",
                    "price": 60000,
                    "seller": "음악사랑",
                    "description": "소니 무선 헤드폰",
                    "image": "🎧",
                    "image_url": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 8,
                    "name": "가방",
                    "category": "의류/신발",
                    "price": 40000,
                    "seller": "백백백",
                    "description": "브랜드 백팩, 내구성 좋음",
                    "image": "🎒",
                    "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 9,
                    "name": "시계",
                    "category": "액세서리",
                    "price": 200000,
                    "seller": "타임키퍼",
                    "description": "스위스 시계, 정품",
                    "image": "⌚",
                    "image_url": "https://images.unsplash.com/photo-1594534475808-b18fc33b045e?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 10,
                    "name": "자전거",
                    "category": "운동용품",
                    "price": 300000,
                    "seller": "바이크러버",
                    "description": "로드바이크, 잘 관리됨",
                    "image": "🚲",
                    "image_url": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 11,
                    "name": "캠핑용품 세트",
                    "category": "생활용품",
                    "price": 150000,
                    "seller": "캠핑러",
                    "description": "텐트, 매트, 랜턴 포함",
                    "image": "⛺",
                    "image_url": "https://images.unsplash.com/photo-1487730116645-74489c95b41b?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                },
                {
                    "id": 12,
                    "name": "게임기",
                    "category": "전자제품",
                    "price": 400000,
                    "seller": "게이머",
                    "description": "플레이스테이션 5, 게임 3개 포함",
                    "image": "🎮",
                    "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=300&h=200&fit=crop",
                    "status": "판매중",
                    "donation_amount": 0
                }
            ]
            
            total_items = len(sample_items)
            total_value = sum(item['price'] for item in sample_items)
            sold_items = np.random.randint(3, 8)
            total_donations = np.random.randint(50000, 150000)
            
            st.session_state.flea_market_data = {
                "items": sample_items,
                "total_items": total_items,
                "total_value": total_value,
                "sold_items": sold_items,
                "total_donations": total_donations,
                "participants": np.random.randint(25, 45),
                "recycling_rate": np.random.randint(85, 95)
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 플리마켓 리포트", width='stretch'):
            st.info("플리마켓 리포트를 생성했습니다!")

# 디지털 다이어트 캠페인 페이지
elif menu == "디지털 다이어트 캠페인":
    st.title("💻 디지털 다이어트 캠페인")
    st.write("이메일, 불필요한 파일·첨부 삭제로 서버 전력 감축을 유도하여 디지털 환경을 개선합니다.")
    
    # 디지털 다이어트 캠페인 정보
    digital_diet_info = {
        "name": "디지털 다이어트 캠페인",
        "description": "이메일, 불필요한 파일·첨부 삭제로 서버 전력 감축 유도",
        "schedule": "월간 정리, 분기별 대청소",
        "goal": "사내 서버 저장용량 절감률, 발신 이메일 감소율 향상"
    }
    
    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'digital_diet_data' not in st.session_state:
        # 부서별 디지털 다이어트 데이터
        departments = {
            "솔루션사업부": {
                "name": "솔루션사업부",
                "icon": "💻",
                "color": "#007bff",
                "storage_saved": 0,
                "emails_reduced": 0,
                "files_deleted": 0,
                "power_saved": 0
            },
            "클라우드사업부": {
                "name": "클라우드사업부",
                "icon": "☁️",
                "color": "#28a745",
                "storage_saved": 0,
                "emails_reduced": 0,
                "files_deleted": 0,
                "power_saved": 0
            },
            "전마실": {
                "name": "전마실",
                "icon": "🏢",
                "color": "#ffc107",
                "storage_saved": 0,
                "emails_reduced": 0,
                "files_deleted": 0,
                "power_saved": 0
            },
            "물류사업": {
                "name": "물류사업",
                "icon": "🚛",
                "color": "#20c997",
                "storage_saved": 0,
                "emails_reduced": 0,
                "files_deleted": 0,
                "power_saved": 0
            },
            "경영지원": {
                "name": "경영지원",
                "icon": "📊",
                "color": "#6f42c1",
                "storage_saved": 0,
                "emails_reduced": 0,
                "files_deleted": 0,
                "power_saved": 0
            },
            "개발센터": {
                "name": "개발센터",
                "icon": "🔧",
                "color": "#fd7e14",
                "storage_saved": 0,
                "emails_reduced": 0,
                "files_deleted": 0,
                "power_saved": 0
            }
        }
        
        # 샘플 데이터 생성
        sample_departments = {
            "솔루션사업부": {
                "name": "솔루션사업부",
                "icon": "💻",
                "color": "#007bff",
                "storage_saved": np.random.randint(15, 25),
                "emails_reduced": np.random.randint(20, 35),
                "files_deleted": np.random.randint(500, 800),
                "power_saved": np.random.randint(8, 15)
            },
            "클라우드사업부": {
                "name": "클라우드사업부",
                "icon": "☁️",
                "color": "#28a745",
                "storage_saved": np.random.randint(12, 20),
                "emails_reduced": np.random.randint(15, 25),
                "files_deleted": np.random.randint(300, 500),
                "power_saved": np.random.randint(6, 12)
            },
            "전마실": {
                "name": "전마실",
                "icon": "🏢",
                "color": "#ffc107",
                "storage_saved": np.random.randint(10, 18),
                "emails_reduced": np.random.randint(18, 30),
                "files_deleted": np.random.randint(400, 600),
                "power_saved": np.random.randint(5, 10)
            },
            "물류사업": {
                "name": "물류사업",
                "icon": "🚛",
                "color": "#20c997",
                "storage_saved": np.random.randint(18, 28),
                "emails_reduced": np.random.randint(25, 40),
                "files_deleted": np.random.randint(600, 900),
                "power_saved": np.random.randint(10, 18)
            },
            "경영지원": {
                "name": "경영지원",
                "icon": "📊",
                "color": "#6f42c1",
                "storage_saved": np.random.randint(20, 30),
                "emails_reduced": np.random.randint(30, 45),
                "files_deleted": np.random.randint(700, 1000),
                "power_saved": np.random.randint(12, 20)
            },
            "개발센터": {
                "name": "개발센터",
                "icon": "🔧",
                "color": "#fd7e14",
                "storage_saved": np.random.randint(22, 32),
                "emails_reduced": np.random.randint(35, 50),
                "files_deleted": np.random.randint(800, 1200),
                "power_saved": np.random.randint(15, 25)
            }
        }
        
        # 전체 통계 계산
        total_storage_saved = sum(dept['storage_saved'] for dept in sample_departments.values())
        total_emails_reduced = sum(dept['emails_reduced'] for dept in sample_departments.values())
        total_files_deleted = sum(dept['files_deleted'] for dept in sample_departments.values())
        total_power_saved = sum(dept['power_saved'] for dept in sample_departments.values())
        avg_storage_saved = round(total_storage_saved / len(sample_departments), 1)
        avg_emails_reduced = round(total_emails_reduced / len(sample_departments), 1)
        
        st.session_state.digital_diet_data = {
            "departments": sample_departments,
            "total_storage_saved": total_storage_saved,
            "total_emails_reduced": total_emails_reduced,
            "total_files_deleted": total_files_deleted,
            "total_power_saved": total_power_saved,
            "avg_storage_saved": avg_storage_saved,
            "avg_emails_reduced": avg_emails_reduced,
            "participation_rate": np.random.randint(80, 95)
        }
    
    st.markdown("---")
    
    # 디지털 다이어트 캠페인 정보 카드
    st.subheader("📋 디지털 다이어트 캠페인 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 일정**: {digital_diet_info['schedule']}
        
        **🎯 목표**: {digital_diet_info['goal']}
        
        **📝 설명**: {digital_diet_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **💾 저장공간**: 서버 용량 절약으로 비용 절감
        
        **⚡ 전력절약**: 서버 부하 감소로 전력 절약
        
        **🌱 환경효과**: 디지털 탄소 발자국 감소
        """)
    
    st.markdown("---")
    
    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 저장용량 절감",
            value=f"{st.session_state.digital_diet_data['total_storage_saved']}GB",
            delta=f"+{np.random.randint(3, 8)}GB"
        )
    
    with col2:
        st.metric(
            label="총 이메일 감소",
            value=f"{st.session_state.digital_diet_data['total_emails_reduced']}%",
            delta=f"+{np.random.randint(5, 12)}%"
        )
    
    with col3:
        st.metric(
            label="총 파일 삭제",
            value=f"{st.session_state.digital_diet_data['total_files_deleted']}개",
            delta=f"+{np.random.randint(50, 150)}개"
        )
    
    with col4:
        st.metric(
            label="총 전력 절약",
            value=f"{st.session_state.digital_diet_data['total_power_saved']}%",
            delta=f"+{np.random.randint(2, 6)}%"
        )
    
    st.markdown("---")
    
    # 부서별 디지털 다이어트 현황
    st.subheader("💻 부서별 디지털 다이어트 현황")
    
    # 부서별 카드 레이아웃 (2열)
    dept_names = list(st.session_state.digital_diet_data['departments'].keys())
    
    for i in range(0, len(dept_names), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(dept_names):
                dept_key = dept_names[i + j]
                dept_info = st.session_state.digital_diet_data['departments'][dept_key]
                
                with cols[j]:
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {dept_info['color']};
                        border-radius: 10px;
                        padding: 20px;
                        text-align: center;
                        background-color: #f8f9fa;
                        margin-bottom: 10px;
                    ">
                        <h3 style="margin: 0; color: {dept_info['color']};">{dept_info['icon']}</h3>
                        <h4 style="margin: 10px 0; color: #333;">{dept_info['name']}</h4>
                        <p style="margin: 5px 0; font-size: 14px; font-weight: bold; color: {dept_info['color']};">
                            저장용량절감: {dept_info['storage_saved']}GB
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #007bff;">
                            이메일감소: {dept_info['emails_reduced']}%
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #28a745;">
                            파일삭제: {dept_info['files_deleted']}개
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            전력절약: {dept_info['power_saved']}%
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 부서별 저장용량 절감률 차트
    st.subheader("💾 부서별 저장용량 절감률")
    
    dept_names = list(st.session_state.digital_diet_data['departments'].keys())
    storage_savings = [dept['storage_saved'] for dept in st.session_state.digital_diet_data['departments'].values()]
    colors = [dept['color'] for dept in st.session_state.digital_diet_data['departments'].values()]
    
    fig_storage = px.bar(
        x=dept_names,
        y=storage_savings,
        title='부서별 저장용량 절감률',
        labels={'x': '부서', 'y': '저장용량 절감 (GB)'},
        color=dept_names,
        color_discrete_sequence=colors
    )
    fig_storage.update_layout(
        xaxis_title="부서",
        yaxis_title="저장용량 절감 (GB)"
    )
    st.plotly_chart(fig_storage, use_container_width=True)
    
    st.markdown("---")
    
    # 부서별 이메일 감소율과 파일 삭제 수
    st.subheader("📧 부서별 이메일 감소율과 파일 삭제 수")
    
    col1, col2 = st.columns(2)
    
    with col1:
        emails_reduced = [dept['emails_reduced'] for dept in st.session_state.digital_diet_data['departments'].values()]
        
        fig_emails = px.bar(
            x=dept_names,
            y=emails_reduced,
            title='부서별 이메일 감소율',
            labels={'x': '부서', 'y': '이메일 감소율 (%)'},
            color=dept_names,
            color_discrete_sequence=colors
        )
        fig_emails.update_layout(xaxis_title="부서", yaxis_title="이메일 감소율 (%)")
        st.plotly_chart(fig_emails, use_container_width=True)
    
    with col2:
        files_deleted = [dept['files_deleted'] for dept in st.session_state.digital_diet_data['departments'].values()]
        
        fig_files = px.bar(
            x=dept_names,
            y=files_deleted,
            title='부서별 파일 삭제 수',
            labels={'x': '부서', 'y': '파일 삭제 수'},
            color=dept_names,
            color_discrete_sequence=colors
        )
        fig_files.update_layout(xaxis_title="부서", yaxis_title="파일 삭제 수")
        st.plotly_chart(fig_files, use_container_width=True)
    
    st.markdown("---")
    
    # 디지털 다이어트 가이드
    st.subheader("📋 디지털 다이어트 가이드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📧 이메일 정리**
        - 불필요한 이메일 삭제
        - 첨부파일 정리
        - 스팸 메일 차단
        - 자동 정리 규칙 설정
        
        **💾 파일 정리**
        - 중복 파일 삭제
        - 임시 파일 정리
        - 오래된 파일 아카이브
        - 클라우드 저장소 정리
        """)
    
    with col2:
        st.success("""
        **🗂️ 폴더 정리**
        - 체계적인 폴더 구조
        - 불필요한 폴더 삭제
        - 파일명 규칙화
        - 정기적인 백업
        
        **⚡ 시스템 최적화**
        - 불필요한 프로그램 제거
        - 시작 프로그램 정리
        - 디스크 정리 실행
        - 시스템 업데이트
        """)
    
    st.markdown("---")
    
    # 디지털 다이어트 참여 등록
    st.subheader("📝 디지털 다이어트 참여 등록")
    
    with st.form("digital_diet_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            participant_name = st.text_input("참여자명", placeholder="예: 홍길동")
            department = st.selectbox("소속 부서", ["솔루션사업부", "클라우드사업부", "전마실", "물류사업", "경영지원", "개발센터"])
            storage_cleaned = st.number_input("정리한 저장용량 (GB)", min_value=0, max_value=100, value=5)
        
        with col2:
            emails_deleted = st.number_input("삭제한 이메일 수", min_value=0, max_value=1000, value=50)
            files_deleted = st.number_input("삭제한 파일 수", min_value=0, max_value=500, value=20)
            cleanup_date = st.date_input("정리 날짜", value=datetime.now().date())
        
        cleanup_description = st.text_area("정리 내용", placeholder="어떤 파일들을 정리했는지 구체적으로 작성해주세요.", height=100)
        
        submitted = st.form_submit_button("디지털 다이어트 등록")
        if submitted:
            if participant_name and cleanup_description:
                # 전력 절약 계산 (저장용량 1GB당 0.5%, 이메일 10개당 0.1%, 파일 10개당 0.1%)
                power_saved = round((storage_cleaned * 0.5) + (emails_deleted * 0.01) + (files_deleted * 0.01), 1)
                
                st.success(f"{participant_name}님의 디지털 다이어트가 성공적으로 등록되었습니다! 💻")
                st.info(f"저장용량: {storage_cleaned}GB, 이메일: {emails_deleted}개, 파일: {files_deleted}개, 전력절약: {power_saved}%")
            else:
                st.error("모든 필수 항목을 입력해주세요!")
    
    st.markdown("---")
    
    # 환경 효과
    st.subheader("🌱 환경 효과")
    
    col1, col2, col3 = st.columns(3)
    
    total_storage = st.session_state.digital_diet_data['total_storage_saved']
    total_emails = st.session_state.digital_diet_data['total_emails_reduced']
    total_files = st.session_state.digital_diet_data['total_files_deleted']
    
    with col1:
        st.metric(
            label="CO2 절약",
            value=f"{total_storage * 0.3:.1f}kg",
            delta="월간 절약"
        )
    
    with col2:
        st.metric(
            label="전력 절약",
            value=f"{total_storage * 0.5:.1f}kWh",
            delta="월간 절약"
        )
    
    with col3:
        st.metric(
            label="서버 효율성",
            value=f"{np.random.randint(85, 95)}%",
            delta="월간 효율성"
        )
    
    st.markdown("---")
    
    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            sample_departments = {
                "솔루션사업부": {
                    "name": "솔루션사업부",
                    "icon": "💻",
                    "color": "#007bff",
                    "storage_saved": np.random.randint(15, 25),
                    "emails_reduced": np.random.randint(20, 35),
                    "files_deleted": np.random.randint(500, 800),
                    "power_saved": np.random.randint(8, 15)
                },
                "클라우드사업부": {
                    "name": "클라우드사업부",
                    "icon": "☁️",
                    "color": "#28a745",
                    "storage_saved": np.random.randint(12, 20),
                    "emails_reduced": np.random.randint(15, 25),
                    "files_deleted": np.random.randint(300, 500),
                    "power_saved": np.random.randint(6, 12)
                },
                "전마실": {
                    "name": "전마실",
                    "icon": "🏢",
                    "color": "#ffc107",
                    "storage_saved": np.random.randint(10, 18),
                    "emails_reduced": np.random.randint(18, 30),
                    "files_deleted": np.random.randint(400, 600),
                    "power_saved": np.random.randint(5, 10)
                },
                "물류사업": {
                    "name": "물류사업",
                    "icon": "🚛",
                    "color": "#20c997",
                    "storage_saved": np.random.randint(18, 28),
                    "emails_reduced": np.random.randint(25, 40),
                    "files_deleted": np.random.randint(600, 900),
                    "power_saved": np.random.randint(10, 18)
                },
                "경영지원": {
                    "name": "경영지원",
                    "icon": "📊",
                    "color": "#6f42c1",
                    "storage_saved": np.random.randint(20, 30),
                    "emails_reduced": np.random.randint(30, 45),
                    "files_deleted": np.random.randint(700, 1000),
                    "power_saved": np.random.randint(12, 20)
                },
                "개발센터": {
                    "name": "개발센터",
                    "icon": "🔧",
                    "color": "#fd7e14",
                    "storage_saved": np.random.randint(22, 32),
                    "emails_reduced": np.random.randint(35, 50),
                    "files_deleted": np.random.randint(800, 1200),
                    "power_saved": np.random.randint(15, 25)
                }
            }
            
            # 전체 통계 재계산
            total_storage_saved = sum(dept['storage_saved'] for dept in sample_departments.values())
            total_emails_reduced = sum(dept['emails_reduced'] for dept in sample_departments.values())
            total_files_deleted = sum(dept['files_deleted'] for dept in sample_departments.values())
            total_power_saved = sum(dept['power_saved'] for dept in sample_departments.values())
            avg_storage_saved = round(total_storage_saved / len(sample_departments), 1)
            avg_emails_reduced = round(total_emails_reduced / len(sample_departments), 1)
            
            st.session_state.digital_diet_data = {
                "departments": sample_departments,
                "total_storage_saved": total_storage_saved,
                "total_emails_reduced": total_emails_reduced,
                "total_files_deleted": total_files_deleted,
                "total_power_saved": total_power_saved,
                "avg_storage_saved": avg_storage_saved,
                "avg_emails_reduced": avg_emails_reduced,
                "participation_rate": np.random.randint(80, 95)
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 다이어트 리포트", width='stretch'):
            st.info("디지털 다이어트 리포트를 생성했습니다!")

# ESG 교육 및 퀴즈데이 페이지
elif menu == "ESG 교육 및 퀴즈데이":
    st.title("🎓 ESG 교육 및 퀴즈데이")
    st.write("직원대상 ESG 온라인 교육·퀴즈를 진행하고, 점수에 따라 리워드를 제공하여 ESG 인식도를 향상시킵니다.")
    
    # ESG 교육 및 퀴즈데이 정보
    esg_education_info = {
        "name": "ESG 교육 및 퀴즈데이",
        "description": "직원대상 ESG 온라인 교육·퀴즈 진행, 점수에 따라 리워드 제공",
        "schedule": "월 2회 교육, 분기별 퀴즈 대회",
        "goal": "참여율, ESG 인식도 조사 점수 변화 향상"
    }
    
    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'esg_education_data' not in st.session_state:
        # 교육 과정별 데이터
        education_courses = {
            "ESG기초": {
                "name": "ESG 기초 교육",
                "icon": "📚",
                "color": "#007bff",
                "participants": 0,
                "completion_rate": 0,
                "avg_score": 0,
                "duration": "2시간",
                "difficulty": "초급"
            },
            "환경경영": {
                "name": "환경 경영 교육",
                "icon": "🌱",
                "color": "#28a745",
                "participants": 0,
                "completion_rate": 0,
                "avg_score": 0,
                "duration": "3시간",
                "difficulty": "중급"
            },
            "사회책임": {
                "name": "사회적 책임 교육",
                "icon": "🤝",
                "color": "#ffc107",
                "participants": 0,
                "completion_rate": 0,
                "avg_score": 0,
                "duration": "2.5시간",
                "difficulty": "중급"
            },
            "지배구조": {
                "name": "지배구조 교육",
                "icon": "⚖️",
                "color": "#6f42c1",
                "participants": 0,
                "completion_rate": 0,
                "avg_score": 0,
                "duration": "2시간",
                "difficulty": "고급"
            },
            "지속가능성": {
                "name": "지속가능성 교육",
                "icon": "♻️",
                "color": "#20c997",
                "participants": 0,
                "completion_rate": 0,
                "avg_score": 0,
                "duration": "3.5시간",
                "difficulty": "고급"
            }
        }
        
        # 샘플 데이터 생성
        sample_courses = {
            "ESG기초": {
                "name": "ESG 기초 교육",
                "icon": "📚",
                "color": "#007bff",
                "participants": np.random.randint(80, 120),
                "completion_rate": np.random.randint(85, 95),
                "avg_score": np.random.randint(75, 85),
                "duration": "2시간",
                "difficulty": "초급"
            },
            "환경경영": {
                "name": "환경 경영 교육",
                "icon": "🌱",
                "color": "#28a745",
                "participants": np.random.randint(60, 90),
                "completion_rate": np.random.randint(80, 90),
                "avg_score": np.random.randint(70, 80),
                "duration": "3시간",
                "difficulty": "중급"
            },
            "사회책임": {
                "name": "사회적 책임 교육",
                "icon": "🤝",
                "color": "#ffc107",
                "participants": np.random.randint(70, 100),
                "completion_rate": np.random.randint(82, 92),
                "avg_score": np.random.randint(72, 82),
                "duration": "2.5시간",
                "difficulty": "중급"
            },
            "지배구조": {
                "name": "지배구조 교육",
                "icon": "⚖️",
                "color": "#6f42c1",
                "participants": np.random.randint(50, 80),
                "completion_rate": np.random.randint(75, 85),
                "avg_score": np.random.randint(65, 75),
                "duration": "2시간",
                "difficulty": "고급"
            },
            "지속가능성": {
                "name": "지속가능성 교육",
                "icon": "♻️",
                "color": "#20c997",
                "participants": np.random.randint(45, 75),
                "completion_rate": np.random.randint(70, 80),
                "avg_score": np.random.randint(60, 70),
                "duration": "3.5시간",
                "difficulty": "고급"
            }
        }
        
        # 전체 통계 계산
        total_participants = sum(course['participants'] for course in sample_courses.values())
        avg_completion_rate = round(sum(course['completion_rate'] for course in sample_courses.values()) / len(sample_courses), 1)
        avg_score = round(sum(course['avg_score'] for course in sample_courses.values()) / len(sample_courses), 1)
        total_completed = sum(int(course['participants'] * course['completion_rate'] / 100) for course in sample_courses.values())
        
        st.session_state.esg_education_data = {
            "courses": sample_courses,
            "total_participants": total_participants,
            "avg_completion_rate": avg_completion_rate,
            "avg_score": avg_score,
            "total_completed": total_completed,
            "participation_rate": np.random.randint(75, 90),
            "awareness_score": np.random.randint(70, 85)
        }
    
    st.markdown("---")
    
    # ESG 교육 및 퀴즈데이 정보 카드
    st.subheader("📋 ESG 교육 및 퀴즈데이 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 일정**: {esg_education_info['schedule']}
        
        **🎯 목표**: {esg_education_info['goal']}
        
        **📝 설명**: {esg_education_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **🎓 교육효과**: ESG 전문 지식 습득
        
        **🏆 경쟁효과**: 퀴즈 대회를 통한 학습 동기 부여
        
        **🎁 리워드효과**: 점수에 따른 인센티브 제공
        """)
    
    st.markdown("---")
    
    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 참여자",
            value=f"{st.session_state.esg_education_data['total_participants']}명",
            delta=f"+{np.random.randint(5, 15)}명"
        )
    
    with col2:
        st.metric(
            label="평균 완주율",
            value=f"{st.session_state.esg_education_data['avg_completion_rate']}%",
            delta=f"+{np.random.randint(2, 5)}%"
        )
    
    with col3:
        st.metric(
            label="평균 점수",
            value=f"{st.session_state.esg_education_data['avg_score']}점",
            delta=f"+{np.random.randint(3, 8)}점"
        )
    
    with col4:
        st.metric(
            label="ESG 인식도",
            value=f"{st.session_state.esg_education_data['awareness_score']}점",
            delta=f"+{np.random.randint(5, 10)}점"
        )
    
    st.markdown("---")
    
    # 교육 과정별 현황
    st.subheader("🎓 교육 과정별 현황")
    
    # 교육 과정별 카드 레이아웃 (2열)
    course_names = list(st.session_state.esg_education_data['courses'].keys())
    
    for i in range(0, len(course_names), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(course_names):
                course_key = course_names[i + j]
                course_info = st.session_state.esg_education_data['courses'][course_key]
                
                with cols[j]:
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {course_info['color']};
                        border-radius: 10px;
                        padding: 20px;
                        text-align: center;
                        background-color: #f8f9fa;
                        margin-bottom: 10px;
                    ">
                        <h3 style="margin: 0; color: {course_info['color']};">{course_info['icon']}</h3>
                        <h4 style="margin: 10px 0; color: #333;">{course_info['name']}</h4>
                        <p style="margin: 5px 0; font-size: 14px; font-weight: bold; color: {course_info['color']};">
                            참여자: {course_info['participants']}명
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #007bff;">
                            완주율: {course_info['completion_rate']}%
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #28a745;">
                            평균점수: {course_info['avg_score']}점
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            소요시간: {course_info['duration']}
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            난이도: {course_info['difficulty']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 교육 과정별 참여자 수 차트
    st.subheader("👥 교육 과정별 참여자 수")
    
    course_names = list(st.session_state.esg_education_data['courses'].keys())
    participants_counts = [course['participants'] for course in st.session_state.esg_education_data['courses'].values()]
    colors = [course['color'] for course in st.session_state.esg_education_data['courses'].values()]
    
    fig_participants = px.bar(
        x=course_names,
        y=participants_counts,
        title='교육 과정별 참여자 수',
        labels={'x': '교육 과정', 'y': '참여자 수'},
        color=course_names,
        color_discrete_sequence=colors
    )
    fig_participants.update_layout(
        xaxis_title="교육 과정",
        yaxis_title="참여자 수"
    )
    st.plotly_chart(fig_participants, use_container_width=True)
    
    st.markdown("---")
    
    # 교육 과정별 완주율과 평균 점수
    st.subheader("📈 교육 과정별 완주율과 평균 점수")
    
    col1, col2 = st.columns(2)
    
    with col1:
        completion_rates = [course['completion_rate'] for course in st.session_state.esg_education_data['courses'].values()]
        
        fig_completion = px.bar(
            x=course_names,
            y=completion_rates,
            title='교육 과정별 완주율',
            labels={'x': '교육 과정', 'y': '완주율 (%)'},
            color=course_names,
            color_discrete_sequence=colors
        )
        fig_completion.update_layout(xaxis_title="교육 과정", yaxis_title="완주율 (%)")
        st.plotly_chart(fig_completion, use_container_width=True)
    
    with col2:
        avg_scores = [course['avg_score'] for course in st.session_state.esg_education_data['courses'].values()]
        
        fig_scores = px.bar(
            x=course_names,
            y=avg_scores,
            title='교육 과정별 평균 점수',
            labels={'x': '교육 과정', 'y': '평균 점수'},
            color=course_names,
            color_discrete_sequence=colors
        )
        fig_scores.update_layout(xaxis_title="교육 과정", yaxis_title="평균 점수")
        st.plotly_chart(fig_scores, use_container_width=True)
    
    st.markdown("---")
    
    # ESG 퀴즈 대회
    st.subheader("🏆 ESG 퀴즈 대회")
    
    # 간단한 퀴즈 인터페이스
    st.write("**ESG 기초 퀴즈 (5문제)**")
    
    quiz_questions = [
        {
            "question": "ESG에서 E는 무엇을 의미하나요?",
            "options": ["Environment (환경)", "Economy (경제)", "Education (교육)", "Energy (에너지)"],
            "correct": 0
        },
        {
            "question": "탄소 중립이란 무엇인가요?",
            "options": ["탄소를 완전히 제거하는 것", "탄소 배출량과 흡수량을 같게 만드는 것", "탄소를 저장하는 것", "탄소를 재활용하는 것"],
            "correct": 1
        },
        {
            "question": "사회적 책임(S)의 주요 요소는?",
            "options": ["환경 보호", "지배구조 개선", "인권 보호, 공정한 노동", "기술 혁신"],
            "correct": 2
        },
        {
            "question": "지속가능한 발전의 핵심은?",
            "options": ["경제 성장만", "환경 보호만", "경제, 사회, 환경의 균형", "기술 발전만"],
            "correct": 2
        },
        {
            "question": "Scope 1 배출이란?",
            "options": ["간접 배출", "직접 배출", "가치사슬 배출", "외부 배출"],
            "correct": 1
        }
    ]
    
    # 퀴즈 상태 초기화
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {
            'current_question': 0,
            'score': 0,
            'answers': [],
            'completed': False
        }
    
    if not st.session_state.quiz_state['completed']:
        current_q = st.session_state.quiz_state['current_question']
        question = quiz_questions[current_q]
        
        st.write(f"**문제 {current_q + 1}/5:** {question['question']}")
        
        selected_option = st.radio("답을 선택하세요:", question['options'], key=f"q{current_q}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("다음 문제", disabled=current_q >= len(quiz_questions)-1):
                st.session_state.quiz_state['answers'].append(selected_option)
                if question['options'].index(selected_option) == question['correct']:
                    st.session_state.quiz_state['score'] += 1
                st.session_state.quiz_state['current_question'] += 1
                st.rerun()
        
        with col2:
            if st.button("퀴즈 완료", disabled=current_q < len(quiz_questions)-1):
                st.session_state.quiz_state['answers'].append(selected_option)
                if question['options'].index(selected_option) == question['correct']:
                    st.session_state.quiz_state['score'] += 1
                st.session_state.quiz_state['completed'] = True
                st.rerun()
    
    else:
        score = st.session_state.quiz_state['score']
        total = len(quiz_questions)
        percentage = (score / total) * 100
        
        st.success(f"🎉 퀴즈 완료! 점수: {score}/{total} ({percentage:.0f}%)")
        
        if percentage >= 80:
            st.balloons()
            st.info("🏆 우수한 성적입니다! 리워드가 지급됩니다!")
        elif percentage >= 60:
            st.info("👍 좋은 성적입니다! 계속 노력하세요!")
        else:
            st.warning("📚 더 공부가 필요합니다. 교육 과정을 다시 수강해보세요!")
        
        if st.button("퀴즈 다시 시작"):
            st.session_state.quiz_state = {
                'current_question': 0,
                'score': 0,
                'answers': [],
                'completed': False
            }
            st.rerun()
    
    st.markdown("---")
    
    # 리워드 시스템
    st.subheader("🎁 리워드 시스템")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="퀴즈 완주",
            value="기본 리워드",
            delta="100포인트"
        )
    
    with col2:
        st.metric(
            label="80점 이상",
            value="우수 리워드",
            delta="200포인트"
        )
    
    with col3:
        st.metric(
            label="만점 달성",
            value="완벽 리워드",
            delta="500포인트"
        )
    
    st.markdown("---")
    
    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            sample_courses = {
                "ESG기초": {
                    "name": "ESG 기초 교육",
                    "icon": "📚",
                    "color": "#007bff",
                    "participants": np.random.randint(80, 120),
                    "completion_rate": np.random.randint(85, 95),
                    "avg_score": np.random.randint(75, 85),
                    "duration": "2시간",
                    "difficulty": "초급"
                },
                "환경경영": {
                    "name": "환경 경영 교육",
                    "icon": "🌱",
                    "color": "#28a745",
                    "participants": np.random.randint(60, 90),
                    "completion_rate": np.random.randint(80, 90),
                    "avg_score": np.random.randint(70, 80),
                    "duration": "3시간",
                    "difficulty": "중급"
                },
                "사회책임": {
                    "name": "사회적 책임 교육",
                    "icon": "🤝",
                    "color": "#ffc107",
                    "participants": np.random.randint(70, 100),
                    "completion_rate": np.random.randint(82, 92),
                    "avg_score": np.random.randint(72, 82),
                    "duration": "2.5시간",
                    "difficulty": "중급"
                },
                "지배구조": {
                    "name": "지배구조 교육",
                    "icon": "⚖️",
                    "color": "#6f42c1",
                    "participants": np.random.randint(50, 80),
                    "completion_rate": np.random.randint(75, 85),
                    "avg_score": np.random.randint(65, 75),
                    "duration": "2시간",
                    "difficulty": "고급"
                },
                "지속가능성": {
                    "name": "지속가능성 교육",
                    "icon": "♻️",
                    "color": "#20c997",
                    "participants": np.random.randint(45, 75),
                    "completion_rate": np.random.randint(70, 80),
                    "avg_score": np.random.randint(60, 70),
                    "duration": "3.5시간",
                    "difficulty": "고급"
                }
            }
            
            # 전체 통계 재계산
            total_participants = sum(course['participants'] for course in sample_courses.values())
            avg_completion_rate = round(sum(course['completion_rate'] for course in sample_courses.values()) / len(sample_courses), 1)
            avg_score = round(sum(course['avg_score'] for course in sample_courses.values()) / len(sample_courses), 1)
            total_completed = sum(int(course['participants'] * course['completion_rate'] / 100) for course in sample_courses.values())
            
            st.session_state.esg_education_data = {
                "courses": sample_courses,
                "total_participants": total_participants,
                "avg_completion_rate": avg_completion_rate,
                "avg_score": avg_score,
                "total_completed": total_completed,
                "participation_rate": np.random.randint(75, 90),
                "awareness_score": np.random.randint(70, 85)
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 교육 리포트", width='stretch'):
            st.info("ESG 교육 리포트를 생성했습니다!")

# 투명한 ESG 성과 공개 플랫폼 페이지
elif menu == "ESG 성과 공개 플랫폼":
    st.title("📊 투명한 ESG 성과 공개 플랫폼")
    st.write("부서별 ESG 지표(전력 절감, 자원 절약, 봉사 참여 등)를 사내 대시보드로 시각화하여 투명한 성과 공개를 실현합니다.")
    
    # ESG 성과 공개 플랫폼 정보
    esg_platform_info = {
        "name": "투명한 ESG 성과 공개 플랫폼",
        "description": "부서별 ESG 지표를 사내 대시보드로 시각화",
        "schedule": "월간 성과 공개, 분기별 종합 평가",
        "goal": "목표 달성률, 참여 팀 비율 향상"
    }
    
    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'esg_platform_data' not in st.session_state:
        # 부서별 ESG 지표 데이터
        departments = {
            "솔루션사업부": {
                "name": "솔루션사업부",
                "icon": "💻",
                "color": "#007bff",
                "power_saving": 0,
                "resource_saving": 0,
                "volunteer_participation": 0,
                "target_achievement": 0,
                "participation_rate": 0
            },
            "클라우드사업부": {
                "name": "클라우드사업부",
                "icon": "☁️",
                "color": "#28a745",
                "power_saving": 0,
                "resource_saving": 0,
                "volunteer_participation": 0,
                "target_achievement": 0,
                "participation_rate": 0
            },
            "전마실": {
                "name": "전마실",
                "icon": "🏢",
                "color": "#ffc107",
                "power_saving": 0,
                "resource_saving": 0,
                "volunteer_participation": 0,
                "target_achievement": 0,
                "participation_rate": 0
            },
            "물류사업": {
                "name": "물류사업",
                "icon": "🚛",
                "color": "#20c997",
                "power_saving": 0,
                "resource_saving": 0,
                "volunteer_participation": 0,
                "target_achievement": 0,
                "participation_rate": 0
            },
            "경영지원": {
                "name": "경영지원",
                "icon": "📊",
                "color": "#6f42c1",
                "power_saving": 0,
                "resource_saving": 0,
                "volunteer_participation": 0,
                "target_achievement": 0,
                "participation_rate": 0
            },
            "개발센터": {
                "name": "개발센터",
                "icon": "🔧",
                "color": "#fd7e14",
                "power_saving": 0,
                "resource_saving": 0,
                "volunteer_participation": 0,
                "target_achievement": 0,
                "participation_rate": 0
            }
        }
        
        # 샘플 데이터 생성
        sample_departments = {
            "솔루션사업부": {
                "name": "솔루션사업부",
                "icon": "💻",
                "color": "#007bff",
                "power_saving": np.random.randint(15, 25),
                "resource_saving": np.random.randint(20, 30),
                "volunteer_participation": np.random.randint(8, 15),
                "target_achievement": np.random.randint(85, 95),
                "participation_rate": np.random.randint(90, 100)
            },
            "클라우드사업부": {
                "name": "클라우드사업부",
                "icon": "☁️",
                "color": "#28a745",
                "power_saving": np.random.randint(25, 35),
                "resource_saving": np.random.randint(30, 40),
                "volunteer_participation": np.random.randint(12, 20),
                "target_achievement": np.random.randint(90, 100),
                "participation_rate": np.random.randint(95, 100)
            },
            "전마실": {
                "name": "전마실",
                "icon": "🏢",
                "color": "#ffc107",
                "power_saving": np.random.randint(10, 20),
                "resource_saving": np.random.randint(25, 35),
                "volunteer_participation": np.random.randint(6, 12),
                "target_achievement": np.random.randint(80, 90),
                "participation_rate": np.random.randint(85, 95)
            },
            "물류사업": {
                "name": "물류사업",
                "icon": "🚛",
                "color": "#20c997",
                "power_saving": np.random.randint(30, 40),
                "resource_saving": np.random.randint(35, 45),
                "volunteer_participation": np.random.randint(15, 25),
                "target_achievement": np.random.randint(95, 100),
                "participation_rate": np.random.randint(98, 100)
            },
            "경영지원": {
                "name": "경영지원",
                "icon": "📊",
                "color": "#6f42c1",
                "power_saving": np.random.randint(12, 22),
                "resource_saving": np.random.randint(18, 28),
                "volunteer_participation": np.random.randint(10, 18),
                "target_achievement": np.random.randint(82, 92),
                "participation_rate": np.random.randint(88, 98)
            },
            "개발센터": {
                "name": "개발센터",
                "icon": "🔧",
                "color": "#fd7e14",
                "power_saving": np.random.randint(20, 30),
                "resource_saving": np.random.randint(25, 35),
                "volunteer_participation": np.random.randint(12, 20),
                "target_achievement": np.random.randint(88, 98),
                "participation_rate": np.random.randint(92, 100)
            }
        }
        
        # 전체 통계 계산
        total_power_saving = sum(dept['power_saving'] for dept in sample_departments.values())
        total_resource_saving = sum(dept['resource_saving'] for dept in sample_departments.values())
        total_volunteer_participation = sum(dept['volunteer_participation'] for dept in sample_departments.values())
        avg_target_achievement = round(sum(dept['target_achievement'] for dept in sample_departments.values()) / len(sample_departments), 1)
        avg_participation_rate = round(sum(dept['participation_rate'] for dept in sample_departments.values()) / len(sample_departments), 1)
        
        st.session_state.esg_platform_data = {
            "departments": sample_departments,
            "total_power_saving": total_power_saving,
            "total_resource_saving": total_resource_saving,
            "total_volunteer_participation": total_volunteer_participation,
            "avg_target_achievement": avg_target_achievement,
            "avg_participation_rate": avg_participation_rate,
            "participating_teams": len([dept for dept in sample_departments.values() if dept['participation_rate'] >= 80])
        }
    
    st.markdown("---")
    
    # ESG 성과 공개 플랫폼 정보 카드
    st.subheader("📋 ESG 성과 공개 플랫폼 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 일정**: {esg_platform_info['schedule']}
        
        **🎯 목표**: {esg_platform_info['goal']}
        
        **📝 설명**: {esg_platform_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **📊 투명성**: 부서별 성과 공개로 투명성 확보
        
        **🏆 경쟁성**: 부서 간 경쟁을 통한 성과 향상
        
        **📈 지속성**: 지속적인 ESG 경영 실현
        """)
    
    st.markdown("---")
    
    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="평균 목표 달성률",
            value=f"{st.session_state.esg_platform_data['avg_target_achievement']}%",
            delta=f"+{np.random.randint(2, 5)}%"
        )
    
    with col2:
        st.metric(
            label="평균 참여율",
            value=f"{st.session_state.esg_platform_data['avg_participation_rate']}%",
            delta=f"+{np.random.randint(3, 7)}%"
        )
    
    with col3:
        st.metric(
            label="참여 부서",
            value=f"{st.session_state.esg_platform_data['participating_teams']}개",
            delta=f"+{np.random.randint(0, 2)}개"
        )
    
    with col4:
        st.metric(
            label="총 전력 절감",
            value=f"{st.session_state.esg_platform_data['total_power_saving']}%",
            delta=f"+{np.random.randint(3, 8)}%"
        )
    
    st.markdown("---")
    
    # 부서별 ESG 성과 대시보드
    st.subheader("🏢 부서별 ESG 성과 대시보드")
    
    # 부서별 카드 레이아웃 (2열)
    dept_names = list(st.session_state.esg_platform_data['departments'].keys())
    
    for i in range(0, len(dept_names), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(dept_names):
                dept_key = dept_names[i + j]
                dept_info = st.session_state.esg_platform_data['departments'][dept_key]
                
                with cols[j]:
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {dept_info['color']};
                        border-radius: 10px;
                        padding: 20px;
                        text-align: center;
                        background-color: #f8f9fa;
                        margin-bottom: 10px;
                    ">
                        <h3 style="margin: 0; color: {dept_info['color']};">{dept_info['icon']}</h3>
                        <h4 style="margin: 10px 0; color: #333;">{dept_info['name']}</h4>
                        <p style="margin: 5px 0; font-size: 14px; font-weight: bold; color: {dept_info['color']};">
                            목표달성: {dept_info['target_achievement']}%
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #007bff;">
                            전력절감: {dept_info['power_saving']}%
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #28a745;">
                            자원절약: {dept_info['resource_saving']}%
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            봉사참여: {dept_info['volunteer_participation']}명
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            참여율: {dept_info['participation_rate']}%
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 부서별 목표 달성률 차트
    st.subheader("🎯 부서별 목표 달성률")
    
    dept_names = list(st.session_state.esg_platform_data['departments'].keys())
    target_achievements = [dept['target_achievement'] for dept in st.session_state.esg_platform_data['departments'].values()]
    colors = [dept['color'] for dept in st.session_state.esg_platform_data['departments'].values()]
    
    fig_target = px.bar(
        x=dept_names,
        y=target_achievements,
        title='부서별 목표 달성률',
        labels={'x': '부서', 'y': '목표 달성률 (%)'},
        color=dept_names,
        color_discrete_sequence=colors
    )
    fig_target.update_layout(
        xaxis_title="부서",
        yaxis_title="목표 달성률 (%)"
    )
    st.plotly_chart(fig_target, use_container_width=True)
    
    st.markdown("---")
    
    # 부서별 참여율 차트
    st.subheader("👥 부서별 참여율")
    
    participation_rates = [dept['participation_rate'] for dept in st.session_state.esg_platform_data['departments'].values()]
    
    fig_participation = px.bar(
        x=dept_names,
        y=participation_rates,
        title='부서별 참여율',
        labels={'x': '부서', 'y': '참여율 (%)'},
        color=dept_names,
        color_discrete_sequence=colors
    )
    fig_participation.update_layout(
        xaxis_title="부서",
        yaxis_title="참여율 (%)"
    )
    st.plotly_chart(fig_participation, use_container_width=True)
    
    st.markdown("---")
    
    # ESG 지표별 성과
    st.subheader("📈 ESG 지표별 성과")
    
    col1, col2 = st.columns(2)
    
    with col1:
        power_savings = [dept['power_saving'] for dept in st.session_state.esg_platform_data['departments'].values()]
        
        fig_power = px.bar(
            x=dept_names,
            y=power_savings,
            title='부서별 전력 절감률',
            labels={'x': '부서', 'y': '전력 절감률 (%)'},
            color=dept_names,
            color_discrete_sequence=colors
        )
        fig_power.update_layout(xaxis_title="부서", yaxis_title="전력 절감률 (%)")
        st.plotly_chart(fig_power, use_container_width=True)
    
    with col2:
        resource_savings = [dept['resource_saving'] for dept in st.session_state.esg_platform_data['departments'].values()]
        
        fig_resource = px.bar(
            x=dept_names,
            y=resource_savings,
            title='부서별 자원 절약률',
            labels={'x': '부서', 'y': '자원 절약률 (%)'},
            color=dept_names,
            color_discrete_sequence=colors
        )
        fig_resource.update_layout(xaxis_title="부서", yaxis_title="자원 절약률 (%)")
        st.plotly_chart(fig_resource, use_container_width=True)
    
    st.markdown("---")
    
    # 랭킹 시스템
    st.subheader("🏆 부서별 ESG 성과 랭킹")
    
    # 종합 점수 계산 (목표달성률 40% + 참여율 30% + 전력절감 20% + 자원절약 10%)
    rankings = []
    for dept_key, dept_info in st.session_state.esg_platform_data['departments'].items():
        total_score = (
            dept_info['target_achievement'] * 0.4 +
            dept_info['participation_rate'] * 0.3 +
            dept_info['power_saving'] * 0.2 +
            dept_info['resource_saving'] * 0.1
        )
        rankings.append({
            'department': dept_info['name'],
            'icon': dept_info['icon'],
            'color': dept_info['color'],
            'score': round(total_score, 1)
        })
    
    # 점수순으로 정렬
    rankings.sort(key=lambda x: x['score'], reverse=True)
    
    # 랭킹 표시
    for i, rank in enumerate(rankings, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}위"
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"<h3 style='text-align: center; color: {rank['color']};'>{medal}</h3>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<h4 style='text-align: center; color: #333;'>{rank['icon']} {rank['department']}</h4>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<h3 style='text-align: center; color: {rank['color']};'>{rank['score']}점</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            sample_departments = {
                "솔루션사업부": {
                    "name": "솔루션사업부",
                    "icon": "💻",
                    "color": "#007bff",
                    "power_saving": np.random.randint(15, 25),
                    "resource_saving": np.random.randint(20, 30),
                    "volunteer_participation": np.random.randint(8, 15),
                    "target_achievement": np.random.randint(85, 95),
                    "participation_rate": np.random.randint(90, 100)
                },
                "클라우드사업부": {
                    "name": "클라우드사업부",
                    "icon": "☁️",
                    "color": "#28a745",
                    "power_saving": np.random.randint(25, 35),
                    "resource_saving": np.random.randint(30, 40),
                    "volunteer_participation": np.random.randint(12, 20),
                    "target_achievement": np.random.randint(90, 100),
                    "participation_rate": np.random.randint(95, 100)
                },
                "전마실": {
                    "name": "전마실",
                    "icon": "🏢",
                    "color": "#ffc107",
                    "power_saving": np.random.randint(10, 20),
                    "resource_saving": np.random.randint(25, 35),
                    "volunteer_participation": np.random.randint(6, 12),
                    "target_achievement": np.random.randint(80, 90),
                    "participation_rate": np.random.randint(85, 95)
                },
                "물류사업": {
                    "name": "물류사업",
                    "icon": "🚛",
                    "color": "#20c997",
                    "power_saving": np.random.randint(30, 40),
                    "resource_saving": np.random.randint(35, 45),
                    "volunteer_participation": np.random.randint(15, 25),
                    "target_achievement": np.random.randint(95, 100),
                    "participation_rate": np.random.randint(98, 100)
                },
                "경영지원": {
                    "name": "경영지원",
                    "icon": "📊",
                    "color": "#6f42c1",
                    "power_saving": np.random.randint(12, 22),
                    "resource_saving": np.random.randint(18, 28),
                    "volunteer_participation": np.random.randint(10, 18),
                    "target_achievement": np.random.randint(82, 92),
                    "participation_rate": np.random.randint(88, 98)
                },
                "개발센터": {
                    "name": "개발센터",
                    "icon": "🔧",
                    "color": "#fd7e14",
                    "power_saving": np.random.randint(20, 30),
                    "resource_saving": np.random.randint(25, 35),
                    "volunteer_participation": np.random.randint(12, 20),
                    "target_achievement": np.random.randint(88, 98),
                    "participation_rate": np.random.randint(92, 100)
                }
            }
            
            # 전체 통계 재계산
            total_power_saving = sum(dept['power_saving'] for dept in sample_departments.values())
            total_resource_saving = sum(dept['resource_saving'] for dept in sample_departments.values())
            total_volunteer_participation = sum(dept['volunteer_participation'] for dept in sample_departments.values())
            avg_target_achievement = round(sum(dept['target_achievement'] for dept in sample_departments.values()) / len(sample_departments), 1)
            avg_participation_rate = round(sum(dept['participation_rate'] for dept in sample_departments.values()) / len(sample_departments), 1)
            
            st.session_state.esg_platform_data = {
                "departments": sample_departments,
                "total_power_saving": total_power_saving,
                "total_resource_saving": total_resource_saving,
                "total_volunteer_participation": total_volunteer_participation,
                "avg_target_achievement": avg_target_achievement,
                "avg_participation_rate": avg_participation_rate,
                "participating_teams": len([dept for dept in sample_departments.values() if dept['participation_rate'] >= 80])
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 성과 리포트", width='stretch'):
            st.info("ESG 성과 리포트를 생성했습니다!")

# 지역 사회 연계 봉사 프로그램 페이지
elif menu == "지역 사회 연계 봉사":
    st.title("🤝 지역 사회 연계 봉사 프로그램")
    st.write("환경정화, 장애인 시설 봉사, 지역 농가 돕기 등 다양한 봉사 활동을 통해 사회적 가치를 창출합니다.")
    
    # 봉사 프로그램 정보
    volunteer_info = {
        "name": "지역 사회 연계 봉사 프로그램",
        "description": "환경정화, 장애인 시설 봉사, 지역 농가 돕기 등 활동 정례화",
        "schedule": "월 2회 정기 봉사, 분기별 특별 봉사",
        "goal": "참여 시간, 봉사 인원, 사회적 가치 환산 점수 향상"
    }
    
    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'volunteer_data' not in st.session_state:
        # 봉사 활동 유형별 데이터
        volunteer_activities = {
            "환경정화": {
                "name": "환경정화 봉사",
                "icon": "🌱",
                "color": "#28a745",
                "participants": 0,
                "total_hours": 0,
                "social_value": 0,
                "frequency": "월 2회",
                "location": "한강공원, 도심 공원"
            },
            "장애인시설": {
                "name": "장애인 시설 봉사",
                "icon": "♿",
                "color": "#007bff",
                "participants": 0,
                "total_hours": 0,
                "social_value": 0,
                "frequency": "월 1회",
                "location": "지역 장애인 복지관"
            },
            "지역농가": {
                "name": "지역 농가 돕기",
                "icon": "🚜",
                "color": "#ffc107",
                "participants": 0,
                "total_hours": 0,
                "social_value": 0,
                "frequency": "분기 1회",
                "location": "경기도 농장"
            },
            "노인복지": {
                "name": "노인 복지 봉사",
                "icon": "👴",
                "color": "#6f42c1",
                "participants": 0,
                "total_hours": 0,
                "social_value": 0,
                "frequency": "월 1회",
                "location": "지역 노인복지관"
            },
            "아동복지": {
                "name": "아동 복지 봉사",
                "icon": "👶",
                "color": "#fd7e14",
                "participants": 0,
                "total_hours": 0,
                "social_value": 0,
                "frequency": "월 1회",
                "location": "지역 아동센터"
            }
        }
        
        # 샘플 데이터 생성
        sample_activities = {
            "환경정화": {
                "name": "환경정화 봉사",
                "icon": "🌱",
                "color": "#28a745",
                "participants": np.random.randint(25, 40),
                "total_hours": np.random.randint(200, 320),
                "social_value": np.random.randint(150, 250),
                "frequency": "월 2회",
                "location": "한강공원, 도심 공원"
            },
            "장애인시설": {
                "name": "장애인 시설 봉사",
                "icon": "♿",
                "color": "#007bff",
                "participants": np.random.randint(15, 25),
                "total_hours": np.random.randint(120, 200),
                "social_value": np.random.randint(100, 180),
                "frequency": "월 1회",
                "location": "지역 장애인 복지관"
            },
            "지역농가": {
                "name": "지역 농가 돕기",
                "icon": "🚜",
                "color": "#ffc107",
                "participants": np.random.randint(20, 35),
                "total_hours": np.random.randint(160, 280),
                "social_value": np.random.randint(120, 200),
                "frequency": "분기 1회",
                "location": "경기도 농장"
            },
            "노인복지": {
                "name": "노인 복지 봉사",
                "icon": "👴",
                "color": "#6f42c1",
                "participants": np.random.randint(18, 30),
                "total_hours": np.random.randint(140, 240),
                "social_value": np.random.randint(110, 190),
                "frequency": "월 1회",
                "location": "지역 노인복지관"
            },
            "아동복지": {
                "name": "아동 복지 봉사",
                "icon": "👶",
                "color": "#fd7e14",
                "participants": np.random.randint(22, 35),
                "total_hours": np.random.randint(180, 300),
                "social_value": np.random.randint(130, 220),
                "frequency": "월 1회",
                "location": "지역 아동센터"
            }
        }
        
        # 전체 통계 계산
        total_participants = sum(activity['participants'] for activity in sample_activities.values())
        total_hours = sum(activity['total_hours'] for activity in sample_activities.values())
        total_social_value = sum(activity['social_value'] for activity in sample_activities.values())
        avg_hours_per_person = round(total_hours / total_participants, 1) if total_participants > 0 else 0
        
        st.session_state.volunteer_data = {
            "activities": sample_activities,
            "total_participants": total_participants,
            "total_hours": total_hours,
            "total_social_value": total_social_value,
            "avg_hours_per_person": avg_hours_per_person,
            "participation_rate": np.random.randint(70, 85)
        }
    
    st.markdown("---")
    
    # 봉사 프로그램 정보 카드
    st.subheader("📋 봉사 프로그램 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 일정**: {volunteer_info['schedule']}
        
        **🎯 목표**: {volunteer_info['goal']}
        
        **📝 설명**: {volunteer_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **🤝 사회효과**: 지역사회와의 유대 강화
        
        **💚 환경효과**: 환경 보호 및 정화 활동
        
        **❤️ 인적효과**: 임직원 사회적 책임 의식 향상
        """)
    
    st.markdown("---")
    
    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 참여자",
            value=f"{st.session_state.volunteer_data['total_participants']}명",
            delta=f"+{np.random.randint(3, 8)}명"
        )
    
    with col2:
        st.metric(
            label="총 봉사시간",
            value=f"{st.session_state.volunteer_data['total_hours']}시간",
            delta=f"+{np.random.randint(20, 40)}시간"
        )
    
    with col3:
        st.metric(
            label="사회적 가치",
            value=f"{st.session_state.volunteer_data['total_social_value']}점",
            delta=f"+{np.random.randint(15, 30)}점"
        )
    
    with col4:
        st.metric(
            label="참여율",
            value=f"{st.session_state.volunteer_data['participation_rate']}%",
            delta=f"+{np.random.randint(2, 5)}%"
        )
    
    st.markdown("---")
    
    # 오늘 날짜 표시
    today = datetime.now().strftime("%Y년 %m월 %d일")
    st.subheader(f"📅 {today} 봉사 활동 현황")
    
    # 봉사 활동별 카드 레이아웃
    cols = st.columns(5)
    
    for i, (activity_key, activity_info) in enumerate(st.session_state.volunteer_data['activities'].items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                border: 2px solid {activity_info['color']};
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                margin-bottom: 10px;
            ">
                <h3 style="margin: 0; color: {activity_info['color']};">{activity_info['icon']}</h3>
                <h4 style="margin: 10px 0; color: #333;">{activity_info['name']}</h4>
                <p style="margin: 5px 0; font-size: 16px; font-weight: bold; color: {activity_info['color']};">
                    참여자: {activity_info['participants']}명
                </p>
                <p style="margin: 5px 0; font-size: 14px; color: #007bff;">
                    봉사시간: {activity_info['total_hours']}시간
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                    사회가치: {activity_info['social_value']}점
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                    빈도: {activity_info['frequency']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 봉사 참여 버튼
            if st.button(f"봉사 참여", key=f"volunteer_{activity_key}", use_container_width=True):
                st.session_state.volunteer_data['activities'][activity_key]['participants'] += 1
                additional_hours = np.random.randint(4, 8)
                st.session_state.volunteer_data['activities'][activity_key]['total_hours'] += additional_hours
                additional_value = np.random.randint(8, 15)
                st.session_state.volunteer_data['activities'][activity_key]['social_value'] += additional_value
                
                # 전체 통계 업데이트
                st.session_state.volunteer_data['total_participants'] += 1
                st.session_state.volunteer_data['total_hours'] += additional_hours
                st.session_state.volunteer_data['total_social_value'] += additional_value
                st.session_state.volunteer_data['avg_hours_per_person'] = round(st.session_state.volunteer_data['total_hours'] / st.session_state.volunteer_data['total_participants'], 1)
                
                st.success(f"{activity_info['name']}에 {additional_hours}시간 참여 완료! 🤝")
                st.rerun()
    
    st.markdown("---")
    
    # 봉사 활동별 참여자 수 차트
    st.subheader("👥 봉사 활동별 참여자 수")
    
    activity_names = list(st.session_state.volunteer_data['activities'].keys())
    participants_counts = [activity['participants'] for activity in st.session_state.volunteer_data['activities'].values()]
    colors = [activity['color'] for activity in st.session_state.volunteer_data['activities'].values()]
    
    fig_participants = px.bar(
        x=activity_names,
        y=participants_counts,
        title='봉사 활동별 참여자 수',
        labels={'x': '봉사 활동', 'y': '참여자 수'},
        color=activity_names,
        color_discrete_sequence=colors
    )
    fig_participants.update_layout(
        xaxis_title="봉사 활동",
        yaxis_title="참여자 수"
    )
    st.plotly_chart(fig_participants, use_container_width=True)
    
    st.markdown("---")
    
    # 봉사 시간별 현황 차트
    st.subheader("⏰ 봉사 활동별 총 시간")
    
    total_hours = [activity['total_hours'] for activity in st.session_state.volunteer_data['activities'].values()]
    
    fig_hours = px.bar(
        x=activity_names,
        y=total_hours,
        title='봉사 활동별 총 시간',
        labels={'x': '봉사 활동', 'y': '총 시간 (시간)'},
        color=activity_names,
        color_discrete_sequence=colors
    )
    fig_hours.update_layout(
        xaxis_title="봉사 활동",
        yaxis_title="총 시간 (시간)"
    )
    st.plotly_chart(fig_hours, use_container_width=True)
    
    st.markdown("---")
    
    # 사회적 가치 환산 점수 차트
    st.subheader("💎 사회적 가치 환산 점수")
    
    social_values = [activity['social_value'] for activity in st.session_state.volunteer_data['activities'].values()]
    
    fig_social = px.bar(
        x=activity_names,
        y=social_values,
        title='봉사 활동별 사회적 가치 점수',
        labels={'x': '봉사 활동', 'y': '사회적 가치 점수'},
        color=activity_names,
        color_discrete_sequence=colors
    )
    fig_social.update_layout(
        xaxis_title="봉사 활동",
        yaxis_title="사회적 가치 점수"
    )
    st.plotly_chart(fig_social, use_container_width=True)
    
    st.markdown("---")
    
    # 봉사 활동 상세 정보
    st.subheader("📋 봉사 활동 상세 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🌱 환경정화 봉사**
        - 한강공원, 도심 공원 청소
        - 월 2회 정기 활동
        - 환경 보호 인식 제고
        
        **♿ 장애인 시설 봉사**
        - 지역 장애인 복지관 지원
        - 월 1회 정기 활동
        - 사회적 포용성 강화
        """)
    
    with col2:
        st.success("""
        **🚜 지역 농가 돕기**
        - 경기도 농장 농작업 지원
        - 분기 1회 특별 활동
        - 지역 경제 활성화
        
        **👴👶 노인/아동 복지**
        - 지역 복지관 지원
        - 월 1회 정기 활동
        - 사회적 약자 배려
        """)
    
    st.markdown("---")
    
    # 사회적 가치 환산 기준
    st.subheader("📊 사회적 가치 환산 기준")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="환경정화",
            value="시간당 1.2점",
            delta="환경 보호 효과"
        )
    
    with col2:
        st.metric(
            label="장애인/노인/아동",
            value="시간당 1.5점",
            delta="사회적 포용 효과"
        )
    
    with col3:
        st.metric(
            label="지역 농가",
            value="시간당 1.0점",
            delta="지역 경제 효과"
        )
    
    st.markdown("---")
    
    # 봉사 참여 등록
    st.subheader("📝 새 봉사 참여 등록")
    
    with st.form("volunteer_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            volunteer_name = st.text_input("참여자명", placeholder="예: 홍길동")
            activity_type = st.selectbox("봉사 활동 유형", ["환경정화", "장애인시설", "지역농가", "노인복지", "아동복지"])
            volunteer_hours = st.number_input("봉사 시간", min_value=1, max_value=8, value=4)
        
        with col2:
            volunteer_date = st.date_input("봉사 날짜", value=datetime.now().date())
            volunteer_location = st.text_input("봉사 장소", placeholder="예: 한강공원")
            volunteer_department = st.selectbox("소속 부서", ["IT개발팀", "시설관리팀", "구매팀", "환경팀", "마케팅팀", "인사팀"])
        
        volunteer_description = st.text_area("봉사 활동 내용", placeholder="봉사 활동의 구체적인 내용과 느낀 점을 작성해주세요.", height=100)
        
        submitted = st.form_submit_button("봉사 참여 등록")
        if submitted:
            if volunteer_name and volunteer_location and volunteer_description:
                # 사회적 가치 점수 계산
                value_multipliers = {
                    "환경정화": 1.2,
                    "장애인시설": 1.5,
                    "지역농가": 1.0,
                    "노인복지": 1.5,
                    "아동복지": 1.5
                }
                social_value_points = round(volunteer_hours * value_multipliers[activity_type], 1)
                
                st.success(f"{volunteer_name}님의 {activity_type} 봉사가 성공적으로 등록되었습니다! 🤝")
                st.info(f"봉사 시간: {volunteer_hours}시간, 사회적 가치: {social_value_points}점")
            else:
                st.error("모든 필수 항목을 입력해주세요!")
    
    st.markdown("---")
    
    # 봉사 성과 요약
    st.subheader("🏆 봉사 성과 요약")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="평균 봉사시간",
            value=f"{st.session_state.volunteer_data['avg_hours_per_person']}시간",
            delta="1인당 평균"
        )
    
    with col2:
        st.metric(
            label="사회적 가치",
            value=f"{st.session_state.volunteer_data['total_social_value']}점",
            delta="총 누적 점수"
        )
    
    with col3:
        st.metric(
            label="참여 부서",
            value="6개 부서",
            delta="전 부서 참여"
        )
    
    st.markdown("---")
    
    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            sample_activities = {
                "환경정화": {
                    "name": "환경정화 봉사",
                    "icon": "🌱",
                    "color": "#28a745",
                    "participants": np.random.randint(25, 40),
                    "total_hours": np.random.randint(200, 320),
                    "social_value": np.random.randint(150, 250),
                    "frequency": "월 2회",
                    "location": "한강공원, 도심 공원"
                },
                "장애인시설": {
                    "name": "장애인 시설 봉사",
                    "icon": "♿",
                    "color": "#007bff",
                    "participants": np.random.randint(15, 25),
                    "total_hours": np.random.randint(120, 200),
                    "social_value": np.random.randint(100, 180),
                    "frequency": "월 1회",
                    "location": "지역 장애인 복지관"
                },
                "지역농가": {
                    "name": "지역 농가 돕기",
                    "icon": "🚜",
                    "color": "#ffc107",
                    "participants": np.random.randint(20, 35),
                    "total_hours": np.random.randint(160, 280),
                    "social_value": np.random.randint(120, 200),
                    "frequency": "분기 1회",
                    "location": "경기도 농장"
                },
                "노인복지": {
                    "name": "노인 복지 봉사",
                    "icon": "👴",
                    "color": "#6f42c1",
                    "participants": np.random.randint(18, 30),
                    "total_hours": np.random.randint(140, 240),
                    "social_value": np.random.randint(110, 190),
                    "frequency": "월 1회",
                    "location": "지역 노인복지관"
                },
                "아동복지": {
                    "name": "아동 복지 봉사",
                    "icon": "👶",
                    "color": "#fd7e14",
                    "participants": np.random.randint(22, 35),
                    "total_hours": np.random.randint(180, 300),
                    "social_value": np.random.randint(130, 220),
                    "frequency": "월 1회",
                    "location": "지역 아동센터"
                }
            }
            
            # 전체 통계 재계산
            total_participants = sum(activity['participants'] for activity in sample_activities.values())
            total_hours = sum(activity['total_hours'] for activity in sample_activities.values())
            total_social_value = sum(activity['social_value'] for activity in sample_activities.values())
            avg_hours_per_person = round(total_hours / total_participants, 1) if total_participants > 0 else 0
            
            st.session_state.volunteer_data = {
                "activities": sample_activities,
                "total_participants": total_participants,
                "total_hours": total_hours,
                "total_social_value": total_social_value,
                "avg_hours_per_person": avg_hours_per_person,
                "participation_rate": np.random.randint(70, 85)
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 봉사 리포트", width='stretch'):
            st.info("봉사 활동 리포트를 생성했습니다!")

# 그린리본 인증 캠페인 페이지
elif menu == "그린리본 인증 캠페인":
    st.title("🏆 그린리본 인증 캠페인")
    st.write("사무실 카페·편의공간에서 ESG 제품 이용 시 '인증 스탬프'를 적립하여 친환경 소비를 장려합니다.")
    
    # 그린리본 인증 캠페인 정보
    green_ribbon_info = {
        "name": "그린리본 인증 캠페인",
        "description": "사무실 카페·편의공간에서 ESG 제품 이용 시 '인증 스탬프' 적립",
        "schedule": "상시 운영",
        "goal": "ESG 제품 구매비율 증가율, 캠페인 참여율 향상"
    }
    
    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'green_ribbon_data' not in st.session_state:
        # 사옥별 카페 정보
        cafes = {
            "잠실": {
                "name": "잠실 카페",
                "image": "☕",
                "participants": 0,
                "stamps_collected": 0,
                "esg_products": 0,
                "total_purchases": 0
            },
            "판교IT": {
                "name": "판교 IT 카페", 
                "image": "☕",
                "participants": 0,
                "stamps_collected": 0,
                "esg_products": 0,
                "total_purchases": 0
            },
            "판교물류": {
                "name": "판교 물류 카페",
                "image": "☕", 
                "participants": 0,
                "stamps_collected": 0,
                "esg_products": 0,
                "total_purchases": 0
            },
            "상암": {
                "name": "상암 카페",
                "image": "☕",
                "participants": 0,
                "stamps_collected": 0,
                "esg_products": 0,
                "total_purchases": 0
            },
            "수원": {
                "name": "수원 카페",
                "image": "☕",
                "participants": 0,
                "stamps_collected": 0,
                "esg_products": 0,
                "total_purchases": 0
            }
        }
        
        # 샘플 데이터 생성
        sample_cafes = {
            "잠실": {
                "name": "잠실 카페",
                "image": "☕",
                "participants": np.random.randint(35, 55),
                "stamps_collected": np.random.randint(120, 180),
                "esg_products": np.random.randint(25, 40),
                "total_purchases": np.random.randint(80, 120)
            },
            "판교IT": {
                "name": "판교 IT 카페", 
                "image": "☕",
                "participants": np.random.randint(40, 60),
                "stamps_collected": np.random.randint(140, 200),
                "esg_products": np.random.randint(30, 45),
                "total_purchases": np.random.randint(90, 130)
            },
            "판교물류": {
                "name": "판교 물류 카페",
                "image": "☕", 
                "participants": np.random.randint(25, 40),
                "stamps_collected": np.random.randint(100, 150),
                "esg_products": np.random.randint(20, 35),
                "total_purchases": np.random.randint(60, 100)
            },
            "상암": {
                "name": "상암 카페",
                "image": "☕",
                "participants": np.random.randint(30, 45),
                "stamps_collected": np.random.randint(110, 160),
                "esg_products": np.random.randint(22, 38),
                "total_purchases": np.random.randint(70, 110)
            },
            "수원": {
                "name": "수원 카페",
                "image": "☕",
                "participants": np.random.randint(20, 35),
                "stamps_collected": np.random.randint(80, 130),
                "esg_products": np.random.randint(18, 30),
                "total_purchases": np.random.randint(50, 90)
            }
        }
        
        # 전체 통계 계산
        total_participants = sum(cafe['participants'] for cafe in sample_cafes.values())
        total_stamps = sum(cafe['stamps_collected'] for cafe in sample_cafes.values())
        total_esg_products = sum(cafe['esg_products'] for cafe in sample_cafes.values())
        total_purchases = sum(cafe['total_purchases'] for cafe in sample_cafes.values())
        esg_purchase_rate = round((total_esg_products / total_purchases) * 100, 1) if total_purchases > 0 else 0
        
        st.session_state.green_ribbon_data = {
            "cafes": sample_cafes,
            "total_participants": total_participants,
            "total_stamps": total_stamps,
            "total_esg_products": total_esg_products,
            "total_purchases": total_purchases,
            "esg_purchase_rate": esg_purchase_rate,
            "participation_rate": np.random.randint(75, 90)
        }
    
    st.markdown("---")
    
    # 그린리본 인증 캠페인 정보 카드
    st.subheader("📋 그린리본 인증 캠페인 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 운영**: {green_ribbon_info['schedule']}
        
        **🎯 목표**: {green_ribbon_info['goal']}
        
        **📝 설명**: {green_ribbon_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **🌱 환경효과**: 친환경 제품 구매 증가
        
        **💚 사회효과**: ESG 인식 확산
        
        **🎁 혜택효과**: 스탬프 적립으로 리워드 제공
        """)
    
    st.markdown("---")
    
    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 참여자",
            value=f"{st.session_state.green_ribbon_data['total_participants']}명",
            delta=f"+{np.random.randint(5, 12)}명"
        )
    
    with col2:
        st.metric(
            label="총 스탬프",
            value=f"{st.session_state.green_ribbon_data['total_stamps']}개",
            delta=f"+{np.random.randint(15, 30)}개"
        )
    
    with col3:
        st.metric(
            label="ESG 구매비율",
            value=f"{st.session_state.green_ribbon_data['esg_purchase_rate']}%",
            delta=f"+{np.random.randint(2, 5)}%"
        )
    
    with col4:
        st.metric(
            label="참여율",
            value=f"{st.session_state.green_ribbon_data['participation_rate']}%",
            delta=f"+{np.random.randint(3, 8)}%"
        )
    
    st.markdown("---")
    
    # 오늘 날짜 표시
    today = datetime.now().strftime("%Y년 %m월 %d일")
    st.subheader(f"📅 {today} 그린리본 인증 현황")
    
    # 사옥별 카페 카드 레이아웃
    cols = st.columns(5)
    
    for i, (cafe_key, cafe_info) in enumerate(st.session_state.green_ribbon_data['cafes'].items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                margin-bottom: 10px;
            ">
                <h3 style="margin: 0; color: #28a745;">{cafe_info['image']}</h3>
                <h4 style="margin: 10px 0; color: #333;">{cafe_info['name']}</h4>
                <p style="margin: 5px 0; font-size: 16px; font-weight: bold; color: #28a745;">
                    참여자: {cafe_info['participants']}명
                </p>
                <p style="margin: 5px 0; font-size: 14px; color: #007bff;">
                    스탬프: {cafe_info['stamps_collected']}개
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                    ESG구매: {cafe_info['esg_products']}건
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                    총구매: {cafe_info['total_purchases']}건
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 스탬프 적립 버튼
            if st.button(f"스탬프 적립", key=f"stamp_{cafe_key}", use_container_width=True):
                st.session_state.green_ribbon_data['cafes'][cafe_key]['participants'] += 1
                additional_stamps = np.random.randint(2, 5)
                st.session_state.green_ribbon_data['cafes'][cafe_key]['stamps_collected'] += additional_stamps
                additional_esg = np.random.randint(1, 3)
                st.session_state.green_ribbon_data['cafes'][cafe_key]['esg_products'] += additional_esg
                additional_purchases = np.random.randint(2, 4)
                st.session_state.green_ribbon_data['cafes'][cafe_key]['total_purchases'] += additional_purchases
                
                # 전체 통계 업데이트
                st.session_state.green_ribbon_data['total_participants'] += 1
                st.session_state.green_ribbon_data['total_stamps'] += additional_stamps
                st.session_state.green_ribbon_data['total_esg_products'] += additional_esg
                st.session_state.green_ribbon_data['total_purchases'] += additional_purchases
                st.session_state.green_ribbon_data['esg_purchase_rate'] = round((st.session_state.green_ribbon_data['total_esg_products'] / st.session_state.green_ribbon_data['total_purchases']) * 100, 1)
                
                st.success(f"{cafe_info['name']}에서 스탬프 {additional_stamps}개 적립 완료! 🏆")
                st.rerun()
    
    st.markdown("---")
    
    # 사옥별 스탬프 적립 현황 차트
    st.subheader("🏆 사옥별 스탬프 적립 현황")
    
    cafe_names = list(st.session_state.green_ribbon_data['cafes'].keys())
    stamps_collected = [cafe['stamps_collected'] for cafe in st.session_state.green_ribbon_data['cafes'].values()]
    
    fig_stamps = px.bar(
        x=cafe_names,
        y=stamps_collected,
        title='사옥별 스탬프 적립 수',
        labels={'x': '사옥', 'y': '스탬프 수'},
        color=stamps_collected,
        color_continuous_scale='Greens'
    )
    fig_stamps.update_layout(
        xaxis_title="사옥",
        yaxis_title="스탬프 수"
    )
    st.plotly_chart(fig_stamps, use_container_width=True)
    
    st.markdown("---")
    
    # 사옥별 ESG 구매비율 차트
    st.subheader("🌱 사옥별 ESG 구매비율")
    
    esg_rates = []
    for cafe in st.session_state.green_ribbon_data['cafes'].values():
        rate = round((cafe['esg_products'] / cafe['total_purchases']) * 100, 1) if cafe['total_purchases'] > 0 else 0
        esg_rates.append(rate)
    
    fig_esg = px.bar(
        x=cafe_names,
        y=esg_rates,
        title='사옥별 ESG 제품 구매비율',
        labels={'x': '사옥', 'y': 'ESG 구매비율 (%)'},
        color=esg_rates,
        color_continuous_scale='Blues'
    )
    fig_esg.update_layout(
        xaxis_title="사옥",
        yaxis_title="ESG 구매비율 (%)"
    )
    st.plotly_chart(fig_esg, use_container_width=True)
    
    st.markdown("---")
    
    # ESG 제품 정보
    st.subheader("🌿 인증 가능한 ESG 제품")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **☕ 카페 제품**
        - 친환경 컵 사용
        - 유기농 원두
        - 재활용 포장재
        - 지역 농산물 사용
        """)
    
    with col2:
        st.success("""
        **🛒 편의공간 제품**
        - 친환경 포장재
        - 유기농 간식
        - 재활용 용품
        - 공정무역 제품
        """)
    
    st.markdown("---")
    
    # 스탬프 적립 규칙
    st.subheader("📋 스탬프 적립 규칙")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="ESG 제품 구매",
            value="1개당 1스탬프",
            delta="기본 적립"
        )
    
    with col2:
        st.metric(
            label="친환경 컵 사용",
            value="1회당 2스탬프",
            delta="추가 적립"
        )
    
    with col3:
        st.metric(
            label="리워드 교환",
            value="10스탬프",
            delta="무료 음료"
        )
    
    st.markdown("---")
    
    # 환경 효과
    st.subheader("🌱 환경 효과")
    
    col1, col2, col3 = st.columns(3)
    
    total_esg = st.session_state.green_ribbon_data['total_esg_products']
    
    with col1:
        st.metric(
            label="CO2 절약",
            value=f"{total_esg * 0.5:.1f}kg",
            delta="월간 절약"
        )
    
    with col2:
        st.metric(
            label="플라스틱 감소",
            value=f"{total_esg * 0.3:.1f}개",
            delta="월간 감소"
        )
    
    with col3:
        st.metric(
            label="재활용률",
            value=f"{np.random.randint(85, 95)}%",
            delta="월간 재활용"
        )
    
    st.markdown("---")
    
    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            sample_cafes = {
                "잠실": {
                    "name": "잠실 카페",
                    "image": "☕",
                    "participants": np.random.randint(35, 55),
                    "stamps_collected": np.random.randint(120, 180),
                    "esg_products": np.random.randint(25, 40),
                    "total_purchases": np.random.randint(80, 120)
                },
                "판교IT": {
                    "name": "판교 IT 카페", 
                    "image": "☕",
                    "participants": np.random.randint(40, 60),
                    "stamps_collected": np.random.randint(140, 200),
                    "esg_products": np.random.randint(30, 45),
                    "total_purchases": np.random.randint(90, 130)
                },
                "판교물류": {
                    "name": "판교 물류 카페",
                    "image": "☕", 
                    "participants": np.random.randint(25, 40),
                    "stamps_collected": np.random.randint(100, 150),
                    "esg_products": np.random.randint(20, 35),
                    "total_purchases": np.random.randint(60, 100)
                },
                "상암": {
                    "name": "상암 카페",
                    "image": "☕",
                    "participants": np.random.randint(30, 45),
                    "stamps_collected": np.random.randint(110, 160),
                    "esg_products": np.random.randint(22, 38),
                    "total_purchases": np.random.randint(70, 110)
                },
                "수원": {
                    "name": "수원 카페",
                    "image": "☕",
                    "participants": np.random.randint(20, 35),
                    "stamps_collected": np.random.randint(80, 130),
                    "esg_products": np.random.randint(18, 30),
                    "total_purchases": np.random.randint(50, 90)
                }
            }
            
            # 전체 통계 재계산
            total_participants = sum(cafe['participants'] for cafe in sample_cafes.values())
            total_stamps = sum(cafe['stamps_collected'] for cafe in sample_cafes.values())
            total_esg_products = sum(cafe['esg_products'] for cafe in sample_cafes.values())
            total_purchases = sum(cafe['total_purchases'] for cafe in sample_cafes.values())
            esg_purchase_rate = round((total_esg_products / total_purchases) * 100, 1) if total_purchases > 0 else 0
            
            st.session_state.green_ribbon_data = {
                "cafes": sample_cafes,
                "total_participants": total_participants,
                "total_stamps": total_stamps,
                "total_esg_products": total_esg_products,
                "total_purchases": total_purchases,
                "esg_purchase_rate": esg_purchase_rate,
                "participation_rate": np.random.randint(75, 90)
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 인증 리포트", width='stretch'):
            st.info("그린리본 인증 리포트를 생성했습니다!")

# 임직원 아이디어 페이지
elif menu == "임직원 아이디어":
    st.title("💡 임직원 아이디어")
    st.write("삼성SDS 임직원들의 혁신적인 ESG 아이디어를 수집하고 단계별로 관리합니다.")
    
    # 아이디어 Workflow 정보
    workflow_info = {
        "name": "ESG 아이디어 공모전",
        "description": "임직원들의 혁신적인 ESG 아이디어 수집 및 단계별 관리",
        "schedule": "분기별 공모전 개최",
        "goal": "아이디어 구현률 20% 달성, 혁신 문화 조성"
    }
    
    # 세션 상태 초기화 (샘플 데이터 포함)
    if 'idea_data' not in st.session_state:
        # Workflow 단계별 샘플 데이터
        workflow_stages = {
            "제안": {
                "count": 45,
                "color": "#FF6B6B",
                "description": "새로운 아이디어 제안",
                "icon": "💡"
            },
            "검토": {
                "count": 28,
                "color": "#4ECDC4", 
                "description": "전문가 검토 중",
                "icon": "🔍"
            },
            "평가": {
                "count": 18,
                "color": "#45B7D1",
                "description": "실현가능성 평가",
                "icon": "📊"
            },
            "승인": {
                "count": 12,
                "color": "#96CEB4",
                "description": "구현 승인됨",
                "icon": "✅"
            },
            "구현": {
                "count": 8,
                "color": "#FFEAA7",
                "description": "실제 구현 중",
                "icon": "🚀"
            },
            "완료": {
                "count": 5,
                "color": "#DDA0DD",
                "description": "구현 완료",
                "icon": "🎉"
            }
        }
        
        # 카테고리별 통계
        category_stats = {
            "Scope 1": {"total": 25, "implemented": 3},
            "Scope 2": {"total": 18, "implemented": 2},
            "Scope 3": {"total": 22, "implemented": 2},
            "순환경제": {"total": 15, "implemented": 1},
            "기타": {"total": 12, "implemented": 0}
        }
        
        st.session_state.idea_data = {
            "workflow_stages": workflow_stages,
            "category_stats": category_stats,
            "total_ideas": sum(stage["count"] for stage in workflow_stages.values()),
            "implemented_ideas": workflow_stages["완료"]["count"],
            "implementation_rate": round((workflow_stages["완료"]["count"] / sum(stage["count"] for stage in workflow_stages.values())) * 100, 1)
        }
    
    st.markdown("---")
    
    # 아이디어 공모전 정보 카드
    st.subheader("📋 아이디어 공모전 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 일정**: {workflow_info['schedule']}
        
        **🎯 목표**: {workflow_info['goal']}
        
        **📝 설명**: {workflow_info['description']}
        """)
    
    with col2:
        st.success(f"""
        **💡 혁신효과**: 임직원 창의성 발휘
        
        **🌱 ESG효과**: 지속가능한 경영 실현
        
        **🤝 협업효과**: 부서 간 소통 강화
        """)
    
    st.markdown("---")
    
    # 전체 통계
    st.subheader("📊 전체 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 아이디어",
            value=f"{st.session_state.idea_data['total_ideas']}건",
            delta=f"+{np.random.randint(3, 8)}건"
        )
    
    with col2:
        st.metric(
            label="구현 완료",
            value=f"{st.session_state.idea_data['implemented_ideas']}건",
            delta=f"+{np.random.randint(1, 3)}건"
        )
    
    with col3:
        st.metric(
            label="구현률",
            value=f"{st.session_state.idea_data['implementation_rate']}%",
            delta=f"+{np.random.randint(1, 3)}%"
        )
    
    with col4:
        st.metric(
            label="진행중",
            value=f"{st.session_state.idea_data['workflow_stages']['구현']['count']}건",
            delta=f"+{np.random.randint(1, 2)}건"
        )
    
    st.markdown("---")
    
    # Workflow 간반차트
    st.subheader("🔄 아이디어 Workflow 진행현황")
    
    # 간반차트 데이터 준비
    stages = list(st.session_state.idea_data['workflow_stages'].keys())
    counts = [st.session_state.idea_data['workflow_stages'][stage]['count'] for stage in stages]
    colors = [st.session_state.idea_data['workflow_stages'][stage]['color'] for stage in stages]
    
    # 간반차트 생성
    fig_workflow = px.funnel(
        x=counts,
        y=stages,
        title='아이디어 Workflow 단계별 진행현황',
        color=stages,
        color_discrete_sequence=colors,
        orientation='h'
    )
    
    fig_workflow.update_layout(
        height=400,
        xaxis_title="아이디어 수",
        yaxis_title="Workflow 단계",
        showlegend=False
    )
    
    st.plotly_chart(fig_workflow, use_container_width=True)
    
    st.markdown("---")
    
    # 단계별 상세 정보
    st.subheader("📈 단계별 상세 현황")
    
    # 3열 레이아웃으로 단계별 카드 표시
    cols = st.columns(3)
    
    for i, (stage_name, stage_info) in enumerate(st.session_state.idea_data['workflow_stages'].items()):
        col_idx = i % 3
        with cols[col_idx]:
            st.markdown(f"""
            <div style="
                border: 2px solid {stage_info['color']};
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                margin-bottom: 10px;
            ">
                <h3 style="margin: 0; color: {stage_info['color']};">{stage_info['icon']}</h3>
                <h4 style="margin: 10px 0; color: #333;">{stage_name}</h4>
                <p style="margin: 5px 0; font-size: 24px; font-weight: bold; color: {stage_info['color']};">
                    {stage_info['count']}건
                </p>
                <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                    {stage_info['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 카테고리별 통계
    st.subheader("📊 카테고리별 아이디어 현황")
    
    categories = list(st.session_state.idea_data['category_stats'].keys())
    total_counts = [st.session_state.idea_data['category_stats'][cat]['total'] for cat in categories]
    implemented_counts = [st.session_state.idea_data['category_stats'][cat]['implemented'] for cat in categories]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_total = px.bar(
            x=categories,
            y=total_counts,
            title='카테고리별 총 아이디어 수',
            labels={'x': '카테고리', 'y': '아이디어 수'},
            color=total_counts,
            color_continuous_scale='Blues'
        )
        fig_total.update_layout(xaxis_title="카테고리", yaxis_title="총 아이디어 수")
        st.plotly_chart(fig_total, use_container_width=True)
    
    with col2:
        fig_implemented = px.bar(
            x=categories,
            y=implemented_counts,
            title='카테고리별 구현된 아이디어 수',
            labels={'x': '카테고리', 'y': '구현된 아이디어 수'},
            color=implemented_counts,
            color_continuous_scale='Greens'
        )
        fig_implemented.update_layout(xaxis_title="카테고리", yaxis_title="구현된 아이디어 수")
        st.plotly_chart(fig_implemented, use_container_width=True)
    
    st.markdown("---")
    
    # 아이디어 제안 섹션
    st.subheader("💡 새 아이디어 제안")
    
    with st.form("idea_submission"):
        col1, col2 = st.columns(2)
        
        with col1:
            idea_title = st.text_input("아이디어 제목", placeholder="예: 스마트 조명 시스템 도입")
            idea_category = st.selectbox("카테고리", ["Scope 1", "Scope 2", "Scope 3", "순환경제", "기타"])
            idea_department = st.selectbox("제안 부서", ["IT개발팀", "시설관리팀", "구매팀", "환경팀", "마케팅팀", "인사팀"])
        
        with col2:
            idea_priority = st.selectbox("우선순위", ["낮음", "보통", "높음", "긴급"])
            expected_impact = st.selectbox("예상 효과", ["낮음", "보통", "높음", "매우 높음"])
            implementation_period = st.selectbox("구현 기간", ["1개월", "3개월", "6개월", "1년", "1년 이상"])
        
        idea_description = st.text_area("아이디어 상세 설명", placeholder="아이디어의 배경, 목적, 구체적인 방안 등을 자세히 설명해주세요.", height=100)
        
        submitted = st.form_submit_button("아이디어 제안")
        if submitted:
            if idea_title and idea_description:
                st.success(f"'{idea_title}' 아이디어가 성공적으로 제안되었습니다! 🎉")
                st.info("제안된 아이디어는 검토 단계로 이동하여 전문가들의 평가를 받게 됩니다.")
            else:
                st.error("제목과 설명을 모두 입력해주세요!")
    
    st.markdown("---")
    
    # 인기 아이디어 TOP 5
    st.subheader("🏆 인기 아이디어 TOP 5")
    
    popular_ideas = [
        {"title": "사무용 전기차 충전소 확대", "likes": 25, "category": "Scope 1", "stage": "구현", "impact": "높음"},
        {"title": "스마트 조명 시스템 도입", "likes": 22, "category": "Scope 2", "stage": "승인", "impact": "높음"},
        {"title": "공급업체 친환경 인증 제도", "likes": 18, "category": "Scope 3", "stage": "평가", "impact": "매우 높음"},
        {"title": "사무실 내 재활용 시스템 개선", "likes": 15, "category": "순환경제", "stage": "검토", "impact": "보통"},
        {"title": "원격근무 환경 최적화", "likes": 12, "category": "기타", "stage": "제안", "impact": "높음"}
    ]
    
    for i, idea in enumerate(popular_ideas, 1):
        with st.expander(f"#{i} {idea['title']} (👍 {idea['likes']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**카테고리:** {idea['category']}")
                st.write(f"**현재 단계:** {idea['stage']}")
            
            with col2:
                st.write(f"**예상 효과:** {idea['impact']}")
                st.write(f"**좋아요 수:** {idea['likes']}개")
            
            with col3:
                st.write("**상태:** 진행중")
                st.write("**제안자:** 김혁신")
            
            st.write("**상세 설명:** 해당 아이디어에 대한 구체적인 내용과 기대효과...")
    
    st.markdown("---")
    
    # 데이터 관리
    st.subheader("🔄 데이터 관리")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 데이터 초기화", width='stretch'):
            # 새로운 샘플 데이터 생성
            workflow_stages = {
                "제안": {
                    "count": np.random.randint(40, 50),
                    "color": "#FF6B6B",
                    "description": "새로운 아이디어 제안",
                    "icon": "💡"
                },
                "검토": {
                    "count": np.random.randint(25, 35),
                    "color": "#4ECDC4", 
                    "description": "전문가 검토 중",
                    "icon": "🔍"
                },
                "평가": {
                    "count": np.random.randint(15, 25),
                    "color": "#45B7D1",
                    "description": "실현가능성 평가",
                    "icon": "📊"
                },
                "승인": {
                    "count": np.random.randint(10, 15),
                    "color": "#96CEB4",
                    "description": "구현 승인됨",
                    "icon": "✅"
                },
                "구현": {
                    "count": np.random.randint(5, 12),
                    "color": "#FFEAA7",
                    "description": "실제 구현 중",
                    "icon": "🚀"
                },
                "완료": {
                    "count": np.random.randint(3, 8),
                    "color": "#DDA0DD",
                    "description": "구현 완료",
                    "icon": "🎉"
                }
            }
            
            category_stats = {
                "Scope 1": {"total": np.random.randint(20, 30), "implemented": np.random.randint(2, 5)},
                "Scope 2": {"total": np.random.randint(15, 25), "implemented": np.random.randint(1, 4)},
                "Scope 3": {"total": np.random.randint(18, 28), "implemented": np.random.randint(1, 4)},
                "순환경제": {"total": np.random.randint(12, 20), "implemented": np.random.randint(1, 3)},
                "기타": {"total": np.random.randint(8, 15), "implemented": np.random.randint(0, 2)}
            }
            
            total_ideas = sum(stage["count"] for stage in workflow_stages.values())
            implemented_ideas = workflow_stages["완료"]["count"]
            implementation_rate = round((implemented_ideas / total_ideas) * 100, 1)
            
            st.session_state.idea_data = {
                "workflow_stages": workflow_stages,
                "category_stats": category_stats,
                "total_ideas": total_ideas,
                "implemented_ideas": implemented_ideas,
                "implementation_rate": implementation_rate
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 아이디어 리포트", width='stretch'):
            st.info("아이디어 리포트를 생성했습니다!")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌱 <strong>삼성SDS ESG Re:source</strong> - 디지털 혁신으로 지속가능한 미래를 만들어갑니다</p>
</div>
""", unsafe_allow_html=True)
