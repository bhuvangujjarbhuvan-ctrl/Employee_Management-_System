// home.js — Dynamic stat counts animation
document.addEventListener('DOMContentLoaded', () => {
  // Animate count-up for stat values
  function animateCount(el, target, duration = 1200) {
    if (isNaN(target)) { el.textContent = target; return; }
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) { el.textContent = target; clearInterval(timer); return; }
      el.textContent = Math.floor(start);
    }, 16);
  }

  // Card tilt on mouse move
  document.querySelectorAll('.nav-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `translateY(-6px) rotateY(${x * 5}deg) rotateX(${-y * 5}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = 'transform 0.5s ease';
    });
    card.addEventListener('mouseenter', () => {
      card.style.transition = 'transform 0.1s ease';
    });
  });

  // Particle sparkle on quick-btn hover
  document.querySelectorAll('.quick-btn').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
      for (let i = 0; i < 5; i++) {
        const spark = document.createElement('div');
        spark.style.cssText = `
          position: absolute;
          width: 4px; height: 4px;
          background: var(--primary-light);
          border-radius: 50%;
          pointer-events: none;
          left: ${Math.random() * 100}%;
          top: ${Math.random() * 100}%;
          animation: sparkle 0.6s ease forwards;
          opacity: 0.8;
        `;
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(spark);
        setTimeout(() => spark.remove(), 600);
      }
    });
  });

  const style = document.createElement('style');
  style.textContent = `
    @keyframes sparkle {
      0% { transform: scale(0) translate(0,0); opacity: 0.8; }
      100% { transform: scale(1.5) translate(${Math.random()*40-20}px, ${Math.random()*40-20}px); opacity: 0; }
    }
  `;
  document.head.appendChild(style);

  // Read real counts from data-count attributes (set by Django context)
  const empEl = document.getElementById('empCount');
  const deptEl = document.getElementById('deptCount');
  if (empEl) {
    const target = parseInt(empEl.dataset.count || '0');
    empEl.textContent = '0'; // reset to 0 first, then animate up
    animateCount(empEl, target);
  }
  if (deptEl) {
    const target = parseInt(deptEl.dataset.count || '0');
    deptEl.textContent = '0';
    animateCount(deptEl, target);
  }
});
