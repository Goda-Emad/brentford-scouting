import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brentford FC | Scouting Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --red:    #e03a3e;
    --black:  #0d0d0d;
    --dark:   #141414;
    --card:   #1a1a1a;
    --border: rgba(224,58,62,0.25);
    --text:   #e8e8e8;
    --muted:  #888;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--black) !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] {
    background: var(--dark) !important;
    border-right: 1px solid var(--border) !important;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0d0d0d 0%, #1a0505 50%, #0d0d0d 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(224,58,62,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.main-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: white;
    letter-spacing: 3px;
    margin: 0;
    line-height: 1;
}
.main-title span { color: var(--red); }
.main-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

/* KPI Cards */
.kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 2px;
    background: var(--red);
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    color: white;
    line-height: 1;
}
.kpi-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.3rem;
}

/* Player Card */
.player-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.player-card:hover { border-color: var(--red); }
.player-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    color: white;
    letter-spacing: 1px;
}
.player-meta {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.2rem;
}
.score-bar-bg {
    background: #2a2a2a;
    border-radius: 4px;
    height: 6px;
    margin-top: 0.8rem;
}
.score-bar-fill {
    background: linear-gradient(90deg, var(--red), #ff6b6b);
    border-radius: 4px;
    height: 6px;
}
.badge {
    display: inline-block;
    background: rgba(224,58,62,0.15);
    border: 1px solid var(--border);
    color: var(--red);
    font-size: 0.68rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-right: 4px;
}
.badge-gray {
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.1);
    color: var(--muted);
}

/* Section title */
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: white;
    letter-spacing: 2px;
    border-left: 3px solid var(--red);
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem 0;
}

/* Streamlit overrides */
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stMultiSelect"] label {
    color: var(--muted) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
div[data-baseweb="select"] > div {
    background-color: #1a1a1a !important;
    border-color: var(--border) !important;
    color: white !important;
}
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
}
.stDataFrame { background: var(--card) !important; }
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ───────────────────────────────────────────────────────────
@st.cache_data
def load_data(file=None):
    if file is not None:
        return pd.read_csv(file)
    try:
        return pd.read_csv("data/processed/ligue1_final.csv")
    except:
        return pd.read_csv("ligue1_final.csv")

def normalize_col(col):
    mn, mx = col.min(), col.max()
    if mx == mn:
        return col * 0
    return (col - mn) / (mx - mn)

def recalculate_scores(df):
    df = df.copy()
    for c in ['Gls_p90','SoT%','Ast','PrgP_proxy','Scoring_Context_Bonus']:
        if c not in df.columns:
            df[c] = 0
    df['norm_gls_p90'] = normalize_col(df['Gls_p90'])
    df['norm_sot_pct']  = normalize_col(df['SoT%'].fillna(0))
    df['norm_ast']      = normalize_col(df['Ast'])
    df['norm_prgp']     = normalize_col(df['PrgP_proxy'])
    df['norm_context']  = normalize_col(df['Scoring_Context_Bonus'] if 'Scoring_Context_Bonus' in df.columns else pd.Series([0]*len(df)))
    df['Perf_Score'] = (
        df['norm_gls_p90'] * 0.30 +
        df['norm_sot_pct'] * 0.18 +
        df['norm_ast']     * 0.22 +
        df['norm_prgp']    * 0.18 +
        df['norm_context'] * 0.12
    ).round(3)
    df['Value_Score']      = (df['Perf_Score'] / df['Market_Value_M'].clip(lower=0.1) * 100).round(3)
    df['Value_Score_norm'] = (normalize_col(df['Value_Score']) * 100).round(1)
    df['Age_bonus']        = df['Age_num'].apply(lambda x: 1.2 if x <= 23 else (1.1 if x <= 25 else 1.0))
    df['Final_Score']      = (df['Value_Score_norm'] * df['Age_bonus']).round(1)
    return df


# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-title">BRENTFORD FC <span>//</span> SCOUTING INTEL</div>
    <div class="main-subtitle">Undervalued Player Detection • Value Score Algorithm • Schedule-Adjusted Analytics</div>
</div>
""", unsafe_allow_html=True)


# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
    color:white;letter-spacing:2px;margin-bottom:1rem;padding-bottom:0.8rem;
    border-bottom:1px solid rgba(224,58,62,0.3);">
    ⚙️ FILTERS
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("📂 Upload New League CSV", type=["csv"],
                                 help="Upload any CSV with same format to add a new league")

    df_raw = load_data(uploaded)
    df_raw = recalculate_scores(df_raw)

    leagues = sorted(df_raw['League'].unique()) if 'League' in df_raw.columns else ['All']
    sel_league = st.multiselect("League", leagues, default=leagues)

    positions = sorted(df_raw['Pos_primary'].unique())
    sel_pos = st.multiselect("Position", positions, default=positions)

    age_range = st.slider("Age Range", 16, 42,
                          (int(df_raw['Age_num'].min()), int(df_raw['Age_num'].max())))

    max_val = float(df_raw['Market_Value_M'].max())
    budget = st.slider("Max Market Value (€m)", 1.0, max_val, max_val)

    min_90s = st.slider("Min 90s Played", 0.0,
                        float(df_raw['90s'].max()), 3.0)

    st.markdown("---")
    top_n = st.selectbox("Show Top N Players", [10, 15, 20, 30, 50], index=2)

    st.markdown("""
    <div style="font-family:'Inter',sans-serif;font-size:0.7rem;color:#555;
    margin-top:2rem;text-align:center;">
    Data: FBref + Transfermarkt<br>Updated: Dec 2025
    </div>
    """, unsafe_allow_html=True)


# ─── FILTER DATA ────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_league and 'League' in df.columns:
    df = df[df['League'].isin(sel_league)]
if sel_pos:
    df = df[df['Pos_primary'].isin(sel_pos)]
df = df[
    (df['Age_num'] >= age_range[0]) &
    (df['Age_num'] <= age_range[1]) &
    (df['Market_Value_M'] <= budget) &
    (df['90s'] >= min_90s)
]
df = df.sort_values('Final_Score', ascending=False).reset_index(drop=True)


# ─── KPI ROW ────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (len(df), "Players Scouted"),
    (f"{df['Market_Value_M'].mean():.1f}m", "Avg Market Value"),
    (f"{df['Final_Score'].max():.0f}", "Top Value Score"),
    (f"{df['Gls_p90'].mean():.2f}", "Avg Goals / 90"),
    (f"{df['SoT%'].mean():.1f}%", "Avg Shot Accuracy"),
]
for col, (val, label) in zip([k1,k2,k3,k4,k5], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── MAIN CONTENT ───────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎯 Top Targets", "📊 Value Analysis", "🔬 Player Deep Dive"])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1: TOP TARGETS
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">TOP TARGETS</div>', unsafe_allow_html=True)

    top_df = df.head(top_n)

    for i, row in top_df.iterrows():
        rank = list(top_df.index).index(i) + 1
        score_pct = row['Final_Score'] / 120 * 100
        difficulty = ""
        if 'Defense_Hardness' in row:
            h = row['Defense_Hardness']
            if h >= 0.6:   difficulty = "🔴 Hard Schedule"
            elif h >= 0.4: difficulty = "🟡 Medium Schedule"
            else:          difficulty = "🟢 Easy Schedule"

        pos_color = {"FW": "badge", "MF": "badge", "DF": "badge-gray", "GK": "badge-gray"}
        pos_cls = pos_color.get(row.get('Pos_primary',''), 'badge-gray')

        st.markdown(f"""
        <div class="player-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div style="color:var(--red);font-family:'Inter',sans-serif;
                    font-size:0.7rem;font-weight:600;letter-spacing:1px;">#{rank}</div>
                    <div class="player-name">{row['Player']}</div>
                    <div class="player-meta">
                        {row.get('Squad','—')} &nbsp;•&nbsp;
                        Age {int(row['Age_num'])} &nbsp;•&nbsp;
                        {row.get('League','—')}
                    </div>
                    <div style="margin-top:0.5rem;">
                        <span class="{pos_cls}">{row.get('Pos_primary','—')}</span>
                        <span class="badge-gray badge">{difficulty}</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;
                    color:var(--red);line-height:1;">{row['Final_Score']:.0f}</div>
                    <div style="font-size:0.65rem;color:var(--muted);
                    text-transform:uppercase;letter-spacing:1px;">Value Score</div>
                    <div style="font-size:0.8rem;color:white;margin-top:0.3rem;">
                        ⚽ {int(row['Gls'])}G &nbsp; 🅰️ {int(row['Ast'])}A &nbsp; 
                        💶 €{row['Market_Value_M']:.0f}m
                    </div>
                </div>
            </div>
            <div class="score-bar-bg">
                <div class="score-bar-fill" style="width:{min(score_pct,100):.0f}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2: VALUE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">VALUE ANALYSIS</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig_scatter = px.scatter(
            df, x='Market_Value_M', y='Final_Score',
            hover_name='Player',
            hover_data={'Squad': True, 'Age_num': True, 'Gls': True,
                        'Market_Value_M': True, 'Final_Score': True},
            color='Pos_primary',
            size='Gls', size_max=22,
            color_discrete_sequence=['#e03a3e','#f5a623','#4a90e2','#7ed321','#9b59b6'],
            title='Value Score vs Market Value',
            labels={'Market_Value_M': 'Market Value (€m)', 'Final_Score': 'Value Score'}
        )
        fig_scatter.update_layout(
            plot_bgcolor='#141414', paper_bgcolor='#1a1a1a',
            font=dict(color='#e8e8e8', family='Inter'),
            title_font=dict(color='white', family='Bebas Neue', size=18),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#888')),
        )
        fig_scatter.add_shape(type='line', x0=0, y0=50, x1=df['Market_Value_M'].max(), y1=50,
                              line=dict(color='rgba(224,58,62,0.4)', dash='dash', width=1))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c2:
        top15 = df.head(15)
        fig_bar = go.Figure(go.Bar(
            x=top15['Final_Score'],
            y=top15['Player'],
            orientation='h',
            marker=dict(
                color=top15['Final_Score'],
                colorscale=[[0,'#2a0a0a'],[0.5,'#8b1a1a'],[1,'#e03a3e']],
                showscale=False
            ),
            text=[f"€{v:.0f}m" for v in top15['Market_Value_M']],
            textposition='outside',
            textfont=dict(color='#888', size=10),
        ))
        fig_bar.update_layout(
            title='Top 15 — Value Score Ranking',
            plot_bgcolor='#141414', paper_bgcolor='#1a1a1a',
            font=dict(color='#e8e8e8', family='Inter'),
            title_font=dict(color='white', family='Bebas Neue', size=18),
            yaxis=dict(autorange='reversed'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(l=10, r=60),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Goals vs SoT%
    fig_eff = px.scatter(
        df, x='Gls_p90', y='SoT%',
        hover_name='Player',
        color='Final_Score',
        size='Market_Value_M', size_max=20,
        color_continuous_scale=[[0,'#1a0505'],[0.5,'#8b1a1a'],[1,'#e03a3e']],
        title='Scoring Efficiency — Goals/90 vs Shot Accuracy',
        labels={'Gls_p90': 'Goals per 90', 'SoT%': 'Shot on Target %'}
    )
    fig_eff.update_layout(
        plot_bgcolor='#141414', paper_bgcolor='#1a1a1a',
        font=dict(color='#e8e8e8', family='Inter'),
        title_font=dict(color='white', family='Bebas Neue', size=18),
        coloraxis_colorbar=dict(title='Score', tickfont=dict(color='#888')),
    )
    st.plotly_chart(fig_eff, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3: DEEP DIVE
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">PLAYER DEEP DIVE</div>', unsafe_allow_html=True)

    all_players = df['Player'].tolist()
    sel_players = st.multiselect("Select Players to Compare (max 3)",
                                  all_players, default=all_players[:2], max_selections=3)

    if sel_players:
        cols = st.columns(len(sel_players))
        for col, pname in zip(cols, sel_players):
            row = df[df['Player'] == pname].iloc[0]
            with col:
                st.markdown(f"""
                <div style="background:#1a1a1a;border:1px solid rgba(224,58,62,0.3);
                border-radius:10px;padding:1.2rem;text-align:center;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                    color:white;letter-spacing:1px;">{row['Player']}</div>
                    <div style="color:#888;font-size:0.75rem;margin:0.3rem 0 1rem;">
                        {row.get('Squad','—')} • {row.get('League','—')}
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;">
                        <div style="background:#141414;border-radius:8px;padding:0.8rem;">
                            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                            color:#e03a3e;">{row['Final_Score']:.0f}</div>
                            <div style="font-size:0.65rem;color:#555;text-transform:uppercase;">Value Score</div>
                        </div>
                        <div style="background:#141414;border-radius:8px;padding:0.8rem;">
                            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                            color:white;">€{row['Market_Value_M']:.0f}m</div>
                            <div style="font-size:0.65rem;color:#555;text-transform:uppercase;">Market Value</div>
                        </div>
                        <div style="background:#141414;border-radius:8px;padding:0.8rem;">
                            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                            color:white;">{int(row['Gls'])}G / {int(row['Ast'])}A</div>
                            <div style="font-size:0.65rem;color:#555;text-transform:uppercase;">Goals / Assists</div>
                        </div>
                        <div style="background:#141414;border-radius:8px;padding:0.8rem;">
                            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
                            color:white;">{row['SoT%']:.0f}%</div>
                            <div style="font-size:0.65rem;color:#555;text-transform:uppercase;">Shot Accuracy</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Radar Chart
        metrics = ['norm_gls_p90', 'norm_sot_pct', 'norm_ast', 'norm_prgp', 'norm_context']
        labels  = ['Goals/90', 'Shot Acc', 'Assists', 'Prog Passes', 'Schedule Adj']
        colors  = ['#e03a3e', '#f5a623', '#4a90e2']

        fig_radar = go.Figure()
        for pname, color in zip(sel_players, colors):
            row = df[df['Player'] == pname].iloc[0]
            vals = [row.get(m, 0) for m in metrics]
            vals += [vals[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals, theta=labels + [labels[0]],
                fill='toself', name=pname,
                line=dict(color=color, width=2),
                fillcolor=color.replace('#', 'rgba(').replace('e03a3e','224,58,62,0.15)').replace('f5a623','245,166,35,0.15)').replace('4a90e2','74,144,226,0.15)'),
            ))

        fig_radar.update_layout(
            polar=dict(
                bgcolor='#141414',
                radialaxis=dict(visible=True, range=[0,1], color='#444',
                                gridcolor='rgba(255,255,255,0.08)', tickfont=dict(color='#555')),
                angularaxis=dict(color='#888', gridcolor='rgba(255,255,255,0.08)')
            ),
            paper_bgcolor='#1a1a1a',
            font=dict(color='#e8e8e8', family='Inter'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#888')),
            title=dict(text='Player Comparison Radar', font=dict(family='Bebas Neue', size=20, color='white')),
            margin=dict(t=60),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-title">FULL DATASET</div>', unsafe_allow_html=True)

    display_cols = ['Player','Squad','League','Age_num','Pos_primary',
                    'Gls','Ast','SoT%','Gls_p90','Market_Value_M',
                    'Defense_Hardness','Final_Score']
    display_cols = [c for c in display_cols if c in df.columns]

    st.dataframe(
        df[display_cols].style
          .background_gradient(subset=['Final_Score'], cmap='Reds')
          .format({'SoT%':'{:.1f}%','Gls_p90':'{:.2f}',
                   'Market_Value_M':'€{:.0f}m',
                   'Defense_Hardness':'{:.2f}','Final_Score':'{:.1f}'}),
        use_container_width=True, height=400
    )

    csv_out = df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Filtered Data", csv_out,
                       "scouting_results.csv", "text/csv")


# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:#333;
font-family:'Inter',sans-serif;font-size:0.72rem;letter-spacing:1px;">
    BRENTFORD FC SCOUTING INTELLIGENCE &nbsp;•&nbsp; 
    DATA: FBREF + TRANSFERMARKT &nbsp;•&nbsp; 
    BUILT WITH PYTHON + STREAMLIT
</div>
""", unsafe_allow_html=True)
