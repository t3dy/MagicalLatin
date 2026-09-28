// ===== MAGICAL LATIN: A READER =====
// Core application logic

// ===== STATE =====
const STATE_KEY = 'magicalLatin_v1';
let STATE = {
  xp: 0,
  level: 1,
  wordsLooked: {},      // word → count
  passagesRead: {},     // id → bool
  passagesTranslated: {}, // id → bool
  readList: [],         // [id, ...]
  ritualsComplete: {},  // id → bool
  experiments: [],      // [{substance, operation, result, ts}]
  achievements: {}      // id → bool
};

// ===== XP LEVELS =====
const LEVELS = [
  { xp: 0,    num: 1, title: 'Novice Scribe' },
  { xp: 100,  num: 2, title: 'Apprentice' },
  { xp: 300,  num: 3, title: 'Adept' },
  { xp: 700,  num: 4, title: 'Magus' },
  { xp: 1500, num: 5, title: 'Archmagus' }
];

// ===== ACHIEVEMENTS =====
const ACHIEVEMENTS = [
  { id: 'first_word',   name: 'First Illumination',   icon: '🕯', desc: 'Look up your first Latin word', check: s => Object.keys(s.wordsLooked).length >= 1 },
  { id: 'ten_words',    name: 'Word Hoarder',          icon: '📚', desc: 'Look up 10 different words',   check: s => Object.keys(s.wordsLooked).length >= 10 },
  { id: 'fifty_words',  name: 'Vocabularian',          icon: '🔤', desc: 'Look up 50 different words',   check: s => Object.keys(s.wordsLooked).length >= 50 },
  { id: 'first_read',   name: 'First Passage',         icon: '📖', desc: 'Mark a passage as read',       check: s => Object.keys(s.passagesRead).length >= 1 },
  { id: 'five_read',    name: 'Diligent Student',      icon: '✦',  desc: 'Read 5 passages',              check: s => Object.keys(s.passagesRead).length >= 5 },
  { id: 'translated',   name: 'Translator',            icon: '⟺',  desc: 'Translate a passage',          check: s => Object.keys(s.passagesTranslated).length >= 1 },
  { id: 'ritual_done',  name: 'Initiate',              icon: '🕍', desc: 'Complete your first ritual',   check: s => Object.keys(s.ritualsComplete).length >= 1 },
  { id: 'three_rituals',name: 'Ceremonialist',         icon: '⊕',  desc: 'Complete 3 rituals',           check: s => Object.keys(s.ritualsComplete).length >= 3 },
  { id: 'alchemist',    name: 'Alchemist',             icon: '⚗',  desc: 'Perform your first experiment', check: s => s.experiments.length >= 1 },
  { id: 'adept_level',  name: 'Adept',                 icon: '✧',  desc: 'Reach Adept level (300 XP)',   check: s => s.xp >= 300 },
  { id: 'magus_level',  name: 'Magus',                 icon: '☽',  desc: 'Reach Magus level (700 XP)',   check: s => s.xp >= 700 },
  { id: 'archmagus',    name: 'Archmagus',             icon: '☉',  desc: 'Reach Archmagus (1500 XP)',    check: s => s.xp >= 1500 },
];

// ===== DATA =====
let PASSAGES = [];
let RITUALS = {};
let ALCHEMY = {};
let BIBLIOGRAPHY = [];
let currentPassage = null;
let currentRitual = null;
let currentRitualStep = 0;
let ritualStepsPerformed = new Set();
let selectedSubstance = null;
let selectedOperation = null;
let scaffoldLevel = 'full'; // 'full' | 'hover' | 'none' | 'interlinear'
let filteredPassages = [];
let currentPassageIndex = -1;

// Quiz state
let quizWords = [];
let quizIndex = 0;
let quizStats = { knew: 0, almost: 0, missed: 0, xpEarned: 0 };

// ===== INIT =====
async function init() {
  loadState();
  await Promise.all([
    fetch('data/passages.json').then(r => r.json()).then(d => PASSAGES = d),
    fetch('data/rituals.json').then(r => r.json()).then(d => RITUALS = d),
    fetch('data/alchemy.json').then(r => r.json()).then(d => ALCHEMY = d),
    fetch('data/bibliography.json').then(r => r.json()).then(d => BIBLIOGRAPHY = d).catch(() => BIBLIOGRAPHY = []),
  ]);
  buildTraditionFilters();
  renderCards();
  updateXPDisplay();
  updateSidebarStats();
  setupEventListeners();
}

// ===== STATE PERSISTENCE =====
function loadState() {
  try {
    const saved = localStorage.getItem(STATE_KEY);
    if (saved) STATE = { ...STATE, ...JSON.parse(saved) };
  } catch(e) {}
}
function saveState() {
  localStorage.setItem(STATE_KEY, JSON.stringify(STATE));
}

// ===== XP SYSTEM =====
function addXP(amount, label) {
  STATE.xp += amount;
  updateXPDisplay();
  checkAchievements();
  saveState();
  showXPBurst(amount, label);
}

function getCurrentLevel() {
  let level = LEVELS[0];
  for (const l of LEVELS) { if (STATE.xp >= l.xp) level = l; }
  return level;
}

function updateXPDisplay() {
  const lvl = getCurrentLevel();
  const nextIdx = LEVELS.findIndex(l => l.num === lvl.num) + 1;
  const next = LEVELS[nextIdx];
  const pct = next ? ((STATE.xp - lvl.xp) / (next.xp - lvl.xp)) * 100 : 100;
  document.getElementById('level-badge').textContent = lvl.title;
  document.getElementById('xp-bar').style.width = Math.min(100, pct) + '%';
  document.getElementById('xp-label').textContent = next
    ? `${STATE.xp} / ${next.xp} XP`
    : `${STATE.xp} XP — Maximum Level`;
}

function showXPBurst(amount, label) {
  const el = document.createElement('div');
  el.className = 'xp-burst';
  el.style.cssText = `
    position:fixed; top:80px; right:30px; z-index:500;
    background:rgba(200,150,42,0.9); color:#0c0a06;
    font-family:var(--font-head); font-size:0.85rem; font-weight:700;
    padding:8px 16px; border-radius:3px; letter-spacing:0.1em;
    animation: burst-fade 1.8s ease forwards; pointer-events:none;
  `;
  el.textContent = `+${amount} XP — ${label}`;
  const style = document.createElement('style');
  style.textContent = `@keyframes burst-fade { 0%{opacity:0;transform:translateY(10px)} 15%{opacity:1;transform:translateY(0)} 70%{opacity:1} 100%{opacity:0;transform:translateY(-20px)} }`;
  document.head.appendChild(style);
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2000);
}

// ===== ACHIEVEMENTS =====
function checkAchievements() {
  for (const ach of ACHIEVEMENTS) {
    if (!STATE.achievements[ach.id] && ach.check(STATE)) {
      STATE.achievements[ach.id] = true;
      showAchievementToast(ach);
    }
  }
}

function showAchievementToast(ach) {
  const el = document.createElement('div');
  el.style.cssText = `
    position:fixed; bottom:30px; right:30px; z-index:500;
    background:var(--bg2); border:1px solid var(--gold);
    border-radius:4px; padding:12px 18px; box-shadow:0 4px 24px rgba(200,150,42,0.3);
    display:flex; align-items:center; gap:12px;
    animation: burst-fade 3.5s ease forwards; pointer-events:none;
    max-width:280px;
  `;
  el.innerHTML = `
    <span style="font-size:1.3rem">${ach.icon}</span>
    <div>
      <div style="font-family:var(--font-head);color:var(--gold-light);font-size:0.82rem;letter-spacing:0.08em">${ach.name}</div>
      <div style="font-size:0.75rem;color:var(--text-dim)">${ach.desc}</div>
    </div>
  `;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3700);
}

// ===== FILTERING =====
function getActiveFilters() {
  const eras = [...document.querySelectorAll('.filter-era:checked')].map(c => c.value);
  const traditions = [...document.querySelectorAll('.filter-tradition:checked')].map(c => c.value);
  const maxDiff = parseInt(document.getElementById('diff-slider').value);
  const onlyReadList = document.getElementById('filter-read-list').checked;
  const onlyRitual = document.getElementById('filter-has-ritual').checked;
  const onlyUnread = document.getElementById('filter-unread').checked;
  const search = document.getElementById('search-box').value.toLowerCase().trim();
  return { eras, traditions, maxDiff, onlyReadList, onlyRitual, onlyUnread, search };
}

function filterPassages(f) {
  return PASSAGES.filter(p => {
    if (!f.eras.includes(p.era)) return false;
    if (f.traditions.length && !f.traditions.includes(p.tradition)) return false;
    if (p.difficulty > f.maxDiff) return false;
    if (f.onlyReadList && !STATE.readList.includes(p.id)) return false;
    if (f.onlyRitual && !p.has_ritual) return false;
    if (f.onlyUnread && STATE.passagesRead[p.id]) return false;
    if (f.search) {
      const hay = (p.title + p.author + p.latin_text + p.representative_sentence).toLowerCase();
      if (!hay.includes(f.search)) return false;
    }
    return true;
  });
}

// ===== RENDER CARDS =====
function buildTraditionFilters() {
  const traditions = [...new Set(PASSAGES.map(p => p.tradition))].sort();
  const container = document.getElementById('tradition-filters');
  container.innerHTML = traditions.map(t => `
    <label class="filter-check">
      <input type="checkbox" class="filter-tradition" value="${t}" checked>
      ${t.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}
    </label>
  `).join('');
  container.querySelectorAll('.filter-tradition').forEach(cb => cb.addEventListener('change', renderCards));
}

function diffDots(n) {
  return '✦'.repeat(n) + '✧'.repeat(5 - n);
}

function eraClass(era) {
  if (era === 'ancient') return 'chip-era-ancient';
  if (era === 'medieval') return 'chip-era-medieval';
  return 'chip-era-renaissance';
}

function getWordCoverage(p) {
  if (!p.vocabulary || !p.vocabulary.length) return { pct: 0, covered: 0, total: 0 };
  const vocabWords = new Set(p.vocabulary.map(v => v.word.toLowerCase()));
  const covered = Object.keys(STATE.wordsLooked).filter(w => vocabWords.has(w)).length;
  return { pct: Math.round(covered / vocabWords.size * 100), covered, total: vocabWords.size };
}

function renderCards() {
  const f = getActiveFilters();
  const filtered = filterPassages(f);
  filteredPassages = filtered;
  const grid = document.getElementById('card-grid');

  if (!filtered.length) {
    grid.innerHTML = '<div class="empty-state"><h3>No passages found</h3><p>Adjust your filters to see more.</p></div>';
    return;
  }

  grid.innerHTML = filtered.map((p, i) => {
    const isRead = !!STATE.passagesRead[p.id];
    const isTranslated = !!STATE.passagesTranslated[p.id];
    const inReadList = STATE.readList.includes(p.id);
    const cov = getWordCoverage(p);
    return `
    <article class="passage-card" data-id="${p.id}" style="animation-delay:${i * 0.04}s" role="button" tabindex="0">
      <div class="card-top">
        <div class="card-chips">
          <span class="chip ${eraClass(p.era)}">${p.era}</span>
          <span class="chip chip-tradition">${p.tradition.replace(/_/g,' ')}</span>
        </div>
        <span class="diff-dots" title="Difficulty ${p.difficulty}/5">${diffDots(p.difficulty)}</span>
      </div>
      <div class="card-title">${p.title}</div>
      <div class="card-author">${p.author} · ${p.date}</div>
      <blockquote class="card-sentence">${p.representative_sentence}</blockquote>
      <div class="card-coverage" title="${cov.covered}/${cov.total} vocabulary words looked up">
        <div class="coverage-bar"><div class="coverage-fill" style="width:${cov.pct}%"></div></div>
        <span class="coverage-pct">${cov.pct}%</span>
      </div>
      <div class="card-footer">
        <div class="card-status-icons">
          <span class="card-status-icon ${inReadList ? 'active' : ''}" title="In read list">📖</span>
          <span class="card-status-icon ${isRead ? 'active' : ''}" title="Read">✓</span>
          <span class="card-status-icon ${isTranslated ? 'active' : ''}" title="Translated">⟺</span>
        </div>
        ${p.has_ritual ? '<span class="card-ritual-badge">⊕ Ritual</span>' : ''}
      </div>
    </article>`;
  }).join('');

  grid.querySelectorAll('.passage-card').forEach(card => {
    card.addEventListener('click', () => openPassage(card.dataset.id));
    card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') openPassage(card.dataset.id); });
  });
}

// ===== PASSAGE MODAL =====
function openPassage(id) {
  const p = PASSAGES.find(x => x.id === id);
  if (!p) return;
  currentPassage = p;
  currentPassageIndex = filteredPassages.findIndex(x => x.id === id);

  // Update nav buttons
  const prevBtn = document.getElementById('passage-prev');
  const nextBtn = document.getElementById('passage-next');
  const navLabel = document.getElementById('passage-nav-label');
  prevBtn.disabled = currentPassageIndex <= 0;
  nextBtn.disabled = currentPassageIndex < 0 || currentPassageIndex >= filteredPassages.length - 1;
  navLabel.textContent = currentPassageIndex >= 0
    ? `${currentPassageIndex + 1} / ${filteredPassages.length}`
    : '';

  document.getElementById('pm-tradition').textContent = p.tradition.replace(/_/g, ' ');
  document.getElementById('pm-era').className = `era-chip ${eraClass(p.era)}`;
  document.getElementById('pm-era').textContent = p.era;
  document.getElementById('pm-diff').textContent = diffDots(p.difficulty);
  document.getElementById('pm-title').textContent = p.title_english || p.title;
  document.getElementById('pm-meta').innerHTML = `
    <strong>${p.author}</strong> &middot; <em>${p.source}</em> &middot; ${p.date}
  `;
  document.getElementById('pm-gloss').textContent = p.english_gloss;
  document.getElementById('pm-notes').textContent = p.source_notes;

  // Build clickable Latin text
  renderLatinText(p);

  // Vocabulary
  renderVocab(p);

  // Scaffold buttons
  setScaffold('full');

  // Read list button
  const rlBtn = document.getElementById('pm-readlist-btn');
  const inList = STATE.readList.includes(p.id);
  rlBtn.textContent = inList ? '☑ In Read List' : '☐ Add to Read List';
  rlBtn.classList.toggle('active', inList);

  // Mark read/translated
  const markRead = document.getElementById('pm-mark-read');
  const markTrans = document.getElementById('pm-mark-translated');
  markRead.classList.toggle('done', !!STATE.passagesRead[p.id]);
  markRead.textContent = STATE.passagesRead[p.id] ? '✓ Marked Read' : '✓ Mark Read (+10 XP)';
  markTrans.classList.toggle('done', !!STATE.passagesTranslated[p.id]);
  markTrans.textContent = STATE.passagesTranslated[p.id] ? '⟺ Marked Translated' : '⟺ Mark Translated (+25 XP)';

  // Ritual button
  const ritualBtn = document.getElementById('pm-ritual-btn');
  if (p.has_ritual && p.ritual_id) {
    ritualBtn.removeAttribute('hidden');
    ritualBtn.dataset.ritualId = p.ritual_id;
  } else {
    ritualBtn.hidden = true;
  }

  document.getElementById('passage-modal').removeAttribute('hidden');
  document.body.style.overflow = 'hidden';
}

function renderLatinText(p) {
  const container = document.getElementById('pm-latin');
  const isInterlinear = scaffoldLevel === 'interlinear';
  const words = p.latin_text.split(/(\s+|[,;:!?.—–]+)/);
  container.innerHTML = words.map(token => {
    if (/^\s+$/.test(token)) return isInterlinear ? ' ' : token;
    const match = token.match(/^([^a-zA-ZÀ-ÿ]*)([a-zA-ZÀ-ÿ\-]+)([^a-zA-ZÀ-ÿ]*)$/);
    if (!match) return `<span>${escHtml(token)}</span>`;
    const [, pre, word, post] = match;
    const lower = word.toLowerCase();
    const lookedUp = !!STATE.wordsLooked[lower];
    if (isInterlinear) {
      const def = lookupWord(lower, p);
      const defText = def ? def.definition.split(';')[0].split(',')[0].trim() : '·';
      return `${escHtml(pre)}<span class="interlinear-pair"><span class="latin-word iword${lookedUp ? ' looked-up' : ''}" data-word="${lower}">${escHtml(word)}</span><span class="idef">${escHtml(defText)}</span></span>${escHtml(post)}`;
    }
    return `${escHtml(pre)}<span class="latin-word${lookedUp ? ' looked-up' : ''}" data-word="${lower}">${escHtml(word)}</span>${escHtml(post)}`;
  }).join('');

  container.querySelectorAll('.latin-word').forEach(el => {
    el.addEventListener('click', e => onWordClick(e, el, p));
    el.addEventListener('mouseenter', e => { if (scaffoldLevel === 'hover') showTooltip(e, el, p); });
    el.addEventListener('mouseleave', () => { if (scaffoldLevel === 'hover') hideTooltip(); });
  });
}

function renderVocab(p) {
  const grid = document.getElementById('pm-vocab');
  grid.innerHTML = p.vocabulary.map(v => `
    <div class="vocab-item" data-word="${v.word.toLowerCase()}">
      <div class="vocab-word">${v.word}</div>
      ${v.lemma !== v.word ? `<div class="vocab-lemma">← ${v.lemma}</div>` : ''}
      <div class="vocab-def">${v.definition}</div>
    </div>
  `).join('');
  grid.querySelectorAll('.vocab-item').forEach(el => {
    el.addEventListener('click', () => {
      const word = el.dataset.word;
      trackWordLookup(word);
      highlightWord(word);
    });
  });
}

function onWordClick(e, el, p) {
  if (scaffoldLevel === 'none') return;
  const word = el.dataset.word;
  const def = lookupWord(word, p);
  trackWordLookup(word);
  el.classList.add('looked-up');
  showTooltip(e, el, p, def);
}

function lookupWord(word, p) {
  // Check passage vocab first
  if (p && p.vocabulary) {
    const v = p.vocabulary.find(x => x.word.toLowerCase() === word);
    if (v) return v;
  }
  // Fall back to global dict
  if (window.LATIN_DICT && window.LATIN_DICT[word]) {
    return window.LATIN_DICT[word];
  }
  return null;
}

function trackWordLookup(word) {
  const lower = word.toLowerCase();
  const isNew = !STATE.wordsLooked[lower];
  STATE.wordsLooked[lower] = (STATE.wordsLooked[lower] || 0) + 1;
  if (isNew) {
    addXP(2, 'New word discovered');
    updateSidebarStats();
  }
  checkAchievements();
  saveState();
}

function highlightWord(word) {
  document.querySelectorAll(`.latin-word[data-word="${word}"]`).forEach(el => {
    el.classList.add('looked-up');
  });
}

function showTooltip(e, el, p, def) {
  if (!def) def = lookupWord(el.dataset.word, p);
  const tip = document.getElementById('word-tooltip');
  document.getElementById('tip-word').textContent = el.dataset.word;
  document.getElementById('tip-lemma').textContent = def ? `← ${def.lemma}` : '';
  document.getElementById('tip-def').textContent = def ? def.definition : '(not in dictionary)';
  tip.removeAttribute('hidden');
  positionTooltip(e, tip);
}

function positionTooltip(e, tip) {
  const margin = 12;
  let x = e.clientX + margin;
  let y = e.clientY + margin;
  const rect = tip.getBoundingClientRect();
  const vw = window.innerWidth, vh = window.innerHeight;
  if (x + rect.width > vw - 10) x = e.clientX - rect.width - margin;
  if (y + rect.height > vh - 10) y = e.clientY - rect.height - margin;
  tip.style.left = x + 'px';
  tip.style.top = y + 'px';
}

function hideTooltip() {
  document.getElementById('word-tooltip').hidden = true;
}

function setScaffold(level) {
  const wasInterlinear = scaffoldLevel === 'interlinear';
  scaffoldLevel = level;
  document.querySelectorAll('.scaf-btn').forEach(b => b.classList.toggle('active', b.dataset.level === level));
  const latin = document.getElementById('pm-latin');
  latin.className = 'latin-passage scaffold-' + level;
  const note = document.getElementById('scaf-note');
  if (level === 'full') note.textContent = 'Click any Latin word for its definition.';
  else if (level === 'hover') note.textContent = 'Hover over words to see definitions.';
  else if (level === 'interlinear') note.textContent = 'Each word shown with its meaning beneath.';
  else note.textContent = 'Pure Latin — no aids. Test yourself.';
  if (level !== 'full') hideTooltip();
  // Re-render when switching to/from interlinear (structure changes)
  if ((level === 'interlinear' || wasInterlinear) && currentPassage) {
    renderLatinText(currentPassage);
    document.getElementById('pm-latin').className = 'latin-passage scaffold-' + level;
  }
}

// ===== GLOSS TOGGLE =====
function setupGlossToggle() {
  const btn = document.getElementById('gloss-toggle');
  const body = document.getElementById('pm-gloss');
  btn.addEventListener('click', () => {
    const hidden = body.hasAttribute('hidden');
    body.toggleAttribute('hidden', !hidden);
    btn.textContent = (hidden ? '▼' : '▶') + ' English Translation';
  });
}

// ===== PASSAGE ACTIONS =====
function setupPassageActions() {
  document.getElementById('pm-readlist-btn').addEventListener('click', () => {
    if (!currentPassage) return;
    const id = currentPassage.id;
    const idx = STATE.readList.indexOf(id);
    if (idx === -1) {
      STATE.readList.push(id);
      document.getElementById('pm-readlist-btn').textContent = '☑ In Read List';
      document.getElementById('pm-readlist-btn').classList.add('active');
    } else {
      STATE.readList.splice(idx, 1);
      document.getElementById('pm-readlist-btn').textContent = '☐ Add to Read List';
      document.getElementById('pm-readlist-btn').classList.remove('active');
    }
    saveState();
    updateSidebarStats();
    renderCards();
  });

  document.getElementById('pm-mark-read').addEventListener('click', () => {
    if (!currentPassage || STATE.passagesRead[currentPassage.id]) return;
    STATE.passagesRead[currentPassage.id] = true;
    document.getElementById('pm-mark-read').textContent = '✓ Marked Read';
    document.getElementById('pm-mark-read').classList.add('done');
    addXP(10, 'Passage read');
    updateSidebarStats();
    renderCards();
    checkAchievements();
  });

  document.getElementById('pm-mark-translated').addEventListener('click', () => {
    if (!currentPassage || STATE.passagesTranslated[currentPassage.id]) return;
    STATE.passagesTranslated[currentPassage.id] = true;
    document.getElementById('pm-mark-translated').textContent = '⟺ Marked Translated';
    document.getElementById('pm-mark-translated').classList.add('done');
    addXP(25, 'Passage translated');
    updateSidebarStats();
    renderCards();
    checkAchievements();
  });

  document.getElementById('pm-ritual-btn').addEventListener('click', () => {
    const ritualId = document.getElementById('pm-ritual-btn').dataset.ritualId;
    if (ritualId) {
      closeModal('passage-modal');
      openRitual(ritualId);
    }
  });
}

// ===== RITUAL SYSTEM =====
function openRitual(ritualId) {
  const ritual = RITUALS[ritualId];
  if (!ritual) return;
  currentRitual = ritual;
  currentRitualStep = 0;
  ritualStepsPerformed = new Set();

  document.getElementById('ritual-source').textContent = ritual.source;
  document.getElementById('ritual-title').textContent = ritual.title;
  document.getElementById('ritual-desc').textContent = ritual.description;
  document.getElementById('ritual-complete').hidden = true;
  document.querySelector('.ritual-step-body').style.display = '';
  document.querySelector('.ritual-actions').style.display = '';

  renderRitualStep();
  document.getElementById('ritual-modal').removeAttribute('hidden');
  document.body.style.overflow = 'hidden';
}

function renderRitualStep() {
  const ritual = currentRitual;
  const step = ritual.steps[currentRitualStep];
  const total = ritual.steps.length;

  document.getElementById('ritual-step-label').textContent = `Step ${currentRitualStep + 1} of ${total}`;
  document.getElementById('ritual-progress').style.width = ((currentRitualStep + 1) / total * 100) + '%';
  document.getElementById('step-type-chip').textContent = step.type.replace(/-/g, ' ');
  document.getElementById('step-title').textContent = step.title;
  document.getElementById('step-latin').textContent = step.latin;

  // Scaffold-aware action text
  const lvl = getCurrentLevel().num;
  let actionText = step.action;
  if (lvl >= 4 && step.scaffold_high) actionText = step.scaffold_high;
  else if (lvl >= 3 && step.scaffold_med) actionText = step.scaffold_med;

  document.getElementById('step-english').textContent = lvl <= 3 ? step.english : '';
  document.getElementById('step-action').textContent = actionText;

  document.getElementById('ritual-prev').disabled = currentRitualStep === 0;
  document.getElementById('ritual-next').disabled = currentRitualStep >= total - 1;

  const performBtn = document.getElementById('ritual-perform');
  const performed = ritualStepsPerformed.has(currentRitualStep);
  performBtn.textContent = performed ? '✓ Step Performed' : 'Perform This Step ✓';
  performBtn.style.opacity = performed ? '0.6' : '1';
}

function completeRitual() {
  const ritual = currentRitual;
  STATE.ritualsComplete[ritual.id] = true;
  addXP(ritual.xp, 'Ritual completed');
  saveState();
  updateSidebarStats();
  checkAchievements();
  renderCards();

  document.querySelector('.ritual-step-body').style.display = 'none';
  document.querySelector('.ritual-actions').style.display = 'none';
  const complete = document.getElementById('ritual-complete');
  complete.removeAttribute('hidden');
  document.getElementById('ritual-xp-msg').textContent = `${ritual.title} complete. +${ritual.xp} XP awarded.`;
}

// ===== ALCHEMY LAB =====
function openAlchemy() {
  renderSubstances();
  renderOperations();
  document.getElementById('alch-history-list').innerHTML = '';
  STATE.experiments.slice().reverse().slice(0, 10).forEach(exp => {
    appendAlchHistory(exp);
  });
  selectedSubstance = null;
  selectedOperation = null;
  updateWorkspace();
  document.getElementById('alchemy-modal').removeAttribute('hidden');
  document.body.style.overflow = 'hidden';
}

function renderSubstances() {
  const list = document.getElementById('substance-list');
  list.innerHTML = ALCHEMY.substances.map(s => `
    <button class="substance-btn" data-id="${s.id}" title="${s.description}">
      <span class="subst-symbol">${s.symbol}</span>
      <div>
        <div class="subst-name">${s.name}</div>
        <div style="font-size:0.72rem;color:var(--text-dim)">${s.english}</div>
      </div>
    </button>
  `).join('');
  list.querySelectorAll('.substance-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      selectedSubstance = ALCHEMY.substances.find(s => s.id === btn.dataset.id);
      list.querySelectorAll('.substance-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      updateWorkspace();
    });
  });
}

function renderOperations() {
  const list = document.getElementById('operation-list');
  list.innerHTML = ALCHEMY.operations.map(op => `
    <button class="operation-btn" data-id="${op.id}" title="${op.description}">
      <span class="op-symbol">${op.symbol}</span>
      <div>
        <div class="op-name">${op.name}</div>
        <div style="font-size:0.72rem;color:var(--text-dim)">${op.english}</div>
      </div>
    </button>
  `).join('');
  list.querySelectorAll('.operation-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      selectedOperation = ALCHEMY.operations.find(op => op.id === btn.dataset.id);
      list.querySelectorAll('.operation-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      updateWorkspace();
    });
  });
}

function updateWorkspace() {
  document.getElementById('ws-substance').textContent = selectedSubstance ? selectedSubstance.name : '—';
  document.getElementById('ws-operation').textContent = selectedOperation ? selectedOperation.name : '—';
  document.getElementById('ws-result').textContent = '?';
  document.getElementById('alch-result-desc').textContent = '';

  if (selectedSubstance && selectedOperation) {
    document.getElementById('alch-latin-desc').textContent = selectedOperation.latin_desc;
    document.getElementById('alch-perform').disabled = false;
  } else {
    document.getElementById('alch-latin-desc').textContent = selectedOperation ? selectedOperation.latin_desc : '';
    document.getElementById('alch-perform').disabled = true;
  }
}

function performExperiment() {
  if (!selectedSubstance || !selectedOperation) return;
  const combo = ALCHEMY.combinations.find(c => c.substance === selectedSubstance.id && c.operation === selectedOperation.id);

  const exp = {
    substance: selectedSubstance.id,
    operation: selectedOperation.id,
    result: combo ? combo.result : 'failure',
    result_name: combo ? combo.result_name : 'Nigredo (Failed Work)',
    ts: Date.now()
  };
  STATE.experiments.unshift(exp);
  if (STATE.experiments.length > 100) STATE.experiments = STATE.experiments.slice(0, 100);

  if (combo) {
    document.getElementById('ws-result').textContent = combo.result_name;
    document.getElementById('alch-result-desc').textContent = combo.description;
    document.getElementById('alch-latin-desc').textContent = combo.latin_result;
    addXP(combo.xp, 'Alchemical experiment');
  } else {
    document.getElementById('ws-result').textContent = 'Nigredo — Work Failed';
    document.getElementById('alch-result-desc').textContent = 'The operation produced no useful result. The matter blackened and fell to ash. Failure is instructive — adjust your materials and timing.';
    document.getElementById('alch-latin-desc').textContent = 'Opus nigredinem ingressum est. Materia in cineres resoluta est. Etiam in fallimento docetur.';
    addXP(2, 'Experiment performed');
  }

  appendAlchHistory(exp, true);
  saveState();
  updateSidebarStats();
  checkAchievements();
}

function appendAlchHistory(exp, prepend) {
  const list = document.getElementById('alch-history-list');
  const entry = document.createElement('div');
  entry.className = 'history-entry';
  const s = ALCHEMY.substances.find(x => x.id === exp.substance);
  const op = ALCHEMY.operations.find(x => x.id === exp.operation);
  entry.innerHTML = `
    <div class="history-result-name">${exp.result_name}</div>
    <div class="history-latin">${s ? s.name : exp.substance} + ${op ? op.name : exp.operation}</div>
  `;
  if (prepend && list.firstChild) list.insertBefore(entry, list.firstChild);
  else list.appendChild(entry);
}

// ===== STATS MODAL =====
function openStats() {
  document.getElementById('st-xp').textContent = STATE.xp;
  document.getElementById('st-level').textContent = getCurrentLevel().num;
  document.getElementById('st-words').textContent = Object.keys(STATE.wordsLooked).length;
  document.getElementById('st-read').textContent = Object.keys(STATE.passagesRead).length;
  document.getElementById('st-translated').textContent = Object.keys(STATE.passagesTranslated).length;
  document.getElementById('st-rituals').textContent = Object.keys(STATE.ritualsComplete).length;
  document.getElementById('st-experiments').textContent = STATE.experiments.length;
  document.getElementById('st-readlist').textContent = STATE.readList.length;

  const achList = document.getElementById('achievement-list');
  achList.innerHTML = ACHIEVEMENTS.map(a => `
    <div class="achievement-item${STATE.achievements[a.id] ? '' : ' locked'}">
      <span class="achievement-icon">${a.icon}</span>
      <div>
        <div class="achievement-name">${a.name}</div>
        <div class="achievement-desc">${a.desc}</div>
      </div>
    </div>
  `).join('');

  document.getElementById('stats-modal').removeAttribute('hidden');
  document.body.style.overflow = 'hidden';
}

// ===== READ LIST MODAL =====
function openReadList() {
  const container = document.getElementById('readlist-contents');
  if (!STATE.readList.length) {
    container.innerHTML = '<p style="color:var(--text-dim);font-style:italic">No passages in your read list yet. Open a passage and click "Add to Read List".</p>';
  } else {
    container.innerHTML = STATE.readList.map(id => {
      const p = PASSAGES.find(x => x.id === id);
      if (!p) return '';
      return `
        <div class="readlist-item" data-id="${id}">
          <div>
            <div class="readlist-item-title">${p.title}</div>
            <div class="readlist-item-author">${p.author} · ${p.date}</div>
          </div>
          <button class="readlist-item-remove" data-id="${id}" title="Remove">✕</button>
        </div>
      `;
    }).join('');
    container.querySelectorAll('.readlist-item').forEach(el => {
      el.addEventListener('click', e => {
        if (e.target.classList.contains('readlist-item-remove')) return;
        closeModal('readlist-modal');
        openPassage(el.dataset.id);
      });
    });
    container.querySelectorAll('.readlist-item-remove').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const id = btn.dataset.id;
        STATE.readList = STATE.readList.filter(x => x !== id);
        saveState();
        renderCards();
        openReadList();
      });
    });
  }
  document.getElementById('readlist-modal').removeAttribute('hidden');
  document.body.style.overflow = 'hidden';
}

// ===== PASSAGE NAVIGATION =====
function navigatePassage(dir) {
  if (!filteredPassages.length) return;
  const newIdx = currentPassageIndex + dir;
  if (newIdx < 0 || newIdx >= filteredPassages.length) return;
  openPassage(filteredPassages[newIdx].id);
}

// ===== FLASHCARD QUIZ =====
function openFlashcards() {
  const words = Object.keys(STATE.wordsLooked);
  const fc = document.getElementById('flashcard-modal');
  document.getElementById('fc-summary').hidden = true;
  document.getElementById('fc-score-btns').hidden = true;
  document.getElementById('fc-definition').hidden = true;
  document.getElementById('fc-lemma').hidden = true;

  if (!words.length) {
    document.getElementById('fc-word').textContent = '?';
    document.getElementById('fc-prompt').textContent = 'No words yet. Click Latin words in any passage to build your vocabulary.';
    document.getElementById('fc-progress').textContent = '0 / 0';
    document.getElementById('fc-reveal').hidden = true;
    fc.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    return;
  }

  // Shuffle words
  quizWords = [...words].sort(() => 0.5 - Math.random());
  quizIndex = 0;
  quizStats = { knew: 0, almost: 0, missed: 0, xpEarned: 0 };
  document.getElementById('fc-reveal').hidden = false;
  renderFlashcard();
  fc.removeAttribute('hidden');
  document.body.style.overflow = 'hidden';
}

function renderFlashcard() {
  if (quizIndex >= quizWords.length) {
    showFlashcardSummary();
    return;
  }
  const word = quizWords[quizIndex];
  document.getElementById('fc-progress').textContent = `${quizIndex + 1} / ${quizWords.length}`;
  document.getElementById('fc-word').textContent = word;
  document.getElementById('fc-prompt').textContent = 'What does this word mean?';
  document.getElementById('fc-definition').hidden = true;
  document.getElementById('fc-lemma').hidden = true;
  document.getElementById('fc-reveal').hidden = false;
  document.getElementById('fc-score-btns').hidden = true;
}

function revealFlashcard() {
  const word = quizWords[quizIndex];
  const def = window.LATIN_DICT && window.LATIN_DICT[word];
  const defEl = document.getElementById('fc-definition');
  const lemmaEl = document.getElementById('fc-lemma');
  defEl.textContent = def ? def.definition : '(not in dictionary)';
  defEl.hidden = false;
  if (def && def.lemma && def.lemma !== word) {
    lemmaEl.textContent = `← ${def.lemma}`;
    lemmaEl.hidden = false;
  } else {
    lemmaEl.hidden = true;
  }
  document.getElementById('fc-reveal').hidden = true;
  document.getElementById('fc-score-btns').hidden = false;
  document.getElementById('fc-prompt').textContent = '';
}

function scoreFlashcard(result) {
  let xp = 0;
  if (result === 'knew') { xp = 3; quizStats.knew++; }
  else if (result === 'almost') { xp = 1; quizStats.almost++; }
  else { quizStats.missed++; }
  if (xp) addXP(xp, 'Flashcard recalled');
  quizStats.xpEarned += xp;
  quizIndex++;
  renderFlashcard();
}

function showFlashcardSummary() {
  document.getElementById('fc-word').textContent = '✦';
  document.getElementById('fc-prompt').textContent = '';
  document.getElementById('fc-reveal').hidden = true;
  document.getElementById('fc-score-btns').hidden = true;
  document.getElementById('fc-progress').textContent = `${quizWords.length} / ${quizWords.length}`;
  document.getElementById('fc-summary-stats').innerHTML = `
    <span style="color:#7acc7a">✓ ${quizStats.knew}</span>
    <span style="color:var(--gold)">~ ${quizStats.almost}</span>
    <span style="color:#dd8888">✗ ${quizStats.missed}</span>
    <span style="color:var(--text-dim)">+${quizStats.xpEarned} XP</span>
  `;
  document.getElementById('fc-summary').hidden = false;
}

// ===== MODAL HELPERS =====
function closeModal(id) {
  document.getElementById(id).hidden = true;
  const anyOpen = ['passage-modal','ritual-modal','alchemy-modal','stats-modal','readlist-modal','flashcard-modal']
    .some(m => !document.getElementById(m).hidden);
  if (!anyOpen) document.body.style.overflow = '';
  hideTooltip();
}

// ===== SIDEBAR STATS =====
function updateSidebarStats() {
  document.getElementById('stat-passages-read').textContent = Object.keys(STATE.passagesRead).length;
  document.getElementById('stat-words-clicked').textContent = Object.keys(STATE.wordsLooked).length;
  document.getElementById('stat-translated').textContent = Object.keys(STATE.passagesTranslated).length;
  document.getElementById('stat-rituals').textContent = Object.keys(STATE.ritualsComplete).length;
  document.getElementById('stat-experiments').textContent = STATE.experiments.length;
}

// ===== UTILS =====
function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
  // Header buttons
  document.getElementById('btn-flashcards').addEventListener('click', openFlashcards);
  document.getElementById('btn-alchemy').addEventListener('click', openAlchemy);
  document.getElementById('btn-stats').addEventListener('click', openStats);
  document.getElementById('btn-readlist').addEventListener('click', openReadList);

  // Close buttons
  document.getElementById('passage-close').addEventListener('click', () => closeModal('passage-modal'));
  document.getElementById('ritual-close').addEventListener('click', () => closeModal('ritual-modal'));
  document.getElementById('alchemy-close').addEventListener('click', () => closeModal('alchemy-modal'));
  document.getElementById('stats-close').addEventListener('click', () => closeModal('stats-modal'));
  document.getElementById('readlist-close').addEventListener('click', () => closeModal('readlist-modal'));
  document.getElementById('flashcard-close').addEventListener('click', () => closeModal('flashcard-modal'));

  // Passage navigation
  document.getElementById('passage-prev').addEventListener('click', () => navigatePassage(-1));
  document.getElementById('passage-next').addEventListener('click', () => navigatePassage(1));

  // Flashcard quiz
  document.getElementById('fc-reveal').addEventListener('click', revealFlashcard);
  document.getElementById('fc-knew').addEventListener('click', () => scoreFlashcard('knew'));
  document.getElementById('fc-almost').addEventListener('click', () => scoreFlashcard('almost'));
  document.getElementById('fc-missed').addEventListener('click', () => scoreFlashcard('missed'));
  document.getElementById('fc-restart').addEventListener('click', openFlashcards);

  // Click outside modal to close
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) closeModal(overlay.id);
    });
  });

  // Filters
  document.querySelectorAll('.filter-era').forEach(cb => cb.addEventListener('change', renderCards));
  document.getElementById('diff-slider').addEventListener('input', () => {
    document.getElementById('diff-value').textContent = document.getElementById('diff-slider').value + ' ✦';
    renderCards();
  });
  document.getElementById('filter-read-list').addEventListener('change', renderCards);
  document.getElementById('filter-has-ritual').addEventListener('change', renderCards);
  document.getElementById('filter-unread').addEventListener('change', renderCards);
  document.getElementById('search-box').addEventListener('input', renderCards);

  // Scaffold buttons
  document.querySelectorAll('.scaf-btn').forEach(btn => {
    btn.addEventListener('click', () => setScaffold(btn.dataset.level));
  });

  // Gloss toggle
  setupGlossToggle();

  // Passage actions
  setupPassageActions();

  // Ritual navigation
  document.getElementById('ritual-prev').addEventListener('click', () => {
    if (currentRitualStep > 0) { currentRitualStep--; renderRitualStep(); }
  });
  document.getElementById('ritual-next').addEventListener('click', () => {
    if (currentRitual && currentRitualStep < currentRitual.steps.length - 1) {
      currentRitualStep++;
      renderRitualStep();
    }
  });
  document.getElementById('ritual-perform').addEventListener('click', () => {
    if (!currentRitual) return;
    ritualStepsPerformed.add(currentRitualStep);
    renderRitualStep();
    addXP(5, 'Ritual step performed');
    // Auto-advance
    if (currentRitualStep < currentRitual.steps.length - 1) {
      setTimeout(() => { currentRitualStep++; renderRitualStep(); }, 600);
    } else {
      // Check if all steps performed
      if (ritualStepsPerformed.size >= currentRitual.steps.length) {
        setTimeout(completeRitual, 800);
      }
    }
  });

  // Alchemy
  document.getElementById('alch-perform').addEventListener('click', performExperiment);

  // Stats reset
  document.getElementById('btn-reset').addEventListener('click', () => {
    if (confirm('Reset all progress? This cannot be undone.')) {
      localStorage.removeItem(STATE_KEY);
      location.reload();
    }
  });

  // Bibliography
  document.getElementById('btn-bibliography').addEventListener('click', openBibliography);
  document.getElementById('bibliography-close').addEventListener('click', () => closeModal('bibliography-modal'));
  document.querySelectorAll('.biblio-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.biblio-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderBibliography(tab.dataset.section);
    });
  });
  document.getElementById('biblio-search').addEventListener('input', () => {
    const activeTab = document.querySelector('.biblio-tab.active');
    renderBibliography(activeTab ? activeTab.dataset.section : 'primary');
  });

  // Hide tooltip on scroll/escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      hideTooltip();
      const modals = ['passage-modal','ritual-modal','alchemy-modal','stats-modal','readlist-modal','flashcard-modal','bibliography-modal'];
      for (const m of modals) {
        if (!document.getElementById(m).hidden) { closeModal(m); break; }
      }
    }
  });
  document.addEventListener('scroll', hideTooltip, true);
  document.getElementById('pm-latin').addEventListener('mouseleave', () => {
    if (scaffoldLevel !== 'full') hideTooltip();
  });
  document.getElementById('pm-latin').addEventListener('mousemove', e => {
    if (scaffoldLevel === 'full' && !e.target.classList.contains('latin-word')) {
      // reposition tooltip if visible
      const tip = document.getElementById('word-tooltip');
      if (!tip.hidden) positionTooltip(e, tip);
    }
  });
}

// ===== BIBLIOGRAPHY =====

const TRADITION_LABELS = {
  natural_magic: 'Natural Magic', hermetic: 'Hermetic', neoplatonic: 'Neoplatonic',
  angelic_magic: 'Angelic Magic', astrological: 'Astrological', alchemy: 'Alchemy',
  solomonic: 'Solomonic', folk_magic: 'Folk Magic', demonology: 'Demonology',
  kabbalistic: 'Kabbalistic', necromancy: 'Necromancy', divination: 'Divination',
  classification: 'Classification'
};

const SOURCE_LABELS = {
  passages: 'Corpus', medievalmagicdb: 'MedievalMagicDB', e_pdf_magic: 'PDF Library', scholarly: 'Scholarship'
};

function escapeHtml(str) {
  return (str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function renderBibliographyEntry(entry) {
  const eras = (entry.eras || []).filter(Boolean);
  const trads = (entry.traditions || []).filter(Boolean);
  const eraTags = eras.map(e => `<span class="biblio-tag era-tag">${e}</span>`).join('');
  const tradTags = trads.map(t => `<span class="biblio-tag">${TRADITION_LABELS[t] || t}</span>`).join('');

  const src = entry.source && entry.source !== 'passages'
    ? `<span class="biblio-tag" style="opacity:0.6">${SOURCE_LABELS[entry.source] || entry.source}</span>` : '';

  const passages = entry.passages || [];
  const countStr = passages.length > 0
    ? `${passages.length} passage${passages.length !== 1 ? 's' : ''}` : '';

  const desc = entry.description && entry.description !== 'Seeded from local PDF corpus manifest.'
    && entry.description !== 'Seeded from local corpus manifest: more_medieval_magic_manifest.json.'
    && entry.description !== 'Seeded from local corpus manifest: thorndike_pdf_manifest.json.'
    ? `<div class="biblio-entry-desc">${escapeHtml(entry.description)}</div>` : '';

  return `<div class="biblio-entry">
    <div class="biblio-entry-meta">
      <div class="biblio-entry-citation">${escapeHtml(entry.citation)}</div>
      ${desc}
      <div class="biblio-entry-tags">${eraTags}${tradTags}${src}</div>
      ${countStr ? `<div class="biblio-count">${countStr}</div>` : ''}
    </div>
  </div>`;
}

function filterBiblio(query) {
  if (!query) return BIBLIOGRAPHY;
  const q = query.toLowerCase();
  return BIBLIOGRAPHY.filter(e =>
    (e.citation || '').toLowerCase().includes(q) ||
    (e.description || '').toLowerCase().includes(q) ||
    (e.author || '').toLowerCase().includes(q)
  );
}

const BIBLIO_PAGE = 80;
let biblioCurrent = [];
let biblioOffset = 0;

function renderBiblioGroups(groups) {
  // groups = [{head, items}]
  // Flatten into a single sorted list for paging
  biblioCurrent = groups.flatMap(g => [{ _head: g.head, _count: g.items.length }, ...g.items]);
  biblioOffset = 0;
  renderBiblioPage();
}

function renderBiblioPage() {
  const container = document.getElementById('biblio-contents');
  const slice = biblioCurrent.slice(0, biblioOffset + BIBLIO_PAGE);
  const remaining = biblioCurrent.length - slice.length;
  let html = '';
  for (const item of slice) {
    if (item._head !== undefined) {
      html += `<div class="biblio-section-head">${item._head} (${item._count})</div>`;
    } else {
      html += renderBibliographyEntry(item);
    }
  }
  if (remaining > 0) {
    html += `<button class="biblio-load-more" id="biblio-load-more">Load ${Math.min(remaining, BIBLIO_PAGE)} more (${remaining} remaining)</button>`;
  }
  container.innerHTML = html;
  biblioOffset += BIBLIO_PAGE;
  const btn = document.getElementById('biblio-load-more');
  if (btn) btn.addEventListener('click', renderBiblioPage);
}

function renderBibliography(section) {
  const query = (document.getElementById('biblio-search').value || '').trim();
  const all = filterBiblio(query);

  if (section === 'primary') {
    const items = all.filter(e =>
      e.relevance === 'PRIMARY' || e.pub_type === 'PRIMARY_TEXT' || e.pub_type === 'EDITION'
    );
    if (!items.length) { document.getElementById('biblio-contents').innerHTML = `<div class="biblio-empty">No primary sources match.</div>`; return; }
    const corpus = items.filter(e => e.source === 'passages');
    const mdb = items.filter(e => e.source === 'medievalmagicdb');
    const other = items.filter(e => e.source !== 'passages' && e.source !== 'medievalmagicdb');
    const groups = [];
    if (corpus.length) groups.push({ head: `From the Corpus`, items: corpus });
    if (mdb.length) groups.push({ head: `From MedievalMagicDB`, items: mdb });
    if (other.length) groups.push({ head: `Editions &amp; Critical Texts`, items: other });
    renderBiblioGroups(groups);

  } else if (section === 'secondary') {
    const items = all.filter(e =>
      (e.relevance === 'SECONDARY' || e.pub_type === 'MONOGRAPH' || e.pub_type === 'ARTICLE' ||
      e.pub_type === 'COLLECTION' || e.pub_type === 'REVIEW') && e.pub_type !== 'PRIMARY_TEXT'
    );
    if (!items.length) { document.getElementById('biblio-contents').innerHTML = `<div class="biblio-empty">No secondary sources match.</div>`; return; }
    const corpus = items.filter(e => e.source === 'passages');
    const mdb = items.filter(e => e.source === 'medievalmagicdb');
    const pdf = items.filter(e => e.source === 'e_pdf_magic');
    const scholarly = items.filter(e => e.source === 'scholarly');
    const groups = [];
    if (corpus.length) groups.push({ head: `Cited in Corpus`, items: corpus });
    if (mdb.length) groups.push({ head: `From MedievalMagicDB`, items: mdb });
    if (pdf.length) groups.push({ head: `PDF Library`, items: pdf });
    if (scholarly.length) groups.push({ head: `Key Scholarship`, items: scholarly });
    renderBiblioGroups(groups);

  } else if (section === 'by-tradition') {
    const tradOrder = Object.keys(TRADITION_LABELS);
    const groups = [];
    for (const trad of tradOrder) {
      const items = all.filter(e => (e.traditions || []).includes(trad));
      if (items.length) groups.push({ head: TRADITION_LABELS[trad], items });
    }
    const unlinked = all.filter(e => !e.traditions || !e.traditions.some(Boolean));
    if (unlinked.length && !query) groups.push({ head: 'General / Cross-Traditional', items: unlinked });
    if (!groups.length) { document.getElementById('biblio-contents').innerHTML = `<div class="biblio-empty">No sources match.</div>`; return; }
    renderBiblioGroups(groups);

  } else if (section === 'all') {
    if (!all.length) { document.getElementById('biblio-contents').innerHTML = `<div class="biblio-empty">No sources match.</div>`; return; }
    renderBiblioGroups([{ head: `All Sources`, items: all }]);
  }
}

function openBibliography() {
  document.getElementById('bibliography-modal').hidden = false;
  document.querySelector('.biblio-tab.active')?.classList.remove('active');
  document.querySelector('.biblio-tab[data-section="primary"]').classList.add('active');
  document.getElementById('biblio-search').value = '';
  renderBibliography('primary');
}

// ===== START =====
document.addEventListener('DOMContentLoaded', init);
