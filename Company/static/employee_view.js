// employee_view.js — Search, view toggle, delete modal
document.addEventListener('DOMContentLoaded', () => {

  const searchInput = document.getElementById('searchInput');
  const empGrid = document.getElementById('empGrid');
  const noResults = document.getElementById('noResults');
  const empTotalCount = document.getElementById('empTotalCount');
  const gridViewBtn = document.getElementById('gridViewBtn');
  const listViewBtn = document.getElementById('listViewBtn');
  const cards = document.querySelectorAll('.emp-card');

  // --- Live Search ---
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase().trim();
      let visible = 0;
      cards.forEach(card => {
        const name = card.dataset.name || '';
        const dept = card.dataset.dept || '';
        const matches = name.includes(query) || dept.includes(query) || query === '';
        card.style.display = matches ? '' : 'none';
        if (matches) visible++;
      });
      if (empTotalCount) empTotalCount.textContent = visible;
      if (noResults) noResults.style.display = visible === 0 ? 'flex' : 'none';
    });
  }

  // --- View Toggle ---
  if (gridViewBtn && listViewBtn && empGrid) {
    gridViewBtn.addEventListener('click', () => {
      empGrid.classList.remove('list-view');
      gridViewBtn.classList.add('active');
      listViewBtn.classList.remove('active');
    });
    listViewBtn.addEventListener('click', () => {
      empGrid.classList.add('list-view');
      listViewBtn.classList.add('active');
      gridViewBtn.classList.remove('active');
    });
  }

  // --- Card stagger entrance ---
  cards.forEach((card, i) => {
    card.style.animationDelay = `${i * 0.06}s`;
    card.style.animationPlayState = 'running';
  });
});

// --- Delete Confirmation Modal ---
let pendingDeleteUrl = '';

window.confirmDelete = function(name) {
  const modal = document.getElementById('deleteModal');
  const msg = document.getElementById('deleteModalMsg');
  const btn = document.getElementById('deleteConfirmBtn');
  if (!modal) return true;

  const link = document.activeElement.closest('a');
  if (link) pendingDeleteUrl = link.href;

  if (msg) msg.textContent = `Are you sure you want to delete "${name}"? This action cannot be undone.`;
  if (btn) btn.href = pendingDeleteUrl;

  modal.classList.add('active');
  return false;
};

window.closeModal = function() {
  const modal = document.getElementById('deleteModal');
  if (modal) modal.classList.remove('active');
};

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') window.closeModal();
});

document.getElementById('deleteModal')?.addEventListener('click', (e) => {
  if (e.target === e.currentTarget) window.closeModal();
});
