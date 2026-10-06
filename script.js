// Sygma Media — Purposeful, Subtle Interactivity & Animations

document.addEventListener('DOMContentLoaded', () => {
  // 1. Highlight active navigation item based on window.location
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navlinks a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // 2. Mobile Menu Toggle
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.navlinks');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isVisible = navLinks.style.display === 'flex';
      navLinks.style.display = isVisible ? 'none' : 'flex';
      if (!isVisible) {
        navLinks.style.flexDirection = 'column';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '78px';
        navLinks.style.left = '0';
        navLinks.style.right = '0';
        navLinks.style.background = '#FFFFFF';
        navLinks.style.padding = '24px 28px';
        navLinks.style.boxShadow = '0 16px 40px rgba(0,0,0,0.1)';
        navLinks.style.borderBottom = '1px solid var(--line)';
      }
    });
  }

  // 3. Subtle Scroll Reveal (Intersection Observer)
  const fadeElements = document.querySelectorAll('.fade-up, .service, .plan, .person, .proofItem');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    fadeElements.forEach(el => {
      el.classList.add('fade-up');
      observer.observe(el);
    });
  } else {
    fadeElements.forEach(el => el.classList.add('visible'));
  }

  // 4. Subtle Number Count-Up for Stat Numbers
  const statNumbers = document.querySelectorAll('.proofItem b, .caseStats b');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const countObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          countObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    statNumbers.forEach(el => countObserver.observe(el));
  }

  function animateCount(el) {
    const text = el.innerText.trim();
    // Parse prefixes and numbers
    const match = text.match(/^([$]?)([0-9,]+(\.[0-9]+)?)([×x%]?)$/);
    if (!match) return;

    const prefix = match[1];
    const rawNum = parseFloat(match[2].replace(/,/g, ''));
    const isDecimal = match[2].includes('.');
    const suffix = match[4];

    if (isNaN(rawNum)) return;

    const duration = 1200;
    const startTime = performance.now();

    function updateNumber(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out quartic
      const ease = 1 - Math.pow(1 - progress, 4);
      const current = rawNum * ease;

      const formatted = isDecimal 
        ? current.toFixed(2)
        : Math.round(current).toLocaleString();

      el.innerText = `${prefix}${formatted}${suffix}`;

      if (progress < 1) {
        requestAnimationFrame(updateNumber);
      } else {
        el.innerText = text;
      }
    }

    requestAnimationFrame(updateNumber);
  }

  // 5. Contact Form Interactive Feedback
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const notice = document.getElementById('formNotice');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Request Sent &check;';
        submitBtn.style.opacity = '0.9';
      }
      if (notice) {
        notice.style.display = 'block';
        notice.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  }
});
