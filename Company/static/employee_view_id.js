// employee_view_id.js
window.confirmDelete = function() {
  const modal = document.getElementById('deleteModal');
  if (modal) { modal.classList.add('active'); return false; }
  return true;
};

window.closeModal = function() {
  const modal = document.getElementById('deleteModal');
  if (modal) modal.classList.remove('active');
};

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') window.closeModal();
});

document.getElementById('deleteModal')?.addEventListener('click', function(e) {
  if (e.target === this) window.closeModal();
});
