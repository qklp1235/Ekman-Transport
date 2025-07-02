#!/usr/bin/env python3
"""
Streamlit 버전 Ekman Transport Visualizer
간단하고 빠른 웹 배포를 위한 Streamlit 앱
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from ekman_calculations import EkmanTransportCalculator
from translations import translations
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="🌊 Ekman Transport Visualizer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0078D4, #106EBE);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stMetric {
        background: linear-gradient(145deg, #f0f8ff, #e6f3ff);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #0078D4;
    }
    
    .result-box {
        background: linear-gradient(145deg, #fff5f5, #ffe6e6);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ff6b6b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1>🌊 Ekman Transport Visualizer</h1>
    <p>Interactive oceanographic visualization powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)

# 계산기 초기화
@st.cache_resource
def get_calculator():
    return EkmanTransportCalculator()

calc = get_calculator()

# 사이드바 컨트롤
st.sidebar.header("🎛️ Control Panel")

# 언어 선택
language = st.sidebar.selectbox(
    "🌍 Language",
    options=['en', 'ko', 'zh', 'ja', 'es', 'ru'],
    format_func=lambda x: {
        'en': 'English',
        'ko': '한국어', 
        'zh': '中文',
        'ja': '日本語',
        'es': 'Español',
        'ru': 'Русский'
    }[x]
)

# 번역 텍스트
t = translations[language]

# 파라미터 입력
st.sidebar.subheader("⚙️ Parameters")

wind_speed = st.sidebar.slider(
    f"💨 {t['wind_speed']} (m/s)",
    min_value=0.0,
    max_value=30.0,
    value=10.0,
    step=0.1
)

wind_direction = st.sidebar.slider(
    f"🧭 {t['wind_direction']} (°)",
    min_value=0,
    max_value=360,
    value=0,
    step=1
)

latitude = st.sidebar.slider(
    f"🌐 {t['latitude']} (°)",
    min_value=-90,
    max_value=90,
    value=30,
    step=1
)

depth = st.sidebar.slider(
    f"📏 {t['depth']} (m)",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

# 시각화 타입
vis_type = st.sidebar.radio(
    "📊 Visualization Type",
    options=['3d', '2d'],
    format_func=lambda x: '3D Visualization' if x == '3d' else '2D Analysis'
)

# 사전 설정
st.sidebar.subheader("⚡ Presets")
col1, col2, col3 = st.sidebar.columns(3)

if col1.button("Normal"):
    wind_speed = 10.0
    wind_direction = 0
    latitude = 30
    depth = 100

if col2.button("Strong"):
    wind_speed = 20.0
    wind_direction = 45
    latitude = 45
    depth = 150

if col3.button("Typhoon"):
    wind_speed = 30.0
    wind_direction = 90
    latitude = 25
    depth = 200

# 주요 위치들
st.sidebar.subheader("🗺️ Famous Locations")
location_presets = {
    'Custom': None,
    'Los Angeles': {'lat': 34.0, 'wind': 3.0, 'wind_dir': 270},
    'Busan': {'lat': 35.1, 'wind': 3.5, 'wind_dir': 135},
    'North Pacific': {'lat': 45.0, 'wind': 6.0, 'wind_dir': 135},
    'North Atlantic': {'lat': 50.0, 'wind': 8.0, 'wind_dir': 270},
    'Southern Ocean': {'lat': -60.0, 'wind': 11.0, 'wind_dir': 270},
}

selected_location = st.sidebar.selectbox("Select Location", list(location_presets.keys()))

if selected_location != 'Custom' and location_presets[selected_location]:
    loc = location_presets[selected_location]
    latitude = loc['lat']
    wind_speed = loc['wind']
    wind_direction = loc['wind_dir']

# 계산 실행
if st.sidebar.button("🌊 Calculate & Visualize", type="primary"):
    with st.spinner("Calculating Ekman transport..."):
        # 계산 수행
        results = calc.calculate_ekman_transport(wind_speed, wind_direction, latitude, depth)
        
        # 메인 화면에 결과 표시
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 시각화
            if vis_type == '3d':
                st.subheader("🎯 3D Ekman Transport Visualization")
                fig = calc.create_3d_visualization(results)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.subheader("📊 2D Analysis")
                fig = calc.create_2d_visualization(results)
                st.pyplot(fig)
        
        with col2:
            # 결과 패널
            st.subheader("📊 Results")
            
            # 주요 지표들
            st.metric(
                label="Wind Stress",
                value=f"{results['wind_stress']*1000:.2f} mN/m²"
            )
            
            st.metric(
                label="Ekman Depth", 
                value=f"{results['ekman_depth']:.1f} m"
            )
            
            total_transport = np.sqrt(results['Mx']**2 + results['My']**2)
            st.metric(
                label="Total Transport",
                value=f"{total_transport:.2e} m³/s"
            )
            
            st.metric(
                label="Energy Transfer",
                value=f"{results['energy_transfer_rate']*1000:.3f} mW/m²"
            )
            
            # 상세 결과 표
            st.subheader("📋 Detailed Results")
            results_df = pd.DataFrame({
                'Parameter': [
                    'Coriolis Parameter (f)',
                    'Wind Stress X',
                    'Wind Stress Y', 
                    'Transport X (Mx)',
                    'Transport Y (My)',
                    'Wind Speed',
                    'Wind Direction',
                    'Latitude',
                    'Depth'
                ],
                'Value': [
                    f"{results['f']:.2e} s⁻¹",
                    f"{results['tau_x']:.3f} N/m²",
                    f"{results['tau_y']:.3f} N/m²",
                    f"{results['Mx']:.3f} m²/s",
                    f"{results['My']:.3f} m²/s",
                    f"{results['wind_speed']:.1f} m/s",
                    f"{results['wind_direction']:.0f}°",
                    f"{results['latitude']:.0f}°",
                    f"{results['depth']:.0f} m"
                ]
            })
            
            st.dataframe(results_df, use_container_width=True)

# 하단 정보
st.markdown("---")

# 탭으로 추가 정보 구성
tab1, tab2, tab3, tab4 = st.tabs(["📚 About", "🔬 Science", "💡 Tips", "🌍 Languages"])

with tab1:
    st.markdown("""
    ### 🌊 About Ekman Transport Visualizer
    
    This interactive app demonstrates the **Ekman Transport** phenomenon in oceanography:
    
    - **Wind drives surface currents** through friction
    - **Coriolis effect** deflects the current 90° to the right (Northern Hemisphere) or left (Southern Hemisphere)
    - **Ekman spiral** shows how current direction changes with depth
    - **Transport vector** represents the net water movement
    
    Perfect for:
    - 🎓 Marine science education
    - 🔬 Research presentations  
    - 📊 Data visualization
    - 🌊 Understanding ocean dynamics
    """)

with tab2:
    st.markdown("""
    ### 🔬 Scientific Background
    
    **Ekman Transport** was first described by Swedish oceanographer Vagn Walfrid Ekman in 1905.
    
    #### Key Equations:
    - **Coriolis Parameter**: `f = 2Ω sin(φ)` where Ω is Earth's rotation rate
    - **Wind Stress**: `τ = ρₐ Cₐ U²` where ρₐ is air density, Cₐ is drag coefficient
    - **Ekman Transport**: `M = τ / (ρw f)` where ρw is water density
    - **Ekman Depth**: `D = π√(2K/f)` where K is eddy viscosity
    
    #### Physical Constants Used:
    - Water density: 1025 kg/m³
    - Air density: 1.225 kg/m³
    - Drag coefficient: 0.0013
    - Earth's rotation: 7.2921×10⁻⁵ rad/s
    """)

with tab3:
    st.markdown("""
    ### 💡 Usage Tips
    
    1. **Start with non-zero latitude** - Coriolis effect requires rotation
    2. **Notice the 90° deflection** - Transport is perpendicular to wind
    3. **Experiment with different latitudes** - Effect is strongest at poles
    4. **Try the presets** - Normal, Strong Wind, and Typhoon scenarios
    5. **Compare 3D and 2D views** - Each shows different aspects
    6. **Use famous locations** - See real-world examples
    
    #### Understanding the Visualization:
    - **Red arrow**: Wind direction and strength
    - **Blue/Green arrow**: Ekman transport direction
    - **Spiral**: How current changes with depth
    - **Numbers**: Quantitative results for analysis
    """)

with tab4:
    st.markdown("""
    ### 🌍 Language Support
    
    This app supports **6 languages**:
    
    - 🇺🇸 **English** - Primary language
    - 🇰🇷 **한국어** - Korean support
    - 🇨🇳 **中文** - Chinese Simplified
    - 🇯🇵 **日本語** - Japanese support  
    - 🇪🇸 **Español** - Spanish support
    - 🇷🇺 **Русский** - Russian support
    
    Change language in the sidebar to see all UI elements and labels in your preferred language.
    
    Perfect for international education and research collaboration! 🌐
    """)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌊 Ekman Transport Visualizer v4.8.1 | Made with ❤️ using Streamlit</p>
    <p>Educational tool for oceanographic science | Open source and free to use</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 하단 정보
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; font-size: 0.8em; color: #666;">
    <p>🌊 Streamlit Edition</p>
    <p>v4.8.1</p>
</div>
""", unsafe_allow_html=True) 