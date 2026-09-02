import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area
} from 'recharts';
import {
  Send, Bell, Settings, LogOut, Menu, X, TrendingUp, AlertCircle, Zap,
  RefreshCw, Download, Filter, Eye, EyeOff, Copy, CheckCircle
} from 'lucide-react';
import SettingsPanel from './SettingsPanel';
import ErrorBoundary from './ErrorBoundary';

const COLORS = {
  primary: '#ff6b35',
  secondary: '#f7931e',
  success: '#94d82d',
  warning: '#ffa94d',
  danger: '#ff6b6b',
  background: '#1a1a1a',
  cardBg: '#2d2d2d',
  border: '#404040',
  text: '#ffffff',
  textMuted: '#b0b0b0',
};

// API Service
const apiService = {
  async fetchMetrics() {
    try {
      const response = await fetch('http://localhost:8000/api/v1/dashboard/metrics');
      if (response.ok) return await response.json();
      return null;
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
      return null;
    }
  },

  async fetchSalesTrend() {
    try {
      const response = await fetch('http://localhost:8000/api/v1/dashboard/sales-trend');
      if (response.ok) return await response.json();
      return null;
    } catch (error) {
      console.error('Failed to fetch sales trend:', error);
      return null;
    }
  },

  async fetchProductPerformance() {
    try {
      const response = await fetch('http://localhost:8000/api/v1/dashboard/products');
      if (response.ok) return await response.json();
      return null;
    } catch (error) {
      console.error('Failed to fetch products:', error);
      return null;
    }
  },

  async fetchAnomalies() {
    try {
      const response = await fetch('http://localhost:8000/api/v1/anomalies');
      if (response.ok) return await response.json();
      return null;
    } catch (error) {
      console.error('Failed to fetch anomalies:', error);
      return null;
    }
  },

  async fetchForecast() {
    try {
      const response = await fetch('http://localhost:8000/api/v1/forecast');
      if (response.ok) return await response.json();
      return null;
    } catch (error) {
      console.error('Failed to fetch forecast:', error);
      return null;
    }
  },

  async askAI(question) {
    try {
      const response = await fetch('http://localhost:8000/api/v1/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: question })
      });
      if (response.ok) return await response.json();
      return null;
    } catch (error) {
      console.error('Failed to ask AI:', error);
      return null;
    }
  }
};

// KPI Card Component
const KPICard = ({ label, value, icon, trend, loading = false }) => (
  <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg p-6 hover:border-[#ff6b35] transition-all group">
    <div className="flex justify-between items-start mb-4">
      <span className="text-3xl">{icon}</span>
      {trend && (
        <span className={`text-sm font-bold ${trend.includes('-') ? 'text-[#ff6b6b]' : 'text-[#94d82d]'}`}>
          {trend}
        </span>
      )}
    </div>
    <p className="text-[#b0b0b0] text-sm mb-2">{label}</p>
    {loading ? (
      <div className="h-8 bg-[#404040] rounded animate-pulse"></div>
    ) : (
      <p className="text-2xl font-black group-hover:text-[#ff6b35] transition-colors">{value}</p>
    )}
    <div className="mt-3 h-1 bg-[#404040] rounded-full overflow-hidden">
      <div className="h-full bg-gradient-to-r from-[#ff6b35] to-[#f7931e] w-3/4 rounded-full"></div>
    </div>
  </div>
);

// Chart Card Component
const ChartCard = ({ title, children, loading = false }) => (
  <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg p-6">
    <h3 className="text-xl font-black mb-4">{title}</h3>
    {loading ? (
      <div className="h-64 bg-[#404040] rounded animate-pulse"></div>
    ) : (
      children
    )}
  </div>
);

// Anomaly Item Component
const AnomalyItem = ({ anomaly, index }) => {
  const severityColors = {
    high: 'border-[#ff6b6b]',
    warning: 'border-[#ffa94d]',
    info: 'border-[#94d82d]',
  };

  return (
    <div
      key={index}
      className={`flex justify-between items-center p-4 bg-[#404040] rounded-lg border-l-4 ${
        severityColors[anomaly.severity] || severityColors.info
      } hover:bg-[#505050] transition-colors`}
    >
      <div className="flex-1">
        <p className="font-bold flex items-center gap-2">
          <AlertCircle size={16} />
          {anomaly.type}
        </p>
        <p className="text-sm text-[#b0b0b0]">{anomaly.date}</p>
      </div>
      <span className="font-black text-lg text-[#f7931e]">{anomaly.value}</span>
    </div>
  );
};

// Chat Message Component
const ChatMessage = ({ message }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} group`}>
      <div
        className={`max-w-xs rounded-lg p-3 ${
          message.type === 'user'
            ? 'bg-[#ff6b35] text-white rounded-br-none'
            : 'bg-[#404040] text-[#b0b0b0] rounded-bl-none'
        }`}
      >
        <p className="text-sm leading-relaxed">{message.text}</p>
        {message.type === 'ai' && (
          <button
            onClick={handleCopy}
            className="mt-2 text-xs opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 hover:text-white"
          >
            {copied ? <CheckCircle size={14} /> : <Copy size={14} />}
            {copied ? 'Copied' : 'Copy'}
          </button>
        )}
      </div>
    </div>
  );
};

// Main Dashboard Component
const BBQDashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [settingsPanelOpen, setSettingsPanelOpen] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  // State for data
  const [metrics, setMetrics] = useState({
    totalRevenue: 0,
    totalOrders: 0,
    avgOrderValue: 0,
    topProduct: 'Loading...',
    anomalyCount: 0,
  });

  const [dashboardData, setDashboardData] = useState({
    salesTrend: [],
    productPerformance: [],
    anomalies: [],
    forecast: [],
    categoryBreakdown: [],
  });

  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      text: '👋 Hello! I\'m your BBQ Restaurant AI Assistant. Ask me anything about your sales, products, or predictions. Try: "What were our best selling products?" or "Show me sales forecast"'
    }
  ]);

  const [inputValue, setInputValue] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);

  // Auto-scroll chat to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load initial data
  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [metricsData, trendsData, productsData, anomaliesData, forecastData] = await Promise.all([
        apiService.fetchMetrics(),
        apiService.fetchSalesTrend(),
        apiService.fetchProductPerformance(),
        apiService.fetchAnomalies(),
        apiService.fetchForecast(),
      ]);

      if (metricsData) setMetrics(metricsData);
      if (trendsData) setDashboardData(prev => ({ ...prev, salesTrend: trendsData }));
      if (productsData) setDashboardData(prev => ({ ...prev, productPerformance: productsData }));
      if (anomaliesData) setDashboardData(prev => ({ ...prev, anomalies: anomaliesData }));
      if (forecastData) setDashboardData(prev => ({ ...prev, forecast: forecastData }));
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = useCallback(async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      text: inputValue,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setChatLoading(true);

    try {
      const response = await apiService.askAI(inputValue);
      const aiMessage = {
        id: messages.length + 2,
        type: 'ai',
        text: response?.answer || 'I couldn\'t process that. Please try again or check if the backend is running.',
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        type: 'ai',
        text: 'Error connecting to AI. Make sure the backend server is running at http://localhost:8000',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setChatLoading(false);
    }
  }, [inputValue, messages.length]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  // Tab Views
  const renderDashboardView = () => (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          label="Total Revenue"
          value={`₨${(metrics.totalRevenue / 1000000).toFixed(2)}M`}
          icon="💰"
          trend="+12%"
          loading={loading}
        />
        <KPICard
          label="Total Orders"
          value={metrics.totalOrders}
          icon="📦"
          trend="+8%"
          loading={loading}
        />
        <KPICard
          label="Avg Order Value"
          value={`₨${metrics.avgOrderValue}`}
          icon="💵"
          trend="+4%"
          loading={loading}
        />
        <KPICard
          label="Anomalies Detected"
          value={metrics.anomalyCount}
          icon="⚠️"
          trend={`${metrics.anomalyCount} detected`}
          loading={loading}
        />
      </div>

      {/* Sales Trend */}
      <ChartCard title="📈 Sales Trend" loading={loading}>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={dashboardData.salesTrend || []}>
            <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
            <XAxis dataKey="date" stroke="#b0b0b0" />
            <YAxis stroke="#b0b0b0" />
            <Tooltip contentStyle={{ backgroundColor: '#2d2d2d', border: '1px solid #404040', borderRadius: '8px' }} />
            <Legend />
            <Line type="monotone" dataKey="revenue" stroke={COLORS.primary} strokeWidth={3} />
            <Line type="monotone" dataKey="orders" stroke={COLORS.secondary} strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Products & Forecast */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="🍖 Product Performance" loading={loading}>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={dashboardData.productPerformance || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
              <XAxis dataKey="name" stroke="#b0b0b0" angle={-45} textAnchor="end" height={80} />
              <YAxis stroke="#b0b0b0" />
              <Tooltip contentStyle={{ backgroundColor: '#2d2d2d', border: '1px solid #404040' }} />
              <Bar dataKey="revenue" fill={COLORS.primary} radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="🔮 Sales Forecast" loading={loading}>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={dashboardData.forecast || []}>
              <defs>
                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS.success} stopOpacity={0.8} />
                  <stop offset="95%" stopColor={COLORS.success} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
              <XAxis dataKey="date" stroke="#b0b0b0" />
              <YAxis stroke="#b0b0b0" />
              <Tooltip contentStyle={{ backgroundColor: '#2d2d2d', border: '1px solid #404040' }} />
              <Area type="monotone" dataKey="predicted" stroke={COLORS.success} fillOpacity={1} fill="url(#colorForecast)" />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Anomalies */}
      <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg p-6">
        <h3 className="text-xl font-black mb-4 flex items-center gap-2">
          <AlertCircle size={24} className="text-[#ff6b35]" />
          🚨 Recent Anomalies
        </h3>
        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-12 bg-[#404040] rounded animate-pulse"></div>
            ))}
          </div>
        ) : dashboardData.anomalies.length > 0 ? (
          <div className="space-y-3">
            {dashboardData.anomalies.map((anomaly, idx) => (
              <AnomalyItem key={idx} anomaly={anomaly} index={idx} />
            ))}
          </div>
        ) : (
          <p className="text-[#b0b0b0] text-center py-6">✅ No anomalies detected. All systems normal!</p>
        )}
      </div>
    </div>
  );

  const renderAnalyticsView = () => (
    <div className="space-y-6">
      <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg p-8 text-center">
        <h3 className="text-2xl font-black mb-4">📊 Advanced Analytics</h3>
        <p className="text-[#b0b0b0] mb-6">Compare periods, analyze trends, and dive deep into your data.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="bg-[#ff6b35] hover:bg-[#f7931e] text-white font-bold py-3 px-6 rounded-lg transition-colors">
            📅 Date Range
          </button>
          <button className="bg-[#404040] hover:bg-[#505050] text-white font-bold py-3 px-6 rounded-lg transition-colors">
            🔄 Compare Periods
          </button>
          <button className="bg-[#404040] hover:bg-[#505050] text-white font-bold py-3 px-6 rounded-lg transition-colors">
            📥 Export Data
          </button>
        </div>
      </div>
    </div>
  );

  const renderModelsView = () => (
    <div className="space-y-6">
      <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg p-8">
        <h3 className="text-2xl font-black mb-6">🤖 ML Model Management</h3>
        <div className="space-y-4">
          {[
            { name: 'Sales Forecasting', status: 'Active', accuracy: '89%' },
            { name: 'Anomaly Detection', status: 'Active', accuracy: '95%' },
            { name: 'Demand Prediction', status: 'Active', accuracy: '87%' },
          ].map((model, idx) => (
            <div key={idx} className="flex justify-between items-center p-4 bg-[#404040] rounded-lg">
              <div>
                <p className="font-bold">{model.name}</p>
                <p className="text-sm text-[#b0b0b0]">Status: {model.status}</p>
              </div>
              <div className="text-right">
                <p className="text-[#94d82d] font-bold text-lg">{model.accuracy}</p>
                <p className="text-sm text-[#b0b0b0]">Accuracy</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderAnomaliesView = () => (
    <div className="space-y-6">
      <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg p-6">
        <h3 className="text-2xl font-black mb-4">⚠️ Anomaly Details</h3>
        {dashboardData.anomalies.length > 0 ? (
          <div className="space-y-4">
            {dashboardData.anomalies.map((anomaly, idx) => (
              <AnomalyItem key={idx} anomaly={anomaly} index={idx} />
            ))}
          </div>
        ) : (
          <p className="text-[#b0b0b0] text-center py-8">✅ No anomalies detected</p>
        )}
      </div>
    </div>
  );

  return (
    <ErrorBoundary>
      <div className="flex h-screen bg-[#1a1a1a] text-white font-inter overflow-hidden">
        {/* Sidebar */}
        <div
          className={`${
            sidebarOpen ? 'w-64' : 'w-20'
          } bg-[#2d2d2d] border-r border-[#404040] transition-all duration-300 flex flex-col overflow-y-auto`}
        >
          {/* Logo */}
          <div className="p-6 border-b border-[#404040] flex items-center justify-between">
            {sidebarOpen && <h1 className="text-2xl font-black text-[#ff6b35]">🍖 BBQ AI</h1>}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="hover:bg-[#404040] p-2 rounded transition-colors"
            >
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: '📊' },
              { id: 'analytics', label: 'Analytics', icon: '📈' },
              { id: 'models', label: 'ML Models', icon: '🤖' },
              { id: 'anomalies', label: 'Anomalies', icon: '⚠️' },
            ].map(item => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all font-medium ${
                  activeTab === item.id
                    ? 'bg-[#ff6b35] text-white shadow-lg'
                    : 'text-[#b0b0b0] hover:bg-[#404040]'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                {sidebarOpen && <span>{item.label}</span>}
              </button>
            ))}
          </nav>

          {/* Settings & Logout */}
          {sidebarOpen && (
            <div className="p-4 border-t border-[#404040] space-y-3">
              <button
                onClick={() => setSettingsPanelOpen(true)}
                className="w-full flex items-center gap-3 text-[#b0b0b0] hover:text-[#ff6b35] transition-colors font-medium py-2"
              >
                <Settings size={20} />
                <span>Settings</span>
              </button>
              <button className="w-full flex items-center gap-3 text-[#b0b0b0] hover:text-[#ff6b35] transition-colors font-medium py-2">
                <LogOut size={20} />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Top Bar */}
          <div className="bg-[#2d2d2d] border-b border-[#404040] px-8 py-4 flex justify-between items-center">
            <h2 className="text-2xl font-black capitalize">
              {activeTab === 'dashboard' && '📊 Dashboard'}
              {activeTab === 'analytics' && '📈 Analytics'}
              {activeTab === 'models' && '🤖 ML Models'}
              {activeTab === 'anomalies' && '⚠️ Anomalies'}
            </h2>
            <div className="flex items-center gap-4">
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="hover:bg-[#404040] p-2 rounded-lg transition-colors disabled:opacity-50"
              >
                <RefreshCw size={24} className={refreshing ? 'animate-spin' : ''} />
              </button>
              <button className="relative hover:bg-[#404040] p-2 rounded-lg transition-colors">
                <Bell size={24} />
                <span className="absolute top-1 right-1 w-2 h-2 bg-[#ff6b35] rounded-full"></span>
              </button>
              <button
                onClick={() => setSettingsPanelOpen(true)}
                className="hover:bg-[#404040] p-2 rounded-lg transition-colors"
              >
                <Settings size={24} />
              </button>
            </div>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-auto flex gap-6 p-8">
            {/* Main Dashboard */}
            <div className="flex-1 overflow-y-auto pr-4">
              {activeTab === 'dashboard' && renderDashboardView()}
              {activeTab === 'analytics' && renderAnalyticsView()}
              {activeTab === 'models' && renderModelsView()}
              {activeTab === 'anomalies' && renderAnomaliesView()}
            </div>

            {/* AI Chat Sidebar */}
            <div className="w-96 bg-[#2d2d2d] border border-[#404040] rounded-lg flex flex-col overflow-hidden shadow-2xl">
              {/* Chat Header */}
              <div className="bg-gradient-to-r from-[#ff6b35] to-[#f7931e] p-4 flex items-center gap-2">
                <Zap size={24} className="animate-pulse" />
                <div>
                  <h3 className="font-black text-lg">AI Assistant</h3>
                  <p className="text-sm text-white/80">Ask about your business</p>
                </div>
              </div>

              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg) => (
                  <ChatMessage key={msg.id} message={msg} />
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-[#404040] rounded-lg rounded-bl-none p-3">
                      <div className="flex gap-2">
                        <div className="w-2 h-2 bg-[#ff6b35] rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-[#ff6b35] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-[#ff6b35] rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Chat Input */}
              <div className="border-t border-[#404040] p-4 space-y-3">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Ask me anything..."
                    className="flex-1 bg-[#404040] border border-[#505050] rounded-lg px-4 py-2 text-white placeholder-[#b0b0b0] focus:outline-none focus:border-[#ff6b35] focus:ring-1 focus:ring-[#ff6b35]"
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={chatLoading || !inputValue.trim()}
                    className="bg-[#ff6b35] hover:bg-[#f7931e] text-white p-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send size={20} />
                  </button>
                </div>
                <p className="text-xs text-[#b0b0b0] text-center">💡 Tip: Ask about sales, products, forecasts, or anomalies</p>
              </div>
            </div>
          </div>
        </div>

        {/* Settings Panel */}
        {settingsPanelOpen && (
          <SettingsPanel onClose={() => setSettingsPanelOpen(false)} />
        )}
      </div>
    </ErrorBoundary>
  );
};

export default BBQDashboard;
