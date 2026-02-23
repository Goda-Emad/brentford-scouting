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
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    css_path = pathlib.Path("assets/style.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# CSS (مختصر للعرض)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');
:root { --red: #e03a3e; --black: #0d0d0d; --dark: #141414; --card: #1a1a1a; --border: rgba(224,58,62,0.22); --text: #e8e8e8; --muted: #777; }
html, body, [data-testid="stAppViewContainer"] { background: var(--black) !important; color: var(--text) !important; }
[data-testid="stSidebar"] { background: #0f0f0f !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
.header-wrap { background: linear-gradient(135deg, #0d0d0d 0%, #1c0606 60%, #0d0d0d 100%); border: 1px solid var(--border); border-radius: 14px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; display: flex; align-items: center; gap: 2rem; }
.header-wrap::before { content: ''; position: absolute; top: -80px; right: -60px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(224,58,62,0.13) 0%, transparent 70%); }
.header-logo { width: 72px; height: 72px; border-radius: 50%; border: 2px solid var(--border); object-fit: contain; flex-shrink: 0; }
.main-title { font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: white; letter-spacing: 4px; line-height: 1; margin: 0; }
.main-title span { color: var(--red); }
.main-sub { font-family: 'Inter', sans-serif; font-size: 0.72rem; color: var(--muted); letter-spacing: 2.5px; text-transform: uppercase; margin-top: 0.4rem; }
.social-links { margin-top: 0.8rem; display: flex; gap: 0.6rem; flex-wrap: wrap; }
.social-btn { display: inline-flex; align-items: center; gap: 5px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.10); color: #aaa !important; font-family: 'Inter', sans-serif; font-size: 0.68rem; font-weight: 500; letter-spacing: 0.8px; padding: 4px 12px; border-radius: 20px; text-decoration: none !important; transition: all 0.2s; }
.social-btn:hover { border-color: var(--red); color: white !important; }
.kpi-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1.1rem 1.3rem; position: relative; overflow: hidden; transition: transform 0.2s; }
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::after { content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, var(--red), transparent); }
.kpi-val { font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: white; line-height: 1; }
.kpi-lbl { font-family: 'Inter', sans-serif; font-size: 0.65rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1.8px; margin-top: 0.3rem; }
.pcard { background: var(--card); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 0.7rem; transition: all 0.2s; }
.pcard:hover { border-color: var(--border); box-shadow: 0 4px 20px rgba(224,58,62,0.07); }
.pname { font-family: 'Bebas Neue', sans-serif; font-size: 1.25rem; color: white; letter-spacing: 1px; }
.pmeta { font-family: 'Inter', sans-serif; font-size: 0.7rem; color: var(--muted); margin-top: 0.15rem; }
.bar-bg { background: #222; border-radius: 4px; height: 4px; margin-top: 0.8rem; }
.bar-fill { background: linear-gradient(90deg, #8b1a1a, var(--red), #ff7070); border-radius: 4px; height: 4px; }
.badge { display: inline-block; background: rgba(224,58,62,0.12); border: 1px solid var(--border); color: var(--red); font-size: 0.62rem; font-family: 'Inter', sans-serif; font-weight: 600; padding: 2px 8px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1px; margin-right: 4px; }
.badge-g { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.08); color: var(--muted); }
.badge-green { background: rgba(126,211,33,0.10); border-color: rgba(126,211,33,0.25); color: #7ed321; }
.badge-yellow { background: rgba(245,166,35,0.10); border-color: rgba(245,166,35,0.25); color: #f5a623; }
.sec-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: white; letter-spacing: 2.5px; border-left: 3px solid var(--red); padding-left: 0.8rem; margin: 1.5rem 0 1rem; }
[data-testid="stTabs"] [data-baseweb="tab"] { color: var(--muted) !important; font-family: 'Inter', sans-serif !important; font-size: 0.78rem !important; font-weight: 500 !important; }
[data-testid="stTabs"] [aria-selected="true"] { color: white !important; border-bottom: 2px solid var(--red) !important; }
[data-testid="stSidebar"] label { font-family: 'Inter', sans-serif !important; font-size: 0.7rem !important; text-transform: uppercase !important; letter-spacing: 1.5px !important; color: var(--muted) !important; }
[data-testid="stDownloadButton"] button { background: transparent !important; border: 1px solid var(--border) !important; color: var(--red) !important; font-family: 'Inter', sans-serif !important; font-size: 0.75rem !important; border-radius: 8px !important; transition: all 0.2s !important; }
[data-testid="stDownloadButton"] button:hover { background: rgba(224,58,62,0.1) !important; }
.footer { text-align: center; padding: 2rem 0 1rem; color: #333; font-family: 'Inter', sans-serif; font-size: 0.68rem; letter-spacing: 1.5px; text-transform: uppercase; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 3rem; }
.footer a { color: #555 !important; text-decoration: none; transition: color 0.2s; }
.footer a:hover { color: var(--red) !important; }
hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.05) !important; }
</style>
""", unsafe_allow_html=True)

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
                # بيانات تجريبية
                st.info("📊 استخدام بيانات تجريبية")
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
            "brentford_logo.png"
        ]
        
        for p in possible_paths:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode()
        return None
    except:
        return None

# بداية التطبيق
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

# السايدبار
with st.sidebar:
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.3rem;color:white;letter-spacing:2px;margin-bottom:1rem;padding-bottom:0.7rem;border-bottom:1px solid rgba(224,58,62,0.25);">⚙️ SCOUT FILTERS</div>', unsafe_allow_html=True)
    
    uploaded = st.file_uploader("📂 Add New League CSV", type=["csv"])
    df_base = load_data(uploaded)
    
    if df_base.empty:
        st.error("❌ لا توجد بيانات")
        st.stop()
    
    # الفلاتر مع معالجة الأخطاء
    leagues = sorted(df_base['League'].dropna().unique()) if 'League' in df_base.columns else ['Ligue 1']
    sel_league = st.multiselect("🌍 League", leagues, default=leagues if leagues else ['Ligue 1'])
    
    positions = sorted(df_base['Pos_primary'].dropna().unique()) if 'Pos_primary' in df_base.columns else ['FW', 'MF']
    sel_pos = st.multiselect("📍 Position", positions, default=positions if positions else ['FW'])
    
    # معالجة العمر
    min_age = int(df_base['Age_num'].min()) if not df_base['Age_num'].empty else 18
    max_age = int(df_base['Age_num'].max()) if not df_base['Age_num'].empty else 40
    
    if min_age >= max_age:
        max_age = min_age + 10
    
    age_range = st.slider("🎂 Age Range", min_age, max_age, (min_age, max_age))
    
    # معالجة القيمة السوقية
    min_val = float(df_base['Market_Value_M'].min()) if not df_base['Market_Value_M'].empty else 0
    max_val = float(df_base['Market_Value_M'].max()) if not df_base['Market_Value_M'].empty else 100
    
    if min_val >= max_val:
        max_val = min_val + 10
    
    budget = st.slider("💶 Max Market Value (€m)", min_val, max_val, max_val)
    
    # معالجة الدقائق
    min_90s_val = float(df_base['90s'].min()) if not df_base['90s'].empty else 0
    max_90s_val = float(df_base['90s'].max()) if not df_base['90s'].empty else 50
    
    if min_90s_val >= max_90s_val:
        max_90s_val = min_90s_val + 10
    
    min_90s = st.slider("⏱️ Min 90s Played", min_90s_val, max_90s_val, min(3.0, max_90s_val), step=0.5)
    
    st.markdown("---")
    top_n = st.selectbox("📊 Show Top N Targets", [5, 10, 15, 20, 30, 50], index=1)

# تطبيق الفلاتر
df = df_base.copy()

if sel_league and 'League' in df.columns:
    df = df[df['League'].isin(sel_league)]

if sel_pos and 'Pos_primary' in df.columns:
    df = df[df['Pos_primary'].isin(sel_pos)]

df = df[
    (df['Age_num'] >= age_range[0]) & 
    (df['Age_num'] <= age_range[1]) & 
    (df['Market_Value_M'] <= budget) & 
    (df['90s'] >= min_90s)
].sort_values('Final_Score', ascending=False).reset_index(drop=True)

# KPIs
if not df.empty:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(df)}</div><div class="kpi-lbl">Players Scouted</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">€{df["Market_Value_M"].mean():.1f}m</div><div class="kpi-lbl">Avg Market Value</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{df["Final_Score"].max():.0f}</div><div class="kpi-lbl">Top Value Score</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{df["Gls_p90"].mean():.2f}</div><div class="kpi-lbl">Avg Goals / 90</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{df["SoT%"].mean():.1f}%</div><div class="kpi-lbl">Avg Shot Accuracy</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # التبويبات
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Top Targets", "📊 Value Analysis", "🔬 Player Deep Dive", "📋 Full Dataset"])

    # TAB 1: Top Targets
    with tab1:
        st.markdown('<div class="sec-title">TOP TARGETS</div>', unsafe_allow_html=True)
        
        for rank, (_, row) in enumerate(df.head(top_n).iterrows(), 1):
            score_pct = min(row['Final_Score'] / 130 * 100, 100)
            
            h = row.get('Defense_Hardness', 0.5)
            if h >= 0.6:
                sch_class, sch_text = 'badge badge', '🔴 Hard Schedule'
            elif h >= 0.4:
                sch_class, sch_text = 'badge-yellow badge', '🟡 Mid Schedule'
            else:
                sch_class, sch_text = 'badge-green badge', '🟢 Easy Schedule'
            
            age = int(row['Age_num'])
            if age <= 23:
                age_badge = '<span class="badge">🌟 U23</span>'
            elif age <= 26:
                age_badge = '<span class="badge-g badge">Prime</span>'
            else:
                age_badge = '<span class="badge-g badge">Veteran</span>'
            
            st.markdown(f"""
            <div class="pcard">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
                    <div style="flex:1;">
                        <div style="color:var(--red);font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;letter-spacing:1.5px;">#{rank:02d}</div>
                        <div class="pname">{row['Player']}</div>
                        <div class="pmeta">{row.get('Squad', '—')} • {row.get('League', '—')} • Age {age}</div>
                        <div style="margin-top:0.5rem;"><span class="badge">{row.get('Pos_primary', '—')}</span>{age_badge}<span class="{sch_class}">{sch_text}</span></div>
                    </div>
                    <div style="text-align:right;flex-shrink:0;">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;color:var(--red);line-height:1;">{row['Final_Score']:.0f}</div>
                        <div style="font-size:0.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px;">Value Score</div>
                        <div style="font-size:0.82rem;color:white;margin-top:0.4rem;">
                            ⚽ {int(row.get('Gls', 0))}G • 🅰️ {int(row.get('Ast', 0))}A • 🎯 {row.get('SoT%', 0):.0f}% • 💶 €{row.get('Market_Value_M', 0):.0f}m
                        </div>
                    </div>
                </div>
                <div class="bar-bg"><div class="bar-fill" style="width:{score_pct:.0f}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

    # TAB 2: Value Analysis
    with tab2:
        st.markdown('<div class="sec-title">VALUE ANALYSIS</div>', unsafe_allow_html=True)
        
        if len(df) > 1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(
                    df, x='Market_Value_M', y='Final_Score', hover_name='Player',
                    color='Pos_primary', size='Gls', size_max=22,
                    title='Value Score vs Market Value',
                    labels={'Market_Value_M': 'Market Value (€m)', 'Final_Score': 'Value Score'}
                )
                fig.update_layout(
                    plot_bgcolor='#141414', paper_bgcolor='#1a1a1a',
                    font=dict(color='#e8e8e8', family='Inter')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig2 = px.bar(
                    df.head(10), x='Final_Score', y='Player', orientation='h',
                    title='Top 10 Value Scores',
                    color='Final_Score', color_continuous_scale=['#1a0505', '#e03a3e']
                )
                fig2.update_layout(
                    plot_bgcolor='#141414', paper_bgcolor='#1a1a1a',
                    font=dict(color='#e8e8e8', family='Inter'),
                    yaxis=dict(autorange='reversed')
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📊 هناك حاجة إلى المزيد من البيانات للرسوم البيانية")

    # TAB 3: Player Deep Dive
    with tab3:
        st.markdown('<div class="sec-title">PLAYER DEEP DIVE</div>', unsafe_allow_html=True)
        
        if len(df) > 0:
            all_players = df['Player'].tolist()
            selected = st.multiselect(
                "Select Players to Compare",
                all_players,
                default=all_players[:min(2, len(all_players))],
                max_selections=3
            )
            
            if selected:
                cols = st.columns(len(selected))
                for col, player in zip(cols, selected):
                    player_data = df[df['Player'] == player].iloc[0]
                    with col:
                        st.markdown(f"""
                        <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1rem;">
                            <h4 style="color:white;font-family:'Bebas Neue';">{player}</h4>
                            <p style="color:var(--muted);font-size:0.8rem;">{player_data.get('Squad', '')}</p>
                            <hr style="margin:10px 0;">
                            <p><span style="color:var(--red);">⚽ {int(player_data.get('Gls', 0))}</span> Goals</p>
                            <p><span style="color:var(--red);">🅰️ {int(player_data.get('Ast', 0))}</span> Assists</p>
                            <p><span style="color:var(--red);">🎯 {player_data.get('SoT%', 0):.1f}%</span> Shot Acc</p>
                            <p><span style="color:var(--red);">💶 €{player_data.get('Market_Value_M', 0):.0f}m</span> Value</p>
                            <p><span style="color:var(--red);">📊 {player_data['Final_Score']:.1f}</span> Score</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("👆 اختر لاعبين للمقارنة")
        else:
            st.warning("لا يوجد لاعبين")

    # TAB 4: Full Dataset - ** بدون background_gradient **
    with tab4:
        st.markdown('<div class="sec-title">FULL DATASET</div>', unsafe_allow_html=True)
        
        # أعمدة العرض
        display_cols = ['Player', 'Squad', 'Age_num', 'Pos_primary', 'Gls', 'Ast', 'SoT%', 'Market_Value_M', 'Final_Score']
        display_cols = [c for c in display_cols if c in df.columns]
        
        # نسخة للعرض بدون تنسيق معقد
        display_df = df[display_cols].copy()
        
        # تنسيق الأرقام
        for col in display_df.columns:
            if col == 'SoT%':
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%")
            elif col == 'Market_Value_M':
                display_df[col] = display_df[col].apply(lambda x: f"€{x:.0f}m")
            elif col == 'Final_Score':
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}")
            elif col in ['Gls', 'Ast', 'Age_num']:
                display_df[col] = display_df[col].apply(lambda x: f"{int(x)}")
        
        # عرض الجدول بدون background_gradient
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # أزرار التحميل
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download Full CSV",
                df.to_csv(index=False).encode('utf-8'),
                "scouting_results.csv",
                "text/csv",
                use_container_width=True
            )
        with col2:
            st.download_button(
                "⬇️ Top 10 Only",
                df.head(10).to_csv(index=False).encode('utf-8'),
                "top10_targets.csv",
                "text/csv",
                use_container_width=True
            )

else:
    st.warning("⚠️ لا توجد نتائج تطابق معايير البحث. حاول تعديل الفلاتر.")

# Footer
st.markdown("""
<div class="footer">
    Built by <a href="https://www.linkedin.com/in/goda-emad/" target="_blank">Goda Emad</a>
    &nbsp;•&nbsp; <a href="https://github.com/Goda-Emad/brentford-scouting" target="_blank">GitHub</a>
    &nbsp;•&nbsp; Data: FBref + Transfermarkt
</div>
""", unsafe_allow_html=True)
