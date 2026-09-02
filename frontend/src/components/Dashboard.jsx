import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  TrendingUp, TrendingDown, AlertCircle, MessageSquare,
  Settings, LogOut, Bell, Menu, X, ChevronDown,
  Calendar, Download, RefreshCw
} from 'lucide-react';
import '../styles/Dashboard.css';

export default function Dashboard({ user, onLogout }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeNav, setActiveNav] = useState('overview');
  const [dateRange, setDateRange] = useState('week');
  const [showNotifications, setShowNotifications] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  // Mock Data
  const salesData = [
    { date: 'Mon', revenue: 4200, orders: 24, avg: 175 },
    { date: 'Tue', revenue: 5100, orders: 28, avg: 182 },
    { date: 'Wed', revenue: 4900, orders: 26, avg: 188 },
    { date: 'Thu', revenue: 5800, orders: 31, avg: 187 },
    { date: 'Fri', revenue: 7200, orders: 38, avg: 189 },
    { date: 'Sat', revenue: 8900, orders: 45, avg: 198 },
    { date: 'Sun', revenue: 6400, orders: 35, avg: 183 },
  ];

  const productData = [
    { name: 'BBQ Platter', value: 2400, color: '#D84C1A' },
    { name: 'Ribs', value: 1800, color: '#F39C12' },
    { name: 'Brisket', value: 1600, color: '#E8703B' },
    { name: 'Chicken', value: 1200, color: '#27AE60' },
    { name: 'Sides', value: 900, color: '#2C3E50' },
  ];

  const forecastData = [
    { week: 'Wk 1', actual: 4200, forecast: 4100 },
    { week: 'Wk 2', actual: 5100, forecast: 5050 },
    { week: 'Wk 3', actual: 4900, forecast: 5200 },
    { week: 'Wk 4', actual: 5800, forecast: 5400 },
    { week: 'Wk 5', forecast: 6200 },
    { week: 'Wk 6', forecast: 6500 },
    { week: 'Wk 7', forecast: 6800 },
  ];

  const anomalies = [
    { id: 1, type: 'Revenue Spike', severity: 'warning', message: 'Revenue increased 23% on Saturday', time: '2 hours ago' },
    { id: 2, type: 'Product Alert', severity: 'info', message: 'BBQ Platter sales increased 15%', time: '4 hours ago' },
    { id: 3, type: 'Forecast Deviation', severity: 'info', message: 'Actual sales within 2% of forecast', time: '6 hours ago' },
  ];

  const kpis = [
    {
      label: 'Total Revenue',
      value: '₨42,600',
      change: '+12.5%',
      trend: 'up',
      icon: '💰'
    },
    {
      label: 'Total Orders',
      value: '227',
      change: '+8.2%',
      trend: 'up',
      icon: '📦'
    },
    {
      label: 'Avg Order Value',
      value: '₨188',
      change: '+3.8%',
      trend: 'up',
      icon: '📊'
    },
    {
      label: 'Top Product',
      value: 'BBQ Platter',
      change: '+18.5%',
      trend: 'up',
      icon: '🔥'
    },
  ];

  const handleRefresh = async () => {
    setRefreshing(true);
    await new Promise(resolve => setTimeout(resolve, 1200));
    setRefreshing(false);
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="dashboard-tooltip">
          <p className="tooltip-label">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-left">
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
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
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="date-select"
            >
              <option value="today">Today</option>
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="quarter">This Quarter</option>
            </select>
          </div>

          <button
            className="icon-button"
            onClick={handleRefresh}
            title="Refresh data"
          >
            <RefreshCw size={20} className={refreshing ? 'spinning' : ''} />
          </button>

          <button
            className="icon-button notification-button"
            onClick={() => setShowNotifications(!showNotifications)}
          >
            <Bell size={20} />
            <span className="notification-badge">3</span>
          </button>

          <div className="user-menu">
            <div className="user-avatar">
              {(user.name || user.username || user.email || 'U').charAt(0).toUpperCase()}
            </div>
            <div className="user-info">
              <p className="user-name">{user.name || user.username || user.email?.split('@')[0] || 'User'}</p>
              <p className="user-role">{user.title || user.role || 'Administrator'}</p>
            </div>
            <button className="user-menu-toggle">
              <ChevronDown size={16} />
            </button>
          </div>

          <button
            className="logout-button"
            onClick={onLogout}
            title="Sign out"
          >
            <LogOut size={18} />
          </button>
        </div>
      </header>

      {/* Notifications Panel */}
      {showNotifications && (
        <div className="notifications-panel">
          <div className="notifications-header">
            <h3>Alerts & Notifications</h3>
            <button onClick={() => setShowNotifications(false)}>
              <X size={18} />
            </button>
          </div>
          <div className="notifications-list">
            {anomalies.map((alert) => (
              <div key={alert.id} className={`notification-item severity-${alert.severity}`}>
                <div className="notification-icon">
                  <AlertCircle size={18} />
                </div>
                <div className="notification-content">
                  <p className="notification-type">{alert.type}</p>
                  <p className="notification-message">{alert.message}</p>
                  <p className="notification-time">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="dashboard-main">
        {/* Sidebar */}
        <aside className={`dashboard-sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <nav className="sidebar-nav">
            <div className="nav-section">
              <p className="nav-label">Main</p>
              {[
                { id: 'overview', icon: '📊', label: 'Overview' },
                { id: 'analytics', icon: '📈', label: 'Analytics' },
                { id: 'products', icon: '🍖', label: 'Products' },
                { id: 'forecasting', icon: '🔮', label: 'Forecasting' },
                { id: 'alerts', icon: '🚨', label: 'Alerts' },
              ].map((item) => (
                <button
                  key={item.id}
                  className={`nav-item ${activeNav === item.id ? 'active' : ''}`}
                  onClick={() => setActiveNav(item.id)}
                >
                  <span className="nav-icon">{item.icon}</span>
                  <span className="nav-label-text">{item.label}</span>
                </button>
              ))}
            </div>

            <div className="nav-section">
              <p className="nav-label">AI Assistant</p>
              <button className="nav-item ai-button">
                <MessageSquare size={18} />
                <span className="nav-label-text">Ask Analytics</span>
              </button>
            </div>

            <div className="nav-section">
              <p className="nav-label">Settings</p>
              {[
                { id: 'config', icon: Settings, label: 'Configuration' },
              ].map((item) => (
                <button
                  key={item.id}
                  className="nav-item"
                  onClick={() => setActiveNav(item.id)}
                >
                  <item.icon size={18} />
                  <span className="nav-label-text">{item.label}</span>
                </button>
              ))}
            </div>
          </nav>
        </aside>

        {/* Content */}
        <main className="dashboard-content">
          {activeNav === 'overview' && (
            <>
              {/* KPI Cards */}
              <section className="kpi-section">
                <h2 className="section-title">Key Performance Indicators</h2>
                <div className="kpi-grid">
                  {kpis.map((kpi, idx) => (
                    <div key={idx} className="kpi-card">
                      <div className="kpi-header">
                        <span className="kpi-icon">{kpi.icon}</span>
                        <span className={`kpi-change ${kpi.trend}`}>
                          {kpi.trend === 'up' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                          {kpi.change}
                        </span>
                      </div>
                      <p className="kpi-label">{kpi.label}</p>
                      <p className="kpi-value">{kpi.value}</p>
                    </div>
                  ))}
                </div>
              </section>

              {/* Charts Section */}
              <section className="charts-section">
                <div className="chart-card">
                  <div className="chart-header">
                    <h3>Revenue & Orders Trend</h3>
                    <button className="chart-action">
                      <Download size={16} />
                    </button>
                  </div>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={salesData}>
                      <defs>
                        <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#D84C1A" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="#D84C1A" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
                      <XAxis dataKey="date" stroke="#8B8B8B" />
                      <YAxis stroke="#8B8B8B" />
                      <Tooltip content={<CustomTooltip />} />
                      <Area
                        type="monotone"
                        dataKey="revenue"
                        stroke="#D84C1A"
                        fillOpacity={1}
                        fill="url(#colorRevenue)"
                        name="Revenue"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                <div className="chart-card">
                  <div className="chart-header">
                    <h3>Product Sales Distribution</h3>
                    <button className="chart-action">
                      <Download size={16} />
                    </button>
                  </div>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={productData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, value }) => `${name}: ${value}`}
                        outerRadius={100}
                        fill="#D84C1A"
                        dataKey="value"
                      >
                        {productData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip content={<CustomTooltip />} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </section>

              {/* Forecast Section */}
              <section className="forecast-section">
                <div className="chart-card full-width">
                  <div className="chart-header">
                    <h3>Sales Forecast vs Actual</h3>
                    <button className="chart-action">
                      <Download size={16} />
                    </button>
                  </div>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={forecastData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E8E6E2" />
                      <XAxis dataKey="week" stroke="#8B8B8B" />
                      <YAxis stroke="#8B8B8B" />
                      <Tooltip content={<CustomTooltip />} />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="actual"
                        stroke="#27AE60"
                        strokeWidth={2}
                        dot={{ fill: '#27AE60', r: 4 }}
                        activeDot={{ r: 6 }}
                        name="Actual Sales"
                      />
                      <Line
                        type="monotone"
                        dataKey="forecast"
                        stroke="#F39C12"
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        dot={{ fill: '#F39C12', r: 4 }}
                        activeDot={{ r: 6 }}
                        name="Forecast"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </section>

              {/* Anomalies Section */}
              <section className="anomalies-section">
                <h2 className="section-title">Recent Anomalies & Insights</h2>
                <div className="anomalies-list">
                  {anomalies.map((alert) => (
                    <div key={alert.id} className={`anomaly-item severity-${alert.severity}`}>
                      <div className="anomaly-icon">
                        {alert.severity === 'warning' && <AlertCircle size={20} />}
                        {alert.severity === 'info' && <AlertCircle size={20} />}
                      </div>
                      <div className="anomaly-content">
                        <p className="anomaly-type">{alert.type}</p>
                        <p className="anomaly-message">{alert.message}</p>
                      </div>
                      <p className="anomaly-time">{alert.time}</p>
                    </div>
                  ))}
                </div>
              </section>
            </>
          )}

          {activeNav === 'analytics' && (
            <section className="placeholder-section">
              <h2>Advanced Analytics</h2>
              <p>Detailed performance metrics and custom reports</p>
            </section>
          )}

          {activeNav === 'products' && (
            <section className="placeholder-section">
              <h2>Product Performance</h2>
              <p>Individual product metrics and trends</p>
            </section>
          )}

          {activeNav === 'forecasting' && (
            <section className="placeholder-section">
              <h2>AI Forecasting</h2>
              <p>Machine learning predictions and model insights</p>
            </section>
          )}

          {activeNav === 'alerts' && (
            <section className="placeholder-section">
              <h2>Alerts & Monitoring</h2>
              <p>Real-time anomaly detection and notifications</p>
            </section>
          )}

          {activeNav === 'config' && (
            <section className="placeholder-section">
              <h2>Configuration</h2>
              <p>System settings and preferences</p>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}
