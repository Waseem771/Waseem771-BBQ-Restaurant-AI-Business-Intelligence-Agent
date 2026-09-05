import { apiRequest, TOKEN_KEY } from '../lib/api';

const SESSION_KEY = 'bbq_user_session';

class AuthService {
  async login(username, password) {
    const data = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    return { ...data.user, token: data.access_token, expiresIn: data.expires_in };
  }

  async demoLogin() {
    const data = await apiRequest('/auth/demo', { method: 'POST' });
    return { ...data.user, token: data.access_token, expiresIn: data.expires_in };
  }

  storeSession(session, rememberMe = true) {
    const storage = rememberMe ? localStorage : sessionStorage;
    const otherStorage = rememberMe ? sessionStorage : localStorage;
    otherStorage.removeItem(SESSION_KEY);
    otherStorage.removeItem(TOKEN_KEY);
    storage.setItem(SESSION_KEY, JSON.stringify(session));
    storage.setItem(TOKEN_KEY, session.token);
  }

  logout() {
    for (const storage of [localStorage, sessionStorage]) {
      storage.removeItem(SESSION_KEY);
      storage.removeItem(TOKEN_KEY);
    }
  }

  getSession() {
    const raw = localStorage.getItem(SESSION_KEY) || sessionStorage.getItem(SESSION_KEY);
    try {
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }
}

export default new AuthService();
