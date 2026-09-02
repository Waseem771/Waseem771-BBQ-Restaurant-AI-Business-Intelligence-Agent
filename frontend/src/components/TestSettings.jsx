import React, { useState } from 'react';
import SettingsPanel from './SettingsPanel';

/**
 * Test component to verify SettingsPanel renders correctly
 */
export default function TestSettings() {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div style={{ width: '100%', height: '100vh', backgroundColor: '#1a1a1a', color: '#fff' }}>
      <div style={{ padding: '20px' }}>
        <h1>Settings Panel Test</h1>
        <button
          onClick={() => setIsOpen(!isOpen)}
          style={{
            padding: '10px 20px',
            backgroundColor: '#ff6b35',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer'
          }}
        >
          {isOpen ? 'Close Settings' : 'Open Settings'}
        </button>
      </div>

      <SettingsPanel
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
      />
    </div>
  );
}
