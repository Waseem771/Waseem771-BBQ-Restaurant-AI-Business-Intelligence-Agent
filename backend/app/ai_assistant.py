"""Natural-language business assistant.

Two engines, same grounded contract — every answer is derived from real
query results, never invented (CLAUDE.md sec. 24, Rule 1):

* **deterministic** (default, no external calls): recognises the common
  business questions and answers them via :mod:`app.analytics`.
* **llm** (optional, when a provider is configured — Groq or Anthropic):
  the model translates the question into a single read-only ``SELECT``,
  which is executed against the read-only connection, then phrases an
  answer *from the returned rows only*.

Both return a dict:
    {question, answer, sql, rows, source, engine, provider?, model?, note?}
"""
from __future__ import annotations

import json
import re

from . import analytics, config, db

# --------------------------------------------------------------------------
# SQL safety — defence in depth (the connection is already read-only)
# --------------------------------------------------------------------------
_FORBIDDEN = (
    "insert", "update", "delete", "drop", "alter", "create", "replace",
    "attach", "detach", "pragma", "vacuum", "reindex", "truncate",
    "--", "/*",
)


def is_safe_select(sql: str) -> bool:
    """True only for a single read-only SELECT/CTE statement."""
    s = sql.strip().rstrip(";").strip()
    if not s or ";" in s:  # reject empty and multi-statement
        return False
    low = s.lower()
    if not (low.startswith("select") or low.startswith("with")):
        return False
    return not any(tok in low for tok in _FORBIDDEN)


# --------------------------------------------------------------------------
# Deterministic engine
# --------------------------------------------------------------------------
def _fmt(n: float) -> str:
    return f"{config.CURRENCY} {n:,.0f}"


EXAMPLE_QUESTIONS = [
    "What is our total revenue?",
    "What are the top 5 products?",
    "What is the average order value?",
    "Which day had the highest sales?",
    "Compare this month with last month.",
    "Which branch performs best?",
    "Are there any unusual sales patterns?",
    "How do weekends compare to weekdays?",
    "Break revenue down by category.",
]


def _answer_deterministic(question: str) -> dict:
    q = question.lower().strip()

    def result(answer: str, sql: str, rows: list) -> dict:
        return {
            "question": question,
            "answer": answer,
            "sql": sql.strip(),
            "rows": rows,
            "source": "database",
            "engine": "deterministic",
        }

    # weekend vs weekday
    if "weekend" in q or "weekday" in q:
        w = analytics.weekend_vs_weekday()
        ans = (
            f"Weekends (Fri/Sat) average **{w['weekend_avg_orders']:.1f} orders/day** "
            f"vs **{w['weekday_avg_orders']:.1f} on weekdays** — about "
            f"**{w['orders_ratio']:.2f}x** busier. Average weekend revenue is "
            f"{_fmt(w['weekend_avg_revenue'])}/day vs {_fmt(w['weekday_avg_revenue'])} on weekdays."
        )
        return result(ans, "-- analytics.weekend_vs_weekday()", [w])

    # anomalies
    if any(k in q for k in ("anomal", "unusual", "strange", "outlier", "spike", "drop", "investigate")):
        a = analytics.detect_anomalies()
        if not a:
            return result("No unusual sales days were detected.", "-- analytics.detect_anomalies()", [])
        lines = [
            f"- {r['date']}: {_fmt(r['revenue'])} ({r['deviation_pct']:+.0f}% vs expected) — {r['direction'].upper()} [{r['severity']}]"
            for r in a
        ]
        ans = f"Detected **{len(a)} unusual day(s)**:\n" + "\n".join(lines)
        return result(ans, "-- analytics.detect_anomalies()", a)

    # month over month
    if ("compare" in q and "month" in q) or "month over month" in q or "last month" in q or "previous month" in q:
        m = analytics.month_compare()
        arrow = "up" if m["change_pct"] >= 0 else "down"
        ans = (
            f"{m['current_month']} revenue was {_fmt(m['current_revenue'])}, "
            f"{arrow} **{abs(m['change_pct']):.1f}%** from {m['previous_month']} "
            f"({_fmt(m['previous_revenue'])})."
        )
        return result(ans, "-- analytics.month_compare()", [m])

    # best / highest day
    if ("day" in q and any(k in q for k in ("highest", "best", "most", "top", "peak"))) or "which day" in q:
        d = analytics.best_day()
        ans = f"The highest-revenue day was **{d['date']}** with {_fmt(d['revenue'])} across {d['orders']} orders."
        return result(ans, "-- analytics.best_day()", [d])

    # top products
    if ("top" in q or "best" in q or "popular" in q or "highest" in q) and ("product" in q or "selling" in q or "item" in q):
        m = re.search(r"top\s+(\d+)", q)
        limit = int(m.group(1)) if m else 5
        rows = analytics.top_products(limit)
        lines = [f"{i}. {r['product_name']} — {_fmt(r['revenue'])} ({r['units_sold']} units)" for i, r in enumerate(rows, 1)]
        ans = f"Top {len(rows)} products by revenue:\n" + "\n".join(lines)
        return result(ans, f"-- analytics.top_products(limit={limit})", rows)

    # category breakdown
    if "categor" in q:
        rows = analytics.category_breakdown()
        lines = [f"- {r['category']}: {_fmt(r['revenue'])}" for r in rows]
        ans = "Revenue by category:\n" + "\n".join(lines)
        return result(ans, "-- analytics.category_breakdown()", rows)

    # branch performance
    if "branch" in q:
        rows = analytics.revenue_by_branch()
        lines = [f"{i}. {r['branch_name']} — {_fmt(r['revenue'])} ({r['orders']} orders)" for i, r in enumerate(rows, 1)]
        ans = "Branches by revenue:\n" + "\n".join(lines)
        return result(ans, "-- analytics.revenue_by_branch()", rows)

    # average order value
    if "average order" in q or "aov" in q or ("average" in q and "order" in q):
        k = analytics.kpis()
        ans = f"The average order value is **{_fmt(k['avg_order_value'])}** across {k['total_orders']:,} orders."
        return result(ans, "-- analytics.kpis()", [{"avg_order_value": k["avg_order_value"]}])

    # order count
    if "how many orders" in q or "number of orders" in q or ("total" in q and "order" in q):
        k = analytics.kpis()
        ans = f"There are **{k['total_orders']:,} orders** in total ({k['start_date']} to {k['end_date']})."
        return result(ans, "-- analytics.kpis()", [{"total_orders": k["total_orders"]}])

    # profit / margin
    if "profit" in q or "margin" in q:
        k = analytics.kpis()
        ans = (
            f"Gross profit is **{_fmt(k['gross_profit'])}** on {_fmt(k['total_revenue'])} of revenue "
            f"— a gross margin of **{k['gross_margin_pct']:.1f}%**."
        )
        return result(ans, "-- analytics.kpis()", [{"gross_profit": k["gross_profit"], "gross_margin_pct": k["gross_margin_pct"]}])

    # revenue / sales / trend (broad — keep near the end)
    if "trend" in q or "monthly" in q or ("revenue" in q and ("month" in q or "over time" in q)):
        rows = analytics.revenue_by_month()
        lines = [f"- {r['month']}: {_fmt(r['revenue'])}" for r in rows]
        ans = "Monthly revenue:\n" + "\n".join(lines)
        return result(ans, "-- analytics.revenue_by_month()", rows)

    if any(k in q for k in ("revenue", "sales", "total", "earn", "made", "income")):
        k = analytics.kpis()
        ans = (
            f"Total revenue is **{_fmt(k['total_revenue'])}** from {k['total_orders']:,} orders "
            f"({k['start_date']} to {k['end_date']}), at an average order value of {_fmt(k['avg_order_value'])}."
        )
        return result(ans, "-- analytics.kpis()", [{"total_revenue": k["total_revenue"], "total_orders": k["total_orders"]}])

    # fallback — guide the user
    examples = "\n".join(f"- {x}" for x in EXAMPLE_QUESTIONS)
    return {
        "question": question,
        "answer": (
            "I couldn't map that to a known query. Try one of these "
            f"(or set a GROQ_API_KEY to ask free-form questions):\n{examples}"
        ),
        "sql": None,
        "rows": [],
        "source": "none",
        "engine": "deterministic",
    }


# --------------------------------------------------------------------------
# LLM engine (optional)
# --------------------------------------------------------------------------
_SCHEMA_DOC = """\
Tables (SQLite):
  branches(branch_id, branch_name, city, popularity_weight)
  products(product_id, product_name, category, unit_price, unit_cost, popularity_weight)
  customers(customer_id, customer_name, phone, signup_date)
  orders(order_id, order_date TEXT 'YYYY-MM-DD', branch_id, customer_id, total_amount)
  order_items(order_item_id, order_id, product_id, quantity, unit_price, discount_pct, line_total)

Notes:
- order_date is stored as text 'YYYY-MM-DD'. Use substr(order_date,1,7) for month.
- strftime('%w', order_date): Sunday=0 ... Saturday=6. Weekend = Friday(5), Saturday(6).
- Revenue = orders.total_amount (per order) or order_items.line_total (per line item).
- Profit for a line = line_total - quantity * products.unit_cost.
- All amounts are in PKR.
"""


def _complete_groq(system: str, user: str, max_tokens: int) -> str:
    """Single-turn completion via Groq's OpenAI-compatible chat endpoint."""
    from groq import Groq

    client = Groq()  # resolves GROQ_API_KEY from the environment
    resp = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.6,
        max_completion_tokens=max_tokens,
        top_p=0.95,
        reasoning_effort=config.GROQ_REASONING_EFFORT,
        stream=False,
    )
    return resp.choices[0].message.content or ""


def _complete_anthropic(system: str, user: str, max_tokens: int) -> str:
    """Single-turn completion via the Anthropic Messages API."""
    import anthropic

    client = anthropic.Anthropic()  # resolves key from env / profile
    msg = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")


# Reasoning models (e.g. Qwen) may inline their scratchpad in the content.
_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def _complete(system: str, user: str, max_tokens: int = 2048) -> str:
    """Ask the active provider for one completion, with reasoning stripped."""
    provider = config.llm_provider()
    if provider == "groq":
        text = _complete_groq(system, user, max_tokens)
    elif provider == "anthropic":
        text = _complete_anthropic(system, user, max_tokens)
    else:
        raise RuntimeError("No LLM provider is configured.")
    return _THINK_RE.sub("", text).strip()


def _extract_sql(text: str) -> str:
    """Pull a bare SQL statement out of a model response."""
    fenced = re.search(r"```(?:sql)?\s*(.+?)```", text, re.DOTALL | re.IGNORECASE)
    sql = (fenced.group(1) if fenced else text).strip()
    if is_safe_select(sql):
        return sql
    # Salvage: drop any preamble before the first SELECT / WITH.
    start = re.search(r"\b(with|select)\b", sql, re.IGNORECASE)
    if start:
        sql = sql[start.start():].strip().rstrip(";").strip()
    return sql


def _generate_sql(question: str) -> str:
    system = (
        "You are a careful data analyst. Given a question about a BBQ restaurant "
        "database, return ONE valid SQLite SELECT statement that answers it.\n"
        "Rules: read-only SELECT only (or a WITH ... SELECT); no INSERT/UPDATE/DELETE/"
        "DDL/PRAGMA; a single statement with no trailing semicolon; add a LIMIT when the "
        "result could be large. Output ONLY the SQL — no prose, no markdown fences.\n\n"
        + _SCHEMA_DOC
    )
    return _extract_sql(_complete(system, question))


def _summarize(question: str, sql: str, rows: list[dict]) -> str:
    system = (
        "You are a BI analyst. Answer the user's question using ONLY the provided "
        "query results — never invent or alter numbers. Be concise (1-3 sentences). "
        "Amounts are in PKR. If the results are empty, say the data doesn't contain an answer."
    )
    payload = (
        f"Question: {question}\n\nSQL:\n{sql}\n\n"
        f"Results (JSON, up to 100 rows):\n{json.dumps(rows[:100], default=str)}"
    )
    return _complete(system, payload)


def _answer_with_llm(question: str) -> dict:
    sql = _generate_sql(question)
    if not is_safe_select(sql):
        raise ValueError(f"Generated SQL failed the safety check: {sql!r}")
    rows = db.query_rows(sql)  # executed on the read-only connection
    answer = _summarize(question, sql, rows)
    return {
        "question": question,
        "answer": answer,
        "sql": sql,
        "rows": rows[:100],
        "source": "database",
        "engine": "llm",
        "provider": config.llm_provider(),
        "model": config.llm_model(),
    }


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------
def answer_question(question: str) -> dict:
    """Answer a natural-language business question, grounded in the data."""
    provider = config.llm_provider()
    if provider:
        try:
            return _answer_with_llm(question)
        except Exception as exc:  # noqa: BLE001 — any LLM/SQL failure -> safe fallback
            fallback = _answer_deterministic(question)
            fallback["note"] = (
                f"{provider} path unavailable ({type(exc).__name__}: {exc}); "
                "used the deterministic engine."
            )
            return fallback
    return _answer_deterministic(question)
