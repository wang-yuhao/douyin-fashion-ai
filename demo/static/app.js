// ===== State =====
const state = {
  lang: 'en',
  assetId: null,
  assetUrl: null,
  selectedTemplate: null,
  selectedRoute: 'standard',
  enhancedPrompt: '',
  activeJobId: null,
  pollTimer: null,
};

const TEMPLATE_EMOJIS = {
  runway_walk: '👠',
  studio_luxury: '✨',
  street_style: '🏙️',
  detail_closeup: '🔍',
  festive_campaign: '🎉',
  outdoor_cinematic: '🌅',
};

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
  loadTemplates();
  setupDragDrop();
});

// ===== Language =====
function setLang(lang) {
  state.lang = lang;
  document.querySelectorAll('[data-en]').forEach(el => {
    el.textContent = lang === 'zh' ? (el.dataset.zh || el.dataset.en) : el.dataset.en;
  });
  document.getElementById('langEn').classList.toggle('active', lang === 'en');
  document.getElementById('langZh').classList.toggle('active', lang === 'zh');
  // Update select options
  document.querySelectorAll('select option[data-en]').forEach(opt => {
    opt.textContent = lang === 'zh' ? (opt.dataset.zh || opt.dataset.en) : opt.dataset.en;
  });
}

// ===== Navigation =====
function showSection(name) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById('section-' + name).classList.add('active');
  document.querySelectorAll('.nav-btn').forEach((b, i) => {
    b.classList.toggle('active', ['generate','jobs','api'][i] === name);
  });
  if (name === 'jobs') refreshJobs();
}

// ===== Upload =====
function setupDragDrop() {
  const zone = document.getElementById('uploadZone');
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.style.borderColor = '#ff3b5c'; });
  zone.addEventListener('dragleave', () => { zone.style.borderColor = ''; });
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.style.borderColor = '';
    const file = e.dataTransfer.files[0];
    if (file) doUpload(file);
  });
}

async function handleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  doUpload(file);
}

async function doUpload(file) {
  showStatus('uploadStatus', 'info', '⏳ Uploading...');
  const formData = new FormData();
  formData.append('file', file);
  try {
    const res = await fetch('/api/assets/upload', { method: 'POST', body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Upload failed');
    state.assetId = data.asset_id;
    state.assetUrl = data.url;
    showStatus('uploadStatus', 'success', `✓ Uploaded: ${data.filename} (${(data.size_bytes/1024).toFixed(1)} KB)`);
    const preview = document.getElementById('uploadPreview');
    document.getElementById('previewImg').src = data.url;
    document.getElementById('previewFilename').textContent = data.filename;
    document.getElementById('previewSize').textContent = `${(data.size_bytes/1024).toFixed(1)} KB · ${data.content_type}`;
    preview.style.display = 'flex';
    document.getElementById('uploadZone').style.display = 'none';
  } catch (err) {
    showStatus('uploadStatus', 'error', '✗ ' + err.message);
  }
}

// ===== Templates =====
async function loadTemplates() {
  const grid = document.getElementById('templateGrid');
  try {
    const res = await fetch('/api/templates');
    const templates = await res.json();
    grid.innerHTML = templates.map(t => `
      <div class="template-card" data-id="${t.id}" onclick="selectTemplate('${t.id}', '${t.recommended_route}')">
        <div class="template-emoji">${TEMPLATE_EMOJIS[t.id] || '🎬'}</div>
        <div class="template-name-en">${t.name_en}</div>
        <div class="template-name-zh">${t.name_zh}</div>
        <div class="template-route route-${t.recommended_route}">● ${t.recommended_route}</div>
      </div>
    `).join('');
  } catch {
    grid.innerHTML = '<p style="color:#888">Failed to load templates</p>';
  }
}

function selectTemplate(id, route) {
  state.selectedTemplate = id;
  document.querySelectorAll('.template-card').forEach(c => {
    c.classList.toggle('selected', c.dataset.id === id);
  });
  // Auto-select recommended route
  selectRoute(route);
}

// ===== Route =====
function selectRoute(route) {
  state.selectedRoute = route;
  document.querySelectorAll('.route-card').forEach(c => {
    c.classList.toggle('selected', c.dataset.route === route);
    if (c.dataset.route === route) {
      c.querySelector('.route-name').textContent = `${route.charAt(0).toUpperCase() + route.slice(1)} ✓`;
    } else {
      c.querySelector('.route-name').textContent = c.dataset.route.charAt(0).toUpperCase() + c.dataset.route.slice(1);
    }
  });
}

// ===== Prompt Enhancement =====
async function enhancePrompt() {
  const btn = document.getElementById('enhanceBtn');
  const prompt = document.getElementById('promptInput').value.trim();
  if (!state.selectedTemplate) {
    alert('Please select a template first.');
    return;
  }
  btn.disabled = true;
  btn.querySelector('span').textContent = '⏳ Enhancing...';
  try {
    const res = await fetch('/api/prompts/enhance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt,
        template: state.selectedTemplate,
        persona: document.getElementById('personaSelect').value,
        language: state.lang === 'zh' ? 'zh-CN' : 'en',
      }),
    });
    const data = await res.json();
    state.enhancedPrompt = data.enhanced;
    const box = document.getElementById('enhancedPromptBox');
    document.getElementById('enhancedText').textContent = data.enhanced;
    box.style.display = 'block';
  } catch (err) {
    alert('Prompt enhancement failed: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.querySelector('span').textContent = state.lang === 'zh' ? '✨ 智能优化提示词' : '✨ Auto-Enhance Prompt';
  }
}

// ===== Job Submission =====
async function submitJob() {
  if (!state.assetId) { alert('Please upload a garment image first.'); return; }
  if (!state.selectedTemplate) { alert('Please select a video template.'); return; }
  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.querySelector('span').textContent = '⏳ Submitting job...';
  const body = {
    asset_id: state.assetId,
    template: state.selectedTemplate,
    prompt: document.getElementById('promptInput').value.trim(),
    enhanced_prompt: state.enhancedPrompt,
    persona: document.getElementById('personaSelect').value,
    route: state.selectedRoute,
    duration_seconds: parseInt(document.getElementById('durationSlider').value),
    aspect_ratio: '9:16',
  };
  try {
    const res = await fetch('/api/jobs', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const job = await res.json();
    if (!res.ok) throw new Error(job.detail || 'Submit failed');
    state.activeJobId = job.job_id;
    openJobModal(job);
    startPolling(job.job_id);
    showSection('jobs');
  } catch (err) {
    alert('Failed to submit job: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.querySelector('span').textContent = state.lang === 'zh' ? '🎬 生成抖音视频' : '🎬 Generate Douyin Video';
  }
}

// ===== Polling =====
function startPolling(jobId) {
  if (state.pollTimer) clearInterval(state.pollTimer);
  state.pollTimer = setInterval(async () => {
    const job = await fetchJob(jobId);
    if (!job) return;
    updateModalContent(job);
    refreshJobs();
    if (job.status === 'completed' || job.status === 'failed') {
      clearInterval(state.pollTimer);
    }
  }, 1500);
}

async function fetchJob(jobId) {
  try {
    const res = await fetch(`/api/jobs/${jobId}`);
    return res.ok ? await res.json() : null;
  } catch { return null; }
}

// ===== Jobs List =====
async function refreshJobs() {
  const container = document.getElementById('jobsList');
  try {
    const res = await fetch('/api/jobs');
    const jobs = await res.json();
    if (!jobs.length) {
      container.innerHTML = '<p style="color:#888;text-align:center;padding:40px">No jobs yet. Generate your first video!</p>';
      return;
    }
    // Sort newest first
    jobs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    container.innerHTML = jobs.map(j => `
      <div class="job-card" onclick="openJobModalById('${j.job_id}')">
        <div class="job-header">
          <div>
            <span class="badge badge-${j.status}">${j.status.toUpperCase()}</span>
            <span style="margin-left:10px;font-size:14px;font-weight:600;color:#fff">${formatTemplate(j.params?.template)}</span>
          </div>
          <div class="job-id">${j.job_id.slice(0, 8)}...</div>
        </div>
        <div class="job-meta">Route: ${j.params?.route || '—'} · Persona: ${j.params?.persona || '—'} · ${formatTime(j.created_at)}</div>
        <div>${j.message}</div>
        <div style="margin-top:10px">
          <div class="progress-bar"><div class="progress-fill progress-${j.status}" style="width:${j.progress}%"></div></div>
          <div style="font-size:12px;color:#666;margin-top:4px">${j.progress}%</div>
        </div>
      </div>
    `).join('');
  } catch {
    container.innerHTML = '<p style="color:#f87171">Failed to load jobs.</p>';
  }
}

// ===== Modal =====
function openJobModal(job) {
  document.getElementById('jobModal').style.display = 'flex';
  updateModalContent(job);
}

async function openJobModalById(jobId) {
  const job = await fetchJob(jobId);
  if (!job) return;
  openJobModal(job);
  if (job.status === 'processing' || job.status === 'queued') {
    state.activeJobId = jobId;
    startPolling(jobId);
  }
}

function updateModalContent(job) {
  const content = document.getElementById('modalContent');
  let html = `
    <h2 style="font-size:20px;font-weight:700;color:#fff;margin-bottom:8px">Job ${job.job_id.slice(0,8)}…</h2>
    <div style="margin-bottom:16px">
      <span class="badge badge-${job.status}" style="font-size:13px">${job.status.toUpperCase()}</span>
      <span style="margin-left:10px;font-size:13px;color:#888">${job.message}</span>
    </div>
    <div class="progress-bar" style="height:8px;margin-bottom:20px">
      <div class="progress-fill progress-${job.status}" style="width:${job.progress}%"></div>
    </div>
  `;
  if (job.status === 'completed' && job.result) {
    const r = job.result;
    html += `
      <video class="result-video" controls playsinline>
        <source src="${r.video_url}" type="video/mp4">
        Your browser doesn't support video.
      </video>
      <div style="font-size:12px;color:#666;margin-bottom:12px;text-align:center">📌 Demo: showing sample video. In production, your generated video appears here.</div>
      <div class="result-stats">
        <div class="stat-box"><div class="stat-val">${(r.quality_score * 100).toFixed(0)}%</div><div class="stat-label">Quality Score</div></div>
        <div class="stat-box"><div class="stat-val">${(r.garment_fidelity_score * 100).toFixed(0)}%</div><div class="stat-label">Garment Fidelity</div></div>
        <div class="stat-box"><div class="stat-val">$${r.cost_usd}</div><div class="stat-label">Generation Cost</div></div>
        <div class="stat-box"><div class="stat-val">${r.duration_seconds}s</div><div class="stat-label">Duration</div></div>
      </div>
      <div style="margin-top:16px;display:flex;gap:10px;flex-wrap:wrap">
        <a href="${r.video_url}" download class="btn btn-primary" target="_blank">⬇ Download Video</a>
        <button class="btn btn-secondary" onclick="closeModal()">Close</button>
      </div>
    `;
  } else if (job.status === 'failed') {
    html += `<div class="status-msg status-error">Generation failed. Please adjust settings and try again.</div>`;
  } else {
    html += `<div style="text-align:center;padding:20px;color:#888">⏳ Generating… polling every 1.5s</div>`;
  }
  content.innerHTML = html;
}

function closeModal() {
  document.getElementById('jobModal').style.display = 'none';
  if (state.pollTimer) { clearInterval(state.pollTimer); state.pollTimer = null; }
}

// ===== Helpers =====
function showStatus(id, type, msg) {
  const el = document.getElementById(id);
  el.className = `status-msg status-${type}`;
  el.textContent = msg;
  el.style.display = 'block';
}

function formatTemplate(id) {
  const map = {
    runway_walk: 'Runway Walk', studio_luxury: 'Studio Luxury',
    street_style: 'Street Style', detail_closeup: 'Detail Close-up',
    festive_campaign: 'Festive Campaign', outdoor_cinematic: 'Outdoor Cinematic',
  };
  return map[id] || id || 'Unknown';
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
