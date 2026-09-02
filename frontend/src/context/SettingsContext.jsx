// Frontend Settings Context & Hooks
// frontend/src/context/SettingsContext.jsx

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import CONFIG from '../config/settings';

/**
 * Settings Context
 * Provides application-wide settings and configuration
 */
const SettingsContext = createContext(null);

/**
 * Settings Provider Component
 */
export function SettingsProvider({ children }) {
  const [settings, setSettings] = useState({
    ui: { ...CONFIG.UI },
    theme: CONFIG.UI.theme,
    autoRefresh: CONFIG.UI.autoRefreshInterval,
    sidebarCollapsed: CONFIG.UI.sidebar.collapsed,
    notifications: CONFIG.UI.maxNotifications,
  });

  const [userPreferences, setUserPreferences] = useState(() => {
    try {
      const saved = localStorage.getItem('bbq_user_preferences');
      return saved ? JSON.parse(saved) : {};
    } catch (e) {
      return {};
    }
  });

  // Save user preferences to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('bbq_user_preferences', JSON.stringify(userPreferences));
    } catch (e) {
      console.warn('Failed to save preferences:', e);
    }
  }, [userPreferences]);

  // Update individual setting
  const updateSetting = useCallback((key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  }, []);

  // Update theme
  const setTheme = useCallback((theme) => {
    setSettings(prev => ({
      ...prev,
      theme
    }));
    document.documentElement.setAttribute('data-theme', theme);
  }, []);

  // Toggle sidebar
  const toggleSidebar = useCallback(() => {
    setSettings(prev => ({
      ...prev,
      sidebarCollapsed: !prev.sidebarCollapsed
    }));
  }, []);

  // Update user preference
  const updateUserPreference = useCallback((key, value) => {
    setUserPreferences(prev => ({
      ...prev,
      [key]: value
    }));
  }, []);

  // Reset to defaults
  const resetSettings = useCallback(() => {
    setSettings({
      ui: { ...CONFIG.UI },
      theme: CONFIG.UI.theme,
      autoRefresh: CONFIG.UI.autoRefreshInterval,
      sidebarCollapsed: CONFIG.UI.sidebar.collapsed,
      notifications: CONFIG.UI.maxNotifications,
    });
  }, []);

  const value = {
    settings,
    userPreferences,
    updateSetting,
    setTheme,
    toggleSidebar,
    updateUserPreference,
    resetSettings,
    config: CONFIG,
  };

  return (
    <SettingsContext.Provider value={value}>
      {children}
    </SettingsContext.Provider>
  );
}

/**
 * Hook: useSettings
 * Access application settings and configuration
 */
export function useSettings() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within SettingsProvider');
  }
  return context;
}

/**
 * Hook: useTheme
 * Manage theme settings
 */
export function useTheme() {
  const { settings, setTheme } = useSettings();

  return {
    theme: settings.theme,
    setTheme,
    isDark: settings.theme === 'dark',
    isLight: settings.theme === 'light',
  };
}

/**
 * Hook: useSidebar
 * Manage sidebar state
 */
export function useSidebar() {
  const { settings, toggleSidebar, updateSetting } = useSettings();

  return {
    isCollapsed: settings.sidebarCollapsed,
    toggle: toggleSidebar,
    setCollapsed: (collapsed) => updateSetting('sidebarCollapsed', collapsed),
  };
}

/**
 * Hook: useAutoRefresh
 * Manage auto-refresh interval
 */
export function useAutoRefresh() {
  const { settings, updateSetting } = useSettings();

  return {
    interval: settings.autoRefresh,
    setInterval: (interval) => updateSetting('autoRefresh', interval),
    isEnabled: settings.autoRefresh > 0,
  };
}

/**
 * Hook: useAccessibility
 * Get accessibility settings
 */
export function useAccessibility() {
  const { config } = useSettings();
  const [accessibility, setAccessibility] = useState(config.ACCESSIBILITY);

  useEffect(() => {
    // Update accessibility settings on preference changes
    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

    const handleChange = () => {
      setAccessibility({
        ...accessibility,
        darkMode: darkModeQuery.matches,
        reducedMotion: reducedMotionQuery.matches,
      });
    };

    darkModeQuery.addEventListener('change', handleChange);
    reducedMotionQuery.addEventListener('change', handleChange);

    return () => {
      darkModeQuery.removeEventListener('change', handleChange);
      reducedMotionQuery.removeEventListener('change', handleChange);
    };
  }, []);

  return accessibility;
}

/**
 * Hook: useDebug
 * Access debug and development settings
 */
export function useDebug() {
  const { config } = useSettings();

  return {
    enabled: config.DEBUG.enabled,
    logLevel: config.DEBUG.logLevel,
    showMetrics: config.DEBUG.showPerformanceMetrics,
    isDevelopment: config.environment.isDevelopment,
    isProduction: config.environment.isProduction,
  };
}

/**
 * Hook: useFeatures
 * Check feature flags
 */
export function useFeatures() {
  const { config } = useSettings();

  return {
    hasAnalytics: config.FEATURES.analytics,
    hasChat: config.FEATURES.chat,
    hasModels: config.FEATURES.models,
    hasRealtime: config.FEATURES.realtime,
    hasNotifications: config.FEATURES.notifications,
  };
}

export default SettingsContext;
