import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="삼성SDS ESG 탄소관리 시스템",
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
</style>
""", unsafe_allow_html=True)

# 사이드바 네비게이션
st.sidebar.markdown("""
<div style="padding: 1rem; text-align: left;">
    <h2 style="color: white; margin: 0; text-align: left !important;">🌱 삼성SDS ESG</h2>
    <p style="color: #e0e0e0; margin: 0; text-align: left !important;">탄소관리 시스템</p>
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

# Level 1 버튼들
for level1 in level1_menus.keys():
    if st.sidebar.button(f"📁 {level1}", key=f"level1_{level1}", use_container_width=True):
        st.session_state.selected_level1 = level1
        st.rerun()

st.sidebar.markdown("---")

# Level 2 메뉴들
st.sidebar.markdown(f"**{st.session_state.selected_level1}**")
for level2_name, level2_value in level1_menus[st.session_state.selected_level1].items():
    if st.sidebar.button(f"📋 {level2_name}", key=f"level2_{level2_value}", use_container_width=True):
        st.session_state.selected_menu = level2_value
        st.rerun()

# 기본 메뉴 선택
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "계단 오르기"

menu = st.session_state.selected_menu

# 현재 선택된 메뉴 표시
st.sidebar.markdown(f"**현재 페이지:** {menu}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 빠른 액세스")
if st.sidebar.button("🏠 환경 메뉴로 이동", use_container_width=True):
    st.session_state.selected_level1 = "E : 환경"
    st.session_state.selected_menu = "계단 오르기"
    st.rerun()

# 계단 오르기 페이지
elif menu == "계단 오르기":
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
            label="탄소 절약",
            value=f"{total_participants * 0.1:.1f}kg",
            delta="CO2"
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

    st.markdown("---")

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
        
        st.session_state.zero_challenge_data = {
            "participants": total_participants,
            "personal_cups": personal_cups,
            "tumblers": tumblers,
            "lunchboxes": lunchboxes,
            "single_use_reduction": single_use_reduction,
            "daily_registrations": sample_registrations
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
    
    col1, col2, col3, col4 = st.columns(4)
    
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
            label="탄소 절약",
            value=f"{st.session_state.zero_challenge_data['single_use_reduction'] * 0.05:.2f}kg",
            delta="CO2"
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
            
            st.session_state.zero_challenge_data = {
                "participants": total_participants,
                "personal_cups": personal_cups,
                "tumblers": tumblers,
                "lunchboxes": lunchboxes,
                "single_use_reduction": single_use_reduction,
                "daily_registrations": sample_registrations
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
        
        st.session_state.paperless_data = {
            "weekly_data": weekly_data,
            "total_prints": sum(day['prints'] for day in weekly_data),
            "total_paper_purchase": sum(day['paper_purchase'] for day in weekly_data),
            "digital_adoption_rate": np.random.randint(65, 80),
            "paper_savings": np.random.randint(20, 35),
            "cost_savings": np.random.randint(500, 800)  # 천원 단위
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
    
    col1, col2, col3, col4 = st.columns(4)
    
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
                전자결재: {e_approval}%
            </p>
            <p style="margin: 5px 0; font-size: 16px; color: #004085;">
                PDF 회의: {pdf_meeting}%
            </p>
        </div>
        """.format(
            e_approval=np.random.randint(85, 95),
            pdf_meeting=np.random.randint(70, 85)
        ), unsafe_allow_html=True)

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
            
            st.session_state.paperless_data = {
                "weekly_data": weekly_data,
                "total_prints": sum(day['prints'] for day in weekly_data),
                "total_paper_purchase": sum(day['paper_purchase'] for day in weekly_data),
                "digital_adoption_rate": np.random.randint(65, 80),
                "paper_savings": np.random.randint(20, 35),
                "cost_savings": np.random.randint(500, 800)
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
    st.write("퇴근 후 불필요한 조명·모니터 끄기와 점심시간 조명 절반 소등을 통해 전력 사용량을 줄입니다.")

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
        base_monthly_power = np.random.randint(8000, 12000)  # 기본 월 전력 사용량 (kWh)
        base_electricity_bill = base_monthly_power * 120  # 기본 전기요금 (원, kWh당 120원)
        
        # 절전 효과 (20% 감소)
        saved_power = int(base_monthly_power * 0.2)
        saved_bill = int(base_electricity_bill * 0.2)
        
        # 일별 데이터 생성 (최근 30일)
        daily_data = []
        for i in range(30):
            day = (datetime.now() - timedelta(days=29-i)).strftime("%m/%d")
            weekday = (datetime.now() - timedelta(days=29-i)).weekday()
            
            # 평일과 주말 구분
            if weekday < 5:  # 평일
                base_daily_power = np.random.randint(250, 350)
                # 절전 효과 적용 (퇴근 후, 점심시간)
                power_saved = np.random.randint(40, 80)
                daily_power = base_daily_power - power_saved
            else:  # 주말
                base_daily_power = np.random.randint(100, 150)
                power_saved = np.random.randint(20, 40)
                daily_power = base_daily_power - power_saved
            
            daily_data.append({
                'date': day,
                'power_usage': daily_power,
                'power_saved': power_saved,
                'is_weekday': weekday < 5,
                'lights_off': np.random.randint(80, 95),  # 조명 소등률
                'monitors_off': np.random.randint(70, 90),  # 모니터 소등률
                'lunch_saving': np.random.randint(60, 80)  # 점심시간 절전률
            })
        
        # 월별 비교 데이터
        monthly_comparison = {
            'previous_month': {
                'power_usage': base_monthly_power,
                'electricity_bill': base_electricity_bill,
                'lights_off_rate': np.random.randint(40, 60),
                'monitors_off_rate': np.random.randint(30, 50)
            },
            'current_month': {
                'power_usage': base_monthly_power - saved_power,
                'electricity_bill': base_electricity_bill - saved_bill,
                'lights_off_rate': np.random.randint(80, 95),
                'monitors_off_rate': np.random.randint(70, 90)
            }
        }
        
        st.session_state.power_saving_data = {
            "daily_data": daily_data,
            "monthly_comparison": monthly_comparison,
            "total_power_saved": saved_power,
            "total_bill_saved": saved_bill,
            "participation_rate": np.random.randint(85, 95),
            "average_daily_saving": saved_power // 30
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

    # 월별 절약 현황
    st.subheader("📊 월별 절약 현황")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="전력 절약량",
            value=f"{st.session_state.power_saving_data['total_power_saved']}kWh",
            delta=f"-{st.session_state.power_saving_data['total_power_saved']}kWh"
        )
    
    with col2:
        st.metric(
            label="전기요금 절약",
            value=f"{st.session_state.power_saving_data['total_bill_saved']:,}원",
            delta=f"-{st.session_state.power_saving_data['total_bill_saved']:,}원"
        )
    
    with col3:
        st.metric(
            label="참여율",
            value=f"{st.session_state.power_saving_data['participation_rate']}%",
            delta=f"+{np.random.randint(5, 15)}%"
        )
    
    with col4:
        st.metric(
            label="일평균 절약",
            value=f"{st.session_state.power_saving_data['average_daily_saving']}kWh",
            delta="일일 평균"
        )

    st.markdown("---")

    # 월별 전력 사용량 비교
    st.subheader("📈 월별 전력 사용량 비교")
    
    comparison_data = st.session_state.power_saving_data['monthly_comparison']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**이전 달**")
        st.metric("전력 사용량", f"{comparison_data['previous_month']['power_usage']:,}kWh")
        st.metric("전기요금", f"{comparison_data['previous_month']['electricity_bill']:,}원")
        st.metric("조명 소등률", f"{comparison_data['previous_month']['lights_off_rate']}%")
        st.metric("모니터 소등률", f"{comparison_data['previous_month']['monitors_off_rate']}%")
    
    with col2:
        st.markdown("**이번 달**")
        st.metric("전력 사용량", f"{comparison_data['current_month']['power_usage']:,}kWh")
        st.metric("전기요금", f"{comparison_data['current_month']['electricity_bill']:,}원")
        st.metric("조명 소등률", f"{comparison_data['current_month']['lights_off_rate']}%")
        st.metric("모니터 소등률", f"{comparison_data['current_month']['monitors_off_rate']}%")

    st.markdown("---")

    # 일별 전력 사용량 추이
    st.subheader("📅 일별 전력 사용량 추이")
    
    daily_df = pd.DataFrame(st.session_state.power_saving_data['daily_data'])
    
    fig_daily = px.line(
        daily_df,
        x='date',
        y='power_usage',
        title='일별 전력 사용량 추이',
        markers=True,
        labels={'power_usage': '전력 사용량 (kWh)', 'date': '날짜'},
        color_discrete_sequence=['#28a745']
    )
    fig_daily.update_layout(
        xaxis_title="날짜",
        yaxis_title="전력 사용량 (kWh)",
        xaxis_tickangle=45
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown("---")

    # 절전 활동별 효과
    st.subheader("💡 절전 활동별 효과")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #fff3cd;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #856404;">💡</h3>
            <h4 style="margin: 10px 0; color: #856404;">퇴근 후 조명 소등</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #856404;">
                소등률: {lights_off}%
            </p>
            <p style="margin: 5px 0; font-size: 16px; color: #856404;">
                절약량: {lights_saving}kWh
            </p>
        </div>
        """.format(
            lights_off=np.random.randint(80, 95),
            lights_saving=np.random.randint(200, 300)
        ), unsafe_allow_html=True)
    
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
            <h3 style="margin: 0; color: #0c5460;">🖥️</h3>
            <h4 style="margin: 10px 0; color: #0c5460;">모니터 자동 소등</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #0c5460;">
                소등률: {monitors_off}%
            </p>
            <p style="margin: 5px 0; font-size: 16px; color: #0c5460;">
                절약량: {monitors_saving}kWh
            </p>
        </div>
        """.format(
            monitors_off=np.random.randint(70, 90),
            monitors_saving=np.random.randint(150, 250)
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            border: 2px solid #6f42c1;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #e2d9f3;
            margin-bottom: 10px;
        ">
            <h3 style="margin: 0; color: #4a2c7a;">🍽️</h3>
            <h4 style="margin: 10px 0; color: #4a2c7a;">점심시간 절전</h4>
            <p style="margin: 5px 0; font-size: 16px; color: #4a2c7a;">
                절전률: {lunch_saving}%
            </p>
            <p style="margin: 5px 0; font-size: 16px; color: #4a2c7a;">
                절약량: {lunch_power_saving}kWh
            </p>
        </div>
        """.format(
            lunch_saving=np.random.randint(60, 80),
            lunch_power_saving=np.random.randint(100, 200)
        ), unsafe_allow_html=True)

    st.markdown("---")

    # 절전 활동별 효과 차트
    st.subheader("📊 절전 활동별 효과")
    
    activities = ['퇴근 후 조명 소등', '모니터 자동 소등', '점심시간 절전']
    savings = [
        np.random.randint(200, 300),
        np.random.randint(150, 250),
        np.random.randint(100, 200)
    ]
    
    fig_activities = px.bar(
        x=activities,
        y=savings,
        title='절전 활동별 월간 절약량',
        labels={'x': '절전 활동', 'y': '절약량 (kWh)'},
        color=savings,
        color_continuous_scale='Greens'
    )
    fig_activities.update_layout(
        xaxis_title="절전 활동",
        yaxis_title="절약량 (kWh)"
    )
    st.plotly_chart(fig_activities, use_container_width=True)

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
            base_monthly_power = np.random.randint(8000, 12000)
            base_electricity_bill = base_monthly_power * 120
            saved_power = int(base_monthly_power * 0.2)
            saved_bill = int(base_electricity_bill * 0.2)
            
            daily_data = []
            for i in range(30):
                day = (datetime.now() - timedelta(days=29-i)).strftime("%m/%d")
                weekday = (datetime.now() - timedelta(days=29-i)).weekday()
                
                if weekday < 5:
                    base_daily_power = np.random.randint(250, 350)
                    power_saved = np.random.randint(40, 80)
                    daily_power = base_daily_power - power_saved
                else:
                    base_daily_power = np.random.randint(100, 150)
                    power_saved = np.random.randint(20, 40)
                    daily_power = base_daily_power - power_saved
                
                daily_data.append({
                    'date': day,
                    'power_usage': daily_power,
                    'power_saved': power_saved,
                    'is_weekday': weekday < 5,
                    'lights_off': np.random.randint(80, 95),
                    'monitors_off': np.random.randint(70, 90),
                    'lunch_saving': np.random.randint(60, 80)
                })
            
            monthly_comparison = {
                'previous_month': {
                    'power_usage': base_monthly_power,
                    'electricity_bill': base_electricity_bill,
                    'lights_off_rate': np.random.randint(40, 60),
                    'monitors_off_rate': np.random.randint(30, 50)
                },
                'current_month': {
                    'power_usage': base_monthly_power - saved_power,
                    'electricity_bill': base_electricity_bill - saved_bill,
                    'lights_off_rate': np.random.randint(80, 95),
                    'monitors_off_rate': np.random.randint(70, 90)
                }
            }
            
            st.session_state.power_saving_data = {
                "daily_data": daily_data,
                "monthly_comparison": monthly_comparison,
                "total_power_saved": saved_power,
                "total_bill_saved": saved_bill,
                "participation_rate": np.random.randint(85, 95),
                "average_daily_saving": saved_power // 30
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
            "participation_rate": np.random.randint(75, 90)
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
    
    col1, col2, col3, col4 = st.columns(4)
    
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
                "participation_rate": np.random.randint(75, 90)
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
        
        # 교통수단별 탄소 감축량 (kg CO2)
        carbon_savings = {
            'stairs': stairs_usage * 0.05,  # 계단 이용시 엘리베이터 대비 절약
            'public_transport': public_transport * 0.3,  # 대중교통 이용시 개인차 대비 절약
            'bicycle': bicycle_usage * 0.2  # 자전거 이용시 개인차 대비 절약
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
            "participation_rate": np.random.randint(70, 85)
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
    
    col1, col2, col3, col4 = st.columns(4)
    
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
            
            carbon_savings = {
                'stairs': stairs_usage * 0.05,
                'public_transport': public_transport * 0.3,
                'bicycle': bicycle_usage * 0.2
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
                "participation_rate": np.random.randint(70, 85)
            }
            st.success("샘플 데이터로 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📈 통계 새로고침", width='stretch'):
            st.info("통계 데이터를 새로고침했습니다!")
    
    with col3:
        if st.button("📋 탄소 리포트", width='stretch'):
            st.info("탄소 발자국 리포트를 생성했습니다!")

# 임직원 아이디어 페이지
elif menu == "임직원 아이디어":
    st.title("💡 임직원 아이디어")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("아이디어 제안")
        
        with st.form("idea_form"):
            title = st.text_input("제목", placeholder="아이디어 제목을 입력하세요")
            description = st.text_area("설명", placeholder="아이디어에 대한 자세한 설명을 입력하세요", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("카테고리", ["Scope 1", "Scope 2", "Scope 3", "순환경제", "기타"])
                department = st.selectbox("부서", ["IT개발팀", "시설관리팀", "구매팀", "환경팀", "마케팅팀", "인사팀"])
            with col2:
                priority = st.selectbox("우선순위", ["낮음", "보통", "높음"])
            
            submitted = st.form_submit_button("제안")
            if submitted:
                st.success(f"'{title}' 아이디어가 제안되었습니다!")
    
    with col2:
        st.subheader("요약")
        st.metric("총 아이디어", "127건")
        st.metric("구현된 아이디어", "15건")
        st.metric("총 좋아요", "342개")
        st.metric("구현률", "11.8%")
    
    # 인기 아이디어 TOP 3
    st.subheader("인기 아이디어 TOP 3")
    
    ideas_data = [
        {"title": "사무용 전기차 충전소 확대", "likes": 15, "category": "Scope 1", "status": "구현됨"},
        {"title": "스마트 조명 시스템 도입", "likes": 12, "category": "Scope 2", "status": "승인됨"},
        {"title": "공급업체 친환경 인증 제도", "likes": 18, "category": "Scope 3", "status": "검토중"}
    ]
    
    for i, idea in enumerate(ideas_data, 1):
        with st.expander(f"#{i} {idea['title']} (👍 {idea['likes']})"):
            st.write(f"**카테고리:** {idea['category']}")
            st.write(f"**상태:** {idea['status']}")
            st.write("**설명:** 해당 아이디어에 대한 상세 설명...")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌱 <strong>삼성SDS 탄소관리 시스템</strong> - 디지털 혁신으로 지속가능한 미래를 만들어갑니다</p>
</div>
""", unsafe_allow_html=True)
