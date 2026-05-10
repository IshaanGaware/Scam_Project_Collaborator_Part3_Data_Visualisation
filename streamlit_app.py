"""
Scammed in Australia — Interactive Streamlit Dashboard
Group 19 | MDSI Data Visualisation & Storytelling | UTS 2026

Run with:
    pip install streamlit pandas numpy matplotlib plotly openpyxl
    streamlit run streamlit_app.py
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

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Scammed in Australia",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────

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

.hero-card {
    padding: 2rem 2.2rem;
    border-radius: 26px;
    background: linear-gradient(135deg, rgba(192,57,43,0.35), rgba(26,58,92,0.45));
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 0 16px 45px rgba(0,0,0,0.35);
    margin-bottom: 1.5rem;
}

.hero-title {
    color: #ff554a;
    font-size: 3.4rem;
    font-weight: 850;
    margin-bottom: 0.25rem;
    line-height: 1.05;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 1.25rem;
    margin-top: 0.2rem;
    margin-bottom: 1rem;
}

.hero-pill {
    display: inline-block;
    padding: 0.45rem 0.8rem;
    margin: 0.15rem 0.2rem 0.15rem 0;
    border-radius: 999px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.16);
    color: #f8fafc;
    font-size: 0.92rem;
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
    color: #cbd5e1;
    font-style: italic;
    margin-bottom: 1rem;
}

.insight-box {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: rgba(241,196,15,0.15);
    border: 1px solid rgba(241,196,15,0.35);
    color: #fff8cc;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
}

.success-box {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: rgba(39,174,96,0.16);
    border: 1px solid rgba(39,174,96,0.35);
    color: #d1fae5;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
}

.warning-box {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: rgba(192,57,43,0.16);
    border: 1px solid rgba(192,57,43,0.35);
    color: #fee2e2;
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
    color: #cbd5e1;
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
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────

P = dict(
    red="#C0392B",
    orange="#E67E22",
    teal="#16A085",
    navy="#1A3A5C",
    gold="#F1C40F",
    grey="#7F8C8D",
    light="#ECF0F1",
    green="#27AE60",
    purple="#8E44AD",
    blue="#2980B9",
    dark="#0B0F17",
)

STATE_CLR = dict(
    NSW="#1A3A5C",
    VIC="#2980B9",
    QLD="#C0392B",
    WA="#E67E22",
    SA="#16A085",
    ACT="#8E44AD",
    TAS="#27AE60",
    NT="#F39C12",
)

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "#FAFAFA",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "font.family": "sans-serif",
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
    }
)

PLOTLY_TEMPLATE = "plotly_dark"

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    def money(v):
        if pd.isna(v):
            return 0.0
        return float(re.sub(r"[^\d.]", "", str(v)) or 0)

    STATE_ABB = {
        "New South Wales": "NSW",
        "Victoria": "VIC",
        "Queensland": "QLD",
        "Western Australia": "WA",
        "South Australia": "SA",
        "Tasmania": "TAS",
        "Australian Capital Territory": "ACT",
        "Northern Territory": "NT",
        "Outside of Australia": "INTL",
        "Unspecified": "UNK",
    }

    AGE_ORDER = [
        "Under 18",
        "18 - 24",
        "25 - 34",
        "35 - 44",
        "45 - 54",
        "55 - 64",
        "65 and over",
    ]

    data_dir = Path("data")

    scam = pd.read_csv(data_dir / "Scamwatch903 Public Scams Dashboard - Export.csv")

    scam = scam.rename(
        columns={
            "StartOfMonth": "month",
            "Address_State": "state_full",
            "Scam___Contact_Mode": "contact_mode",
            "Complainant_Age": "age_group",
            "Complainant_Gender": "gender",
            "Category_Level_3": "scam_type",
            "Amount_lost": "amount_lost_raw",
            "Number_of_reports": "reports",
        }
    )

    scam["month"] = pd.to_datetime(scam["month"])
    scam["amount_lost"] = scam["amount_lost_raw"].apply(money)
    scam["reports"] = pd.to_numeric(scam["reports"], errors="coerce").fillna(0)
    scam["state"] = scam["state_full"].map(STATE_ABB)

    AUS = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
    scam_aus = scam[scam["state"].isin(AUS)].copy()

    abs_raw = pd.read_excel(
        data_dir / "32350DS0003_2024.xlsx",
        sheet_name="Table 3",
        header=5,
    )

    abs_raw.columns = [
        "st",
        "sn",
        "lc",
        "ln",
        "p0",
        "p5",
        "p10",
        "p15",
        "p20",
        "p25",
        "p30",
        "p35",
        "p40",
        "p45",
        "p50",
        "p55",
        "p60",
        "p65",
        "p70",
        "p75",
        "p80",
        "p85",
        "total",
    ]

    abs_raw = abs_raw.iloc[1:].copy()

    for c in abs_raw.columns[4:]:
        abs_raw[c] = pd.to_numeric(abs_raw[c], errors="coerce")

    abs_raw = abs_raw[abs_raw["total"].notna()].copy()
    abs_raw["state"] = abs_raw["sn"].map(STATE_ABB)

    abs_raw["pop_young"] = abs_raw[["p15", "p20"]].sum(axis=1)
    abs_raw["pop_elderly"] = abs_raw[["p65", "p70", "p75", "p80", "p85"]].sum(axis=1)

    state_pop = (
        abs_raw.groupby("state")
        .agg(
            young_pop=("pop_young", "sum"),
            elderly_pop=("pop_elderly", "sum"),
            total_pop=("total", "sum"),
        )
        .reset_index()
    )

    state_pop = state_pop[state_pop["state"].isin(AUS)]

    by_type = (
        scam_aus.groupby("scam_type")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .sort_values("losses", ascending=False)
        .reset_index()
    )
    by_type["avg_loss"] = by_type["losses"] / by_type["reports"].replace(0, np.nan)
    by_type["loss_pct"] = by_type["losses"] / by_type["losses"].sum() * 100

    by_state = (
        scam_aus.groupby("state")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
        .merge(state_pop, on="state", how="left")
    )
    by_state["loss_per_100k"] = by_state["losses"] / by_state["total_pop"] * 100_000
    by_state["rpt_per_100k"] = by_state["reports"] / by_state["total_pop"] * 100_000

    by_age = (
        scam_aus[scam_aus["age_group"] != "Unspecified"]
        .groupby("age_group")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
    )
    by_age["age_group"] = pd.Categorical(
        by_age["age_group"], categories=AGE_ORDER, ordered=True
    )
    by_age = by_age.sort_values("age_group")
    by_age["avg_loss"] = by_age["losses"] / by_age["reports"].replace(0, np.nan)

    monthly = (
        scam_aus.groupby("month")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
    )

    return scam_aus, by_type, by_state, by_age, monthly, state_pop, AGE_ORDER, AUS


scam_aus, by_type, by_state, by_age, monthly, state_pop, AGE_ORDER, AUS_STATES = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

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


def plotly_layout(fig, height=460):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.55)",
        font=dict(color="#f8fafc"),
        margin=dict(l=20, r=20, t=70, b=40),
        title_font=dict(size=20, color="#f8fafc"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
        ),
    )
    return fig


def section_header(title, caption):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-caption'>{caption}</div>", unsafe_allow_html=True)


def insight(text, kind="insight"):
    css_class = {
        "insight": "insight-box",
        "success": "success-box",
        "warning": "warning-box",
    }.get(kind, "insight-box")

    st.markdown(f"<div class='{css_class}'>{text}</div>", unsafe_allow_html=True)


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


# ─────────────────────────────────────────────────────────────────────────────
# SESSION DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────

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

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Flag_of_Australia_%28converted%29.svg/320px-Flag_of_Australia_%28converted%29.svg.png",
        width=120,
    )

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
    st.markdown(
        """
- **Scamwatch** / ACCC
- **ABS Population** · 2024
- **ACMA Enforcement**
- **ACMA Communications Survey**
        """
    )

    st.markdown("---")
    st.caption("Group 19 · MDSI UTS · 2026")

filtered = get_filtered_data(selected_state, selected_ages, selected_types, month_range)

# ─────────────────────────────────────────────────────────────────────────────
# DYNAMIC NARRATIVE
# ─────────────────────────────────────────────────────────────────────────────

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

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────

total_reports = filtered["reports"].sum()
total_losses = filtered["amount_lost"].sum()
avg_loss = safe_div(total_losses, total_reports)
n_months = filtered["month"].nunique()

top_type = (
    filtered.groupby("scam_type")["amount_lost"].sum().idxmax()
    if len(filtered) > 0 and filtered["amount_lost"].sum() > 0
    else "N/A"
)

top_age = (
    filtered.groupby("age_group")["amount_lost"].sum().idxmax()
    if len(filtered) > 0 and filtered["amount_lost"].sum() > 0
    else "N/A"
)

st.markdown(
    f"""
<div class="hero-card">
    <div class="hero-title"> Scammed in Australia a cry for protection </div>
    <div class="hero-subtitle">
        An interactive data investigation into who is being targeted, where losses concentrate, and which scam channels create the most harm.
    </div>
    <span class="hero-pill">Stakeholder: ACMA Commissioner + National Anti Scam Centre of Australia </span>
    <span class="hero-pill">Narrative Arc: The Detective</span>
    <span class="hero-pill">Current Lens: {selected_state}</span>
    <span class="hero-pill">{len(selected_ages)} age groups</span>
    <span class="hero-pill">{len(selected_types)} scam types</span>
</div>
""",
    unsafe_allow_html=True,
)

if selected_state != "All States" and selected_state in STATE_NARRATIVE:
    st.info(f"📍 {STATE_NARRATIVE[selected_state]}")

if len(filtered) == 0:
    st.error("No data matches the current filters. Try resetting the filters in the sidebar.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# FILTER SUMMARY + DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────

summary_col, download_col = st.columns([3, 1])

with summary_col:
    st.info(
        f"""
**Current lens:**  
State: `{selected_state}` · Age groups: `{len(selected_ages)}` selected · Scam types: `{len(selected_types)}` selected · Months: `{n_months}`
        """
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

# ─────────────────────────────────────────────────────────────────────────────
# ACT 1
# ─────────────────────────────────────────────────────────────────────────────

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

# Monthly Loss Chart

mon_f = (
    filtered.groupby("month")
    .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
    .reset_index()
)
mon_f["month_label"] = mon_f["month"].dt.strftime("%b %Y")
mon_f["losses_m"] = mon_f["losses"] / 1e6
mon_f["avg_line"] = mon_f["losses_m"].mean()
mon_f["status"] = np.where(mon_f["losses_m"] > mon_f["avg_line"], "Above average", "Below average")

fig_month = px.bar(
    mon_f,
    x="month_label",
    y="losses_m",
    color="status",
    color_discrete_map={"Above average": P["red"], "Below average": P["teal"]},
    text=mon_f["losses_m"].round(1),
    title="Monthly Scam Losses",
    labels={"month_label": "Month", "losses_m": "$ Millions", "status": "Loss level"},
)

fig_month.update_traces(
    customdata=np.stack(
        [mon_f["status"], mon_f["losses"], mon_f["reports"]],
        axis=-1,
    ),
    texttemplate="$%{text}M",
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Loss level: %{customdata[0]}<br>"
        "Losses: $%{customdata[1]:,.0f}<br>"
        "Reports: %{customdata[2]:,.0f}"
        "<extra></extra>"
    ),
)

# Scam type distribution

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
        x="losses_m",
        y="scam_type",
        orientation="h",
        title="Top Scam Types by Total Losses",
        labels={"losses_m": "$ Millions", "scam_type": "Scam Type"},
        text=top_type_chart.sort_values("losses_m")["losses_m"].round(1),
        color="losses_m",
        color_continuous_scale="Reds",
        hover_data={"reports": ":,.0f", "losses": ":,.0f", "avg_loss": ":,.0f"},
    )
    fig_type.update_traces(texttemplate="$%{text}M", textposition="outside")
    fig_type = plotly_layout(fig_type, height=520)
    st.plotly_chart(fig_type, use_container_width=True)

with right:
    pie_data = type_f.head(6).copy()
    if len(type_f) > 6:
        other_row = pd.DataFrame(
            {
                "scam_type": ["Other scams"],
                "reports": [type_f.iloc[6:]["reports"].sum()],
                "losses": [type_f.iloc[6:]["losses"].sum()],
                "avg_loss": [
                    safe_div(type_f.iloc[6:]["losses"].sum(), type_f.iloc[6:]["reports"].sum())
                ],
                "loss_pct": [type_f.iloc[6:]["losses"].sum() / type_f["losses"].sum() * 100],
            }
        )
        pie_data = pd.concat([pie_data, other_row], ignore_index=True)

    fig_pie = px.pie(
        pie_data,
        names="scam_type",
        values="losses",
        hole=0.45,
        title="% of Losses by Scam Type",
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent")
    fig_pie = plotly_layout(fig_pie, height=520)
    st.plotly_chart(fig_pie, use_container_width=True)

insight(
    f"""
<b>Key Insight:</b> Under the current filters, <b>{top_type}</b> is the biggest loss driver.
The dashboard separates volume from severity so stakeholders do not only chase the highest number of reports.
""",
    "success",
)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# ACT 2
# ─────────────────────────────────────────────────────────────────────────────

section_header(
    "🕵️ Act 2: The Investigation",
    "Who is being targeted? Where? How? Explore the evidence through linked analytical views.",
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "👤 Victim Profile",
        "📍 Geographic Risk",
        "📡 Contact Channels",
        "⚠️ Risk Score",
        "⚖️ Compare Segments",
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — VICTIM PROFILE
# ─────────────────────────────────────────────────────────────────────────────

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
        fig_age = go.Figure()

        fig_age.add_trace(
            go.Bar(
                y=age_f["age_group"],
                x=age_f["reports"],
                name="Reports",
                orientation="h",
                marker_color=P["orange"],
                hovertemplate="<b>%{y}</b><br>Reports: %{x:,.0f}<extra></extra>",
            )
        )

        fig_age.add_trace(
            go.Bar(
                y=age_f["age_group"],
                x=age_f["avg_loss"],
                name="Avg loss per report",
                orientation="h",
                marker_color=P["navy"],
                xaxis="x2",
                hovertemplate="<b>%{y}</b><br>Avg loss: $%{x:,.0f}<extra></extra>",
            )
        )

        fig_age.update_layout(
            title="Reports vs Average Loss by Age",
            xaxis=dict(title="Reports"),
            xaxis2=dict(
                title="Average Loss",
                overlaying="x",
                side="top",
                showgrid=False,
            ),
            barmode="group",
        )
        fig_age = plotly_layout(fig_age, height=500)
        st.plotly_chart(fig_age, use_container_width=True)

    with a2:
        fig_bubble = px.scatter(
            age_f,
            x="reports",
            y="avg_loss",
            size="losses",
            color="age_group",
            text="age_group",
            title="Risk Matrix: Volume vs Severity",
            labels={
                "reports": "Number of Reports",
                "avg_loss": "Average Loss per Report",
                "losses": "Total Losses",
                "age_group": "Age Group",
            },
            hover_data={
                "reports": ":,.0f",
                "avg_loss": ":,.0f",
                "losses": ":,.0f",
                "age_group": False,
            },
        )
        fig_bubble.update_traces(textposition="middle center")
        fig_bubble = plotly_layout(fig_bubble, height=500)
        st.plotly_chart(fig_bubble, use_container_width=True)

    top_avg_age = age_f.sort_values("avg_loss", ascending=False).iloc[0]["age_group"]
    top_loss_age = age_f.sort_values("losses", ascending=False).iloc[0]["age_group"]

    insight(
        f"""
<b>Key Insight:</b> <b>{top_avg_age}</b> has the highest average loss per report, while
<b>{top_loss_age}</b> contributes the largest total loss under the current filters.
This distinction helps separate vulnerability from total financial impact.
""",
        "insight",
    )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — GEOGRAPHIC RISK
# ─────────────────────────────────────────────────────────────────────────────

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

    g1, g2 = st.columns([1, 1])

    with g1:
        fig_raw = px.bar(
            state_f.sort_values("losses_m", ascending=True),
            x="losses_m",
            y="state",
            orientation="h",
            color="state",
            color_discrete_map=STATE_CLR,
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
            x="loss_per_100k",
            y="state",
            orientation="h",
            color="state",
            color_discrete_map=STATE_CLR,
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

        insight(
            f"""
<b>Key Insight:</b> <b>{raw_leader}</b> leads in raw losses, but <b>{pc_leader}</b>
has the highest per-capita exposure. That means resource allocation should not be based only on raw totals.
""",
            "warning",
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — CONTACT CHANNELS
# ─────────────────────────────────────────────────────────────────────────────

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
            x="losses_m",
            y="contact_mode",
            orientation="h",
            title="Losses by Contact Channel",
            labels={"losses_m": "$ Millions", "contact_mode": "Contact Channel"},
            text=channel_f.sort_values("losses_m")["losses_m"].round(1),
            color="losses_m",
            color_continuous_scale="OrRd",
            hover_data={"reports": ":,.0f", "avg_loss": ":,.0f"},
        )
        fig_channel.update_traces(texttemplate="$%{text}M", textposition="outside")
        fig_channel = plotly_layout(fig_channel, height=500)
        st.plotly_chart(fig_channel, use_container_width=True)

    with ch2:
        heat = (
            contact_clean.groupby(["scam_type", "contact_mode"])["amount_lost"]
            .sum()
            .reset_index()
        )

        pivot = heat.pivot_table(
            index="scam_type",
            columns="contact_mode",
            values="amount_lost",
            aggfunc="sum",
            fill_value=0,
        )

        pivot_pct = pivot.div(pivot.sum(axis=1).replace(0, np.nan), axis=0) * 100
        pivot_pct = pivot_pct.loc[pivot.sum(axis=1).sort_values(ascending=False).head(12).index]

        fig_heat = px.imshow(
            pivot_pct,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            title="Channel Share by Scam Type",
            labels=dict(x="Contact Channel", y="Scam Type", color="% Loss Share"),
            text_auto=".0f",
        )
        fig_heat = plotly_layout(fig_heat, height=500)
        st.plotly_chart(fig_heat, use_container_width=True)

    if len(channel_f) > 0:
        top_channel = channel_f.iloc[0]["contact_mode"]
        insight(
            f"""
<b>Key Insight:</b> <b>{top_channel}</b> is the largest loss channel under the current filters.
This helps reveal whether the policy response should focus on telcos, online platforms, banks, or consumer education.
""",
            "insight",
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — RISK SCORE
# ─────────────────────────────────────────────────────────────────────────────

with tab4:
    st.markdown("### ⚠️ Scam Risk Score")
    st.caption(
        "A composite score combining report volume, total losses, and average loss. Higher score = stronger policy priority."
    )

    risk = (
        filtered.groupby("scam_type")
        .agg(reports=("reports", "sum"), losses=("amount_lost", "sum"))
        .reset_index()
    )
    risk["avg_loss"] = risk["losses"] / risk["reports"].replace(0, np.nan)

    risk["volume_rank"] = risk["reports"].rank(pct=True)
    risk["loss_rank"] = risk["losses"].rank(pct=True)
    risk["severity_rank"] = risk["avg_loss"].rank(pct=True)

    risk["risk_score"] = (
        risk["volume_rank"] * 0.30
        + risk["loss_rank"] * 0.50
        + risk["severity_rank"] * 0.20
    ) * 100

    risk = risk.sort_values("risk_score", ascending=False)
    risk["losses_m"] = risk["losses"] / 1e6

    r1, r2 = st.columns([1.1, 1])

    with r1:
        fig_risk = px.bar(
            risk.head(12).sort_values("risk_score"),
            x="risk_score",
            y="scam_type",
            orientation="h",
            title="Top Scam Types by Composite Risk Score",
            labels={"risk_score": "Risk Score / 100", "scam_type": "Scam Type"},
            text=risk.head(12).sort_values("risk_score")["risk_score"].round(0),
            color="risk_score",
            color_continuous_scale="Reds",
            hover_data={
                "reports": ":,.0f",
                "losses": ":,.0f",
                "avg_loss": ":,.0f",
                "risk_score": ":.1f",
            },
        )
        fig_risk.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig_risk = plotly_layout(fig_risk, height=540)
        st.plotly_chart(fig_risk, use_container_width=True)

    with r2:
        display_risk = risk[
            ["scam_type", "reports", "losses", "avg_loss", "risk_score"]
        ].copy()
        display_risk["losses"] = display_risk["losses"].map(lambda x: f"${x:,.0f}")
        display_risk["avg_loss"] = display_risk["avg_loss"].map(lambda x: f"${x:,.0f}")
        display_risk["risk_score"] = display_risk["risk_score"].map(lambda x: f"{x:.1f}")

        st.dataframe(
            display_risk,
            use_container_width=True,
            hide_index=True,
            height=540,
        )

    if len(risk) > 0:
        top_risk = risk.iloc[0]["scam_type"]
        insight(
            f"""
<b>Key Insight:</b> <b>{top_risk}</b> ranks as the highest composite-risk scam type.
This score is useful because it balances scale, severity, and frequency rather than relying on one metric.
""",
            "success",
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — COMPARE SEGMENTS
# ─────────────────────────────────────────────────────────────────────────────

with tab5:
    st.markdown("### ⚖️ Compare Two Segments")
    st.caption("Compare states, age groups, or scam types side-by-side.")

    compare_mode = st.radio(
        "Choose comparison type",
        ["State", "Age Group", "Scam Type"],
        horizontal=True,
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

    fig_compare.add_trace(
        go.Bar(
            name="Reports",
            x=compare_summary[field],
            y=compare_summary["reports"],
            marker_color=P["orange"],
            yaxis="y",
        )
    )

    fig_compare.add_trace(
        go.Bar(
            name="Losses ($M)",
            x=compare_summary[field],
            y=compare_summary["losses_m"],
            marker_color=P["red"],
            yaxis="y2",
        )
    )

    fig_compare.update_layout(
        title=f"{compare_mode} Comparison: Reports vs Losses",
        yaxis=dict(title="Reports"),
        yaxis2=dict(
            title="Losses ($M)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
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

# ─────────────────────────────────────────────────────────────────────────────
# ACT 3 — WHAT IF MODEL
# ─────────────────────────────────────────────────────────────────────────────

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
        [
            "Conservative response",
            "Targeted response",
            "Aggressive response",
        ],
    )

    target_focus = st.selectbox(
        "Primary target focus",
        [
            "High-loss scam types",
            "Older victims",
            "Online scams",
            "Phone and SMS scams",
            "Regional exposure",
        ],
    )

    if policy_scenario == "Conservative response":
        default_reduction = 15
        default_budget = 30
    elif policy_scenario == "Targeted response":
        default_reduction = 25
        default_budget = 40
    else:
        default_reduction = 35
        default_budget = 50

    reduction_rate = st.slider(
        "Estimated loss reduction (%)",
        0,
        60,
        default_reduction,
        5,
    )

    budget = st.slider(
        "Program budget ($M)",
        10,
        150,
        default_budget,
        10,
    )

with sim_right:
    intervention_df = filtered.copy()

    # Base reduction applies to all filtered losses
    intervention_df["policy_weight"] = 0.60

    # Extra weighting based on chosen target focus
    if target_focus == "High-loss scam types":
        high_loss_types = (
            intervention_df.groupby("scam_type")["amount_lost"]
            .sum()
            .sort_values(ascending=False)
            .head(3)
            .index
        )
        intervention_df.loc[
            intervention_df["scam_type"].isin(high_loss_types),
            "policy_weight",
        ] = 1.00

    elif target_focus == "Older victims":
        intervention_df.loc[
            intervention_df["age_group"].isin(["55 - 64", "65 and over"]),
            "policy_weight",
        ] = 1.00

    elif target_focus == "Online scams":
        intervention_df.loc[
            intervention_df["contact_mode"].str.contains("Online|Email", case=False, na=False),
            "policy_weight",
        ] = 1.00

    elif target_focus == "Phone and SMS scams":
        intervention_df.loc[
            intervention_df["contact_mode"].str.contains("Phone|Text", case=False, na=False),
            "policy_weight",
        ] = 1.00

    elif target_focus == "Regional exposure":
        intervention_df.loc[
            intervention_df["state"].isin(["WA", "NT", "TAS", "SA"]),
            "policy_weight",
        ] = 1.00

    intervention_df["effective_reduction"] = (
        reduction_rate / 100 * intervention_df["policy_weight"]
    )

    intervention_df["prevented"] = (
        intervention_df["amount_lost"] * intervention_df["effective_reduction"]
    )

    intervention_df["residual"] = (
        intervention_df["amount_lost"] - intervention_df["prevented"]
    )

    total_l = intervention_df["amount_lost"].sum()
    prevented = intervention_df["prevented"].sum()
    budget_value = budget * 1e6
    bcr = safe_div(prevented, budget_value)
    net_benefit = prevented - budget_value
    prevented_pct = safe_div(prevented, total_l) * 100

    st.markdown("### 📊 Projected Outcomes")

    o1, o2 = st.columns(2)
    o1.metric("💸 Current Losses", money_fmt(total_l))
    o2.metric(
        "✅ Losses Prevented",
        money_fmt(prevented),
        delta=f"-{prevented_pct:.1f}%",
    )

    o3, o4 = st.columns(2)
    o3.metric("💰 Net Benefit", money_fmt(net_benefit))
    o4.metric("📈 Benefit-Cost Ratio", f"{bcr:.1f}×")

    if bcr >= 3:
        insight(
            f"🎯 <b>Strong case for investment</b> — every $1 invested is projected to prevent <b>${bcr:.1f}</b> in scam losses.",
            "success",
        )
    elif bcr >= 1:
        insight(
            f"✅ <b>Positive return</b> — every $1 invested is projected to prevent <b>${bcr:.1f}</b> in scam losses.",
            "insight",
        )
    else:
        insight(
            "⚠️ <b>Weak return</b> — either reduce the budget, increase targeting, or test a stronger intervention scenario.",
            "warning",
        )

impact_age = (
    intervention_df[intervention_df["age_group"].isin(DEFAULT_AGES)]
    .groupby("age_group")
    .agg(
        prevented=("prevented", "sum"),
        residual=("residual", "sum"),
        original=("amount_lost", "sum"),
    )
    .reset_index()
)

impact_age["age_group"] = pd.Categorical(
    impact_age["age_group"],
    categories=DEFAULT_AGES,
    ordered=True,
)

impact_age = impact_age.sort_values("age_group")
impact_age["prevented_m"] = impact_age["prevented"] / 1e6
impact_age["residual_m"] = impact_age["residual"] / 1e6

fig_impact = go.Figure()

fig_impact.add_trace(
    go.Bar(
        x=impact_age["age_group"],
        y=impact_age["residual_m"],
        name="Remaining losses",
        marker_color=P["red"],
    )
)

fig_impact.add_trace(
    go.Bar(
        x=impact_age["age_group"],
        y=impact_age["prevented_m"],
        name="Prevented losses",
        marker_color=P["green"],
    )
)

fig_impact.update_layout(
    title=f"Intervention Impact by Age Group — BCR {bcr:.1f}×",
    xaxis_title="Age Group",
    yaxis_title="$ Millions",
    barmode="stack",
)

fig_impact = plotly_layout(fig_impact, height=520)
st.plotly_chart(fig_impact, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

section_header(
    "🧠 Auto-Generated Executive Summary",
    "This summary updates automatically when filters or simulator assumptions change.",
)

if len(type_f) > 0:
    top_type_loss = type_f.iloc[0]
    top_type_name = top_type_loss["scam_type"]
    top_type_loss_value = top_type_loss["losses"]
    top_type_share = top_type_loss["losses"] / type_f["losses"].sum() * 100
else:
    top_type_name = "N/A"
    top_type_loss_value = 0
    top_type_share = 0

if "age_f" in locals() and len(age_f) > 0:
    highest_severity_age = age_f.sort_values("avg_loss", ascending=False).iloc[0]["age_group"]
else:
    highest_severity_age = "N/A"

st.markdown(
    f"""
<div class="glass-card">
<h3 style="color:#f8fafc;">The Detective's Verdict</h3>

<p>
Under the current filters, the dashboard covers <b>{number_fmt(total_reports)}</b> scam reports and
<b>{money_fmt(total_losses)}</b> in reported losses across <b>{n_months}</b> months.
The largest loss category is <b>{top_type_name}</b>, accounting for approximately
<b>{top_type_share:.1f}%</b> of filtered losses.
</p>

<p>
The age group with the highest average loss per report is <b>{highest_severity_age}</b>.
This suggests that policy design should separate <b>high-volume groups</b> from
<b>high-severity groups</b>, because they may require different interventions.
</p>

<p>
The selected policy package, <b>{policy_scenario}</b>, is projected to prevent
<b>{money_fmt(prevented)}</b> in losses with a <b>{money_fmt(budget * 1e6)}</b> budget,
producing a benefit-cost ratio of <b>{bcr:.1f}×</b>.
</p>

<h4 style="color:#f8fafc;">Recommended Actions</h4>
<ol>
    <li><b>Prioritise the highest-risk scam types</b> using the composite risk score, not raw reports alone.</li>
    <li><b>Target older and high-severity victims</b> with prevention messages matched to their contact channels.</li>
    <li><b>Allocate extra support by per-capita exposure</b>, not only by raw state totals.</li>
    <li><b>Use the what-if simulator</b> to justify investment through a clear benefit-cost ratio.</li>
</ol>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# DETAILED DATA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────

with st.expander("🔎 Open Detailed Data Explorer"):
    st.caption("Use this to inspect the currently filtered rows.")

    explorer_cols = [
        "month",
        "state",
        "age_group",
        "gender",
        "scam_type",
        "contact_mode",
        "reports",
        "amount_lost",
    ]

    available_cols = [c for c in explorer_cols if c in filtered.columns]

    sort_by = st.selectbox(
        "Sort table by",
        available_cols,
        index=available_cols.index("amount_lost") if "amount_lost" in available_cols else 0,
    )

    show_n = st.slider("Rows to show", 10, 500, 100, 10)

    data_view = filtered[available_cols].sort_values(sort_by, ascending=False).head(show_n)

    st.dataframe(data_view, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
<hr>
<small class="small-muted">
<b>Data Sources:</b> Scamwatch/ACCC · ABS Cat. 3235.0 · ACMA Enforcement Report · ACMA Communications Survey |
<b>Group 19:</b> Ishaan Gaware · Aryan Goel · Aishwarya · Nhi Nguyen · Neko/Yan Hao · Yuxiang Wang · Faisal |
MDSI Data Visualisation & Storytelling · UTS · 2026
</small>
""",
    unsafe_allow_html=True,
)