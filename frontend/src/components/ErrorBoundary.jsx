import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center h-screen bg-[#1a1a1a] text-white">
          <div className="bg-[#2d2d2d] border border-[#404040] rounded-lg p-8 max-w-md text-center">
            <h2 className="text-2xl font-black text-[#ff6b35] mb-4">⚠️ Something Went Wrong</h2>
            <p className="text-[#b0b0b0] mb-6">{this.state.error?.message || 'An unexpected error occurred'}</p>
            <button
              onClick={() => window.location.reload()}
              className="bg-[#ff6b35] hover:bg-[#f7931e] text-white font-bold py-2 px-6 rounded-lg transition-colors"
            >
              🔄 Reload Dashboard
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
