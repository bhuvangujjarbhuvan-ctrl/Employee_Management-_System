// message.js — Confetti celebration animation
document.addEventListener('DOMContentLoaded', () => {
  const confettiContainer = document.getElementById('confetti');
  if (!confettiContainer) return;

  const colors = [
    '#6480ff', '#b464ff', '#28c878', '#f0aa28',
    '#ff6480', '#64c8ff', '#ffffff'
  ];

  function createConfettiPiece() {
    const piece = document.createElement('div');
    const size = Math.random() * 10 + 4;
    const color = colors[Math.floor(Math.random() * colors.length)];
    const left = Math.random() * 100;
    const delay = Math.random() * 1.5;
    const duration = Math.random() * 2 + 2;
    const shape = Math.random() > 0.5 ? '50%' : '0';

    piece.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      background: ${color};
      left: ${left}%;
      top: -10px;
      border-radius: ${shape};
      animation: confettiFall ${duration}s ${delay}s ease-in forwards;
      opacity: 0.9;
    `;
    confettiContainer.appendChild(piece);
    setTimeout(() => piece.remove(), (delay + duration) * 1000 + 100);
  }

  // Inject keyframe
  const style = document.createElement('style');
  style.textContent = `
    @keyframes confettiFall {
      0% { transform: translateY(-10px) rotate(0deg); opacity: 0.9; }
      100% { transform: translateY(calc(100vh + 50px)) rotate(${Math.random() * 720}deg); opacity: 0; }
    }
  `;
  document.head.appendChild(style);

  // Fire confetti
  for (let i = 0; i < 60; i++) {
    setTimeout(createConfettiPiece, i * 30);
  }

  // Auto redirect after 5 seconds (optional - commented)
  // setTimeout(() => window.location.href = '/employee/view/', 5000);
});
