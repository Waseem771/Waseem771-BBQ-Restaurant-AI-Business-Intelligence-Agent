# Operations runbook

## Before go-live

1. Generate and store a unique `JWT_SECRET_KEY` in the deployment secret manager.
2. Set `APP_ENV=production`, `DEMO_MODE=false`, and the exact HTTPS `CORS_ORIGINS`.
3. Back up `data/bbq.db` and confirm its mount is writable only by the backend service.
4. Create the first administrator with `backend/scripts/create_user.py`.
5. Run frontend lint/build and backend tests in CI.

## Monitoring

- Probe `GET /health` from infrastructure monitoring.
- Alert on container restart loops, 5xx rate, failed login spikes, and database mount errors.
- Rotate JWT secrets deliberately; existing sessions will be invalidated.

## Incident response

If a credential or token secret is exposed, rotate `JWT_SECRET_KEY`, reset affected passwords through the maintenance command, and review deployment logs. Keep AI provider keys only in the environment or a secret manager.
