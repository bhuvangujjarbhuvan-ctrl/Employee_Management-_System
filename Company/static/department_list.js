// department_list.js — search + delete modal
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('deptSearch');
  const deptGrid = document.getElementById('deptGrid');
  const noResults = document.getElementById('noResults');
  const cards = document.querySelectorAll('.dept-card');

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase().trim();
      let visible = 0;
      cards.forEach(card => {
        const name = card.dataset.name || '';
        const matches = name.includes(query) || query === '';
        card.style.display = matches ? '' : 'none';
        if (matches) visible++;
      });
      if (noResults) noResults.style.display = visible === 0 ? 'flex' : 'none';
    });
  }

  // Stagger animation for cards
  cards.forEach((card, i) => {
    card.style.animationDelay = `${i * 0.08}s`;
  });
});

// Delete modal
window.confirmDelete = function(name, href) {
  const modal = document.getElementById('deleteModal');
  const msg = document.getElementById('deleteModalMsg');
  const btn = document.getElementById('deleteConfirmBtn');
  if (!modal) return true;

  if (msg) msg.textContent = `Are you sure you want to delete the "${name}" department? This action cannot be undone.`;
  if (btn) btn.href = href;

  modal.classList.add('active');
  return false;
};

window.closeModal = function() {
  const modal = document.getElementById('deleteModal');
  if (modal) modal.classList.remove('active');
};

document.addEventListener('keydown', (e) => { if (e.key === 'Escape') window.closeModal(); });
document.getElementById('deleteModal')?.addEventListener('click', function(e) {
  if (e.target === this) window.closeModal();
});
