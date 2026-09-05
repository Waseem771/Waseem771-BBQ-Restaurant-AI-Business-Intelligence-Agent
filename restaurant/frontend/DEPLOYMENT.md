# BBQ Analytics Frontend - Setup & Deployment Guide

## Part 1: Local Development Setup

### Prerequisites

- **Node.js** 16+ (verify: `node --version`)
- **npm** 8+ (verify: `npm --version`)
- **Git** (verify: `git --version`)
- Modern browser (Chrome 90+, Firefox 88+, Safari 15+)

### Quick Start (5 minutes)

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# 4. Open browser
# Visit http://localhost:5173
```

### What You'll See

- **Login Page** at startup
- Demo credentials available (click "Try Demo")
- Full dashboard with mock data
- All charts and analytics functional

### Development Scripts

```bash
npm run dev        # Start dev server (http://localhost:5173)
npm run build      # Build for production
npm run preview    # Preview production build locally
npm run lint       # Check code quality
npm run format     # Format code with Prettier
npm run type-check # Validate JSDoc types
```

---

## Part 2: Environment Configuration

### Environment Variables

Create `.env` in frontend root:

```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Debug Mode
VITE_DEBUG=true

# Feature Flags
VITE_ENABLE_DEMO=true
VITE_ENABLE_ANALYTICS=true
```

### Using Environment Variables

In components:

```jsx
const API_URL = import.meta.env.VITE_API_URL;
const DEBUG = import.meta.env.VITE_DEBUG === 'true';
```

### Example: Connecting to Backend

In `utils/api.js`:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) throw new Error('Login failed');
  return response.json();
}
```

---

## Part 3: Production Build

### Building for Production

```bash
# Build optimized bundle
npm run build

# Output generated in dist/
# Files are minified, optimized, code-split
```

### Build Output

```
dist/
├── index.html          # Main entry point
├── assets/
│   ├── index-HASH.js   # Main JavaScript bundle
│   ├── index-HASH.css  # Main CSS bundle
│   └── vendor-HASH.js  # Dependencies (Recharts, React, etc.)
└── favicon.ico         # Site icon
```

### Build Optimization

- Code splitting for lazy loading
- CSS minification
- JavaScript minification
- Asset optimization
- Source maps for debugging

---

## Part 4: Docker Deployment

### Docker Setup

Create `Dockerfile` in frontend root:

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
RUN npm install -g http-server
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["http-server", "dist", "-p", "3000", "--gzip", "-c-1"]
```

### Build & Run Docker Image

```bash
# Build image
docker build -t bbq-analytics-frontend:latest .

# Run container
docker run -p 3000:3000 bbq-analytics-frontend:latest

# Access at http://localhost:3000
```

### Docker Compose Integration

In root `docker-compose.yml`:

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://api:8000
    depends_on:
      - api
    networks:
      - bbq-network

networks:
  bbq-network:
    driver: bridge
```

---

## Part 5: Deployment Platforms

### Option A: Vercel (Recommended - Easiest)

**Advantages:**
- Zero-config deployment
- Automatic HTTPS
- Global CDN
- Free tier available
- Git integration

**Steps:**

1. Push code to GitHub
2. Go to vercel.com and sign in with GitHub
3. Click "New Project"
4. Select your repository
5. Click "Import"
6. Add environment variables:
   - `VITE_API_URL`: Your API endpoint
7. Click "Deploy"
8. Done! Live at `your-project.vercel.app`

**Environment Variables in Vercel:**
- Settings → Environment Variables
- Add `VITE_API_URL`, etc.
- Redeploy to apply changes

---

## Part 6: Netlify Deployment

### Deploy to Netlify

1. **Via Git:**
   - Connect GitHub repository to netlify.com
   - Select repository
   - Build command: `npm run build`
   - Publish directory: `dist`

2. **Via CLI:**
   ```bash
   npm install -g netlify-cli
   npm run build
   netlify deploy --prod --dir=dist
   ```

3. **Environment Variables:**
   - Settings → Build & Deploy → Environment
   - Add `VITE_API_URL`

### Netlify Configuration

Create `netlify.toml`:

```toml
[build]
command = "npm run build"
publish = "dist"

[build.environment]
NODE_VERSION = "18"

[[redirects]]
from = "/*"
to = "/index.html"
status = 200

[[headers]]
for = "/assets/*"
[headers.values]
Cache-Control = "public, max-age=31536000, immutable"
```

