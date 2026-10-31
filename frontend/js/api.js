/**
 * GreenMate AI - API Service Module
 * Handles all REST API communications with the FastAPI backend.
 */

const API_BASE = (typeof window !== 'undefined' && window.GREENMATE_API_URL) 
  ? window.GREENMATE_API_URL 
  : (window.location.protocol && window.location.protocol.startsWith('http') ? '' : 'http://127.0.0.1:8000');

const API = {
  getToken() {
    return localStorage.getItem('greenmate_token');
  },

  setToken(token) {
    if (token) {
      localStorage.setItem('greenmate_token', token);
    } else {
      localStorage.removeItem('greenmate_token');
    }
  },

  getHeaders(isJson = true) {
    const headers = {};
    if (isJson) {
      headers['Content-Type'] = 'application/json';
    }
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  },

  async request(endpoint, options = {}) {
    const isFormData = options.body instanceof FormData;
    const config = {
      ...options,
      headers: {
        ...this.getHeaders(!isFormData),
        ...(options.headers || {})
      }
    };

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, config);
      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const errorMsg = data?.detail || `Error (${response.status}): ${response.statusText}`;
        throw new Error(errorMsg);
      }

      return data;
    } catch (err) {
      console.error(`API [${options.method || 'GET'} ${endpoint}] failed:`, err);
      throw err;
    }
  },

  // Auth Endpoints
  async register(name, email, password) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password })
    });
  },

  async login(email, password) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  },

  async getMe() {
    return this.request('/api/auth/me');
  },

  // Plants Endpoints
  async getPlants(params = {}) {
    const query = new URLSearchParams();
    if (params.category && params.category !== 'all') query.set('category', params.category);
    if (params.search) query.set('search', params.search);
    if (params.difficulty && params.difficulty !== 'all') query.set('difficulty', params.difficulty);
    if (params.sunlight && params.sunlight !== 'all') query.set('sunlight', params.sunlight);
    if (params.limit) query.set('limit', params.limit);
    
    const qs = query.toString() ? `?${query.toString()}` : '';
    return this.request(`/api/plants${qs}`);
  },

  async getPlantById(id) {
    return this.request(`/api/plants/${id}`);
  },

  // Wishlist Endpoints
  async getWishlist() {
    return this.request('/api/wishlist');
  },

  async addToWishlist(plantId) {
    return this.request('/api/wishlist', {
      method: 'POST',
      body: JSON.stringify({ plant_id: plantId })
    });
  },

  async removeFromWishlist(plantId) {
    return this.request(`/api/wishlist/${plantId}`, {
      method: 'DELETE'
    });
  },

  // Smart Garden Endpoints
  async getGarden() {
    return this.request('/api/garden');
  },

  async addToGarden(gardenData) {
    return this.request('/api/garden', {
      method: 'POST',
      body: JSON.stringify(gardenData)
    });
  },

  async updateGardenPlant(plantId, updateData) {
    return this.request(`/api/garden/${plantId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData)
    });
  },

  async deleteGardenPlant(plantId) {
    return this.request(`/api/garden/${plantId}`, {
      method: 'DELETE'
    });
  },

  // Care & Logs Endpoints
  async getCareSchedules() {
    return this.request('/api/care-schedules');
  },

  async setCareSchedule(scheduleData) {
    return this.request('/api/care-schedules', {
      method: 'POST',
      body: JSON.stringify(scheduleData)
    });
  },

  async recordWatering(gardenPlantId, notes = '', amountMl = 250) {
    return this.request('/api/watering-logs', {
      method: 'POST',
      body: JSON.stringify({ garden_plant_id: gardenPlantId, notes, amount_ml: amountMl })
    });
  },

  async getWateringLogs() {
    return this.request('/api/watering-logs');
  },

  async recordGrowth(growthData) {
    return this.request('/api/growth-records', {
      method: 'POST',
      body: JSON.stringify(growthData)
    });
  },

  async getGrowthRecords() {
    return this.request('/api/growth-records');
  },

  // AI Endpoints
  async identifyPlant(file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.request('/api/ai/identify', {
      method: 'POST',
      body: formData
    });
  },

  async diagnoseDisease(file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.request('/api/ai/diagnose', {
      method: 'POST',
      body: formData
    });
  },

  async getCarePlan(planRequest) {
    return this.request('/api/ai/care-plan', {
      method: 'POST',
      body: JSON.stringify(planRequest)
    });
  },

  async sendChatMessage(message, plantContext = null, history = []) {
    return this.request('/api/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ message, plant_context: plantContext, history })
    });
  },

  // Guides Endpoints
  async getGuides() {
    return this.request('/api/guides');
  },

  async getGuideById(id) {
    return this.request(`/api/guides/${id}`);
  },

  // Paytm Payment & Order Endpoints
  async initiatePaytmPayment(orderData) {
    return this.request('/api/payments/paytm/initiate', {
      method: 'POST',
      body: JSON.stringify(orderData)
    });
  },

  async verifyPaytmPayment(verifyData) {
    return this.request('/api/payments/paytm/verify', {
      method: 'POST',
      body: JSON.stringify(verifyData)
    });
  },

  async getOrderTracking(orderId) {
    return this.request(`/api/payments/orders/${orderId}`);
  },

  async getUserOrders() {
    return this.request('/api/payments/orders');
  }
};

window.API = API;
