import React, { useState } from 'react';
import { Eye, EyeOff, Flame, User, Lock } from 'lucide-react';
import authService from '../services/authService';
import '../styles/LoginPage.css';

export default function LoginPage({ onLoginSuccess }) {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const demoEnabled = import.meta.env.VITE_DEMO_MODE === 'true';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const sessionData = await authService.login(usernameOrEmail.trim(), password);
      authService.storeSession(sessionData, rememberMe);
      onLoginSuccess?.(sessionData);
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setIsLoading(true);
    setError('');
    try {
      const sessionData = await authService.demoLogin();
      authService.storeSession(sessionData, false);
      onLoginSuccess?.(sessionData);
    } catch (err) {
      setError(err.message || 'Demo access is unavailable.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-gradient-bg"></div>

      <div className="login-content">
        {/* Left: Form */}
        <div className="login-form-section">
          <div className="login-form-wrapper">
            <div className="login-header">
              <div className="login-logo">
                <Flame size={28} className="logo-icon" />
                <span className="logo-text">BBQ Analytics</span>
              </div>
              <p className="login-subtitle">Intelligent Restaurant Analytics</p>
            </div>

            <form onSubmit={handleSubmit} className="login-form">
              {error && (
                <div className="login-error">
                  <span className="error-icon">⚠</span>
                  {error}
                </div>
              )}

              <div className="form-group">
                <label htmlFor="usernameOrEmail" className="form-label">
                  <User size={14} style={{ display: 'inline', marginRight: 4 }} />
                  Username or Email
                </label>
                <input
                  id="usernameOrEmail"
                  type="text"
                  value={usernameOrEmail}
                  onChange={(e) => setUsernameOrEmail(e.target.value)}
                  placeholder='e.g. "waseem" or "waseem@bbqrestaurant.com"'
                  className="form-input"
                  disabled={isLoading}
                  required
                  autoComplete="username"
                />
              </div>

              <div className="form-group">
                <label htmlFor="password" className="form-label">
                  <Lock size={14} style={{ display: 'inline', marginRight: 4 }} />
                  Password
                </label>
                <div className="password-input-wrapper">
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="form-input"
                    disabled={isLoading}
                    required
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="password-toggle"
                    tabIndex="-1"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              <div className="form-options">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    disabled={isLoading}
                  />
                  <span>Remember me</span>
                </label>
              </div>

              <button
                type="submit"
                className="login-button"
                disabled={isLoading}
              >
                {isLoading ? <span className="spinner"></span> : null}
                {isLoading ? 'Signing in...' : 'Sign In'}
              </button>
            </form>

            {demoEnabled && (
              <>
                <div className="login-divider"><span>or</span></div>
                <button type="button" onClick={handleDemoLogin} className="demo-button" disabled={isLoading}>
                  Try Demo
                </button>
              </>
            )}
          </div>
        </div>

        {/* Right: Brand */}
        <div className="login-brand-section">
          <div className="brand-content">
            <div className="brand-statement">
              <h1>Ask Your Data<br />Anything.</h1>
              <p>
                Unlock actionable insights from your restaurant&apos;s performance
                with AI-powered analytics, real-time forecasting, and anomaly detection.
              </p>
            </div>

            <div className="brand-features">
              <div className="feature">
                <div className="feature-icon">📊</div>
                <div>Real-time Analytics</div>
              </div>
              <div className="feature">
                <div className="feature-icon">🤖</div>
                <div>AI-Powered Insights</div>
              </div>
              <div className="feature">
                <div className="feature-icon">⚡</div>
                <div>Instant Predictions</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
