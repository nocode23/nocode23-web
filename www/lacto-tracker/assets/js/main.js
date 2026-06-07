(function () {
  'use strict';

  /* ── 1. Nav scroll ───────────────────────────────────────── */
  const nav = document.getElementById('nav');
  const onScroll = () => {
    nav.classList.toggle('scrolled', window.scrollY > 20);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── 2 & 3. Sticky showcase IntersectionObserver ─────────── */
  const steps      = Array.from(document.querySelectorAll('.showcase-step'));
  const screenImgs = Array.from(document.querySelectorAll('#showcaseScreen img'));
  const dots       = Array.from(document.querySelectorAll('#showcaseDots .dot'));

  let currentStep = 0;

  function setActiveStep(index) {
    if (index === currentStep && steps[index].classList.contains('active')) return;
    currentStep = index;

    steps.forEach((s, i) => s.classList.toggle('active', i === index));
    screenImgs.forEach((img, i) => img.classList.toggle('active', i === index));
    dots.forEach((d, i) => {
      d.classList.toggle('active', i === index);
      d.setAttribute('aria-selected', i === index ? 'true' : 'false');
    });
  }

  const stepObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setActiveStep(parseInt(entry.target.dataset.step, 10));
      }
    });
  }, {
    threshold: 0.5,
    rootMargin: '-15% 0px -15% 0px'
  });

  steps.forEach(step => stepObserver.observe(step));

  /* ── 4. Dot click ────────────────────────────────────────── */
  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      const idx = parseInt(dot.dataset.index, 10);
      setActiveStep(idx);
      steps[idx].scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  /* ── 5. Fade-in observer for section headers ─────────────── */
  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.fade-in').forEach(el => fadeObserver.observe(el));

  /* ── 6. Feature cards staggered fade-in ──────────────────── */
  const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        cardObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.feature-card').forEach((card, i) => {
    card.style.transitionDelay = `${i * 80}ms`;
    cardObserver.observe(card);
  });

})();
