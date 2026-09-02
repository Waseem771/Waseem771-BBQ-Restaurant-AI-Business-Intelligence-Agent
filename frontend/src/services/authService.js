/**
 * Authentication Service
 * Handles user session management, login/logout, and token management.
 *
 * Registered accounts:
 *   Username : waseem  |  Password: iba@123  |  Role: Administrator (Account Manager)
 *   Username : demo    |  Password: demo      |  Role: Manager
 */

// Local user registry – mirrors backend USERS_DB in app/api/routes/auth.py
const LOCAL_USERS = [
  {
    id: 'usr_001',
    username: 'waseem',
    email: 'waseem@bbqrestaurant.com',
    password: 'iba@123',
    name: 'Waseem',
    role: 'Administrator',
    title: 'Account Manager',
    status: 'Active',
    permissions: ['all', 'read', 'write', 'admin', 'dashboard_access', 'settings_access'],
  },
  {
    id: 'usr_002',
    username: 'demo',
    email: 'demo@bbqrestaurant.com',
    password: 'demo',
    name: 'Demo Manager',
    role: 'Manager',
    title: 'Restaurant Manager',
    status: 'Active',
    permissions: ['read', 'dashboard_access'],
  },
];

class AuthService {
  constructor() {
    this.sessionKey = 'bbq_user_session';
    this.tokenKey = 'bbq_auth_token';
  }

  /**
   * Login user with username/email and password.
   * First tries the backend API; falls back to local validation.
   */
  async login(usernameOrEmail, password) {
    if (!usernameOrEmail || !password) {
      throw new Error('Username/email and password are required');
    }

    // Try backend API first
    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: usernameOrEmail, password }),
      });

      if (res.ok) {
        const data = await res.json();
        const sessionData = {
          id: data.user.id,
          username: data.user.username,
          email: data.user.email,
          name: data.user.name,
          role: data.user.role,
          title: data.user.title,
          status: data.user.status,
          permissions: data.user.permissions,
          token: data.token,
          loginTime: data.loginTime,
        };
        return sessionData;
      }

      if (res.status === 401) {
        throw new Error('Invalid username/email or password');
      }
    } catch (err) {
      // If it's an auth error, re-throw it
      if (err.message === 'Invalid username/email or password') throw err;
      // Otherwise fall through to local validation (backend might be unavailable)
      console.warn('Backend auth unavailable, using local validation:', err.message);
    }

    // Local fallback validation
    const target = usernameOrEmail.trim().toLowerCase();
    const user = LOCAL_USERS.find(
      (u) => u.username.toLowerCase() === target || u.email.toLowerCase() === target
    );

    if (!user || user.password !== password) {
      throw new Error('Invalid username/email or password');
    }

    const sessionData = {
      id: user.id,
      username: user.username,
      email: user.email,
      name: user.name,
      role: user.role,
      title: user.title,
      status: user.status,
      permissions: user.permissions,
      token: `token_local_${user.id}_${Date.now()}`,
      loginTime: new Date().toISOString(),
    };

    return sessionData;
  }

  /**
   * Store session in localStorage or sessionStorage.
   */
  storeSession(sessionData, rememberMe = true) {
    const storage = rememberMe ? localStorage : sessionStorage;
    storage.setItem(this.sessionKey, JSON.stringify(sessionData));
  }

  /**
   * Logout user and clear session.
   */
  logout() {
    localStorage.removeItem(this.sessionKey);
    sessionStorage.removeItem(this.sessionKey);
    localStorage.removeItem(this.tokenKey);
  }

  /**
   * Get current session (returns null if not logged in).
   */
  getSession() {
    const raw = localStorage.getItem(this.sessionKey) || sessionStorage.getItem(this.sessionKey);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  /** Check if user is authenticated. */
  isAuthenticated() {
    return this.getSession() !== null;
  }

  /** Get display name of logged-in user. */
  getUserName() {
    return this.getSession()?.name || null;
  }

  /** Get email of logged-in user. */
  getUserEmail() {
    return this.getSession()?.email || null;
  }

  /** Get role of logged-in user. */
  getUserRole() {
    return this.getSession()?.role || null;
  }

  /** Get list of all local user accounts (for admin display). */
  getAllUsers() {
    return LOCAL_USERS.map(({ password: _pw, ...rest }) => rest);
  }
}

export default new AuthService();
