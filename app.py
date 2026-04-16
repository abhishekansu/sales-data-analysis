import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme / CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label { color: #94a3b8 !important; font-size: 12px; letter-spacing: 0.05em; text-transform: uppercase; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
[data-testid="stMetricValue"] { font-family: 'Space Mono', monospace; font-size: 26px; color: #0f172a; }
[data-testid="stMetricLabel"] { color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stMetricDelta"] { font-size: 13px; }

/* Header */
.dash-header { 
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
    border: 1px solid #1e2d4a;
}
.dash-title { font-family: 'Space Mono', monospace; color: #f8fafc; font-size: 28px; font-weight: 700; margin: 0; }
.dash-sub   { color: #94a3b8; font-size: 14px; margin: 6px 0 0; }

/* Section labels */
.section-title { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #94a3b8; margin: 24px 0 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }

/* Chart cards */
.chart-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; }

/* Insight chips */
.insight { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #15803d; margin: 4px 0; }
.insight-warn { background: #fff7ed; border-color: #fed7aa; color: #c2410c; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "data" / "sales_data.csv"
    if not data_path.exists():
        # Auto-generate if missing
        import subprocess, sys
        subprocess.run([sys.executable, str(Path(__file__).parent / "generate_data.py")], check=True)
    df = pd.read_csv(data_path, parse_dates=["order_date"])
    df["month"]      = df["order_date"].dt.to_period("M").astype(str)
    df["quarter"]    = df["order_date"].dt.to_period("Q").astype(str)
    df["year"]       = df["order_date"].dt.year
    df["month_name"] = df["order_date"].dt.strftime("%b %Y")
    df["margin_pct"] = (df["profit"] / df["revenue"] * 100).round(1)
    return df

df_raw = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    year_opts = sorted(df_raw["year"].unique())
    sel_years = st.multiselect("Year", year_opts, default=year_opts)

    region_opts = sorted(df_raw["region"].unique())
    sel_regions = st.multiselect("Region", region_opts, default=region_opts)

    cat_opts = sorted(df_raw["category"].unique())
    sel_cats = st.multiselect("Category", cat_opts, default=cat_opts)

    channel_opts = sorted(df_raw["channel"].unique())
    sel_channels = st.multiselect("Channel", channel_opts, default=channel_opts)

    st.markdown("---")
    st.markdown("**About**")
    st.caption("Sales Intelligence Dashboard · Built with Python, Pandas & Streamlit")

# ── Apply filters ──────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["year"].isin(sel_years) &
    df_raw["region"].isin(sel_regions) &
    df_raw["category"].isin(sel_cats) &
    df_raw["channel"].isin(sel_channels)
]

if df.empty:
    st.warning("No data matches your current filters. Please adjust the sidebar.")
    st.stop()

# ── Plotly theme ───────────────────────────────────────────────────────────────
PALETTE   = ["#2563eb","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4","#f97316","#84cc16"]
CHART_CFG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="DM Sans",
    font_color="#374151",
    margin=dict(l=10, r=10, t=36, b=10),
)

# ── Header ─────────────────────────────────────────────────────────────────────
total_rev    = df["revenue"].sum()
total_profit = df["profit"].sum()
total_orders = len(df)
avg_margin   = df["margin_pct"].mean()

date_min = df["order_date"].min().strftime("%b %d, %Y")
date_max = df["order_date"].max().strftime("%b %d, %Y")

st.markdown(f"""
<div class="dash-header">
  <p class="dash-title">📊 Sales Intelligence</p>
  <p class="dash-sub">{date_min} → {date_max} &nbsp;·&nbsp; {total_orders:,} orders &nbsp;·&nbsp; {len(sel_regions)} regions &nbsp;·&nbsp; {len(sel_cats)} categories</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue",    f"₹{total_rev/1e6:.2f}M")
k2.metric("Total Profit",     f"₹{total_profit/1e6:.2f}M")
k3.metric("Avg Margin",       f"{avg_margin:.1f}%")
k4.metric("Total Orders",     f"{total_orders:,}")
k5.metric("Avg Order Value",  f"₹{total_rev/total_orders:,.0f}")

st.markdown('<p class="section-title">Revenue Trends</p>', unsafe_allow_html=True)

# ── Revenue over time + Category breakdown ─────────────────────────────────────
c1, c2 = st.columns([2, 1])

with c1:
    monthly = (df.groupby("month")[["revenue","profit"]]
                 .sum().reset_index()
                 .sort_values("month"))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["revenue"],
        name="Revenue", line=dict(color="#2563eb", width=2.5),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.08)"
    ))
    fig.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["profit"],
        name="Profit", line=dict(color="#10b981", width=2, dash="dot")
    ))
    fig.update_layout(title="Monthly Revenue vs Profit", legend=dict(orientation="h", y=1.1), **CHART_CFG)
    fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9", tickprefix="₹")
    fig.update_xaxes(showgrid=False, tickangle=-30, tickfont_size=10)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    cat_rev = df.groupby("category")["revenue"].sum().reset_index()
    fig2 = px.pie(cat_rev, names="category", values="revenue",
                  color_discrete_sequence=PALETTE,
                  hole=0.52, title="Revenue by Category")
    fig2.update_traces(textposition="outside", textfont_size=11)
    fig2.update_layout(**CHART_CFG)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<p class="section-title">Regional & Channel Performance</p>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    reg = df.groupby("region")[["revenue","profit"]].sum().reset_index().sort_values("revenue", ascending=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(y=reg["region"], x=reg["revenue"], name="Revenue",
                          orientation="h", marker_color="#2563eb", opacity=0.85))
    fig3.add_trace(go.Bar(y=reg["region"], x=reg["profit"], name="Profit",
                          orientation="h", marker_color="#10b981", opacity=0.85))
    fig3.update_layout(barmode="overlay", title="Revenue & Profit by Region",
                       legend=dict(orientation="h", y=1.1), **CHART_CFG)
    fig3.update_xaxes(tickprefix="₹", showgrid=True, gridcolor="#f1f5f9")
    fig3.update_yaxes(showgrid=False)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    ch = df.groupby("channel")[["revenue","profit"]].sum().reset_index()
    ch["margin"] = (ch["profit"] / ch["revenue"] * 100).round(1)
    fig4 = px.bar(ch, x="channel", y="revenue", color="margin",
                  color_continuous_scale=["#dbeafe","#2563eb"],
                  title="Channel Revenue (colour = margin %)",
                  text=ch["margin"].apply(lambda x: f"{x}%"))
    fig4.update_traces(textposition="outside")
    fig4.update_layout(**CHART_CFG)
    fig4.update_yaxes(tickprefix="₹", showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('<p class="section-title">Product & Rep Performance</p>', unsafe_allow_html=True)

c5, c6 = st.columns(2)

with c5:
    top_prod = (df.groupby("product")
                  .agg(revenue=("revenue","sum"), profit=("profit","sum"), orders=("order_id","count"))
                  .reset_index()
                  .sort_values("revenue", ascending=False)
                  .head(8))
    top_prod["margin"] = (top_prod["profit"] / top_prod["revenue"] * 100).round(1)
    fig5 = px.scatter(top_prod, x="revenue", y="margin", size="orders",
                      color="profit", color_continuous_scale="Blues",
                      hover_name="product", title="Product Matrix: Revenue vs Margin",
                      labels={"revenue":"Revenue (₹)","margin":"Profit Margin (%)","orders":"Order Count"})
    fig5.update_layout(**CHART_CFG)
    fig5.update_xaxes(tickprefix="₹", showgrid=True, gridcolor="#f1f5f9")
    fig5.update_yaxes(showgrid=True, gridcolor="#f1f5f9", ticksuffix="%")
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    reps = (df.groupby("sales_rep")
              .agg(revenue=("revenue","sum"), orders=("order_id","count"), profit=("profit","sum"))
              .reset_index()
              .sort_values("revenue", ascending=True))
    reps["color"] = reps["revenue"].rank(pct=True).apply(
        lambda x: "#2563eb" if x > 0.6 else ("#f59e0b" if x > 0.3 else "#ef4444"))
    fig6 = go.Figure(go.Bar(
        x=reps["revenue"], y=reps["sales_rep"],
        orientation="h", marker_color=reps["color"],
        text=reps["revenue"].apply(lambda x: f"₹{x/1000:.0f}K"),
        textposition="outside"
    ))
    fig6.update_layout(title="Sales Rep Leaderboard", **CHART_CFG)
    fig6.update_xaxes(tickprefix="₹", showgrid=True, gridcolor="#f1f5f9")
    fig6.update_yaxes(showgrid=False)
    st.plotly_chart(fig6, use_container_width=True)

# ── Discount analysis ──────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Discount & Margin Analysis</p>', unsafe_allow_html=True)

c7, c8 = st.columns(2)

with c7:
    disc = df.groupby("discount_pct").agg(
        orders=("order_id","count"),
        avg_margin=("margin_pct","mean"),
        revenue=("revenue","sum")
    ).reset_index()
    fig7 = make_subplots(specs=[[{"secondary_y": True}]])
    fig7.add_trace(go.Bar(x=disc["discount_pct"].astype(str)+" %", y=disc["orders"],
                          name="Orders", marker_color="#dbeafe"), secondary_y=False)
    fig7.add_trace(go.Scatter(x=disc["discount_pct"].astype(str)+" %", y=disc["avg_margin"],
                              name="Avg Margin %", line=dict(color="#ef4444", width=2.5),
                              mode="lines+markers"), secondary_y=True)
    fig7.update_layout(title="Discount Level: Volume vs Margin", **CHART_CFG,
                       legend=dict(orientation="h", y=1.1))
    fig7.update_yaxes(title_text="Orders", showgrid=True, gridcolor="#f1f5f9", secondary_y=False)
    fig7.update_yaxes(title_text="Margin %", ticksuffix="%", secondary_y=True)
    st.plotly_chart(fig7, use_container_width=True)

with c8:
    heat = df.groupby(["category","region"])["margin_pct"].mean().reset_index()
    heat_pivot = heat.pivot(index="category", columns="region", values="margin_pct")
    fig8 = px.imshow(heat_pivot, color_continuous_scale="Blues",
                     title="Avg Margin % — Category × Region",
                     text_auto=".1f", aspect="auto")
    fig8.update_layout(**CHART_CFG)
    st.plotly_chart(fig8, use_container_width=True)

# ── AI Insights ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📌 Key Insights</p>', unsafe_allow_html=True)

best_region  = df.groupby("region")["revenue"].sum().idxmax()
worst_margin = df.groupby("channel")["margin_pct"].mean().idxmin()
top_product  = df.groupby("product")["revenue"].sum().idxmax()
high_disc    = df[df["discount_pct"] >= 15]["revenue"].sum() / df["revenue"].sum() * 100
best_rep     = df.groupby("sales_rep")["revenue"].sum().idxmax()

i1, i2, i3 = st.columns(3)
with i1:
    st.markdown(f'<div class="insight">🏆 <b>{best_region}</b> is the top-performing region by revenue.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight">⭐ Best rep: <b>{best_rep}</b> leads the leaderboard.</div>', unsafe_allow_html=True)
with i2:
    st.markdown(f'<div class="insight">🥇 Top product: <b>{top_product}</b> drives highest revenue.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-warn">⚠️ <b>{high_disc:.1f}%</b> of revenue comes from 15%+ discounts — review pricing.</div>', unsafe_allow_html=True)
with i3:
    st.markdown(f'<div class="insight-warn">📉 <b>{worst_margin}</b> channel has the lowest avg margin — re-evaluate channel mix.</div>', unsafe_allow_html=True)
    avg_q = df.groupby("quarter")["revenue"].sum().mean()
    st.markdown(f'<div class="insight">📈 Avg quarterly revenue: <b>₹{avg_q/1e3:.1f}K</b> across selected filters.</div>', unsafe_allow_html=True)

# ── Raw data expander ──────────────────────────────────────────────────────────
with st.expander("🗃️ View Raw Data"):
    st.dataframe(
        df[["order_id","order_date","product","category","region","channel",
            "sales_rep","quantity","unit_price","discount_pct","revenue","profit","margin_pct"]]
        .sort_values("order_date", ascending=False)
        .reset_index(drop=True),
        use_container_width=True,
        height=350
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "filtered_sales.csv", "text/csv")

st.markdown("---")
st.caption("Sales Intelligence Dashboard · Python · Pandas · Plotly · Streamlit · Built with Claude")
