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
import Configuration from './Configuration';
import { apiRequest } from '../lib/api';

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
const TOKEN_KEY = 'bbq_auth_token';

async function api(path) {
  try {
    let token = localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY);
    if (!token) {
      const sessionRaw = localStorage.getItem('bbq_user_session') || sessionStorage.getItem('bbq_user_session');
      if (sessionRaw) {
        try { token = JSON.parse(sessionRaw).token; } catch (e) {}
      }
    }
    const headers = { 'Accept': 'application/json' };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    const res = await fetch(`${BASE}${path}`, { headers });
    
    if (res.status === 401) {
      console.warn('Session expired. Logging out...');
      localStorage.removeItem('bbq_user_session');
      sessionStorage.removeItem('bbq_user_session');
      localStorage.removeItem(TOKEN_KEY);
      sessionStorage.removeItem(TOKEN_KEY);
      window.location.reload();
      return null;
    }
    
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
function Overview({ dateRange = 'all' }) {
  const [kpis, setKpis] = useState(null);
  const [monthly, setMonthly] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      setBusy(true);
      try {
        const [k, m, a] = await Promise.all([
          api(`/dashboard/kpis?timeframe=${dateRange}`),
          api('/sales/monthly'),
          api('/anomalies?threshold=0.6'),
        ]);

        if (k && typeof k === 'object' && !Array.isArray(k)) setKpis(k);
        if (Array.isArray(m)) setMonthly(m);
        if (Array.isArray(a)) setAnomalies(a);
      } catch (err) {
        console.error('Overview load error:', err);
        setError(err.message);
      } finally {
        setBusy(false);
      }
    };

    loadData();
  }, [dateRange]);

  if (error) {
    return (
      <div className="p-8 text-red-500 bg-red-500/10 rounded-2xl border border-red-500/20">
        <p className="flex items-center gap-2"><AlertCircle /> Error loading overview: {error}</p>
      </div>
    );
  }

  if (busy) return <Loader />;

  return (
    <div className="flex flex-col gap-6">
      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* KPI 1 */}
        <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm flex flex-col transition-transform hover:-translate-y-1 hover:shadow-md">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-[var(--color-text-secondary)] font-medium">Total Revenue</h3>
            <div className="w-8 h-8 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center">
              <DollarSign size={18} />
            </div>
          </div>
          <div className="text-3xl font-bold text-[var(--color-text-primary)]">{kpis ? fmtPKR(kpis.total_revenue) : '—'}</div>
          <div className="mt-2 text-sm text-green-500 font-medium flex items-center">
            <TrendingUp size={14} className="mr-1" /> {kpis?.gross_margin_pct}% margin
          </div>
        </div>

        {/* KPI 2 */}
        <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm flex flex-col transition-transform hover:-translate-y-1 hover:shadow-md">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-[var(--color-text-secondary)] font-medium">Total Orders</h3>
            <div className="w-8 h-8 rounded-full bg-blue-500/10 text-blue-500 flex items-center justify-center">
              <ShoppingBag size={18} />
            </div>
          </div>
          <div className="text-3xl font-bold text-[var(--color-text-primary)]">{kpis ? fmtN(kpis.total_orders) : '—'}</div>
          <div className="mt-2 text-sm text-blue-500 font-medium flex items-center">
            <TrendingUp size={14} className="mr-1" /> +8.2% vs last period
          </div>
        </div>

        {/* KPI 3 */}
        <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm flex flex-col transition-transform hover:-translate-y-1 hover:shadow-md">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-[var(--color-text-secondary)] font-medium">Avg Order Value</h3>
            <div className="w-8 h-8 rounded-full bg-orange-500/10 text-orange-500 flex items-center justify-center">
              <BarChart2 size={18} />
            </div>
          </div>
          <div className="text-3xl font-bold text-[var(--color-text-primary)]">{kpis ? fmtPKR(kpis.avg_order_value) : '—'}</div>
          <div className="mt-2 text-sm text-[var(--color-text-secondary)] font-medium flex items-center">
            <TrendingUp size={14} className="mr-1" /> +3.8% vs last period
          </div>
        </div>
      </div>

      {/* AI Insights & Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Main Chart */}
        <div className="lg:col-span-2 bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-[var(--color-text-primary)]">Revenue Trend</h2>
            <select className="bg-[var(--color-bg-primary)] border border-[var(--color-border)] text-[var(--color-text-primary)] rounded-lg px-3 py-1 text-sm outline-none">
              <option>Last 6 Months</option>
            </select>
          </div>
          <div className="relative h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthly}>
                <defs>
                  <linearGradient id="g1_new" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="var(--color-primary)" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0}   />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-divider)" vertical={false} />
                <XAxis dataKey="month" stroke="var(--color-text-tertiary)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis stroke="var(--color-text-tertiary)" tickFormatter={(v) => `₨${(v / 1000).toFixed(0)}k`} axisLine={false} tickLine={false} />
                <Tooltip content={<Tip />} />
                <Area type="monotone" dataKey="revenue" stroke="var(--color-primary)" fill="url(#g1_new)" strokeWidth={3} name="Revenue" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Alerts */}
        <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm flex flex-col h-[350px]">
          <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6 flex items-center">
            <div className="bg-[var(--color-primary)]/10 text-[var(--color-primary)] w-8 h-8 rounded-lg flex items-center justify-center mr-3">
              <AlertCircle size={18} style={{ color: 'var(--color-primary)' }} />
            </div>
            AI Anomalies
          </h2>

          <div className="flex flex-col gap-4 overflow-y-auto pr-2 custom-scrollbar flex-1">
            {anomalies.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-[var(--color-text-secondary)]">
                <CheckCircle size={32} className="text-green-500 mb-2" />
                <p>No anomalies detected</p>
              </div>
            ) : (
              anomalies.slice(0, 5).map((a, i) => (
                <div key={i} className={`p-4 rounded-xl border relative overflow-hidden shrink-0 ${a.severity === 'HIGH' ? 'bg-red-500/5 border-red-500/20' : 'bg-blue-500/5 border-blue-500/20'}`}>
                  <div className={`absolute top-0 left-0 w-1 h-full ${a.severity === 'HIGH' ? 'bg-red-500' : 'bg-blue-500'}`}></div>
                  <div className="flex justify-between items-start mb-1">
                    <span className={`font-bold text-sm ${a.severity === 'HIGH' ? 'text-red-500' : 'text-blue-500'}`}>
                      {a.direction === 'spike' ? 'Spike Detected' : 'Drop Detected'}
                    </span>
                    <span className="text-[var(--color-text-tertiary)] text-xs">{a.date}</span>
                  </div>
                  <p className="text-[var(--color-text-primary)] text-sm mt-1">
                    {a.severity === 'HIGH' ? 'Significant' : 'Minor'} deviation: {a.deviation_pct}% from expected {fmtPKR(a.expected)}.
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
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
      <div className="p-8 text-red-500 bg-red-500/10 rounded-2xl border border-red-500/20">
        <p className="flex items-center gap-2"><AlertCircle /> Error loading analytics: {error}</p>
      </div>
    );
  }

  if (busy) return <Loader />;

  const BCOL = ['var(--color-primary)', '#F39C12', '#27AE60'];
  const totalRev = branches.reduce((s, b) => s + (b.revenue || 0), 0);

  return (
    <div className="flex flex-col gap-6">
      {/* Month comparison */}
      {monthComp && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { label: 'Previous Month', sub: monthComp.previous_month, val: fmtPKR(monthComp.previous_revenue), color: 'var(--color-text-tertiary)', border: 'var(--color-text-tertiary)' },
            { label: 'Current Month',  sub: monthComp.current_month,  val: fmtPKR(monthComp.current_revenue),  color: 'var(--color-primary)', border: 'var(--color-primary)' },
            {
              label: 'Month-over-Month', sub: 'Change',
              val: `${monthComp.change_pct >= 0 ? '+' : ''}${monthComp.change_pct}%`,
              color: monthComp.change_pct >= 0 ? '#27AE60' : '#E74C3C', border: monthComp.change_pct >= 0 ? '#27AE60' : '#E74C3C'
            },
          ].map((c, i) => (
            <div key={i} className="bg-[var(--color-surface)] p-6 rounded-2xl border shadow-sm flex flex-col" style={{ borderTop: `4px solid ${c.border}`, borderColor: 'var(--color-border)' }}>
              <h3 className="text-[var(--color-text-secondary)] font-medium mb-1">{c.label}</h3>
              <p className="text-xs text-[var(--color-text-tertiary)] mb-4">{c.sub}</p>
              <div className="text-3xl font-bold" style={{ color: c.color }}>{c.val}</div>
            </div>
          ))}
        </div>
      )}

      {/* Branch bar chart + cards */}
      <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm">
        <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6 flex items-center">
           🏪 Branch Performance
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={branches} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-divider)" horizontal={false} />
                <XAxis type="number" stroke="var(--color-text-tertiary)"
                  tickFormatter={(v) => `₨${(v / 1000000).toFixed(1)}M`} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="branch_name" stroke="var(--color-text-tertiary)"
                  width={130} tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
                <Tooltip formatter={(v) => fmtPKR(v)} cursor={{fill: 'var(--color-divider)'}} />
                <Bar dataKey="revenue" name="Revenue" radius={[0, 4, 4, 0]}>
                  {branches.map((_, i) => <Cell key={i} fill={BCOL[i]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="flex flex-col gap-4">
            {branches.map((b, i) => {
              const pct = totalRev ? ((b.revenue / totalRev) * 100).toFixed(1) : 0;
              return (
                <div key={i} className="p-4 bg-[var(--color-bg-primary)] rounded-xl" style={{ borderLeft: `4px solid ${BCOL[i]}` }}>
                  <div className="flex justify-between items-center mb-2">
                    <strong className="text-[var(--color-text-primary)]">{b.branch_name}</strong>
                    <span className="font-bold" style={{ color: BCOL[i] }}>{pct}%</span>
                  </div>
                  <p className="text-xs text-[var(--color-text-secondary)]">
                    Revenue: <span className="font-medium text-[var(--color-text-primary)]">{fmtPKR(b.revenue)}</span> &nbsp;|&nbsp;
                    Orders: <span className="font-medium text-[var(--color-text-primary)]">{fmtN(b.orders)}</span> &nbsp;|&nbsp;
                    Avg: <span className="font-medium text-[var(--color-text-primary)]">{fmtPKR(b.avg_order_value)}</span>
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Daily 30-day trend */}
        <div className="lg:col-span-2 bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm">
          <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6">
            📅 Daily Revenue (30 Days)
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={daily}>
                <defs>
                  <linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#3498DB" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#3498DB" stopOpacity={0}   />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-divider)" vertical={false} />
                <XAxis dataKey="date" stroke="var(--color-text-tertiary)" tick={{ fontSize: 10 }}
                  interval={Math.floor(daily.length / 6)} axisLine={false} tickLine={false} />
                <YAxis stroke="var(--color-text-tertiary)" tickFormatter={(v) => `₨${(v / 1000).toFixed(0)}k`} axisLine={false} tickLine={false} />
                <Tooltip content={<Tip />} />
                <Area type="monotone" dataKey="revenue" stroke="#3498DB"
                  fill="url(#g2)" strokeWidth={3} name="Daily Revenue" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Weekend vs Weekday */}
        {weekend && (
          <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm flex flex-col">
            <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6">
              📆 Weekend vs Weekday
            </h2>
            <div className="grid grid-cols-2 gap-4 flex-1">
              {[
                { label: 'Weekend Avg Rev', val: fmtPKR(weekend.weekend_avg_revenue), color: 'var(--color-primary)' },
                { label: 'Weekday Avg Rev', val: fmtPKR(weekend.weekday_avg_revenue), color: '#3498DB' },
                { label: 'Weekend Orders',  val: weekend.weekend_avg_orders,           color: 'var(--color-primary)' },
                { label: 'Weekday Orders',  val: weekend.weekday_avg_orders,           color: '#3498DB' },
              ].map((item, i) => (
                <div key={i} className="p-4 bg-[var(--color-bg-primary)] rounded-xl flex flex-col items-center justify-center text-center">
                  <p className="text-xs text-[var(--color-text-secondary)] mb-2">{item.label}</p>
                  <p className="text-lg font-bold" style={{ color: item.color }}>{item.val}</p>
                </div>
              ))}
            </div>
            {weekend.orders_ratio && (
              <div className="mt-4 p-3 bg-green-500/10 text-green-600 rounded-lg text-sm text-center font-medium">
                ✅ Weekends generate {weekend.orders_ratio}× more orders
              </div>
            )}
          </div>
        )}
      </div>
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
      <div className="p-8 text-red-500 bg-red-500/10 rounded-2xl border border-red-500/20">
        <p className="flex items-center gap-2"><AlertCircle /> Error loading products: {error}</p>
      </div>
    );
  }

  if (busy) return <Loader />;

  const CAT = { 'BBQ Platters': 'var(--color-primary)', Sides: '#27AE60', Beverages: '#3498DB', Desserts: '#9B59B6' };
  const totalRev = products.reduce((s, p) => s + (p.revenue || 0), 0);

  return (
    <div className="flex flex-col gap-6">
      {/* Category charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm">
          <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6">📂 Revenue by Category</h2>
          <div className="h-[260px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={categories} cx="50%" cy="50%" outerRadius={95} innerRadius={45} stroke="var(--color-surface)" strokeWidth={3}
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
                  {categories.map((c, i) => <Cell key={i} fill={CAT[c.category] || 'var(--color-text-tertiary)'} />)}
                </Pie>
                <Tooltip formatter={(v) => fmtPKR(v)} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm">
          <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6">📦 Units Sold by Category</h2>
          <div className="h-[260px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categories}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-divider)" vertical={false} />
                <XAxis dataKey="category" stroke="var(--color-text-tertiary)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis stroke="var(--color-text-tertiary)" axisLine={false} tickLine={false} />
                <Tooltip cursor={{fill: 'var(--color-divider)'}} />
                <Bar dataKey="units_sold" name="Units Sold" radius={[4, 4, 0, 0]}>
                  {categories.map((c, i) => <Cell key={i} fill={CAT[c.category] || 'var(--color-text-tertiary)'} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Full product table */}
      <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm overflow-hidden">
        <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6">📋 All Products — Detailed Breakdown</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="bg-[var(--color-bg-primary)] border-b-2 border-[var(--color-border)] text-[var(--color-text-secondary)]">
                {['#', 'Product', 'Category', 'Revenue', 'Units Sold', 'Share', 'Avg Price'].map((h) => (
                  <th key={h} className="p-3 font-semibold whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {products.map((p, i) => {
                const share = totalRev ? ((p.revenue / totalRev) * 100).toFixed(1) : 0;
                const avgPrice = p.units_sold ? (p.revenue / p.units_sold).toFixed(0) : 0;
                return (
                  <tr key={i} className="border-b border-[var(--color-border)] hover:bg-[var(--color-bg-primary)]/50 transition-colors">
                    <td className="p-3 text-[var(--color-text-tertiary)]">{i + 1}</td>
                    <td className="p-3 font-medium text-[var(--color-text-primary)]">
                      {i === 0 && <Star size={14} className="inline mr-1 text-[#F39C12]" />}
                      {p.product_name}
                    </td>
                    <td className="p-3">
                      <span className="text-xs text-white px-2.5 py-1 rounded-full" style={{ background: CAT[p.category] || 'var(--color-text-tertiary)' }}>
                        {p.category}
                      </span>
                    </td>
                    <td className="p-3 font-bold text-[var(--color-primary)]">{fmtPKR(p.revenue)}</td>
                    <td className="p-3 text-[var(--color-text-primary)]">{fmtN(p.units_sold)}</td>
                    <td className="p-3">
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 bg-[var(--color-border)] rounded-full overflow-hidden">
                          <div className="h-full bg-[var(--color-primary)] rounded-full" style={{ width: `${share}%` }} />
                        </div>
                        <span className="text-xs text-[var(--color-text-secondary)] font-medium">{share}%</span>
                      </div>
                    </td>
                    <td className="p-3 text-[var(--color-text-secondary)] font-mono">₨{fmtN(avgPrice)}</td>
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
      <div className="p-8 text-red-500 bg-red-500/10 rounded-2xl border border-red-500/20">
        <p className="flex items-center gap-2"><AlertCircle /> Error loading forecasting: {error}</p>
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
    <div className="flex flex-col gap-6">
      {/* summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { label: 'Last Month Revenue',    val: fmtPKR(lastRev),                               icon: '📊', color: 'var(--color-primary)' },
          { label: 'Month-over-Month',       val: `${Number(growth) >= 0 ? '+' : ''}${growth}%`, icon: '📈', color: Number(growth) >= 0 ? '#27AE60' : '#E74C3C' },
          { label: 'Best Sales Day',         val: bestDay ? bestDay.date : '—',                  icon: '🏆', color: '#F39C12', sub: bestDay ? fmtPKR(bestDay.revenue) : '' },
        ].map((c, i) => (
          <div key={i} className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm flex flex-col" style={{ borderTop: `4px solid ${c.color}` }}>
            <div className="text-3xl mb-3">{c.icon}</div>
            <h3 className="text-[var(--color-text-secondary)] font-medium mb-1">{c.label}</h3>
            <div className="text-2xl font-bold" style={{ color: c.color }}>{c.val}</div>
            {c.sub && <p className="text-xs text-[var(--color-text-tertiary)] mt-1">{c.sub}</p>}
          </div>
        ))}
      </div>

      {/* 6-month forecast chart */}
      <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-bold text-[var(--color-text-primary)]">📉 Revenue Forecast — Next 6 Months</h2>
          <span className="text-xs text-[var(--color-primary)] bg-[var(--color-primary)]/10 px-3 py-1 rounded-full font-medium">
            AI Linear Trend Model
          </span>
        </div>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-divider)" vertical={false} />
              <XAxis dataKey="month" stroke="var(--color-text-tertiary)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis stroke="var(--color-text-tertiary)" tickFormatter={(v) => `₨${(v / 1000000).toFixed(1)}M`} axisLine={false} tickLine={false} />
              <Tooltip formatter={(v) => fmtPKR(v)} cursor={{stroke: 'var(--color-divider)'}} />
              <Legend />
              <Line type="monotone" dataKey="actual"   stroke="#27AE60" strokeWidth={3} dot={{ r: 4 }} name="Actual"          connectNulls={false} />
              <Line type="monotone" dataKey="forecast" stroke="var(--color-primary)" strokeWidth={3} strokeDasharray="6 3" dot={{ r: 4 }} name="Forecast" connectNulls={false} />
              <Line type="monotone" dataKey="upper"    stroke="#F39C12" strokeWidth={1}   strokeDasharray="3 3" dot={false}     name="Upper"           connectNulls={false} />
              <Line type="monotone" dataKey="lower"    stroke="#3498DB" strokeWidth={1}   strokeDasharray="3 3" dot={false}     name="Lower"           connectNulls={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* historical bar */}
      <div className="bg-[var(--color-surface)] p-6 rounded-2xl border border-[var(--color-border)] shadow-sm">
        <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-6">📊 Historical Monthly Revenue</h2>
        <div className="h-[240px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={monthly}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-divider)" vertical={false} />
              <XAxis dataKey="month" stroke="var(--color-text-tertiary)" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis stroke="var(--color-text-tertiary)" tickFormatter={(v) => `₨${(v / 1000000).toFixed(1)}M`} axisLine={false} tickLine={false} />
              <Tooltip formatter={(v) => fmtPKR(v)} cursor={{fill: 'var(--color-divider)'}} />
              <Bar dataKey="revenue" name="Revenue" fill="var(--color-primary)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
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

      const data = await apiRequest('/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

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
          {activeNav === 'overview' && <Overview dateRange={dateRange} />}
          {activeNav === 'analytics' && <Analytics dateRange={dateRange} />}
          {activeNav === 'products' && <Products dateRange={dateRange} />}
          {activeNav === 'forecasting' && <Forecasting dateRange={dateRange} />}
          {activeNav === 'alerts'      && <Alerts />}
          {activeNav === 'ai'          && <AIChat />}
          {activeNav === 'config'      && <Configuration />}
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
