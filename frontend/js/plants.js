/**
 * GreenMate AI - Plants Module
 * Handles plant catalog browsing, featured listings, details, and wishlist operations.
 */

const Plants = {
  activeCategory: 'all',
  currentPlants: [],

  renderCard(plant) {
    const isWished = plant.is_wishlisted;
    return `
      <div class="plant-card" data-id="${plant.id}">
        <div class="plant-card-media">
          <button class="btn-wishlist-heart ${isWished ? 'active' : ''}" 
                  onclick="Plants.toggleWishlist('${plant.id}', this, event)" 
                  title="Save to Wishlist">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="${isWished ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </button>
          <img src="${plant.image_url}" class="plant-card-img" alt="${plant.name}" loading="lazy">
        </div>
        <div class="plant-card-body">
          <h4 class="plant-name">${plant.name}</h4>
          <p class="plant-scientific">${plant.scientific_name}</p>
          
          <div class="plant-traits">
            <div class="trait-row">
              <svg class="trait-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2a10 10 0 0 1 10 10c0 5.52-4.48 10-10 10S2 17.52 2 12A10 10 0 0 1 12 2z"/>
                <path d="M12 6v6l4 2"/>
              </svg>
              <span>${plant.difficulty}</span>
            </div>
            <div class="trait-row">
              <svg class="trait-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"/>
                <line x1="12" y1="1" x2="12" y2="3"/>
                <line x1="12" y1="21" x2="12" y2="23"/>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                <line x1="1" y1="12" x2="3" y2="12"/>
                <line x1="21" y1="12" x2="23" y2="12"/>
              </svg>
              <span>${plant.sunlight}</span>
            </div>
            <div class="trait-row">
              <svg class="trait-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
              </svg>
              <span>${plant.watering}</span>
            </div>
          </div>

          <div class="plant-card-footer">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div class="plant-price">₹${plant.price ? Math.round(plant.price) : 399}</div>
              <button onclick="PaytmCheckout.open('${plant.id}', '${plant.name.replace(/'/g, "\\'")}', ${plant.price || 399}, '${plant.image_url}')" 
                      class="btn-card-pill" style="background:#002e6e; color:#ffffff; font-size:0.75rem; padding:5px 12px;" title="Fast Checkout with Paytm">
                <span style="color:#00b9f5; font-weight:800;">Paytm</span> Buy
              </button>
            </div>
            <a href="/plant-details.html?id=${plant.id}" class="btn-view-details">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"/>
                <circle cx="20" cy="21" r="1"/>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
              </svg>
              View Details
            </a>
          </div>
        </div>
      </div>
    `;
  },

  async loadFeaturedPlants(containerId = 'featured-plants-grid') {
    const container = document.getElementById(containerId);
    if (!container) return;

    try {
      container.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding: 30px;"><div class="spinner"></div><p style="margin-top:10px; color:#5e7367;">Loading botanical collection...</p></div>';
      const plants = await API.getPlants({ limit: 5 });
      this.currentPlants = plants;

      if (!plants || plants.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align:center;">No plants available at this time.</p>';
        return;
      }

      container.innerHTML = plants.map(p => this.renderCard(p)).join('');
    } catch (err) {
      container.innerHTML = `<p style="grid-column: 1/-1; color:#ef4444; text-align:center;">Failed to load featured plants: ${err.message}</p>`;
    }
  },

  async loadExploreCatalog() {
    const container = document.getElementById('explore-plants-grid');
    if (!container) return;

    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category') || 'all';
    const searchParam = urlParams.get('search') || '';

    this.activeCategory = categoryParam;

    try {
      container.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding: 40px;"><div class="spinner"></div></div>';
      const plants = await API.getPlants({ category: this.activeCategory, search: searchParam, limit: 50 });
      this.currentPlants = plants;

      const countBadge = document.getElementById('catalog-count-badge');
      if (countBadge) countBadge.textContent = `${plants.length} plants found`;

      if (!plants || plants.length === 0) {
        container.innerHTML = `
          <div style="grid-column: 1/-1; text-align:center; padding: 40px; background:#f8faf8; border-radius:16px;">
            <p style="font-size:1.1rem; font-weight:700; color:#133e29;">No matching plants discovered.</p>
            <p style="color:#5e7367; margin-top:6px;">Try adjusting your search keywords or category filters.</p>
          </div>
        `;
        return;
      }

      container.innerHTML = plants.map(p => this.renderCard(p)).join('');
    } catch (err) {
      container.innerHTML = `<p style="grid-column: 1/-1; color:#ef4444; text-align:center;">Error loading plant catalog: ${err.message}</p>`;
    }
  },

  async toggleWishlist(plantId, btnElement, event) {
    if (event) event.stopPropagation();

    if (!Auth.isAuthenticated()) {
      App.showToast('Please sign in to save plants to your wishlist', 'info');
      setTimeout(() => {
        window.location.href = `/login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
      }, 1200);
      return;
    }

    const isActive = btnElement.classList.contains('active');
    try {
      if (isActive) {
        await API.removeFromWishlist(plantId);
        btnElement.classList.remove('active');
        btnElement.querySelector('svg').setAttribute('fill', 'none');
        App.showToast('Removed from wishlist', 'info');
      } else {
        await API.addToWishlist(plantId);
        btnElement.classList.add('active');
        btnElement.querySelector('svg').setAttribute('fill', 'currentColor');
        App.showToast('Saved to your wishlist! 💚', 'success');
      }
      Auth.updateCounters();
    } catch (err) {
      App.showToast(err.message, 'error');
    }
  },

  async loadPlantDetail() {
    const urlParams = new URLSearchParams(window.location.search);
    const plantId = urlParams.get('id');
    if (!plantId) {
      window.location.href = '/explore.html';
      return;
    }

    const container = document.getElementById('plant-detail-container');
    if (!container) return;

    try {
      container.innerHTML = '<div style="text-align:center; padding: 60px;"><div class="spinner"></div></div>';
      const plant = await API.getPlantById(plantId);

      document.title = `${plant.name} Care & Profile - GreenMate AI`;

      container.innerHTML = `
        <div style="display:grid; grid-template-columns: 1fr 1.15fr; gap: 48px; align-items:flex-start;">
          <div style="position:sticky; top: 100px;">
            <div style="border-radius:24px; overflow:hidden; box-shadow:var(--shadow-md); border:1px solid var(--border-light); background:#f8faf8;">
              <img src="${plant.image_url}" alt="${plant.name}" style="width:100%; height:440px; object-fit:cover;">
            </div>
            <div style="display:flex; gap:14px; margin-top:20px;">
              <button onclick="Plants.openAddToGardenModal('${plant.id}', '${plant.name}', '${plant.image_url}', ${plant.watering_interval_days || 5})" 
                      class="btn-primary-pill" style="flex:1; justify-content:center;">
                🌱 Add to My Garden
              </button>
              <button onclick="Plants.toggleWishlist('${plant.id}', this)" 
                      class="btn-outline-pill ${plant.is_wishlisted ? 'active' : ''}" style="padding:12px 18px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="${plant.is_wishlisted ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </button>
            </div>
            <button onclick="PaytmCheckout.open('${plant.id}', '${plant.name.replace(/'/g, "\\'")}', ${plant.price || 399}, '${plant.image_url}')" 
                    class="btn-paytm-pay" style="margin-top:12px;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="#00b9f5"><rect width="24" height="24" rx="4"/></svg>
              Fast Buy with Paytm (₹${plant.price ? Math.round(plant.price) : 399})
            </button>
          </div>

          <div>
            <div style="display:inline-block; background:var(--mint-pill); color:var(--primary-forest); font-weight:700; font-size:0.85rem; padding:4px 14px; border-radius:var(--radius-full); margin-bottom:12px;">
              ${plant.category}
            </div>
            <h1 style="font-size:2.6rem; font-weight:800; color:var(--primary-forest); line-height:1.2; margin-bottom:4px;">${plant.name}</h1>
            <p style="font-size:1.1rem; font-style:italic; color:var(--text-subtle); margin-bottom:20px;">${plant.scientific_name}</p>

            <div style="font-size:1.8rem; font-weight:800; color:var(--primary-forest); margin-bottom:24px;">₹${plant.price ? Math.round(plant.price) : 399}</div>

            <p style="font-size:1.05rem; line-height:1.7; color:var(--text-muted); margin-bottom:32px;">${plant.description}</p>

            <!-- Care Grid -->
            <h3 style="font-size:1.3rem; font-weight:800; color:var(--primary-forest); margin-bottom:16px;">Core Environmental Needs</h3>
            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:16px; margin-bottom:36px;">
              <div style="background:var(--mint-bg); padding:16px; border-radius:14px; border:1px solid var(--mint-border);">
                <div style="font-weight:700; color:var(--primary-forest); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                  ☀️ Sunlight
                </div>
                <div style="font-size:0.9rem; color:var(--text-muted);">${plant.sunlight}</div>
              </div>

              <div style="background:var(--mint-bg); padding:16px; border-radius:14px; border:1px solid var(--mint-border);">
                <div style="font-weight:700; color:var(--primary-forest); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                  💧 Watering
                </div>
                <div style="font-size:0.9rem; color:var(--text-muted);">${plant.watering} (every ~${plant.watering_interval_days || 5} days)</div>
              </div>

              <div style="background:var(--mint-bg); padding:16px; border-radius:14px; border:1px solid var(--mint-border);">
                <div style="font-weight:700; color:var(--primary-forest); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                  🪴 Soil Substrate
                </div>
                <div style="font-size:0.9rem; color:var(--text-muted);">${plant.soil_type || 'Well-draining rich potting mix'}</div>
              </div>

              <div style="background:var(--mint-bg); padding:16px; border-radius:14px; border:1px solid var(--mint-border);">
                <div style="font-weight:700; color:var(--primary-forest); margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                  🌡️ Ideal Temperature
                </div>
                <div style="font-size:0.9rem; color:var(--text-muted);">${plant.temperature_range || '18°C - 30°C (65°F - 85°F)'}</div>
              </div>
            </div>

            <!-- Pro Care Instructions -->
            <h3 style="font-size:1.3rem; font-weight:800; color:var(--primary-forest); margin-bottom:16px;">Botanist Care Instructions</h3>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; margin-bottom:40px;">
              ${(plant.care_instructions || []).map(tip => `
                <li style="display:flex; align-items:flex-start; gap:10px; font-size:0.95rem; color:var(--text-main); line-height:1.5;">
                  <span style="color:var(--primary-emerald); font-weight:800;">✓</span>
                  <span>${tip}</span>
                </li>
              `).join('')}
            </ul>

            <!-- AI Personalized Care Plan Generator -->
            <div style="background:linear-gradient(135deg, #133e29 0%, #1c5539 100%); border-radius:20px; padding:28px; color:#ffffff;">
              <h4 style="font-size:1.25rem; font-weight:800; margin-bottom:8px;">Generate Custom AI Care Plan</h4>
              <p style="font-size:0.9rem; color:#d1fae5; margin-bottom:18px;">Input your specific room environment to let GreenMate AI calculate a tailored watering and fertilization schedule.</p>
              
              <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:12px; margin-bottom:16px;">
                <div>
                  <label style="font-size:0.75rem; text-transform:uppercase; color:#a7f3d0; font-weight:700;">Location</label>
                  <select id="care-env-select" class="form-control" style="background:#ffffff; color:#0f172a; margin-top:4px;">
                    <option value="indoor">Indoor (Living Room / Bedroom)</option>
                    <option value="outdoor">Outdoor (Balcony / Garden)</option>
                  </select>
                </div>
                <div>
                  <label style="font-size:0.75rem; text-transform:uppercase; color:#a7f3d0; font-weight:700;">Growth Stage</label>
                  <select id="care-stage-select" class="form-control" style="background:#ffffff; color:#0f172a; margin-top:4px;">
                    <option value="Mature">Mature Established</option>
                    <option value="Vegetative">Young Rapid Growth</option>
                    <option value="Seedling">Newly Repotted / Seedling</option>
                  </select>
                </div>
              </div>

              <button onclick="Plants.generateCustomPlan('${plant.name}')" class="btn-disease-upload" style="width:100%; justify-content:center;">
                ⚡ Calculate Custom AI Plan
              </button>

              <div id="custom-plan-result" style="display:none; margin-top:20px; background:rgba(255,255,255,0.1); border-radius:14px; padding:18px;"></div>
            </div>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div style="text-align:center; padding:50px; color:#ef4444;">Failed to load plant details: ${err.message}</div>`;
    }
  },

  async generateCustomPlan(speciesName) {
    const env = document.getElementById('care-env-select').value;
    const stage = document.getElementById('care-stage-select').value;
    const resultBox = document.getElementById('custom-plan-result');

    resultBox.style.display = 'block';
    resultBox.innerHTML = '<div style="text-align:center;"><div class="spinner"></div><p style="margin-top:8px; font-size:0.85rem;">Synthesizing botanical recommendations...</p></div>';

    try {
      const plan = await API.getCarePlan({
        plant_species: speciesName,
        environment: env,
        growth_stage: stage
      });

      resultBox.innerHTML = `
        <h5 style="color:#a7f3d0; font-weight:800; font-size:1rem; margin-bottom:10px;">Tailored Routine for ${speciesName} (${env.toUpperCase()}):</h5>
        <div style="font-size:0.85rem; line-height:1.6; color:#f1f5f9;">
          <p><strong>Weekly Schedule:</strong> ${plan.weekly_watering.frequency} on ${plan.weekly_watering.schedule_days.join(' & ')}.</p>
          <p><strong>Watering Technique:</strong> ${plan.weekly_watering.technique}</p>
          <p style="margin-top:6px;"><strong>Fertilization:</strong> ${plan.monthly_fertilizer.frequency} (${plan.monthly_fertilizer.ratio}).</p>
          <p style="margin-top:8px; font-size:0.75rem; color:#86efac;">Source: ${plan.ai_source}</p>
        </div>
      `;
    } catch (err) {
      resultBox.innerHTML = `<p style="color:#fca5a5; font-size:0.85rem;">Failed to generate plan: ${err.message}</p>`;
    }
  },

  openAddToGardenModal(plantId, plantName, imageUrl, defaultInterval) {
    if (!Auth.requireAuth()) return;

    const modal = document.getElementById('add-to-garden-modal');
    if (!modal) return;

    document.getElementById('modal-plant-id').value = plantId;
    document.getElementById('modal-plant-name').value = plantName;
    document.getElementById('modal-plant-image').value = imageUrl;
    document.getElementById('modal-plant-interval').value = defaultInterval || 5;

    modal.classList.add('active');
  }
};

window.Plants = Plants;
