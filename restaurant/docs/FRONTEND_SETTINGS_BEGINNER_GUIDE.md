# Frontend Settings System - Beginner's Guide

**For: Beginners learning React settings management**  
**Date: 2026-08-31**  
**Project: BBQ Restaurant AI Business Intelligence Agent**

---

## Table of Contents

1. [What is a Settings System?](#what-is-a-settings-system)
2. [The Four Core Components](#the-four-core-components)
3. [File-by-File Explanation](#file-by-file-explanation)
4. [How Data Flows](#how-data-flows)
5. [Real-World Examples](#real-world-examples)
6. [Step-by-Step Implementation](#step-by-step-implementation)

---

## What is a Settings System?

A settings system lets users customize how an application looks and behaves.

### Real-World Analogy

**Without Settings:**
```
Every user sees the same dashboard:
- Dark background (no choice)
- Standard font size (no choice)
- Data refreshes every 5 seconds (no choice)
```

**With Settings:**
```
Each user can customize:
- "I prefer light theme" ✓
- "Make font bigger for my eyes" ✓
- "Refresh data every 30 seconds" ✓
```

---

## The Four Core Components

### Component 1: Configuration File (`settings.js`)

**What it is:** A master blueprint that defines all possible settings

**Where it lives:** `frontend/src/config/settings.js`

**What it contains:**
```javascript
// Example: Color palette
COLORS = {
  primary: '#ff6b35',      // Orange (main color)
  success: '#94d82d',      // Green (success)
  error: '#ff6b6b',        // Red (errors)
}

// Example: Default UI settings
UI_CONFIG = {
  theme: 'dark',           // Dark by default
  autoRefreshInterval: 5000, // Refresh every 5 seconds
}

// Example: Feature flags
FEATURES = {
  analytics: true,         // Show analytics
  chat: true,             // Show chat
  notifications: true,    // Show alerts
}
```

**Why it matters:**
- Single source of truth
- Easy to change defaults
- Environment-based configuration (dev vs production)

---

### Component 2: Context (`SettingsContext.jsx`)

**What it is:** A React mechanism to share settings across the entire app without passing props

**Where it lives:** `frontend/src/context/SettingsContext.jsx`

**Real-World Analogy:**

Imagine a restaurant:
- **Without Context:** Each server carries the menu to every table individually
  ```
  Waiter walks to Table 1: "Here's the menu"
  Waiter walks to Table 2: "Here's the menu"
  Waiter walks to Table 3: "Here's the menu"
  (Repetitive and error-prone)
  ```

- **With Context:** There's one bulletin board. Anyone can look at it
  ```
  Bulletin Board: Menu is posted
  Table 1 looks: "Coffee is $3"
  Table 2 looks: "Coffee is $3"
  Table 3 looks: "Coffee is $3"
  (Efficient!)
  ```

**What it does:**
```javascript
SettingsContext = {
  settings: { theme: 'dark', autoRefresh: 5000, ... },
  updateSetting: function,
  setTheme: function,
  resetSettings: function,
  config: CONFIG,
}
```

**How it works:**
1. Context wraps the entire app at the root level
2. Any component can access it using hooks
3. When settings update, all components using them re-render automatically

---

### Component 3: Custom Hooks

**What they are:** Shortcuts to access specific parts of settings

**Where they live:** `frontend/src/context/SettingsContext.jsx`

**Available hooks:**

```javascript
// Get everything
useSettings()
// Returns: { settings, config, updateSetting, ... }

// Just get theme
useTheme()
// Returns: { theme, setTheme, isDark, isLight }

// Just get sidebar state
useSidebar()
// Returns: { isCollapsed, toggle, setCollapsed }

// Just get refresh interval
useAutoRefresh()
// Returns: { interval, setInterval, isEnabled }

// Get accessibility settings
useAccessibility()
// Returns: { reducedMotion, highContrast, ... }
```

**Why use hooks?**
```javascript
// BAD - verbose
const { settings } = useSettings();
const theme = settings.theme;
const isDark = settings.theme === 'dark';

// GOOD - concise
const { theme, isDark } = useTheme();
```

---

### Component 4: Settings Panel (UI Component)

**What it is:** The visual interface where users change settings

**Where it lives:** `frontend/src/components/SettingsPanel.jsx`

**What users see:**

```
┌─────────────────────────────────────┐
│  ⚙️  Settings              [X]      │
├─────────────────────────────────────┤
│ [Appearance] [Performance]...       │
├─────────────────────────────────────┤
│                                     │
│  APPEARANCE                         │
│  ☀️ Light   🌙 Dark   ⚡ Auto      │
│                                     │
│  SIDEBAR                            │
│  ☑️ Show sidebar                   │
│                                     │
│  ANIMATIONS                         │
│  ☑️ Enable animations              │
│                                     │
├─────────────────────────────────────┤
│  [Reset to Defaults]  [Done]        │
└─────────────────────────────────────┘
```

**Four tabs:**
1. **Appearance** - Theme, sidebar, animations, chart height
2. **Performance** - Refresh rate, caching, lazy loading
3. **Notifications** - Alert types, sound, duration
4. **Accessibility** - Font size, contrast, reduced motion

---

## File-by-File Explanation

### File 1: `settings.js` - The Blueprint

**Path:** `frontend/src/config/settings.js` (423 lines)

**Sections:**

```javascript
// 1. ENVIRONMENT DETECTION
const isDevelopment = import.meta.env.MODE === 'development';

// 2. API CONFIGURATION
API_CONFIG = {
  baseURL: 'http://localhost:8000/api/v1',
  wsURL: 'ws://localhost:8000/ws',
  timeout: 30000,
}

// 3. UI CONFIGURATION
UI_CONFIG = {
  theme: 'dark',
  sidebar: { collapsed: false, width: 280 },
  autoRefreshInterval: 5000,
}

// 4. FEATURE FLAGS
FEATURES = {
  analytics: true,
  chat: true,
  realtime: true,
}

// 5. COLORS
COLORS = {
  primary: '#ff6b35',    // Orange
  success: '#94d82d',    // Green
  error: '#ff6b6b',      // Red
}

// 6. TYPOGRAPHY
TYPOGRAPHY = {
  fontFamily: { default: 'Inter', mono: 'IBM Plex Mono' },
  sizes: { xs: '12px', sm: '14px', base: '16px', ... },
}
```

**Key Feature: Environment Variables**
```javascript
// Reads from .env.local
baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
//       ↑ Use .env value if exists, otherwise use default
```

---

### File 2: `SettingsContext.jsx` - The Distribution System

**Path:** `frontend/src/context/SettingsContext.jsx` (226 lines)

**How it works:**

```javascript
// Step 1: Create context (empty container)
const SettingsContext = createContext(null);

// Step 2: Create provider (fills the container)
export function SettingsProvider({ children }) {
  
  // State: holds current settings
  const [settings, setSettings] = useState({
    theme: 'dark',
    autoRefresh: 5000,
    sidebarCollapsed: false,
  });
  
  // State: holds user preferences (persisted to localStorage)
  const [userPreferences, setUserPreferences] = useState(() => {
    const saved = localStorage.getItem('bbq_user_preferences');
    return saved ? JSON.parse(saved) : {};
  });
  
  // Function: update any setting
  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };
  
  // Function: change theme
  const setTheme = (theme) => {
    setSettings(prev => ({ ...prev, theme }));
    document.documentElement.setAttribute('data-theme', theme);
  };
  
  // Return: value object with everything consumers need
  return (
    <SettingsContext.Provider value={{ settings, updateSetting, setTheme, ... }}>
      {children}
    </SettingsContext.Provider>
  );
}

// Step 3: Create hooks (shortcuts to access context)
export function useSettings() {
  const context = useContext(SettingsContext);
  if (!context) throw new Error('useSettings must be used within SettingsProvider');
  return context;
}

export function useTheme() {
  const { settings, setTheme } = useSettings();
  return {
    theme: settings.theme,
    setTheme,
    isDark: settings.theme === 'dark',
    isLight: settings.theme === 'light',
  };
}
```

**State Persistence:**
```javascript
// Save to localStorage whenever userPreferences changes
useEffect(() => {
  localStorage.setItem('bbq_user_preferences', JSON.stringify(userPreferences));
}, [userPreferences]);

// When page reloads, restore from localStorage
const [userPreferences, setUserPreferences] = useState(() => {
  const saved = localStorage.getItem('bbq_user_preferences');
  return saved ? JSON.parse(saved) : {};
});
```

---

### File 3: `App.jsx` - The Root Setup

**Path:** `frontend/src/App.jsx` (77 lines)

**What it does:**

```javascript
// Step 1: Wrap entire app with SettingsProvider
export default function App() {
  return (
    <SettingsProvider>
      <AppContent />
    </SettingsProvider>
  );
}

// Step 2: Inside, access settings
function AppContent() {
  const { config, settings, setTheme } = useSettings();
  
  // Initialize theme on page load
  useEffect(() => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('bbq_theme');
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    setTheme(theme);
  }, []);
  
  // Apply CSS variables (colors, fonts, etc.)
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty('--color-primary', config.COLORS.primary);
    root.style.setProperty('--color-success', config.COLORS.success);
    root.style.setProperty('--color-error', config.COLORS.error);
  }, [config]);
  
  return <BBQDashboard />;
}
```

**Why wrap at root level?**
- Every component below it can access settings
- No prop drilling needed
- Changes update all components automatically

---

### File 4: `SettingsPanel.jsx` - The UI

**Path:** `frontend/src/components/SettingsPanel.jsx` (421 lines)

**Component structure:**

```javascript
export default function SettingsPanel({ isOpen, onClose }) {
  // Access settings hooks
  const { settings, updateSetting, resetSettings } = useSettings();
  const { theme, setTheme } = useTheme();
  
  // Track which tab user is on
  const [activeTab, setActiveTab] = useState('appearance');
  
  // Tab 1: Appearance Settings
  const AppearanceSettings = () => (
    <div>
      <h3>Appearance</h3>
      
      {/* Theme buttons */}
      <button onClick={() => setTheme('light')}>☀️ Light</button>
      <button onClick={() => setTheme('dark')}>🌙 Dark</button>
      <button onClick={() => setTheme('auto')}>⚡ Auto</button>
      
      {/* Sidebar toggle */}
      <label>
        <input type="checkbox" onChange={() => toggle()} />
        Show sidebar
      </label>
    </div>
  );
  
  // Tab 2: Performance Settings
  const PerformanceSettings = () => (
    <div>
      <h3>Performance</h3>
      <select onChange={(e) => setInterval(e.target.value)}>
        <option value="5000">5 seconds</option>
        <option value="30000">30 seconds</option>
        <option value="60000">1 minute</option>
      </select>
    </div>
  );
  
  // ... More tabs
  
  // Render: Header + Tabs + Content + Footer
  return (
    <div className="settings-panel-overlay">
      <div className="settings-panel">
        <header>
          <h2>Settings</h2>
          <button onClick={onClose}>✕</button>
        </header>
        
        <div className="tabs">
          <button onClick={() => setActiveTab('appearance')}>Appearance</button>
          <button onClick={() => setActiveTab('performance')}>Performance</button>
          {/* ... more tabs */}
        </div>
        
        <div className="content">
          {activeTab === 'appearance' && <AppearanceSettings />}
          {activeTab === 'performance' && <PerformanceSettings />}
        </div>
        
        <footer>
          <button onClick={resetSettings}>Reset to Defaults</button>
          <button onClick={onClose}>Done</button>
        </footer>
      </div>
    </div>
  );
}
```

---

### File 5: `SettingsPanel.css` - The Styling

**Path:** `frontend/src/styles/SettingsPanel.css` (581 lines)

**Key sections:**

```css
/* Overlay (semi-transparent background) */
.settings-panel-overlay {
  position: fixed;
  background: rgba(0, 0, 0, 0.5);
  animation: fadeIn 0.3s ease-out;
}

/* Panel (the modal box) */
.settings-panel {
  width: 450px;
  background: #2d2d2d;
  animation: slideIn 0.3s ease-out;
}

/* Tabs */
.settings-tabs .tab {
  padding: 16px;
  border-bottom: 3px solid transparent;
  transition: all 0.2s ease;
}

.settings-tabs .tab.active {
  color: #ff6b35;
  border-bottom-color: #ff6b35;
}

/* Form elements */
.checkbox-label input[type="checkbox"] {
  accent-color: #ff6b35;
}

.select-group select:focus {
  border-color: #ff6b35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

/* Dark mode */
[data-theme="light"] .settings-panel {
  background: #f5f5f5;
  color: #1a1a1a;
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

---

## How Data Flows

### Scenario 1: User Changes Theme to Light

**Step 1: User clicks Light button**
```
User clicks "☀️ Light" button in SettingsPanel
```

**Step 2: Event handler calls setTheme**
```javascript
<button onClick={() => setTheme('light')}>
  ☀️ Light
</button>
```

**Step 3: setTheme updates context**
```javascript
const setTheme = (theme) => {
  setSettings(prev => ({ ...prev, theme }));
  document.documentElement.setAttribute('data-theme', theme);
};
```

**Step 4: App re-renders with new theme**
```javascript
// App.jsx watches settings.theme
useEffect(() => {
  root.style.setProperty('--color-background', config.COLORS.background);
}, [config]);
```

**Step 5: CSS changes based on data-theme**
```css
/* Default: dark theme */
body {
  background: #1a1a1a;
  color: #ffffff;
}

/* When data-theme="light" */
[data-theme="light"] body {
  background: #f5f5f5;
  color: #1a1a1a;
}
```

---

### Scenario 2: User Changes Refresh Interval

**Step 1: User selects "30 seconds"**
```
<select onChange={(e) => setInterval(parseInt(e.target.value))}>
  <option value="5000">5 seconds</option>
  <option value="30000">30 seconds</option> ← User selects
</select>
```

**Step 2: setInterval updates context**
```javascript
const { interval, setInterval } = useAutoRefresh();

setInterval(30000);
// Updates: settings.autoRefresh = 30000
```

**Step 3: Dashboard detects change and updates refresh rate**
```javascript
function Dashboard() {
  const { interval, isEnabled } = useAutoRefresh();
  
  useEffect(() => {
    if (isEnabled) {
      const timer = setInterval(() => {
        fetchDashboardData();
      }, interval); // Now refreshes every 30 seconds
      
      return () => clearInterval(timer);
    }
  }, [interval]); // Re-run when interval changes
}
```

---

### Scenario 3: User Closes Browser

**Step 1: Settings get saved to localStorage**
```javascript
useEffect(() => {
  localStorage.setItem('bbq_user_preferences', JSON.stringify(userPreferences));
}, [userPreferences]);
```

**Browser storage now contains:**
```json
{
  "bbq_user_preferences": {
    "theme": "light",
    "fontSize": "large",
    "notificationsEnabled": false,
    "autoRefresh": 30000
  }
}
```

**Step 2: User opens browser next day**
```javascript
const [userPreferences, setUserPreferences] = useState(() => {
  const saved = localStorage.getItem('bbq_user_preferences');
  return saved ? JSON.parse(saved) : {};
  // Restores saved preferences automatically
});
```

**Result:** All user's settings are preserved!

---

## Real-World Examples

### Example 1: Using Settings in a Component

**Scenario:** You're building a Chart component that respects user's animation setting

```javascript
import { useSettings } from '../context/SettingsContext';

export default function SalesChart() {
  const { settings } = useSettings();
  
  // Check if animations are enabled
  const chartOptions = {
    animation: settings.ui.charts.animationEnabled,
    animationDuration: 800,
  };
  
  return <Chart options={chartOptions} data={salesData} />;
}
```

**When user disables animations in settings:**
1. User clicks toggle in SettingsPanel
2. `updateSetting` updates `settings.ui.charts.animationEnabled` to `false`
3. SalesChart component re-renders
4. Chart re-renders without animations

---

### Example 2: Conditional Feature Display

**Scenario:** Show/hide features based on feature flags

```javascript
import { useFeatures } from '../context/SettingsContext';

export default function Dashboard() {
  const { hasChat, hasAnalytics, hasNotifications } = useFeatures();
  
  return (
    <div>
      {hasChat && <ChatPanel />}
      {hasAnalytics && <AnalyticsTab />}
      {hasNotifications && <NotificationCenter />}
    </div>
  );
}
```

---

### Example 3: Responsive to Accessibility Settings

**Scenario:** Respect user's reduced motion preference

```javascript
import { useAccessibility } from '../context/SettingsContext';

export default function Modal() {
  const { reducedMotion } = useAccessibility();
  
  return (
    <div
      style={{
        animation: reducedMotion ? 'none' : 'slideIn 0.3s ease-out',
        transition: reducedMotion ? 'none' : 'all 0.2s ease',
      }}
    >
      {/* Modal content */}
    </div>
  );
}
```

---

## Step-by-Step Implementation

### How to Add a New Setting

**Example: Add a "Show Dashboard Tooltips" setting**

#### Step 1: Add to `settings.js`

```javascript
// In UI_CONFIG section
UI_CONFIG = {
  // ... existing settings
  tooltips: {
    enabled: import.meta.env.VITE_SHOW_TOOLTIPS !== 'false',
    delay: 200,
    maxWidth: 300,
  }
}
```

#### Step 2: Add UI to SettingsPanel

```javascript
// In AppearanceSettings component
<div className="setting-item">
  <label>Tooltips</label>
  <div className="toggle-group">
    <label className="checkbox-label">
      <input
        type="checkbox"
        checked={settings.ui.tooltips.enabled}
        onChange={(e) =>
          updateSetting('ui', {
            ...settings.ui,
            tooltips: { ...settings.ui.tooltips, enabled: e.target.checked }
          })
        }
      />
      <span>Show helpful tooltips</span>
    </label>
  </div>
</div>
```

#### Step 3: Use in Component

```javascript
export default function DashboardCard({ title, value }) {
  const { settings } = useSettings();
  
  return (
    <div>
      <h3>
        {title}
        {settings.ui.tooltips.enabled && (
          <Tooltip text="This shows your daily revenue" />
        )}
      </h3>
      <p>{value}</p>
    </div>
  );
}
```

---

## Summary

| Concept | Purpose | File |
|---------|---------|------|
| **Configuration** | Define all settings | `settings.js` |
| **Context** | Distribute settings globally | `SettingsContext.jsx` |
| **Hooks** | Access settings easily | `SettingsContext.jsx` |
| **Panel** | User interface for settings | `SettingsPanel.jsx` |
| **Styling** | Visual appearance | `SettingsPanel.css` |

### Key Takeaways

✅ Settings are defined in ONE place (`settings.js`)  
✅ Settings are distributed via React Context (no prop drilling)  
✅ Custom hooks make accessing settings simple  
✅ User preferences are saved to localStorage (persist across sessions)  
✅ Settings update reactively (components re-render automatically)  
✅ Accessibility is built-in (reduced motion, high contrast, etc.)

---

## Next Steps

1. **Integrate Settings Button** - Add a settings icon to the dashboard
2. **Use Settings in Components** - Replace hardcoded values with settings
3. **Test Settings** - Change theme, refresh rate, notifications
4. **Monitor localStorage** - Check browser DevTools to see saved preferences

Would you like me to show you how to add a Settings button to the BBQ Dashboard next?
