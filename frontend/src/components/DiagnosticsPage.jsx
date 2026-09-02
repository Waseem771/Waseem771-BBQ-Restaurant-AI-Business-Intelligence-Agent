import React, { useState, useEffect } from 'react';

/**
 * Simple diagnostic component to test React setup
 * Shows if all dependencies are working correctly
 */
export default function DiagnosticsPage() {
  const [tests, setTests] = useState({
    react: { status: 'checking', time: 0 },
    recharts: { status: 'checking', time: 0 },
    lucide: { status: 'checking', time: 0 },
    api: { status: 'checking', time: 0 },
    localstorage: { status: 'checking', time: 0 },
  });

  useEffect(() => {
    // Test React
    setTests(prev => ({
      ...prev,
      react: { status: 'ok', time: Date.now() }
    }));

    // Test Recharts by importing
    try {
      import('recharts').then(() => {
        setTests(prev => ({
          ...prev,
          recharts: { status: 'ok', time: Date.now() }
        }));
      }).catch((err) => {
        setTests(prev => ({
          ...prev,
          recharts: { status: 'error', time: err.message }
        }));
      });
    } catch (err) {
      setTests(prev => ({
        ...prev,
        recharts: { status: 'error', time: err.message }
      }));
    }

    // Test Lucide
    try {
      import('lucide-react').then(() => {
        setTests(prev => ({
          ...prev,
          lucide: { status: 'ok', time: Date.now() }
        }));
      }).catch((err) => {
        setTests(prev => ({
          ...prev,
          lucide: { status: 'error', time: err.message }
        }));
      });
    } catch (err) {
      setTests(prev => ({
        ...prev,
        lucide: { status: 'error', time: err.message }
      }));
    }

    // Test API connectivity
    fetch('http://localhost:8000/api/v1/health')
      .then(res => {
        setTests(prev => ({
          ...prev,
          api: { status: 'ok', time: `${res.status}` }
        }));
      })
      .catch((err) => {
        setTests(prev => ({
          ...prev,
          api: { status: 'error', time: err.message }
        }));
      });

    // Test localStorage
    try {
      localStorage.setItem('_diagnostic_test', 'ok');
      localStorage.removeItem('_diagnostic_test');
      setTests(prev => ({
        ...prev,
        localstorage: { status: 'ok', time: Date.now() }
      }));
    } catch (err) {
      setTests(prev => ({
        ...prev,
        localstorage: { status: 'error', time: err.message }
      }));
    }
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'ok': return '#27AE60';
      case 'error': return '#E74C3C';
      default: return '#F39C12';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'ok': return '✅';
      case 'error': return '❌';
      default: return '⏳';
    }
  };

  return (
    <div style={{
      maxWidth: 600,
      margin: '4rem auto',
      padding: '2rem',
      background: '#fff',
      borderRadius: 12,
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
      fontFamily: 'Inter, sans-serif',
    }}>
      <h1 style={{ marginBottom: '1rem', color: '#1a1a1a' }}>🔍 Diagnostics</h1>
      <p style={{ color: '#5c5c5c', marginBottom: '2rem' }}>
        Testing React frontend setup and backend connectivity
      </p>

      {Object.entries(tests).map(([key, test]) => (
        <div
          key={key}
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '1rem',
            marginBottom: '0.75rem',
            background: '#f8f6f2',
            borderRadius: 8,
            borderLeft: `4px solid ${getStatusColor(test.status)}`,
          }}
        >
          <div>
            <div style={{
              fontSize: '0.875rem',
              fontWeight: 600,
              color: '#1a1a1a',
              textTransform: 'capitalize',
            }}>
              {getStatusIcon(test.status)} {key}
            </div>
            <div style={{
              fontSize: '0.75rem',
              color: '#8b8b8b',
              marginTop: 4,
            }}>
              {test.time}
            </div>
          </div>
          <div style={{
            padding: '4px 12px',
            background: getStatusColor(test.status),
            color: '#fff',
            borderRadius: 20,
            fontSize: '0.75rem',
            fontWeight: 600,
            textTransform: 'uppercase',
          }}>
            {test.status}
          </div>
        </div>
      ))}

      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        background: '#FFF5F0',
        borderRadius: 8,
        border: '1px solid #FDDDD5',
        color: '#5c5c5c',
        fontSize: '0.875rem',
        lineHeight: 1.5,
      }}>
        <p style={{ marginBottom: '0.5rem' }}>
          <strong>Next Steps:</strong>
        </p>
        <ul style={{ margin: 0, paddingLeft: '1.5rem' }}>
          <li>If all tests pass ✅, navigate to the Dashboard</li>
          <li>If API shows error ❌, ensure backend is running on port 8000</li>
          <li>If libraries fail ❌, run <code>npm install</code> in frontend folder</li>
        </ul>
      </div>
    </div>
  );
}
