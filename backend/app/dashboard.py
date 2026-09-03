"""Streamlit dashboard for the BBQ Restaurant AI BI platform (MVP).

A thin presentation layer: it talks to the FastAPI backend over HTTP and
renders KPIs, charts, anomaly detection and the grounded AI assistant.
It deliberately imports nothing from ``app`` so it can run as a standalone
Streamlit process.

Run:  streamlit run app/dashboard.py
(Requires the API to be running — see run.py or the README.)
"""
from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
API = f"{API_BASE}/api/v1"

# --- palette (warm, smoky BBQ tones) --------------------------------------
PRIMARY = "#C1432E"
PALETTE = ["#C1432E", "#E07A5F", "#F2A65A", "#E9C46A", "#8AB17D", "#4A6C6F", "#3D405B"]
SEQ = "OrRd"

# Friendly names for the LLM providers reported by /health.
PROVIDER_LABELS = {"groq": "Groq", "anthropic": "Claude"}

st.set_page_config(page_title="BBQ BI", page_icon="🍢", layout="wide")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def money(n: float) -> str:
    n = float(n or 0)
    if abs(n) >= 1_000_000:
        return f"PKR {n / 1_000_000:.1f}M"
    if abs(n) >= 100_000:
        return f"PKR {n / 1_000:.0f}K"
    return f"PKR {n:,.0f}"


@st.cache_data(ttl=120, show_spinner=False)
def api_get(path: str, params: dict | None = None):
    r = requests.get(f"{API}{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=20, show_spinner=False)
def get_health():
    r = requests.get(f"{API_BASE}/health", timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(path: str, payload: dict):
    r = requests.post(f"{API}{path}", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()


def engine_badge(meta: dict) -> str:
    """Label the engine that produced an answer (model id when an LLM did)."""
    if meta.get("engine") == "llm":
        provider = PROVIDER_LABELS.get(meta.get("provider"), meta.get("provider") or "llm")
        return f"{provider} · {meta.get('model')}"
    return "deterministic"


def style_fig(fig, height: int = 340):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
        showlegend=False,
    )
    return fig


# --------------------------------------------------------------------------
# Header + connectivity guard
# --------------------------------------------------------------------------
st.title("🍢 BBQ Restaurant — Business Intelligence")

try:
    health = get_health()
except Exception:
    st.error(
        f"Cannot reach the API at **{API_BASE}**.\n\n"
        "Start the backend first, then reload this page:\n\n"
        "```bash\nuvicorn app.main:app --port 8000\n```\n"
        "…or run everything with `python run.py`."
    )
    st.stop()

with st.sidebar:
    st.header("Status")
    if health.get("status") == "healthy":
        st.success("API + database: healthy")
    else:
        st.warning(f"API degraded: {health.get('database')}")
    engine = health.get("ai_engine", "deterministic")
    if engine != "deterministic":
        st.info(f"AI engine: {PROVIDER_LABELS.get(engine, engine)} (`{health.get('ai_model')}`)")
    else:
        st.info("AI engine: deterministic (offline)\n\nSet `GROQ_API_KEY` in `.env` for free-form questions.")
    if st.button("↻ Refresh data", width="stretch"):
        st.cache_data.clear()
        st.rerun()
    st.caption("Data source: local SQLite (`data/bbq.db`), loaded from the Phase 1 CSVs.")

tab_dash, tab_ai = st.tabs(["📊 Dashboard", "🤖 AI Assistant"])

# --------------------------------------------------------------------------
# Dashboard tab
# --------------------------------------------------------------------------
with tab_dash:
    k = api_get("/dashboard/kpis")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Revenue", money(k["total_revenue"]))
    c2.metric("Orders", f"{k['total_orders']:,}")
    c3.metric("Avg Order Value", money(k["avg_order_value"]))
    c4.metric("Gross Margin", f"{k['gross_margin_pct']:.1f}%")
    c5.metric("Gross Profit", money(k["gross_profit"]))
    st.caption(
        f"{k['start_date']} → {k['end_date']}  •  "
        f"{k['total_branches']} branches  •  {k['total_products']} products  •  "
        f"{k['total_customers']:,} customers"
    )

    st.divider()

    # Monthly revenue trend
    st.subheader("Monthly revenue")
    m = pd.DataFrame(api_get("/sales/monthly"))
    fig = px.line(m, x="month", y="revenue", markers=True)
    fig.update_traces(line_color=PRIMARY, line_width=3, marker=dict(size=8))
    fig.update_yaxes(title=None, gridcolor="rgba(0,0,0,0.08)")
    fig.update_xaxes(title=None)
    st.plotly_chart(style_fig(fig), width="stretch")

    # Branch + category
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Revenue by branch")
        b = pd.DataFrame(api_get("/sales/by-branch")).sort_values("revenue")
        fig = px.bar(b, x="revenue", y="branch_name", orientation="h",
                     color="revenue", color_continuous_scale=SEQ, text="revenue")
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        fig.update_yaxes(title=None)
        fig.update_xaxes(title=None, showticklabels=False)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig), width="stretch")
    with col_b:
        st.subheader("Revenue by category")
        c = pd.DataFrame(api_get("/products/categories"))
        fig = px.pie(c, names="category", values="revenue", hole=0.5,
                     color_discrete_sequence=PALETTE)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig), width="stretch")

    # Top products
    st.subheader("Top products")
    n = st.slider("How many", 5, 20, 10, key="topn")
    t = pd.DataFrame(api_get("/products/top", {"limit": n})).sort_values("revenue")
    fig = px.bar(t, x="revenue", y="product_name", orientation="h",
                 color="revenue", color_continuous_scale=SEQ)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title="Revenue (PKR)")
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(style_fig(fig, height=max(320, 28 * n)), width="stretch")

    # Anomalies
    st.subheader("Anomaly detection")
    st.caption(
        "Days whose revenue deviates sharply from the median for that weekday "
        "(day-of-week aware, so normal weekend peaks are not flagged)."
    )
    daily = pd.DataFrame(api_get("/sales/daily"))
    anoms = pd.DataFrame(api_get("/anomalies"))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["revenue"], mode="lines",
        line=dict(color="rgba(120,120,120,0.55)", width=1.4), name="Daily revenue",
    ))
    if not anoms.empty:
        colors = ["#2A9D8F" if d == "spike" else "#C1432E" for d in anoms["direction"]]
        fig.add_trace(go.Scatter(
            x=anoms["date"], y=anoms["revenue"], mode="markers",
            marker=dict(size=13, color=colors, line=dict(width=1, color="white")),
            name="Anomaly",
            text=[f"{d.upper()} {p:+.0f}%" for d, p in zip(anoms["direction"], anoms["deviation_pct"])],
            hovertemplate="%{x}<br>%{y:,.0f} PKR<br>%{text}<extra></extra>",
        ))
    fig.update_yaxes(title=None, gridcolor="rgba(0,0,0,0.08)")
    fig.update_xaxes(title=None)
    st.plotly_chart(style_fig(fig, height=320), width="stretch")

    if anoms.empty:
        st.success("No unusual sales days detected.")
    else:
        show = anoms.rename(columns={
            "date": "Date", "revenue": "Revenue", "expected": "Expected",
            "deviation_pct": "Deviation %", "direction": "Direction", "severity": "Severity",
        })
        st.dataframe(show, width="stretch", hide_index=True)

# --------------------------------------------------------------------------
# AI Assistant tab
# --------------------------------------------------------------------------
with tab_ai:
    st.subheader("Ask a business question")
    st.caption(
        "Answers are grounded in the database — every figure comes from a real query, "
        "never invented. The offline engine handles the common questions; add a "
        "`GROQ_API_KEY` to ask anything free-form."
    )

    EXAMPLES = [
        "What is our total revenue?",
        "Which branch performs best?",
        "What are the top 5 products?",
        "Are there any unusual sales patterns?",
        "How do weekends compare to weekdays?",
        "Compare this month with last month.",
    ]

    st.session_state.setdefault("chat", [])

    pending = None
    ex_cols = st.columns(3)
    for i, ex in enumerate(EXAMPLES):
        if ex_cols[i % 3].button(ex, key=f"ex{i}", width="stretch"):
            pending = ex

    typed = st.chat_input("e.g. Which branch made the most revenue?")

    # Replay history
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            meta = msg.get("meta")
            if meta:
                badge = engine_badge(meta)
                with st.expander(f"How this was answered · engine: {badge} · source: {meta.get('source')}"):
                    if meta.get("note"):
                        st.warning(meta["note"])
                    if meta.get("sql"):
                        st.code(meta["sql"], language="sql")
                    if meta.get("rows"):
                        st.dataframe(pd.DataFrame(meta["rows"]), width="stretch", hide_index=True)

    q = typed or pending
    if q:
        with st.chat_message("user"):
            st.markdown(q)
        st.session_state.chat.append({"role": "user", "content": q})
        with st.chat_message("assistant"):
            try:
                with st.spinner("Analyzing the data…"):
                    resp = api_post("/ai/chat", {"question": q})
                st.markdown(resp["answer"])
                badge = engine_badge(resp)
                with st.expander(f"How this was answered · engine: {badge} · source: {resp.get('source')}"):
                    if resp.get("note"):
                        st.warning(resp["note"])
                    if resp.get("sql"):
                        st.code(resp["sql"], language="sql")
                    if resp.get("rows"):
                        st.dataframe(pd.DataFrame(resp["rows"]), width="stretch", hide_index=True)
                st.session_state.chat.append({"role": "assistant", "content": resp["answer"], "meta": resp})
            except Exception as exc:  # noqa: BLE001
                err = f"⚠️ Could not get an answer: {exc}"
                st.error(err)
                st.session_state.chat.append({"role": "assistant", "content": err})
