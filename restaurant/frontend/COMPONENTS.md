# BBQ Analytics - Advanced UI Components & Patterns

## Component Architecture

### Design Principles

1. **Single Responsibility** - Each component does one thing well
2. **Composability** - Components combine to form larger UIs
3. **Accessibility** - WCAG 2.1 AA standard throughout
4. **Performance** - Optimized rendering and re-renders
5. **Consistency** - Unified visual language and behavior

---

## Authentication Components

### LoginPage Component

**Purpose:** Secure user authentication with professional UX

**Props:**
```jsx
LoginPage.propTypes = {
  onLoginSuccess: PropTypes.func.isRequired, // Called with user data
}
```

**Features:**
- Email validation (RFC 5322)
- Password strength feedback
- Show/hide password toggle
- Remember me checkbox
- Demo mode for testing
- Loading states and error handling
- Responsive on all devices
- Animated transitions

**Example Usage:**
```jsx
<LoginPage 
  onLoginSuccess={(userData) => {
    // userData = { email, token, loginTime }
    setUser(userData);
    navigate('/dashboard');
  }}
/>
```

**Styling Classes:**
- `.login-container` - Main wrapper
- `.login-form-section` - Form area (left side)
- `.login-brand-section` - Brand area (right side)
- `.login-button` - Primary CTA
- `.demo-button` - Secondary action

---

## Dashboard Components

### Dashboard Component

**Purpose:** Central analytics hub with KPIs, charts, and alerts

**Props:**
```jsx
Dashboard.propTypes = {
  user: PropTypes.shape({
    email: PropTypes.string.isRequired,
    token: PropTypes.string,
  }).isRequired,
  onLogout: PropTypes.func.isRequired,
}
```

**Sub-sections:**

#### 1. Header
- Navigation toggle
- Title and subtitle
- Date range selector
- Refresh button
- Notifications indicator
- User menu
- Logout button

#### 2. Sidebar
- Navigation items (collapsible)
- Active state indicator
- AI Assistant shortcut
- Settings link
- Responsive behavior

#### 3. KPI Cards
- Metric display with icon
- Current value
- Change percentage
- Trend indicator (up/down)
- Hover effects

#### 4. Charts
- Area chart (Revenue & Orders)
- Pie chart (Product Distribution)
- Line chart (Forecast)
- Custom tooltips
- Download buttons

#### 5. Anomalies Section
- Alert cards with severity
- Message and timestamp
- Icon indicators
- Responsive grid

**Example Usage:**
```jsx
const [user, setUser] = useState(null);

<Dashboard 
  user={{ 
    email: 'manager@restaurant.com',
    token: 'jwt_token_here'
  }}
  onLogout={() => {
    setUser(null);
    // Clean up session
  }}
/>
```

---

## Form Components

### LoginForm Pattern

**Best Practices:**

1. **Validation:**
```jsx
const [errors, setErrors] = useState({});

const validate = (email, password) => {
  const newErrors = {};
  
  if (!email.includes('@')) {
    newErrors.email = 'Invalid email format';
  }
  
  if (password.length < 6) {
    newErrors.password = 'Password must be 6+ characters';
  }
  
  return newErrors;
};
```

2. **Error Display:**
```jsx
{errors.email && (
  <div className="login-error">
    <span className="error-icon">⚠</span>
    {errors.email}
  </div>
)}
```

3. **Loading States:**
```jsx
<button disabled={isLoading}>
  {isLoading ? (
    <>
      <span className="spinner"></span>
      Signing in...
    </>
  ) : (
    'Sign In'
  )}
</button>
```

---

## Chart Components

### Custom Tooltip Pattern

```jsx
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

<Tooltip content={<CustomTooltip />} />
```

### Chart Best Practices

1. **Color Consistency:**
```jsx
const chartColors = {
  revenue: '#D84C1A',      // Primary
  forecast: '#F39C12',      // Warning
  success: '#27AE60',       // Green
  danger: '#E74C3C',        // Red
};
```

2. **Responsive Sizing:**
```jsx
<ResponsiveContainer width="100%" height={300}>
  <AreaChart data={data}>
    {/* Chart config */}
  </AreaChart>
</ResponsiveContainer>
```

3. **Data Formatting:**
```jsx
// Format currency
const formatCurrency = (value) => `₨${value.toLocaleString()}`;

// Format percentage
const formatPercent = (value) => `${value.toFixed(1)}%`;

// Format date
const formatDate = (date) => new Date(date).toLocaleDateString();
```

---

## State Management Patterns

### Context API Setup

```jsx
// SettingsContext.jsx
import React, { createContext, useContext, useState } from 'react';

const SettingsContext = createContext();

export function SettingsProvider({ children }) {
  const [settings, setSettings] = useState({
    theme: 'light',
    sidebarOpen: true,
    notifications: true,
  });

  const updateSettings = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSettings }}>
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings() {
  return useContext(SettingsContext);
}
```

### Session State Pattern

```jsx
// In App.jsx
const [user, setUser] = useState(null);
const [isLoading, setIsLoading] = useState(true);

// Check session on mount
useEffect(() => {
  const session = localStorage.getItem('bbq_user_session');
  if (session) {
    setUser(JSON.parse(session));
  }
  setIsLoading(false);
}, []);

// Handle login
const handleLogin = (userData) => {
  setUser(userData);
  localStorage.setItem('bbq_user_session', JSON.stringify(userData));
};

// Handle logout
const handleLogout = () => {
  setUser(null);
  localStorage.removeItem('bbq_user_session');
};
```

---

## Styling Patterns

### CSS Custom Properties (Variables)

```css
/* Color semantic tokens */
--color-primary: #D84C1A;
--color-text-primary: #1A1A1A;
--color-bg-secondary: #FFFFFF;

/* Spacing scale */
--spacing-md: 1rem;
--spacing-lg: 1.5rem;

/* Transitions */
--transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
```

### Dark Mode Implementation

```css
/* Light theme (default) */
:root {
  --color-bg: #FFFFFF;
  --color-text: #1A1A1A;
}

/* Dark theme preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg: #1A1F2E;
    --color-text: #F5F5F5;
  }
}

/* Dark theme explicit */
:root[data-theme="dark"] {
  --color-bg: #1A1F2E;
  --color-text: #F5F5F5;
}
```

### Responsive Pattern

```css
/* Mobile-first approach */
.component {
  padding: var(--spacing-md);
  font-size: var(--text-base);
}

/* Tablet and up */
@media (min-width: 768px) {
  .component {
    padding: var(--spacing-lg);
    font-size: var(--text-lg);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .component {
    padding: var(--spacing-xl);
  }
}
```

---

## Animation Patterns

### Entrance Animations

```css
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: slideDown 200ms var(--transition-fast);
}
```

### Hover Interactions

```css
.button:hover {
  background-color: var(--color-primary-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.button:active {
  transform: translateY(0);
}
```

### Loading Spinner

```css
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

---

## Accessibility Patterns

### Keyboard Navigation

```jsx
// Button with proper focus handling
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Click me
</button>
```

### ARIA Labels

```jsx
<button aria-label="Close notification">
  <X size={20} />
</button>

<nav aria-label="Main navigation">
  {/* Navigation items */}
</nav>

<div role="alert" aria-live="polite">
  {error}
</div>
```

### Focus Management

```jsx
const buttonRef = useRef();

useEffect(() => {
  if (showModal) {
    // Focus trap
    buttonRef.current?.focus();
  }
}, [showModal]);

<button ref={buttonRef}>
  Action
</button>
```

---

## Performance Optimization

### Code Splitting

```jsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./components/Dashboard'));
const Settings = lazy(() => import('./components/Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Dashboard />
    </Suspense>
  );
}
```

### Memoization

```jsx
// Memoize expensive components
const KPICard = React.memo(({ data, icon }) => {
  return (
    <div className="kpi-card">
      {/* Content */}
    </div>
  );
});

export default KPICard;
```

### useCallback Pattern

```jsx
const handleClick = useCallback(() => {
  // Expensive operation
}, [dependency]);

// Prevents unnecessary re-renders
<ChildComponent onClick={handleClick} />
```

---

## Testing Patterns

### Component Testing

```jsx
import { render, screen } from '@testing-library/react';
import LoginPage from './LoginPage';

describe('LoginPage', () => {
  it('renders login form', () => {
    render(<LoginPage onLoginSuccess={() => {}} />);
    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
  });

  it('validates email format', () => {
    const { getByText } = render(<LoginPage onLoginSuccess={() => {}} />);
    // Test validation
  });
});
```

### Integration Testing

```jsx
it('completes login flow', async () => {
  render(<App />);
  
  const emailInput = screen.getByLabelText(/email/i);
  const passwordInput = screen.getByLabelText(/password/i);
  const submitButton = screen.getByText(/sign in/i);

  await userEvent.type(emailInput, 'test@example.com');
  await userEvent.type(passwordInput, 'password123');
  await userEvent.click(submitButton);

  expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
});
```

---

## Error Handling

### Global Error Boundary

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h1>Something went wrong</h1>
          <p>{this.state.error?.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

### API Error Handling

```jsx
async function fetchData() {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    setError(error.message);
    return null;
  }
}
```

---

## Best Practices Summary

✅ **Do:**
- Use semantic HTML
- Implement keyboard navigation
- Support dark mode
- Optimize for performance
- Test thoroughly
- Document components
- Use consistent naming
- Keep components small
- Follow accessibility standards
- Handle errors gracefully

❌ **Don't:**
- Use inline styles
- Ignore focus states
- Create mega-components
- Skip error handling
- Hardcode colors/fonts
- Block on long operations
- Ignore console warnings
- Use deprecated APIs
- Skip mobile testing
- Forget about accessibility

---

**This guide ensures your components are production-ready, accessible, and performant.**
