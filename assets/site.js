/* LaunchNexus — shared behaviour. Kept deliberately small: no dependencies. */
(function () {
  'use strict';

  /* ---- Mobile drawer ---- */
  var toggle = document.querySelector('.nav-toggle');
  var drawer = document.getElementById('drawer');
  if (toggle && drawer) {
    var scrollY = 0;
    var siblings = [];

    var focusables = function () {
      return drawer.querySelectorAll('a[href], button:not([disabled])');
    };

    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      drawer.classList.toggle('is-open', open);

      // Hide the rest of the page from assistive tech and from tabbing, so
      // keyboard and screen-reader users can't wander behind the drawer.
      if (!siblings.length) {
        siblings = Array.prototype.filter.call(document.body.children, function (el) {
          return el !== drawer;
        });
      }
      siblings.forEach(function (el) {
        if (open) {
          el.setAttribute('aria-hidden', 'true');
          if ('inert' in HTMLElement.prototype) el.inert = true;
        } else {
          el.removeAttribute('aria-hidden');
          if ('inert' in HTMLElement.prototype) el.inert = false;
        }
      });
      // The toggle itself lives inside the header, so re-expose it.
      if (open) {
        toggle.removeAttribute('aria-hidden');
        if ('inert' in HTMLElement.prototype) toggle.inert = false;
      }

      if (open) {
        // position:fixed beats overflow:hidden on mobile Safari, which keeps
        // scrolling the document behind a fixed overlay during touch drags.
        scrollY = window.scrollY;
        document.body.style.position = 'fixed';
        document.body.style.top = -scrollY + 'px';
        document.body.style.width = '100%';
        var first = focusables()[0];
        if (first) first.focus();
      } else {
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        window.scrollTo(0, scrollY);
      }
    };

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });

    document.addEventListener('keydown', function (e) {
      if (toggle.getAttribute('aria-expanded') !== 'true') return;

      if (e.key === 'Escape') {
        setOpen(false);
        toggle.focus();
        return;
      }

      // Keep Tab inside the drawer while it's open.
      if (e.key === 'Tab') {
        var items = focusables();
        if (!items.length) return;
        var first = items[0];
        var last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 900 && toggle.getAttribute('aria-expanded') === 'true') setOpen(false);
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
   Enquiry form.

   The form has a real action/method, so it still works with JavaScript
   disabled: the endpoint answers a plain POST with a 303 to thanks.html.
   With JS, we submit in the background and offer an email fallback if the
   request can't reach the endpoint at all.
   ========================================================================== */
(function () {
  'use strict';

  var form = document.getElementById('enquiry-form');
  if (!form) return;

  var status = document.getElementById('form-status');
  var submit = form.querySelector('button[type="submit"]');

  // mailto: URLs have no dependable length limit — mobile mail clients
  // truncate or fail well before our 5,000-character message cap.
  var MAILTO_MESSAGE_CAP = 1200;

  var read = function () {
    return {
      name: form.name_field.value.trim(),
      organisation: form.organisation.value.trim(),
      email: form.email.value.trim(),
      service: (form.querySelector('input[name="service"]:checked') || {}).value || 'Not sure yet',
      message: form.message.value.trim(),
      budget: form.budget.value.trim(),
      target_date: form.target_date.value,
      website: form.website.value
    };
  };

  var mailtoUrl = function (data) {
    var message = data.message.length > MAILTO_MESSAGE_CAP
      ? data.message.slice(0, MAILTO_MESSAGE_CAP) + '\u2026\n\n[Message shortened \u2014 please paste the rest.]'
      : data.message;
    var body = 'Name: ' + data.name +
      '\nOrganisation: ' + data.organisation +
      '\nEmail: ' + data.email +
      '\nLooking for: ' + data.service +
      '\nBudget: ' + (data.budget || 'Not given') +
      '\nIdeal launch date: ' + (data.target_date || 'Not given') +
      '\n\n' + message;
    return 'mailto:info@launchnexus.co.uk?subject=' +
      encodeURIComponent('Project enquiry \u2014 ' + (data.organisation || data.name)) +
      '&body=' + encodeURIComponent(body);
  };

  var fail = function (message, data) {
    // Offer the email route rather than hijacking the visitor into their mail
    // client — a server-side error shouldn't throw away what they typed.
    status.className = 'form-status is-error';
    status.textContent = message + ' ';
    var link = document.createElement('a');
    link.href = mailtoUrl(data);
    link.textContent = 'Send it by email instead';
    status.appendChild(link);
    submit.disabled = false;
  };

  form.addEventListener('submit', function (e) {
    if (!form.checkValidity()) return; // let the browser show its own messages
    e.preventDefault();

    var data = read();
    submit.disabled = true;
    status.className = 'form-status is-busy';
    status.textContent = 'Sending\u2026';

    fetch('/api/enquiry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'fetch' },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        if (res.ok) {
          window.location.href = 'thanks.html';
          return;
        }
        return res.json().catch(function () { return {}; }).then(function (payload) {
          fail(payload.error || 'That didn\u2019t send.', data);
        });
      })
      .catch(function () {
        fail('That didn\u2019t send \u2014 you may be offline.', data);
      });
  });
})();

/* ==========================================================================
   Motion layer.

   Three rules throughout: nothing runs if the visitor asked for reduced
   motion, ambient loops stop when off-screen or on a hidden tab, and every
   effect is progressive — the page is complete without any of it.
   ========================================================================== */
(function () {
  'use strict';

  var still = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (still.matches) return;

  var narrow = window.matchMedia('(max-width: 700px)');

  /* ---- Hero headline: rise word by word ---- */
  var headline = document.querySelector('.hero h1');
  if (headline) {
    var parts = [];
    Array.prototype.forEach.call(headline.childNodes, function (node) {
      if (node.nodeType === 3) {
        node.textContent.split(/(\s+)/).forEach(function (chunk) {
          if (chunk.trim()) parts.push({ text: chunk, em: false });
          else if (chunk) parts.push({ space: true });
        });
      } else {
        // <em> holds the gradient words; keep it whole so the fill survives
        parts.push({ text: node.textContent, em: true });
      }
    });
    headline.textContent = '';
    var n = 0;
    parts.forEach(function (part) {
      if (part.space) {
        headline.appendChild(document.createTextNode(' '));
        return;
      }
      var wrap = document.createElement('span');
      wrap.className = 'word-wrap';
      var inner = document.createElement(part.em ? 'em' : 'span');
      inner.textContent = part.text;
      if (part.em) {
        var shell = document.createElement('span');
        shell.appendChild(inner);
        shell.style.animationDelay = (n * 65) + 'ms';
        wrap.appendChild(shell);
      } else {
        inner.style.animationDelay = (n * 65) + 'ms';
        wrap.appendChild(inner);
      }
      headline.appendChild(wrap);
      n++;
    });
  }

  /* ---- Index children so staggered transitions have something to key off ---- */
  document.querySelectorAll('.grid, .modules, .scatter').forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty('--i', i);
    });
  });

  /* ---- Reveal blocks that animate as a unit ---- */
  var group = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('in');
      group.unobserve(entry.target);
    });
  }, { threshold: 0.2 });
  document.querySelectorAll('.split, .modules').forEach(function (el) { group.observe(el); });

  /* ---- Process steps: light each one, and grow the line to match ---- */
  document.querySelectorAll('.steps').forEach(function (list) {
    var steps = list.querySelectorAll('.step');
    if (!steps.length) return;
    var lit = 0;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('lit');
        io.unobserve(entry.target);
        lit++;
        list.style.setProperty('--fill', Math.min(lit / steps.length, 1));
      });
    }, { threshold: 0.55, rootMargin: '0px 0px -12% 0px' });
    steps.forEach(function (s) { io.observe(s); });
  });

  /* ---- Hero mockup: ambient life ---- */
  var stage = document.querySelector('.hero .stage');
  if (!stage) return;

  var bars = stage.querySelectorAll('.chart i');
  var pills = stage.querySelectorAll('.rows .st');
  var kpis = stage.querySelectorAll('.kpi b');
  var timer = null;
  var onScreen = false;

  var countUp = function (el) {
    var target = parseInt(el.textContent, 10);
    if (isNaN(target)) return;
    var started = null;
    var tick = function (now) {
      if (!started) started = now;
      var p = Math.min((now - started) / 900, 1);
      // ease-out so it settles rather than stopping dead
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    };
    el.textContent = '0';
    requestAnimationFrame(tick);
  };

  var shuffle = function () {
    bars.forEach(function (bar, i) {
      setTimeout(function () {
        bar.style.height = (34 + Math.random() * 56) + '%';
      }, i * 70);
    });
    if (pills.length) {
      var pill = pills[Math.floor(Math.random() * pills.length)];
      pill.classList.remove('pop');
      void pill.offsetWidth; // restart the animation
      pill.classList.add('pop');
    }
  };

  var run = function () {
    if (timer || !onScreen || document.hidden) return;
    // Slower on phones: less work, and less distracting on a small screen.
    timer = setInterval(shuffle, narrow.matches ? 6500 : 4200);
  };
  var halt = function () {
    clearInterval(timer);
    timer = null;
  };

  var counted = false;
  new IntersectionObserver(function (entries) {
    onScreen = entries[0].isIntersecting;
    if (onScreen) {
      if (!counted) {
        counted = true;
        kpis.forEach(countUp);
      }
      run();
    } else {
      halt();
    }
  }, { threshold: 0.25 }).observe(stage);

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) halt();
    else run();
  });
})();
