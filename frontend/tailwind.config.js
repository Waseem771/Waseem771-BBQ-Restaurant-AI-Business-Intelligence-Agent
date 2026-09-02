/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fff5f0',
          100: '#ffe0d6',
          500: '#ff6b35',
          600: '#f7931e',
          700: '#e85a1a',
          900: '#1a1a1a',
        },
        dark: {
          background: '#1a1a1a',
          card: '#2d2d2d',
          border: '#404040',
          hover: '#505050',
          text: '#ffffff',
          'text-muted': '#b0b0b0',
        },
        accent: {
          success: '#94d82d',
          warning: '#ffa94d',
          error: '#ff6b6b',
          info: '#ff6b35',
        }
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
        mono: ['IBM Plex Mono', 'monospace'],
      },
      fontSize: {
        'display-lg': ['2.5rem', { lineHeight: '1.1', letterSpacing: '-0.02em', fontWeight: '900' }],
        'display-md': ['2rem', { lineHeight: '1.2', letterSpacing: '-0.02em', fontWeight: '900' }],
        'display-sm': ['1.5rem', { lineHeight: '1.3', letterSpacing: '-0.01em', fontWeight: '900' }],
        'body-lg': ['1.125rem', { lineHeight: '1.6', fontWeight: '400' }],
        'body-md': ['1rem', { lineHeight: '1.6', fontWeight: '400' }],
        'body-sm': ['0.875rem', { lineHeight: '1.5', fontWeight: '400' }],
      },
      fontWeight: {
        light: '300',
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
        extrabold: '800',
        black: '900',
      },
      spacing: {
        '0': '0',
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '6': '1.5rem',
        '8': '2rem',
        '12': '3rem',
        '16': '4rem',
        '20': '5rem',
        '24': '6rem',
      },
      borderRadius: {
        'none': '0',
        'sm': '0.375rem',
        'DEFAULT': '0.5rem',
        'md': '0.75rem',
        'lg': '1rem',
        'full': '9999px',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'DEFAULT': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'md': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        'lg': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
        'xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'glow': '0 0 20px rgba(255, 107, 53, 0.1)',
      },
      animation: {
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce': 'bounce 1s infinite',
        'slide-in': 'slideIn 0.3s ease-out',
        'fade-in': 'fadeIn 0.5s ease-out',
      },
      keyframes: {
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '.5' },
        },
        bounce: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-0.5rem)' },
        },
        slideIn: {
          'from': {
            opacity: '0',
            transform: 'translateX(-1.25rem)',
          },
          'to': {
            opacity: '1',
            transform: 'translateX(0)',
          },
        },
        fadeIn: {
          'from': { opacity: '0' },
          'to': { opacity: '1' },
        },
      },
      transitionTimingFunction: {
        'smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      backdropBlur: {
        'sm': '4px',
        'md': '12px',
        'lg': '16px',
      }
    }
  },
  plugins: [],
  corePlugins: {
    preflight: true,
  }
}
