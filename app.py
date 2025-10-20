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
</style>
""", unsafe_allow_html=True)

# 사이드바 네비게이션
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <h2 style="color: white; margin: 0;">🌱 삼성SDS ESG</h2>
    <p style="color: #e0e0e0; margin: 0;">탄소관리 시스템</p>
</div>
""", unsafe_allow_html=True)

# 메뉴 선택
menu = st.sidebar.selectbox(
    "메뉴 선택",
    ["대시보드", "Scope 1 (직접 배출)", "Scope 2 (간접 배출)", "Scope 3 (밸류체인)", "순환경제", "임직원 아이디어"]
)

# 샘플 데이터 로드
@st.cache_data
def load_emission_data():
    """월별 배출량 데이터"""
    months = ['1월', '2월', '3월', '4월', '5월', '6월']
    scope1_data = [1200, 1100, 1000, 950, 900, 850]
    scope2_data = [800, 750, 700, 680, 650, 620]
    scope3_data = [2000, 1900, 1800, 1750, 1700, 1650]
    
    return pd.DataFrame({
        '월': months,
        'Scope 1': scope1_data,
        'Scope 2': scope2_data,
        'Scope 3': scope3_data
    })

@st.cache_data
def load_scope_data():
    """Scope별 배출량 비율"""
    return pd.DataFrame({
        'Scope': ['Scope 1', 'Scope 2', 'Scope 3'],
        '배출량': [850, 620, 1650],
        '비율': [27, 20, 53]
    })

@st.cache_data
def load_circular_economy_data():
    """순환경제 데이터"""
    return pd.DataFrame({
        '지표': ['재활용률', '매립 제로화', '자원 회수'],
        '현재값': [85, 100, 92],
        '목표값': [90, 100, 95]
    })

# 대시보드 페이지
if menu == "대시보드":
    st.markdown('<h1 class="main-header">📊 탄소관리 대시보드</h1>', unsafe_allow_html=True)
    
    # KPI 메트릭
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 배출량",
            value="3,120 tCO2e",
            delta="-15%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="재활용률",
            value="85%",
            delta="+5%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="매립 제로화",
            value="100%",
            delta="+5%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="제안된 아이디어",
            value="127",
            delta="+15",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 월별 온실가스 배출량 추이")
        emission_data = load_emission_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=emission_data['월'], y=emission_data['Scope 1'], 
                               mode='lines+markers', name='Scope 1', line=dict(color='#8884d8')))
        fig.add_trace(go.Scatter(x=emission_data['월'], y=emission_data['Scope 2'], 
                               mode='lines+markers', name='Scope 2', line=dict(color='#82ca9d')))
        fig.add_trace(go.Scatter(x=emission_data['월'], y=emission_data['Scope 3'], 
                               mode='lines+markers', name='Scope 3', line=dict(color='#ffc658')))
        
        fig.update_layout(
            xaxis_title="월",
            yaxis_title="배출량 (tCO2e)",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Scope별 배출량 비율")
        scope_data = load_scope_data()
        
        fig = px.pie(scope_data, values='배출량', names='Scope', 
                    color_discrete_sequence=['#8884d8', '#82ca9d', '#ffc658'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # 순환경제 지표
    st.subheader("♻️ 순환경제 달성률")
    circular_data = load_circular_economy_data()
    
    col1, col2, col3 = st.columns(3)
    for i, (idx, row) in enumerate(circular_data.iterrows()):
        with [col1, col2, col3][i]:
            progress = row['현재값'] / row['목표값']
            st.progress(progress)
            st.write(f"**{row['지표']}**")
            st.write(f"현재: {row['현재값']}% / 목표: {row['목표값']}%")

# Scope 1 페이지
elif menu == "Scope 1 (직접 배출)":
    st.title("🏭 Scope 1 - 직접 배출량 관리")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("배출량 등록")
        
        with st.form("scope1_form"):
            col1, col2 = st.columns(2)
            with col1:
                source = st.selectbox("배출원", ["사무용 차량", "보일러", "발전기", "기타"])
                emission_type = st.selectbox("배출 유형", ["연료 연소", "공정 배출", "냉매 누출", "기타 직접 배출"])
            with col2:
                amount = st.number_input("배출량 (tCO2e)", min_value=0.0, value=0.0, step=0.1)
                location = st.text_input("위치", value="본사")
            
            submitted = st.form_submit_button("등록")
            if submitted:
                st.success(f"{source} 배출량 {amount} tCO2e가 등록되었습니다!")
    
    with col2:
        st.subheader("요약")
        st.metric("총 배출량", "850 tCO2e")
        st.metric("등록된 기록", "15건")
        st.metric("전년 대비", "-12%")
        st.metric("목표 달성률", "85%")
    
    # 배출 유형별 차트
    st.subheader("배출 유형별 현황")
    emission_types = ['연료 연소', '공정 배출', '냉매 누출', '기타']
    values = [243.7, 45.2, 12.8, 8.5]
    
    fig = px.bar(x=emission_types, y=values, 
                color=values, color_continuous_scale='Blues')
    fig.update_layout(xaxis_title="배출 유형", yaxis_title="배출량 (tCO2e)")
    st.plotly_chart(fig, use_container_width=True)

# Scope 2 페이지
elif menu == "Scope 2 (간접 배출)":
    st.title("⚡ Scope 2 - 간접 배출량 관리")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("에너지 사용량 등록")
        
        with st.form("scope2_form"):
            col1, col2 = st.columns(2)
            with col1:
                energy_type = st.selectbox("에너지 유형", ["전력", "냉난방", "증기", "기타 에너지"])
                supplier = st.text_input("공급원", value="한국전력공사")
            with col2:
                amount = st.number_input("사용량 (kWh)", min_value=0, value=0, step=1)
                renewable = st.checkbox("재생에너지")
            
            submitted = st.form_submit_button("등록")
            if submitted:
                energy_type_text = "재생에너지" if renewable else "일반에너지"
                st.success(f"{energy_type} {amount} kWh ({energy_type_text})가 등록되었습니다!")
    
    with col2:
        st.subheader("요약")
        st.metric("총 에너지 사용량", "22,500 kWh")
        st.metric("재생에너지 비율", "35.1%")
        st.metric("전년 대비", "-8%")
        st.metric("목표 달성률", "92%")
    
    # 월별 에너지 사용량 추이
    st.subheader("월별 에너지 사용량 추이")
    months = ['1월', '2월', '3월', '4월', '5월', '6월']
    total_usage = [22000, 21000, 20000, 19500, 19000, 18500]
    renewable_usage = [5000, 4800, 5200, 5500, 6000, 6500]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=total_usage, mode='lines+markers', 
                            name='총 사용량', line=dict(color='#8884d8')))
    fig.add_trace(go.Scatter(x=months, y=renewable_usage, mode='lines+markers', 
                            name='재생에너지', line=dict(color='#82ca9d')))
    
    fig.update_layout(xaxis_title="월", yaxis_title="사용량 (kWh)", height=400)
    st.plotly_chart(fig, use_container_width=True)

# Scope 3 페이지
elif menu == "Scope 3 (밸류체인)":
    st.title("🌐 Scope 3 - 밸류체인 배출량 관리")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("배출량 등록")
        
        with st.form("scope3_form"):
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("카테고리", ["구매 상품 및 서비스", "운송 및 배송", "출장", "폐기물 처리", "임직원 출퇴근"])
                activity = st.text_input("활동", value="IT 장비 구매")
            with col2:
                amount = st.number_input("배출량 (tCO2e)", min_value=0.0, value=0.0, step=0.1)
                supplier = st.text_input("공급업체", value="삼성전자")
            
            submitted = st.form_submit_button("등록")
            if submitted:
                st.success(f"{category} - {activity} 배출량 {amount} tCO2e가 등록되었습니다!")
    
    with col2:
        st.subheader("요약")
        st.metric("총 배출량", "3,120 tCO2e")
        st.metric("활성 배출량", "2,100 tCO2e")
        st.metric("감축된 배출량", "1,020 tCO2e")
        st.metric("감축률", "32.7%")
    
    # 카테고리별 배출량
    st.subheader("카테고리별 배출량")
    categories = ['구매 상품 및 서비스', '운송 및 배송', '출장', '폐기물 처리', '임직원 출퇴근']
    values = [450.2, 320.5, 180.3, 95.8, 120.5]
    
    fig = px.bar(x=categories, y=values, 
                color=values, color_continuous_scale='Oranges')
    fig.update_layout(xaxis_title="카테고리", yaxis_title="배출량 (tCO2e)")
    fig.update_xaxis(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

# 순환경제 페이지
elif menu == "순환경제":
    st.title("♻️ 순환경제 관리")
    
    # 매립 제로화 알림
    st.success("🎉 매립 제로화 달성! 모든 폐기물이 재활용되거나 친환경적으로 처리되고 있습니다.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("폐기물 등록")
        
        with st.form("waste_form"):
            col1, col2 = st.columns(2)
            with col1:
                waste_type = st.selectbox("폐기물 유형", ["종이", "플라스틱", "전자폐기물", "음식물 쓰레기", "유리", "금속"])
                disposal_method = st.selectbox("처리 방법", ["재활용", "퇴비화", "에너지 회수", "매립"])
            with col2:
                amount = st.number_input("양 (kg)", min_value=0, value=0, step=1)
                recycling_rate = st.slider("재활용률 (%)", 0, 100, 85)
            
            submitted = st.form_submit_button("등록")
            if submitted:
                st.success(f"{waste_type} {amount} kg ({disposal_method})가 등록되었습니다!")
    
    with col2:
        st.subheader("요약")
        st.metric("총 폐기물", "4,020 kg")
        st.metric("재활용률", "85.0%")
        st.metric("매립 제로화", "100%")
        st.metric("자원 회수", "92%")
    
    # 폐기물 처리 방법별 비율
    st.subheader("폐기물 처리 방법별 비율")
    methods = ['재활용', '퇴비화', '에너지 회수', '매립']
    values = [3420, 600, 200, 0]
    colors = ['#82ca9d', '#8884d8', '#ffc658', '#ff7300']
    
    fig = px.pie(values=values, names=methods, color_discrete_sequence=colors)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

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
