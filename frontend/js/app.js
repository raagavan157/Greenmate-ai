/**
 * GreenMate AI - Global Application Controller
 * Handles global events, modals, notifications, search, and navigation.
 */

const App = {
  init() {
    this.setupSearch();
    this.setupMobileMenu();
    this.setupModals();
    this.setupNewsletter();
    this.highlightActiveNav();
  },

  showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✓' : (type === 'error' ? '✕' : 'ℹ');
    toast.innerHTML = `<span style="font-size:1.1rem;">${icon}</span> <span>${message}</span>`;
    
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3800);
  },

  setupSearch() {
    const searchForms = document.querySelectorAll('.search-form');
    searchForms.forEach(form => {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = form.querySelector('.search-input');
        if (input && input.value.trim()) {
          const query = encodeURIComponent(input.value.trim());
          window.location.href = `/explore.html?search=${query}`;
        }
      });
    });
  },

  setupMobileMenu() {
    const toggle = document.querySelector('.mobile-nav-toggle');
    const navBar = document.querySelector('.nav-bar');
    if (toggle && navBar) {
      toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        navBar.classList.toggle('active');
      });

      // Close drawer when clicking a link
      navBar.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
          navBar.classList.remove('active');
        });
      });

      // Close on click outside
      document.addEventListener('click', (e) => {
        if (!navBar.contains(e.target) && !toggle.contains(e.target)) {
          navBar.classList.remove('active');
        }
      });
    }
  },

  highlightActiveNav() {
    const currentPath = window.location.pathname.toLowerCase();
    
    // Desktop Nav
    const navLinks = document.querySelectorAll('.nav-links .nav-item');
    navLinks.forEach(item => {
      const link = item.querySelector('a');
      if (link) {
        const href = link.getAttribute('href').toLowerCase();
        if (
          ((currentPath === '/' || currentPath === '/index.html' || currentPath === '') && (href === '/' || href === '/index.html')) ||
          (currentPath.includes('explore') && href.includes('explore')) ||
          (currentPath.includes('ai-doctor') && href.includes('ai-doctor')) ||
          (currentPath.includes('my-garden') && href.includes('my-garden')) ||
          (currentPath.includes('guides') && href.includes('guides')) ||
          (currentPath.includes('admin') && href.includes('admin'))
        ) {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      }
    });

    // Mobile Bottom Dock
    const bottomNavItems = document.querySelectorAll('.mobile-bottom-nav-item');
    bottomNavItems.forEach(item => {
      const href = item.getAttribute('href').toLowerCase();
      if (
        ((currentPath === '/' || currentPath === '/index.html' || currentPath === '') && (href === '/' || href === '/index.html')) ||
        (currentPath.includes('explore') && href.includes('explore')) ||
        (currentPath.includes('ai-doctor') && href.includes('ai-doctor')) ||
        (currentPath.includes('my-garden') && href.includes('my-garden')) ||
        (currentPath.includes('admin') && href.includes('admin'))
      ) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });
  },

  setupModals() {
    // Close modal on backdrop or close button click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          overlay.classList.remove('active');
        }
      });
    });

    document.querySelectorAll('.modal-close-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const modal = btn.closest('.modal-overlay');
        if (modal) modal.classList.remove('active');
      });
    });

    // Add to garden modal submission
    const gardenForm = document.getElementById('add-to-garden-form');
    if (gardenForm) {
      gardenForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const plantId = document.getElementById('modal-plant-id').value;
        const plantName = document.getElementById('modal-plant-name').value;
        const imageUrl = document.getElementById('modal-plant-image').value;
        const nickname = document.getElementById('modal-plant-nickname').value;
        const location = document.getElementById('modal-plant-location').value;
        const interval = parseInt(document.getElementById('modal-plant-interval').value, 10);

        try {
          await API.addToGarden({
            plant_id: plantId || null,
            name: plantName,
            nickname: nickname || null,
            location: location || 'Living Room',
            image_url: imageUrl || null,
            watering_interval_days: interval || 5
          });

          App.showToast(`"${nickname || plantName}" safely added to your Smart Garden! 🌿`, 'success');
          const modal = document.getElementById('add-to-garden-modal');
          if (modal) modal.classList.remove('active');

          if (window.Garden && typeof Garden.refreshAll === 'function') {
            Garden.refreshAll();
          }
          Auth.updateCounters();
        } catch (err) {
          App.showToast(err.message, 'error');
        }
      });
    }

    // Growth log form submission
    const growthForm = document.getElementById('growth-log-form');
    if (growthForm) {
      growthForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const plantId = document.getElementById('growth-plant-select').value;
        const height = parseFloat(document.getElementById('growth-height-input').value) || null;
        const leaves = parseInt(document.getElementById('growth-leaves-input').value, 10) || null;
        const notes = document.getElementById('growth-notes-input').value;

        try {
          await API.recordGrowth({
            garden_plant_id: plantId,
            height_cm: height,
            new_leaves_count: leaves,
            health_notes: notes
          });

          App.showToast('Growth milestone logged successfully! 📈', 'success');
          const modal = document.getElementById('growth-log-modal');
          if (modal) modal.classList.remove('active');

          if (window.Garden && typeof Garden.refreshAll === 'function') {
            Garden.refreshAll();
          }
        } catch (err) {
          App.showToast(err.message, 'error');
        }
      });
    }
  },

  setupNewsletter() {
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(f => {
      f.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = f.querySelector('.newsletter-input');
        if (input && input.value) {
          App.showToast('Thank you for joining our green community! 🌿', 'success');
          input.value = '';
        }
      });
    });
  },

  openQuickIdentifyModal() {
    const modal = document.getElementById('quick-identify-modal');
    if (modal) modal.classList.add('active');
  },

  openQuickDiagnoseModal() {
    const modal = document.getElementById('quick-diagnose-modal');
    if (modal) modal.classList.add('active');
  },

  async openGuideModal(guideId) {
    const modal = document.getElementById('guide-detail-modal');
    const titleElem = document.getElementById('guide-modal-title');
    const contentElem = document.getElementById('guide-modal-body');

    if (!modal) return;
    modal.classList.add('active');
    titleElem.textContent = 'Loading Guide...';
    contentElem.innerHTML = '<div style="text-align:center; padding:30px;"><div class="spinner"></div></div>';

    try {
      const guide = await API.getGuideById(guideId);
      titleElem.textContent = guide.title;
      contentElem.innerHTML = `
        <img src="${guide.image_url}" style="width:100%; height:220px; object-fit:cover; border-radius:14px; margin-bottom:18px;">
        <div style="font-size:0.8rem; font-weight:700; color:#16a34a; text-transform:uppercase; margin-bottom:6px;">${guide.category} • ${guide.read_time}</div>
        <h4 style="font-size:1.15rem; font-weight:800; color:#133e29; margin-bottom:12px;">${guide.subtitle}</h4>
        <div style="font-size:0.925rem; line-height:1.7; color:#334155; margin-bottom:20px;">
          ${guide.content.replace(/\n\n/g, '<br><br>').replace(/### (.*?)\n/g, '<h4 style="font-weight:800; color:#133e29; margin:16px 0 8px;">$1</h4>').replace(/#### (.*?)\n/g, '<h5 style="font-weight:700; color:#133e29; margin:12px 0 6px;">$1</h5>')}
        </div>
      `;
    } catch (err) {
      contentElem.innerHTML = `<p style="color:#ef4444;">Failed to load guide: ${err.message}</p>`;
    }
  }
};

window.App = App;
document.addEventListener('DOMContentLoaded', () => App.init());
