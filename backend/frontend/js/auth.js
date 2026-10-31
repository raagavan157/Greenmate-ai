/**
 * GreenMate AI - Authentication & Session Manager
 */

const Auth = {
  currentUser: null,

  async init() {
    const token = API.getToken();
    if (token) {
      try {
        this.currentUser = await API.getMe();
      } catch (err) {
        console.warn('Session expired or invalid, logging out.');
        API.setToken(null);
        this.currentUser = null;
      }
    }
    this.updateUI();
    this.updateCounters();
  },

  isAuthenticated() {
    return !!this.currentUser;
  },

  async login(email, password) {
    const res = await API.login(email, password);
    API.setToken(res.access_token);
    this.currentUser = res.user;
    this.updateUI();
    this.updateCounters();
    return res.user;
  },

  async register(name, email, password) {
    const res = await API.register(name, email, password);
    API.setToken(res.access_token);
    this.currentUser = res.user;
    this.updateUI();
    this.updateCounters();
    return res.user;
  },

  logout() {
    API.setToken(null);
    this.currentUser = null;
    this.updateUI();
    this.updateCounters();
    if (window.location.pathname.includes('my-garden') || window.location.pathname.includes('profile')) {
      window.location.href = '/login.html';
    } else {
      window.location.reload();
    }
  },

  updateUI() {
    const authContainer = document.getElementById('header-auth-container');
    if (!authContainer) return;

    if (this.currentUser) {
      authContainer.innerHTML = `
        <div class="user-profile-header">
          <a href="/profile.html" style="display:flex; align-items:center; gap:8px;">
            <img src="${this.currentUser.avatar || 'https://api.dicebear.com/7.x/bottts/svg?seed=' + this.currentUser.name}" class="user-avatar-small" alt="${this.currentUser.name}">
            <span class="user-welcome-text">${this.currentUser.name}</span>
          </a>
          <button onclick="Auth.logout()" class="btn-logout-tiny" title="Sign Out">Logout</button>
        </div>
      `;
    } else {
      authContainer.innerHTML = `
        <a href="/login.html" class="top-action-link">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Login / Sign Up
        </a>
      `;
    }
  },

  async updateCounters() {
    const wishlistBadge = document.getElementById('wishlist-badge');
    const gardenBadge = document.getElementById('garden-badge');

    if (!this.isAuthenticated()) {
      if (wishlistBadge) wishlistBadge.textContent = '0';
      if (gardenBadge) gardenBadge.textContent = '0';
      return;
    }

    try {
      const [wishlist, garden] = await Promise.all([
        API.getWishlist().catch(() => []),
        API.getGarden().catch(() => [])
      ]);
      if (wishlistBadge) wishlistBadge.textContent = wishlist.length;
      if (gardenBadge) gardenBadge.textContent = garden.length;
    } catch (e) {
      // Ignore count fetch errors
    }
  },

  requireAuth(redirectUrl = null) {
    if (!this.isAuthenticated()) {
      const target = redirectUrl || window.location.pathname;
      window.location.href = `/login.html?redirect=${encodeURIComponent(target)}`;
      return false;
    }
    return true;
  }
};

window.Auth = Auth;
document.addEventListener('DOMContentLoaded', () => Auth.init());
