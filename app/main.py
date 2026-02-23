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

# ─── BACKGROUND IMAGE ────────────────────────────────────────────────────────
def inject_background():
    for path in ["assets/bg_stadium.jpg","assets/bg_stadium.jpeg","bg_stadium.jpg"]:
        if os.path.exists(path):
            with open(path,"rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            ext = "png" if path.endswith(".png") else "jpeg"
            st.markdown(f"""<style>
.stApp {{
    background-image: url("data:image/{ext};base64,{b64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}
.stApp > .main > .block-container,
section[data-testid="stSidebar"] > div,
[data-testid="stAppViewContainer"] {{
    background: transparent !important;
}}
</style>""", unsafe_allow_html=True)
            return
    # fallback
    st.markdown("""<style>
.stApp {{ background: linear-gradient(135deg,#0a0a0a 0%,#1a0505 50%,#0a0a0a 100%) !important; }}
</style>""", unsafe_allow_html=True)

inject_background()

# ─── LOAD EXTERNAL CSS ───────────────────────────────────────────────────────
def load_css():
    p = pathlib.Path("assets/style.css")
    if p.exists():
        st.markdown(f"<style>{p.read_text()}</style>", unsafe_allow_html=True)
load_css()

# ─── INLINE CSS ──────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');
:root{--red:#e03a3e;--black:#0a0a0a;--card:rgba(15,15,15,0.82);--border:rgba(224,58,62,0.28);--text:#f0f0f0;--muted:#888;}

/* Global dark overlay on stApp */
.stApp::before{content:'';position:fixed;inset:0;background:rgba(5,5,5,0.78);z-index:0;pointer-events:none;}
.stApp>*{position:relative;z-index:1;}

/* Sidebar */
[data-testid="stSidebar"]{background:rgba(8,8,8,0.88)!important;backdrop-filter:blur(20px)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}

/* Header */
.header-wrap{background:rgba(8,8,8,0.78);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border:1px solid var(--border);border-radius:16px;padding:1.8rem 2.2rem;margin-bottom:1.5rem;
  position:relative;overflow:hidden;display:flex;align-items:center;gap:2rem;
  box-shadow:0 8px 32px rgba(0,0,0,0.6);}
.header-wrap::before{content:'';position:absolute;top:-80px;right:-60px;width:380px;height:380px;
  background:radial-gradient(circle,rgba(224,58,62,0.18) 0%,transparent 70%);}
.header-wrap::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:1px;
  background:linear-gradient(90deg,transparent,var(--red),transparent);}
.header-logo{width:70px;height:70px;border-radius:50%;border:2px solid var(--border);object-fit:contain;transition:transform 0.3s;}
.header-logo:hover{transform:scale(1.1) rotate(5deg);}
.main-title{font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:white;letter-spacing:4px;line-height:1;margin:0;}
.main-title span{color:var(--red);}
.main-sub{font-family:'Inter',sans-serif;font-size:0.72rem;color:var(--muted);letter-spacing:2.5px;text-transform:uppercase;margin-top:0.4rem;}
.social-links{margin-top:0.8rem;display:flex;gap:0.6rem;flex-wrap:wrap;}
.social-btn{display:inline-flex;align-items:center;gap:5px;background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.12);color:#bbb!important;font-family:'Inter',sans-serif;
  font-size:0.68rem;font-weight:500;padding:5px 14px;border-radius:30px;
  text-decoration:none!important;transition:all 0.2s;}
.social-btn:hover{border-color:var(--red);color:white!important;background:rgba(224,58,62,0.12);transform:translateY(-2px);}

/* KPI */
.kpi-card{background:rgba(12,12,12,0.82);backdrop-filter:blur(12px);border:1px solid var(--border);
  border-radius:12px;padding:1.1rem 1.3rem;position:relative;overflow:hidden;transition:all 0.25s;}
.kpi-card:hover{transform:translateY(-3px);border-color:var(--red);box-shadow:0 8px 24px rgba(224,58,62,0.18);}
.kpi-card::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,var(--red),transparent);}
.kpi-val{font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:white;line-height:1;}
.kpi-lbl{font-family:'Inter',sans-serif;font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.8px;margin-top:0.3rem;}

/* Glass Card */
.glass-card{background:rgba(12,12,12,0.80);backdrop-filter:blur(12px);border:1px solid var(--border);
  border-radius:12px;padding:1.2rem;transition:all 0.25s;}
.glass-card:hover{border-color:var(--red);box-shadow:0 6px 20px rgba(224,58,62,0.12);}

/* Player card */
.pcard{background:rgba(12,12,12,0.78);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.06);
  border-radius:12px;padding:1.1rem 1.4rem;margin-bottom:0.75rem;position:relative;overflow:hidden;transition:all 0.25s;}
.pcard::before{content:'';position:absolute;top:0;left:0;width:3px;height:0;background:var(--red);transition:height 0.3s;}
.pcard:hover::before{height:100%;}
.pcard:hover{background:rgba(25,25,25,0.85);border-color:rgba(224,58,62,0.4);box-shadow:0 6px 20px rgba(224,58,62,0.1);transform:translateX(4px);}
.pname{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:white;letter-spacing:1px;}
.pmeta{font-family:'Inter',sans-serif;font-size:0.7rem;color:var(--muted);margin-top:0.15rem;}
.bar-bg{background:rgba(255,255,255,0.08);border-radius:6px;height:5px;margin-top:0.8rem;overflow:hidden;}
.bar-fill{background:linear-gradient(90deg,#8b1a1a,var(--red),#ff7070);border-radius:6px;height:5px;}

/* Badges */
.badge{display:inline-block;background:rgba(224,58,62,0.15);border:1px solid var(--border);color:var(--red);
  font-size:0.62rem;font-family:'Inter',sans-serif;font-weight:600;padding:2px 9px;border-radius:20px;
  text-transform:uppercase;letter-spacing:1px;margin-right:4px;}
.badge-g{background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.1);color:var(--muted);}
.badge-green{background:rgba(46,204,113,0.1);border-color:rgba(46,204,113,0.3);color:#2ecc71;}
.badge-yellow{background:rgba(243,156,18,0.1);border-color:rgba(243,156,18,0.3);color:#f39c12;}

/* Section title */
.sec-title{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:white;letter-spacing:2.5px;
  border-left:3px solid var(--red);padding-left:0.8rem;margin:1.5rem 0 1rem;}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:rgba(10,10,10,0.6)!important;border-radius:10px!important;padding:4px!important;backdrop-filter:blur(10px)!important;}
[data-testid="stTabs"] [data-baseweb="tab"]{color:var(--muted)!important;font-family:'Inter',sans-serif!important;font-size:0.78rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:1px!important;border-radius:8px!important;}
[data-testid="stTabs"] [aria-selected="true"]{color:white!important;background:rgba(224,58,62,0.18)!important;border-bottom:2px solid var(--red)!important;}

/* Sidebar labels */
[data-testid="stSidebar"] label{font-family:'Inter',sans-serif!important;font-size:0.7rem!important;text-transform:uppercase!important;letter-spacing:1.5px!important;color:var(--muted)!important;}
div[data-baseweb="select"]>div{background:rgba(15,15,15,0.9)!important;border-color:var(--border)!important;color:white!important;border-radius:8px!important;}

/* Download button */
[data-testid="stDownloadButton"] button{background:rgba(15,15,15,0.8)!important;border:1px solid var(--border)!important;color:var(--red)!important;font-family:'Inter',sans-serif!important;font-size:0.75rem!important;font-weight:600!important;border-radius:8px!important;letter-spacing:1px!important;text-transform:uppercase!important;}
[data-testid="stDownloadButton"] button:hover{background:rgba(224,58,62,0.12)!important;color:white!important;}

/* Scrollbar */
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:rgba(0,0,0,0.3);}
::-webkit-scrollbar-thumb{background:#333;border-radius:10px;}
::-webkit-scrollbar-thumb:hover{background:var(--red);}

/* Footer */
.footer{text-align:center;padding:2rem 0 1rem;color:#444;font-family:'Inter',sans-serif;font-size:0.68rem;letter-spacing:1.5px;text-transform:uppercase;border-top:1px solid rgba(255,255,255,0.05);margin-top:3rem;}
.footer a{color:#555!important;text-decoration:none!important;transition:color 0.2s!important;}
.footer a:hover{color:var(--red)!important;}
hr{border:none!important;border-top:1px solid rgba(255,255,255,0.06)!important;}
</style>""", unsafe_allow_html=True)


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def normalize_col(col):
    col = pd.to_numeric(col, errors='coerce').fillna(0)
    mn, mx = col.min(), col.max()
    return col * 0 if mx == mn else (col - mn) / (mx - mn)

def recalculate(df):
    if df.empty: return df
    df = df.copy()
    for c in ['Gls_p90','SoT%','Ast','PrgP_proxy','Scoring_Context_Bonus','Market_Value_M','Age_num','90s','Gls']:
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
    except Exception as e:
        st.error(f"❌ Error: {e}")
    # Demo fallback
    data = {
        'Player':['Aubameyang','Ansu Fati','Wesley Said','Odsonne Edouard','Pavel Sulc','Elye Wahi','Adrien Thomasson','Gauthier Hein'],
        'Nation':['GAB','ESP','FRA','FRA','CZE','FRA','FRA','FRA'],
        'Pos_primary':['FW','MF','FW','FW','MF','FW','MF','MF'],
        'Squad':['Marseille','Monaco','Lens','Lens','Brest','Lens','Lens','Auxerre'],
        'Age_num':[36,23,28,27,24,22,32,29],
        'League':['Ligue 1']*8,
        '90s':[13.6,6.4,18.5,19.2,15.3,12.8,21.3,17.7],
        'Gls':[6,8,10,9,10,8,2,6],
        'Ast':[5,0,2,3,3,1,6,4],
        'Gls_p90':[0.44,1.25,0.54,0.47,0.65,0.63,0.09,0.34],
        'SoT%':[61.3,58.3,48.8,52.1,55.4,50.2,28.6,33.3],
        'Market_Value_M':[4,6,8,12,12,12,5,5],
        'Peak_Value_M':[40,20,8,20,40,40,5,5],
        'PrgP_proxy':[0,0,2,3,4,1,6,2],
        'Scoring_Context_Bonus':[0.077,0.153,0.083,0.094,0.088,0.083,0.123,0.039],
        'Defense_Hardness':[0.59,0.41,0.69,0.69,0.52,0.69,0.69,0.35],
    }
    return recalculate(pd.DataFrame(data))

def img_to_b64(path):
    for p in [path,"assets/brentford_logo.png","assets/brentford_logo.jpg","assets/rentford_logo.jpg","assets/rentford_logo.jpg"]:
        if os.path.exists(p):
            with open(p,"rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

def tl(text, size=20):
    return dict(text=text, font=dict(color='white', family='Bebas Neue', size=size))

LAYOUT = dict(
    plot_bgcolor='rgba(10,10,10,0.5)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e8e8e8', family='Inter', size=11),
    legend=dict(bgcolor='rgba(15,15,15,0.8)', bordercolor='rgba(224,58,62,0.2)', font=dict(color='#e8e8e8')),
    margin=dict(t=50, b=30, l=10, r=10),
)


# ─── HEADER ──────────────────────────────────────────────────────────────────
logo_b64  = img_to_b64("assets/brentford_logo.png")
logo_html = f'<img class="header-logo" src="data:image/png;base64,{logo_b64}"/>' if logo_b64 else \
            f'<img class="header-logo" src="data:image/jpeg;base64,{img_to_b64("assets/rentford_logo.jpg") or ""}"/>' if img_to_b64("assets/rentford_logo.jpg") else \
            '<div style="font-size:3.5rem;flex-shrink:0;">🐝</div>'

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
    uploaded   = st.file_uploader("📂 Add New League CSV", type=["csv"])
    df_base    = load_data(uploaded)
    leagues    = sorted(df_base['League'].dropna().unique()) if 'League' in df_base.columns else ['Ligue 1']
    sel_league = st.multiselect("🌍 League", leagues, default=leagues)
    positions  = sorted(df_base['Pos_primary'].dropna().unique())
    sel_pos    = st.multiselect("📍 Position", positions, default=positions)
    age_min, age_max = int(df_base['Age_num'].min()), int(df_base['Age_num'].max())
    age_range  = st.slider("🎂 Age Range", age_min, age_max, (age_min, age_max))
    max_val    = float(df_base['Market_Value_M'].max())
    budget     = st.slider("💶 Max Market Value (€m)", 1.0, max(max_val,1.1), max_val)
    max_90s    = float(df_base['90s'].max())
    min_90s    = st.slider("⏱️ Min 90s Played", 0.0, max(max_90s,1.0), 0.0, step=0.5)
    st.markdown("---")
    top_n = st.selectbox("📊 Show Top N Targets", [10,15,20,30,50], index=2)
    st.markdown("""<div style="margin-top:1.5rem;padding:1rem;background:rgba(224,58,62,0.07);border:1px solid rgba(224,58,62,0.18);border-radius:10px;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:0.9rem;color:#e03a3e;letter-spacing:1.5px;margin-bottom:0.5rem;">VALUE SCORE FORMULA</div>
    <div style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;line-height:2;">
    Goals/90 × 0.30<br>Shot Acc × 0.18<br>Assists × 0.22<br>Prog Passes × 0.18<br>Schedule Adj × 0.12<br>
    <span style="color:#444;">÷ Market Value × Age Bonus</span></div></div>""", unsafe_allow_html=True)


# ─── FILTER ──────────────────────────────────────────────────────────────────
df = df_base.copy()
if sel_league and 'League' in df.columns: df = df[df['League'].isin(sel_league)]
if sel_pos:                               df = df[df['Pos_primary'].isin(sel_pos)]
df = df[
    (df['Age_num'] >= age_range[0]) & (df['Age_num'] <= age_range[1]) &
    (df['Market_Value_M'] <= budget) & (df['90s'] >= min_90s)
].sort_values('Final_Score', ascending=False).reset_index(drop=True)


# ─── KPIs ────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
if len(df) > 0:
    kpis = [
        (len(df),                                    "Players Scouted"),
        (f"€{df['Market_Value_M'].mean():.1f}m",     "Avg Market Value"),
        (f"{df['Final_Score'].max():.0f}",            "Top Value Score"),
        (f"{df['Gls_p90'].mean():.2f}",               "Avg Goals / 90"),
        (f"{df['SoT%'].mean():.1f}%",                 "Avg Shot Accuracy"),
    ]
else:
    kpis = [(0,"Players Scouted"),("—","Avg Market Value"),("—","Top Score"),("—","Goals/90"),("—","Shot Acc")]

for col,(val,lbl) in zip([k1,k2,k3,k4,k5],kpis):
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4 = st.tabs(["🎯  Top Targets","📊  Value Analysis","🔬  Deep Dive","📋  Full Dataset"])


# ══════ TAB 1 ════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-title">TOP TARGETS</div>', unsafe_allow_html=True)
    if len(df) == 0:
        st.warning("⚠️ No players match the current filters. Try adjusting the sidebar.")
    else:
        for rank,(_, row) in enumerate(df.head(top_n).iterrows(), 1):
            score_pct = min(row['Final_Score']/130*100, 100)
            h   = row.get('Defense_Hardness', 0.5)
            sch = ('badge-g badge','🔴 Hard Sch') if h>=0.6 else (('badge-yellow badge','🟡 Mid Sch') if h>=0.4 else ('badge-green badge','🟢 Easy Sch'))
            age = int(row['Age_num'])
            ab  = '<span class="badge">🌟 U23</span>' if age<=23 else ('<span class="badge-g badge">Prime</span>' if age<=26 else '<span class="badge-g badge">Veteran</span>')
            st.markdown(f"""
            <div class="pcard">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
                <div style="flex:1;">
                  <div style="color:#e03a3e;font-family:'Inter',sans-serif;font-size:0.63rem;font-weight:700;letter-spacing:2px;">#{rank:02d}</div>
                  <div class="pname">{row['Player']}</div>
                  <div class="pmeta">{row.get('Squad','—')} &nbsp;•&nbsp; {row.get('League','—')} &nbsp;•&nbsp; Age {age}</div>
                  <div style="margin-top:0.5rem;">
                    <span class="badge">{row.get('Pos_primary','—')}</span>{ab}<span class="{sch[0]}">{sch[1]}</span>
                  </div>
                </div>
                <div style="text-align:right;flex-shrink:0;">
                  <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:#e03a3e;line-height:1;">{row['Final_Score']:.0f}</div>
                  <div style="font-size:0.6rem;color:#555;text-transform:uppercase;letter-spacing:1px;">Value Score</div>
                  <div style="font-size:0.82rem;color:white;margin-top:0.4rem;font-weight:500;">
                    ⚽{int(row['Gls'])}G &nbsp; 🅰️{int(row['Ast'])}A &nbsp; 🎯{row['SoT%']:.0f}% &nbsp; 💶€{row['Market_Value_M']:.0f}m
                  </div>
                </div>
              </div>
              <div class="bar-bg"><div class="bar-fill" style="width:{score_pct:.0f}%"></div></div>
            </div>""", unsafe_allow_html=True)


# ══════ TAB 2 ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-title">VALUE ANALYSIS</div>', unsafe_allow_html=True)
    if len(df) < 2:
        st.info("📊 Need more data for charts. Adjust filters.")
    else:
        s1,s2,s3,s4 = st.columns(4)
        for col,(val,lbl,c) in zip([s1,s2,s3,s4],[
            (f"{df['Final_Score'].max():.0f}","TOP SCORE","#e03a3e"),
            (f"€{df['Market_Value_M'].max():.0f}M","MAX VALUE","white"),
            (f"{df['Final_Score'].mean():.1f}","AVG SCORE","#f39c12"),
            (str(len(df)),"PLAYERS","#2ecc71"),
        ]):
            with col:
                st.markdown(f'<div class="glass-card" style="text-align:center;padding:1rem;"><div style="font-size:1.6rem;color:{c};font-family:\'Bebas Neue\';">{val}</div><div style="color:#666;font-size:0.68rem;">{lbl}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            fig = px.scatter(df,x='Market_Value_M',y='Final_Score',hover_name='Player',
                hover_data={'Squad':True,'Age_num':True,'Gls':True,'Ast':True},
                color='Pos_primary',size='Gls',size_max=20,
                color_discrete_sequence=['#e03a3e','#f5a623','#4a90e2','#2ecc71','#9b59b6'],
                title='Value Score vs Market Value',
                labels={'Market_Value_M':'Market Value (€m)','Final_Score':'Value Score','Pos_primary':'Position'})
            fig.update_layout(**LAYOUT, title=tl('Value Score vs Market Value'), height=400)
            fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
            fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            t10 = df.nlargest(10,'Final_Score')
            fig2 = go.Figure(go.Bar(x=t10['Final_Score'],y=t10['Player'],orientation='h',
                marker=dict(color=t10['Final_Score'],colorscale=[[0,'#1a0505'],[0.5,'#8b1a1a'],[1,'#e03a3e']],showscale=False),
                text=[f"€{v:.0f}M | ⚽{int(g)}G" for v,g in zip(t10['Market_Value_M'],t10['Gls'])],
                textposition='outside',textfont=dict(color='#666',size=10)))
            fig2.update_layout(**LAYOUT, title=tl('Top 10 — Value Score Ranking'), height=400,
                               yaxis=dict(autorange='reversed',gridcolor='rgba(255,255,255,0.04)'),
                               xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
                               margin=dict(t=50,b=30,l=10,r=80))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="sec-title">⚽ GOALS EFFICIENCY</div>', unsafe_allow_html=True)
        avg_g,avg_s = df['Gls_p90'].mean(), df['SoT%'].mean()
        fig3 = px.scatter(df,x='Gls_p90',y='SoT%',hover_name='Player',
            hover_data={'Squad':True,'Gls':True,'Ast':True},
            color='Final_Score',size='Market_Value_M',size_max=20,
            color_continuous_scale=[[0,'#0d0d0d'],[0.4,'#8b1a1a'],[1,'#e03a3e']],
            title='Scoring Efficiency',
            labels={'Gls_p90':'Goals per 90','SoT%':'Shot on Target %'})
        fig3.update_layout(**LAYOUT, title=tl('Scoring Efficiency: Goals/90 vs Shot Accuracy'), height=380,
                           coloraxis_colorbar=dict(title='Score',tickfont=dict(color='#666'),bgcolor='rgba(15,15,15,0.8)'))
        fig3.add_hline(y=avg_s,line_dash="dash",line_color="rgba(255,255,255,0.15)",
                       annotation_text=f"Avg {avg_s:.1f}%",annotation_font=dict(color='#666',size=10))
        fig3.add_vline(x=avg_g,line_dash="dash",line_color="rgba(255,255,255,0.15)",
                       annotation_text=f"Avg {avg_g:.2f}",annotation_font=dict(color='#666',size=10))
        st.plotly_chart(fig3, use_container_width=True)

        if 'Defense_Hardness' in df.columns:
            st.markdown('<div class="sec-title">📅 SCHEDULE DIFFICULTY</div>', unsafe_allow_html=True)
            sh = df.groupby('Squad')['Defense_Hardness'].mean().sort_values().reset_index()
            fig4 = go.Figure(go.Bar(x=sh['Defense_Hardness'],y=sh['Squad'],orientation='h',
                marker=dict(color=sh['Defense_Hardness'],colorscale=[[0,'#1a0505'],[1,'#e03a3e']],showscale=False)))
            fig4.update_layout(**LAYOUT, title=tl('Defense Hardness Score'), height=380,
                               yaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
                               xaxis=dict(gridcolor='rgba(255,255,255,0.04)'))
            st.plotly_chart(fig4, use_container_width=True)


# ══════ TAB 3 ════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-title">🔬 PLAYER DEEP DIVE</div>', unsafe_allow_html=True)
    col_sel,col_hint = st.columns([2,1])
    with col_sel:
        search = st.text_input("🔍 Search Player", placeholder="Type player name...")
        all_p  = df['Player'].tolist()
        filt_p = [p for p in all_p if search.lower() in p.lower()] if search else all_p
        selected = st.multiselect("Select Players to Compare (max 3)", filt_p,
                                   default=filt_p[:min(2,len(filt_p))], max_selections=3)
    with col_hint:
        st.markdown("""<div class="glass-card" style="padding:1rem;margin-top:1.6rem;">
        <div style="color:#888;font-size:0.72rem;">📊 METRICS</div>
        <div style="color:white;font-size:0.82rem;margin-top:0.4rem;line-height:1.8;">
        ⚽ Goals &nbsp;|&nbsp; 🅰️ Assists<br>🎯 Accuracy &nbsp;|&nbsp; 💶 Value<br>📈 Score &nbsp;|&nbsp; 📅 Schedule</div></div>""", unsafe_allow_html=True)

    if selected:
        st.markdown("---")
        colors_p = ['#e03a3e','#f5a623','#4a90e2']
        cols_p = st.columns(len(selected))
        for idx,(col,pname) in enumerate(zip(cols_p,selected)):
            r  = df[df['Player']==pname].iloc[0]
            pc = colors_p[idx]
            h  = r.get('Defense_Hardness',0.5)
            si = "🔴" if h>=0.6 else ("🟡" if h>=0.4 else "🟢")
            peak = float(r.get('Peak_Value_M', r['Market_Value_M']))
            vc   = ((r['Market_Value_M']-peak)/peak*100) if peak>0 else 0
            sot_w = min(float(r['SoT%']),100)
            val_w = max(0, min((1-r['Market_Value_M']/df['Market_Value_M'].max())*100,100))
            with col:
                st.markdown(f"""
                <div class="glass-card" style="padding:1.5rem;border-left:4px solid {pc};">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:white;">{pname}</div>
                    <span style="background:{pc}22;color:{pc};padding:3px 9px;border-radius:12px;font-size:0.65rem;">#{idx+1}</span>
                  </div>
                  <div style="color:#888;font-size:0.72rem;margin:0.3rem 0 1rem;">{r.get('Squad','—')} • {r.get('League','—')} • Age {int(r['Age_num'])}</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.7rem;text-align:center;margin-bottom:1rem;">
                    <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:0.8rem;">
                      <div style="font-size:1.8rem;">⚽</div>
                      <div style="font-size:1.4rem;color:white;font-family:'Bebas Neue';">{int(r.get('Gls',0))}</div>
                      <div style="color:#555;font-size:0.62rem;">GOALS</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:0.8rem;">
                      <div style="font-size:1.8rem;">🅰️</div>
                      <div style="font-size:1.4rem;color:white;font-family:'Bebas Neue';">{int(r.get('Ast',0))}</div>
                      <div style="color:#555;font-size:0.62rem;">ASSISTS</div>
                    </div>
                  </div>
                  <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:1rem;margin-bottom:0.8rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                      <span style="color:#888;font-size:0.75rem;">🎯 Shot Accuracy</span><span style="color:white;">{r['SoT%']:.1f}%</span>
                    </div>
                    <div class="bar-bg"><div class="bar-fill" style="width:{sot_w:.0f}%"></div></div>
                    <div style="display:flex;justify-content:space-between;margin:0.8rem 0 0.4rem;">
                      <span style="color:#888;font-size:0.75rem;">💶 Market Value</span><span style="color:white;">€{r['Market_Value_M']:.0f}m</span>
                    </div>
                    <div class="bar-bg"><div class="bar-fill" style="width:{val_w:.0f}%"></div></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><span style="color:#888;font-size:0.72rem;">📊 Score</span>
                      <span style="color:{pc};font-size:1.5rem;font-family:'Bebas Neue';margin-left:0.4rem;">{r['Final_Score']:.0f}</span></div>
                    <div style="font-size:0.7rem;color:#666;">{si} {h:.2f} | Peak €{peak:.0f}m <span style="color:{'#2ecc71' if vc>=0 else '#e03a3e'};">({vc:+.0f}%)</span></div>
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
        for pname,pc in zip(selected,colors_p):
            r    = df[df['Player']==pname].iloc[0]
            vals = [float(r.get(m,0)) for m in metrics]+[float(r.get(metrics[0],0))]
            lbs  = labels+[labels[0]]
            rgba = tuple(int(pc.lstrip('#')[i:i+2],16) for i in (0,2,4))
            fig_r.add_trace(go.Scatterpolar(r=vals,theta=lbs,fill='toself',name=pname,
                line=dict(color=pc,width=3),fillcolor=f'rgba{rgba+(0.15,)}'))
        fig_r.update_layout(
            polar=dict(bgcolor='rgba(10,10,10,0.6)',
                       radialaxis=dict(visible=True,range=[0,1],color='#444',gridcolor='rgba(255,255,255,0.06)',tickfont=dict(color='#555')),
                       angularaxis=dict(color='#666',gridcolor='rgba(255,255,255,0.06)')),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e8e8e8',family='Inter'),
            legend=dict(bgcolor='rgba(15,15,15,0.8)',bordercolor='rgba(224,58,62,0.2)',font=dict(color='#e8e8e8')),
            title=tl('Player Comparison Radar',22),
            height=480, margin=dict(t=60,b=20,l=20,r=20))
        st.plotly_chart(fig_r, use_container_width=True)

        if len(selected)>1:
            st.markdown('<div class="sec-title">📊 PERFORMANCE COMPARISON</div>', unsafe_allow_html=True)
            cc1,cc2 = st.columns(2)
            with cc1:
                fig_ga = go.Figure()
                fig_ga.add_trace(go.Bar(name='Goals',x=selected,
                    y=[int(df[df['Player']==p]['Gls'].values[0]) for p in selected],
                    marker_color='#e03a3e',text=[int(df[df['Player']==p]['Gls'].values[0]) for p in selected],textposition='inside'))
                fig_ga.add_trace(go.Bar(name='Assists',x=selected,
                    y=[int(df[df['Player']==p]['Ast'].values[0]) for p in selected],
                    marker_color='#f39c12',text=[int(df[df['Player']==p]['Ast'].values[0]) for p in selected],textposition='inside'))
                fig_ga.update_layout(**LAYOUT,barmode='group',title=tl('Goals & Assists'),height=320)
                st.plotly_chart(fig_ga, use_container_width=True)
            with cc2:
                best  = df[df['Player'].isin(selected)].sort_values('Final_Score',ascending=False).iloc[0]
                worst = df[df['Player'].isin(selected)].sort_values('Final_Score',ascending=False).iloc[-1]
                st.markdown(f"""
                <div class="glass-card" style="padding:1.5rem;text-align:center;min-height:300px;display:flex;flex-direction:column;justify-content:center;">
                  <div style="color:#e03a3e;font-family:'Bebas Neue';font-size:1.1rem;letter-spacing:2px;">🏆 RECOMMENDED TARGET</div>
                  <div style="font-size:1.8rem;color:white;font-family:'Bebas Neue';margin:0.5rem 0;">{best['Player']}</div>
                  <div style="color:#888;font-size:0.8rem;margin-bottom:1rem;">over {worst['Player']}</div>
                  <div style="display:flex;justify-content:center;gap:2rem;">
                    <div><span style="color:#888;">Score</span><span style="color:#e03a3e;font-size:1.5rem;font-family:'Bebas Neue';margin-left:0.5rem;">{best['Final_Score']:.0f}</span></div>
                    <div><span style="color:#444;">vs {worst['Final_Score']:.0f}</span></div>
                  </div>
                  <div style="color:#555;font-size:0.75rem;margin-top:1rem;">Age {int(best['Age_num'])} • €{best['Market_Value_M']:.0f}m • Better value</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("👆 Select players to compare from the list above")


# ══════ TAB 4 ════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-title">📋 FULL DATASET</div>', unsafe_allow_html=True)
    t1c,t2c,t3c,t4c = st.columns([3,2,2,1])
    with t1c:
        all_cols = ['Player','Nation','Pos_primary','Squad','Age_num','League','Gls','Ast','Gls_p90','SoT%','Market_Value_M','Perf_Score','Final_Score','Defense_Hardness']
        av_cols  = [c for c in all_cols if c in df.columns]
        sel_cols = st.multiselect("📌 Columns", av_cols,
                                   default=['Player','Squad','Age_num','Pos_primary','Gls','Ast','SoT%','Market_Value_M','Final_Score'])
    with t2c:
        sort_options = [c for c in ['Final_Score','Market_Value_M','Gls','Age_num','SoT%'] if c in df.columns]
        sort_by = st.selectbox("🔽 Sort By", sort_options)
    with t3c:
        rows_to_show = st.selectbox("📊 Rows", [10,25,50,100,len(df)], index=2)
    with t4c:
        asc = st.checkbox("🔄 Asc", False)

    if sel_cols and len(df)>0:
        sort_cols = [sort_by] + [c for c in sel_cols if c!=sort_by]
        sort_cols = [c for c in sort_cols if c in df.columns]
        disp = df[sort_cols].sort_values(sort_by,ascending=asc).head(rows_to_show).copy()
        disp = disp[[c for c in sel_cols if c in disp.columns]]
        fmt  = {k:v for k,v in {'SoT%':'{:.1f}%','Gls_p90':'{:.3f}','Market_Value_M':'€{:.0f}m','Final_Score':'{:.1f}','Perf_Score':'{:.3f}','Defense_Hardness':'{:.2f}'}.items() if k in disp.columns}
        st.dataframe(disp.style.format(fmt), use_container_width=True, height=480)

    st.markdown('<div class="sec-title">📊 DATA INSIGHTS</div>', unsafe_allow_html=True)
    si1,si2,si3,si4,si5 = st.columns(5)
    for col,(val,lbl,c) in zip([si1,si2,si3,si4,si5],[
        (len(df),"Total Players","#e03a3e"),
        (df['Squad'].nunique(),"Teams","white"),
        (df['Pos_primary'].nunique(),"Positions","#f39c12"),
        (int(df['Gls'].sum()),"Total Goals","#2ecc71"),
        (f"{df['Age_num'].mean():.1f}","Avg Age","#4a90e2"),
    ]):
        with col:
            st.markdown(f'<div class="glass-card" style="text-align:center;padding:0.8rem;"><div style="font-size:1.6rem;color:{c};font-family:\'Bebas Neue\';">{val}</div><div style="color:#555;font-size:0.65rem;">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if len(df)>1:
        ci1,ci2 = st.columns(2)
        with ci1:
            pos_c = df['Pos_primary'].value_counts()
            fig_p = go.Figure(go.Pie(labels=pos_c.index,values=pos_c.values,hole=0.45,
                marker_colors=['#e03a3e','#f5a623','#4a90e2','#2ecc71','#9b59b6']))
            fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e8e8e8',family='Inter'),
                title=tl('Position Distribution'),
                legend=dict(bgcolor='rgba(15,15,15,0.8)',font=dict(color='#e8e8e8')),height=300)
            st.plotly_chart(fig_p, use_container_width=True)
        with ci2:
            fig_a = go.Figure(go.Histogram(x=df['Age_num'],nbinsx=15,marker_color='#e03a3e',opacity=0.7))
            fig_a.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(10,10,10,0.5)',
                font=dict(color='#e8e8e8',family='Inter'),
                title=tl('Age Distribution'),
                xaxis=dict(title='Age',gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(title='Count',gridcolor='rgba(255,255,255,0.05)'),height=300)
            st.plotly_chart(fig_a, use_container_width=True)

    st.markdown("---")
    d1,d2,d3,_ = st.columns([1,1,1,3])
    with d1:
        st.download_button("📥 Full Dataset",df.to_csv(index=False).encode('utf-8'),"brentford_scouting_full.csv","text/csv",use_container_width=True)
    with d2:
        st.download_button("📥 Top 50",df.head(50).to_csv(index=False).encode('utf-8'),"brentford_top50.csv","text/csv",use_container_width=True)
    with d3:
        st.download_button("📥 Top 10",df.head(10).to_csv(index=False).encode('utf-8'),"brentford_top10.csv","text/csv",use_container_width=True)


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:0.8rem;">
    <span>🐝 BRENTFORD FC SCOUTING SYSTEM</span>
    <span>⚽ SEASON 2025-26</span>
    <span>📊 FBREF + TRANSFERMARKT</span>
  </div>
  <div style="display:flex;justify-content:center;gap:1.5rem;margin-bottom:0.5rem;">
    <a href="https://www.linkedin.com/in/goda-emad/" target="_blank">🔗 LinkedIn</a>
    <a href="https://github.com/Goda-Emad/brentford-scouting" target="_blank">🐙 GitHub</a>
    <span style="color:#444;">📞 +20 112 624 2932</span>
  </div>
  <div style="color:#333;">Developed by Goda Emad © 2026</div>
</div>""", unsafe_allow_html=True)
