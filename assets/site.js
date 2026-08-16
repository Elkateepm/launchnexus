/* LaunchNexus — shared behaviour. Kept deliberately small: no dependencies. */
(function () {
  'use strict';

  /* ---- Mobile drawer ---- */
  var toggle = document.querySelector('.nav-toggle');
  var drawer = document.getElementById('drawer');
  if (toggle && drawer) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      drawer.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) setOpen(false);
    });
  }

  /* ---- Sticky header shadow ---- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Scroll reveal ---- */
  var reveals = document.querySelectorAll('.rise');
  if (reveals.length) {
    if (!('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
      reveals.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---- Current year in footer ---- */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();

/* ==========================================================================
   Enquiry form — LaunchNexus
   Posts to Supabase if window.LNX_CONFIG is filled in (see assets/config.js),
   otherwise falls back to opening the visitor's email client so no enquiry is
   ever silently lost.
   ========================================================================== */
(function () {
  'use strict';

  var form = document.getElementById('enquiry-form');
  if (!form) return;

  var status = document.getElementById('form-status');
  var submit = form.querySelector('button[type="submit"]');
  var cfg = window.LNX_CONFIG || {};
  var configured = Boolean(cfg.supabaseUrl && cfg.supabaseAnonKey);

  var say = function (message, kind) {
    status.className = 'form-status' + (kind ? ' is-' + kind : '');
    status.textContent = message;
  };

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Honeypot: bots fill hidden fields, people don't.
    if (form.querySelector('[name="website"]').value) return;

    var data = {
      name: form.name_field.value.trim(),
      organisation: form.organisation.value.trim(),
      email: form.email.value.trim(),
      service: (form.querySelector('input[name="service"]:checked') || {}).value || 'Not sure yet',
      message: form.message.value.trim(),
      budget: form.budget.value.trim() || null,
      target_date: form.target_date.value || null,
      status: 'New'
    };

    if (!configured) {
      // No backend wired up yet — hand off to email rather than pretend it sent.
      var body = 'Name: ' + data.name +
        '\nOrganisation: ' + data.organisation +
        '\nEmail: ' + data.email +
        '\nLooking for: ' + data.service +
        '\nBudget: ' + (data.budget || 'Not given') +
        '\nIdeal launch date: ' + (data.target_date || 'Not given') +
        '\n\n' + data.message;
      window.location.href = 'mailto:info@launchnexus.co.uk?subject=' +
        encodeURIComponent('Project enquiry — ' + (data.organisation || data.name)) +
        '&body=' + encodeURIComponent(body);
      return;
    }

    submit.disabled = true;
    say('Sending…', 'busy');

    fetch(cfg.supabaseUrl + '/rest/v1/enquiries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        apikey: cfg.supabaseAnonKey,
        Authorization: 'Bearer ' + cfg.supabaseAnonKey,
        Prefer: 'return=minimal'
      },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        if (!res.ok) throw new Error('Request failed: ' + res.status);
        window.location.href = 'thanks.html';
      })
      .catch(function () {
        submit.disabled = false;
        say('That didn\u2019t send. Please email info@launchnexus.co.uk and we\u2019ll pick it up from there.', 'error');
      });
  });
})();
