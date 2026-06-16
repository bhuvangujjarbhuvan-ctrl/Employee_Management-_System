// employee_form.js — Live validation + submit animation
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('empForm');
  if (!form) return;

  const inputs = form.querySelectorAll('.form-input[required]');

  // Live validation on blur
  inputs.forEach(input => {
    input.addEventListener('blur', () => validateField(input));
    input.addEventListener('input', () => {
      if (input.classList.contains('is-invalid')) validateField(input);
    });
  });

  function validateField(input) {
    const parent = input.closest('.form-group');
    const existingError = parent ? parent.querySelector('.field-error') : null;
    if (existingError) existingError.remove();

    let isValid = true;
    let errorMsg = '';
    const isSelect = input.tagName === 'SELECT';

    if (!input.value.trim()) {
      isValid = false;
      errorMsg = isSelect ? 'Please select a department' : 'This field is required';
    } else if (!isSelect && input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
      isValid = false;
      errorMsg = 'Please enter a valid email address';
    } else if (!isSelect && input.type === 'number') {
      const val = parseInt(input.value);
      if (isNaN(val) || val < 18 || val > 80) {
        isValid = false;
        errorMsg = 'Age must be between 18 and 80';
      }
    }

    if (!isValid) {
      input.classList.add('is-invalid');
      input.classList.remove('is-valid');
      const err = document.createElement('div');
      err.className = 'field-error';
      err.textContent = errorMsg;
      if (parent) parent.appendChild(err);
    } else {
      input.classList.remove('is-invalid');
      input.classList.add('is-valid');
    }
    return isValid;
  }

  // Submit handler
  form.addEventListener('submit', (e) => {
    let allValid = true;
    inputs.forEach(input => {
      if (!validateField(input)) allValid = false;
    });

    if (!allValid) {
      e.preventDefault();
      // Shake the form card
      const card = document.querySelector('.form-card');
      if (card) {
        card.style.animation = 'shake 0.4s ease';
        setTimeout(() => card.style.animation = '', 400);
      }
      return;
    }

    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
      submitBtn.classList.add('btn-loading');
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = '<span>Processing...</span>';
    }
  });

  // Inject shake animation
  const style = document.createElement('style');
  style.textContent = `
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20% { transform: translateX(-8px); }
      40% { transform: translateX(8px); }
      60% { transform: translateX(-6px); }
      80% { transform: translateX(6px); }
    }
  `;
  document.head.appendChild(style);

  // Reset clears validation states
  form.addEventListener('reset', () => {
    setTimeout(() => {
      inputs.forEach(input => {
        input.classList.remove('is-valid', 'is-invalid');
        const parent = input.closest('.form-group');
        const err = parent ? parent.querySelector('.field-error') : null;
        if (err) err.remove();
      });
    }, 10);
  });
});
