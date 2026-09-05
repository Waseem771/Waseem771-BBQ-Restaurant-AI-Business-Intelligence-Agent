import React, { useState, useEffect } from 'react';
import { X, Moon, Sun, Palette, Bell, Lock } from 'lucide-react';

const SettingsPanel = ({ onClose }) => {
  const [theme, setTheme] = useState('dark');
  const [notifications, setNotifications] = useState(true);
  const [refreshRate, setRefreshRate] = useState(30);
  const [colors, setColors] = useState({
    primary: '#ff6b35',
    secondary: '#f7931e',
    success: '#94d82d',
  });

  useEffect(() => {
    // Load saved settings
    const saved = localStorage.getItem('bbq-settings');
    if (saved) {
      const settings = JSON.parse(saved);
      setTheme(settings.theme || 'dark');
      setNotifications(settings.notifications !== false);
      setRefreshRate(settings.refreshRate || 30);
      setColors(settings.colors || colors);
    }
  }, []);

  const saveSettings = () => {
    const settings = { theme, notifications, refreshRate, colors };
    localStorage.setItem('bbq-settings', JSON.stringify(settings));
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg max-w-md w-full mx-4 overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-[#ff6b35] to-[#f7931e] px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-black">⚙️ Settings</h2>
          <button onClick={onClose} className="hover:bg-white/20 p-1 rounded transition-colors">
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 max-h-96 overflow-y-auto">
          {/* Theme */}
          <div>
            <label className="flex items-center gap-2 text-white font-bold mb-3">
              {theme === 'dark' ? <Moon size={20} /> : <Sun size={20} />}
              Theme
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => setTheme('dark')}
                className={`flex-1 py-2 px-4 rounded-lg font-bold transition-all ${
                  theme === 'dark'
                    ? 'bg-[#ff6b35] text-white'
                    : 'bg-[#404040] text-[#b0b0b0] hover:bg-[#505050]'
                }`}
              >
                🌙 Dark
              </button>
              <button
                onClick={() => setTheme('light')}
                className={`flex-1 py-2 px-4 rounded-lg font-bold transition-all ${
                  theme === 'light'
                    ? 'bg-[#ff6b35] text-white'
                    : 'bg-[#404040] text-[#b0b0b0] hover:bg-[#505050]'
                }`}
              >
                ☀️ Light
              </button>
            </div>
          </div>

          {/* Notifications */}
          <div>
            <label className="flex items-center gap-2 text-white font-bold mb-3">
              <Bell size={20} />
              Notifications
            </label>
            <button
              onClick={() => setNotifications(!notifications)}
              className={`w-full py-2 px-4 rounded-lg font-bold transition-all ${
                notifications
                  ? 'bg-[#94d82d] text-white'
                  : 'bg-[#404040] text-[#b0b0b0]'
              }`}
            >
              {notifications ? '🔔 Enabled' : '🔕 Disabled'}
            </button>
          </div>

          {/* Refresh Rate */}
          <div>
            <label className="flex items-center gap-2 text-white font-bold mb-3">
              ⏱️ Refresh Rate
            </label>
            <input
              type="range"
              min="10"
              max="120"
              step="10"
              value={refreshRate}
              onChange={(e) => setRefreshRate(parseInt(e.target.value))}
              className="w-full accent-[#ff6b35]"
            />
            <p className="text-sm text-[#b0b0b0] mt-2">Update every {refreshRate} seconds</p>
          </div>

          {/* Colors */}
          <div>
            <label className="flex items-center gap-2 text-white font-bold mb-3">
              <Palette size={20} />
              Primary Color
            </label>
            <input
              type="color"
              value={colors.primary}
              onChange={(e) => setColors({ ...colors, primary: e.target.value })}
              className="w-full h-10 rounded-lg cursor-pointer"
            />
          </div>

          {/* Info */}
          <div className="bg-[#404040] rounded-lg p-3">
            <p className="text-xs text-[#b0b0b0]">
              <Lock size={14} className="inline mr-2" />
              Your settings are saved locally in your browser
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-[#404040] px-6 py-4 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-2 px-4 rounded-lg text-white font-bold bg-[#505050] hover:bg-[#606060] transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={saveSettings}
            className="flex-1 py-2 px-4 rounded-lg text-white font-bold bg-[#ff6b35] hover:bg-[#f7931e] transition-colors"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;
