# 🐝 Brentford FC — Scouting Intelligence System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-2ecc71?style=for-the-badge)

**A data-driven scouting system built to surface undervalued Ligue 1 players — inspired by Brentford FC's analytics-first recruitment philosophy.**

[🚀 Live Dashboard](https://brentford-scouting-9jklvlvyhukvyqzhzdntag.streamlit.app/) · [📊 Data Sources](#data-sources) · [🧮 Algorithm](#the-value-score-algorithm) · [📸 Screenshots](#screenshots)

---

</div>

## 📌 Overview

Brentford FC built their entire identity around identifying elite talent **before** the market prices it correctly. This project replicates that philosophy using open football data — building a full pipeline from raw scraping to an interactive scouting dashboard.

> **The core question:** Which Ligue 1 players deliver elite performance relative to their market value — and which ones is the market sleeping on?

---

## 🎯 What This Project Does

| Feature | Description |
|---|---|
| 🔍 **Value Score Ranking** | Custom algorithm ranks all players by performance-to-price ratio |
| 📊 **Interactive Dashboard** | Filter by position, age, budget, and minutes played |
| 📡 **Radar Comparison** | Compare up to 3 players across 5 dimensions simultaneously |
| 📅 **Schedule Adjustment** | Goals vs harder defenses are weighted higher |
| 💶 **Market Analysis** | Scatter plots reveal hidden outliers vs their Transfermarkt value |
| 📥 **CSV Export** | One-click export of top targets for any recruitment meeting |

---

## 🧮 The Value Score Algorithm

The algorithm is designed around one principle: **raw stats without context are misleading.**

```python
# Step 1 — Normalize each metric (0 to 1 scale)
norm_goals   = normalize(Goals_per_90)       # weight: 0.30
norm_shot    = normalize(Shot_Accuracy)       # weight: 0.18
norm_assists = normalize(Assists)             # weight: 0.22
norm_prog    = normalize(Progressive_Passes) # weight: 0.18
norm_sched   = normalize(Schedule_Hardness)  # weight: 0.12

# Step 2 — Combine into Performance Score
Perf_Score = (norm_goals   * 0.30 +
              norm_shot    * 0.18 +
              norm_assists * 0.22 +
              norm_prog    * 0.18 +
              norm_sched   * 0.12)

# Step 3 — Adjust for market value and age
Value_Score  = Perf_Score / Market_Value_M   # reward low-cost performers
Age_Bonus    = 1.2 if age <= 23 else (1.1 if age <= 25 else 1.0)
Final_Score  = normalize(Value_Score) * 100 * Age_Bonus
```

### 💡 Key Design Decisions

- **Schedule-adjusted scoring** — a goal against PSG or Lens is worth more than one against a bottom-table side
- **Age bonus** — U23 players carry 20% upside; their future ceiling matters
- **Market-relative** — a €5m player outscoring a €40m player on this metric is a genuine scouting signal
- **Min-Max normalization** — all metrics scaled to [0,1] before weighting to prevent any single metric dominating

---

## 🗂️ Project Structure

```
brentford-scouting/
│
├── app/
│   └── main.py                  # Streamlit dashboard (main application)
│
├── data/
│   ├── raw/                     # Raw scraped data (FBref + Transfermarkt)
│   └── processed/
│       └── ligue1_final.csv     # Cleaned, merged, algorithm-ready dataset
│
├── notebooks/
│   ├── 01_scraping.ipynb        # FBref data collection
│   ├── 02_transfermarkt.ipynb   # Market value scraping
│   └── 03_algorithm.ipynb      # Value Score computation & analysis
│
├── assets/
│   ├── bg_stadium.jpg           # Dashboard background image
│   ├── brentford_logo.png       # Club logo
│   └── style.css                # Custom CSS (glass morphism UI)
│
├── requirements.txt
└── README.md
```

---

## 📊 Data Sources

| Source | Data Collected | Method |
|---|---|---|
| **FBref** | Goals, Assists, xG, Progressive Passes, Shot Accuracy, 90s played | `requests` + `BeautifulSoup` |
| **Transfermarkt** | Current market value, Peak value, Nationality | `requests` + `BeautifulSoup` |

### Dataset Coverage

- **League:** Ligue 1, Season 2024–25
- **Players:** 64 outfield players (FW + MF positions)
- **Minimum threshold:** 5+ full 90-minute appearances
- **Market values:** Scraped directly from Transfermarkt, not estimated

---

## 🚀 Getting Started

### Prerequisites

```bash
python >= 3.10
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Goda-Emad/brentford-scouting.git
cd brentford-scouting

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard locally
streamlit run app/main.py
```

### requirements.txt

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
numpy>=1.26.0
requests>=2.31.0
beautifulsoup4>=4.12.0
```

---

## 🖥️ Dashboard Features

### Tab 1 — 🎯 Top Targets
Ranked player cards showing Final Score, age badge (U23 / Prime / Veteran), position, schedule difficulty badge, goals, assists, shot accuracy, and market value. Animated progress bar for each player's score.

### Tab 2 — 📊 Value Analysis
- **Scatter plot:** Market Value (€m) vs Final Score — undervalued players appear top-left
- **Horizontal bar chart:** Top 10 ranked by Value Score with market value annotations
- **Efficiency plot:** Goals/90 vs Shot Accuracy, colored by Final Score
- **Schedule heatmap:** Defense hardness per squad

### Tab 3 — 🔬 Deep Dive
- Side-by-side player comparison cards (up to 3 players)
- **Radar chart** across 5 normalized dimensions
- Goals & Assists bar chart comparison
- Recommended target card with reasoning

### Tab 4 — 📋 Full Dataset
- Sortable, filterable dataframe with column selector
- Position distribution pie chart
- Age distribution histogram
- One-click CSV download (Full / Top 50 / Top 10)

---

## ⚙️ Sidebar Filters

| Filter | Description |
|---|---|
| 📂 Upload CSV | Add players from any new league |
| 🌍 League | Filter by league (Ligue 1 + any uploaded) |
| 📍 Position | FW, MF, DF, GK |
| 🎂 Age Range | Slider: min–max age |
| 💶 Max Market Value | Budget cap in €m |
| ⏱️ Min 90s Played | Minimum playing time threshold |
| 📊 Top N | Show top 10 / 15 / 20 / 30 / 50 targets |

---

## 🎨 Design System

The dashboard uses a custom **glass morphism** UI with:

- **Typography:** Bebas Neue (display) + Inter (body)
- **Color palette:** `#e03a3e` red accent on `#080808` near-black
- **Cards:** `rgba(8,8,8,0.82)` background + `backdrop-filter: blur(16px)`
- **Background:** Stadium image loaded as base64, rendered via fixed `<div>` (Streamlit Cloud compatible)
- **Charts:** Plotly with transparent `paper_bgcolor`, dark `plot_bgcolor`

---

## 🌍 Live Deployment

The dashboard is deployed on **Streamlit Community Cloud**.

🔗 **[Open Dashboard →](https://brentford-scouting-9jklvlvyhukvyqzhzdntag.streamlit.app/)**

> The app loads demo data (8 Ligue 1 players) when the CSV is not found — all features remain functional for exploration.

---

## 🗺️ Roadmap

- [ ] Add Premier League, Bundesliga, and La Liga datasets
- [ ] Integrate xG and xA from StatsBomb open data
- [ ] Build automated weekly data refresh pipeline
- [ ] Add player similarity engine (cosine distance on normalized metrics)
- [ ] Export scouting report as PDF per player

---

## 👤 Author

**Goda Emad**
Data Analyst · Football Analytics · Python · Streamlit

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/goda-emad/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Goda-Emad)

📞 +20 112 624 2932

---

## 🙏 Acknowledgements

Special thanks to **Dr. Mohamed Elhaddad** for his continuous guidance, encouragement, and mentorship throughout this project. Having a mentor who pushes you to go beyond what's expected made all the difference.

---

## 📄 License

This project is for educational and portfolio purposes. Data sourced from FBref and Transfermarkt — all rights belong to their respective owners.

---

<div align="center">
  <sub>Built with ❤️ and a lot of coffee · Inspired by Brentford FC's data-first philosophy</sub>
</div>
