import React from 'react';

/**
 * Minimal Test Component
 * If this loads, React is working
 */
export default function TestComponent() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      background: '#F8F6F2',
      fontFamily: 'Inter, sans-serif',
    }}>
      <div style={{
        background: '#fff',
        padding: '3rem',
        borderRadius: 12,
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        textAlign: 'center',
        maxWidth: 400,
      }}>
        <h1 style={{ color: '#D84C1A', marginBottom: '1rem' }}>✅ React is Working!</h1>

        <p style={{ color: '#5C5C5C', marginBottom: '1.5rem', fontSize: '0.95rem' }}>
          If you see this page, React and Vite are configured correctly.
        </p>

        <div style={{
          background: '#F8F6F2',
          padding: '1rem',
          borderRadius: 8,
          marginBottom: '1.5rem',
          textAlign: 'left',
          fontSize: '0.875rem',
          color: '#5C5C5C',
        }}>
          <p><strong>Next Steps:</strong></p>
          <ol style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>
            <li>Check backend is running on port 8000</li>
            <li>Navigate to Dashboard component</li>
            <li>If Dashboard crashes, check console (F12)</li>
          </ol>
        </div>

        <button onClick={() => window.location.href = '/'} style={{
          background: '#D84C1A',
          color: '#fff',
          border: 'none',
          padding: '0.75rem 1.5rem',
          borderRadius: 6,
          cursor: 'pointer',
          fontSize: '0.95rem',
          fontWeight: 600,
        }}>
          Go to Dashboard
        </button>
      </div>

      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        background: '#FFF5F0',
        borderRadius: 8,
        border: '1px solid #FDDDD5',
        maxWidth: 600,
      }}>
        <p style={{ margin: 0, color: '#5C5C5C', fontSize: '0.85rem' }}>
          💡 <strong>Tip:</strong> Open DevTools (F12) and check the Console tab for any errors
        </p>
      </div>
    </div>
  );
}
