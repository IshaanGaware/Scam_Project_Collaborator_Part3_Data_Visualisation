"""
Scammed in Australia — Interactive Streamlit Dashboard (V1 + V2 Hybrid)
Group 19 | MDSI Data Visualisation & Storytelling | UTS 2026

Run with:
    pip install streamlit pandas numpy matplotlib plotly openpyxl
    streamlit run streamlit_app_group19_advanced.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import re
import warnings
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")

#page config

st.set_page_config(
    page_title="Scammed in Australia",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

#custom css

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #182033 0%, #0b0f17 40%, #080b10 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #252733 0%, #171923 100%);
}

[data-testid="stSidebar"] * {
    color: #f4f4f4;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/*V2*/
.emotional-hero {
    margin-top: 1rem;
    margin-bottom: 2rem;
}

.emotional-tag {
    color: #ff4d4d;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 0.5rem;
}

.emotional-title-1 {
    font-size: 4rem;
    font-weight: 900;
    line-height: 1.05;
    margin: 0;
    background: linear-gradient(120deg, #ff4d4d, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.emotional-title-2 {
    font-size: 4rem;
    font-weight: 900;
    line-height: 1.05;
    margin: 0;
    color: #f5f5f7;
    letter-spacing: -0.02em;
}

/*Big emotional number*/
.big-number-label {
    font-size: 1rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 600;
    margin-top: 1.5rem;
}

.big-number {
    font-size: 5rem;
    font-weight: 800;
    color: #ff4d4d;
    line-height: 1;
    letter-spacing: -0.04em;
    margin: 0.5rem 0;
}

.big-number-context {
    font-size: 1.3rem;
    color: #f5f5f7;
    font-style: italic;
    margin-top: 1rem;
    max-width: 800px;
    line-height: 1.5;
}

/*Mini stat cards */
.stat-mini {
    text-align: center;
    padding: 1.5rem 1rem;
    background: rgba(20, 25, 35, 0.85);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.06);
    height: 100%;
}

.stat-mini-number {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    line-height: 1.2;
}

.stat-mini-label {
    font-size: 0.85rem;
    color: #9ca3af;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/*V1 */
.context-pill-row {
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.hero-pill {
    display: inline-block;
    padding: 0.45rem 0.9rem;
    margin: 0.15rem 0.3rem 0.15rem 0;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    color: #f8fafc;
    font-size: 0.9rem;
    font-weight: 500;
}

.hero-pill-accent {
    background: rgba(255, 77, 77, 0.15);
    border-color: rgba(255, 77, 77, 0.4);
    color: #ff8080;
    font-weight: 600;
}

.glass-card {
    padding: 1.25rem;
    border-radius: 22px;
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 12px 35px rgba(0,0,0,0.28);
}

.section-title {
    color: #f8fafc;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 1rem;
    margin-bottom: 0.25rem;
}

.section-caption {
    color: #e5e7eb;
    font-style: italic;
    margin-bottom: 1rem;
}

/*V2 */
.pull-quote {
    border-left: 4px solid #ff4d4d;
    padding: 1.5rem 2rem;
    margin: 1.5rem 0;
    background: rgba(255, 77, 77, 0.06);
    border-radius: 0 16px 16px 0;
}

.pull-quote-text {
    font-size: 1.2rem;
    font-style: italic;
    color: #f5f5f7;
    line-height: 1.5;
    margin: 0;
}

.pull-quote-attr {
    color: #9ca3af;
    font-size: 0.85rem;
    margin-top: 0.6rem;
}

/*V1 */
.insight-box {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: rgba(241,196,15,0.15);
    border: 1px solid rgba(241,196,15,0.35);
    color: #ffffff;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
}

.success-box {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: rgba(39,174,96,0.16);
    border: 1px solid rgba(39,174,96,0.35);
    color: #ffffff;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
}

.warning-box {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: rgba(192,57,43,0.16);
    border: 1px solid rgba(192,57,43,0.35);
    color: #ffffff;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
}

.small-muted {
    color: #94a3b8;
    font-size: 0.9rem;
}

div[data-testid="stMetric"] {
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

div[data-testid="stMetricLabel"] {
    color: #ffffff !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(15,23,42,0.75);
    border-radius: 14px 14px 0 0;
    padding: 0.75rem 1rem;
    border: 1px solid rgba(255,255,255,0.08);
}

.stTabs [aria-selected="true"] {
    background-color: rgba(192,57,43,0.55);
}

hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.13);
    margin: 2rem 0;
}

[data-testid="stSidebar"] button {
    background-color: rgba(192, 57, 43, 0.85) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-weight: 600;
}

[data-testid="stSidebar"] button:hover {
    background-color: rgba(192, 57, 43, 1.0) !important;
    border-color: #ffffff !important;
}

/* Fix sidebar dropdown text color */
[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: rgba(15, 23, 42, 0.85) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.85) !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #ffffff !important;
}

/* Multiselect tags in sidebar */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: rgba(192, 57, 43, 0.85) !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #ffffff !important;
}

/* Dropdown menu (when open) */
[data-baseweb="popover"] [role="listbox"] {
    background-color: rgba(20, 25, 35, 0.98) !important;
}

[data-baseweb="popover"] [role="option"] {
    color: #ffffff !important;
}

[data-baseweb="popover"] [role="option"]:hover {
    background-color: rgba(192, 57, 43, 0.4) !important;
}

/* Brighten all Streamlit text in main area */
.main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
    color: #ffffff !important;
}

.main p, .main label, .main .stMarkdown {
    color: #f8fafc !important;
}

.main [data-testid="stCaptionContainer"],
.main .stCaption,
.main small {
    color: #cbd5e1 !important;
    font-size: 0.95rem !important;
}

.main label[data-testid="stWidgetLabel"],
.main .stRadio label,
.main .stSelectbox label,
.main .stMultiSelect label,
.main .stSlider label {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

.main .stRadio div[role="radiogroup"] label {
    color: #ffffff !important;
    font-weight: 500 !important;
}

.main .streamlit-expanderHeader {
    color: #ffffff !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricLabel"] p {
    color: #ffffff !important;
}

/*V2 */
.cta-box {
    background: linear-gradient(135deg, #ff4d4d 0%, #c0392b 100%);
    border-radius: 24px;
    padding: 2.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    text-align: center;
    box-shadow: 0 20px 50px rgba(255, 77, 77, 0.2);
}

.cta-headline {
    color: white;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
    line-height: 1.3;
}

.cta-body {
    color: rgba(255,255,255,0.95);
    font-size: 1.1rem;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
}

/*V2 */
.action-card {
    background: rgba(20, 25, 35, 0.85);
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
    border-left: 4px solid #ff4d4d;
}

.action-verb {
    color: #ff4d4d;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-size: 0.85rem;
}

.action-body {
    color: #f5f5f7;
    font-size: 1.05rem;
    margin: 0.5rem 0;
    font-weight: 600;
    line-height: 1.4;
}

.action-why {
    color: #9ca3af;
    font-size: 0.9rem;
    font-style: italic;
}
</style>
""",
    unsafe_allow_html=True,
)

#color

P = dict(
    red="#C0392B", orange="#E67E22", teal="#16A085", navy="#1A3A5C",
    gold="#F1C40F", grey="#7F8C8D", light="#ECF0F1", green="#27AE60",
    purple="#8E44AD", blue="#2980B9", dark="#0B0F17",
)

STATE_CLR = dict(
    NSW="#1A3A5C", VIC="#2980B9", QLD="#C0392B", WA="#E67E22",
    SA="#16A085", ACT="#8E44AD", TAS="#27AE60", NT="#F39C12",
)

# Approximate state/territory centroids for the interactive geographic risk map
STATE_COORDS = pd.DataFrame({
    "state": ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"],
    "lat": [-31.2532, -37.0201, -22.5752, -25.2744, -30.0002, -41.4545, -35.4735, -19.4914],
    "lon": [146.9211, 144.9646, 144.0848, 122.0137, 136.2092, 145.9707, 149.0124, 132.5510],
})

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "#FAFAFA",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelsize": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    "font.family": "sans-serif", "xtick.labelsize": 8, "ytick.labelsize": 8,
})

PLOTLY_TEMPLATE = "plotly_dark"

#data load

@st.cache_data
def load_data():
    def money(v):
        if pd.isna(v):
            return 0.0
        return float(re.sub(r"[^\d.]", "", str(v)) or 0)

    STATE_ABB = {
        "New South Wales": "NSW", "Victoria": "VIC", "Queensland": "QLD",
        "Western Australia": "WA", "South Australia": "SA", "Tasmania": "TAS",
        "Australian Capital Territory": "ACT", "Northern Territory": "NT",
        "Outside of Australia": "INTL", "Unspecified": "UNK",
    }

    AGE_ORDER = ["Under 18", "18 - 24", "25 - 34", "35 - 44",
                 "45 - 54", "55 - 64", "65 and over"]

    data_dir = Path("data")
    scam = pd.read_csv(data_dir / "Scamwatch903 Public Scams Dashboard - Export.csv")

    scam = scam.rename(columns={
        "StartOfMonth": "month", "Address_State": "state_full",
        "Scam___Contact_Mode": "contact_mode", "Complainant_Age": "age_group",
        "Complainant_Gender": "gender", "Category_Level_3": "scam_type",
        "Amount_lost": "amount_lost_raw", "Number_of_reports": "reports",
    })

    scam["month"] = pd.to_datetime(scam["month"])
    scam["amount_lost"] = scam["amount_lost_raw"].apply(money)
    scam["reports"] = pd.to_numeric(scam["reports"], errors="coerce").fillna(0)
    scam["state"] = scam["state_full"].map(STATE_ABB)

    AUS = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
    scam_aus = scam[scam["state"].isin(AUS)].copy()

    abs_raw = pd.read_excel(data_dir / "32350DS0003_2024.xlsx",
                            sheet_name="Table 3", header=5)
    abs_raw.columns = ["st", "sn", "lc", "ln"] + [f"p{i}" for i in range(0, 90, 5)] + ["total"]
    abs_raw = abs_raw.iloc[1:].copy()
    for c in abs_raw.columns[4:]:
        abs_raw[c] = pd.to_numeric(abs_raw[c], errors="coerce")
    abs_raw = abs_raw[abs_raw["total"].notna()].copy()
    abs_raw["state"] = abs_raw["sn"].map(STATE_ABB)
    abs_raw["pop_young"] = abs_raw[["p15", "p20"]].sum(axis=1)
    abs_raw["pop_elderly"] = abs_raw[["p65", "p70", "p75", "p80", "p85"]].sum(axis=1)

    state_pop = (
        abs_raw.groupby("state")
        .agg(young_pop=("pop_young", "sum"),
             elderly_pop=("pop_elderly", "sum"),
             total_pop=("total", "sum"))
        .reset_index()
    )
    state_pop = state_pop[state_pop["state"].isin(AUS)]

    return scam, scam_aus, state_pop, AGE_ORDER, AUS


scam_raw, scam_aus, state_pop, AGE_ORDER, AUS_STATES = load_data()

#helpers

def money_fmt(v):
    if pd.isna(v):
        return "$0"
    if abs(v) >= 1e9:
        return f"${v / 1e9:.1f}B"
    if abs(v) >= 1e6:
        return f"${v / 1e6:.1f}M"
    if abs(v) >= 1e3:
        return f"${v / 1e3:.1f}k"
    return f"${v:,.0f}"


def number_fmt(v):
    if pd.isna(v):
        return "0"
    return f"{v:,.0f}"


def safe_div(a, b):
    return a / b if b not in [0, None] and not pd.isna(b) else 0


def score_0_100(series):
    """Convert a numeric series into a 0-100 score. Handles flat/empty series safely."""
    s = pd.to_numeric(series, errors="coerce").fillna(0)
    if len(s) == 0 or s.max() == s.min():
        return pd.Series(np.repeat(50, len(s)), index=s.index)
    return (s - s.min()) / (s.max() - s.min()) * 100


def clean_hover_money(fig, name_col="y"):
    """Small utility kept for future hover cleanup."""
    return fig


def plotly_layout(fig, height=460):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.55)",
        font=dict(color="#ffffff", size=13),
        margin=dict(l=20, r=20, t=80, b=40),
        title=dict(
            font=dict(size=22, color="#ffffff", family="Arial Black, sans-serif"),
            x=0.02, xanchor="left",
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0.3)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1,
            font=dict(color="#ffffff", size=12),
        ),
        xaxis=dict(
            title_font=dict(color="#ffffff", size=14),
            tickfont=dict(color="#e5e7eb", size=12),
            gridcolor="rgba(255,255,255,0.1)",
        ),
        yaxis=dict(
            title_font=dict(color="#ffffff", size=14),
            tickfont=dict(color="#e5e7eb", size=12),
            gridcolor="rgba(255,255,255,0.1)",
        ),
    )
    return fig


def section_header(title, caption):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-caption'>{caption}</div>", unsafe_allow_html=True)


def insight(text, kind="insight"):
    css_class = {
        "insight": "insight-box", "success": "success-box", "warning": "warning-box",
    }.get(kind, "insight-box")
    st.markdown(f"<div class='{css_class}'>{text}</div>", unsafe_allow_html=True)


def pull_quote(text, attr=None):
    """V2 style pull quote — replaces dull insight boxes where emotion matters"""
    attr_html = f"<p class='pull-quote-attr'>{attr}</p>" if attr else ""
    st.markdown(f"""
    <div class='pull-quote'>
        <p class='pull-quote-text'>{text}</p>
        {attr_html}
    </div>
    """, unsafe_allow_html=True)


def get_filtered_data(selected_state, selected_ages, selected_types, month_range):
    filtered = scam_aus.copy()
    if selected_state != "All States":
        filtered = filtered[filtered["state"] == selected_state]
    if selected_ages:
        filtered = filtered[filtered["age_group"].isin(selected_ages)]
    if selected_types:
        filtered = filtered[filtered["scam_type"].isin(selected_types)]
    if month_range:
        start_m, end_m = month_range
        filtered = filtered[
            (filtered["month"] >= pd.to_datetime(start_m))
            & (filtered["month"] <= pd.to_datetime(end_m))
        ]
    return filtered


#sessions

DEFAULT_AGES = [a for a in AGE_ORDER if a != "Unspecified"]
DEFAULT_TYPES = sorted(scam_aus["scam_type"].dropna().unique())

if "selected_state" not in st.session_state:
    st.session_state.selected_state = "All States"
if "selected_ages" not in st.session_state:
    st.session_state.selected_ages = DEFAULT_AGES
if "selected_types" not in st.session_state:
    st.session_state.selected_types = DEFAULT_TYPES
if "month_range" not in st.session_state:
    st.session_state.month_range = (
        scam_aus["month"].min().to_pydatetime(),
        scam_aus["month"].max().to_pydatetime(),
    )

#sidebar

with st.sidebar:
    st.title("🔍 Filter Controls")
    st.caption("Change the lens. Watch the story update.")
    st.markdown("---")

    selected_state = st.selectbox(
        "📍 State / Territory",
        ["All States"] + AUS_STATES,
        key="selected_state",
    )

    selected_ages = st.multiselect(
        "👤 Age Groups",
        options=DEFAULT_AGES,
        key="selected_ages",
    )

    selected_types = st.multiselect(
        "🎯 Scam Types",
        options=DEFAULT_TYPES,
        key="selected_types",
    )

    st.markdown("### 📅 Time Window")
    month_range = st.slider(
        "Months covered",
        min_value=scam_aus["month"].min().to_pydatetime(),
        max_value=scam_aus["month"].max().to_pydatetime(),
        value=st.session_state.month_range,
        format="MMM YYYY",
        key="month_slider",
    )
    st.session_state.month_range = month_range

    st.markdown("---")
    if st.button("🔄 Reset all filters", use_container_width=True):
        st.session_state.selected_state = "All States"
        st.session_state.selected_ages = DEFAULT_AGES
        st.session_state.selected_types = DEFAULT_TYPES
        st.session_state.month_range = (
            scam_aus["month"].min().to_pydatetime(),
            scam_aus["month"].max().to_pydatetime(),
        )
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Data Sources")
    st.markdown("""
- **Scamwatch** / ACCC
- **ABS Population** · 2024
- **ACMA Enforcement**
- **ACMA Communications Survey**
    """)
    st.markdown("---")
    st.caption("Group 19 · MDSI UTS · 2026")

filtered = get_filtered_data(selected_state, selected_ages, selected_types, month_range)

# Transparent scope check: prevents confusion between raw EDA totals and dashboard-filtered totals
raw_total_losses = scam_raw["amount_lost"].sum()
aus_total_losses = scam_aus["amount_lost"].sum()
filtered_total_losses = filtered["amount_lost"].sum()
raw_total_reports = scam_raw["reports"].sum()
aus_total_reports = scam_aus["reports"].sum()

#narative

STATE_NARRATIVE = {
    "NSW": "**NSW** leads in raw numbers, but population size inflates the headline. Per-capita analysis gives a fairer risk picture.",
    "VIC": "**Victoria** shows a strong urban digital-risk profile, especially across working-age adults.",
    "QLD": "**Queensland** has a notable exposure to phone and online scam channels across older cohorts.",
    "WA": "**Western Australia** often appears more exposed once losses are adjusted for population.",
    "SA": "**South Australia** has an older demographic profile, making severity-focused protection important.",
    "ACT": "**ACT** can show a distinctive profile linked to its public-sector workforce and digital activity.",
    "TAS": "**Tasmania** highlights the importance of regional digital literacy and local support channels.",
    "NT": "**Northern Territory** requires special attention because per-capita exposure can reveal hidden vulnerability.",
}

#compute

total_reports = filtered["reports"].sum()
total_losses = filtered["amount_lost"].sum()
avg_loss = safe_div(total_losses, total_reports)
n_months = filtered["month"].nunique()

#V2
minutes_in_period = n_months * 30 * 24 * 60 if n_months > 0 else 1
loss_per_minute = total_losses / minutes_in_period
minutes_per_report = minutes_in_period / total_reports if total_reports > 0 else 0

top_type = (
    filtered.groupby("scam_type")["amount_lost"].sum().idxmax()
    if len(filtered) > 0 and filtered["amount_lost"].sum() > 0
    else "N/A"
)

#V2

st.markdown(f"""
<div class="emotional-hero">
    <div class="emotional-tag">A data investigation · Group 19 · UTS MDSI 2026</div>
    <div class="emotional-title-1">Australia is being robbed.</div>
    <div class="emotional-title-2">One scam at a time.</div>
</div>
""", unsafe_allow_html=True)

#big emotional number
st.markdown(f"""
<div class="big-number-label">Total stolen under current filters</div>
<div class="big-number">{money_fmt(total_losses)}</div>
<div class="big-number-context">
    That's roughly <b>${loss_per_minute:,.0f} stolen every minute</b> of every day —
    while you read this sentence, another Australian became a victim.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#V2
sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-number">{total_reports:,.0f}</div>
        <div class="stat-mini-label">Reports filed</div>
    </div>
    """, unsafe_allow_html=True)
with sc2:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-number">1 every {minutes_per_report:.0f} min</div>
        <div class="stat-mini-label">New victim</div>
    </div>
    """, unsafe_allow_html=True)
with sc3:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-number">{money_fmt(avg_loss)}</div>
        <div class="stat-mini-label">Average loss per victim</div>
    </div>
    """, unsafe_allow_html=True)

#stakeholder + narrative arc
st.markdown(f"""
<div class="context-pill-row">
    <span class="hero-pill hero-pill-accent">🎯 Stakeholder: ACMA Commissioner</span>
    <span class="hero-pill">📖 Narrative Arc: The Detective</span>
    <span class="hero-pill">📍 Current Lens: {selected_state}</span>
    <span class="hero-pill">{len(selected_ages)} age groups · {len(selected_types)} scam types</span>
</div>
""", unsafe_allow_html=True)

if selected_state != "All States" and selected_state in STATE_NARRATIVE:
    st.info(f"📍 {STATE_NARRATIVE[selected_state]}")

st.info(
    f"""
**Data scope check:** Raw dataset losses: **{money_fmt(raw_total_losses)}** across **{number_fmt(raw_total_reports)}** reports ·
Australian states/territories only: **{money_fmt(aus_total_losses)}** across **{number_fmt(aus_total_reports)}** reports ·
Current filtered view: **{money_fmt(filtered_total_losses)}**.
"""
)

if len(filtered) == 0:
    st.error("No data matches the current filters. Try resetting the filters in the sidebar.")
    st.stop()

#download button
summary_col, download_col = st.columns([3, 1])
with summary_col:
    st.info(
        f"**Current lens:** State: `{selected_state}` · "
        f"Age groups: `{len(selected_ages)}` selected · "
        f"Scam types: `{len(selected_types)}` selected · Months: `{n_months}`"
    )
with download_col:
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv,
        file_name="filtered_scamwatch_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown("---")

#act 1

section_header(
    "🔍 Act 1: The Anomaly",
    "Establishing the scale of the crisis for a non-technical executive audience.",
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 Total Reports", number_fmt(total_reports))
c2.metric("💸 Total $ Lost", money_fmt(total_losses))
c3.metric("📅 Months Covered", str(n_months))
c4.metric("💰 Avg Loss / Report", money_fmt(avg_loss))

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# Advanced modelling layer: monthly trend + simple 3-month projection
# ─────────────────────────────────────────────────────────────────────────────
mon_f = (
    filtered.groupby("month")
    .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
    .reset_index()
    .sort_values("month")
)
mon_f["losses_m"] = mon_f["losses"] / 1e6
mon_f["month_label"] = mon_f["month"].dt.strftime("%b %Y")

forecast_df = pd.DataFrame()
if len(mon_f) >= 3:
    x = np.arange(len(mon_f))
    y = mon_f["losses_m"].values
    slope, intercept = np.polyfit(x, y, 1)
    future_x = np.arange(len(mon_f), len(mon_f) + 3)
    future_months = pd.date_range(mon_f["month"].max() + pd.offsets.MonthBegin(1), periods=3, freq="MS")
    forecast_values = np.maximum(slope * future_x + intercept, 0)
    forecast_df = pd.DataFrame({
        "month": future_months,
        "month_label": future_months.strftime("%b %Y"),
        "losses_m": forecast_values,
        "type": "Projected"
    })
    actual_df = mon_f[["month", "month_label", "losses_m"]].copy()
    actual_df["type"] = "Actual"
    trend_plot = pd.concat([actual_df, forecast_df], ignore_index=True)

    fig_trend = px.line(
        trend_plot,
        x="month_label",
        y="losses_m",
        color="type",
        markers=True,
        title="Advanced Modelling: 3-Month Scam Loss Projection",
        labels={"month_label": "Month", "losses_m": "Losses ($M)", "type": "Series"},
        color_discrete_map={"Actual": P["red"], "Projected": P["gold"]},
    )
    fig_trend.update_traces(
        hovertemplate="<b>%{x}</b><br>Losses: $%{y:.1f}M<extra></extra>"
    )
    fig_trend.add_vrect(
        x0=mon_f["month_label"].iloc[-1],
        x1=forecast_df["month_label"].iloc[-1],
        fillcolor="rgba(241,196,15,0.12)",
        line_width=0,
        annotation_text="Projection window",
        annotation_position="top left",
    )
    fig_trend = plotly_layout(fig_trend, height=420)
    st.plotly_chart(fig_trend, use_container_width=True)

    projected_loss_3m = forecast_df["losses_m"].sum() * 1e6
    pull_quote(
        f"If the current trend continues, the next three months could expose Australians to roughly "
        f"<b>{money_fmt(projected_loss_3m)}</b> in additional scam losses. This is a simple trend projection, "
        f"not a formal forecast — its purpose is to show the cost of delay."
    )
else:
    st.caption("Projection needs at least three months of data under the current filters.")

#scam type distribution
type_f = (
    filtered.groupby("scam_type")
    .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
    .reset_index()
    .sort_values("losses", ascending=False)
)
type_f["avg_loss"] = type_f["losses"] / type_f["reports"].replace(0, np.nan)
type_f["loss_pct"] = type_f["losses"] / type_f["losses"].sum() * 100

left, right = st.columns([1.15, 1])

with left:
    top_type_chart = type_f.head(10).copy()
    top_type_chart["losses_m"] = top_type_chart["losses"] / 1e6

    fig_type = px.bar(
        top_type_chart.sort_values("losses_m"),
        x="losses_m", y="scam_type", orientation="h",
        title="Top Scam Types by Total Losses",
        labels={"losses_m": "$ Millions", "scam_type": "Scam Type"},
        text=top_type_chart.sort_values("losses_m")["losses_m"].round(1),
        color="losses_m", color_continuous_scale="Reds",
        hover_data={"reports": ":,.0f", "losses": ":,.0f", "avg_loss": ":,.0f"},
    )
    fig_type.update_traces(texttemplate="$%{text}M", textposition="outside")
    fig_type = plotly_layout(fig_type, height=520)
    st.plotly_chart(fig_type, use_container_width=True)

with right:
    pie_data = type_f.head(6).copy()
    if len(type_f) > 6:
        other_row = pd.DataFrame({
            "scam_type": ["Other scams"],
            "reports": [type_f.iloc[6:]["reports"].sum()],
            "losses": [type_f.iloc[6:]["losses"].sum()],
            "avg_loss": [safe_div(type_f.iloc[6:]["losses"].sum(),
                                   type_f.iloc[6:]["reports"].sum())],
            "loss_pct": [type_f.iloc[6:]["losses"].sum() / type_f["losses"].sum() * 100],
        })
        pie_data = pd.concat([pie_data, other_row], ignore_index=True)

    fig_pie = px.pie(pie_data, names="scam_type", values="losses",
                    hole=0.45, title="% of Losses by Scam Type")
    fig_pie.update_traces(textposition="inside", textinfo="percent")
    fig_pie = plotly_layout(fig_pie, height=520)
    st.plotly_chart(fig_pie, use_container_width=True)

#V2
top_type_amount = type_f.iloc[0]["losses"] if len(type_f) > 0 else 0
top_type_pct = type_f.iloc[0]["loss_pct"] if len(type_f) > 0 else 0
pull_quote(
    f"<b>{top_type}</b> alone accounts for <b>{money_fmt(top_type_amount)}</b> "
    f"in losses - that's <b>{top_type_pct:.0f}%</b> of all financial damage tracked. "
)

st.markdown("---")

#2

section_header(
    "🕵️ Act 2: The Investigation",
    "Who is being targeted? Where? How? Explore the evidence through linked analytical views.",
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Victim Profile", "📍 Geographic Risk", "📡 Contact Channels",
    "⚠️ Risk Score", "⚖️ Compare Segments",
])

#tab 1
with tab1:
    age_f = (
        filtered[filtered["age_group"].isin(DEFAULT_AGES)]
        .groupby("age_group")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
    )
    age_f["age_group"] = pd.Categorical(age_f["age_group"], categories=DEFAULT_AGES, ordered=True)
    age_f = age_f.sort_values("age_group")
    age_f["avg_loss"] = age_f["losses"] / age_f["reports"].replace(0, np.nan)
    age_f["losses_m"] = age_f["losses"] / 1e6

    a1, a2 = st.columns([1, 1])

    with a1:
        fig_age = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Reports by Age", "Avg Loss per Report ($)"),
            horizontal_spacing=0.18,
        )
        fig_age.add_trace(
            go.Bar(
                y=age_f["age_group"].astype(str), x=age_f["reports"],
                name="Reports", orientation="h", marker_color=P["orange"],
                hovertemplate="<b>%{y}</b><br>Reports: %{x:,.0f}<extra></extra>",
                showlegend=False,
            ), row=1, col=1,
        )
        fig_age.add_trace(
            go.Bar(
                y=age_f["age_group"].astype(str), x=age_f["avg_loss"],
                name="Avg loss per report", orientation="h", marker_color=P["navy"],
                hovertemplate="<b>%{y}</b><br>Avg loss: $%{x:,.0f}<extra></extra>",
                showlegend=False,
            ), row=1, col=2,
        )
        fig_age.update_layout(title="Reports vs Average Loss by Age")
        fig_age = plotly_layout(fig_age, height=500)
        st.plotly_chart(fig_age, use_container_width=True)

    with a2:
        fig_bubble = px.scatter(
            age_f, x="reports", y="avg_loss", size="losses",
            color="age_group", text="age_group",
            title="Risk Matrix: Volume vs Severity",
            labels={"reports": "Number of Reports",
                    "avg_loss": "Average Loss per Report",
                    "losses": "Total Losses", "age_group": "Age Group"},
            hover_data={"reports": ":,.0f", "avg_loss": ":,.0f",
                       "losses": ":,.0f", "age_group": False},
        )
        fig_bubble.update_traces(textposition="middle center")
        fig_bubble = plotly_layout(fig_bubble, height=500)
        st.plotly_chart(fig_bubble, use_container_width=True)

    top_avg_age = age_f.sort_values("avg_loss", ascending=False).iloc[0]["age_group"]
    top_loss_age = age_f.sort_values("losses", ascending=False).iloc[0]["age_group"]

    #2
    pull_quote(
        f"<b>{top_loss_age}</b> lose the most overall — but <b>{top_avg_age}</b> lose "
        f"the most <i>per incident</i>. That distinction matters: prevention messaging "
        f"cannot be one-size-fits-all.",
    )

#tab 2
with tab2:
    state_f = (
        filtered.groupby("state")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
        .merge(state_pop, on="state", how="left")
    )
    state_f["loss_per_100k"] = state_f["losses"] / state_f["total_pop"] * 100_000
    state_f["reports_per_100k"] = state_f["reports"] / state_f["total_pop"] * 100_000
    state_f["losses_m"] = state_f["losses"] / 1e6
    state_f = state_f.dropna(subset=["total_pop"])

    # Advanced geographic modelling: a policy-ready State Harm Index
    state_f["loss_score"] = score_0_100(state_f["losses"])
    state_f["severity_score"] = score_0_100(state_f["losses"] / state_f["reports"].replace(0, np.nan))
    state_f["percap_score"] = score_0_100(state_f["loss_per_100k"])
    state_f["volume_score"] = score_0_100(state_f["reports"])
    state_f["state_harm_index"] = (
        0.40 * state_f["loss_score"]
        + 0.25 * state_f["percap_score"]
        + 0.20 * state_f["severity_score"]
        + 0.15 * state_f["volume_score"]
    )
    state_f = state_f.merge(STATE_COORDS, on="state", how="left")

    map_col, table_col = st.columns([1.25, 0.9])
    with map_col:
        fig_map = px.scatter_geo(
            state_f,
            lat="lat", lon="lon",
            scope="world",
            size="losses",
            color="state_harm_index",
            hover_name="state",
            text="state",
            projection="natural earth",
            title="Australia Scam Harm Map: Losses + Per-Capita Exposure",
            color_continuous_scale="Reds",
            hover_data={
                "losses": ":,.0f",
                "reports": ":,.0f",
                "loss_per_100k": ":,.0f",
                "reports_per_100k": ":,.0f",
                "state_harm_index": ":.1f",
                "lat": False, "lon": False,
            },
        )
        fig_map.update_geos(
            lataxis_range=[-45, -10],
            lonaxis_range=[110, 155],
            showland=True, landcolor="rgba(15,23,42,0.8)",
            showcountries=False, showcoastlines=True, coastlinecolor="rgba(255,255,255,0.35)",
            showocean=True, oceancolor="rgba(8,11,16,0.9)",
            fitbounds=False,
        )
        fig_map.update_traces(
            textposition="top center",
            marker=dict(line=dict(width=1, color="white")),
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Total losses: $%{customdata[0]:,.0f}<br>"
                "Reports: %{customdata[1]:,.0f}<br>"
                "Loss per 100k: $%{customdata[2]:,.0f}<br>"
                "Reports per 100k: %{customdata[3]:,.0f}<br>"
                "State Harm Index: %{customdata[4]:.1f}/100"
                "<extra></extra>"
            )
        )
        fig_map = plotly_layout(fig_map, height=520)
        st.plotly_chart(fig_map, use_container_width=True)

    with table_col:
        st.markdown("### 🧭 State Harm Index")
        st.caption("Composite score: 40% losses, 25% per-capita exposure, 20% severity, 15% report volume.")
        state_index_view = state_f.sort_values("state_harm_index", ascending=False)[
            ["state", "state_harm_index", "losses", "loss_per_100k", "reports"]
        ].copy()
        state_index_view["state_harm_index"] = state_index_view["state_harm_index"].map(lambda x: f"{x:.1f}")
        state_index_view["losses"] = state_index_view["losses"].map(lambda x: f"${x:,.0f}")
        state_index_view["loss_per_100k"] = state_index_view["loss_per_100k"].map(lambda x: f"${x:,.0f}")
        state_index_view = state_index_view.rename(columns={
            "state": "State",
            "state_harm_index": "Harm Index",
            "losses": "Losses",
            "loss_per_100k": "Loss / 100k",
            "reports": "Reports",
        })
        st.dataframe(state_index_view, use_container_width=True, hide_index=True, height=430)

    g1, g2 = st.columns([1, 1])

    with g1:
        fig_raw = px.bar(
            state_f.sort_values("losses_m", ascending=True),
            x="losses_m", y="state", orientation="h",
            color="state", color_discrete_map=STATE_CLR,
            title="Raw Losses by State",
            labels={"losses_m": "$ Millions", "state": "State"},
            text=state_f.sort_values("losses_m", ascending=True)["losses_m"].round(1),
            hover_data={"reports": ":,.0f", "losses": ":,.0f"},
        )
        fig_raw.update_traces(texttemplate="$%{text}M", textposition="outside")
        fig_raw = plotly_layout(fig_raw, height=480)
        st.plotly_chart(fig_raw, use_container_width=True)

    with g2:
        fig_pc = px.bar(
            state_f.sort_values("loss_per_100k", ascending=True),
            x="loss_per_100k", y="state", orientation="h",
            color="state", color_discrete_map=STATE_CLR,
            title="Per-Capita Loss Exposure",
            labels={"loss_per_100k": "$ Lost per 100k Residents", "state": "State"},
            text=state_f.sort_values("loss_per_100k", ascending=True)["loss_per_100k"].round(0),
            hover_data={"reports_per_100k": ":,.0f", "total_pop": ":,.0f"},
        )
        fig_pc.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig_pc = plotly_layout(fig_pc, height=480)
        st.plotly_chart(fig_pc, use_container_width=True)

    if len(state_f) > 0:
        raw_leader = state_f.sort_values("losses", ascending=False).iloc[0]["state"]
        pc_leader = state_f.sort_values("loss_per_100k", ascending=False).iloc[0]["state"]
        pull_quote(
            f"<b>{raw_leader}</b> leads in raw losses, but <b>{pc_leader}</b> has the "
            f"highest per-capita exposure. Resource allocation cannot be based on "
            f"headline totals alone — that misses the real victims.",
        )

#tab 3
with tab3:
    contact_clean = filtered[
        filtered["contact_mode"].notna()
        & (filtered["contact_mode"].str.lower() != "unspecified")
    ].copy()

    channel_f = (
        contact_clean.groupby("contact_mode")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
        .sort_values("losses", ascending=False)
    )
    channel_f["avg_loss"] = channel_f["losses"] / channel_f["reports"].replace(0, np.nan)
    channel_f["losses_m"] = channel_f["losses"] / 1e6

    ch1, ch2 = st.columns([1, 1])

    with ch1:
        fig_channel = px.bar(
            channel_f.sort_values("losses_m"),
            x="losses_m", y="contact_mode", orientation="h",
            title="Losses by Contact Channel",
            labels={"losses_m": "$ Millions", "contact_mode": "Contact Channel"},
            text=channel_f.sort_values("losses_m")["losses_m"].round(1),
            color="losses_m", color_continuous_scale="OrRd",
            hover_data={"reports": ":,.0f", "avg_loss": ":,.0f"},
        )
        fig_channel.update_traces(texttemplate="$%{text}M", textposition="outside")
        fig_channel = plotly_layout(fig_channel, height=500)
        st.plotly_chart(fig_channel, use_container_width=True)

    with ch2:
        heat = (
            contact_clean.groupby(["scam_type", "contact_mode"])["amount_lost"]
            .sum().reset_index()
        )
        pivot = heat.pivot_table(
            index="scam_type", columns="contact_mode",
            values="amount_lost", aggfunc="sum", fill_value=0,
        )
        pivot_pct = pivot.div(pivot.sum(axis=1).replace(0, np.nan), axis=0) * 100
        pivot_pct = pivot_pct.loc[pivot.sum(axis=1).sort_values(ascending=False).head(12).index]

        fig_heat = px.imshow(
            pivot_pct, aspect="auto", color_continuous_scale="YlOrRd",
            title="Channel Share by Scam Type",
            labels=dict(x="Contact Channel", y="Scam Type", color="% Loss Share"),
            text_auto=".0f",
        )
        fig_heat = plotly_layout(fig_heat, height=500)
        st.plotly_chart(fig_heat, use_container_width=True)

    if len(channel_f) > 0:
        top_channel = channel_f.iloc[0]["contact_mode"]
        top_channel_amt = channel_f.iloc[0]["losses"]
        pull_quote(
            f"<b>{top_channel}</b> alone accounts for <b>{money_fmt(top_channel_amt)}</b> "
            f"in losses. The telcos and platforms running this channel have the technical "
            f"means to stop most of it — what's missing is regulatory will.",
        )

#tab 4
with tab4:
    st.markdown("### ⚠️ Scam Harm Index")
    st.caption("Advanced composite model: 50% total losses, 20% average loss, 20% report volume, 10% concentration. Higher score = stronger policy priority.")

    risk = (
        filtered.groupby("scam_type")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
    )
    risk["avg_loss"] = risk["losses"] / risk["reports"].replace(0, np.nan)
    risk["volume_rank"] = risk["reports"].rank(pct=True)
    risk["loss_rank"] = risk["losses"].rank(pct=True)
    risk["severity_rank"] = risk["avg_loss"].rank(pct=True)
    risk["concentration_rank"] = (risk["losses"] / risk["losses"].sum()).rank(pct=True)
    risk["risk_score"] = (
        risk["loss_rank"] * 0.50 + risk["severity_rank"] * 0.20 + risk["volume_rank"] * 0.20 + risk["concentration_rank"] * 0.10
    ) * 100
    risk = risk.sort_values("risk_score", ascending=False)
    risk["losses_m"] = risk["losses"] / 1e6

    r1, r2 = st.columns([1.1, 1])

    with r1:
        fig_risk = px.bar(
            risk.head(12).sort_values("risk_score"),
            x="risk_score", y="scam_type", orientation="h",
            title="Top Scam Types by Scam Harm Index",
            labels={"risk_score": "Harm Index / 100", "scam_type": "Scam Type"},
            text=risk.head(12).sort_values("risk_score")["risk_score"].round(0),
            color="risk_score", color_continuous_scale="Reds",
            hover_data={"reports": ":,.0f", "losses": ":,.0f",
                       "avg_loss": ":,.0f", "risk_score": ":.1f"},
        )
        fig_risk.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig_risk = plotly_layout(fig_risk, height=540)
        st.plotly_chart(fig_risk, use_container_width=True)

    with r2:
        display_risk = risk[["scam_type", "reports", "losses", "avg_loss", "risk_score"]].copy()
        display_risk["losses"] = display_risk["losses"].map(lambda x: f"${x:,.0f}")
        display_risk["avg_loss"] = display_risk["avg_loss"].map(lambda x: f"${x:,.0f}")
        display_risk["risk_score"] = display_risk["risk_score"].map(lambda x: f"{x:.1f}")
        st.dataframe(display_risk, use_container_width=True, hide_index=True, height=540)

    if len(risk) > 0:
        top_risk = risk.iloc[0]["scam_type"]
        pull_quote(
            f"<b>{top_risk}</b> ranks as the highest-priority scam type under the Harm Index. "
            f"This model strengthens the policy argument because it combines scale, severity, frequency, and loss concentration — "
            f"not one misleading metric alone.",
            "— Priority for regulators"
        )

#tab 5
with tab5:
    st.markdown("### ⚖️ Compare Two Segments")
    st.caption("Compare states, age groups, or scam types side-by-side.")

    compare_mode = st.radio(
        "Choose comparison type",
        ["State", "Age Group", "Scam Type"], horizontal=True,
    )

    if compare_mode == "State":
        options = AUS_STATES
        field = "state"
    elif compare_mode == "Age Group":
        options = DEFAULT_AGES
        field = "age_group"
    else:
        options = DEFAULT_TYPES
        field = "scam_type"

    cc1, cc2 = st.columns(2)
    with cc1:
        segment_a = st.selectbox("Segment A", options, index=0, key="segment_a")
    with cc2:
        default_b_index = 1 if len(options) > 1 else 0
        segment_b = st.selectbox("Segment B", options, index=default_b_index, key="segment_b")

    compare_df = filtered[filtered[field].isin([segment_a, segment_b])].copy()
    compare_summary = (
        compare_df.groupby(field)
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
    )
    compare_summary["avg_loss"] = compare_summary["losses"] / compare_summary["reports"].replace(0, np.nan)
    compare_summary["losses_m"] = compare_summary["losses"] / 1e6

    comp1, comp2, comp3 = st.columns(3)
    a_row = compare_summary[compare_summary[field] == segment_a]
    b_row = compare_summary[compare_summary[field] == segment_b]

    if len(a_row) and len(b_row):
        a_losses = a_row["losses"].iloc[0]
        b_losses = b_row["losses"].iloc[0]
        a_reports = a_row["reports"].iloc[0]
        b_reports = b_row["reports"].iloc[0]
        a_avg = a_row["avg_loss"].iloc[0]
        b_avg = b_row["avg_loss"].iloc[0]
        comp1.metric("Loss Difference", money_fmt(abs(a_losses - b_losses)))
        comp2.metric("Report Difference", number_fmt(abs(a_reports - b_reports)))
        comp3.metric("Avg Loss Difference", money_fmt(abs(a_avg - b_avg)))

    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        name="Reports", x=compare_summary[field], y=compare_summary["reports"],
        marker_color=P["orange"], yaxis="y",
    ))
    fig_compare.add_trace(go.Bar(
        name="Losses ($M)", x=compare_summary[field], y=compare_summary["losses_m"],
        marker_color=P["red"], yaxis="y2",
    ))
    fig_compare.update_layout(
        title=f"{compare_mode} Comparison: Reports vs Losses",
        yaxis=dict(title="Reports"),
        yaxis2=dict(title="Losses ($M)", overlaying="y", side="right", showgrid=False),
        barmode="group",
    )
    fig_compare = plotly_layout(fig_compare, height=480)
    st.plotly_chart(fig_compare, use_container_width=True)

    table_compare = compare_summary.copy()
    table_compare["losses"] = table_compare["losses"].map(lambda x: f"${x:,.0f}")
    table_compare["avg_loss"] = table_compare["avg_loss"].map(lambda x: f"${x:,.0f}")
    table_compare["losses_m"] = table_compare["losses_m"].map(lambda x: f"${x:.1f}M")
    st.dataframe(table_compare, use_container_width=True, hide_index=True)

st.markdown("---")

#act 3 
section_header(
    "🚨 Act 3: The Verdict & What-If Simulator",
    "Test a simple policy response and calculate the projected benefit-cost ratio.",
)

sim_left, sim_right = st.columns([1, 1.2])

with sim_left:
    st.markdown("### 🎚️ Intervention Parameters")
    st.caption("A simplified simulator for executive decision-making.")

    policy_scenario = st.selectbox(
        "Policy scenario",
        ["Conservative response", "Targeted response", "Aggressive response"],
        index=1,
    )
    target_focus = st.selectbox(
        "Primary target focus",
        ["High-loss scam types", "Older victims", "Online scams",
         "Phone and SMS scams", "Regional exposure"],
    )

    if policy_scenario == "Conservative response":
        default_reduction = 20
        default_budget = 25
    elif policy_scenario == "Targeted response":
        default_reduction = 35
        default_budget = 30
    else:
        default_reduction = 50
        default_budget = 40

    reduction_rate = st.slider("Estimated loss reduction (%)", 0, 60, default_reduction, 5)
    budget = st.slider("Program budget ($M)", 10, 150, default_budget, 10)

with sim_right:
    intervention_df = filtered.copy()
    intervention_df["policy_weight"] = 0.60

    if target_focus == "High-loss scam types":
        high_loss_types = (
            intervention_df.groupby("scam_type")["amount_lost"]
            .sum().sort_values(ascending=False).head(3).index
        )
        intervention_df.loc[intervention_df["scam_type"].isin(high_loss_types), "policy_weight"] = 1.00
    elif target_focus == "Older victims":
        intervention_df.loc[intervention_df["age_group"].isin(["55 - 64", "65 and over"]), "policy_weight"] = 1.00
    elif target_focus == "Online scams":
        intervention_df.loc[intervention_df["contact_mode"].str.contains("Online|Email", case=False, na=False), "policy_weight"] = 1.00
    elif target_focus == "Phone and SMS scams":
        intervention_df.loc[intervention_df["contact_mode"].str.contains("Phone|Text", case=False, na=False), "policy_weight"] = 1.00
    elif target_focus == "Regional exposure":
        intervention_df.loc[intervention_df["state"].isin(["WA", "NT", "TAS", "SA"]), "policy_weight"] = 1.00

    intervention_df["effective_reduction"] = reduction_rate / 100 * intervention_df["policy_weight"]
    intervention_df["prevented"] = intervention_df["amount_lost"] * intervention_df["effective_reduction"]
    intervention_df["residual"] = intervention_df["amount_lost"] - intervention_df["prevented"]

    total_l = intervention_df["amount_lost"].sum()
    prevented = intervention_df["prevented"].sum()
    budget_value = budget * 1e6
    bcr = safe_div(prevented, budget_value)
    net_benefit = prevented - budget_value
    prevented_pct = safe_div(prevented, total_l) * 100

    st.markdown("### 📊 Projected Outcomes")

    o1, o2 = st.columns(2)
    o1.metric("💸 Current Losses", money_fmt(total_l))
    o2.metric("✅ Losses Prevented", money_fmt(prevented), delta=f"-{prevented_pct:.1f}%")

    o3, o4 = st.columns(2)
    o3.metric("💰 Net Benefit", money_fmt(net_benefit))
    o4.metric("📈 Benefit-Cost Ratio", f"{bcr:.1f}×")

    if bcr >= 3:
        insight(f"🎯 <b>Strong case for investment</b> — every $1 invested is projected to prevent <b>${bcr:.1f}</b> in scam losses.", "success")
    elif bcr >= 1:
        insight(f"✅ <b>Positive return</b> — every $1 invested is projected to prevent <b>${bcr:.1f}</b> in scam losses.", "insight")
    else:
        insight("⚠️ <b>Weak return</b> — either reduce the budget, increase targeting, or test a stronger intervention scenario.", "warning")

    with st.expander("🧪 Model transparency: how the simulator works"):
        st.markdown(
            f"""
This is a simple policy simulator, not a causal model. It applies the selected reduction rate to the filtered scam losses,
with extra weight given to the selected target focus. For example, choosing **Older victims** gives full effect to 55–64 and 65+ records,
while all other records receive a lower background effect. The purpose is to test whether a targeted intervention can plausibly
return more prevented losses than it costs.

**Current assumption:** {policy_scenario} · {target_focus} · {reduction_rate}% maximum reduction · ${budget}M budget.
"""
        )

impact_age = (
    intervention_df[intervention_df["age_group"].isin(DEFAULT_AGES)]
    .groupby("age_group")
    .agg(prevented=("prevented", "sum"), residual=("residual", "sum"),
         original=("amount_lost", "sum"))
    .reset_index()
)
impact_age["age_group"] = pd.Categorical(impact_age["age_group"], categories=DEFAULT_AGES, ordered=True)
impact_age = impact_age.sort_values("age_group")
impact_age["prevented_m"] = impact_age["prevented"] / 1e6
impact_age["residual_m"] = impact_age["residual"] / 1e6

fig_impact = go.Figure()
fig_impact.add_trace(go.Bar(
    x=impact_age["age_group"], y=impact_age["residual_m"],
    name="Remaining losses", marker_color=P["red"],
))
fig_impact.add_trace(go.Bar(
    x=impact_age["age_group"], y=impact_age["prevented_m"],
    name="Prevented losses", marker_color=P["green"],
))
fig_impact.update_layout(
    title=f"Intervention Impact by Age Group — BCR {bcr:.1f}×",
    xaxis_title="Age Group", yaxis_title="$ Millions", barmode="stack",
)
fig_impact = plotly_layout(fig_impact, height=520)
st.plotly_chart(fig_impact, use_container_width=True)

#V2

st.markdown("<br>", unsafe_allow_html=True)
section_header(
    "🎯 The Ask: To the ACMA Commissioner",
    "You have the regulatory authority. The data shows where to act. Here is what intervention looks like as policy."
)

#compute action context dynamically
contact_clean_full = filtered[
    filtered["contact_mode"].notna()
    & (filtered["contact_mode"].str.lower() != "unspecified")
].copy()
if len(contact_clean_full) > 0:
    channel_top = contact_clean_full.groupby("contact_mode")["amount_lost"].sum().idxmax()
else:
    channel_top = "Phone"

preventable_per_day = prevented / (n_months * 30) if n_months > 0 else 0

ac1, ac2, ac3 = st.columns(3)
with ac1:
    st.markdown(f"""
    <div class="action-card">
        <div class="action-verb">Mandate</div>
        <div class="action-body">Carrier-level blocking of suspicious sender IDs and SMS short-codes</div>
        <div class="action-why">Targets {channel_top} — the largest single loss channel</div>
    </div>
    """, unsafe_allow_html=True)
with ac2:
    st.markdown(f"""
    <div class="action-card">
        <div class="action-verb">Fund</div>
        <div class="action-body">A National Anti-Scam Centre with ${budget}M annual budget</div>
        <div class="action-why">Projected to prevent {money_fmt(prevented)} — BCR {bcr:.1f}×</div>
    </div>
    """, unsafe_allow_html=True)
with ac3:
    st.markdown(f"""
    <div class="action-card">
        <div class="action-verb">Require</div>
        <div class="action-body">Real-time scam reporting from banks within 24 hours of detection</div>
        <div class="action-why">Closes the gap between victim, regulator, and prevention</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown(f"""
<div class="cta-box">
    <div class="cta-headline">Every day of inaction costs Australians {money_fmt(preventable_per_day)}.</div>
    <div class="cta-body">
        The data is clear. The interventions are known. The only variable left is political will.
        We invite the ACMA Commissioner to act before the next quarter's numbers come in.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

#data explorer

with st.expander("🔎 Open Detailed Data Explorer"):
    st.caption("Use this to inspect the currently filtered rows.")
    explorer_cols = ["month", "state", "age_group", "gender", "scam_type",
                     "contact_mode", "reports", "amount_lost"]
    available_cols = [c for c in explorer_cols if c in filtered.columns]
    sort_by = st.selectbox(
        "Sort table by", available_cols,
        index=available_cols.index("amount_lost") if "amount_lost" in available_cols else 0,
    )
    show_n = st.slider("Rows to show", 10, 500, 100, 10)
    data_view = filtered[available_cols].sort_values(sort_by, ascending=False).head(show_n)
    st.dataframe(data_view, use_container_width=True, hide_index=True)

#multi-dataset evidence layer

st.markdown("---")
section_header(
    "🧩 Multi-Dataset Evidence Layer",
    "A clear audit trail showing how the dashboard moves from raw reports to policy evidence."
)

evidence_layer = pd.DataFrame({
    "Dataset / Evidence": [
        "Scamwatch / ACCC",
        "ABS Population 2024",
        "Derived State Harm Index",
        "Derived Scam Harm Index",
        "What-if intervention simulator",
    ],
    "Role in dashboard": [
        "Reports, losses, scam type, contact mode, state, age group",
        "Population denominator for per-capita exposure",
        "Ranks states by combined loss, per-capita exposure, severity and volume",
        "Ranks scam types by loss concentration, severity, volume and total harm",
        "Tests whether targeted prevention creates a positive benefit-cost ratio",
    ],
    "Why it matters for ACMA / NASC": [
        "Shows the scale and channels of financial harm",
        "Prevents NSW/VIC population size from dominating policy decisions",
        "Identifies where resources should be geographically prioritised",
        "Identifies which scam types deserve urgent regulatory attention",
        "Turns analysis into a defensible funding ask",
    ],
})
st.dataframe(evidence_layer, use_container_width=True, hide_index=True)

#footer

st.markdown("""
<hr>
<small class="small-muted">
<b>Data Sources:</b> Scamwatch/ACCC · ABS Cat. 3235.0 · ACMA Enforcement Report · ACMA Communications Survey |
<b>Group 19:</b> Ishaan Gaware · Aryan Goel · Aishwarya · Nhi Nguyen · Neko/Yan Hao · Yuxiang Wang · Faisal |
MDSI Data Visualisation & Storytelling · UTS · 2026
</small>
""", unsafe_allow_html=True)
