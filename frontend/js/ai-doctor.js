/**
 * GreenMate AI - AI Plant Doctor & Identification Module
 * Powers computer vision scanning, disease pathology analysis, and camera captures.
 */

const AIDoctor = {
  selectedFile: null,

  initDropzones() {
    // Plant Identify Dropzone
    this.setupDropzone('identify-dropzone', 'identify-file-input', 'identify-preview-img', 'identify-preview-container', (file) => {
      this.selectedFile = file;
    });

    // Disease Diagnose Dropzone
    this.setupDropzone('disease-dropzone', 'disease-file-input', 'disease-preview-img', 'disease-preview-container', (file) => {
      this.selectedFile = file;
    });
  },

  setupDropzone(dropzoneId, inputId, previewImgId, previewContainerId, onFileSelected) {
    const dropzone = document.getElementById(dropzoneId);
    const input = document.getElementById(inputId);
    const previewImg = document.getElementById(previewImgId);
    const previewContainer = document.getElementById(previewContainerId);

    if (!dropzone || !input) return;

    dropzone.addEventListener('click', () => input.click());

    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFile(e.dataTransfer.files[0]);
      }
    });

    input.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFile(e.target.files[0]);
      }
    });

    const handleFile = (file) => {
      if (!file.type.startsWith('image/')) {
        App.showToast('Please select a valid image file (JPG, PNG, WEBP).', 'error');
        return;
      }
      onFileSelected(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        if (previewImg && previewContainer) {
          previewImg.src = e.target.result;
          previewContainer.style.display = 'block';
        }
      };
      reader.readAsDataURL(file);
    };
  },

  async runIdentification(file = null, resultContainerId = 'identify-result-container') {
    const uploadFile = file || this.selectedFile;
    if (!uploadFile) {
      App.showToast('Please upload or snap a photo of the plant first!', 'info');
      return;
    }

    const container = document.getElementById(resultContainerId);
    if (!container) return;

    container.style.display = 'block';
    container.innerHTML = `
      <div style="text-align:center; padding: 40px; background:#f8faf8; border-radius:16px;">
        <div class="spinner" style="width:36px; height:36px; border-width:3px; border-top-color:#133e29;"></div>
        <h4 style="margin-top:14px; font-weight:800; color:#133e29;">Analyzing Plant Specimen...</h4>
        <p style="color:#5e7367; font-size:0.875rem; margin-top:4px;">Scanning foliage structure, leaf venation, and botanical taxonomy.</p>
      </div>
    `;

    try {
      const result = await API.identifyPlant(uploadFile);
      const confPercent = Math.round(result.confidence * 100);

      container.innerHTML = `
        <div style="background:#ffffff; border-radius:18px; border:1.5px solid var(--border-light); padding:28px; box-shadow:var(--shadow-md);">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px;">
            <div>
              <span style="display:inline-block; font-size:0.75rem; font-weight:800; text-transform:uppercase; background:var(--mint-pill); color:var(--primary-forest); padding:4px 12px; border-radius:var(--radius-full); margin-bottom:6px;">
                ${result.category}
              </span>
              <h2 style="font-size:1.85rem; font-weight:800; color:var(--primary-forest);">${result.common_name}</h2>
              <p style="font-style:italic; color:var(--text-subtle);">${result.scientific_name}</p>
            </div>
            <div style="text-align:right;">
              <div style="font-size:1.5rem; font-weight:800; color:#16a34a;">${confPercent}%</div>
              <div style="font-size:0.75rem; font-weight:600; color:#5e7367;">Confidence Match</div>
            </div>
          </div>

          ${result.notice ? `
            <div style="background:#eff6ff; border-left:4px solid #3b82f6; padding:10px 14px; border-radius:6px; font-size:0.8rem; color:#1e40af; margin-bottom:18px;">
              ℹ️ ${result.notice}
            </div>
          ` : ''}

          <p style="font-size:0.95rem; color:#5e7367; line-height:1.6; margin-bottom:24px;">${result.description}</p>

          <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:12px; margin-bottom:24px;">
            <div style="background:var(--mint-bg); padding:12px 16px; border-radius:12px;">
              <span style="font-weight:700; color:var(--primary-forest); font-size:0.825rem;">☀️ Light Requirement</span>
              <p style="font-size:0.875rem; color:#5e7367; margin-top:2px;">${result.sunlight}</p>
            </div>
            <div style="background:var(--mint-bg); padding:12px 16px; border-radius:12px;">
              <span style="font-weight:700; color:var(--primary-forest); font-size:0.825rem;">💧 Watering Schedule</span>
              <p style="font-size:0.875rem; color:#5e7367; margin-top:2px;">${result.watering}</p>
            </div>
            <div style="background:var(--mint-bg); padding:12px 16px; border-radius:12px;">
              <span style="font-weight:700; color:var(--primary-forest); font-size:0.825rem;">🪴 Soil Medium</span>
              <p style="font-size:0.875rem; color:#5e7367; margin-top:2px;">${result.soil_type}</p>
            </div>
            <div style="background:var(--mint-bg); padding:12px 16px; border-radius:12px;">
              <span style="font-weight:700; color:var(--primary-forest); font-size:0.825rem;">🌡️ Temperature</span>
              <p style="font-size:0.875rem; color:#5e7367; margin-top:2px;">${result.temperature_range}</p>
            </div>
          </div>

          <h4 style="font-size:1.05rem; font-weight:800; color:var(--primary-forest); margin-bottom:10px;">Botanical Care Protocol:</h4>
          <ul style="list-style:none; display:flex; flex-direction:column; gap:8px; margin-bottom:24px;">
            ${result.care_instructions.map(tip => `
              <li style="display:flex; align-items:flex-start; gap:8px; font-size:0.875rem; color:var(--text-main);">
                <span style="color:#16a34a; font-weight:700;">✓</span>
                <span>${tip}</span>
              </li>
            `).join('')}
          </ul>

          <div style="display:flex; gap:12px;">
            <button onclick="Plants.openAddToGardenModal('', '${result.common_name}', '${result.image_url}', 5)" class="btn-primary-pill" style="flex:1; justify-content:center;">
              🌿 Save to My Garden
            </button>
            <button onclick="AIDoctor.openChatAbout('${result.common_name}')" class="btn-outline-pill">
              💬 Ask AI About This
            </button>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div style="padding:24px; color:#ef4444; background:#fef2f2; border-radius:12px;">Identification error: ${err.message}</div>`;
    }
  },

  async runDiagnosis(file = null, resultContainerId = 'diagnose-result-container') {
    const uploadFile = file || this.selectedFile;
    if (!uploadFile) {
      App.showToast('Please select or snap a photo of the affected leaf first!', 'info');
      return;
    }

    const container = document.getElementById(resultContainerId);
    if (!container) return;

    container.style.display = 'block';
    container.innerHTML = `
      <div style="text-align:center; padding: 40px; background:#f8faf8; border-radius:16px;">
        <div class="spinner" style="width:36px; height:36px; border-width:3px; border-top-color:#133e29;"></div>
        <h4 style="margin-top:14px; font-weight:800; color:#133e29;">Diagnosing Plant Pathology...</h4>
        <p style="color:#5e7367; font-size:0.875rem; margin-top:4px;">Scanning for fungal lesions, chlorosis, necrotic tissues, and pests.</p>
      </div>
    `;

    try {
      const result = await API.diagnoseDisease(uploadFile);
      const confPercent = Math.round(result.confidence * 100);

      const sevColor = result.severity === 'Severe' ? '#dc2626' : (result.severity === 'Moderate' ? '#d97706' : '#16a34a');
      const sevBg = result.severity === 'Severe' ? '#fee2e2' : (result.severity === 'Moderate' ? '#fef3c7' : '#dcfce7');

      container.innerHTML = `
        <div style="background:#ffffff; border-radius:18px; border:1.5px solid var(--border-light); padding:28px; box-shadow:var(--shadow-md);">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px;">
            <div>
              <span style="display:inline-block; font-size:0.75rem; font-weight:800; text-transform:uppercase; padding:3px 10px; border-radius:10px; background:${sevBg}; color:${sevColor}; margin-bottom:6px;">
                Severity: ${result.severity}
              </span>
              <h2 style="font-size:1.85rem; font-weight:800; color:var(--primary-forest);">${result.disease_name}</h2>
              <p style="font-size:0.85rem; color:var(--text-subtle);">Analyzed from: ${result.plant_name || 'Foliage Photo'}</p>
            </div>
            <div style="text-align:right;">
              <div style="font-size:1.5rem; font-weight:800; color:#16a34a;">${confPercent}%</div>
              <div style="font-size:0.75rem; font-weight:600; color:#5e7367;">Confidence</div>
            </div>
          </div>

          ${result.notice ? `
            <div style="background:#eff6ff; border-left:4px solid #3b82f6; padding:10px 14px; border-radius:6px; font-size:0.8rem; color:#1e40af; margin-bottom:16px;">
              ℹ️ ${result.notice}
            </div>
          ` : ''}

          <!-- Symptoms & Causes -->
          <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:16px; margin-bottom:24px;">
            <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:14px; padding:16px;">
              <h4 style="font-size:0.95rem; font-weight:800; color:#92400e; margin-bottom:8px;">🔍 Visible Symptoms</h4>
              <ul style="list-style:none; display:flex; flex-direction:column; gap:6px; font-size:0.825rem; color:#78350f;">
                ${result.symptoms.map(s => `<li>• ${s}</li>`).join('')}
              </ul>
            </div>

            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:14px; padding:16px;">
              <h4 style="font-size:0.95rem; font-weight:800; color:#166534; margin-bottom:8px;">🌱 Probable Causes</h4>
              <ul style="list-style:none; display:flex; flex-direction:column; gap:6px; font-size:0.825rem; color:#14532d;">
                ${result.causes.map(c => `<li>• ${c}</li>`).join('')}
              </ul>
            </div>
          </div>

          <!-- Actionable Treatment -->
          <div style="background:var(--mint-bg); border-radius:14px; padding:20px; margin-bottom:20px; border:1px solid var(--mint-border);">
            <h4 style="font-size:1.1rem; font-weight:800; color:var(--primary-forest); margin-bottom:10px;">🩺 Recommended Treatment Protocol</h4>
            <ol style="padding-left:18px; display:flex; flex-direction:column; gap:8px; font-size:0.9rem; color:var(--text-main); line-height:1.5;">
              ${result.treatment.map(t => `<li><strong>${t}</strong></li>`).join('')}
            </ol>
          </div>

          <!-- Prevention Tips -->
          <div style="margin-bottom:20px;">
            <h5 style="font-size:0.95rem; font-weight:800; color:var(--primary-forest); margin-bottom:8px;">🛡️ Long-term Prevention</h5>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:6px; font-size:0.85rem; color:#5e7367;">
              ${result.prevention.map(p => `<li>✓ ${p}</li>`).join('')}
            </ul>
          </div>

          <!-- Disclaimer -->
          <div style="background:#f8fafc; border:1px dashed #cbd5e1; border-radius:10px; padding:12px; font-size:0.75rem; color:#64748b; line-height:1.45; margin-bottom:20px;">
            ⚠️ <em>${result.disclaimer}</em>
          </div>

          <div style="display:flex; gap:12px;">
            <button onclick="AIDoctor.openChatAbout('${result.disease_name}')" class="btn-primary-pill" style="flex:1; justify-content:center;">
              💬 Ask AI Doctor for Advice
            </button>
            <button onclick="window.print()" class="btn-outline-pill">
              🖨️ Print Report
            </button>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div style="padding:24px; color:#ef4444; background:#fef2f2; border-radius:12px;">Diagnosis error: ${err.message}</div>`;
    }
  },

  openChatAbout(topic) {
    if (window.Chatbot) {
      Chatbot.open();
      Chatbot.sendMessage(`Tell me more about ${topic} and how to properly care for it.`);
    }
  }
};

window.AIDoctor = AIDoctor;
document.addEventListener('DOMContentLoaded', () => AIDoctor.initDropzones());
