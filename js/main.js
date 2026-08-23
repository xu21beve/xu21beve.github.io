// ============================================
// BEVERLY XU PORTFOLIO — main.js
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  // ---- LOADER ----
  const loader = document.getElementById('loader');
  if (loader) {
    // Fallback: always hide after 2.5s regardless
    const hideLoader = () => loader.classList.add('hide');
    window.addEventListener('load', () => setTimeout(hideLoader, 400));
    setTimeout(hideLoader, 2500); // safety net
  }

  // ---- CUSTOM CURSOR ----
  const dot  = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');
  let mouseX = 0, mouseY = 0;
  let ringX  = 0, ringY  = 0;

  document.addEventListener('mousemove', e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    if (dot) {
      dot.style.left = mouseX + 'px';
      dot.style.top  = mouseY + 'px';
    }
  });

  function animRing() {
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;
    if (ring) {
      ring.style.left = ringX + 'px';
      ring.style.top  = ringY + 'px';
    }
    requestAnimationFrame(animRing);
  }
  animRing();

  // Hover state
  const hoverEls = document.querySelectorAll('a, button, .project-icon, .research-header, [data-hover]');
  hoverEls.forEach(el => {
    el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
  });

  // ---- DARK MODE TOGGLE ----
  const darkToggle = document.getElementById('dark-toggle');
  if (darkToggle) {
    const saved = localStorage.getItem('bev-dark');
    if (saved === 'true') document.body.classList.add('dark');
    // Initialize button text to reflect current mode (keep sun/moon icons)
    darkToggle.textContent = document.body.classList.contains('dark') ? '☀ light' : '◑ dark';
    darkToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark');
      localStorage.setItem('bev-dark', document.body.classList.contains('dark'));
      // Update label: show "☀ light" when in dark mode, "◑ dark" when in light mode
      darkToggle.textContent = document.body.classList.contains('dark') ? '☀ light' : '◑ dark';
    });
  }

  // ---- NAVBAR SCROLL + ACTIVE ----
  const navbar  = document.getElementById('navbar');
  const navLinks = document.querySelectorAll('.nav-links a');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    if (!navbar) return;
    navbar.classList.toggle('scrolled', window.scrollY > 80);

    // Update active link
    let current = '';
    sections.forEach(sec => {
      const top = sec.offsetTop - 200;
      if (window.scrollY >= top) current = sec.id;
    });
    navLinks.forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === `#${current}` || a.getAttribute('href') === `./${current}.html`);
    });
  });

  // ---- SCROLL REVEAL ----
  const revealEls = document.querySelectorAll('.scroll-reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealEls.forEach(el => revealObserver.observe(el));

  // ---- ORBITING LEAF (Projects page) ----
  const leafOrbit = document.querySelector('.leaf-orbit');
  const leafWrap  = document.querySelector('.leaf-orbit-wrap');
  const trails    = [];

  if (leafOrbit && leafWrap) {
    let scrollY = 0;
    let angle   = 0;
    const RADIUS = 160;

    // Create trail dots
    for (let i = 0; i < 12; i++) {
      const t = document.createElement('div');
      t.className = 'leaf-trail';
      document.body.appendChild(t);
      trails.push({ el: t, x: 0, y: 0 });
    }

    // Anchor to center of projects section
    function getAnchorCenter() {
      const projSec = document.getElementById('projects');
      if (!projSec) return { cx: window.innerWidth / 2, cy: window.innerHeight / 2 };
      const rect = projSec.getBoundingClientRect();
      const cy = rect.top + rect.height * 0.38;
      const cx = rect.left + rect.width * 0.72;
      return { cx, cy };
    }

    let leafX = 0, leafY = 0;

    function animLeaf() {
      // angle advances with scroll
      angle = window.scrollY * 0.003;
      const { cx, cy } = getAnchorCenter();
      leafX = cx + Math.cos(angle) * RADIUS;
      leafY = cy + Math.sin(angle) * RADIUS;

      leafOrbit.style.left = leafX + 'px';
      leafOrbit.style.top  = leafY + 'px';
      leafOrbit.style.transform = `rotate(${angle * 30}deg)`;

      // Update trail
      for (let i = trails.length - 1; i > 0; i--) {
        trails[i].x = trails[i-1].x;
        trails[i].y = trails[i-1].y;
      }
      trails[0].x = leafX;
      trails[0].y = leafY;

      trails.forEach((t, i) => {
        t.el.style.left    = t.x + 'px';
        t.el.style.top     = t.y + 'px';
        t.el.style.opacity = (1 - i / trails.length) * 0.5;
        const s = (1 - i / trails.length) * 8;
        t.el.style.width  = s + 'px';
        t.el.style.height = s + 'px';
        t.el.style.transform = 'translate(-50%, -50%)';
      });

      requestAnimationFrame(animLeaf);
    }
    animLeaf();
  }

  // ---- PROJECT MODALS (moved to projects.html page-specific script) ----
  // This code now runs in projects.html only to avoid DOM selector issues on other pages

  // ---- PAGE INDICATOR (Projects) ----
  const pageDots = document.querySelectorAll('.page-dot');
  if (pageDots.length) {
    pageDots[0].classList.add('active');
    pageDots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        pageDots.forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
      });
    });
  }

  // ---- RESEARCH ACCORDION ----
  const researchItems = document.querySelectorAll('.research-item');
  researchItems.forEach(item => {
    const header = item.querySelector('.research-header');
    if (header) {
      header.addEventListener('click', () => {
        item.classList.toggle('expanded');
      });
    }
  });

  // ---- WIFI TOAST (simulate disconnect) ----
  const wifiToast = document.getElementById('wifi-toast');
  function showWifiToast() {
    if (!wifiToast) return;
    wifiToast.classList.add('show');
    setTimeout(() => wifiToast.classList.remove('show'), 4500);
  }

  // Show on actual connection change
  window.addEventListener('offline', showWifiToast);

  // Also demo after 8s if on main page (just to show it works)
  // Demo removed: don't auto-show the wifi toast after 8s on the homepage
  // if (document.body.dataset.page === 'home') {
  //   setTimeout(showWifiToast, 8000);
  // }

  const wifiDismiss = document.getElementById('wifi-dismiss');
  if (wifiDismiss) wifiDismiss.addEventListener('click', () => wifiToast.classList.remove('show'));

});
