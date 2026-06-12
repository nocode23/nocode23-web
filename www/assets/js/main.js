// Scroll reveal
const obs = new IntersectionObserver(
  (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); }),
  { threshold: 0.1 }
);
document.querySelectorAll('.reveal').forEach(el => obs.observe(el));

// Blob physics — pomalé plutí, odpuzování od kurzoru, odrazy od stěn i sebe navzájem.
// Pozicuje se přes transform (bez layout přepočtu); základní pozice v CSS
// zůstávají jako fallback bez JS / s reduced motion.
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const els = ['bl1','bl2','bl3','bl4'].map(c => document.querySelector('.' + c)).filter(Boolean);
  if (!els.length) return;

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
      // CSS pozice nahrazuje JS — ukotvit do levého horního rohu a hýbat transformem
      el.style.left = '0'; el.style.top = '0';
      el.style.right = 'auto'; el.style.bottom = 'auto';
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

      b.el.style.transform = `translate3d(${b.x - b.r}px, ${b.y - b.r}px, 0)`;
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

// Scrollspy — zvýraznění aktivní sekce v navigaci
(function () {
  const links = [...document.querySelectorAll('.nav-links a[href^="#"]')];
  if (!links.length) return;
  const sections = links
    .map(a => document.getElementById(a.getAttribute('href').slice(1)))
    .filter(Boolean);

  const spy = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
    });
  }, { rootMargin: '-40% 0px -55% 0px' });

  sections.forEach(s => spy.observe(s));
})();
