// dept_form.js — Department form validation
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('deptForm');
  if (!form) return;

  const inputs = form.querySelectorAll('.form-input[required]');

  inputs.forEach(input => {
    input.addEventListener('blur', () => validateField(input));
    input.addEventListener('input', () => {
      if (input.classList.contains('is-invalid')) validateField(input);
    });
  });

  function validateField(input) {
    const parent = input.parentElement.parentElement;
    const existing = parent.querySelector('.field-error');
    if (existing) existing.remove();

    let isValid = true;
    let errorMsg = '';

    if (!input.value.trim()) {
      isValid = false; errorMsg = 'This field is required';
    } else if (input.type === 'number' && (isNaN(parseInt(input.value)) || parseInt(input.value) < 0)) {
      isValid = false; errorMsg = 'Please enter a valid number';
    }

    if (!isValid) {
      input.classList.add('is-invalid'); input.classList.remove('is-valid');
      const err = document.createElement('div');
      err.className = 'field-error'; err.textContent = errorMsg;
      parent.appendChild(err);
    } else {
      input.classList.remove('is-invalid'); input.classList.add('is-valid');
    }
    return isValid;
  }

  form.addEventListener('submit', (e) => {
    let allValid = true;
    inputs.forEach(input => { if (!validateField(input)) allValid = false; });
    if (!allValid) {
      e.preventDefault();
      const card = document.querySelector('.form-card');
      if (card) { card.style.animation = 'shake 0.4s ease'; setTimeout(() => card.style.animation = '', 400); }
      return;
    }
    const btn = document.getElementById('submitBtn');
    if (btn) { btn.classList.add('btn-loading'); btn.querySelector('span') && (btn.innerHTML = '<span>Processing...</span>'); }
  });

  const style = document.createElement('style');
  style.textContent = `@keyframes shake { 0%,100%{transform:translateX(0)} 20%{transform:translateX(-8px)} 40%{transform:translateX(8px)} 60%{transform:translateX(-6px)} 80%{transform:translateX(6px)} }`;
  document.head.appendChild(style);

  form.addEventListener('reset', () => {
    setTimeout(() => {
      inputs.forEach(input => {
        input.classList.remove('is-valid', 'is-invalid');
        const err = input.parentElement.parentElement.querySelector('.field-error');
        if (err) err.remove();
      });
    }, 10);
  });
});
