import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Supply Chain & Logistics Analytics Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Dark background */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #21262d;
    }
    [data-testid="stSidebar"] * {
        color: #c9d1d9 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 20px 24px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 12px 12px 0 0;
    }
    .kpi-card.blue::before   { background: linear-gradient(90deg, #1f6feb, #388bfd); }
    .kpi-card.green::before  { background: linear-gradient(90deg, #238636, #3fb950); }
    .kpi-card.orange::before { background: linear-gradient(90deg, #d29922, #e3b341); }
    .kpi-card.purple::before { background: linear-gradient(90deg, #8957e5, #a371f7); }

    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8b949e;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        line-height: 1;
        color: #e6edf3;
        font-family: 'DM Mono', monospace;
    }
    .kpi-delta {
        font-size: 12px;
        margin-top: 8px;
        color: #3fb950;
    }
    .kpi-delta.neg     { color: #f85149; }
    .kpi-delta.warn    { color: #e3b341; }
    .kpi-delta.neutral { color: #8b949e; }

    /* Section headers */
    .section-header {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #8b949e;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #21262d;
    }

    /* Sub-header below title */
    .biz-overview {
        font-size: 13px;
        font-weight: 500;
        color: #484f58;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-top: 6px;
        margin-bottom: 2px;
    }

    /* Chart containers */
    .chart-container {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 4px;
    }

    /* Remove default streamlit spacing */
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    div[data-testid="column"] { padding: 0 6px; }
    .element-container { margin-bottom: 0 !important; }

    /* Plotly chart background */
    .js-plotly-plot .plotly { background: transparent !important; }

    /* Sidebar filters */
    .stSelectbox label, .stMultiSelect label, .stDateInput label {
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #8b949e !important;
    }
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #21262d !important;
        border-color: #30363d !important;
        color: #e6edf3 !important;
        border-radius: 8px !important;
    }

    /* Title area */
    .dash-title {
        font-size: 22px;
        font-weight: 700;
        color: #e6edf3;
        letter-spacing: -0.02em;
    }
    .dash-subtitle {
        font-size: 13px;
        color: #8b949e;
        margin-top: 2px;
    }
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #3fb950;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }

    /* ── Insights section ─────────────── */
    .insights-wrapper {
        background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 24px 28px;
        margin-top: 4px;
    }
    .insight-item {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 12px 0;
        border-bottom: 1px solid #21262d;
        line-height: 1.6;
    }
    .insight-item:last-child  { border-bottom: none; padding-bottom: 0; }
    .insight-item:first-child { padding-top: 0; }
    .insight-icon {
        font-size: 17px;
        min-width: 24px;
        margin-top: 1px;
    }
    .insight-text {
        font-size: 13.5px;
        color: #c9d1d9;
    }
    .insight-text strong {
        color: #e6edf3;
        font-weight: 600;
    }
    .tag {
        display: inline-block;
        border-radius: 4px;
        padding: 1px 8px;
        font-size: 11px;
        font-family: 'DM Mono', monospace;
        margin-left: 4px;
        vertical-align: middle;
        border: 1px solid;
    }
    .tag-red    { border-color: #f85149; color: #f85149; background: rgba(248,81,73,0.08); }
    .tag-green  { border-color: #3fb950; color: #3fb950; background: rgba(63,185,80,0.08); }
    .tag-blue   { border-color: #388bfd; color: #388bfd; background: rgba(56,139,253,0.08); }
    .tag-amber  { border-color: #e3b341; color: #e3b341; background: rgba(227,179,65,0.08); }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        letter-spacing: 0.04em !important;
        width: 100% !important;
        margin-top: 8px !important;
    }
    [data-testid="stDownloadButton"] button:hover { opacity: 0.85 !important; }

    /* Footer */
    .dash-footer {
        margin-top: 40px;
        padding: 16px 0;
        border-top: 1px solid #21262d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
    }
    .footer-left  { font-size: 11px; color: #484f58; }
    .footer-right { font-size: 11px; color: #484f58; text-align: right; }
    .footer-author {
        font-size: 11px;
        color: #6e7681;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SYNTHETIC DATA GENERATION
# ─────────────────────────────────────────────
@st.cache_data
def generate_data(n=2000):
    random.seed(42)
    np.random.seed(42)

    regions      = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa"]
    categories   = ["Electronics", "Apparel", "Pharmaceuticals", "Automotive", "FMCG", "Industrial"]
    ship_modes   = ["Air", "Sea", "Road"]
    statuses     = ["On-Time", "Delayed", "In Transit"]

    region_weights   = [0.30, 0.25, 0.25, 0.12, 0.08]
    category_weights = [0.22, 0.20, 0.15, 0.18, 0.15, 0.10]
    mode_weights     = [0.25, 0.40, 0.35]
    status_weights   = [0.62, 0.25, 0.13]

    start_date = datetime(2023, 1, 1)
    end_date   = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    order_dates    = [start_date + timedelta(days=int(np.random.triangular(0, date_range * 0.6, date_range))) for _ in range(n)]
    ship_mode_list = random.choices(ship_modes, weights=mode_weights, k=n)

    delivery_time_map = {"Air": (1, 5), "Sea": (15, 45), "Road": (3, 14)}
    delivery_times = [
        max(1, int(np.random.normal(
            np.mean(delivery_time_map[m]),
            (delivery_time_map[m][1] - delivery_time_map[m][0]) / 4
        )))
        for m in ship_mode_list
    ]

    delivery_dates = [od + timedelta(days=dt) for od, dt in zip(order_dates, delivery_times)]

    cost_map    = {"Air": (800, 3500), "Sea": (200, 900), "Road": (100, 600)}
    revenue_map = {"Air": (1200, 6000), "Sea": (350, 1500), "Road": (180, 1000)}

    costs    = [round(random.uniform(*cost_map[m]), 2)    for m in ship_mode_list]
    revenues = [round(random.uniform(*revenue_map[m]) + c * random.uniform(0.1, 0.6), 2)
                for m, c in zip(ship_mode_list, costs)]

    df = pd.DataFrame({
        "Order ID":        [f"ORD-{100000 + i}" for i in range(n)],
        "Order Date":      order_dates,
        "Delivery Date":   delivery_dates,
        "Region":          random.choices(regions,    weights=region_weights,   k=n),
        "Category":        random.choices(categories, weights=category_weights, k=n),
        "Shipment Mode":   ship_mode_list,
        "Delivery Status": random.choices(statuses,   weights=status_weights,   k=n),
        "Delivery Time":   delivery_times,
        "Cost":            costs,
        "Revenue":         revenues,
    })
    df["Order Date"]    = pd.to_datetime(df["Order Date"])
    df["Delivery Date"] = pd.to_datetime(df["Delivery Date"])
    df["Profit"]        = (df["Revenue"] - df["Cost"]).round(2)
    df["Profit Margin"] = ((df["Profit"] / df["Revenue"]) * 100).round(1)
    return df.sort_values("Order Date").reset_index(drop=True)

df_full = generate_data()

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
CHART_BG      = "#161b22"
PAPER_BG      = "#161b22"
GRID_COLOR    = "#21262d"
FONT_COLOR    = "#8b949e"
ACCENT_COLORS = ["#388bfd", "#3fb950", "#e3b341", "#f85149", "#a371f7", "#79c0ff"]

def base_layout(title="", height=320):
    return dict(
        title=dict(text=title, font=dict(size=13, color="#c9d1d9", family="DM Sans"), x=0.0, xanchor="left"),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="DM Sans", color=FONT_COLOR, size=11),
        height=height,
        margin=dict(l=16, r=16, t=40, b=16),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )

# ─────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 24px 0;'>
        <div style='font-size:18px;font-weight:700;color:#e6edf3;'>🚚 SCM Analytics</div>
        <div style='font-size:11px;color:#8b949e;margin-top:4px;'>Supply Chain Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Date Range**")
    min_date = df_full["Order Date"].min().date()
    max_date = df_full["Order Date"].max().date()
    date_from = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
    date_to   = st.date_input("To",   value=max_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    regions_all = sorted(df_full["Region"].unique())
    region_sel  = st.multiselect("Region", regions_all, default=regions_all)

    st.markdown("<br>", unsafe_allow_html=True)
    modes_all = sorted(df_full["Shipment Mode"].unique())
    mode_sel  = st.multiselect("Shipment Mode", modes_all, default=modes_all)

    st.markdown("<br>", unsafe_allow_html=True)
    cats_all = sorted(df_full["Category"].unique())
    cat_sel  = st.multiselect("Category", cats_all, default=cats_all)

    st.markdown("---")
    st.markdown(f"<div style='font-size:11px;color:#484f58;'>Dataset: {len(df_full):,} orders</div>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
df = df_full[
    (df_full["Order Date"].dt.date >= date_from) &
    (df_full["Order Date"].dt.date <= date_to) &
    (df_full["Region"].isin(region_sel if region_sel else regions_all)) &
    (df_full["Shipment Mode"].isin(mode_sel if mode_sel else modes_all)) &
    (df_full["Category"].isin(cat_sel if cat_sel else cats_all))
].copy()

# ── CSV Download Button ────────────────────────
with st.sidebar:
    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:11px;font-weight:600;text-transform:uppercase;"
        "letter-spacing:0.06em;color:#8b949e;margin-bottom:2px;'>Export Filtered Data</div>",
        unsafe_allow_html=True,
    )
    export_df = df.copy()
    export_df["Order Date"]    = export_df["Order Date"].dt.strftime("%Y-%m-%d")
    export_df["Delivery Date"] = export_df["Delivery Date"].dt.strftime("%Y-%m-%d")
    csv_buffer = io.StringIO()
    export_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇  Download CSV",
        data=csv_buffer.getvalue(),
        file_name=f"scm_filtered_{date_from}_{date_to}.csv",
        mime="text/csv",
        help=f"Download {len(df):,} filtered orders as CSV",
    )

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown(f"""
    <div class='dash-title'>Supply Chain &amp; Logistics Analytics Dashboard</div>
    <div class='biz-overview'>Business Performance Overview</div>
    <div class='dash-subtitle'>
        <span class='status-dot'></span>
        Live Analytics &nbsp;·&nbsp; {date_from.strftime("%b %d, %Y")} — {date_to.strftime("%b %d, %Y")}
    </div>
    """, unsafe_allow_html=True)
with col_badge:
    st.markdown(f"""
    <div style='text-align:right;padding-top:4px;'>
        <span style='background:#21262d;border:1px solid #30363d;border-radius:20px;
                     padding:4px 12px;font-size:11px;color:#8b949e;font-weight:600;'>
            {len(df):,} Orders
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CALCULATIONS (period-over-period)
# ─────────────────────────────────────────────
total_orders  = len(df)
ontime_pct    = (df["Delivery Status"] == "On-Time").mean() * 100 if total_orders else 0
delayed_pct   = (df["Delivery Status"] == "Delayed").mean() * 100 if total_orders else 0
avg_del_time  = df["Delivery Time"].mean() if total_orders else 0
total_revenue = df["Revenue"].sum()
total_profit  = df["Profit"].sum()
avg_margin    = df["Profit Margin"].mean() if total_orders else 0

# Split filtered window into first-half / second-half for comparison
if total_orders >= 4:
    midpoint = df["Order Date"].min() + (df["Order Date"].max() - df["Order Date"].min()) / 2
    df_h1 = df[df["Order Date"] <= midpoint]
    df_h2 = df[df["Order Date"] >  midpoint]

    def safe_pct(new, old):
        return ((new - old) / old * 100) if old != 0 else 0

    orders_chg = safe_pct(len(df_h2), len(df_h1))
    ontime_chg = (
        (df_h2["Delivery Status"] == "On-Time").mean() * 100 -
        (df_h1["Delivery Status"] == "On-Time").mean() * 100
    ) if len(df_h1) > 0 else 0
    dtime_chg  = df_h2["Delivery Time"].mean() - df_h1["Delivery Time"].mean() if len(df_h1) > 0 else 0
    rev_chg    = safe_pct(df_h2["Revenue"].sum(), df_h1["Revenue"].sum())
else:
    orders_chg = ontime_chg = dtime_chg = rev_chg = 0.0

def kpi_delta_html(val, unit, higher_is_better=True, suffix="vs prior half"):
    if abs(val) < 0.05:
        sym, cls = "→", "neutral"
    else:
        sym = "▲" if val > 0 else "▼"
        good = (val > 0) == higher_is_better
        cls = "green" if good else "neg"
    sign = "+" if val >= 0 else ""
    return f"{sym} {sign}{val:.1f}{unit} {suffix}", cls

od_txt, od_cls = kpi_delta_html(orders_chg, "%",   higher_is_better=True)
ot_txt, ot_cls = kpi_delta_html(ontime_chg, " pp", higher_is_better=True)
dt_txt, dt_cls = kpi_delta_html(dtime_chg,  "d",   higher_is_better=False)
rv_txt, rv_cls = kpi_delta_html(rev_chg,    "%",   higher_is_better=True)

rv_sub = f"Profit margin: {avg_margin:.1f}%"

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

kpi_rows = [
    (k1, "blue",   "Total Orders",      f"{total_orders:,}",          od_txt, od_cls),
    (k2, "green",  "On-Time Delivery",  f"{ontime_pct:.1f}%",         ot_txt, ot_cls),
    (k3, "orange", "Avg Delivery Time", f"{avg_del_time:.1f}d",       dt_txt, dt_cls),
    (k4, "purple", "Total Revenue",     f"${total_revenue/1e6:.2f}M", rv_txt + f" · {rv_sub}", rv_cls),
]
for col, color, label, value, delta, delta_cls in kpi_rows:
    with col:
        st.markdown(f"""
        <div class='kpi-card {color}'>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-delta {delta_cls}'>{delta}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 1: Orders over time + Orders by Region
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'>Order Trends &amp; Geographic Distribution</div>", unsafe_allow_html=True)

c1, c2 = st.columns([3, 2])

with c1:
    monthly = (df.set_index("Order Date")
                 .resample("ME")
                 .agg(Orders=("Order ID","count"), Revenue=("Revenue","sum"))
                 .reset_index())
    monthly["Month"] = monthly["Order Date"].dt.strftime("%b %Y")

    fig_line = make_subplots(specs=[[{"secondary_y": True}]])
    fig_line.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Orders"],
        name="Orders", mode="lines+markers",
        line=dict(color="#388bfd", width=2.5),
        marker=dict(size=5, color="#388bfd"),
        fill="tozeroy", fillcolor="rgba(56,139,253,0.08)"
    ), secondary_y=False)
    fig_line.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Revenue"],
        name="Revenue ($)", mode="lines",
        line=dict(color="#3fb950", width=1.8, dash="dot"),
    ), secondary_y=True)

    layout = base_layout("Orders & Revenue Over Time", 330)
    layout["xaxis"]["tickangle"] = -30
    layout["xaxis"]["nticks"] = 10
    layout["yaxis"]["title"] = dict(text="Orders", font=dict(size=10))
    layout["yaxis2"] = dict(title=dict(text="Revenue ($)", font=dict(size=10)),
                            gridcolor=GRID_COLOR, tickfont=dict(size=10),
                            showgrid=False, tickfont_color=FONT_COLOR)
    fig_line.update_layout(**layout)
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

with c2:
    reg_grp = df.groupby("Region").agg(
        Orders=("Order ID","count"),
        Revenue=("Revenue","sum")
    ).sort_values("Orders", ascending=True).reset_index()

    fig_bar = go.Figure(go.Bar(
        y=reg_grp["Region"], x=reg_grp["Orders"],
        orientation="h",
        marker=dict(
            color=reg_grp["Orders"],
            colorscale=[[0,"#1c2128"],[1,"#388bfd"]],
            showscale=False,
            line=dict(width=0)
        ),
        text=reg_grp["Orders"],
        textposition="inside",
        textfont=dict(color="#e6edf3", size=11, family="DM Mono"),
        hovertemplate="<b>%{y}</b><br>Orders: %{x:,}<extra></extra>",
    ))
    layout2 = base_layout("Orders by Region", 330)
    layout2.pop("xaxis", None)
    layout2.pop("yaxis", None)
    fig_bar.update_layout(**layout2,
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10), autorange=True),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# ROW 2: Delivery Status + Delivery Time by Mode + Category Revenue
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'>Delivery Performance &amp; Shipment Analysis</div>", unsafe_allow_html=True)

c3, c4, c5 = st.columns(3)

with c3:
    status_cnt = df["Delivery Status"].value_counts().reset_index()
    status_cnt.columns = ["Status", "Count"]
    color_map = {"On-Time": "#3fb950", "Delayed": "#f85149", "In Transit": "#e3b341"}

    fig_pie = go.Figure(go.Pie(
        labels=status_cnt["Status"],
        values=status_cnt["Count"],
        hole=0.55,
        marker=dict(colors=[color_map.get(s, "#388bfd") for s in status_cnt["Status"]],
                    line=dict(color="#161b22", width=2)),
        textinfo="percent",
        textfont=dict(size=11, color="#e6edf3"),
        hovertemplate="<b>%{label}</b><br>%{value:,} orders (%{percent})<extra></extra>",
    ))
    fig_pie.add_annotation(
        text=f"<b>{total_orders:,}</b><br><span style='font-size:9px'>Total</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="#e6edf3", family="DM Mono"),
        align="center"
    )

    # ── FIX: exclude 'legend' from base_layout before unpacking ──
    pie_layout = {k: v for k, v in base_layout("Delivery Status Distribution", 310).items()
                  if k not in ["xaxis", "yaxis", "legend"]}
    pie_layout["showlegend"] = True
    pie_layout["legend"] = dict(
        orientation="h", yanchor="bottom", y=-0.15,
        xanchor="center", x=0.5,
        font=dict(size=10), bgcolor="rgba(0,0,0,0)"
    )
    fig_pie.update_layout(**pie_layout)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

with c4:
    mode_grp = df.groupby("Shipment Mode")["Delivery Time"].mean().reset_index()
    mode_grp.columns = ["Mode", "Avg Days"]
    mode_grp = mode_grp.sort_values("Avg Days", ascending=False)
    mode_colors = {"Air": "#388bfd", "Sea": "#a371f7", "Road": "#3fb950"}

    fig_mode = go.Figure(go.Bar(
        x=mode_grp["Mode"],
        y=mode_grp["Avg Days"],
        marker=dict(color=[mode_colors.get(m, "#388bfd") for m in mode_grp["Mode"]],
                    line=dict(width=0)),
        text=[f"{v:.1f}d" for v in mode_grp["Avg Days"]],
        textposition="outside",
        textfont=dict(color="#e6edf3", size=12, family="DM Mono"),
        width=0.45,
        hovertemplate="<b>%{x}</b><br>Avg: %{y:.1f} days<extra></extra>",
    ))
    l4 = base_layout("Avg Delivery Time by Shipment Mode", 310)
    l4["yaxis"]["title"] = dict(text="Days", font=dict(size=10))
    l4["yaxis"]["range"] = [0, mode_grp["Avg Days"].max() * 1.25]
    fig_mode.update_layout(**l4)
    st.plotly_chart(fig_mode, use_container_width=True, config={"displayModeBar": False})

with c5:
    cat_grp = df.groupby("Category")["Revenue"].sum().sort_values(ascending=True).reset_index()

    fig_cat = go.Figure(go.Bar(
        y=cat_grp["Category"], x=cat_grp["Revenue"],
        orientation="h",
        marker=dict(
            color=cat_grp["Revenue"],
            colorscale=[[0,"#1c2128"],[0.5,"#8957e5"],[1,"#a371f7"]],
            showscale=False,
            line=dict(width=0)
        ),
        text=[f"${v/1e3:.0f}K" for v in cat_grp["Revenue"]],
        textposition="inside",
        textfont=dict(color="#e6edf3", size=10, family="DM Mono"),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))
    l5 = base_layout("Revenue by Category", 310)
    l5.pop("xaxis", None); l5.pop("yaxis", None)
    fig_cat.update_layout(**l5,
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10),
                   tickprefix="$", tickformat=".0s"),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10)),
    )
    st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# ROW 3: Cost vs Revenue scatter + Monthly Profit Trend
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'>Cost vs Revenue Analysis &amp; Profitability</div>", unsafe_allow_html=True)

c6, c7 = st.columns([2, 3])

with c6:
    sample = df.sample(min(500, len(df)), random_state=42) if len(df) > 500 else df
    fig_scatter = go.Figure()
    for mode, color in mode_colors.items():
        sub = sample[sample["Shipment Mode"] == mode]
        if not sub.empty:
            fig_scatter.add_trace(go.Scatter(
                x=sub["Cost"], y=sub["Revenue"],
                mode="markers", name=mode,
                marker=dict(color=color, size=5, opacity=0.65,
                            line=dict(width=0)),
                hovertemplate=f"<b>{mode}</b><br>Cost: $%{{x:,.0f}}<br>Revenue: $%{{y:,.0f}}<extra></extra>",
            ))
    mx = max(sample["Cost"].max(), sample["Revenue"].max())
    fig_scatter.add_trace(go.Scatter(
        x=[0, mx], y=[0, mx], mode="lines",
        line=dict(color="#484f58", width=1, dash="dash"),
        name="Break-even", showlegend=True,
    ))
    l6 = base_layout("Cost vs Revenue by Shipment Mode", 340)
    l6["xaxis"]["title"] = dict(text="Cost ($)", font=dict(size=10))
    l6["yaxis"]["title"] = dict(text="Revenue ($)", font=dict(size=10))
    l6["xaxis"]["tickprefix"] = "$"
    l6["yaxis"]["tickprefix"] = "$"
    fig_scatter.update_layout(**l6)
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

with c7:
    monthly2 = (df.set_index("Order Date")
                  .resample("ME")
                  .agg(Revenue=("Revenue","sum"),
                       Cost=("Cost","sum"),
                       Profit=("Profit","sum"))
                  .reset_index())
    monthly2["Month"] = monthly2["Order Date"].dt.strftime("%b %Y")

    fig_profit = go.Figure()
    fig_profit.add_trace(go.Bar(
        x=monthly2["Month"], y=monthly2["Revenue"],
        name="Revenue", marker_color="#388bfd",
        marker_line_width=0, opacity=0.85,
    ))
    fig_profit.add_trace(go.Bar(
        x=monthly2["Month"], y=monthly2["Cost"],
        name="Cost", marker_color="#f85149",
        marker_line_width=0, opacity=0.75,
    ))
    fig_profit.add_trace(go.Scatter(
        x=monthly2["Month"], y=monthly2["Profit"],
        name="Profit", mode="lines+markers",
        line=dict(color="#3fb950", width=2.5),
        marker=dict(size=5),
        yaxis="y2",
    ))
    l7 = base_layout("Monthly Revenue, Cost & Profit", 340)
    l7["barmode"] = "group"
    l7["xaxis"]["tickangle"] = -30
    l7["xaxis"]["nticks"] = 10
    l7["yaxis"]["title"] = dict(text="Amount ($)", font=dict(size=10))
    l7["yaxis"]["tickprefix"] = "$"
    l7["yaxis2"] = dict(
        title=dict(text="Profit ($)", font=dict(size=10, color="#3fb950")),
        overlaying="y", side="right",
        showgrid=False, tickfont=dict(size=10, color="#3fb950"),
        tickprefix="$",
    )
    fig_profit.update_layout(**l7)
    st.plotly_chart(fig_profit, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# ROW 4: Heatmap + Delay Rate by Region
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'>Delay Analysis &amp; Mode-Region Matrix</div>", unsafe_allow_html=True)

c8, c9 = st.columns([3, 2])

with c8:
    heat_data = df.pivot_table(
        index="Region", columns="Shipment Mode",
        values="Delivery Time", aggfunc="mean"
    ).round(1)

    fig_heat = go.Figure(go.Heatmap(
        z=heat_data.values,
        x=heat_data.columns.tolist(),
        y=heat_data.index.tolist(),
        colorscale=[[0,"#0d1117"],[0.3,"#1f6feb"],[0.7,"#388bfd"],[1,"#a371f7"]],
        text=heat_data.values.round(1),
        texttemplate="%{text}d",
        textfont=dict(size=11, family="DM Mono", color="#e6edf3"),
        showscale=True,
        colorbar=dict(
            tickfont=dict(size=9, color="#8b949e"),
            bgcolor="#161b22",
            bordercolor="#21262d",
            thickness=10,
        ),
        hovertemplate="<b>%{y} · %{x}</b><br>Avg: %{z:.1f} days<extra></extra>",
    ))
    l8 = base_layout("Avg Delivery Time (Days) — Region × Shipment Mode", 310)
    l8.pop("xaxis", None); l8.pop("yaxis", None)
    fig_heat.update_layout(**l8,
        xaxis=dict(tickfont=dict(size=11), side="bottom"),
        yaxis=dict(tickfont=dict(size=10), autorange="reversed"),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

with c9:
    delay_rate = (df.groupby("Region")
                    .apply(lambda x: (x["Delivery Status"] == "Delayed").mean() * 100)
                    .reset_index(name="Delay Rate (%)"))
    delay_rate = delay_rate.sort_values("Delay Rate (%)", ascending=True)

    fig_delay = go.Figure(go.Bar(
        y=delay_rate["Region"],
        x=delay_rate["Delay Rate (%)"],
        orientation="h",
        marker=dict(
            color=delay_rate["Delay Rate (%)"],
            colorscale=[[0,"#238636"],[0.5,"#e3b341"],[1,"#f85149"]],
            showscale=False,
            line=dict(width=0),
        ),
        text=[f"{v:.1f}%" for v in delay_rate["Delay Rate (%)"]],
        textposition="inside",
        textfont=dict(color="#e6edf3", size=11, family="DM Mono"),
        hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<extra></extra>",
    ))
    l9 = base_layout("Delay Rate by Region (%)", 310)
    l9.pop("xaxis", None); l9.pop("yaxis", None)
    fig_delay.update_layout(**l9,
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10), ticksuffix="%"),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10)),
    )
    st.plotly_chart(fig_delay, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# RECENT ORDERS TABLE
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'>Recent Orders</div>", unsafe_allow_html=True)

recent = (df.sort_values("Order Date", ascending=False)
            .head(8)[["Order ID","Order Date","Region","Category",
                       "Shipment Mode","Delivery Status","Delivery Time","Revenue","Profit Margin"]]
            .copy())
recent["Order Date"]    = recent["Order Date"].dt.strftime("%b %d, %Y")
recent["Revenue"]       = recent["Revenue"].apply(lambda x: f"${x:,.0f}")
recent["Profit Margin"] = recent["Profit Margin"].apply(lambda x: f"{x:.1f}%")
recent["Delivery Time"] = recent["Delivery Time"].apply(lambda x: f"{x}d")

st.dataframe(
    recent,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Order ID":        st.column_config.TextColumn("Order ID",  width=110),
        "Order Date":      st.column_config.TextColumn("Date",      width=100),
        "Region":          st.column_config.TextColumn("Region",    width=150),
        "Category":        st.column_config.TextColumn("Category",  width=120),
        "Shipment Mode":   st.column_config.TextColumn("Mode",      width=80),
        "Delivery Status": st.column_config.TextColumn("Status",    width=100),
        "Delivery Time":   st.column_config.TextColumn("Del. Time", width=80),
        "Revenue":         st.column_config.TextColumn("Revenue",   width=90),
        "Profit Margin":   st.column_config.TextColumn("Margin",    width=75),
    }
)

# ─────────────────────────────────────────────
# KEY BUSINESS INSIGHTS  (data-driven)
# ─────────────────────────────────────────────
st.markdown("<div class='section-header'>Key Business Insights</div>", unsafe_allow_html=True)

# ── Compute insight values from filtered df ──

# 1. Delay concentration
worst_delay = delay_rate.sort_values("Delay Rate (%)", ascending=False).iloc[0]
best_delay  = delay_rate.sort_values("Delay Rate (%)", ascending=True).iloc[0]
delay_ratio = worst_delay["Delay Rate (%)"] / best_delay["Delay Rate (%)"] if best_delay["Delay Rate (%)"] > 0 else 0
overall_del_tag = ("tag-red", "High Risk") if delayed_pct > 30 else (("tag-amber", "Moderate") if delayed_pct > 20 else ("tag-green", "On Target"))

# 2. Shipment mode ROI (revenue per cost unit)
mode_roi = (
    df.groupby("Shipment Mode")
      .apply(lambda x: x["Revenue"].sum() / x["Cost"].sum() if x["Cost"].sum() > 0 else 0)
      .reset_index()
)
mode_roi.columns = ["Mode", "ROI"]
best_mode_row    = mode_roi.sort_values("ROI", ascending=False).iloc[0]
weakest_mode_row = mode_roi.sort_values("ROI", ascending=True).iloc[0]

# 3. Mode speed comparison
air_avg  = df[df["Shipment Mode"] == "Air"]["Delivery Time"].mean()  if "Air"  in df["Shipment Mode"].values else 1
sea_avg  = df[df["Shipment Mode"] == "Sea"]["Delivery Time"].mean()  if "Sea"  in df["Shipment Mode"].values else 0
road_avg = df[df["Shipment Mode"] == "Road"]["Delivery Time"].mean() if "Road" in df["Shipment Mode"].values else 0

# 4. Top revenue region + category
top_region = reg_grp.sort_values("Orders", ascending=False).iloc[0]
top2_share = reg_grp.sort_values("Orders", ascending=False).head(2)["Orders"].sum() / total_orders * 100 if total_orders else 0
top_cat_row = cat_grp.sort_values("Revenue", ascending=False).iloc[-1]

# 5. Revenue trend (last vs prior 3 months)
if len(monthly2) >= 6:
    last3  = monthly2["Revenue"].iloc[-3:].sum()
    prior3 = monthly2["Revenue"].iloc[-6:-3].sum()
    rev_trend_chg = ((last3 - prior3) / prior3 * 100) if prior3 > 0 else 0
    rev_trend_word = "grown" if rev_trend_chg >= 0 else "declined"
    rev_trend_tag  = ("tag-green", f"+{rev_trend_chg:.1f}%") if rev_trend_chg >= 0 else ("tag-red", f"{rev_trend_chg:.1f}%")
else:
    rev_trend_chg, rev_trend_word = 0.0, "remained stable"
    rev_trend_tag = ("tag-amber", "Stable")

# 6. Margin context
road_avg_cost = df[df["Shipment Mode"] == "Road"]["Cost"].mean() if "Road" in df["Shipment Mode"].values else 0
air_avg_cost  = df[df["Shipment Mode"] == "Air"]["Cost"].mean()  if "Air"  in df["Shipment Mode"].values else 0

insights_html = f"""
<div class='insights-wrapper'>

  <div class='insight-item'>
    <div class='insight-icon'>🚨</div>
    <div class='insight-text'>
      <strong>Delivery Delays — Regional Pressure Point:</strong>
      <strong>{worst_delay['Region']}</strong> has the highest delay rate at
      <strong>{worst_delay['Delay Rate (%)']:.1f}%</strong> —
      {delay_ratio:.1f}× higher than the best-performing region
      (<strong>{best_delay['Region']}</strong> at {best_delay['Delay Rate (%)']:.1f}%).
      With an overall delay rate of <strong>{delayed_pct:.1f}%</strong>
      <span class='tag {overall_del_tag[0]}'>{overall_del_tag[1]}</span>,
      renegotiating carrier SLAs and positioning buffer stock in high-delay regions
      is the most immediate action available to improve fulfilment reliability.
    </div>
  </div>

  <div class='insight-item'>
    <div class='insight-icon'>✈️</div>
    <div class='insight-text'>
      <strong>Shipment Mode Efficiency — Air Delivers the Best Return on Spend:</strong>
      Air freight yields the highest revenue-to-cost ratio at
      <strong>{best_mode_row['ROI']:.2f}×</strong>, ahead of
      {weakest_mode_row['Mode']} ({weakest_mode_row['ROI']:.2f}×).
      Sea shipments average <strong>{sea_avg:.1f} days</strong> versus Air's
      <strong>{air_avg:.1f} days</strong> — a {sea_avg/air_avg:.0f}× speed difference —
      making Sea the right choice only for bulk, non-urgent cargo.
      A dynamic mode-selection policy based on order value and delivery deadline
      could reduce blended logistics cost without sacrificing speed.
    </div>
  </div>

  <div class='insight-item'>
    <div class='insight-icon'>🌍</div>
    <div class='insight-text'>
      <strong>Geographic Concentration — Top Regions Create Dependency Risk:</strong>
      <strong>{top_region['Region']}</strong> accounts for the largest share of orders,
      and the top two regions together represent
      <strong>{top2_share:.0f}%</strong> of all filtered orders.
      While this reflects strong market presence, a single network disruption in either hub
      would significantly impact fulfilment KPIs.
      Diversifying carrier partnerships and building safety stock in secondary markets
      would meaningfully reduce this exposure.
    </div>
  </div>

  <div class='insight-item'>
    <div class='insight-icon'>📈</div>
    <div class='insight-text'>
      <strong>Revenue Trend — Momentum Signal for Top Category:</strong>
      Revenue has <strong>{rev_trend_word}</strong> in the most recent 3-month window
      <span class='tag {rev_trend_tag[0]}'>{rev_trend_tag[1]}</span>
      compared to the prior period.
      <strong>{top_cat_row['Category']}</strong> is the leading revenue category
      at <strong>${top_cat_row['Revenue']/1e3:.0f}K</strong>. Protecting service levels
      for this segment through dedicated capacity agreements should be a strategic priority.
    </div>
  </div>

  <div class='insight-item'>
    <div class='insight-icon'>💡</div>
    <div class='insight-text'>
      <strong>Profitability — Mode Mix Optimisation Opportunity:</strong>
      At an average margin of <strong>{avg_margin:.1f}%</strong> and total profit of
      <strong>${total_profit/1e6:.2f}M</strong>, the cost gap between Air
      (avg ${air_avg_cost:,.0f}) and Road (avg ${road_avg_cost:,.0f}) per shipment
      points to a clear segmentation opportunity.
      Routing high-margin, time-sensitive orders via Air while using Road for standard
      replenishment could lift blended margins by 2–4 percentage points with no additional
      headcount or infrastructure spend.
      <span class='tag tag-blue'>Actionable</span>
    </div>
  </div>

</div>
"""
st.markdown(insights_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='dash-footer'>
    <div>
        <div class='footer-left'>Supply Chain &amp; Logistics Analytics Dashboard · Built with Streamlit &amp; Plotly</div>
        <div class='footer-author' style='margin-top:4px;'>Developed by Mayank Mayank</div>
    </div>
    <div class='footer-right'>
        Data refreshed: {datetime.now().strftime("%b %d, %Y %H:%M")}
    </div>
</div>
""", unsafe_allow_html=True)
