/**
 * GreenMate AI - Smart Garden Module
 * Manages user's personal plants, watering reminders, growth logs, and care history.
 */

const Garden = {
  plants: [],
  schedules: [],
  wateringLogs: [],
  growthRecords: [],

  async initDashboard() {
    if (!Auth.requireAuth()) return;

    await this.refreshAll();
  },

  async refreshAll() {
    try {
      const [plants, schedules, logs, records] = await Promise.all([
        API.getGarden(),
        API.getCareSchedules().catch(() => []),
        API.getWateringLogs().catch(() => []),
        API.getGrowthRecords().catch(() => [])
      ]);

      this.plants = plants;
      this.schedules = schedules;
      this.wateringLogs = logs;
      this.growthRecords = records;

      this.renderPlantsGrid();
      this.renderWateringReminders();
      this.renderHealthSummary();
      this.renderGrowthSection();
      this.renderCareHistory();
      Auth.updateCounters();
    } catch (err) {
      console.error('Error refreshing garden dashboard:', err);
      App.showToast('Could not load garden records: ' + err.message, 'error');
    }
  },

  renderPlantsGrid() {
    const container = document.getElementById('my-garden-plants-grid');
    if (!container) return;

    if (this.plants.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align:center; padding: 48px; background:#f8faf8; border-radius:18px; border:2px dashed #d4ecdc;">
          <div style="font-size:2.4rem; margin-bottom:12px;">🪴</div>
          <h4 style="font-size:1.25rem; font-weight:800; color:#133e29; margin-bottom:6px;">Your Garden is Empty</h4>
          <p style="color:#5e7367; max-width:440px; margin:0 auto 20px;">Add your first botanical companion from our catalog or identify one using the AI camera.</p>
          <div style="display:flex; justify-content:center; gap:12px;">
            <a href="/explore.html" class="btn-primary-pill">Explore Plants</a>
            <button onclick="Garden.openCustomAddModal()" class="btn-outline-pill">+ Add Custom Plant</button>
          </div>
        </div>
      `;
      return;
    }

    container.innerHTML = this.plants.map(p => `
      <div class="plant-card" style="border-radius:16px;">
        <div class="plant-card-media" style="height:180px;">
          <img src="${p.image_url || 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=600&q=80'}" class="plant-card-img" alt="${p.name}">
          <span style="position:absolute; bottom:10px; left:10px; background:rgba(255,255,255,0.92); backdrop-filter:blur(4px); padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; color:#133e29;">
            📍 ${p.location || 'Living Room'}
          </span>
        </div>
        <div class="plant-card-body" style="padding:16px;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <h4 style="font-size:1.05rem; font-weight:800; color:#133e29;">${p.nickname ? `"${p.nickname}"` : p.name}</h4>
              <p style="font-size:0.75rem; color:#87998e;">${p.name}</p>
            </div>
            <span style="font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:10px; background:${p.health_status === 'Healthy' ? '#dcfce7; color:#166534;' : '#fef9c3; color:#854d0e;'}">
              ${p.health_status}
            </span>
          </div>

          <div style="margin:14px 0 16px; font-size:0.8rem; color:#5e7367; display:flex; flex-direction:column; gap:6px;">
            <div>💧 Waters every: <strong>${p.watering_interval_days} days</strong></div>
            <div>📅 Next drink: <strong>${p.next_watering_at ? new Date(p.next_watering_at).toLocaleDateString() : 'Today'}</strong></div>
          </div>

          <div style="display:flex; gap:8px;">
            <button onclick="Garden.quickWater('${p.id}', '${p.name}')" class="btn-primary-solid" style="flex:1; font-size:0.775rem; padding:8px 10px;">
              💧 Water Now
            </button>
            <button onclick="Garden.openEditModal('${p.id}')" class="btn-secondary" style="font-size:0.775rem; padding:8px 12px;" title="Edit details">
              ✏️
            </button>
            <button onclick="Garden.deletePlant('${p.id}', '${p.name}')" class="btn-danger-outline" style="padding:6px 10px;" title="Delete plant">
              🗑️
            </button>
          </div>
        </div>
      </div>
    `).join('');
  },

  renderWateringReminders() {
    const container = document.getElementById('watering-reminders-container');
    if (!container) return;

    if (this.schedules.length === 0) {
      container.innerHTML = '<p style="color:#5e7367; font-size:0.9rem;">No watering reminders scheduled. Add plants to see active routines.</p>';
      return;
    }

    container.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:12px;">
        ${this.schedules.map(s => `
          <div style="display:flex; align-items:center; justify-content:space-between; padding:12px 16px; background:#f8faf8; border-radius:14px; border:1px solid ${s.is_overdue ? '#fecaca' : 'var(--border-light)'};">
            <div style="display:flex; align-items:center; gap:12px;">
              <img src="${s.plant_image || 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=200&q=80'}" style="width:40px; height:40px; border-radius:10px; object-fit:cover;">
              <div>
                <h5 style="font-size:0.9rem; font-weight:800; color:#133e29;">${s.plant_name}</h5>
                <span style="font-size:0.75rem; color:${s.is_overdue ? '#dc2626' : '#5e7367'}; font-weight:${s.is_overdue ? '700' : '500'};">
                  ${s.is_overdue ? '⚠️ Overdue for watering!' : `Scheduled: ${s.next_watering_at ? new Date(s.next_watering_at).toLocaleDateString() : 'Today'}`}
                </span>
              </div>
            </div>
            <button onclick="Garden.quickWater('${s.garden_plant_id}', '${s.plant_name}')" class="btn-card-pill" style="font-size:0.75rem; padding:6px 14px;">
              Mark Watered
            </button>
          </div>
        `).join('')}
      </div>
    `;
  },

  renderHealthSummary() {
    const container = document.getElementById('garden-health-summary');
    if (!container) return;

    const total = this.plants.length;
    const healthy = this.plants.filter(p => p.health_status === 'Healthy').length;
    const attention = total - healthy;

    container.innerHTML = `
      <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; text-align:center;">
        <div style="background:var(--mint-bg); padding:14px; border-radius:12px;">
          <div style="font-size:1.6rem; font-weight:800; color:#133e29;">${total}</div>
          <div style="font-size:0.75rem; color:#5e7367; font-weight:600;">Total Plants</div>
        </div>
        <div style="background:#f0fdf4; padding:14px; border-radius:12px;">
          <div style="font-size:1.6rem; font-weight:800; color:#16a34a;">${healthy}</div>
          <div style="font-size:0.75rem; color:#166534; font-weight:600;">Healthy</div>
        </div>
        <div style="background:#fefce8; padding:14px; border-radius:12px;">
          <div style="font-size:1.6rem; font-weight:800; color:#ca8a04;">${attention}</div>
          <div style="font-size:0.75rem; color:#854d0e; font-weight:600;">Needs Check</div>
        </div>
      </div>
    `;
  },

  renderGrowthSection() {
    const container = document.getElementById('garden-growth-container');
    if (!container) return;

    if (this.growthRecords.length === 0) {
      container.innerHTML = `
        <div style="text-align:center; padding:24px; color:#5e7367; font-size:0.875rem;">
          <p>No growth measurements recorded yet.</p>
          <button onclick="Garden.openGrowthLogModal()" class="btn-primary-solid" style="margin-top:12px; font-size:0.8rem; padding:7px 16px;">
            + Log First Milestone
          </button>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span style="font-weight:700; color:#133e29; font-size:0.9rem;">Recent Milestones</span>
        <button onclick="Garden.openGrowthLogModal()" class="btn-card-pill" style="font-size:0.75rem; padding:5px 12px;">+ Log Height</button>
      </div>
      <div style="display:flex; flex-direction:column; gap:8px;">
        ${this.growthRecords.slice(0, 5).map(r => `
          <div style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; background:#f8faf8; border-radius:10px; font-size:0.825rem;">
            <div>
              <strong>${r.plant_name}</strong>: ${r.height_cm ? `${r.height_cm} cm tall` : ''} ${r.new_leaves_count ? `(${r.new_leaves_count} new leaves)` : ''}
              <div style="font-size:0.7rem; color:#87998e;">${new Date(r.recorded_at).toLocaleDateString()} ${r.health_notes ? `— "${r.health_notes}"` : ''}</div>
            </div>
            ${r.photo_url ? `<img src="${r.photo_url}" style="width:34px; height:34px; border-radius:6px; object-fit:cover;">` : ''}
          </div>
        `).join('')}
      </div>
    `;
  },

  renderCareHistory() {
    const container = document.getElementById('care-history-container');
    if (!container) return;

    if (this.wateringLogs.length === 0) {
      container.innerHTML = '<p style="color:#5e7367; font-size:0.85rem;">No recent activities logged.</p>';
      return;
    }

    container.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:8px;">
        ${this.wateringLogs.slice(0, 6).map(l => `
          <div style="display:flex; align-items:center; justify-content:space-between; padding:8px 12px; border-bottom:1px solid #f1f5f2; font-size:0.825rem;">
            <div>
              <span style="color:#16a34a; font-weight:700;">💧 Watered</span> <strong>${l.plant_name}</strong>
              ${l.notes ? `<span style="color:#87998e; font-size:0.75rem;"> - ${l.notes}</span>` : ''}
            </div>
            <div style="font-size:0.75rem; color:#87998e;">${new Date(l.watered_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
          </div>
        `).join('')}
      </div>
    `;
  },

  async quickWater(plantId, plantName) {
    try {
      await API.recordWatering(plantId, 'Routine hydration', 250);
      App.showToast(`Hydrated "${plantName}"! 💧 Reminder updated.`, 'success');
      await this.refreshAll();
    } catch (err) {
      App.showToast('Failed to log watering: ' + err.message, 'error');
    }
  },

  async deletePlant(plantId, plantName) {
    if (!confirm(`Are you sure you want to remove "${plantName}" from your garden?`)) return;

    try {
      await API.deleteGardenPlant(plantId);
      App.showToast(`Removed "${plantName}" from garden.`, 'info');
      await this.refreshAll();
    } catch (err) {
      App.showToast('Failed to delete plant: ' + err.message, 'error');
    }
  },

  openCustomAddModal() {
    const modal = document.getElementById('add-to-garden-modal');
    if (!modal) return;

    document.getElementById('modal-plant-id').value = '';
    document.getElementById('modal-plant-name').value = '';
    document.getElementById('modal-plant-image').value = '';
    document.getElementById('modal-plant-interval').value = 5;
    modal.classList.add('active');
  },

  openEditModal(plantId) {
    const plant = this.plants.find(p => p.id === plantId);
    if (!plant) return;

    const nickname = prompt(`Edit nickname for ${plant.name}:`, plant.nickname || '');
    if (nickname === null) return;

    const location = prompt('Edit placement location (e.g. Balcony, Living Room, Desk):', plant.location || 'Living Room');
    if (location === null) return;

    const intervalStr = prompt('Edit watering interval in days (1 - 30):', plant.watering_interval_days || 5);
    const interval = parseInt(intervalStr, 10);
    if (isNaN(interval) || interval < 1) return;

    API.updateGardenPlant(plantId, {
      nickname: nickname.trim(),
      location: location.trim(),
      watering_interval_days: interval
    }).then(() => {
      App.showToast('Plant details updated! ✨', 'success');
      this.refreshAll();
    }).catch(err => {
      App.showToast(err.message, 'error');
    });
  },

  openGrowthLogModal() {
    if (this.plants.length === 0) {
      App.showToast('Add a plant first before recording growth milestones.', 'info');
      return;
    }

    const modal = document.getElementById('growth-log-modal');
    if (modal) {
      const select = document.getElementById('growth-plant-select');
      if (select) {
        select.innerHTML = this.plants.map(p => `<option value="${p.id}">${p.nickname ? `${p.nickname} (${p.name})` : p.name}</option>`).join('');
      }
      modal.classList.add('active');
    }
  }
};

window.Garden = Garden;
