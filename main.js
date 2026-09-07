(function () {
  "use strict";
  var S = window.SITE;
  if (!S) return;
  var $ = function (id) { return document.getElementById(id); };
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Arms the scroll animations. The stylesheet only hides content beneath this
  // class, so if this line is never reached the page still renders in full.
  if (!reduced) document.documentElement.classList.add("anim");

  /* ---- Masthead ---- */
  $("masthead").innerHTML =
    '<div class="masthead__inner">' +
      '<div>' +
        '<a class="masthead__name" href="#">' + S.person.name + '</a>' +
        '<span class="masthead__sub">' + S.person.role + ' · ' + S.person.location + '</span>' +
      '</div>' +
      '<nav class="masthead__nav" aria-label="Contents">' +
        '<a href="#work">Work</a>' +
        '<a href="#patents">Patents</a>' +
        '<a href="#skills">Skills</a>' +
        '<a href="#contact">Contact</a>' +
      '</nav>' +
    '</div>';

  /* ---- Lede ---- */
  var env = S.person.envelope;
  $("lede").innerHTML =
    '<p class="lede__text">' + S.person.lede[0] + '<br>' + S.person.lede[1] + '</p>' +
    '<svg class="lede__envelope" viewBox="0 0 440 65" role="img" ' +
      'aria-label="Operating envelope: ' + env.low + ' to ' + env.high + '">' +
      '<line class="env-rule" x1="50" y1="32" x2="390" y2="32" stroke="#16181a" stroke-width="1"/>' +
      '<polygon class="env-fade" points="50,32 58,28 58,36" fill="#16181a"/>' +
      '<polygon class="env-fade" points="390,32 382,28 382,36" fill="#16181a"/>' +
      '<line class="env-fade" x1="50" y1="22" x2="50" y2="42" stroke="#c7cbce"/>' +
      '<line class="env-fade" x1="390" y1="22" x2="390" y2="42" stroke="#c7cbce"/>' +
      '<text class="env-fade" x="50" y="58" text-anchor="middle" fill="#82878c" font-size="12" ' +
        'font-family="SFMono-Regular,Consolas,monospace">' + env.low + '</text>' +
      '<text class="env-fade" x="390" y="58" text-anchor="middle" fill="#82878c" font-size="12" ' +
        'font-family="SFMono-Regular,Consolas,monospace">' + env.high + '</text>' +
      '<text class="env-fade" x="220" y="18" text-anchor="middle" fill="#16181a" font-size="13" ' +
        'font-weight="500" font-family="Archivo,sans-serif">' + env.span + '</text>' +
      '<line class="env-fade" x1="390" y1="24" x2="390" y2="40" stroke="#cc2a1e" stroke-width="2.5"/>' +
    '</svg>';

  /* ---- Work ---- */
  function figLinks(figs) {
    return figs.map(function (f) {
      return '<a href="#fig-' + f.n + '" class="fig-ref">FIG. ' + f.n + '</a>';
    }).join(', ');
  }

  var bomRows = S.projects.map(function (p) {
    return '<tr>' +
      '<td class="bom__code"><a href="#' + p.code + '">' + p.code + '</a></td>' +
      '<td>' + p.title + '</td>' +
      '<td>' + p.role + '</td>' +
      '<td class="bom__year">' + p.year + '</td>' +
      '<td class="bom__fig">' + figLinks(p.figs) + '</td></tr>';
  }).join('');

  bomRows += S.earlier.map(function (e) {
    return '<tr class="bom__earlier">' +
      '<td class="bom__code">—</td>' +
      '<td>' + e.title + '</td>' +
      '<td>' + e.clause + '</td>' +
      '<td class="bom__year">' + e.year + '</td>' +
      '<td class="bom__fig">—</td></tr>';
  }).join('');

  var blocks = S.projects.map(function (p, i) {
    var folio = String(i + 1).padStart(2, '0');
    var plates = p.figs.map(function (f) {
      return '<figure class="plate" id="fig-' + f.n + '">' +
        '<div class="plate__tag">FIG. ' + f.n +
          ' <span class="plate__tag-title">' + f.title + '</span></div>' +
        '<div class="plate__frame" data-svg="' + f.src + '" ' +
          'role="img" aria-label="' + f.title + '"></div>' +
        '<div class="plate__caption">' + f.caption + '</div>' +
        '<div class="plate__stamp">representative topology — not to scale</div>' +
      '</figure>';
    }).join('');

    return '<article class="project reveal" id="' + p.code + '">' +
      '<div class="project__folio" aria-hidden="true">' + folio + '</div>' +
      '<div class="project__body">' +
        '<div class="project__head">' +
          '<span class="project__code">' + p.code + '</span>' +
          '<h3 class="project__title">' + p.title + '</h3>' +
        '</div>' +
        '<p class="project__sentence">' + p.sentence + '</p>' +
        '<dl class="meta-row">' +
          '<div class="meta-item"><dt>Role</dt><dd>' + p.role + '</dd></div>' +
          '<div class="meta-item"><dt>Scale</dt><dd>' + p.scale + '</dd></div>' +
          '<div class="meta-item"><dt>Outcome</dt><dd>' + p.outcome + '</dd></div>' +
          '<div class="meta-item"><dt>Fig.</dt><dd>' + figLinks(p.figs) + '</dd></div>' +
        '</dl>' +
        plates +
      '</div>' +
    '</article>';
  }).join('');

  var earlierRows = S.earlier.map(function (e) {
    return '<tr><td class="e-year">' + e.year + '</td>' +
      '<td>' + e.title + '</td><td>' + e.clause + '</td></tr>';
  }).join('');

  $("work").innerHTML =
    '<div class="sect__label">Work</div>' +
    '<div class="sect__intro">' +
      '<p class="sect__count">' + (S.projects.length + S.earlier.length) +
        ' projects · 2018–2025</p>' +
      '<div class="bom-wrap"><table class="bom"><thead><tr>' +
        '<th>No.</th><th>Project</th><th>Role</th><th>Year</th><th>Fig.</th>' +
      '</tr></thead><tbody>' + bomRows + '</tbody></table></div>' +
    '</div>' +
    blocks +
    '<div class="sect__earlier reveal" id="TH-05">' +
      '<div class="earlier-label">Earlier</div>' +
      '<table class="earlier-table"><tbody>' + earlierRows + '</tbody></table>' +
    '</div>';

  /* ---- Position ---- */
  $("position").innerHTML =
    '<blockquote class="position reveal">' + S.position + '</blockquote>';

  /* ---- Experience ---- */
  var expRows = S.experience.map(function (x) {
    return '<tr><td class="exp-year">' + x.year + '</td>' +
      '<td class="exp-org">' + x.org + '</td>' +
      '<td>' + x.role + '</td><td>' + x.place + '</td></tr>';
  }).join('');
  $("experience").innerHTML =
    '<div class="sect__label">Experience</div>' +
    '<div class="sect__body reveal">' +
      '<table class="exp-table"><tbody>' + expRows + '</tbody></table>' +
    '</div>';

  /* ---- Patents ---- */
  var patRows = S.patents.map(function (p) {
    return '<tr><td class="pub-no">' + p.number + '</td>' +
      '<td>' + p.title + '</td><td>' + p.status + '</td></tr>';
  }).join('');
  var awardRows = S.awards.map(function (a) {
    return '<tr><td class="award-year">' + a.year + '</td>' +
      '<td class="award-name">' + a.name + '</td>' +
      '<td>' + a.note + '</td></tr>';
  }).join('');
  // Photographs get the plate frame but no FIG. number — they are evidence,
  // not figures, and numbering them would fold them into the drawing set.
  var awardPlates = (S.awardMedia || []).map(function (m) {
    return '<figure class="plate plate--photo lift">' +
      '<div class="plate__tag">' + m.tag + '</div>' +
      '<div class="plate__frame plate__frame--photo">' +
        '<img src="' + m.src + '" alt="' + m.alt + '" loading="lazy" decoding="async">' +
      '</div>' +
      '<div class="plate__caption">' + m.caption + '</div>' +
    '</figure>';
  }).join('');
  $("patents").innerHTML =
    '<div class="sect__label">Patents</div>' +
    '<div class="sect__body reveal">' +
      '<table class="patents-table"><thead><tr>' +
        '<th>Pub. No.</th><th>Title</th><th>Status</th>' +
      '</tr></thead><tbody>' + patRows + '</tbody></table>' +
      '<p class="award-line">' + S.patentNote + '</p>' +
      '<div class="award-label">Recognition</div>' +
      '<table class="award-table"><tbody>' + awardRows + '</tbody></table>' +
      '<div class="award-media">' + awardPlates + '</div>' +
    '</div>';

  /* ---- Skills ---- */
  var skillHTML = S.skills.map(function (s) {
    return '<div class="skills-row">' +
      '<div class="skills-row__domain">' + s.domain + '</div>' +
      '<div class="skills-row__tokens">' + s.tokens.join(' · ') + '</div>' +
    '</div>';
  }).join('');
  $("skills").innerHTML =
    '<div class="sect__label">Skills</div>' +
    '<div class="sect__body reveal">' + skillHTML + '</div>';

  /* ---- Education ---- */
  var eduRows = S.education.map(function (e) {
    return '<tr><td class="edu-year">' + e.year + '</td>' +
      '<td>' + e.qual + '</td><td>' + e.inst + '</td>' +
      '<td>' + (e.focus || '') + '</td></tr>';
  }).join('');
  $("education").innerHTML =
    '<div class="sect__label">Education</div>' +
    '<div class="sect__body reveal">' +
      '<table class="edu-table"><thead><tr>' +
        '<th>Year</th><th>Qualification</th><th>Institution</th><th>Focus</th>' +
      '</tr></thead><tbody>' + eduRows + '</tbody></table>' +
    '</div>';

  /* ---- Contact ---- */
  $("contact").innerHTML =
    '<div class="sect__label">Contact</div>' +
    '<div class="sect__body reveal">' +
      '<div class="contact__grid">' +
        '<div class="contact__main">' +
          '<p class="contact__avail">' + S.contact.availability + '</p>' +
          '<div class="contact__links">' +
            '<a href="mailto:' + S.person.email + '">' + S.person.email + '</a>' +
            '<a href="' + S.person.linkedin + '" target="_blank" rel="noopener">LinkedIn</a>' +
            '<a href="' + S.person.resume + '" target="_blank" rel="noopener">Résumé (PDF)</a>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>';

  /* ---- Portrait (title block) ----
     Injected only after the file is confirmed to load. Probing first means a
     missing portrait leaves no gap, no broken-image icon and no reserved space,
     so the page is publishable before the photograph exists. */
  (function () {
    var P = S.portrait;
    if (!P || !P.src) return;
    var probe = new Image();
    probe.onload = function () {
      var grid = document.querySelector(".contact__grid");
      if (grid) {
        var fig = document.createElement("figure");
        fig.className = "plate plate--portrait";
        fig.innerHTML =
          '<div class="plate__tag">' + P.tag + '</div>' +
          '<div class="plate__frame plate__frame--portrait">' +
            '<img src="' + P.src + '" alt="' + P.alt + '" ' +
              'width="576" height="768" decoding="async">' +
          '</div>' +
          '<div class="plate__caption">' + P.caption + '</div>';
        grid.appendChild(fig);
      }
      // A 36px face in the running head rides the whole scroll, so a reader who
      // never reaches Contact still sees there is a person behind the sheets.
      var rhLeft = document.querySelector(".rh__left");
      if (rhLeft && !rhLeft.querySelector("img")) {
        var thumb = document.createElement("img");
        thumb.className = "rh__face";
        thumb.src = P.src;
        thumb.alt = "";
        thumb.setAttribute("aria-hidden", "true");
        rhLeft.insertBefore(thumb, rhLeft.firstChild);
      }
    };
    probe.src = P.src;
  })();

  /* ---- Footer ---- */
  $("footer").innerHTML =
    '<span>' + S.person.name + '</span>' +
    '<span class="footer__meta">Updated ' + S.contact.updated +
      ' · ' + S.person.location + '</span>';

  /* ==========================================================
     Plate plotter — inline each schematic so its strokes can be
     drawn on rather than shown all at once. An <img> is opaque to
     script, so the SVG has to be fetched and adopted into the DOM.
     ========================================================== */

  var GEOM = "path,line,polyline,polygon,circle,rect,ellipse";

  function prime(svg) {
    var strokes = [], fades = [];

    svg.querySelectorAll(GEOM).forEach(function (el) {
      // Marker and pattern geometry is drawn as part of whatever references it,
      // so animating it here would blank arrowheads instead of drawing them.
      if (el.closest("defs")) return;
      // The quadrille ground is scenery, not a drawn line — leave it be.
      if ((el.getAttribute("fill") || "").indexOf("url(#") === 0) return;

      var stroke = el.getAttribute("stroke");
      var inked = stroke && stroke !== "none";
      // Elements already carrying a dash pattern encode meaning with it
      // (chilled runs, sensor lines); overwriting it to animate would
      // destroy the distinction, so those fade instead.
      var patterned = el.hasAttribute("stroke-dasharray");
      var len = 0;

      if (inked && !patterned && el.getTotalLength) {
        try { len = el.getTotalLength(); } catch (e) { len = 0; }
      }

      if (len > 1 && len < 12000) {
        el.style.strokeDasharray = len;
        el.style.strokeDashoffset = len;
        strokes.push(el);
      } else {
        el.style.opacity = "0";
        fades.push(el);
      }
    });

    svg.querySelectorAll("text").forEach(function (el) {
      el.style.opacity = "0";
      fades.push(el);
    });

    return { strokes: strokes, fades: fades };
  }

  function plot(p) {
    p.strokes.forEach(function (el, i) {
      var d = 40 + (i % 14) * 45;
      el.style.transition = "stroke-dashoffset 760ms cubic-bezier(.22,.61,.36,1) " + d + "ms";
      el.style.strokeDashoffset = "0";
    });
    p.fades.forEach(function (el, i) {
      var d = 300 + (i % 22) * 26;
      el.style.transition = "opacity 460ms ease " + d + "ms";
      el.style.opacity = "1";
    });
  }

  /* ==========================================================
     Reveal engine.

     Deliberately NOT IntersectionObserver. IO silently never fires in some
     embedded/background contexts, and because this design hides content until
     it is revealed, a single missed callback leaves the page permanently blank.
     A rAF-throttled scroll check cannot fail that way, costs nothing at this
     page size, and is backed by a timeout that reveals everything regardless.
     ========================================================== */

  var watched = [];
  function watch(el, fire) { watched.push({ el: el, fire: fire, done: false }); }

  function sweep() {
    var vh = window.innerHeight || document.documentElement.clientHeight;
    var pending = false;
    watched.forEach(function (w) {
      if (w.done) return;
      var r = w.el.getBoundingClientRect();
      // Trigger once any part of the element crosses 88% of the viewport height.
      if (r.top < vh * 0.88 && r.bottom > 0) {
        w.done = true;
        w.fire(w.el);
      } else {
        pending = true;
      }
    });
    return pending;
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { sweep(); ticking = false; });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });

  // Safety net: whatever has not been reached after 4s is shown outright, so a
  // stalled scroll handler can never leave the page looking empty.
  setTimeout(function () {
    watched.forEach(function (w) {
      if (!w.done) { w.done = true; w.fire(w.el); }
    });
  }, 4000);

  document.querySelectorAll(".plate__frame[data-svg]").forEach(function (frame) {
    fetch(frame.dataset.svg)
      .then(function (r) { return r.text(); })
      .then(function (markup) {
        var holder = document.createElement("div");
        holder.innerHTML = markup;
        var svg = holder.querySelector("svg");
        if (!svg) return;
        svg.removeAttribute("width");
        svg.removeAttribute("height");
        svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
        frame.appendChild(svg);
        if (reduced) return;
        var primed = prime(svg);
        watch(frame, function () { plot(primed); });
        onScroll();
      })
      .catch(function () {
        // Fall back to a plain image if the fetch is blocked.
        var img = document.createElement("img");
        img.src = frame.dataset.svg;
        img.alt = frame.getAttribute("aria-label") || "";
        frame.appendChild(img);
      });
  });

  /* ---- Envelope draws itself on load ---- */
  if (!reduced) {
    var envSvg = document.querySelector(".lede__envelope");
    if (envSvg) {
      var rule = envSvg.querySelector(".env-rule");
      var len = rule.getTotalLength();
      rule.style.strokeDasharray = len;
      rule.style.strokeDashoffset = len;
      envSvg.querySelectorAll(".env-fade").forEach(function (el) { el.style.opacity = "0"; });
      requestAnimationFrame(function () {
        rule.style.transition = "stroke-dashoffset 900ms cubic-bezier(.22,.61,.36,1) 250ms";
        rule.style.strokeDashoffset = "0";
        envSvg.querySelectorAll(".env-fade").forEach(function (el, i) {
          el.style.transition = "opacity 500ms ease " + (900 + i * 70) + "ms";
          el.style.opacity = "1";
        });
      });
    }
  }

  /* ---- Section reveals ---- */
  function show(el) { el.classList.add("in"); }

  if (!reduced) {
    // Each plate lifts as it is reached, so a two-plate project arrives in
    // sequence instead of the whole block landing at once.
    document.querySelectorAll(".project .plate").forEach(function (el) {
      el.classList.add("lift");
    });
    document.querySelectorAll(".lift").forEach(function (el, i) {
      el.style.setProperty("--lift-delay", ((i % 3) * 90) + "ms");
    });
    // Rows stagger within the index so it assembles rather than blinks in.
    document.querySelectorAll(".bom tbody tr").forEach(function (tr, i) {
      tr.style.setProperty("--row-delay", (i * 55) + "ms");
      tr.classList.add("row-reveal");
    });

    document.querySelectorAll(".reveal, .lift").forEach(function (el) {
      watch(el, show);
    });
    var bomEl = document.querySelector(".bom");
    if (bomEl) {
      watch(bomEl, function (t) {
        t.querySelectorAll(".row-reveal").forEach(show);
      });
    }
    onScroll();
  } else {
    document.querySelectorAll(".reveal, .lift, .row-reveal").forEach(show);
  }

  /* ---- Running head + scroll progress ---- */
  var rh = $("running-head");
  var rhSec = $("rh-section");
  var sentinel = $("masthead");

  var sectionEls = ["work", "experience", "patents", "skills", "education", "contact"]
    .map($).filter(Boolean);

  var bar = document.createElement("div");
  bar.className = "rh__progress";
  rh.appendChild(bar);

  // Same reasoning as the reveal engine: read positions directly rather than
  // trusting IntersectionObserver, which does not fire in every context.
  function updateChrome() {
    var mast = sentinel.getBoundingClientRect();
    rh.classList.toggle("visible", mast.bottom <= 0);

    var max = document.documentElement.scrollHeight - window.innerHeight;
    var pct = max > 0 ? window.scrollY / max : 0;
    bar.style.transform = "scaleX(" + Math.min(1, Math.max(0, pct)) + ")";

    // The current section is the last one whose top has passed the running head.
    var current = null;
    sectionEls.forEach(function (el) {
      if (el.getBoundingClientRect().top <= 48) current = el;
    });
    rhSec.textContent = current ? current.id : "";
  }

  var chromeTick = false;
  window.addEventListener("scroll", function () {
    if (chromeTick) return;
    chromeTick = true;
    requestAnimationFrame(function () { updateChrome(); chromeTick = false; });
  }, { passive: true });
  window.addEventListener("resize", updateChrome, { passive: true });
  updateChrome();

  /* ---- FIG-reference click ---- */
  document.addEventListener("click", function (e) {
    var ref = e.target.closest(".fig-ref");
    if (!ref) return;
    e.preventDefault();
    var plate = document.querySelector(ref.getAttribute("href"));
    if (!plate) return;
    plate.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
    if (reduced) return;
    plate.classList.add("plate--flash");
    setTimeout(function () { plate.classList.remove("plate--flash"); }, 1000);
  });

  /* ---- Deep links ---- */
  function handleHash() {
    var h = location.hash.slice(1);
    if (!h) return;
    var t = $(h);
    if (!t) return;
    setTimeout(function () {
      t.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
    }, 120);
  }
  handleHash();
  window.addEventListener("hashchange", handleHash);
})();
