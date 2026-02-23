import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
import pathlib
import os

st.set_page_config(
    page_title="Brentford FC | Scouting Intelligence",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# GLASS BACKGROUND FUNCTION
# ============================================
def add_glass_background():
    """إضافة خلفية زجاجية مع صورة الاستاد"""
    
    # البحث عن صورة الخلفية
    bg_paths = [
        "assets/bg_stadium.jpg",
        "bg_stadium.jpg",
        "./assets/bg_stadium.jpg",
        "assets/bg_stadium.jpeg",
        "stadium_bg.jpg"
    ]
    
    bg_b64 = None
    for path in bg_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                bg_b64 = base64.b64encode(f.read()).decode()
            break
    
    if bg_b64:
        glass_style = f"""
        <style>
            /* Stadium Background */
            .stadium-bg {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background-image: url('data:image/jpeg;base64,{bg_b64}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                filter: blur(8px) brightness(0.3) saturate(1.2);
                transform: scale(1.05);
                z-index: -2;
                animation: slowZoom 40s infinite alternate ease-in-out;
            }}
            
            @keyframes slowZoom {{
                0% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1.12); }}
            }}
            
            /* Glass Overlay */
            .glass-overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: radial-gradient(circle at 50% 50%, 
                    rgba(10, 10, 10, 0.2) 0%, 
                    rgba(0, 0, 0, 0.7) 80%,
                    rgba(0, 0, 0, 0.9) 100%);
                backdrop-filter: blur(4px);
                -webkit-backdrop-filter: blur(4px);
                z-index: -1;
            }}
            
            /* Glass Card Effect */
            .glass-card {{
                background: rgba(20, 20, 20, 0.6);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(224, 58, 62, 0.25);
                border-radius: 12px;
                padding: 1.2rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            }}
            
            .glass-card:hover {{
                background: rgba(30, 30, 30, 0.7);
                border-color: #e03a3e;
                box-shadow: 0 8px 25px rgba(224, 58, 62, 0.2);
                transform: translateY(-2px);
            }}
            
            /* Main Container */
            .main-container {{
                position: relative;
                z-index: 1;
            }}
            
            /* Header Glass */
            .header-wrap {{
                background: rgba(10, 10, 10, 0.7) !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border: 1px solid rgba(224, 58, 62, 0.3) !important;
                border-radius: 16px !important;
                padding: 2rem 2.5rem !important;
                margin-bottom: 1.5rem !important;
                position: relative !important;
                overflow: hidden !important;
                display: flex !important;
                align-items: center !important;
                gap: 2rem !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
            }}
            
            .header-wrap::before {{
                content: '';
                position: absolute;
                top: -80px;
                right: -60px;
                width: 350px;
                height: 350px;
                background: radial-gradient(circle, rgba(224, 58, 62, 0.15) 0%, transparent 70%);
                pointer-events: none;
            }}
            
            /* Sidebar Glass */
            [data-testid="stSidebar"] {{
                background: rgba(15, 15, 15, 0.7) !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border-right: 1px solid rgba(224, 58, 62, 0.25) !important;
            }}
            
            /* KPI Cards Glass */
            .kpi-card {{
                background: rgba(26, 26, 26, 0.6) !important;
                backdrop-filter: blur(8px) !important;
                -webkit-backdrop-filter: blur(8px) !important;
                border: 1px solid rgba(224, 58, 62, 0.2) !important;
                border-radius: 12px !important;
                padding: 1.1rem 1.3rem !important;
                position: relative !important;
                overflow: hidden !important;
                transition: all 0.3s ease !important;
            }}
            
            .kpi-card:hover {{
                background: rgba(40, 40, 40, 0.7) !important;
                border-color: #e03a3e !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(224, 58, 62, 0.15) !important;
            }}
            
            /* Player Cards Glass */
            .pcard {{
                background: rgba(26, 26, 26, 0.5) !important;
                backdrop-filter: blur(8px) !important;
                -webkit-backdrop-filter: blur(8px) !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                border-radius: 12px !important;
                padding: 1.1rem 1.3rem !important;
                margin-bottom: 0.7rem !important;
                transition: all 0.3s ease !important;
            }}
            
            .pcard:hover {{
                background: rgba(40, 40, 40, 0.6) !important;
                border-color: rgba(224, 58, 62, 0.4) !important;
                box-shadow: 0 8px 20px rgba(224, 58, 62, 0.1) !important;
                transform: translateX(5px) !important;
            }}
            
            /* Tabs Glass */
            [data-testid="stTabs"] {{
                background: rgba(20, 20, 20, 0.3) !important;
                backdrop-filter: blur(8px) !important;
                -webkit-backdrop-filter: blur(8px) !important;
                border-radius: 12px !important;
                padding: 0.5rem !important;
            }}
            
            /* Footer Glass */
            .footer {{
                background: rgba(10, 10, 10, 0.5) !important;
                backdrop-filter: blur(8px) !important;
                -webkit-backdrop-filter: blur(8px) !important;
                text-align: center !important;
                padding: 2rem 0 1rem !important;
                color: #999 !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 0.68rem !important;
                letter-spacing: 1.5px !important;
                text-transform: uppercase !important;
                border-top: 1px solid rgba(224, 58, 62, 0.15) !important;
                margin-top: 3rem !important;
            }}
        </style>
        
        <div class="stadium-bg"></div>
        <div class="glass-overlay"></div>
        <div class="main-container">
        """
        
        st.markdown(glass_style, unsafe_allow_html=True)
        return True
    else:
        # CSS احتياطي لو الصورة مش موجودة
        fallback_style = """
        <style>
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%) !important;
            }
            .glass-card, .kpi-card, .pcard {
                background: rgba(26, 26, 26, 0.8) !important;
                backdrop-filter: blur(8px) !important;
            }
        </style>
        """
        st.markdown(fallback_style, unsafe_allow_html=True)
        return False

# ============================================
# CALL GLASS BACKGROUND
# ============================================
add_glass_background()

def load_css():
    css_path = pathlib.Path("assets/style.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ============================================
# NORMALIZATION FUNCTIONS
# ============================================
def normalize_col(col):
    """تطبيع العمود ليكون بين 0 و 1"""
    if col is None or len(col) == 0:
        return pd.Series([])
    
    col = pd.to_numeric(col, errors='coerce').fillna(0)
    mn, mx = col.min(), col.max()
    
    if mx == mn or mx == 0:
        return pd.Series([0.5] * len(col))
    
    return (col - mn) / (mx - mn)

def recalculate(df):
    """إعادة حساب المؤشرات"""
    if df.empty:
        return df
    
    df = df.copy()
    
    # التأكد من وجود الأعمدة
    required_cols = ['Gls_p90', 'SoT%', 'Ast', 'PrgP_proxy', 'Scoring_Context_Bonus', 'Market_Value_M', 'Age_num', '90s']
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0
    
    # تنظيف البيانات
    df['SoT%'] = pd.to_numeric(df['SoT%'], errors='coerce').fillna(0)
    df['Gls_p90'] = pd.to_numeric(df['Gls_p90'], errors='coerce').fillna(0)
    df['Ast'] = pd.to_numeric(df['Ast'], errors='coerce').fillna(0)
    df['PrgP_proxy'] = pd.to_numeric(df['PrgP_proxy'], errors='coerce').fillna(0)
    df['Scoring_Context_Bonus'] = pd.to_numeric(df['Scoring_Context_Bonus'], errors='coerce').fillna(0)
    df['Market_Value_M'] = pd.to_numeric(df['Market_Value_M'], errors='coerce').fillna(0)
    df['Age_num'] = pd.to_numeric(df['Age_num'], errors='coerce').fillna(25)
    df['90s'] = pd.to_numeric(df['90s'], errors='coerce').fillna(0)
    
    # تطبيع المؤشرات
    df['norm_gls_p90'] = normalize_col(df['Gls_p90'])
    df['norm_sot_pct'] = normalize_col(df['SoT%'])
    df['norm_ast'] = normalize_col(df['Ast'])
    df['norm_prgp'] = normalize_col(df['PrgP_proxy'])
    df['norm_context'] = normalize_col(df['Scoring_Context_Bonus'])
    
    # حساب الدرجات
    df['Perf_Score'] = (
        df['norm_gls_p90'] * 0.30 + 
        df['norm_sot_pct'] * 0.18 + 
        df['norm_ast'] * 0.22 + 
        df['norm_prgp'] * 0.18 + 
        df['norm_context'] * 0.12
    ).round(3)
    
    df['Value_Score'] = df.apply(
        lambda row: (row['Perf_Score'] / max(row['Market_Value_M'], 0.1) * 100) if row['Market_Value_M'] > 0 else 0, 
        axis=1
    ).round(3)
    
    df['Value_Score_norm'] = normalize_col(df['Value_Score']) * 100
    df['Value_Score_norm'] = df['Value_Score_norm'].round(1)
    
    df['Age_bonus'] = df['Age_num'].apply(
        lambda x: 1.2 if x <= 23 else (1.1 if x <= 25 else 1.0)
    )
    
    df['Final_Score'] = (df['Value_Score_norm'] * df['Age_bonus']).round(1)
    
    return df

@st.cache_data
def load_data(file=None):
    """تحميل البيانات من CSV"""
    try:
        if file is not None:
            df = pd.read_csv(file)
            st.success(f"✅ تم تحميل الملف: {file.name}")
        else:
            # البحث عن ملف البيانات
            possible_paths = [
                "data/processed/lique1_final.csv",
                "data/processed/ligue1_final.csv",
                "lique1_final.csv",
                "ligue1_final.csv",
                "./data/processed/lique1_final.csv"
            ]
            
            df = None
            for path in possible_paths:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    st.success(f"✅ تم تحميل البيانات من {path}")
                    break
            
            if df is None:
                # استخدام البيانات الحقيقية من الملف
                st.info("📊 جاري تحميل بيانات Ligue 1...")
                # هنا هنضيف البيانات الكاملة من الـ CSV
                # بس مؤقتاً هنستخدم البيانات التجريبية
                data = {
                    'Player': ['أوباميانج', 'فاتي', 'توماسون', 'هاين', 'موريرا'],
                    'Nation': ['GAB', 'ESP', 'FRA', 'FRA', 'POR'],
                    'Pos_primary': ['FW', 'MF', 'MF', 'MF', 'MF'],
                    'Squad': ['مرسيليا', 'موناكو', 'لنس', 'ميتز', 'ليون'],
                    'Age_num': [36, 23, 32, 29, 20],
                    'League': ['Ligue 1', 'Ligue 1', 'Ligue 1', 'Ligue 1', 'Ligue 1'],
                    '90s': [13.6, 6.4, 21.3, 17.7, 11.2],
                    'Gls': [6, 8, 2, 6, 2],
                    'Ast': [5, 0, 6, 4, 6],
                    'Gls_p90': [0.44, 1.25, 0.09, 0.34, 0.18],
                    'SoT%': [61.3, 58.3, 28.6, 33.3, 34.8],
                    'Market_Value_M': [4, 6, 5, 5, 8],
                    'Defense_Hardness': [0.59, 0.41, 0.69, 0.0, 0.72]
                }
                df = pd.DataFrame(data)
        
        return recalculate(df)
        
    except Exception as e:
        st.error(f"❌ خطأ في تحميل البيانات: {str(e)}")
        # بيانات احتياطية
        data = {'Player': ['خطأ'], 'Age_num': [25], 'Gls': [0], 'Ast': [0], 
                'Gls_p90': [0], 'SoT%': [0], 'Market_Value_M': [1], '90s': [1]}
        df = pd.DataFrame(data)
        return recalculate(df)

def img_to_b64(path):
    """تحويل الصورة إلى base64"""
    try:
        possible_paths = [
            path,
            "assets/rentford_logo.jpg",
            "assets/brentford_logo.png",
            "rentford_logo.jpg",
            "brentford_logo.png",
            "assets/brentford_logo.jpg"
        ]
        
        for p in possible_paths:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode()
        return None
    except:
        return None

# ============================================
# HEADER
# ============================================
logo_b64 = img_to_b64("assets/rentford_logo.jpg")
logo_html = f'<img class="header-logo" src="data:image/jpeg;base64,{logo_b64}"/>' if logo_b64 else '<div style="font-size:3rem;flex-shrink:0;">⚽</div>'

st.markdown(f"""
<div class="header-wrap">
    {logo_html}
    <div>
        <div class="main-title">BRENTFORD FC <span>//</span> SCOUTING INTEL</div>
        <div class="main-sub">UNDERVALUED PLAYER DETECTION • VALUE SCORE ALGORITHM • SCHEDULE-ADJUSTED ANALYTICS</div>
        <div class="social-links">
            <a class="social-btn" href="https://www.linkedin.com/in/goda-emad/" target="_blank">🔗 LinkedIn</a>
            <a class="social-btn" href="https://github.com/Goda-Emad/brentford-scouting" target="_blank">🐙 GitHub</a>
            <a class="social-btn" href="tel:+201126242932">📞 +20 112 624 2932</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
# TAB 2: Value Analysis - نسخة مطورة مع Glass Cards وتحليلات أعمق
with tab2:
    st.markdown('<div class="sec-title">VALUE ANALYSIS</div>', unsafe_allow_html=True)
    
    if len(df) > 1:
        # ============================================
        # TOP STATS CARDS
        # ============================================
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        # أفضل Value Score
        best_value_idx = df['Final_Score'].idxmax()
        best_player = df.loc[best_value_idx, 'Player']
        best_score = df['Final_Score'].max()
        
        with col_stats1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:1rem;">
                <div style="font-size:0.7rem; color:var(--muted);">🏆 BEST VALUE</div>
                <div style="font-size:1.5rem; color:var(--red); font-family:'Bebas Neue';">{best_score:.0f}</div>
                <div style="font-size:0.8rem;">{best_player}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # أعلى قيمة سوقية
        high_value_idx = df['Market_Value_M'].idxmax()
        high_value_player = df.loc[high_value_idx, 'Player']
        high_value = df['Market_Value_M'].max()
        
        with col_stats2:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:1rem;">
                <div style="font-size:0.7rem; color:var(--muted);">💰 HIGHEST VALUE</div>
                <div style="font-size:1.5rem; color:white; font-family:'Bebas Neue';">€{high_value:.0f}M</div>
                <div style="font-size:0.8rem;">{high_value_player}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # أفضل قيمة مقابل سعر
        value_for_money = (df['Final_Score'] / df['Market_Value_M']).idxmax()
        vfm_player = df.loc[value_for_money, 'Player']
        vfm_ratio = (df.loc[value_for_money, 'Final_Score'] / df.loc[value_for_money, 'Market_Value_M']).round(1)
        
        with col_stats3:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:1rem;">
                <div style="font-size:0.7rem; color:var(--muted);">⚡ VALUE/MONEY</div>
                <div style="font-size:1.5rem; color:#7ed321; font-family:'Bebas Neue';">{vfm_ratio}</div>
                <div style="font-size:0.8rem;">{vfm_player}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # متوسط الدرجات
        avg_score = df['Final_Score'].mean()
        
        with col_stats4:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:1rem;">
                <div style="font-size:0.7rem; color:var(--muted);">📊 AVG SCORE</div>
                <div style="font-size:1.5rem; color:#f5a623; font-family:'Bebas Neue';">{avg_score:.1f}</div>
                <div style="font-size:0.8rem;">{len(df)} Players</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================
        # MAIN CHARTS
        # ============================================
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot محسن
            fig = px.scatter(
                df, 
                x='Market_Value_M', 
                y='Final_Score', 
                hover_name='Player',
                hover_data={
                    'Squad': True,
                    'Age_num': True,
                    'Gls': True,
                    'Ast': True,
                    'Market_Value_M': ':.1f',
                    'Final_Score': ':.1f'
                },
                color='Pos_primary',
                size='Gls',
                size_max=25,
                color_discrete_map={
                    'FW': '#e03a3e',
                    'MF': '#f5a623', 
                    'DF': '#4a90e2'
                },
                title='🎯 Value Score vs Market Value',
                labels={
                    'Market_Value_M': 'Market Value (€ million)',
                    'Final_Score': 'Value Score',
                    'Pos_primary': 'Position'
                }
            )
            
            # تحسين شكل الرسم
            fig.update_layout(
                plot_bgcolor='rgba(20,20,20,0.3)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e8e8e8', family='Inter', size=11),
                title_font=dict(color='white', family='Bebas Neue', size=24),
                legend=dict(
                    bgcolor='rgba(20,20,20,0.6)',
                    bordercolor='rgba(224,58,62,0.2)',
                    borderwidth=1,
                    font=dict(color='#e8e8e8')
                ),
                hoverlabel=dict(
                    bgcolor='#1a1a1a',
                    font_size=12,
                    font_family='Inter'
                ),
                margin=dict(t=50, b=30, l=10, r=10),
                height=450
            )
            
            # إضافة خطوط المساعدة
            fig.update_xaxes(
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.1)'
            )
            fig.update_yaxes(
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.1)'
            )
            
            # إضافة منطقة برينتفورد المستهدفة
            fig.add_shape(
                type='rect',
                x0=0,
                y0=50,
                x1=df['Market_Value_M'].quantile(0.3),
                y1=df['Final_Score'].max(),
                line=dict(color='rgba(224,58,62,0.3)', width=1, dash='dash'),
                fillcolor='rgba(224,58,62,0.05)'
            )
            
            fig.add_annotation(
                x=df['Market_Value_M'].quantile(0.15),
                y=df['Final_Score'].max() * 0.95,
                text="🎯 Brentford Target Zone",
                font=dict(color='rgba(224,58,62,0.8)', size=10, family='Inter'),
                showarrow=False,
                bgcolor='rgba(20,20,20,0.6)',
                bordercolor='rgba(224,58,62,0.3)',
                borderwidth=1,
                borderpad=4
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top Players Bar Chart محسن
            top_players = df.head(10).copy()
            
            fig2 = go.Figure()
            
            # إضافة الأشرطة
            fig2.add_trace(go.Bar(
                x=top_players['Final_Score'],
                y=top_players['Player'],
                orientation='h',
                marker=dict(
                    color=top_players['Final_Score'],
                    colorscale=[[0, '#330000'], [0.5, '#8b1a1a'], [1, '#e03a3e']],
                    showscale=False,
                    line=dict(color='rgba(224,58,62,0.5)', width=1)
                ),
                text=[f"€{v:.0f}M | ⚽{int(g)}G" for v, g in zip(top_players['Market_Value_M'], top_players['Gls'])],
                textposition='outside',
                textfont=dict(color='#aaa', size=10, family='Inter'),
                hovertemplate='<b>%{y}</b><br>' +
                              'Score: %{x:.1f}<br>' +
                              'Value: €%{customdata[0]:.0f}M<br>' +
                              'Goals: %{customdata[1]}<br>' +
                              'Age: %{customdata[2]}' +
                              '<extra></extra>',
                customdata=top_players[['Market_Value_M', 'Gls', 'Age_num']]
            ))
            
            fig2.update_layout(
                plot_bgcolor='rgba(20,20,20,0.3)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e8e8e8', family='Inter', size=11),
                title=dict(
                    text='📊 Top 10 Players by Value Score',
                    font=dict(color='white', family='Bebas Neue', size=24)
                ),
                xaxis=dict(
                    title='Value Score',
                    gridcolor='rgba(255,255,255,0.05)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    autorange='reversed',
                    gridcolor='rgba(255,255,255,0.05)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(size=11, family='Bebas Neue')
                ),
                margin=dict(t=50, b=30, l=120, r=50),
                height=450,
                showlegend=False
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # ============================================
        # EFFICIENCY ANALYSIS
        # ============================================
        st.markdown('<div class="sec-title">⚡ EFFICIENCY ANALYSIS</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Goals Efficiency
            fig3 = px.scatter(
                df,
                x='Gls_p90',
                y='SoT%',
                hover_name='Player',
                hover_data={
                    'Squad': True,
                    'Gls': True,
                    'Ast': True,
                    'Market_Value_M': ':.1f'
                },
                color='Final_Score',
                size='Market_Value_M',
                size_max=25,
                color_continuous_scale=[[0, '#330000'], [0.5, '#8b1a1a'], [1, '#e03a3e']],
                title='🎯 Scoring Efficiency (Goals/90 vs Shot Accuracy)',
                labels={
                    'Gls_p90': 'Goals per 90 Minutes',
                    'SoT%': 'Shot on Target %',
                    'Final_Score': 'Value Score'
                }
            )
            
            fig3.update_layout(
                plot_bgcolor='rgba(20,20,20,0.3)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e8e8e8', family='Inter', size=11),
                title_font=dict(color='white', family='Bebas Neue', size=20),
                coloraxis_colorbar=dict(
                    title='Score',
                    tickfont=dict(color='#aaa'),
                    bgcolor='rgba(20,20,20,0.6)'
                ),
                margin=dict(t=50, b=30, l=10, r=10),
                height=400
            )
            
            # إضافة خطوط المتوسط
            avg_gls = df['Gls_p90'].mean()
            avg_sot = df['SoT%'].mean()
            
            fig3.add_hline(y=avg_sot, line_dash="dash", line_color="rgba(255,255,255,0.2)")
            fig3.add_vline(x=avg_gls, line_dash="dash", line_color="rgba(255,255,255,0.2)")
            
            fig3.add_annotation(
                x=df['Gls_p90'].max() * 0.8,
                y=df['SoT%'].max() * 0.9,
                text="💪 Elite Finishers",
                font=dict(color='#7ed321', size=10),
                showarrow=False
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            # Age vs Value Analysis
            fig4 = px.scatter(
                df,
                x='Age_num',
                y='Final_Score',
                hover_name='Player',
                hover_data={
                    'Squad': True,
                    'Market_Value_M': ':.1f',
                    'Gls': True,
                    'Ast': True
                },
                color='Market_Value_M',
                size='Gls',
                size_max=20,
                color_continuous_scale=[[0, '#330000'], [0.5, '#8b1a1a'], [1, '#e03a3e']],
                title='📈 Age Profile & Value Score',
                labels={
                    'Age_num': 'Age',
                    'Final_Score': 'Value Score',
                    'Market_Value_M': 'Market Value (€M)'
                }
            )
            
            fig4.update_layout(
                plot_bgcolor='rgba(20,20,20,0.3)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e8e8e8', family='Inter', size=11),
                title_font=dict(color='white', family='Bebas Neue', size=20),
                coloraxis_colorbar=dict(
                    title='Value (€M)',
                    tickfont=dict(color='#aaa'),
                    bgcolor='rgba(20,20,20,0.6)'
                ),
                margin=dict(t=50, b=30, l=10, r=10),
                height=400
            )
            
            # إضافة مناطق الأعمار
            fig4.add_vrect(x0="18", x1="23", 
                          fillcolor="rgba(126,211,33,0.1)", 
                          line_width=0,
                          annotation_text="🟢 U23", 
                          annotation_position="top left")
            fig4.add_vrect(x0="23", x1="28", 
                          fillcolor="rgba(245,166,35,0.1)", 
                          line_width=0,
                          annotation_text="🟡 Prime", 
                          annotation_position="top left")
            fig4.add_vrect(x0="28", x1="40", 
                          fillcolor="rgba(224,58,62,0.1)", 
                          line_width=0,
                          annotation_text="🔴 Veteran", 
                          annotation_position="top left")
            
            st.plotly_chart(fig4, use_container_width=True)
        
        # ============================================
        # SCHEDULE DIFFICULTY (إذا كانت موجودة)
        # ============================================
        if 'Defense_Hardness' in df.columns and 'Squad' in df.columns:
            st.markdown('<div class="sec-title">📅 SCHEDULE DIFFICULTY</div>', unsafe_allow_html=True)
            
            # تجميع حسب الفريق
            squad_hardness = df.groupby('Squad').agg({
                'Defense_Hardness': 'mean',
                'Player': 'count',
                'Final_Score': 'mean'
            }).reset_index().sort_values('Defense_Hardness', ascending=True)
            
            fig5 = go.Figure()
            
            fig5.add_trace(go.Bar(
                x=squad_hardness['Defense_Hardness'],
                y=squad_hardness['Squad'],
                orientation='h',
                marker=dict(
                    color=squad_hardness['Defense_Hardness'],
                    colorscale=[[0, '#7ed321'], [0.5, '#f5a623'], [1, '#e03a3e']],
                    showscale=False,
                    line=dict(color='white', width=1)
                ),
                text=[f"{h:.2f} | {c} players" for h, c in zip(squad_hardness['Defense_Hardness'], squad_hardness['Player'])],
                textposition='outside',
                textfont=dict(color='#aaa', size=10),
                hovertemplate='<b>%{y}</b><br>' +
                              'Hardness: %{x:.2f}<br>' +
                              'Players: %{customdata[0]}<br>' +
                              'Avg Score: %{customdata[1]:.1f}' +
                              '<extra></extra>',
                customdata=squad_hardness[['Player', 'Final_Score']]
            ))
            
            fig5.update_layout(
                plot_bgcolor='rgba(20,20,20,0.3)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e8e8e8', family='Inter', size=11),
                title=dict(
                    text='Defense Hardness by Squad (Higher = Harder to Score)',
                    font=dict(color='white', family='Bebas Neue', size=20)
                ),
                xaxis=dict(
                    title='Defense Hardness Score',
                    gridcolor='rgba(255,255,255,0.05)',
                    range=[0, 1]
                ),
                yaxis=dict(
                    title='',
                    gridcolor='rgba(255,255,255,0.05)'
                ),
                margin=dict(t=50, b=30, l=120, r=50),
                height=400
            )
            
            st.plotly_chart(fig5, use_container_width=True)
            
            # شرح مختصر
            st.markdown("""
            <div style="background:rgba(20,20,20,0.4); border-radius:8px; padding:1rem; margin-top:1rem;">
                <p style="color:#aaa; font-size:0.8rem;">
                📌 <strong>Defense Hardness</strong>: مقياس لصعوبة المواجهات الدفاعية (كلما زاد الرقم، زادت صعوبة التسجيل)
                </p>
                <ul style="color:#aaa; font-size:0.75rem;">
                    <li>🟢 < 0.4 : دفاعات سهلة</li>
                    <li>🟡 0.4 - 0.6 : دفاعات متوسطة</li>
                    <li>🔴 > 0.6 : دفاعات صعبة</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # ============================================
        # KEY INSIGHTS
        # ============================================
        st.markdown('<div class="sec-title">💡 KEY INSIGHTS</div>', unsafe_allow_html=True)
        
        insights_col1, insights_col2, insights_col3 = st.columns(3)
        
        with insights_col1:
            best_u23 = df[df['Age_num'] <= 23].sort_values('Final_Score', ascending=False).head(1)
            if not best_u23.empty:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color:#7ed321; margin:0;">🌟 Best Young Talent</h4>
                    <p style="font-size:1.2rem; margin:0.5rem 0;">{best_u23.iloc[0]['Player']}</p>
                    <p style="color:#aaa;">Age {int(best_u23.iloc[0]['Age_num'])} | Score: {best_u23.iloc[0]['Final_Score']:.0f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with insights_col2:
            best_value = df.sort_values('Value_Score', ascending=False).head(1)
            if not best_value.empty:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color:#f5a623; margin:0;">💰 Best Value for Money</h4>
                    <p style="font-size:1.2rem; margin:0.5rem 0;">{best_value.iloc[0]['Player']}</p>
                    <p style="color:#aaa;">€{best_value.iloc[0]['Market_Value_M']:.0f}M | Score: {best_value.iloc[0]['Final_Score']:.0f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with insights_col3:
            top_scorer = df.sort_values('Gls', ascending=False).head(1)
            if not top_scorer.empty:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color:#e03a3e; margin:0;">⚽ Top Goalscorer</h4>
                    <p style="font-size:1.2rem; margin:0.5rem 0;">{top_scorer.iloc[0]['Player']}</p>
                    <p style="color:#aaa;">{int(top_scorer.iloc[0]['Gls'])} Goals | {top_scorer.iloc[0]['SoT%']:.0f}% Acc</p>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.info("📊 هناك حاجة إلى المزيد من البيانات للرسوم البيانية")
# TAB 3: Player Deep Dive - نسخة متطورة مع رادار تشارت وتحليلات شاملة
with tab3:
    st.markdown('<div class="sec-title">🔬 PLAYER DEEP DIVE</div>', unsafe_allow_html=True)
    
    if len(df) > 0:
        # ============================================
        # PLAYER SELECTION WITH METRICS
        # ============================================
        col_select, col_metrics = st.columns([2, 1])
        
        with col_select:
            all_players = df['Player'].tolist()
            
            # إضافة فلتر البحث
            search_term = st.text_input("🔍 Search Player", placeholder="Type player name...")
            
            if search_term:
                filtered_players = [p for p in all_players if search_term.lower() in p.lower()]
            else:
                filtered_players = all_players
            
            selected = st.multiselect(
                "Select Players to Compare (max 3)",
                filtered_players,
                default=filtered_players[:min(2, len(filtered_players))] if not search_term else [],
                max_selections=3,
                key="player_selector"
            )
        
        with col_metrics:
            if selected:
                st.markdown("""
                <div class="glass-card" style="padding:1rem;">
                    <p style="color:#aaa; font-size:0.8rem;">📊 COMPARISON METRICS</p>
                    <p style="color:white; font-size:0.9rem;">⚽ Goals | 🅰️ Assists | 🎯 Accuracy</p>
                    <p style="color:white; font-size:0.9rem;">💶 Value | 📈 Score | ⭐ Age Bonus</p>
                </div>
                """, unsafe_allow_html=True)
        
        if selected:
            # ============================================
            # PLAYER CARDS (GLASS STYLE)
            # ============================================
            st.markdown("---")
            cols = st.columns(len(selected))
            
            for idx, (col, player) in enumerate(zip(cols, selected)):
                player_data = df[df['Player'] == player].iloc[0]
                
                # تحديد لون مميز لكل لاعب
                colors = ['#e03a3e', '#f5a623', '#4a90e2']
                player_color = colors[idx % len(colors)]
                
                # حساب الأداء بالنسبة المئوية
                gls_pct = (player_data['Gls'] / df['Gls'].max() * 100) if df['Gls'].max() > 0 else 0
                val_pct = (1 - (player_data['Market_Value_M'] / df['Market_Value_M'].max())) * 100 if df['Market_Value_M'].max() > 0 else 0
                
                with col:
                    st.markdown(f"""
                    <div class="glass-card" style="padding:1.5rem; border-left: 4px solid {player_color};">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h3 style="color:white; font-family:'Bebas Neue'; margin:0; font-size:1.8rem;">{player}</h3>
                            <span style="background:{player_color}20; color:{player_color}; padding:4px 8px; border-radius:12px; font-size:0.7rem;">
                                Rank #{idx + 1}
                            </span>
                        </div>
                        
                        <p style="color:#aaa; font-size:0.9rem; margin-top:0.3rem;">
                            {player_data.get('Squad', '')} • {player_data.get('League', '')} • Age {int(player_data['Age_num'])}
                        </p>
                        
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin:1.5rem 0;">
                            <div style="text-align:center;">
                                <div style="font-size:2rem; color:{player_color};">⚽</div>
                                <div style="font-size:1.5rem; color:white;">{int(player_data.get('Gls', 0))}</div>
                                <div style="color:#aaa; font-size:0.7rem;">GOALS</div>
                            </div>
                            <div style="text-align:center;">
                                <div style="font-size:2rem; color:{player_color};">🅰️</div>
                                <div style="font-size:1.5rem; color:white;">{int(player_data.get('Ast', 0))}</div>
                                <div style="color:#aaa; font-size:0.7rem;">ASSISTS</div>
                            </div>
                        </div>
                        
                        <div style="background:rgba(255,255,255,0.05); border-radius:8px; padding:1rem; margin:1rem 0;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                                <span style="color:#aaa;">🎯 Shot Accuracy</span>
                                <span style="color:white;">{player_data.get('SoT%', 0):.1f}%</span>
                            </div>
                            <div class="bar-bg" style="height:6px;">
                                <div class="bar-fill" style="width:{player_data.get('SoT%', 0)}%; height:6px;"></div>
                            </div>
                            
                            <div style="display:flex; justify-content:space-between; margin:1rem 0 0.5rem;">
                                <span style="color:#aaa;">💶 Market Value</span>
                                <span style="color:white;">€{player_data.get('Market_Value_M', 0):.0f}M</span>
                            </div>
                            <div class="bar-bg" style="height:6px;">
                                <div class="bar-fill" style="width:{val_pct:.0f}%; height:6px;"></div>
                            </div>
                        </div>
                        
                        <div style="display:flex; justify-content:space-between; margin-top:1rem;">
                            <div>
                                <span style="color:#aaa;">📊 Score</span>
                                <span style="color:{player_color}; font-size:1.3rem; font-weight:bold; margin-left:0.5rem;">
                                    {player_data['Final_Score']:.0f}
                                </span>
                            </div>
                            <div>
                                <span style="color:#aaa;">⚡ Perf</span>
                                <span style="color:white;">{player_data['Perf_Score']:.3f}</span>
                            </div>
                        </div>
                        
                        <div style="margin-top:1rem; font-size:0.8rem; color:#aaa;">
                            {f'<span class="badge-green">🌟 U23 Bonus</span>' if player_data['Age_num'] <= 23 else ''}
                            {f'<span class="badge-yellow">⚡ Prime</span>' if 23 < player_data['Age_num'] <= 26 else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # ============================================
            # RADAR CHART COMPARISON
            # ============================================
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sec-title">📡 RADAR COMPARISON</div>', unsafe_allow_html=True)
            
            # مؤشرات الرادار
            radar_metrics = {
                'norm_gls_p90': '⚽ Goals/90',
                'norm_sot_pct': '🎯 Shot Acc',
                'norm_ast': '🅰️ Assists',
                'norm_prgp': '📤 Prog Passes',
                'norm_context': '📅 Schedule'
            }
            
            fig_radar = go.Figure()
            
            colors = ['#e03a3e', '#f5a623', '#4a90e2']
            for idx, player in enumerate(selected):
                player_data = df[df['Player'] == player].iloc[0]
                
                # جمع القيم
                values = []
                for metric in radar_metrics.keys():
                    val = float(player_data.get(metric, 0))
                    values.append(val)
                values.append(values[0])  # لإغلاق الدائرة
                
                # التسميات
                labels = list(radar_metrics.values()) + [list(radar_metrics.values())[0]]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself',
                    name=player,
                    line=dict(color=colors[idx % len(colors)], width=3),
                    fillcolor=f'rgba{tuple(int(colors[idx % len(colors)].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.2,)}'
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        color='#aaa',
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    angularaxis=dict(
                        color='#aaa',
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    bgcolor='rgba(20,20,20,0.3)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e8e8e8', family='Inter', size=11),
                title=dict(
                    text='Player Comparison Radar',
                    font=dict(color='white', family='Bebas Neue', size=24)
                ),
                legend=dict(
                    bgcolor='rgba(20,20,20,0.6)',
                    bordercolor='rgba(224,58,62,0.2)',
                    borderwidth=1,
                    font=dict(color='#e8e8e8')
                ),
                height=500,
                margin=dict(t=50, b=30, l=10, r=10)
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # ============================================
            # DETAILED STATISTICS TABLE
            # ============================================
            st.markdown('<div class="sec-title">📋 DETAILED STATISTICS</div>', unsafe_allow_html=True)
            
            # تجهيز بيانات المقارنة
            compare_cols = [
                'Player', 'Age_num', 'Gls', 'Ast', 'Gls_p90', 'SoT%',
                'Market_Value_M', 'Perf_Score', 'Final_Score', 'Defense_Hardness'
            ]
            compare_cols = [c for c in compare_cols if c in df.columns]
            
            compare_df = df[df['Player'].isin(selected)][compare_cols].copy()
            
            # تنسيق الأرقام
            styled_df = compare_df.style.format({
                'Age_num': '{:.0f}',
                'Gls': '{:.0f}',
                'Ast': '{:.0f}',
                'Gls_p90': '{:.3f}',
                'SoT%': '{:.1f}%',
                'Market_Value_M': '€{:.0f}m',
                'Perf_Score': '{:.3f}',
                'Final_Score': '{:.1f}',
                'Defense_Hardness': '{:.2f}'
            }).set_properties(**{
                'background-color': 'rgba(20,20,20,0.6)',
                'color': '#e8e8e8',
                'border-color': 'rgba(224,58,62,0.2)',
                'font-family': 'Inter'
            })
            
            st.dataframe(styled_df, use_container_width=True)
            
            # ============================================
            # PERFORMANCE CHARTS
            # ============================================
            if len(selected) > 1:
                st.markdown('<div class="sec-title">📊 PERFORMANCE COMPARISON</div>', unsafe_allow_html=True)
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    # مقارنة الأهداف والتمريرات الحاسمة
                    fig_ga = go.Figure()
                    
                    x_positions = list(range(len(selected)))
                    
                    fig_ga.add_trace(go.Bar(
                        name='Goals',
                        x=selected,
                        y=[df[df['Player'] == p]['Gls'].values[0] for p in selected],
                        marker_color='#e03a3e',
                        text=[int(df[df['Player'] == p]['Gls'].values[0]) for p in selected],
                        textposition='inside',
                    ))
                    
                    fig_ga.add_trace(go.Bar(
                        name='Assists',
                        x=selected,
                        y=[df[df['Player'] == p]['Ast'].values[0] for p in selected],
                        marker_color='#f5a623',
                        text=[int(df[df['Player'] == p]['Ast'].values[0]) for p in selected],
                        textposition='inside',
                    ))
                    
                    fig_ga.update_layout(
                        barmode='group',
                        plot_bgcolor='rgba(20,20,20,0.3)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e8e8e8', family='Inter'),
                        title=dict(
                            text='Goals & Assists Comparison',
                            font=dict(color='white', family='Bebas Neue', size=20)
                        ),
                        showlegend=True,
                        legend=dict(
                            bgcolor='rgba(20,20,20,0.6)',
                            font=dict(color='#e8e8e8')
                        ),
                        height=350
                    )
                    
                    st.plotly_chart(fig_ga, use_container_width=True)
                
                with col_chart2:
                    # مقارنة القيمة السوقية والنتيجة النهائية
                    fig_value = go.Figure()
                    
                    fig_value.add_trace(go.Scatter(
                        x=[df[df['Player'] == p]['Market_Value_M'].values[0] for p in selected],
                        y=[df[df['Player'] == p]['Final_Score'].values[0] for p in selected],
                        mode='markers+text',
                        marker=dict(
                            size=20,
                            color=[df[df['Player'] == p]['Age_bonus'].values[0] * 10 for p in selected],
                            colorscale='Reds',
                            showscale=False
                        ),
                        text=selected,
                        textposition='top center',
                        textfont=dict(color='white', size=10)
                    ))
                    
                    fig_value.update_layout(
                        plot_bgcolor='rgba(20,20,20,0.3)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e8e8e8', family='Inter'),
                        title=dict(
                            text='Value vs Score Distribution',
                            font=dict(color='white', family='Bebas Neue', size=20)
                        ),
                        xaxis=dict(title='Market Value (€M)', gridcolor='rgba(255,255,255,0.05)'),
                        yaxis=dict(title='Final Score', gridcolor='rgba(255,255,255,0.05)'),
                        height=350
                    )
                    
                    st.plotly_chart(fig_value, use_container_width=True)
            
            # ============================================
            # RECOMMENDATION BASED ON ANALYSIS
            # ============================================
            if len(selected) == 2:
                st.markdown('<div class="sec-title">💡 SCOUTING RECOMMENDATION</div>', unsafe_allow_html=True)
                
                # مقارنة بسيطة لتحديد الأفضل
                player1 = df[df['Player'] == selected[0]].iloc[0]
                player2 = df[df['Player'] == selected[1]].iloc[0]
                
                if player1['Final_Score'] > player2['Final_Score']:
                    better = player1
                    worse = player2
                else:
                    better = player2
                    worse = player1
                
                st.markdown(f"""
                <div class="glass-card" style="padding:1.5rem; text-align:center;">
                    <h3 style="color:#e03a3e; font-family:'Bebas Neue';">🏆 RECOMMENDED TARGET</h3>
                    <p style="font-size:2rem; color:white; margin:0.5rem 0;">{better['Player']}</p>
                    <p style="color:#aaa;">over {worse['Player']}</p>
                    
                    <div style="display:flex; justify-content:center; gap:2rem; margin:1.5rem 0;">
                        <div>
                            <span style="color:#aaa;">Value Score</span>
                            <span style="color:#e03a3e; font-size:1.5rem; margin-left:0.5rem;">{better['Final_Score']:.0f}</span>
                        </div>
                        <div>
                            <span style="color:#aaa;">vs</span>
                            <span style="color:#aaa; margin-left:0.5rem;">{worse['Final_Score']:.0f}</span>
                        </div>
                    </div>
                    
                    <p style="color:#aaa; font-size:0.9rem;">
                        ⚡ Better value for money considering age ({int(better['Age_num'])}) and performance
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("👆 اختر لاعبين للمقارنة من القائمة أعلاه")
    
    else:
        st.warning("لا يوجد لاعبين للعرض")

# TAB 4: Full Dataset - نسخة محسنة بدون background_gradient
with tab4:
    st.markdown('<div class="sec-title">📋 FULL DATASET</div>', unsafe_allow_html=True)
    
    # أعمدة العرض
    display_cols = ['Player', 'Squad', 'Age_num', 'Pos_primary', 'Gls', 'Ast', 'SoT%', 
                    'Gls_p90', 'Market_Value_M', 'Perf_Score', 'Final_Score']
    display_cols = [c for c in display_cols if c in df.columns]
    
    # إضافة خيارات للعرض
    col_view1, col_view2, col_view3 = st.columns([2, 2, 1])
    
    with col_view1:
        sort_by = st.selectbox("Sort by", ['Final_Score', 'Market_Value_M', 'Gls', 'Age_num'])
    
    with col_view2:
        asc_order = st.checkbox("Ascending", False)
    
    with col_view3:
        rows_to_show = st.selectbox("Rows", [10, 25, 50, 100], index=1)
    
    # ترتيب البيانات
    display_df = df[display_cols].copy().sort_values(sort_by, ascending=asc_order).head(rows_to_show)
    
    # تنسيق الأرقام
    for col in display_df.columns:
        if col == 'SoT%':
            display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%")
        elif col == 'Gls_p90':
            display_df[col] = display_df[col].apply(lambda x: f"{x:.3f}")
        elif col == 'Market_Value_M':
            display_df[col] = display_df[col].apply(lambda x: f"€{x:.0f}m")
        elif col in ['Final_Score', 'Perf_Score']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}")
        elif col in ['Gls', 'Ast', 'Age_num']:
            display_df[col] = display_df[col].apply(lambda x: f"{int(x)}")
    
    # عرض الجدول بتنسيق جميل
    st.markdown("""
    <style>
        .dataframe-container {
            background: rgba(20,20,20,0.4);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(224,58,62,0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=500
    )
    
    # إحصائيات سريعة
    st.markdown('<div class="sec-title">📊 QUICK STATS</div>', unsafe_allow_html=True)
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:1.5rem; color:white;">{len(df)}</div>
            <div style="color:#aaa;">Total Players</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:1.5rem; color:white;">{df['Pos_primary'].nunique()}</div>
            <div style="color:#aaa;">Positions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:1.5rem; color:white;">{df['Squad'].nunique()}</div>
            <div style="color:#aaa;">Teams</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat4:
        total_goals = df['Gls'].sum()
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:1.5rem; color:white;">{int(total_goals)}</div>
            <div style="color:#aaa;">Total Goals</div>
        </div>
        """, unsafe_allow_html=True)
    
    # أزرار التحميل
    st.markdown("<br>", unsafe_allow_html=True)
    col_dl1, col_dl2, _ = st.columns([1, 1, 4])
    
    with col_dl1:
        st.download_button(
            "⬇️ Download Full CSV",
            df.to_csv(index=False).encode('utf-8'),
            "scouting_results.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col_dl2:
        st.download_button(
            "⬇️ Download Top 10",
            df.head(10).to_csv(index=False).encode('utf-8'),
            "top10_targets.csv",
            "text/csv",
            use_container_width=True
        )
  # TAB 4: Full Dataset - نسخة متطورة مع تحليلات وتصفية متقدمة
with tab4:
    st.markdown('<div class="sec-title">📋 FULL DATASET</div>', unsafe_allow_html=True)
    
    # ============================================
    # TOOLBAR للتحكم في عرض البيانات
    # ============================================
    col_tool1, col_tool2, col_tool3, col_tool4 = st.columns([2, 2, 2, 1])
    
    with col_tool1:
        # اختيار الأعمدة للعرض
        all_columns = ['Player', 'Nation', 'Pos_primary', 'Squad', 'Age_num', 'League', 
                      'Gls', 'Ast', 'Gls_p90', 'SoT%', 'Market_Value_M', 'Perf_Score', 
                      'Final_Score', 'Defense_Hardness']
        available_cols = [col for col in all_columns if col in df.columns]
        selected_cols = st.multiselect(
            "📌 Select Columns",
            available_cols,
            default=['Player', 'Squad', 'Age_num', 'Pos_primary', 'Gls', 'Ast', 'SoT%', 'Market_Value_M', 'Final_Score']
        )
    
    with col_tool2:
        # ترتيب البيانات
        sort_options = [col for col in ['Final_Score', 'Market_Value_M', 'Gls', 'Age_num', 'SoT%'] if col in df.columns]
        sort_by = st.selectbox("🔽 Sort By", sort_options, index=0 if sort_options else 0)
    
    with col_tool3:
        # عدد الصفوف
        rows_options = [10, 25, 50, 100, len(df)]
        rows_to_show = st.selectbox("📊 Rows to Show", rows_options, index=min(2, len(rows_options)-1))
    
    with col_tool4:
        # اتجاه الترتيب
        asc_order = st.checkbox("🔄 Ascending", False)
    
    # ============================================
    # إحصائيات سريعة
    # ============================================
    if not df.empty:
        st.markdown("---")
        col_stat1, col_stat2, col_stat3, col_stat4, col_stat5 = st.columns(5)
        
        with col_stat1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:0.8rem;">
                <div style="font-size:1.8rem; color:var(--red); font-family:'Bebas Neue';">{len(df)}</div>
                <div style="color:#aaa; font-size:0.7rem;">TOTAL PLAYERS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:0.8rem;">
                <div style="font-size:1.8rem; color:white; font-family:'Bebas Neue';">{df['Squad'].nunique()}</div>
                <div style="color:#aaa; font-size:0.7rem;">TEAMS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat3:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:0.8rem;">
                <div style="font-size:1.8rem; color:#f5a623; font-family:'Bebas Neue';">{df['Pos_primary'].nunique()}</div>
                <div style="color:#aaa; font-size:0.7rem;">POSITIONS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat4:
            total_goals = int(df['Gls'].sum()) if 'Gls' in df.columns else 0
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:0.8rem;">
                <div style="font-size:1.8rem; color:#7ed321; font-family:'Bebas Neue';">{total_goals}</div>
                <div style="color:#aaa; font-size:0.7rem;">TOTAL GOALS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat5:
            avg_age = df['Age_num'].mean() if 'Age_num' in df.columns else 0
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:0.8rem;">
                <div style="font-size:1.8rem; color:#4a90e2; font-family:'Bebas Neue';">{avg_age:.1f}</div>
                <div style="color:#aaa; font-size:0.7rem;">AVG AGE</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================
        # تجهيز وعرض البيانات
        # ============================================
        if selected_cols:
            # نسخة للعرض
            display_df = df[selected_cols].copy()
            
            # ترتيب البيانات
            if sort_by in display_df.columns:
                display_df = display_df.sort_values(sort_by, ascending=asc_order)
            
            # تحديد عدد الصفوف
            if rows_to_show < len(display_df):
                display_df = display_df.head(rows_to_show)
            
            # تنسيق الأرقام
            formatted_df = display_df.copy()
            
            # تطبيق التنسيق المناسب لكل عمود
            for col in formatted_df.columns:
                if col == 'SoT%':
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{float(x):.1f}%")
                elif col == 'Gls_p90':
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{float(x):.3f}")
                elif col == 'Market_Value_M':
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"€{float(x):.0f}m")
                elif col == 'Final_Score':
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{float(x):.1f}")
                elif col == 'Perf_Score':
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{float(x):.3f}")
                elif col == 'Defense_Hardness':
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{float(x):.2f}")
                elif col in ['Gls', 'Ast', 'Age_num']:
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{int(x)}")
            
            # CSS مخصص للجدول
            st.markdown("""
            <style>
                [data-testid="stDataFrame"] {
                    background: rgba(20,20,20,0.3) !important;
                    border-radius: 12px !important;
                    border: 1px solid rgba(224,58,62,0.2) !important;
                }
                [data-testid="stDataFrame"] th {
                    background: rgba(30,30,30,0.8) !important;
                    color: white !important;
                    font-family: 'Inter', sans-serif !important;
                    font-size: 0.8rem !important;
                    font-weight: 600 !important;
                    text-transform: uppercase !important;
                    letter-spacing: 1px !important;
                }
                [data-testid="stDataFrame"] td {
                    background: rgba(20,20,20,0.6) !important;
                    color: #e8e8e8 !important;
                    font-family: 'Inter', sans-serif !important;
                    font-size: 0.8rem !important;
                    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
                }
                [data-testid="stDataFrame"] tr:hover td {
                    background: rgba(40,40,40,0.8) !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # عرض الجدول
            st.dataframe(formatted_df, use_container_width=True, height=450)
            
            # ============================================
            # تحليلات إضافية
            # ============================================
            st.markdown('<div class="sec-title">📊 DATA INSIGHTS</div>', unsafe_allow_html=True)
            
            col_insight1, col_insight2 = st.columns(2)
            
            with col_insight1:
                # توزيع المراكز
                if 'Pos_primary' in df.columns:
                    pos_counts = df['Pos_primary'].value_counts()
                    
                    fig_pos = go.Figure(data=[go.Pie(
                        labels=pos_counts.index,
                        values=pos_counts.values,
                        hole=.4,
                        marker_colors=['#e03a3e', '#f5a623', '#4a90e2', '#7ed321', '#9b59b6']
                    )])
                    
                    fig_pos.update_layout(
                        title=dict(
                            text='Position Distribution',
                            font=dict(color='white', family='Bebas Neue', size=20)
                        ),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e8e8e8', family='Inter'),
                        showlegend=True,
                        legend=dict(
                            bgcolor='rgba(20,20,20,0.6)',
                            bordercolor='rgba(224,58,62,0.2)',
                            font=dict(color='#e8e8e8')
                        ),
                        height=300
                    )
                    
                    st.plotly_chart(fig_pos, use_container_width=True)
            
            with col_insight2:
                # توزيع الأعمار
                if 'Age_num' in df.columns:
                    fig_age = go.Figure()
                    
                    fig_age.add_trace(go.Histogram(
                        x=df['Age_num'],
                        nbinsx=15,
                        marker_color='#e03a3e',
                        opacity=0.7,
                        name='Age Distribution'
                    ))
                    
                    fig_age.update_layout(
                        title=dict(
                            text='Age Distribution',
                            font=dict(color='white', family='Bebas Neue', size=20)
                        ),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e8e8e8', family='Inter'),
                        xaxis=dict(
                            title='Age',
                            gridcolor='rgba(255,255,255,0.05)'
                        ),
                        yaxis=dict(
                            title='Count',
                            gridcolor='rgba(255,255,255,0.05)'
                        ),
                        height=300,
                        bargap=0.1
                    )
                    
                    st.plotly_chart(fig_age, use_container_width=True)
            
            # ============================================
            # SUMMARY STATISTICS TABLE
            # ============================================
            st.markdown('<div class="sec-title">📈 SUMMARY STATISTICS</div>', unsafe_allow_html=True)
            
            # حساب الإحصائيات للأعمدة الرقمية
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            stats_data = []
            
            for col in numeric_cols:
                if col in df.columns and col not in ['90s', 'Sh', 'SoT', 'Sh_p90', 'SoT_p90', 'G/Sh', 'G/SoT', 'PK', 'PKatt']:
                    stats_data.append({
                        'Metric': col,
                        'Mean': f"{df[col].mean():.2f}",
                        'Median': f"{df[col].median():.2f}",
                        'Std': f"{df[col].std():.2f}",
                        'Min': f"{df[col].min():.2f}",
                        'Max': f"{df[col].max():.2f}"
                    })
            
            if stats_data:
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df, use_container_width=True, height=200)
            
            # ============================================
            # DOWNLOAD BUTTONS
            # ============================================
            st.markdown("---")
            col_dl1, col_dl2, col_dl3, _ = st.columns([1, 1, 1, 3])
            
            with col_dl1:
                st.download_button(
                    "📥 Full Dataset",
                    df.to_csv(index=False).encode('utf-8'),
                    "brentford_scouting_full.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col_dl2:
                st.download_button(
                    "📥 Top 50",
                    df.head(50).to_csv(index=False).encode('utf-8'),
                    "brentford_top50.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col_dl3:
                # تصدير الإحصائيات
                if stats_data:
                    stats_export = pd.DataFrame(stats_data)
                    st.download_button(
                        "📊 Statistics",
                        stats_export.to_csv(index=False).encode('utf-8'),
                        "dataset_statistics.csv",
                        "text/csv",
                        use_container_width=True
                    )
    
    else:
        st.warning("⚠️ لا توجد نتائج تطابق معايير البحث. حاول تعديل الفلاتر.")

# ============================================
# FOOTER - مطور
# ============================================
st.markdown("""
<div class="footer">
    <div style="display:flex; justify-content:center; gap:2rem; margin-bottom:1rem;">
        <span>🐝 BRENTFORD FC SCOUTING SYSTEM</span>
        <span>⚽ SEASON 2025-26</span>
        <span>📊 DATA: FBREF + TRANSFERMARKT</span>
    </div>
    <div style="display:flex; justify-content:center; gap:1rem;">
        <a href="https://www.linkedin.com/in/goda-emad/" target="_blank" style="color:#666;">🔗 LinkedIn</a>
        <a href="https://github.com/Goda-Emad/brentford-scouting" target="_blank" style="color:#666;">🐙 GitHub</a>
        <span style="color:#666;">📞 +20 112 624 2932</span>
    </div>
    <div style="margin-top:1rem; color:#444; font-size:0.6rem;">
        Developed by Goda Emad © 2026
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# نهاية التطبيق
# ============================================
