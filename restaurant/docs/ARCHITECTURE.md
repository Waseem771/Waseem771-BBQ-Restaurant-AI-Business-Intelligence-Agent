# Architecture

## Boundaries

- **Frontend:** React/Vite, served by Nginx. Components use one authenticated API gateway (`src/lib/api.js`).
- **API:** FastAPI exposes `/api/v1`. The authentication middleware protects versioned business endpoints and permits only login/demo routes anonymously.
- **Data:** SQLite is the current transactional and analytics data store. The database is mounted at `/data/bbq.db` in Docker.
- **AI:** Optional provider calls stay server-side; API keys are never sent to the browser.

## Security controls

- Passwords use salted PBKDF2-SHA256 hashes.
- Tokens are signed JWTs with expiry.
- No demo password, fallback login, or localhost-only API address is in browser source.
- Production startup rejects a missing or weak JWT secret.
- CORS is an allowlist, not a wildcard.

## Growth path

For multiple restaurants or concurrent staff, migrate `app_users` and analytics data to PostgreSQL, use managed secrets, add database migrations, and put the frontend behind HTTPS with a managed certificate.
