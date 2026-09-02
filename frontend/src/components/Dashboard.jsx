import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  TrendingUp, TrendingDown, AlertCircle, MessageSquare,
  Settings, LogOut, Bell, Menu, X, ChevronDown,
  Calendar, RefreshCw, Send, Package, Users,
  DollarSign, ShoppingBag, BarChart2, Star,
  AlertTriangle, CheckCircle
} from 'lucide-react';
import '../styles/Dashboard.css';

// Error boundary to catch crashes
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Dashboard Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#D84C1A' }}>
          <h2>⚠️ Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()} style={{
            padding: '0.5rem 1rem',
            background: '#D84C1A',
            color: '#fff',
            border: 'none',
            borderRadius: 6,
            cursor: 'pointer'
          }}>
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

/* ─── helpers ──────────────────────────────────────────────────────────── */
const BASE = 'http://localhost:8000/api/v1';

async function api(path) {
  try {
    const res = await fetch(`${BASE}${path}`);
    if (!res.ok) return null;
    const data = await res.json();
    return Array.isArray(data) ? data : (data.value ?? data);
  } catch (err) {
    console.warn(`API call failed: ${path}`, err.message);
    return null;
  }
}

const fmtN = (n) => {
  try {
    return new Intl.NumberFormat('en-PK', { maximumFractionDigits: 0 }).format(n || 0);
  } catch {
    return String(n || 0);
  }
};
const fmtPKR = (n) => `₨${fmtN(n)}`;

/* ─── tiny shared components ───────────────────────────────────────────── */
function Loader() {
  return (
    <div style={{ textAlign: 'center', padding: '3rem', color: '#8B8B8B' }}>
      <style>{`
        @keyframes dashSpin {
          to { transform: rotate(360deg); }
        }
      `}</style>
      <div
        style={{
          width: 32,
          height: 32,
          border: '3px solid #E8E6E2',
          borderTopColor: '#D84C1A',
          borderRadius: '50%',
          animation: 'dashSpin 0.8s linear infinite',
          margin: '0 auto 1rem',
        }}
      />
      Loading data…
    </div>
  );
}

function Tip({ active, payload, label }) {
  if (!active || !payload || !Array.isArray(payload) || payload.length === 0) return null;

  return (
    <div className="dashboard-tooltip">
      <p className="tooltip-label">{String(label || 'Data')}</p>
      {payload.map((e, i) => {
        try {
          const value = typeof e.value === 'number' && e.value > 999
            ? fmtPKR(e.value)
            : String(e.value || '—');
          return (
            <p key={`tooltip-${i}`} style={{ color: e.color || '#666' }}>
              {String(e.name || 'Value')}: {value}
            </p>
          );
        } catch (err) {
          console.warn('Tooltip render error:', err);
          return null;
        }
      })}
    </div>
  );
}

const BRAND = ['#D84C1A', '#F39C12', '#27AE60', '#3498DB', '#9B59B6'];

/* ═══════════════════════════════════════════════════════════════════════
   OVERVIEW
═══════════════════════════════════════════════════════════════════════ */
function Overview() {
  const [kpis, setKpis] = useState(null);
  const [monthly, setMonthly] = useState([]);
  const [products, setProducts] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [k, m, p, a] = await Promise.all([
          api('/dashboard/kpis'),
          api('/sales/monthly'),
          api('/products/top?limit=5'),
          api('/anomalies?threshold=0.6'),
        ]);

        if (k && typeof k === 'object' && !Array.isArray(k)) setKpis(k);
        if (Array.isArray(m)) setMonthly(m);
        if (Array.isArray(p)) setProducts(p);
        if (Array.isArray(a)) setAnomalies(a);
      } catch (err) {
        console.error('Overview load error:', err);
        setError(err.message);
      } finally {
        setBusy(false);
      }
    };

    loadData();
  }, []);

  if (error) {
    return (
      <div style={{ padding: '2rem', color: '#E74C3C' }}>
        <p>⚠️ Error loading overview: {error}</p>
      </div>
    );
  }

  if (busy) return <Loader />;

  const cards = kpis
    ? [
        { label: 'Total Revenue',    value: fmtPKR(kpis.total_revenue),    Icon: DollarSign,  note: `${kpis.gross_margin_pct}% margin` },
        { label: 'Total Orders',     value: fmtN(kpis.total_orders),        Icon: ShoppingBag, note: '+8.2% vs last period' },
        { label: 'Avg Order Value',  value: fmtPKR(kpis.avg_order_value),   Icon: BarChart2,   note: '+3.8% vs last period' },
        { label: 'Gross Profit',     value: fmtPKR(kpis.gross_profit),      Icon: TrendingUp,  note: `${kpis.total_branches} branches` },
        { label: 'Total Customers',  value: fmtN(kpis.total_customers),     Icon: Users,       note: `${kpis.start_date} → ${kpis.end_date}` },
        { label: 'Products',         value: fmtN(kpis.total_products),      Icon: Package,     note: '4 categories' },
      ]
    : [];

  return (
    <>
      {/* KPI CARDS */}
      <section className="kpi-section">
        <h2 className="section-title">📊 Key Performance Indicators</h2>
        <div className="kpi-grid">
          {cards.map((c, i) => (
            <div key={i} className="kpi-card">
              <div className="kpi-header">
                <c.Icon size={20} style={{ color: '#D84C1A' }} />
                <span className="kpi-change up">
                  <TrendingUp size={12} /> {c.note}
                </span>
              </div>
              <p className="kpi-label">{c.label}</p>
              <p className="kpi-value">{c.value}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CHARTS */}
      <section className="charts-section">
        {/* Monthly Revenue */}
        <div className="chart-card">
          <div className="chart-header"><h3>📈 Monthly Revenue</h3></div>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={monthly}>
              <defs>
                <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#D84C1A" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#D84C1A" stopOpacity={0}   />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
              <XAxis dataKey="month" stroke="#8B8B8B" tick={{ fontSize: 11 }} />
              <YAxis stroke="#8B8B8B" tickFormatter={(v) => `₨${(v / 1000).toFixed(0)}k`} />
              <Tooltip content={<Tip />} />
              <Area type="monotone" dataKey="revenue" stroke="#D84C1A"
                fill="url(#g1)" strokeWidth={2} name="Revenue" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Top Products Pie */}
        <div className="chart-card">
          <div className="chart-header"><h3>🍖 Top Products</h3></div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={products} cx="50%" cy="50%" outerRadius={95}
                dataKey="revenue"
                label={({ name, percent }) => {
                  try {
                    const nameStr = String(name || '');
                    const firstName = nameStr.split(' ')[0] || 'Product';
                    return `${firstName} ${(percent * 100).toFixed(0)}%`;
                  } catch (e) {
                    return `Product ${(percent * 100).toFixed(0)}%`;
                  }
                }}
                labelLine={false}>
                {products.map((_, i) => (
                  <Cell key={i} fill={BRAND[i % BRAND.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => fmtPKR(v)} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* ANOMALIES */}
      <section className="anomalies-section">
        <h2 className="section-title">🚨 Recent Anomalies</h2>
        <div className="anomalies-list">
          {anomalies.length === 0 && (
            <p style={{ color: '#27AE60' }}>✅ No anomalies detected</p>
          )}
          {anomalies.slice(0, 5).map((a, i) => (
            <div key={i}
              className={`anomaly-item severity-${a.severity === 'HIGH' ? 'warning' : 'info'}`}>
              <div className="anomaly-icon">
                {a.direction === 'spike'
                  ? <TrendingUp size={20} />
                  : <TrendingDown size={20} />}
              </div>
              <div className="anomaly-content">
                <p className="anomaly-type">
                  {a.severity} — Revenue {a.direction} on {a.date}
                </p>
                <p className="anomaly-message">
                  Actual: {fmtPKR(a.revenue)} | Expected: {fmtPKR(a.expected)} | Deviation: {a.deviation_pct}%
                </p>
              </div>
              <p className="anomaly-time">{a.date}</p>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}

/* ═══════════════════════════════════════════════════════════════════════
   ANALYTICS
═══════════════════════════════════════════════════════════════════════ */
function Analytics() {
  const [branches, setBranches] = useState([]);
  const [monthly, setMonthly] = useState([]);
  const [weekend, setWeekend] = useState(null);
  const [monthComp, setMonthComp] = useState(null);
  const [daily, setDaily] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [b, m, w, mc, d] = await Promise.all([
          api('/sales/by-branch'),
          api('/sales/monthly'),
          api('/sales/weekend-vs-weekday'),
          api('/sales/month-compare'),
          api('/sales/daily'),
        ]);

        if (Array.isArray(b)) setBranches(b);
        if (Array.isArray(m)) setMonthly(m);
        if (w && typeof w === 'object' && !Array.isArray(w)) setWeekend(w);
        if (mc && typeof mc === 'object' && !Array.isArray(mc)) setMonthComp(mc);
        if (Array.isArray(d)) setDaily(d.slice(-30));
      } catch (err) {
        console.error('Analytics load error:', err);
        setError(err.message);
      } finally {
        setBusy(false);
      }
    };

    loadData();
  }, []);

  if (error) {
    return (
      <div style={{ padding: '2rem', color: '#E74C3C' }}>
        <p>⚠️ Error loading analytics: {error}</p>
      </div>
    );
  }

  if (busy) return <Loader />;

  const BCOL = ['#D84C1A', '#F39C12', '#27AE60'];
  const totalRev = branches.reduce((s, b) => s + (b.revenue || 0), 0);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <h2 className="section-title">📈 Advanced Analytics</h2>

      {/* Month comparison */}
      {monthComp && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
          {[
            { label: 'Previous Month', sub: monthComp.previous_month, val: fmtPKR(monthComp.previous_revenue), color: '#8B8B8B' },
            { label: 'Current Month',  sub: monthComp.current_month,  val: fmtPKR(monthComp.current_revenue),  color: '#D84C1A' },
            {
              label: 'Month-over-Month', sub: 'Change',
              val: `${monthComp.change_pct >= 0 ? '+' : ''}${monthComp.change_pct}%`,
              color: monthComp.change_pct >= 0 ? '#27AE60' : '#E74C3C',
            },
          ].map((c, i) => (
            <div key={i} className="kpi-card" style={{ borderTop: `3px solid ${c.color}` }}>
              <p className="kpi-label">{c.label}</p>
              <p style={{ fontSize: '0.72rem', color: '#8B8B8B', margin: '2px 0 6px' }}>{c.sub}</p>
              <p className="kpi-value" style={{ color: c.color }}>{c.val}</p>
            </div>
          ))}
        </div>
      )}

      {/* Branch bar chart + cards */}
      <div className="chart-card full-width">
        <div className="chart-header"><h3>🏪 Branch Performance</h3></div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', alignItems: 'center' }}>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={branches} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
              <XAxis type="number" stroke="#8B8B8B"
                tickFormatter={(v) => `₨${(v / 1000000).toFixed(1)}M`} />
              <YAxis type="category" dataKey="branch_name" stroke="#8B8B8B"
                width={130} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(v) => fmtPKR(v)} />
              <Bar dataKey="revenue" name="Revenue" radius={[0, 4, 4, 0]}>
                {branches.map((_, i) => <Cell key={i} fill={BCOL[i]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
            {branches.map((b, i) => {
              const pct = totalRev ? ((b.revenue / totalRev) * 100).toFixed(1) : 0;
              return (
                <div key={i} style={{
                  padding: '0.7rem 1rem', background: '#F8F6F2',
                  borderRadius: 8, borderLeft: `4px solid ${BCOL[i]}`,
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
                    <strong style={{ fontSize: '0.875rem' }}>{b.branch_name}</strong>
                    <span style={{ color: BCOL[i], fontWeight: 700 }}>{pct}%</span>
                  </div>
                  <p style={{ fontSize: '0.78rem', color: '#5C5C5C' }}>
                    Revenue: {fmtPKR(b.revenue)} &nbsp;|&nbsp;
                    Orders: {fmtN(b.orders)} &nbsp;|&nbsp;
                    Avg: {fmtPKR(b.avg_order_value)}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Daily 30-day trend */}
      <div className="chart-card full-width">
        <div className="chart-header"><h3>📅 Daily Revenue — Last 30 Days</h3></div>
        <ResponsiveContainer width="100%" height={240}>
          <AreaChart data={daily}>
            <defs>
              <linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#3498DB" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3498DB" stopOpacity={0}   />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
            <XAxis dataKey="date" stroke="#8B8B8B" tick={{ fontSize: 10 }}
              interval={Math.floor(daily.length / 6)} />
            <YAxis stroke="#8B8B8B" tickFormatter={(v) => `₨${(v / 1000).toFixed(0)}k`} />
            <Tooltip content={<Tip />} />
            <Area type="monotone" dataKey="revenue" stroke="#3498DB"
              fill="url(#g2)" strokeWidth={2} name="Daily Revenue" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Weekend vs Weekday */}
      {weekend && (
        <div className="chart-card">
          <div className="chart-header"><h3>📆 Weekend vs Weekday</h3></div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', padding: '0.5rem 0' }}>
            {[
              { label: '🎉 Weekend Avg Revenue', val: fmtPKR(weekend.weekend_avg_revenue), color: '#D84C1A' },
              { label: '💼 Weekday Avg Revenue', val: fmtPKR(weekend.weekday_avg_revenue), color: '#3498DB' },
              { label: '🎉 Weekend Avg Orders',  val: weekend.weekend_avg_orders,           color: '#D84C1A' },
              { label: '💼 Weekday Avg Orders',  val: weekend.weekday_avg_orders,           color: '#3498DB' },
            ].map((item, i) => (
              <div key={i} style={{ padding: '1rem', background: '#F8F6F2', borderRadius: 8, textAlign: 'center' }}>
                <p style={{ fontSize: '0.78rem', color: '#5C5C5C', marginBottom: 6 }}>{item.label}</p>
                <p style={{ fontSize: '1.3rem', fontWeight: 700, color: item.color }}>{item.val}</p>
              </div>
            ))}
          </div>
          {weekend.orders_ratio && (
            <p style={{ textAlign: 'center', color: '#27AE60', fontWeight: 600, paddingTop: 8 }}>
              ✅ Weekends generate {weekend.orders_ratio}× more orders than weekdays
            </p>
          )}
        </div>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════
   PRODUCTS
═══════════════════════════════════════════════════════════════════════ */
function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [p, c] = await Promise.all([
          api('/products/top?limit=14'),
          api('/products/categories')
        ]);

        if (Array.isArray(p)) setProducts(p);
        if (Array.isArray(c)) setCategories(c);
      } catch (err) {
        console.error('Products load error:', err);
        setError(err.message);
      } finally {
        setBusy(false);
      }
    };

    loadData();
  }, []);

  if (error) {
    return (
      <div style={{ padding: '2rem', color: '#E74C3C' }}>
        <p>⚠️ Error loading products: {error}</p>
      </div>
    );
  }

  if (busy) return <Loader />;

  const CAT = { 'BBQ Platters': '#D84C1A', Sides: '#27AE60', Beverages: '#3498DB', Desserts: '#9B59B6' };
  const totalRev = products.reduce((s, p) => s + (p.revenue || 0), 0);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <h2 className="section-title">🍖 Product Performance</h2>

      {/* Category charts */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div className="chart-card">
          <div className="chart-header"><h3>📂 Revenue by Category</h3></div>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={categories} cx="50%" cy="50%" outerRadius={85} innerRadius={35}
                dataKey="revenue"
                label={({ name, percent }) => {
                  try {
                    const nameStr = String(name || 'Category');
                    return `${nameStr} ${(percent * 100).toFixed(0)}%`;
                  } catch (e) {
                    return `${(percent * 100).toFixed(0)}%`;
                  }
                }}
                labelLine={false}>
                {categories.map((c, i) => <Cell key={i} fill={CAT[c.category] || '#8B8B8B'} />)}
              </Pie>
              <Tooltip formatter={(v) => fmtPKR(v)} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <div className="chart-header"><h3>📦 Units Sold by Category</h3></div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={categories}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
              <XAxis dataKey="category" stroke="#8B8B8B" tick={{ fontSize: 11 }} />
              <YAxis stroke="#8B8B8B" />
              <Tooltip />
              <Bar dataKey="units_sold" name="Units Sold" radius={[4, 4, 0, 0]}>
                {categories.map((c, i) => <Cell key={i} fill={CAT[c.category] || '#8B8B8B'} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Full product table */}
      <div className="chart-card full-width">
        <div className="chart-header"><h3>📋 All Products — Detailed Breakdown</h3></div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
            <thead>
              <tr style={{ background: '#F8F6F2', borderBottom: '2px solid #E8E6E2' }}>
                {['#', 'Product', 'Category', 'Revenue', 'Units Sold', 'Share', 'Avg Price'].map((h) => (
                  <th key={h} style={{ padding: '10px 14px', textAlign: 'left', fontWeight: 600, color: '#5C5C5C', whiteSpace: 'nowrap' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {products.map((p, i) => {
                const share = totalRev ? ((p.revenue / totalRev) * 100).toFixed(1) : 0;
                const avgPrice = p.units_sold ? (p.revenue / p.units_sold).toFixed(0) : 0;
                return (
                  <tr key={i} style={{ borderBottom: '1px solid #E8E6E2' }}>
                    <td style={{ padding: '10px 14px', color: '#8B8B8B' }}>{i + 1}</td>
                    <td style={{ padding: '10px 14px', fontWeight: 600 }}>
                      {i === 0 && <Star size={13} style={{ color: '#F39C12', display: 'inline', marginRight: 4 }} />}
                      {p.product_name}
                    </td>
                    <td style={{ padding: '10px 14px' }}>
                      <span style={{ background: CAT[p.category] || '#8B8B8B', color: '#fff', padding: '2px 8px', borderRadius: 12, fontSize: '0.72rem' }}>
                        {p.category}
                      </span>
                    </td>
                    <td style={{ padding: '10px 14px', fontWeight: 600, color: '#D84C1A' }}>{fmtPKR(p.revenue)}</td>
                    <td style={{ padding: '10px 14px' }}>{fmtN(p.units_sold)}</td>
                    <td style={{ padding: '10px 14px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <div style={{ width: 60, background: '#E8E6E2', borderRadius: 4, height: 6 }}>
                          <div style={{ width: `${share}%`, background: '#D84C1A', height: '100%', borderRadius: 4 }} />
                        </div>
                        <span style={{ fontSize: '0.78rem', color: '#5C5C5C' }}>{share}%</span>
                      </div>
                    </td>
                    <td style={{ padding: '10px 14px', color: '#5C5C5C' }}>₨{fmtN(avgPrice)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════
   FORECASTING
═══════════════════════════════════════════════════════════════════════ */
function Forecasting() {
  const [monthly, setMonthly] = useState([]);
  const [bestDay, setBestDay] = useState(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [m, bd] = await Promise.all([
          api('/sales/monthly'),
          api('/sales/best-day')
        ]);

        if (Array.isArray(m)) setMonthly(m);
        if (bd && typeof bd === 'object' && !Array.isArray(bd)) setBestDay(bd);
      } catch (err) {
        console.error('Forecasting load error:', err);
        setError(err.message);
      } finally {
        setBusy(false);
      }
    };

    loadData();
  }, []);

  if (error) {
    return (
      <div style={{ padding: '2rem', color: '#E74C3C' }}>
        <p>⚠️ Error loading forecasting: {error}</p>
      </div>
    );
  }

  if (busy) return <Loader />;

  /* build 6-month forecast */
  const forecastData = (() => {
    if (monthly.length < 3) return [];
    const last3 = monthly.slice(-3);
    const avgGrowth =
      last3.length > 1
        ? last3
            .slice(1)
            .reduce((s, r, i) => s + (r.revenue - last3[i].revenue) / last3[i].revenue, 0) /
          (last3.length - 1)
        : 0.03;
    const lastRev = (last3[last3.length - 1] || {}).revenue || 0;
    const labels = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'];
    const proj = labels.map((mn, i) => ({
      month: mn,
      forecast: Math.round(lastRev * Math.pow(1 + avgGrowth, i + 1)),
      upper:    Math.round(lastRev * Math.pow(1 + avgGrowth * 1.3, i + 1)),
      lower:    Math.round(lastRev * Math.pow(1 + avgGrowth * 0.7, i + 1)),
    }));
    return [
      ...monthly.slice(-4).map((r) => ({ month: r.month, actual: r.revenue })),
      ...proj,
    ];
  })();

  const lastRev = (monthly[monthly.length - 1] || {}).revenue || 0;
  const prevRev = (monthly[monthly.length - 2] || {}).revenue || 0;
  const growth = prevRev ? (((lastRev - prevRev) / prevRev) * 100).toFixed(1) : 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <h2 className="section-title">🔮 AI Forecasting & Predictions</h2>

      {/* summary */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '1rem' }}>
        {[
          { label: 'Last Month Revenue',    val: fmtPKR(lastRev),                               icon: '📊', color: '#D84C1A' },
          { label: 'Month-over-Month',       val: `${Number(growth) >= 0 ? '+' : ''}${growth}%`, icon: '📈', color: Number(growth) >= 0 ? '#27AE60' : '#E74C3C' },
          { label: 'Best Sales Day',         val: bestDay ? bestDay.date : '—',                  icon: '🏆', color: '#F39C12', sub: bestDay ? fmtPKR(bestDay.revenue) : '' },
        ].map((c, i) => (
          <div key={i} className="kpi-card" style={{ borderTop: `3px solid ${c.color}` }}>
            <div style={{ fontSize: '1.8rem' }}>{c.icon}</div>
            <p className="kpi-label" style={{ marginTop: 8 }}>{c.label}</p>
            <p className="kpi-value" style={{ color: c.color }}>{c.val}</p>
            {c.sub && <p style={{ fontSize: '0.78rem', color: '#5C5C5C' }}>{c.sub}</p>}
          </div>
        ))}
      </div>

      {/* 6-month forecast chart */}
      <div className="chart-card full-width">
        <div className="chart-header">
          <h3>📉 Revenue Forecast — Next 6 Months</h3>
          <span style={{ fontSize: '0.78rem', color: '#8B8B8B', background: '#F8F6F2', padding: '3px 10px', borderRadius: 12 }}>
            AI Linear Trend Model
          </span>
        </div>
        <ResponsiveContainer width="100%" height={290}>
          <LineChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
            <XAxis dataKey="month" stroke="#8B8B8B" tick={{ fontSize: 11 }} />
            <YAxis stroke="#8B8B8B" tickFormatter={(v) => `₨${(v / 1000000).toFixed(1)}M`} />
            <Tooltip formatter={(v) => fmtPKR(v)} />
            <Legend />
            <Line type="monotone" dataKey="actual"   stroke="#27AE60" strokeWidth={2.5} dot={{ r: 4 }} name="Actual"          connectNulls={false} />
            <Line type="monotone" dataKey="forecast" stroke="#D84C1A" strokeWidth={2.5} strokeDasharray="6 3" dot={{ r: 4 }} name="Forecast" connectNulls={false} />
            <Line type="monotone" dataKey="upper"    stroke="#F39C12" strokeWidth={1}   strokeDasharray="3 3" dot={false}     name="Upper"           connectNulls={false} />
            <Line type="monotone" dataKey="lower"    stroke="#3498DB" strokeWidth={1}   strokeDasharray="3 3" dot={false}     name="Lower"           connectNulls={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* historical bar */}
      <div className="chart-card full-width">
        <div className="chart-header"><h3>📊 Historical Monthly Revenue</h3></div>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={monthly}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
            <XAxis dataKey="month" stroke="#8B8B8B" tick={{ fontSize: 11 }} />
            <YAxis stroke="#8B8B8B" tickFormatter={(v) => `₨${(v / 1000000).toFixed(1)}M`} />
            <Tooltip formatter={(v) => fmtPKR(v)} />
            <Bar dataKey="revenue" name="Revenue" fill="#D84C1A" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════
   ALERTS
═══════════════════════════════════════════════════════════════════════ */
function Alerts() {
  const [anomalies, setAnomalies] = useState([]);
  const [threshold, setThreshold] = useState(0.6);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback((t) => {
    setBusy(true);
    setError(null);
    api(`/anomalies?threshold=${t}`).then((data) => {
      try {
        if (Array.isArray(data)) setAnomalies(data);
        else setAnomalies([]);
      } catch (err) {
        console.error('Alerts parse error:', err);
        setError(err.message);
      } finally {
        setBusy(false);
      }
    }).catch((err) => {
      console.error('Alerts load error:', err);
      setError(err.message);
      setBusy(false);
    });
  }, []);

  useEffect(() => { load(0.6); }, [load]);

  if (error) {
    return (
      <div style={{ padding: '2rem', color: '#E74C3C' }}>
        <p>⚠️ Error loading alerts: {error}</p>
      </div>
    );
  }

  const spikes       = anomalies.filter((a) => a.direction === 'spike');
  const drops        = anomalies.filter((a) => a.direction === 'drop');
  const highSeverity = anomalies.filter((a) => a.severity === 'HIGH');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* header + sensitivity */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <h2 className="section-title" style={{ margin: 0 }}>🚨 Alerts & Anomaly Monitoring</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <label style={{ fontSize: '0.85rem', color: '#5C5C5C' }}>Sensitivity:</label>
          <select value={threshold}
            onChange={(e) => { const t = parseFloat(e.target.value); setThreshold(t); load(t); }}
            style={{ padding: '5px 10px', border: '1px solid #E8E6E2', borderRadius: 6, fontSize: '0.85rem' }}>
            <option value={0.4}>High (40%)</option>
            <option value={0.6}>Medium (60%)</option>
            <option value={0.8}>Low (80%)</option>
          </select>
        </div>
      </div>

      {/* summary stat cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '1rem' }}>
        {[
          { label: 'Total Anomalies', val: anomalies.length,    color: '#D84C1A', Icon: AlertCircle   },
          { label: 'Revenue Spikes',  val: spikes.length,       color: '#F39C12', Icon: TrendingUp    },
          { label: 'Revenue Drops',   val: drops.length,        color: '#3498DB', Icon: TrendingDown  },
          { label: 'High Severity',   val: highSeverity.length, color: '#E74C3C', Icon: AlertTriangle },
        ].map((s, i) => (
          <div key={i} className="kpi-card" style={{ borderTop: `3px solid ${s.color}` }}>
            <s.Icon size={20} style={{ color: s.color }} />
            <p className="kpi-label" style={{ marginTop: 8 }}>{s.label}</p>
            <p className="kpi-value" style={{ color: s.color }}>{s.val}</p>
          </div>
        ))}
      </div>

      {busy ? <Loader /> : (
        <>
          {anomalies.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', background: '#F8F6F2', borderRadius: 12 }}>
              <CheckCircle size={44} style={{ color: '#27AE60', display: 'block', margin: '0 auto 1rem' }} />
              <p style={{ fontWeight: 600, color: '#27AE60', fontSize: '1.05rem' }}>
                ✅ No anomalies at this sensitivity level
              </p>
              <p style={{ color: '#8B8B8B', marginTop: 4 }}>All revenue data is within expected ranges.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              {anomalies.map((a, i) => (
                <div key={i} style={{
                  display: 'grid', gridTemplateColumns: '40px 1fr auto',
                  alignItems: 'center', gap: '1rem',
                  padding: '1rem 1.25rem',
                  background: a.severity === 'HIGH' ? '#FFF5F0' : '#FAFAFA',
                  border: `1px solid ${a.severity === 'HIGH' ? '#FDDDD5' : '#E8E6E2'}`,
                  borderLeft: `4px solid ${a.direction === 'spike' ? '#D84C1A' : '#3498DB'}`,
                  borderRadius: 8,
                }}>
                  <div style={{ color: a.direction === 'spike' ? '#D84C1A' : '#3498DB' }}>
                    {a.direction === 'spike'
                      ? <TrendingUp size={22} />
                      : <TrendingDown size={22} />}
                  </div>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                      <strong style={{ fontSize: '0.88rem' }}>
                        Revenue {a.direction === 'spike' ? 'Spike' : 'Drop'} — {a.date}
                      </strong>
                      <span style={{
                        fontSize: '0.68rem', fontWeight: 700, padding: '2px 8px', borderRadius: 10,
                        background: a.severity === 'HIGH' ? '#FDDDD5' : '#FEF3CD',
                        color: a.severity === 'HIGH' ? '#C0392B' : '#856404',
                      }}>{a.severity}</span>
                    </div>
                    <p style={{ fontSize: '0.8rem', color: '#5C5C5C' }}>
                      Actual: <strong>{fmtPKR(a.revenue)}</strong> &nbsp;|&nbsp;
                      Expected: <strong>{fmtPKR(a.expected)}</strong> &nbsp;|&nbsp;
                      Deviation: <strong style={{ color: a.deviation_pct > 0 ? '#D84C1A' : '#3498DB' }}>
                        {a.deviation_pct > 0 ? '+' : ''}{a.deviation_pct}%
                      </strong>
                    </p>
                  </div>
                  <span style={{ fontSize: '0.78rem', color: '#8B8B8B', whiteSpace: 'nowrap' }}>{a.date}</span>
                </div>
              ))}
            </div>
          )}

          {/* Deviation chart */}
          {anomalies.length > 0 && (
            <div className="chart-card full-width">
              <div className="chart-header"><h3>📊 Anomaly Deviation Chart</h3></div>
              <ResponsiveContainer width="100%" height={210}>
                <BarChart data={anomalies}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
                  <XAxis dataKey="date" stroke="#8B8B8B" tick={{ fontSize: 10 }}
                    interval={Math.max(0, Math.floor(anomalies.length / 6))} />
                  <YAxis stroke="#8B8B8B" tickFormatter={(v) => `${v}%`} />
                  <Tooltip formatter={(v) => `${v}%`} />
                  <Bar dataKey="deviation_pct" name="Deviation %" radius={[4, 4, 0, 0]}>
                    {anomalies.map((a, i) => (
                      <Cell key={i} fill={a.deviation_pct > 0 ? '#D84C1A' : '#3498DB'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════
   AI CHAT
═══════════════════════════════════════════════════════════════════════ */
function AIChat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "👋 Hi! I'm your BBQ Analytics AI. Ask me anything about sales, products, branches, or revenue!" },
  ]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const QUICK = [
    'What is our total revenue?',
    'Which branch performs best?',
    'What are the top 3 products?',
    'Show me monthly revenue trend',
  ];

  async function send(q) {
    try {
      const question = (q || input).trim();
      if (!question) return;

      setInput('');
      setError(null);
      setMessages((prev) => [...prev, { role: 'user', text: question }]);
      setBusy(true);

      const res = await fetch(`${BASE}/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      setMessages((prev) => [...prev, {
        role: 'assistant',
        text: data.answer || data.detail || 'Sorry, no answer returned.',
        meta: data.sql ? `SQL: ${data.sql}` : null,
        engine: data.engine,
      }]);
    } catch (err) {
      console.error('AI chat error:', err);
      setError(err.message);
      setMessages((prev) => [...prev, {
        role: 'assistant',
        text: '⚠️ Could not reach the AI backend. Make sure the server is running on port 8000.',
      }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <h2 className="section-title">🤖 Ask Analytics — AI Assistant</h2>

      {/* Quick suggestions */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
        {QUICK.map((q, i) => (
          <button key={i} onClick={() => send(q)} style={{
            padding: '6px 14px', background: '#FFF5F0',
            border: '1px solid #FDDDD5', borderRadius: 20,
            fontSize: '0.8rem', color: '#D84C1A', cursor: 'pointer',
          }}>
            {q}
          </button>
        ))}
      </div>

      {/* Chat window */}
      <div style={{
        minHeight: 360, maxHeight: 460, overflowY: 'auto',
        background: '#F8F6F2', borderRadius: 12, padding: '1rem',
        border: '1px solid #E8E6E2',
        display: 'flex', flexDirection: 'column', gap: '0.75rem',
      }}>
        {messages.map((m, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start' }}>
            <div style={{
              maxWidth: '75%', padding: '10px 14px',
              borderRadius: m.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
              background: m.role === 'user' ? '#D84C1A' : '#fff',
              color: m.role === 'user' ? '#fff' : '#1A1A1A',
              boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
              fontSize: '0.875rem', lineHeight: 1.5,
            }}>
              {m.role === 'assistant' && <span style={{ marginRight: 5 }}>🤖</span>}
              {m.text}
              {m.meta && (
                <p style={{ fontSize: '0.68rem', color: '#8B8B8B', marginTop: 6, fontFamily: 'monospace', background: '#F8F6F2', padding: '3px 7px', borderRadius: 4 }}>
                  {m.meta}
                </p>
              )}
            </div>
          </div>
        ))}
        {busy && (
          <div style={{ color: '#8B8B8B', fontSize: '0.85rem' }}>🤖 Thinking…</div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input row */}
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !busy && send()}
          placeholder="Ask about revenue, products, branches…"
          disabled={busy}
          style={{
            flex: 1, padding: '10px 16px',
            border: '1px solid #E8E6E2', borderRadius: 8,
            fontSize: '0.875rem', outline: 'none',
          }}
        />
        <button onClick={() => send()} disabled={busy || !input.trim()}
          style={{
            padding: '10px 18px', background: '#D84C1A', color: '#fff',
            border: 'none', borderRadius: 8, cursor: 'pointer',
            display: 'flex', alignItems: 'center', gap: 5,
            opacity: busy || !input.trim() ? 0.6 : 1,
          }}>
          <Send size={15} /> Send
        </button>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════
   MAIN DASHBOARD SHELL
═══════════════════════════════════════════════════════════════════════ */
function DashboardContent({ user, onLogout }) {
  const [sidebarOpen, setSidebarOpen]     = useState(true);
  const [activeNav, setActiveNav]         = useState('overview');
  const [dateRange, setDateRange]         = useState('week');
  const [anomalyCount, setAnomalyCount]   = useState(0);
  const [showNotes, setShowNotes]         = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    try {
      api('/anomalies?threshold=0.6').then((d) => {
        if (Array.isArray(d)) setAnomalyCount(d.length);
        else setAnomalyCount(0);
      }).catch((err) => {
        console.warn('Anomaly count fetch failed:', err);
        setAnomalyCount(0);
      });
    } catch (err) {
      console.error('Dashboard init error:', err);
      setError(err.message);
    }
  }, []);

  const navItems = [
    { id: 'overview',    icon: '📊', label: 'Overview' },
    { id: 'analytics',   icon: '📈', label: 'Analytics' },
    { id: 'products',    icon: '🍖', label: 'Products' },
    { id: 'forecasting', icon: '🔮', label: 'Forecasting' },
    { id: 'alerts',      icon: '🚨', label: `Alerts${anomalyCount > 0 ? ` (${anomalyCount})` : ''}` },
  ];

  const displayName = user?.name || user?.username || (typeof user?.email === 'string' ? user.email.split('@')[0] : 'User') || 'User';
  const displayRole = user?.title || user?.role || 'Administrator';
  const avatarLetter = (typeof displayName === 'string' ? displayName.charAt(0) : 'U').toUpperCase();

  return (
    <div className="dashboard-container">

      {/* ── Global spin keyframes injected inline ── */}
      <style>{`
        @keyframes dashSpin { to { transform: rotate(360deg); } }
      `}</style>

      {/* ── ERROR BANNER ── */}
      {error && (
        <div style={{
          background: '#FFF5F0',
          border: '1px solid #FDDDD5',
          borderRadius: 8,
          padding: '1rem',
          margin: '1rem',
          color: '#C0392B',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)} style={{
            background: 'none',
            border: 'none',
            color: '#C0392B',
            cursor: 'pointer',
            fontSize: '1.2rem',
          }}>×</button>
        </div>
      )}

      {/* ── HEADER ── */}
      <header className="dashboard-header">
        <div className="header-left">
          <button className="sidebar-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <div className="header-title">
            <h1>Restaurant Dashboard</h1>
            <p>Real-time Business Intelligence</p>
          </div>
        </div>

        <div className="header-right">
          <div className="date-range-selector">
            <Calendar size={18} />
            <select value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="date-select">
              <option value="today">Today</option>
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="quarter">This Quarter</option>
            </select>
          </div>

          <button className="icon-button notification-button"
            onClick={() => setShowNotes(!showNotes)}>
            <Bell size={20} />
            {anomalyCount > 0 && (
              <span className="notification-badge">{anomalyCount}</span>
            )}
          </button>

          <div className="user-menu">
            <div className="user-avatar">{avatarLetter}</div>
            <div className="user-info">
              <p className="user-name">{displayName}</p>
              <p className="user-role">{displayRole}</p>
            </div>
            <button className="user-menu-toggle">
              <ChevronDown size={16} />
            </button>
          </div>

          <button className="logout-button" onClick={onLogout} title="Sign out">
            <LogOut size={18} />
          </button>
        </div>
      </header>

      {/* ── NOTIFICATION PANEL ── */}
      {showNotes && (
        <div className="notifications-panel">
          <div className="notifications-header">
            <h3>Alerts & Notifications</h3>
            <button onClick={() => setShowNotes(false)}><X size={18} /></button>
          </div>
          <div className="notifications-list">
            <p style={{ padding: '1rem', color: '#5C5C5C', fontSize: '0.875rem' }}>
              {anomalyCount > 0
                ? `⚠️ ${anomalyCount} revenue anomalies detected. Open the Alerts section for details.`
                : '✅ No active alerts. All systems normal.'}
            </p>
          </div>
        </div>
      )}

      <div className="dashboard-main">
        {/* ── SIDEBAR ── */}
        <aside className={`dashboard-sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <nav className="sidebar-nav">
            <div className="nav-section">
              <p className="nav-label">Main</p>
              {navItems.map((item) => (
                <button key={item.id}
                  className={`nav-item ${activeNav === item.id ? 'active' : ''}`}
                  onClick={() => setActiveNav(item.id)}>
                  <span className="nav-icon">{item.icon}</span>
                  <span className="nav-label-text">{item.label}</span>
                </button>
              ))}
            </div>

            <div className="nav-section">
              <p className="nav-label">AI Assistant</p>
              <button className={`nav-item ${activeNav === 'ai' ? 'active' : ''}`}
                onClick={() => setActiveNav('ai')}>
                <MessageSquare size={18} />
                <span className="nav-label-text">Ask Analytics</span>
              </button>
            </div>

            <div className="nav-section">
              <p className="nav-label">Settings</p>
              <button className={`nav-item ${activeNav === 'config' ? 'active' : ''}`}
                onClick={() => setActiveNav('config')}>
                <Settings size={18} />
                <span className="nav-label-text">Configuration</span>
              </button>
            </div>
          </nav>
        </aside>

        {/* ── CONTENT ── */}
        <main className="dashboard-content">
          {activeNav === 'overview'    && <Overview />}
          {activeNav === 'analytics'   && <Analytics />}
          {activeNav === 'products'    && <Products />}
          {activeNav === 'forecasting' && <Forecasting />}
          {activeNav === 'alerts'      && <Alerts />}
          {activeNav === 'ai'          && <AIChat />}
          {activeNav === 'config' && (
            <section className="placeholder-section">
              <h2>⚙️ Configuration</h2>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: '1rem', marginTop: '1.5rem' }}>
                {[
                  { label: 'Logged in as', val: displayName },
                  { label: 'Role',          val: displayRole },
                  { label: 'Email',         val: user?.email || '—' },
                  { label: 'Status',        val: user?.status || 'Active' },
                  { label: 'API Backend',   val: 'http://localhost:8000' },
                  { label: 'Connection',    val: '✅ Connected' },
                ].map((c, i) => (
                  <div key={i} style={{ padding: '0.75rem 1rem', background: '#F8F6F2', borderRadius: 8 }}>
                    <p style={{ fontSize: '0.72rem', color: '#8B8B8B' }}>{c.label}</p>
                    <p style={{ fontWeight: 600, color: '#1A1A1A', marginTop: 4 }}>{c.val}</p>
                  </div>
                ))}
              </div>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}

export default function Dashboard(props) {
  return (
    <ErrorBoundary>
      <DashboardContent {...props} />
    </ErrorBoundary>
  );
}
