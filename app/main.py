import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64, pathlib

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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');
:root {
    --red:#e03a3e; --black:#0d0d0d; --dark:#141414;
    --card:#1a1a1a; --border:rgba(224,58,62,0.22);
    --text:#e8e8e8; --muted:#777;
}
html,body,[data-testid="stAppViewContainer"]{background:var(--black)!important;color:var(--text)!important;}
[data-testid="stSidebar"]{background:#0f0f0f!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
.header-wrap{background:linear-gradient(135deg,#0d0d0d 0%,#1c0606 60%,#0d0d0d 100%);
  border:1px solid var(--border);border-radius:14px;padding:2rem 2.5rem;
  margin-bottom:1.5rem;position:relative;overflow:hidden;display:flex;align-items:center;gap:2rem;}
.header-wrap::before{content:'';position:absolute;top:-80px;right:-60px;width:350px;height:350px;
  background:radial-gradient(circle,rgba(224,58,62,0.13) 0%,transparent 70%);}
.header-logo{width:72px;height:72px;border-radius:50%;border:2px solid var(--border);object-fit:contain;flex-shrink:0;}
.main-title{font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:white;letter-spacing:4px;line-height:1;margin:0;}
.main-title span{color:var(--red);}
.main-sub{font-family:'Inter',sans-serif;font-size:0.72rem;color:var(--muted);letter-spacing:2.5px;text-transform:uppercase;margin-top:0.4rem;}
.social-links{margin-top:0.8rem;display:flex;gap:0.6rem;flex-wrap:wrap;}
.social-btn{display:inline-flex;align-items:center;gap:5px;background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.10);color:#aaa!important;font-family:'Inter',sans-serif;
  font-size:0.68rem;font-weight:500;letter-spacing:0.8px;padding:4px 12px;border-radius:20px;
  text-decoration:none!important;transition:border-color 0.2s,color 0.2s;}
.social-btn:hover{border-color:var(--red);color:white!important;}
.kpi-card{background:var(--card);border:1px solid var(--border);border-radius:10px;
  padding:1.1rem 1.3rem;position:relative;overflow:hidden;transition:transform 0.2s;}
.kpi-card:hover{transform:translateY(-2px);}
.kpi-card::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:2px;
  background:linear-gradient(90deg,var(--red),transparent);}
.kpi-val{font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:white;line-height:1;}
.kpi-lbl{font-family:'Inter',sans-serif;font-size:0.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.8px;margin-top:0.3rem;}
.pcard{background:var(--card);border:1px solid rgba(255,255,255,0.05);border-radius:10px;
  padding:1.1rem 1.3rem;margin-bottom:0.7rem;transition:border-color 0.2s,box-shadow 0.2s;}
.pcard:hover{border-color:var(--border);box-shadow:0 4px 20px rgba(224,58,62,0.07);}
.pname{font-family:'Bebas Neue',sans-serif;font-size:1.25rem;color:white;letter-spacing:1px;}
.pmeta{font-family:'Inter',sans-serif;font-size:0.7rem;color:var(--muted);margin-top:0.15rem;}
.bar-bg{background:#222;border-radius:4px;height:4px;margin-top:0.8rem;}
.bar-fill{background:linear-gradient(90deg,#8b1a1a,var(--red),#ff7070);border-radius:4px;height:4px;}
.badge{display:inline-block;background:rgba(224,58,62,0.12);border:1px solid var(--border);
  color:var(--red);font-size:0.62rem;font-family:'Inter',sans-serif;font-weight:600;
  padding:2px 8px;border-radius:20px;text-transform:uppercase;letter-spacing:1px;margin-right:4px;}
.badge-g{background:rgba(255,255,255,0.04);border-color:rgba(255,255,255,0.08);color:var(--muted);}
.badge-green{background:rgba(126,211,33,0.10);border-color:rgba(126,211,33,0.25);color:#7ed321;}
.badge-yellow{background:rgba(245,166,35,0.10);border-color:rgba(245,166,35,0.25);color:#f5a623;}
.sec-title{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:white;letter-spacing:2.5px;
  border-left:3px solid var(--red);padding-left:0.8rem;margin:1.5rem 0 1rem;}
[data-testid="stTabs"] [data-baseweb="tab"]{color:var(--muted)!important;font-family:'Inter',sans-serif!important;font-size:0.78rem!important;font-weight:500!important;}
[data-testid="stTabs"] [aria-selected="true"]{color:white!important;border-bottom:2px solid var(--red)!important;}
[data-testid="stSidebar"] label{font-family:'Inter',sans-serif!important;font-size:0.7rem!important;text-transform:uppercase!important;letter-spacing:1.5px!important;color:var(--muted)!important;}
[data-testid="stDownloadButton"] button{background:transparent!important;border:1px solid var(--border)!important;color:var(--red)!important;font-family:'Inter',sans-serif!important;font-size:0.75rem!important;border-radius:8px!important;}
.footer{text-align:center;padding:2rem 0 1rem;color:#333;font-family:'Inter',sans-serif;font-size:0.68rem;letter-spacing:1.5px;text-transform:uppercase;border-top:1px solid rgba(255,255,255,0.05);margin-top:3rem;}
.footer a{color:#555!important;text-decoration:none;}
.footer a:hover{color:var(--red)!important;}
hr{border:none!important;border-top:1px solid rgba(255,255,255,0.05)!important;}
</style>
""", unsafe_allow_html=True)

def normalize_col(col):
    mn,mx = col.min(),col.max()
    return col*0 if mx==mn else (col-mn)/(mx-mn)

def recalculate(df):
    df = df.copy()
    for c in ['Gls_p90','SoT%','Ast','PrgP_proxy','Scoring_Context_Bonus','Market_Value_M','Age_num','90s']:
        if c not in df.columns: df[c]=0
    df['norm_gls_p90']=normalize_col(df['Gls_p90'])
    df['norm_sot_pct']=normalize_col(df['SoT%'].fillna(0))
    df['norm_ast']=normalize_col(df['Ast'])
    df['norm_prgp']=normalize_col(df['PrgP_proxy'])
    df['norm_context']=normalize_col(df['Scoring_Context_Bonus'])
    df['Perf_Score']=(df['norm_gls_p90']*0.30+df['norm_sot_pct']*0.18+df['norm_ast']*0.22+df['norm_prgp']*0.18+df['norm_context']*0.12).round(3)
    df['Value_Score']=(df['Perf_Score']/df['Market_Value_M'].clip(lower=0.1)*100).round(3)
    df['Value_Score_norm']=(normalize_col(df['Value_Score'])*100).round(1)
    df['Age_bonus']=df['Age_num'].apply(lambda x:1.2 if x<=23 else(1.1 if x<=25 else 1.0))
    df['Final_Score']=(df['Value_Score_norm']*df['Age_bonus']).round(1)
    return df

import os

@st.cache_data
def load_data(file=None):
    if file is not None:
        df = pd.read_csv(file)
    else:
        # تحديد جذر المشروع (يشتغل Local و Streamlit Cloud)
        base_path = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(base_path, "data", "processed", "ligue1_final.csv")
        df = pd.read_csv(data_path)

    return recalculate(df)


def img_to_b64(path):
    try:
        # نفس فكرة تحديد الجذر علشان الصور تشتغل على Cloud
        base_path = os.path.dirname(os.path.dirname(__file__))
        full_path = os.path.join(base_path, path)

        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


LAYOUT = dict(
    plot_bgcolor='#141414',
    paper_bgcolor='#1a1a1a',
    font=dict(color='#e8e8e8', family='Inter'),
    title_font=dict(color='white', family='Bebas Neue', size=20),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#777')),
    margin=dict(t=50, b=30, l=10, r=10)
)
# HEADER
logo_b64=img_to_b64("assets/brentford_logo.png")
logo_html=f'<img class="header-logo" src="data:image/png;base64,{logo_b64}"/>' if logo_b64 else '<div style="font-size:3rem;flex-shrink:0;">⚽</div>'
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

# SIDEBAR
with st.sidebar:
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.3rem;color:white;letter-spacing:2px;margin-bottom:1rem;padding-bottom:0.7rem;border-bottom:1px solid rgba(224,58,62,0.25);">⚙️ SCOUT FILTERS</div>', unsafe_allow_html=True)
    uploaded=st.file_uploader("📂 Add New League CSV",type=["csv"],help="Upload CSV with same format — new league auto-merges")
    df_base=load_data(uploaded)
    leagues=sorted(df_base['League'].dropna().unique()) if 'League' in df_base.columns else ['Ligue 1']
    sel_league=st.multiselect("🌍 League",leagues,default=leagues)
    positions=sorted(df_base['Pos_primary'].dropna().unique())
    sel_pos=st.multiselect("📍 Position",positions,default=positions)
    age_range=st.slider("🎂 Age Range",int(df_base['Age_num'].min()),int(df_base['Age_num'].max()),(int(df_base['Age_num'].min()),int(df_base['Age_num'].max())))
    budget=st.slider("💶 Max Market Value (€m)",1.0,float(df_base['Market_Value_M'].max()),float(df_base['Market_Value_M'].max()))
    min_90s=st.slider("⏱️ Min 90s Played",0.0,float(df_base['90s'].max()),3.0,step=0.5)
    st.markdown("---")
    top_n=st.selectbox("📊 Show Top N Targets",[10,15,20,30,50],index=2)
    st.markdown("""<div style="margin-top:1.5rem;padding:1rem;background:rgba(224,58,62,0.06);border:1px solid rgba(224,58,62,0.15);border-radius:8px;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:0.9rem;color:#e03a3e;letter-spacing:1.5px;margin-bottom:0.5rem;">VALUE SCORE FORMULA</div>
    <div style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;line-height:1.9;">
    Goals/90 × 0.30<br>Shot Acc × 0.18<br>Assists × 0.22<br>Prog Passes × 0.18<br>Schedule Adj × 0.12<br>
    <span style="color:#444;">÷ Market Value × Age Bonus</span></div></div>""", unsafe_allow_html=True)
    st.markdown('<div style="margin-top:1rem;font-family:Inter,sans-serif;font-size:0.65rem;color:#333;text-align:center;">Data: FBref + Transfermarkt<br>Dec 2025 • Ligue 1 2025-26</div>', unsafe_allow_html=True)

# FILTER
df=df_base.copy()
if sel_league and 'League' in df.columns: df=df[df['League'].isin(sel_league)]
if sel_pos: df=df[df['Pos_primary'].isin(sel_pos)]
df=df[(df['Age_num']>=age_range[0])&(df['Age_num']<=age_range[1])&(df['Market_Value_M']<=budget)&(df['90s']>=min_90s)].sort_values('Final_Score',ascending=False).reset_index(drop=True)

# KPIs
k1,k2,k3,k4,k5=st.columns(5)
kpis=[(len(df),"Players Scouted"),(f"€{df['Market_Value_M'].mean():.1f}m","Avg Market Value"),(f"{df['Final_Score'].max():.0f}","Top Value Score"),(f"{df['Gls_p90'].mean():.2f}","Avg Goals / 90"),(f"{df['SoT%'].mean():.1f}%","Avg Shot Accuracy")]
for col,(val,lbl) in zip([k1,k2,k3,k4,k5],kpis):
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>',unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)

# TABS
tab1,tab2,tab3,tab4=st.tabs(["🎯  Top Targets","📊  Value Analysis","🔬  Player Deep Dive","📋  Full Dataset"])

# TAB1
with tab1:
    st.markdown('<div class="sec-title">TOP TARGETS</div>',unsafe_allow_html=True)
    for rank,(_,row) in enumerate(df.head(top_n).iterrows(),1):
        score_pct=min(row['Final_Score']/130*100,100)
        h=row.get('Defense_Hardness',0.5)
        sch=('badge-g badge','🔴 Hard Schedule') if h>=0.6 else (('badge-yellow badge','🟡 Mid Schedule') if h>=0.4 else ('badge-green badge','🟢 Easy Schedule'))
        age=int(row['Age_num'])
        age_badge='<span class="badge">🌟 U23</span>' if age<=23 else ('<span class="badge-g badge">Prime</span>' if age<=26 else '<span class="badge-g badge">Veteran</span>')
        st.markdown(f"""<div class="pcard">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
            <div style="flex:1;">
              <div style="color:var(--red);font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;letter-spacing:1.5px;">#{rank:02d}</div>
              <div class="pname">{row['Player']}</div>
              <div class="pmeta">{row.get('Squad','—')} &nbsp;•&nbsp; {row.get('League','—')} &nbsp;•&nbsp; Age {age}</div>
              <div style="margin-top:0.5rem;"><span class="badge">{row.get('Pos_primary','—')}</span>{age_badge}<span class="{sch[0]}">{sch[1]}</span></div>
            </div>
            <div style="text-align:right;flex-shrink:0;">
              <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;color:var(--red);line-height:1;">{row['Final_Score']:.0f}</div>
              <div style="font-size:0.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px;">Value Score</div>
              <div style="font-size:0.82rem;color:white;margin-top:0.4rem;font-family:'Inter',sans-serif;font-weight:500;">
                ⚽ {int(row['Gls'])}G &nbsp; 🅰️ {int(row['Ast'])}A &nbsp; 🎯 {row['SoT%']:.0f}% &nbsp; 💶 €{row['Market_Value_M']:.0f}m
              </div>
            </div>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width:{score_pct:.0f}%"></div></div>
        </div>""",unsafe_allow_html=True)

# TAB2
with tab2:
    st.markdown('<div class="sec-title">VALUE ANALYSIS</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        fig=px.scatter(df,x='Market_Value_M',y='Final_Score',hover_name='Player',
            hover_data={'Squad':True,'Age_num':True,'Gls':True,'Ast':True,'Market_Value_M':True,'Final_Score':True},
            color='Pos_primary',size='Gls',size_max=22,
            color_discrete_sequence=['#e03a3e','#f5a623','#4a90e2','#7ed321','#9b59b6'],
            title='Value Score vs Market Value',labels={'Market_Value_M':'Market Value (€m)','Final_Score':'Value Score'})
        fig.update_layout(**LAYOUT)
        fig.add_shape(type='line',x0=0,y0=55,x1=df['Market_Value_M'].max(),y1=55,line=dict(color='rgba(224,58,62,0.35)',dash='dash',width=1))
        fig.add_annotation(x=df['Market_Value_M'].max()*0.65,y=59,text="Brentford Target Zone",font=dict(color='rgba(224,58,62,0.6)',size=10),showarrow=False)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        t15=df.head(15)
        fig2=go.Figure(go.Bar(x=t15['Final_Score'],y=t15['Player'],orientation='h',
            marker=dict(color=t15['Final_Score'],colorscale=[[0,'#1a0505'],[0.5,'#8b1a1a'],[1,'#e03a3e']],showscale=False),
            text=[f"€{v:.0f}m" for v in t15['Market_Value_M']],textposition='outside',textfont=dict(color='#555',size=10)))
        fig2.update_layout(**LAYOUT,title='Top 15 — Value Score Ranking',yaxis=dict(autorange='reversed',gridcolor='rgba(255,255,255,0.03)'),xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),margin=dict(t=50,b=30,l=10,r=70))
        st.plotly_chart(fig2,use_container_width=True)
    fig3=px.scatter(df,x='Gls_p90',y='SoT%',hover_name='Player',color='Final_Score',size='Market_Value_M',size_max=22,
        color_continuous_scale=[[0,'#0d0d0d'],[0.4,'#8b1a1a'],[1,'#e03a3e']],
        title='Scoring Efficiency — Goals/90 vs Shot Accuracy',labels={'Gls_p90':'Goals per 90','SoT%':'Shot on Target %'})
    fig3.update_layout(**LAYOUT,coloraxis_colorbar=dict(title='Score',tickfont=dict(color='#555')))
    st.plotly_chart(fig3,use_container_width=True)
    if 'Defense_Hardness' in df.columns:
        st.markdown('<div class="sec-title">SCHEDULE DIFFICULTY BY SQUAD</div>',unsafe_allow_html=True)
        sh=df.groupby('Squad')['Defense_Hardness'].mean().sort_values(ascending=True).reset_index()
        fig4=go.Figure(go.Bar(x=sh['Defense_Hardness'],y=sh['Squad'],orientation='h',marker=dict(color=sh['Defense_Hardness'],colorscale=[[0,'#1a0505'],[1,'#e03a3e']],showscale=False)))
        fig4.update_layout(**LAYOUT,title='Defense Hardness Score (higher = harder to score against)',height=400,yaxis=dict(gridcolor='rgba(255,255,255,0.03)'),xaxis=dict(gridcolor='rgba(255,255,255,0.04)'))
        st.plotly_chart(fig4,use_container_width=True)

# TAB3
with tab3:
    st.markdown('<div class="sec-title">PLAYER DEEP DIVE</div>',unsafe_allow_html=True)
    all_p=df['Player'].tolist()
    sel=st.multiselect("Select Players to Compare (max 3)",all_p,default=all_p[:min(2,len(all_p))],max_selections=3)
    if sel:
        cols=st.columns(len(sel))
        for col,pname in zip(cols,sel):
            r=df[df['Player']==pname].iloc[0]
            h=r.get('Defense_Hardness',0.5)
            sch_icon="🔴" if h>=0.6 else("🟡" if h>=0.4 else "🟢")
            peak=r.get('Peak_Value_M',r['Market_Value_M'])
            vc=((r['Market_Value_M']-peak)/peak*100) if peak>0 else 0
            with col:
                st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.4rem;text-align:center;">
                  <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:white;letter-spacing:1px;">{r['Player']}</div>
                  <div style="color:var(--muted);font-size:0.7rem;margin:0.3rem 0 1rem;">{r.get('Squad','—')} • {r.get('League','—')} • Age {int(r['Age_num'])}</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.7rem;text-align:left;">
                    <div style="background:#141414;border-radius:8px;padding:0.8rem;"><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:var(--red);line-height:1;">{r['Final_Score']:.0f}</div><div style="font-size:0.6rem;color:#444;text-transform:uppercase;letter-spacing:1px;">Value Score</div></div>
                    <div style="background:#141414;border-radius:8px;padding:0.8rem;"><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:white;line-height:1;">€{r['Market_Value_M']:.0f}m</div><div style="font-size:0.6rem;color:#444;text-transform:uppercase;letter-spacing:1px;">Market Value</div></div>
                    <div style="background:#141414;border-radius:8px;padding:0.8rem;"><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:white;line-height:1;">{int(r['Gls'])}G/{int(r['Ast'])}A</div><div style="font-size:0.6rem;color:#444;text-transform:uppercase;letter-spacing:1px;">Goals / Assists</div></div>
                    <div style="background:#141414;border-radius:8px;padding:0.8rem;"><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:white;line-height:1;">{r['SoT%']:.0f}%</div><div style="font-size:0.6rem;color:#444;text-transform:uppercase;letter-spacing:1px;">Shot Accuracy</div></div>
                  </div>
                  <div style="margin-top:0.8rem;font-size:0.72rem;color:var(--muted);font-family:'Inter',sans-serif;">
                    {sch_icon} Schedule: {h:.2f} &nbsp;•&nbsp; Peak: €{peak:.0f}m <span style="color:{'#7ed321' if vc>=0 else '#e03a3e'};">({vc:+.0f}%)</span>
                  </div>
                </div>""",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        metrics=['norm_gls_p90','norm_sot_pct','norm_ast','norm_prgp','norm_context']
        labels=['Goals/90','Shot Acc','Assists','Prog Passes','Schedule Adj']
        colors=['#e03a3e','#f5a623','#4a90e2']
        fig_r=go.Figure()
        for pname,color in zip(sel,colors):
            r=df[df['Player']==pname].iloc[0]
            vals=[float(r.get(m,0)) for m in metrics]+[float(r.get(metrics[0],0))]
            lbs=labels+[labels[0]]
            rgba=color.lstrip('#')
            ri,gi,bi=int(rgba[0:2],16),int(rgba[2:4],16),int(rgba[4:6],16)
            fig_r.add_trace(go.Scatterpolar(r=vals,theta=lbs,fill='toself',name=pname,
                line=dict(color=color,width=2),fillcolor=f'rgba({ri},{gi},{bi},0.12)'))
        fig_r.update_layout(**LAYOUT,polar=dict(bgcolor='#141414',
            radialaxis=dict(visible=True,range=[0,1],color='#333',gridcolor='rgba(255,255,255,0.06)',tickfont=dict(color='#444')),
            angularaxis=dict(color='#666',gridcolor='rgba(255,255,255,0.06)')),
            title=dict(text='Player Comparison Radar',font=dict(family='Bebas Neue',size=22,color='white')),height=450)
        st.plotly_chart(fig_r,use_container_width=True)

# TAB4
with tab4:
    st.markdown('<div class="sec-title">FULL DATASET</div>',unsafe_allow_html=True)
    disp=['Player','Squad','League','Age_num','Pos_primary','Gls','Ast','SoT%','Gls_p90','Market_Value_M','Defense_Hardness','Perf_Score','Final_Score']
    disp=[c for c in disp if c in df.columns]
    st.dataframe(df[disp].style.background_gradient(subset=['Final_Score'],cmap='Reds').background_gradient(subset=['Market_Value_M'],cmap='Greys').format({'SoT%':'{:.1f}%','Gls_p90':'{:.2f}','Market_Value_M':'€{:.0f}m','Defense_Hardness':'{:.2f}','Perf_Score':'{:.3f}','Final_Score':'{:.1f}'}),use_container_width=True,height=500)
    c_dl1,c_dl2,_=st.columns([1,1,4])
    with c_dl1:
        st.download_button("⬇️ Download CSV",df[disp].to_csv(index=False).encode('utf-8'),"scouting_results.csv","text/csv")
    with c_dl2:
        st.download_button("⬇️ Top 10 Only",df[disp].head(10).to_csv(index=False).encode('utf-8'),"top10_targets.csv","text/csv")

# FOOTER
st.markdown("""<div class="footer">
  Built by <a href="https://www.linkedin.com/in/goda-emad/" target="_blank">Goda Emad</a>
  &nbsp;•&nbsp; <a href="https://github.com/Goda-Emad/brentford-scouting" target="_blank">GitHub</a>
  &nbsp;•&nbsp; Data: FBref + Transfermarkt &nbsp;•&nbsp; Ligue 1 2025–26
</div>""", unsafe_allow_html=True)
