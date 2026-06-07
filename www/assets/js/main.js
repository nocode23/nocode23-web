if (typeof lucide !== 'undefined') lucide.createIcons();

// Scroll reveal
const obs = new IntersectionObserver(
  (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); }),
  { threshold: 0.1 }
);
document.querySelectorAll('.reveal').forEach(el => obs.observe(el));

// Blob physics engine
(function () {
  const els = ['bl1','bl2','bl3','bl4'].map(c => document.querySelector('.' + c));

  const speeds = [0.55, 0.75, 0.60, 0.90];
  const angles = [0.4,  2.3,  4.1,  5.5 ];

  let blobs = [];
  let mx = -9999, my = -9999;

  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
  document.addEventListener('mouseleave', () => { mx = -9999; my = -9999; });

  function init() {
    const W = window.innerWidth, H = window.innerHeight;
    blobs = els.map((el, i) => {
      const r = el.offsetWidth / 2;
      return {
        el, r,
        speed: speeds[i],
        x: r + Math.random() * (W - 2 * r),
        y: r + Math.random() * (H - 2 * r),
        vx: Math.cos(angles[i]) * speeds[i],
        vy: Math.sin(angles[i]) * speeds[i],
      };
    });
  }

  function tick() {
    const W = window.innerWidth, H = window.innerHeight;

    blobs.forEach(b => {
      // Odpuzování od kurzoru
      const mdx = b.x - mx, mdy = b.y - my;
      const mdist = Math.sqrt(mdx * mdx + mdy * mdy);
      if (mdist < 280 && mdist > 0.01) {
        const force = (1 - mdist / 280) * 1.0;
        b.vx += (mdx / mdist) * force;
        b.vy += (mdy / mdist) * force;
      }

      // Postupný návrat na původní rychlost
      const spd = Math.sqrt(b.vx * b.vx + b.vy * b.vy);
      if (spd > b.speed && spd > 0.01) {
        const ratio = 1 - (spd - b.speed) / spd * 0.04;
        b.vx *= ratio;
        b.vy *= ratio;
      }

      b.x += b.vx;
      b.y += b.vy;

      if (b.x - b.r < 0)  { b.x = b.r;     b.vx =  Math.abs(b.vx); }
      if (b.x + b.r > W)  { b.x = W - b.r; b.vx = -Math.abs(b.vx); }
      if (b.y - b.r < 0)  { b.y = b.r;     b.vy =  Math.abs(b.vy); }
      if (b.y + b.r > H)  { b.y = H - b.r; b.vy = -Math.abs(b.vy); }

      b.el.style.left = (b.x - b.r) + 'px';
      b.el.style.top  = (b.y - b.r) + 'px';
    });

    // Blob–blob kolize
    for (let i = 0; i < blobs.length; i++) {
      for (let j = i + 1; j < blobs.length; j++) {
        const a = blobs[i], b = blobs[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const min  = (a.r + b.r) * 0.5;
        if (dist < min && dist > 0.01) {
          const nx = dx / dist, ny = dy / dist;
          const rv = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny;
          if (rv < 0) {
            a.vx -= rv * nx; a.vy -= rv * ny;
            b.vx += rv * nx; b.vy += rv * ny;
          }
        }
      }
    }

    requestAnimationFrame(tick);
  }

  init();
  tick();
  window.addEventListener('resize', init);
})();

// Desktop-only: cursor + spotlight
if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  const spotlight = document.createElement('div');
  spotlight.className = 'cursor-spotlight';
  document.body.insertBefore(spotlight, document.body.firstChild);

  const dot = document.createElement('div');
  dot.className = 'cursor-dot';
  const ring = document.createElement('div');
  ring.className = 'cursor-ring';
  document.body.appendChild(dot);
  document.body.appendChild(ring);
  document.body.classList.add('custom-cursor');

  let mx = -200, my = -200;
  let rx = -200, ry = -200;

  document.addEventListener('mousemove', e => {
    mx = e.clientX;
    my = e.clientY;
    dot.style.left = mx + 'px';
    dot.style.top  = my + 'px';
    spotlight.style.opacity = '1';
    spotlight.style.background = `radial-gradient(520px circle at ${mx}px ${my}px, rgba(79,142,247,.08), transparent 60%)`;
  });

  document.addEventListener('mouseleave', () => { spotlight.style.opacity = '0'; });

  (function cursorLoop() {
    rx += (mx - rx) * 0.11;
    ry += (my - ry) * 0.11;
    ring.style.left = rx + 'px';
    ring.style.top  = ry + 'px';
    requestAnimationFrame(cursorLoop);
  })();

  document.querySelectorAll('a, button').forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('is-hover'));
    el.addEventListener('mouseleave', () => ring.classList.remove('is-hover'));
  });
}

// Typewriter hero tagline
const tagline = document.querySelector('.hero-tagline');
if (tagline) {
  const text = tagline.textContent.trim();
  tagline.textContent = '';
  tagline.style.cssText = 'opacity:1;transform:none;animation:none;';

  const caret = document.createElement('span');
  caret.className = 'type-cursor';
  tagline.appendChild(caret);

  let i = 0;
  setTimeout(() => {
    const id = setInterval(() => {
      if (i < text.length) {
        tagline.insertBefore(document.createTextNode(text[i++]), caret);
      } else {
        clearInterval(id);
        setTimeout(() => { caret.style.opacity = '0'; }, 2500);
      }
    }, 38);
  }, 900);
}
