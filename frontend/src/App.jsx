import React, { useState, useEffect } from 'react';
import { SettingsProvider, useSettings } from './context/SettingsContext';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import TestComponent from './components/TestComponent';
import './App.css';

/**
 * Inner App Component
 * Wrapped by SettingsProvider for access to settings context
 */
function AppContent() {
  const { config, settings, setTheme } = useSettings();
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showTest, setShowTest] = useState(false);

  // Initialize theme on mount
  useEffect(() => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('bbq_theme');
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');

    setTheme(theme);
    document.documentElement.setAttribute('data-theme', theme);
  }, [setTheme]);

  // Check for existing session
  useEffect(() => {
    const sessionData = localStorage.getItem('bbq_user_session') ||
                       sessionStorage.getItem('bbq_user_session');

    if (sessionData) {
      try {
        const parsedSession = JSON.parse(sessionData);
        setUser(parsedSession);
      } catch (err) {
        console.error('Failed to parse session:', err);
        localStorage.removeItem('bbq_user_session');
      }
    }

    setIsLoading(false);
  }, []);

  // Apply global styles based on settings
  useEffect(() => {
    const root = document.documentElement;

    // Set CSS variables for colors
    root.style.setProperty('--color-primary', config.COLORS.primary);
    root.style.setProperty('--color-secondary', config.COLORS.secondary);
    root.style.setProperty('--color-success', config.COLORS.success);
    root.style.setProperty('--color-warning', config.COLORS.warning);
    root.style.setProperty('--color-error', config.COLORS.error);
    root.style.setProperty('--color-background', config.COLORS.background);
    root.style.setProperty('--color-surface', config.COLORS.surface);
    root.style.setProperty('--color-text', config.COLORS.text);

    // Set typography
    root.style.setProperty('--font-family-default', config.TYPOGRAPHY.fontFamily.default);
    root.style.setProperty('--font-family-mono', config.TYPOGRAPHY.fontFamily.mono);

    // Set transition duration
    root.style.setProperty('--transition-duration', `${config.UI.transitionDuration}ms`);
  }, [config]);

  // Log debug info if enabled
  useEffect(() => {
    if (config.DEBUG.enabled) {
      console.log('🎨 BBQ Dashboard Initialized');
      console.log('Configuration:', config);
      console.log('Settings:', settings);
      console.log('Theme:', settings.theme);
      console.log('User:', user);
    }
  }, [config, settings, user]);

  const handleLoginSuccess = (sessionData) => {
    setUser(sessionData);
    setShowTest(false);

    if (config.DEBUG.enabled) {
      console.log('✅ User logged in:', sessionData.email);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('bbq_user_session');
    sessionStorage.removeItem('bbq_user_session');
    setUser(null);

    if (config.DEBUG.enabled) {
      console.log('🚪 User logged out');
    }
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  // Show test page if user clicks to debug
  if (showTest) {
    return (
      <div style={{ position: 'relative' }}>
        <TestComponent />
        <button
          onClick={() => setShowTest(false)}
          style={{
            position: 'fixed',
            top: '1rem',
            left: '1rem',
            padding: '0.5rem 1rem',
            background: '#D84C1A',
            color: '#fff',
            border: 'none',
            borderRadius: 6,
            cursor: 'pointer',
            zIndex: 1000,
          }}
        >
          ← Back
        </button>
      </div>
    );
  }

  return (
    <div className="app-container" data-theme={settings.theme}>
      {/* Debug button in corner */}
      <button
        onClick={() => setShowTest(!showTest)}
        style={{
          position: 'fixed',
          bottom: '1rem',
          right: '1rem',
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          background: '#D84C1A',
          color: '#fff',
          border: 'none',
          cursor: 'pointer',
          zIndex: 999,
          fontSize: '1.2rem',
          opacity: 0.6,
          hover: { opacity: 1 },
        }}
        title="Click for diagnostics"
      >
        🔧
      </button>

      {user ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

/**
 * Root App Component
 * Provides settings context to entire application
 */
export default function App() {
  return (
    <SettingsProvider>
      <AppContent />
    </SettingsProvider>
  );
}
