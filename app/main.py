import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64, pathlib, os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brentford FC | Scouting Intelligence",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLASS BACKGROUND ────────────────────────────────────────────────────────
def add_glass_background():
    """Load background image and inject via base64 - works on Streamlit Cloud"""
    bg_paths = [
        "assets/bg_stadium.jpg",
        "assets/bg_stadium.jpeg", 
        "assets/bg_stadium.png",
        "bg_stadium.jpg",
    ]
    bg_b64, ext = None, "jpeg"
    for path in bg_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    bg_b64 = base64.b64encode(f.read()).decode()
                ext = "png" if path.endswith(".png") else "jpeg"
                break
            except:
                pass

    if bg_b64:
        st.markdown(f"""
<style>
/* ── BACKGROUND IMAGE ── */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/{ext};base64,{bg_b64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}}
/* dark overlay */
[data-testid="stAppViewContainer"]::after {{
    content: "" !important;
    position: fixed !important;
    inset: 0 !important;
    background: rgba(5,5,5,0.83) !important;
    z-index: 0 !important;
    pointer-events: none !important;
}}
/* push content above overlay */
[data-testid="stAppViewContainer"] > * {{
    position: relative !important;
    z-index: 1 !important;
}}
[data-testid="stHeader"] {{
    background: transparent !important;
}}
[data-testid="stToolbar"] {{
    background: transparent !important;
}}
</style>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0505 50%, #0a0a0a 100%) !important;
}
</style>
""", unsafe_allow_html=True)

add_glass_background()

# ─── LOAD CSS ────────────────────────────────────────────────────────────────
def load_css():
    css_path = pathlib.Path("assets/style.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

# ─── INLINE CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');
:root {
    --red:#e03a3e; --red-dark:#8b1a1a; --black:#0a0a0a; --dark:#141414;
    --card:rgba(22,22,22,0.75); --border:rgba(224,58,62,0.25);
    --text:#f0f0f0; --muted:#888;
}
html,body,[data-testid="stAppViewContainer"]{color:var(--text)!important;font-family:'Inter',sans-serif!important;}
[data-testid="stSidebar"]{background:rgba(10,10,10,0.85)!important;backdrop-filter:blur(16px)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}

/* Header */
.header-wrap{background:rgba(10,10,10,0.72);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border:1px solid var(--border);border-radius:16px;padding:2rem 2.5rem;margin-bottom:1.5rem;
  position:relative;overflow:hidden;display:flex;align-items:center;gap:2rem;
  box-shadow:0 8px 32px rgba(0,0,0,0.5);}
.header-wrap::before{content:'';position:absolute;top:-80px;right:-60px;width:380px;height:380px;
  background:radial-gradient(circle,rgba(224,58,62,0.18) 0%,transparent 70%);}
.header-wrap::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:1px;
  background:linear-gradient(90deg,transparent,var(--red),transparent);}
.header-logo{width:72px;height:72px;border-radius:50%;border:2px solid var(--border);object-fit:contain;transition:transform 0.3s;}
.header-logo:hover{transform:scale(1.08) rotate(5deg);border-color:var(--red);}
.main-title{font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:white;letter-spacing:4px;line-height:1;margin:0;}
.main-title span{color:var(--red);}
.main-sub{font-family:'Inter',sans-serif;font-size:0.72rem;color:var(--muted);letter-spacing:2.5px;text-transform:uppercase;margin-top:0.4rem;}
.social-links{margin-top:0.8rem;display:flex;gap:0.6rem;flex-wrap:wrap;}
.social-btn{display:inline-flex;align-items:center;gap:5px;background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.1);color:#aaa!important;font-family:'Inter',sans-serif;
  font-size:0.68rem;font-weight:500;letter-spacing:0.8px;padding:5px 14px;border-radius:30px;
  text-decoration:none!important;transition:all 0.2s;}
.social-btn:hover{border-color:var(--red);color:white!important;background:rgba(224,58,62,0.1);transform:translateY(-2px);}

/* KPI */
.kpi-card{background:rgba(22,22,22,0.65);backdrop-filter:blur(10px);border:1px solid var(--border);
  border-radius:12px;padding:1.1rem 1.3rem;position:relative;overflow:hidden;transition:all 0.25s;}
.kpi-card:hover{transform:translateY(-3px);border-color:var(--red);box-shadow:0 8px 24px rgba(224,58,62,0.15);}
.kpi-card::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:2px;
  background:linear-gradient(90deg,var(--red),transparent);}
.kpi-val{font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:white;line-height:1;}
.kpi-lbl{font-family:'Inter',sans-serif;font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.8px;margin-top:0.3rem;}

/* Glass Card */
.glass-card{background:rgba(22,22,22,0.65);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  border:1px solid var(--border);border-radius:12px;padding:1.2rem;transition:all 0.25s;}
.glass-card:hover{border-color:var(--red);box-shadow:0 8px 24px rgba(224,58,62,0.12);transform:translateY(-2px);}

/* Player card */
.pcard{background:rgba(22,22,22,0.6);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.05);
  border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:0.7rem;position:relative;overflow:hidden;transition:all 0.25s;}
.pcard::before{content:'';position:absolute;top:0;left:0;width:3px;height:0;background:var(--red);transition:height 0.3s;}
.pcard:hover::before{height:100%;}
.pcard:hover{background:rgba(35,35,35,0.7);border-color:rgba(224,58,62,0.35);box-shadow:0 6px 20px rgba(224,58,62,0.1);transform:translateX(4px);}
.pname{font-family:'Bebas Neue',sans-serif;font-size:1.28rem;color:white;letter-spacing:1px;}
.pmeta{font-family:'Inter',sans-serif;font-size:0.7rem;color:var(--muted);margin-top:0.15rem;}
.bar-bg{background:#222;border-radius:6px;height:5px;margin-top:0.8rem;overflow:hidden;}
.bar-fill{background:linear-gradient(90deg,var(--red-dark),var(--red),#ff7070);border-radius:6px;height:5px;}

/* Badges */
.badge{display:inline-block;background:rgba(224,58,62,0.14);border:1px solid var(--border);color:var(--red);
  font-size:0.62rem;font-family:'Inter',sans-serif;font-weight:600;padding:2px 9px;border-radius:20px;
  text-transform:uppercase;letter-spacing:1px;margin-right:4px;}
.badge-g{background:rgba(255,255,255,0.04);border-color:rgba(255,255,255,0.08);color:var(--muted);}
.badge-green{background:rgba(46,204,113,0.1);border-color:rgba(46,204,113,0.25);color:#2ecc71;}
.badge-yellow{background:rgba(243,156,18,0.1);border-color:rgba(243,156,18,0.25);color:#f39c12;}

/* Section title */
.sec-title{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:white;letter-spacing:2.5px;
  border-left:3px solid var(--red);padding-left:0.8rem;margin:1.5rem 0 1rem;}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:rgba(15,15,15,0.5)!important;border-radius:10px!important;padding:4px!important;}
[data-testid="stTabs"] [data-baseweb="tab"]{color:var(--muted)!important;font-family:'Inter',sans-serif!important;font-size:0.78rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:1px!important;border-radius:8px!important;}
[data-testid="stTabs"] [aria-selected="true"]{color:white!important;background:rgba(224,58,62,0.15)!important;border-bottom:2px solid var(--red)!important;}

/* Sidebar labels */
[data-testid="stSidebar"] label{font-family:'Inter',sans-serif!important;font-size:0.7rem!important;text-transform:uppercase!important;letter-spacing:1.5px!important;color:var(--muted)!important;}
div[data-baseweb="select"]>div{background:#1a1a1a!important;border-color:var(--border)!important;color:white!important;border-radius:8px!important;}
div[data-baseweb="select"]>div:hover{border-color:var(--red)!important;}

/* Download button */
[data-testid="stDownloadButton"] button{background:rgba(22,22,22,0.6)!important;border:1px solid var(--border)!important;color:var(--red)!important;font-family:'Inter',sans-serif!important;font-size:0.75rem!important;font-weight:600!important;border-radius:8px!important;letter-spacing:1px!important;text-transform:uppercase!important;}
[data-testid="stDownloadButton"] button:hover{background:rgba(224,58,62,0.1)!important;border-color:var(--red)!important;color:white!important;}

/* Scrollbar */
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:var(--dark);}
::-webkit-scrollbar-thumb{background:#333;border-radius:10px;}
::-webkit-scrollbar-thumb:hover{background:var(--red);}

/* Footer */
.footer{text-align:center;padding:2rem 0 1rem;color:#444;font-family:'Inter',sans-serif;font-size:0.68rem;letter-spacing:1.5px;text-transform:uppercase;border-top:1px solid rgba(255,255,255,0.05);margin-top:3rem;}
.footer a{color:#555!important;text-decoration:none!important;transition:color 0.2s!important;}
.footer a:hover{color:var(--red)!important;}
hr{border:none!important;border-top:1px solid rgba(255,255,255,0.05)!important;}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def normalize_col(col):
    col = pd.to_numeric(col, errors='coerce').fillna(0)
    mn, mx = col.min(), col.max()
    return col * 0 if mx == mn else (col - mn) / (mx - mn)

def recalculate(df):
    if df.empty: return df
    df = df.copy()
    for c in ['Gls_p90','SoT%','Ast','PrgP_proxy','Scoring_Context_Bonus','Market_Value_M','Age_num','90s']:
        if c not in df.columns: df[c] = 0
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    df['norm_gls_p90'] = normalize_col(df['Gls_p90'])
    df['norm_sot_pct']  = normalize_col(df['SoT%'])
    df['norm_ast']      = normalize_col(df['Ast'])
    df['norm_prgp']     = normalize_col(df['PrgP_proxy'])
    df['norm_context']  = normalize_col(df['Scoring_Context_Bonus'])
    df['Perf_Score'] = (
        df['norm_gls_p90']*0.30 + df['norm_sot_pct']*0.18 +
        df['norm_ast']*0.22 + df['norm_prgp']*0.18 + df['norm_context']*0.12
    ).round(3)
    df['Value_Score']      = (df['Perf_Score'] / df['Market_Value_M'].clip(lower=0.1) * 100).round(3)
    df['Value_Score_norm'] = (normalize_col(df['Value_Score']) * 100).round(1)
    df['Age_bonus']        = df['Age_num'].apply(lambda x: 1.2 if x<=23 else (1.1 if x<=25 else 1.0))
    df['Final_Score']      = (df['Value_Score_norm'] * df['Age_bonus']).round(1)
    return df

@st.cache_data
def load_data(file=None):
    try:
        if file is not None:
            return recalculate(pd.read_csv(file))
        for path in ["data/processed/ligue1_final.csv","ligue1_final.csv","data/processed/lique1_final.csv"]:
            if os.path.exists(path):
                return recalculate(pd.read_csv(path))
        # Demo fallback
        data = {
            'Player':['Aubameyang','Ansu Fati','Adrien Thomasson','Wesley Said','Martial Godo','Esteban Lepaul'],
            'Nation':['GAB','ESP','FRA','FRA','CMR','FRA'],
            'Pos_primary':['FW','MF','MF','FW','MF','FW'],
            'Squad':['Marseille','Monaco','Lens','Lens','Strasbourg','Rennes'],
            'Age_num':[36,23,32,30,22,25],
            'League':['Ligue 1']*6,
            '90s':[13.6,6.4,21.3,18.5,14.2,19.8],
            'Gls':[6,8,2,10,7,11],
            'Ast':[5,0,6,2,1,3],
            'Gls_p90':[0.44,1.25,0.09,0.54,0.49,0.56],
            'SoT%':[61.3,58.3,28.6,48.8,54.2,44.2],
            'Market_Value_M':[4,6,5,8,8,15],
            'PrgP_proxy':[0,0,6,2,1,3],
            'Scoring_Context_Bonus':[0.07,0.15,0.12,0.08,0.10,0.09],
            'Defense_Hardness':[0.59,0.41,0.69,0.69,0.53,0.42],
            'Peak_Value_M':[40,20,5,8,8,15],
        }
        return recalculate(pd.DataFrame(data))
    except Exception as e:
        st.error(f"❌ خطأ: {str(e)}")
        return recalculate(pd.DataFrame({'Player':['Error'],'Age_num':[25],'Gls':[0],'Ast':[0],'Gls_p90':[0],'SoT%':[0],'Market_Value_M':[1],'90s':[1]}))

def img_to_b64(path):
    for p in [path, "assets/brentford_logo.png", "assets/brentford_logo.jpg", "assets/rentford_logo.jpg"]:
        if os.path.exists(p):
            with open(p,"rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

# For go.Figure charts (full control)
LAYOUT = dict(
    plot_bgcolor='rgba(15,15,15,0.4)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e8e8e8', family='Inter', size=11),
    legend=dict(bgcolor='rgba(20,20,20,0.7)', bordercolor='rgba(224,58,62,0.2)', font=dict(color='#e8e8e8')),
    margin=dict(t=50, b=30, l=10, r=10),
)

# For px charts - apply AFTER creation via .update_layout()
def apply_theme(fig, title_text='', height=400):
    fig.update_layout(
        plot_bgcolor='rgba(15,15,15,0.4)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8e8e8', family='Inter', size=11),
        legend=dict(bgcolor='rgba(20,20,20,0.7)', bordercolor='rgba(224,58,62,0.2)', font=dict(color='#e8e8e8')),
        margin=dict(t=50, b=30, l=10, r=10),
        height=height,
    )
    if title_text:
        fig.update_layout(title=dict(text=title_text, font=dict(color='white', family='Bebas Neue', size=20)))
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
    return fig

def tl(text, size=20):
    """Chart title helper"""
    return dict(text=text, font=dict(color='white', family='Bebas Neue', size=size))



# ─── HEADER ──────────────────────────────────────────────────────────────────
logo_b64  = img_to_b64("assets/brentford_logo.png")
logo_html = f'<img class="header-logo" src="data:image/png;base64,{logo_b64}"/>' if logo_b64 else '<div style="font-size:3.5rem;">🐝</div>'

st.markdown(f"""
<div class="header-wrap">
  {logo_html}
  <div>
    <div class="main-title">BRENTFORD FC <span>//</span> SCOUTING INTEL</div>
    <div class="main-sub">Undervalued Player Detection • Value Score Algorithm • Schedule-Adjusted Analytics</div>
    <div class="social-links">
      <a class="social-btn" href="https://www.linkedin.com/in/goda-emad/" target="_blank">🔗 LinkedIn</a>
      <a class="social-btn" href="https://github.com/Goda-Emad/brentford-scouting" target="_blank">🐙 GitHub</a>
      <a class="social-btn" href="tel:+201126242932">📞 +20 112 624 2932</a>
    </div>
  </div>
</div>""", unsafe_allow_html=True)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.3rem;color:white;letter-spacing:2px;margin-bottom:1rem;padding-bottom:0.7rem;border-bottom:1px solid rgba(224,58,62,0.25);">⚙️ SCOUT FILTERS</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("📂 Add New League CSV", type=["csv"],
                                 help="Same format → auto merges as new league")
    df_base = load_data(uploaded)

    leagues  = sorted(df_base['League'].dropna().unique()) if 'League' in df_base.columns else ['Ligue 1']
    sel_league = st.multiselect("🌍 League", leagues, default=leagues)

    positions  = sorted(df_base['Pos_primary'].dropna().unique())
    sel_pos    = st.multiselect("📍 Position", positions, default=positions)

    age_range  = st.slider("🎂 Age Range", int(df_base['Age_num'].min()), int(df_base['Age_num'].max()),
                            (int(df_base['Age_num'].min()), int(df_base['Age_num'].max())))
    budget     = st.slider("💶 Max Market Value (€m)", 1.0, float(df_base['Market_Value_M'].max()),
                            float(df_base['Market_Value_M'].max()))
    min_90s    = st.slider("⏱️ Min 90s Played", 0.0, float(df_base['90s'].max()), 3.0, step=0.5)

    st.markdown("---")
    top_n = st.selectbox("📊 Show Top N Targets", [10,15,20,30,50], index=2)

    st.markdown("""
    <div style="margin-top:1.5rem;padding:1rem;background:rgba(224,58,62,0.06);
    border:1px solid rgba(224,58,62,0.18);border-radius:10px;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:0.9rem;color:#e03a3e;letter-spacing:1.5px;margin-bottom:0.5rem;">
        VALUE SCORE FORMULA</div>
      <div style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;line-height:2;">
        Goals/90 × 0.30<br>Shot Acc × 0.18<br>Assists × 0.22<br>
        Prog Passes × 0.18<br>Schedule Adj × 0.12<br>
        <span style="color:#444;">÷ Market Value × Age Bonus</span>
      </div>
    </div>
    <div style="margin-top:1rem;font-family:'Inter',sans-serif;font-size:0.63rem;color:#333;text-align:center;">
      FBref + Transfermarkt • Dec 2025
    </div>""", unsafe_allow_html=True)


# ─── FILTER ──────────────────────────────────────────────────────────────────
df = df_base.copy()
if sel_league and 'League' in df.columns: df = df[df['League'].isin(sel_league)]
if sel_pos:                               df = df[df['Pos_primary'].isin(sel_pos)]
df = df[
    (df['Age_num']       >= age_range[0]) & (df['Age_num']       <= age_range[1]) &
    (df['Market_Value_M'] <= budget)      & (df['90s']            >= min_90s)
].sort_values('Final_Score', ascending=False).reset_index(drop=True)


# ─── KPIs ────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
kpis = [
    (len(df),                              "Players Scouted"),
    (f"€{df['Market_Value_M'].mean():.1f}m","Avg Market Value"),
    (f"{df['Final_Score'].max():.0f}",      "Top Value Score"),
    (f"{df['Gls_p90'].mean():.2f}",         "Avg Goals / 90"),
    (f"{df['SoT%'].mean():.1f}%",           "Avg Shot Accuracy"),
]
for col,(val,lbl) in zip([k1,k2,k3,k4,k5], kpis):
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── TABS ────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4 = st.tabs(["🎯  Top Targets","📊  Value Analysis","🔬  Deep Dive","📋  Full Dataset"])


# ════════ TAB 1: TOP TARGETS ══════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-title">TOP TARGETS</div>', unsafe_allow_html=True)

    for rank, (_, row) in enumerate(df.head(top_n).iterrows(), 1):
        score_pct = min(row['Final_Score']/130*100, 100)
        h = row.get('Defense_Hardness', 0.5)
        sch  = ('badge-g badge','🔴 Hard Sch') if h>=0.6 else (('badge-yellow badge','🟡 Mid Sch') if h>=0.4 else ('badge-green badge','🟢 Easy Sch'))
        age  = int(row['Age_num'])
        ab   = '<span class="badge">🌟 U23</span>' if age<=23 else ('<span class="badge-g badge">Prime</span>' if age<=26 else '<span class="badge-g badge">Veteran</span>')

        st.markdown(f"""
        <div class="pcard">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
            <div style="flex:1;">
              <div style="color:#e03a3e;font-family:'Inter',sans-serif;font-size:0.63rem;font-weight:700;letter-spacing:2px;">#{rank:02d}</div>
              <div class="pname">{row['Player']}</div>
              <div class="pmeta">{row.get('Squad','—')} &nbsp;•&nbsp; {row.get('League','—')} &nbsp;•&nbsp; Age {age}</div>
              <div style="margin-top:0.5rem;">
                <span class="badge">{row.get('Pos_primary','—')}</span>{ab}
                <span class="{sch[0]}">{sch[1]}</span>
              </div>
            </div>
            <div style="text-align:right;flex-shrink:0;">
              <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:#e03a3e;line-height:1;">{row['Final_Score']:.0f}</div>
              <div style="font-size:0.6rem;color:#666;text-transform:uppercase;letter-spacing:1px;">Value Score</div>
              <div style="font-size:0.82rem;color:white;margin-top:0.4rem;font-weight:500;">
                ⚽{int(row['Gls'])}G &nbsp; 🅰️{int(row['Ast'])}A &nbsp; 🎯{row['SoT%']:.0f}% &nbsp; 💶€{row['Market_Value_M']:.0f}m
              </div>
            </div>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width:{score_pct:.0f}%"></div></div>
        </div>""", unsafe_allow_html=True)


# ════════ TAB 2: VALUE ANALYSIS ═══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-title">VALUE ANALYSIS</div>', unsafe_allow_html=True)

    # Mini stats
    s1,s2,s3,s4 = st.columns(4)
    for col,(val,lbl,color) in zip([s1,s2,s3,s4],[
        (f"{df['Final_Score'].max():.0f}","TOP SCORE","#e03a3e"),
        (f"€{df['Market_Value_M'].max():.0f}M","MAX VALUE","white"),
        (f"{df['Final_Score'].mean():.1f}","AVG SCORE","#f5a623"),
        (str(len(df)),"PLAYERS","#2ecc71"),
    ]):
        with col:
            st.markdown(f'<div class="glass-card" style="text-align:center;padding:1rem;"><div style="font-size:1.6rem;color:{color};font-family:\'Bebas Neue\';">{val}</div><div style="color:#666;font-size:0.68rem;">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.scatter(df, x='Market_Value_M', y='Final_Score', hover_name='Player',
            hover_data={'Squad':True,'Age_num':True,'Gls':True,'Ast':True,'Market_Value_M':':.1f','Final_Score':':.1f'},
            color='Pos_primary', size='Gls', size_max=20,
            color_discrete_sequence=['#e03a3e','#f5a623','#4a90e2','#2ecc71','#9b59b6'],
            labels={'Market_Value_M':'Market Value (€m)','Final_Score':'Value Score','Pos_primary':'Position'})
        apply_theme(fig, 'Value Score vs Market Value', 400)
        fig.add_shape(type='line', x0=0, y0=55, x1=df['Market_Value_M'].max(), y1=55,
                      line=dict(color='rgba(224,58,62,0.3)', dash='dash', width=1))
        fig.add_annotation(x=df['Market_Value_M'].max()*0.6, y=59,
                           text="Brentford Target Zone", font=dict(color='rgba(224,58,62,0.6)',size=10), showarrow=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        t10 = df.nlargest(10,'Final_Score')
        fig2 = go.Figure(go.Bar(
            x=t10['Final_Score'], y=t10['Player'], orientation='h',
            marker=dict(color=t10['Final_Score'], colorscale=[[0,'#1a0505'],[0.5,'#8b1a1a'],[1,'#e03a3e']], showscale=False,
                        line=dict(color='rgba(224,58,62,0.3)',width=1)),
            text=[f"€{v:.0f}M | ⚽{int(g)}G" for v,g in zip(t10['Market_Value_M'],t10['Gls'])],
            textposition='outside', textfont=dict(color='#666',size=10)))
        fig2.update_layout(
            plot_bgcolor='rgba(15,15,15,0.4)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e8e8e8', family='Inter', size=11),
            legend=dict(bgcolor='rgba(20,20,20,0.7)', font=dict(color='#e8e8e8')),
            title=dict(text='Top 10 — Value Score Ranking', font=dict(color='white', family='Bebas Neue', size=20)),
            height=400, yaxis=dict(autorange='reversed', gridcolor='rgba(255,255,255,0.04)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)'), margin=dict(t=50,b=30,l=10,r=80))
        st.plotly_chart(fig2, use_container_width=True)

    # Efficiency
    st.markdown('<div class="sec-title">⚽ GOALS EFFICIENCY</div>', unsafe_allow_html=True)
    avg_g = df['Gls_p90'].mean(); avg_s = df['SoT%'].mean()
    fig3 = px.scatter(df, x='Gls_p90', y='SoT%', hover_name='Player',
        hover_data={'Squad':True,'Gls':True,'Ast':True},
        color='Final_Score', size='Market_Value_M', size_max=20,
        color_continuous_scale=[[0,'#0d0d0d'],[0.4,'#8b1a1a'],[1,'#e03a3e']],
        labels={'Gls_p90':'Goals per 90','SoT%':'Shot on Target %','Final_Score':'Value Score'})
    apply_theme(fig3, 'Scoring Efficiency: Goals/90 vs Shot Accuracy', 400)
    fig3.update_layout(coloraxis_colorbar=dict(title='Score', tickfont=dict(color='#666'), bgcolor='rgba(20,20,20,0.6)'))
    fig3.add_hline(y=avg_s, line_dash="dash", line_color="rgba(255,255,255,0.15)",
                   annotation_text=f"Avg: {avg_s:.1f}%", annotation_font=dict(color='#666',size=10))
    fig3.add_vline(x=avg_g, line_dash="dash", line_color="rgba(255,255,255,0.15)",
                   annotation_text=f"Avg: {avg_g:.2f}", annotation_font=dict(color='#666',size=10))
    st.plotly_chart(fig3, use_container_width=True)

    # Schedule difficulty
    if 'Defense_Hardness' in df.columns:
        st.markdown('<div class="sec-title">📅 SCHEDULE DIFFICULTY</div>', unsafe_allow_html=True)
        sh = df.groupby('Squad')['Defense_Hardness'].mean().sort_values().reset_index()
        fig4 = go.Figure(go.Bar(x=sh['Defense_Hardness'], y=sh['Squad'], orientation='h',
            marker=dict(color=sh['Defense_Hardness'], colorscale=[[0,'#1a0505'],[1,'#e03a3e']], showscale=False)))
        fig4.update_layout(
            plot_bgcolor='rgba(15,15,15,0.4)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e8e8e8', family='Inter', size=11),
            title=dict(text='Defense Hardness (higher = harder to score against)', font=dict(color='white', family='Bebas Neue', size=20)),
            height=400, yaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)'))
        st.plotly_chart(fig4, use_container_width=True)


# ════════ TAB 3: DEEP DIVE ════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-title">🔬 PLAYER DEEP DIVE</div>', unsafe_allow_html=True)

    col_sel, col_hint = st.columns([2,1])
    with col_sel:
        search = st.text_input("🔍 Search Player", placeholder="Type player name...")
        filtered_p = [p for p in df['Player'].tolist() if search.lower() in p.lower()] if search else df['Player'].tolist()
        selected = st.multiselect("Select Players to Compare (max 3)", filtered_p,
                                   default=filtered_p[:min(2,len(filtered_p))], max_selections=3)
    with col_hint:
        st.markdown("""
        <div class="glass-card" style="padding:1rem;margin-top:1.6rem;">
          <div style="color:#888;font-size:0.72rem;">📊 METRICS COMPARED</div>
          <div style="color:white;font-size:0.82rem;margin-top:0.4rem;line-height:1.8;">
            ⚽ Goals &nbsp;|&nbsp; 🅰️ Assists<br>
            🎯 Accuracy &nbsp;|&nbsp; 💶 Value<br>
            📈 Score &nbsp;|&nbsp; 📅 Schedule
          </div>
        </div>""", unsafe_allow_html=True)

    if selected:
        st.markdown("---")
        colors_list = ['#e03a3e','#f5a623','#4a90e2']
        cols = st.columns(len(selected))

        for idx,(col,pname) in enumerate(zip(cols,selected)):
            r = df[df['Player']==pname].iloc[0]
            pc = colors_list[idx]
            h  = r.get('Defense_Hardness',0.5)
            sch_icon = "🔴" if h>=0.6 else ("🟡" if h>=0.4 else "🟢")
            peak = r.get('Peak_Value_M', r['Market_Value_M'])
            vc   = ((r['Market_Value_M']-peak)/peak*100) if peak>0 else 0
            sot_w = min(r['SoT%'],100)
            val_w = min((1-r['Market_Value_M']/df['Market_Value_M'].max())*100,100)

            with col:
                st.markdown(f"""
                <div class="glass-card" style="padding:1.5rem;border-left:4px solid {pc};">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:white;">{pname}</div>
                    <span style="background:{pc}22;color:{pc};padding:3px 9px;border-radius:12px;font-size:0.65rem;">#{idx+1}</span>
                  </div>
                  <div style="color:#888;font-size:0.72rem;margin:0.3rem 0 1.2rem;">
                    {r.get('Squad','—')} • {r.get('League','—')} • Age {int(r['Age_num'])}
                  </div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;text-align:center;margin-bottom:1rem;">
                    <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:0.8rem;">
                      <div style="font-size:2rem;">⚽</div>
                      <div style="font-size:1.5rem;color:white;font-family:'Bebas Neue';">{int(r.get('Gls',0))}</div>
                      <div style="color:#555;font-size:0.65rem;">GOALS</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:0.8rem;">
                      <div style="font-size:2rem;">🅰️</div>
                      <div style="font-size:1.5rem;color:white;font-family:'Bebas Neue';">{int(r.get('Ast',0))}</div>
                      <div style="color:#555;font-size:0.65rem;">ASSISTS</div>
                    </div>
                  </div>
                  <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:1rem;margin-bottom:0.8rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                      <span style="color:#888;font-size:0.75rem;">🎯 Shot Accuracy</span>
                      <span style="color:white;">{r['SoT%']:.1f}%</span>
                    </div>
                    <div class="bar-bg"><div class="bar-fill" style="width:{sot_w:.0f}%"></div></div>
                    <div style="display:flex;justify-content:space-between;margin:0.8rem 0 0.4rem;">
                      <span style="color:#888;font-size:0.75rem;">💶 Market Value</span>
                      <span style="color:white;">€{r['Market_Value_M']:.0f}m</span>
                    </div>
                    <div class="bar-bg"><div class="bar-fill" style="width:{val_w:.0f}%"></div></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <span style="color:#888;font-size:0.72rem;">📊 Score</span>
                      <span style="color:{pc};font-size:1.5rem;font-family:'Bebas Neue';margin-left:0.4rem;">{r['Final_Score']:.0f}</span>
                    </div>
                    <div style="font-size:0.72rem;color:#666;">
                      {sch_icon} {h:.2f} &nbsp;|&nbsp; Peak €{peak:.0f}m
                      <span style="color:{'#2ecc71' if vc>=0 else '#e03a3e'};">({vc:+.0f}%)</span>
                    </div>
                  </div>
                  <div style="margin-top:0.8rem;">
                    {'<span class="badge-green badge">🌟 U23 Bonus</span>' if r['Age_num']<=23 else ''}
                    {'<span class="badge-yellow badge">⚡ Prime Age</span>' if 23<r['Age_num']<=26 else ''}
                  </div>
                </div>""", unsafe_allow_html=True)

        # Radar
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-title">📡 RADAR COMPARISON</div>', unsafe_allow_html=True)
        metrics = ['norm_gls_p90','norm_sot_pct','norm_ast','norm_prgp','norm_context']
        labels  = ['⚽ Goals/90','🎯 Shot Acc','🅰️ Assists','📤 Prog Pass','📅 Schedule']
        fig_r   = go.Figure()
        for pname,pc in zip(selected,colors_list):
            r    = df[df['Player']==pname].iloc[0]
            vals = [float(r.get(m,0)) for m in metrics] + [float(r.get(metrics[0],0))]
            lbs  = labels+[labels[0]]
            rgba = tuple(int(pc.lstrip('#')[i:i+2],16) for i in (0,2,4))
            fig_r.add_trace(go.Scatterpolar(r=vals, theta=lbs, fill='toself', name=pname,
                line=dict(color=pc,width=3), fillcolor=f'rgba{rgba+(0.15,)}'))
        fig_r.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e8e8e8', family='Inter'),
            polar=dict(bgcolor='rgba(15,15,15,0.5)',
                       radialaxis=dict(visible=True,range=[0,1],color='#444',gridcolor='rgba(255,255,255,0.06)',tickfont=dict(color='#555')),
                       angularaxis=dict(color='#666',gridcolor='rgba(255,255,255,0.06)')),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e8e8e8',family='Inter'),
            legend=dict(bgcolor='rgba(20,20,20,0.7)',bordercolor='rgba(224,58,62,0.2)',font=dict(color='#e8e8e8')),
            title=dict(text='Player Comparison Radar',font=dict(family='Bebas Neue',size=22,color='white')),
            height=480, margin=dict(t=60,b=20,l=20,r=20))
        st.plotly_chart(fig_r, use_container_width=True)

        # Goals & Assists comparison
        if len(selected) > 1:
            st.markdown('<div class="sec-title">📊 PERFORMANCE COMPARISON</div>', unsafe_allow_html=True)
            cc1,cc2 = st.columns(2)
            with cc1:
                fig_ga = go.Figure()
                fig_ga.add_trace(go.Bar(name='Goals', x=selected,
                    y=[int(df[df['Player']==p]['Gls'].values[0]) for p in selected],
                    marker_color='#e03a3e', text=[int(df[df['Player']==p]['Gls'].values[0]) for p in selected], textposition='inside'))
                fig_ga.add_trace(go.Bar(name='Assists', x=selected,
                    y=[int(df[df['Player']==p]['Ast'].values[0]) for p in selected],
                    marker_color='#f5a623', text=[int(df[df['Player']==p]['Ast'].values[0]) for p in selected], textposition='inside'))
                fig_ga.update_layout(
                    plot_bgcolor='rgba(15,15,15,0.4)', paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e8e8e8', family='Inter', size=11),
                    barmode='group',
                    title=dict(text='Goals & Assists', font=dict(color='white', family='Bebas Neue', size=20)),
                    height=320, legend=dict(bgcolor='rgba(20,20,20,0.7)', font=dict(color='#e8e8e8')))
                st.plotly_chart(fig_ga, use_container_width=True)

            with cc2:
                # Recommendation
                best  = df[df['Player'].isin(selected)].sort_values('Final_Score',ascending=False).iloc[0]
                worst = df[df['Player'].isin(selected)].sort_values('Final_Score',ascending=False).iloc[-1]
                st.markdown(f"""
                <div class="glass-card" style="padding:1.5rem;text-align:center;height:100%;display:flex;flex-direction:column;justify-content:center;">
                  <div style="color:#e03a3e;font-family:'Bebas Neue';font-size:1.2rem;letter-spacing:2px;">🏆 RECOMMENDED</div>
                  <div style="font-size:1.8rem;color:white;font-family:'Bebas Neue';margin:0.5rem 0;">{best['Player']}</div>
                  <div style="color:#888;font-size:0.8rem;">over {worst['Player']}</div>
                  <div style="display:flex;justify-content:center;gap:2rem;margin:1.5rem 0;">
                    <div><span style="color:#888;">Score</span><span style="color:#e03a3e;font-size:1.5rem;font-family:'Bebas Neue';margin-left:0.5rem;">{best['Final_Score']:.0f}</span></div>
                    <div><span style="color:#888;">vs</span><span style="color:#555;margin-left:0.5rem;">{worst['Final_Score']:.0f}</span></div>
                  </div>
                  <div style="color:#666;font-size:0.75rem;">Better value • Age {int(best['Age_num'])} • €{best['Market_Value_M']:.0f}m</div>
                </div>""", unsafe_allow_html=True)

    else:
        st.info("👆 اختر لاعبين للمقارنة")


# ════════ TAB 4: FULL DATASET ════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-title">📋 FULL DATASET</div>', unsafe_allow_html=True)

    # Toolbar
    t1,t2,t3,t4 = st.columns([3,2,2,1])
    with t1:
        all_cols = ['Player','Nation','Pos_primary','Squad','Age_num','League','Gls','Ast',
                    'Gls_p90','SoT%','Market_Value_M','Perf_Score','Final_Score','Defense_Hardness']
        av_cols  = [c for c in all_cols if c in df.columns]
        sel_cols = st.multiselect("📌 Columns", av_cols,
                                   default=['Player','Squad','Age_num','Pos_primary','Gls','Ast','SoT%','Market_Value_M','Final_Score'])
    with t2:
        sort_options = [c for c in ['Final_Score','Market_Value_M','Gls','Age_num','SoT%'] if c in df.columns]
        sort_by = st.selectbox("🔽 Sort By", sort_options)
    with t3:
        rows_to_show = st.selectbox("📊 Rows", [10,25,50,100,len(df)], index=2)
    with t4:
        asc = st.checkbox("🔄 Asc", False)

    if sel_cols:
        disp = df[sel_cols].sort_values(sort_by, ascending=asc).head(rows_to_show).copy()
        fmt  = {'SoT%':'{:.1f}%','Gls_p90':'{:.3f}','Market_Value_M':'€{:.0f}m',
                'Final_Score':'{:.1f}','Perf_Score':'{:.3f}','Defense_Hardness':'{:.2f}'}
        fmt  = {k:v for k,v in fmt.items() if k in disp.columns}
        st.dataframe(disp.style.format(fmt), use_container_width=True, height=480)

    # Quick stats
    st.markdown('<div class="sec-title">📊 DATA INSIGHTS</div>', unsafe_allow_html=True)
    s1,s2,s3,s4,s5 = st.columns(5)
    for col,(val,lbl,c) in zip([s1,s2,s3,s4,s5],[
        (len(df),"Total Players","#e03a3e"),
        (df['Squad'].nunique(),"Teams","white"),
        (df['Pos_primary'].nunique(),"Positions","#f5a623"),
        (int(df['Gls'].sum()),"Total Goals","#2ecc71"),
        (f"{df['Age_num'].mean():.1f}","Avg Age","#4a90e2"),
    ]):
        with col:
            st.markdown(f'<div class="glass-card" style="text-align:center;padding:0.8rem;"><div style="font-size:1.6rem;color:{c};font-family:\'Bebas Neue\';">{val}</div><div style="color:#555;font-size:0.65rem;">{lbl}</div></div>', unsafe_allow_html=True)

    # Charts
    st.markdown("<br>", unsafe_allow_html=True)
    ci1,ci2 = st.columns(2)
    with ci1:
        pos_c = df['Pos_primary'].value_counts()
        fig_p = go.Figure(go.Pie(labels=pos_c.index, values=pos_c.values, hole=0.45,
            marker_colors=['#e03a3e','#f5a623','#4a90e2','#2ecc71','#9b59b6']))
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e8e8e8', family='Inter'),
            title=dict(text='Position Distribution', font=dict(color='white', family='Bebas Neue', size=20)),
            legend=dict(bgcolor='rgba(20,20,20,0.7)', font=dict(color='#e8e8e8')), height=300)
        st.plotly_chart(fig_p, use_container_width=True)
    with ci2:
        fig_a = go.Figure(go.Histogram(x=df['Age_num'], nbinsx=15,
            marker_color='#e03a3e', opacity=0.7))
        fig_a.update_layout(plot_bgcolor='rgba(15,15,15,0.4)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e8e8e8', family='Inter', size=11),
            title=dict(text='Age Distribution', font=dict(color='white', family='Bebas Neue', size=20)),
            height=300,
                             xaxis=dict(title='Age',gridcolor='rgba(255,255,255,0.05)'),
                             yaxis=dict(title='Count',gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig_a, use_container_width=True)

    # Downloads
    st.markdown("---")
    d1,d2,d3,_ = st.columns([1,1,1,3])
    with d1:
        st.download_button("📥 Full Dataset", df.to_csv(index=False).encode('utf-8'),
                           "brentford_scouting_full.csv","text/csv", use_container_width=True)
    with d2:
        st.download_button("📥 Top 50", df.head(50).to_csv(index=False).encode('utf-8'),
                           "brentford_top50.csv","text/csv", use_container_width=True)
    with d3:
        st.download_button("📥 Top 10", df.head(10).to_csv(index=False).encode('utf-8'),
                           "brentford_top10.csv","text/csv", use_container_width=True)


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:0.8rem;">
    <span>🐝 BRENTFORD FC SCOUTING SYSTEM</span>
    <span>⚽ SEASON 2025-26</span>
    <span>📊 FBREF + TRANSFERMARKT</span>
  </div>
  <div style="display:flex;justify-content:center;gap:1.5rem;">
    <a href="https://www.linkedin.com/in/goda-emad/" target="_blank">🔗 LinkedIn</a>
    <a href="https://github.com/Goda-Emad/brentford-scouting" target="_blank">🐙 GitHub</a>
    <span style="color:#444;">📞 +20 112 624 2932</span>
  </div>
  <div style="margin-top:0.8rem;color:#333;">Developed by Goda Emad © 2026</div>
</div>""", unsafe_allow_html=True)
