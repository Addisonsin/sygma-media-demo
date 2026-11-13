/**
 * Sygma Media — High-Performance Motion & Inertial Scroll Engine
 * Inspired by Aesthetic Launch Lab & Apple Keynote Microsites
 */

(function () {
  'use strict';

  // 1. Initialize Lenis Smooth Scroll (via script or fallback inertia loop)
  function initSmoothScroll() {
    if (typeof Lenis !== 'undefined') {
      const lenis = new Lenis({
        duration: 1.25,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 0.95,
        touchMultiplier: 1.5
      });

      function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
      }
      requestAnimationFrame(raf);
      window.lenis = lenis;
    }
  }

  // 2. Cursor Spotlight Effect on Bento & Case Cards
  function initSpotlight() {
    const cards = document.querySelectorAll('.bento-card, .luxury-case-card, .calc-card, .showcase-container');
    cards.forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    });
  }

  // 3. Ambient Cursor Light Follower
  function initCursorFollower() {
    if (window.innerWidth < 980) return;
    const light = document.createElement('div');
    light.className = 'cursor-light';
    document.body.appendChild(light);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function render() {
      // Linear interpolation for smooth trailing
      currentX += (mouseX - currentX) * 0.08;
      currentY += (mouseY - currentY) * 0.08;
      light.style.transform = `translate3d(${currentX - 250}px, ${currentY - 250}px, 0)`;
      requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
  }

  // 4. Scroll Reveal & Intersection Observer
  function initScrollReveal() {
    const revealTargets = document.querySelectorAll(
      '.hero-title, .hero-lead, .hero-actions, .showcase-container, .section-title, .section-subtitle, .bento-card, .luxury-case-card, .calc-card, .compare-container, .blueprint-cta-wrap'
    );

    revealTargets.forEach((el, index) => {
      el.classList.add('reveal');
      if (index % 3 === 1) el.classList.add('delay-1');
      if (index % 3 === 2) el.classList.add('delay-2');
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('active');
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
      }
    );

    revealTargets.forEach((el) => observer.observe(el));
  }

  // 5. Number Counter Animation on Visible Stats
  function initCounterAnimation() {
    const counters = document.querySelectorAll('.chart-metric-num, .bento-metric-val, .case-ribbon-stat strong');
    let animated = false;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !animated) {
          // Subtle pulse on number reveal
          entry.target.style.transition = 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
          entry.target.style.transform = 'scale(1.04)';
          setTimeout(() => {
            entry.target.style.transform = 'scale(1)';
          }, 400);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
  }

  // 6. Interactive 3D Tilt on Showcase Cockpit
  function initTilt() {
    const showcase = document.querySelector('.showcase-container');
    if (!showcase || window.innerWidth < 980) return;

    showcase.addEventListener('mousemove', (e) => {
      const rect = showcase.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      const tiltX = (y / rect.height) * -6; // max 6 deg
      const tiltY = (x / rect.width) * 6;

      showcase.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
    });

    showcase.addEventListener('mouseleave', () => {
      showcase.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
    });
  }

  // 7. Mobile Navigation Toggle
  function initNav() {
    const toggle = document.querySelector('.nav-toggle');
    const links = document.querySelector('.nav-links');
    if (toggle && links) {
      toggle.addEventListener('click', () => {
        links.classList.toggle('active');
        if (links.classList.contains('active')) {
          links.style.display = 'flex';
          links.style.flexDirection = 'column';
          links.style.position = 'fixed';
          links.style.top = '78px';
          links.style.left = '20px';
          links.style.right = '20px';
          links.style.background = '#0e1017';
          links.style.padding = '30px';
          links.style.borderRadius = '20px';
          links.style.border = '1px solid rgba(255,255,255,0.1)';
          links.style.boxShadow = '0 30px 60px rgba(0,0,0,0.8)';
          links.style.zIndex = '999';
        } else {
          links.style.display = '';
        }
      });
    }
  }

  // Initialize all motion modules on DOM Ready
  document.addEventListener('DOMContentLoaded', () => {
    initSmoothScroll();
    initSpotlight();
    initCursorFollower();
    initScrollReveal();
    initCounterAnimation();
    initTilt();
    initNav();
  });

})();
