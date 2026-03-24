/**
 * RHGI-14314-MIGRATION-53 — Global Pulse clocks (Abuja · London · Dubai UTC+4 · New York)
 * Data anchor: 144,000 wards · 39,790,350 votes · ₦60,840,000,000
 */

(function () {
  "use strict";

  var RHGI_TACTICAL_WARDS = 144000;
  var RHGI_MANDATE_VOTES = 20709668;
  var RHGI_GLOBAL_FUND_NGN = 60840000000;
  var RHGI_STATE_NOW = 18;
  var RHGI_STATE_MAX = 24;
  var RHGI_VICTORY_REQUIREMENT = 37;
  var RHGI_ELECTION_TARGET = new Date("2027-01-16T00:00:00+01:00");
  var RHGI_PROJECTION_TARGET = 39700000;
  var big4Matrix = [
    { key: "lagos", base2023: 18, target2027: 44 },
    { key: "kano", base2023: 22, target2027: 47 },
    { key: "rivers", base2023: 16, target2027: 39 },
    { key: "fct", base2023: 20, target2027: 45 }
  ];

  var zones = [
    { city: "Abuja", offset: 1 },
    { city: "London", offset: 0 },
    { city: "Dubai", offset: 4 },
    { city: "New York", offset: -4 }
  ];
  var corridorMatrix = [
    { key: "nw", label: "Northwest", budget: "₦17.38B", total2023: 6500000, total2027: 9600000, baseline: { APC: 46, ADC: 16, PDP: 22, LP: 10 }, projection: { APC: 66, ADC: 24, PDP: 28, LP: 16 } },
    { key: "ne", label: "Northeast", budget: "₦10.45B", total2023: 3800000, total2027: 5500000, baseline: { APC: 43, ADC: 14, PDP: 24, LP: 9 }, projection: { APC: 63, ADC: 22, PDP: 31, LP: 14 } },
    { key: "nc", label: "Northcentral", budget: "₦11.22B", total2023: 4200000, total2027: 6000000, baseline: { APC: 34, ADC: 13, PDP: 27, LP: 16 }, projection: { APC: 57, ADC: 20, PDP: 33, LP: 21 } },
    { key: "sw", label: "Southwest", budget: "₦12.84B", total2023: 5200000, total2027: 7600000, baseline: { APC: 38, ADC: 15, PDP: 18, LP: 27 }, projection: { APC: 61, ADC: 23, PDP: 24, LP: 34 } },
    { key: "se", label: "Southeast", budget: "₦8.91B", total2023: 2600000, total2027: 2200000, baseline: { APC: 12, ADC: 10, PDP: 31, LP: 41 }, projection: { APC: 24, ADC: 14, PDP: 29, LP: 33 } },
    { key: "ss", label: "Southsouth", budget: "₦10.00B", total2023: 3200000, total2027: 6600000, baseline: { APC: 19, ADC: 11, PDP: 36, LP: 24 }, projection: { APC: 36, ADC: 17, PDP: 42, LP: 31 } }
  ];

  function tickGroupHtml() {
    var html = "";
    var t;
    for (t = 0; t < 12; t++) {
      var ang = ((t * 30 - 90) * Math.PI) / 180;
      var x1 = 50 + 42 * Math.cos(ang);
      var y1 = 50 + 42 * Math.sin(ang);
      var x2 = 50 + 38 * Math.cos(ang);
      var y2 = 50 + 38 * Math.sin(ang);
      html +=
        '<line class="rhgi-tick" x1="' +
        x1 +
        '" y1="' +
        y1 +
        '" x2="' +
        x2 +
        '" y2="' +
        y2 +
        '"/>';
    }
    return html;
  }

  function clockMarkup(idx) {
    var dubaiNote =
      zones[idx].offset === 4
        ? '<span class="rhgi-clock-tz">UTC+4</span>'
        : "";
    return (
      '<div class="rhgi-clock-wrap' +
      (idx === 0 ? " rhgi-clock-abuja-frame" : "") +
      '" data-city="' +
      zones[idx].city +
      '" data-tz="' +
      zones[idx].offset +
      '">' +
      '<div class="rhgi-clock-face-wrap">' +
      '<svg class="rhgi-clock-svg" viewBox="0 0 100 100" aria-hidden="true">' +
      '<circle cx="50" cy="50" r="48" fill="rgba(4,14,28,0.92)" stroke="rgba(40,72,118,0.65)" stroke-width="1.2"/>' +
      "<g>" +
      tickGroupHtml() +
      "</g>" +
      '<line class="rhgi-hand rhgi-hand-hour" x1="50" y1="50" x2="50" y2="32" stroke="#00f0ff" stroke-width="3" stroke-linecap="round"/>' +
      '<line class="rhgi-hand rhgi-hand-minute" x1="50" y1="50" x2="50" y2="22" stroke="#4df0ff" stroke-width="2" stroke-linecap="round"/>' +
      '<line class="rhgi-hand rhgi-hand-second" x1="50" y1="50" x2="50" y2="18" stroke="#00b4ff" stroke-width="1" stroke-linecap="round"/>' +
      '<circle cx="50" cy="50" r="2.5" fill="#00e5ff"/>' +
      "</svg></div>" +
      '<span class="rhgi-clock-city">' +
      zones[idx].city +
      "</span>" +
      dubaiNote +
      "</div>"
    );
  }

  function clockPartsForOffset(offsetHours, nowUtcMs) {
    var local = new Date(nowUtcMs + offsetHours * 3600000);
    return { h24: local.getUTCHours(), Mi: local.getUTCMinutes(), Se: local.getUTCSeconds() };
  }

  function lagosClockPartsFromLocaleString() {
    var lagosNow = new Date(
      new Date().toLocaleString("en-US", { timeZone: "Africa/Lagos" })
    );
    return {
      h24: lagosNow.getHours(),
      Mi: lagosNow.getMinutes(),
      Se: lagosNow.getSeconds()
    };
  }

  function updateSovereignClocks() {
    var row = document.getElementById("rhgi-clocksRow");
    if (!row) {
      return;
    }
    var nowUtcMs = Date.now();
    row.querySelectorAll(".rhgi-clock-wrap").forEach(function (wrap) {
      var city = wrap.getAttribute("data-city");
      var offset = parseInt(wrap.getAttribute("data-tz"), 10);
      var t =
        city === "Abuja"
          ? lagosClockPartsFromLocaleString()
          : clockPartsForOffset(offset, nowUtcMs);
      var h12 = t.h24 % 12;
      var hourDeg = (h12 + t.Mi / 60 + t.Se / 3600) * 30 - 90;
      var minuteDeg = (t.Mi + t.Se / 60) * 6 - 90;
      var secondDeg = t.Se * 6 - 90;
      var hEl = wrap.querySelector(".rhgi-hand-hour");
      var mEl = wrap.querySelector(".rhgi-hand-minute");
      var sEl = wrap.querySelector(".rhgi-hand-second");
      if (hEl) {
        hEl.setAttribute("transform", "rotate(" + hourDeg + " 50 50)");
      }
      if (mEl) {
        mEl.setAttribute("transform", "rotate(" + minuteDeg + " 50 50)");
      }
      if (sEl) {
        sEl.setAttribute("transform", "rotate(" + secondDeg + " 50 50)");
      }
    });
  }

  function renderClockFaces() {
    var row = document.getElementById("rhgi-clocksRow");
    if (!row) {
      return;
    }
    row.innerHTML = zones
      .map(function (_, i) {
        return clockMarkup(i);
      })
      .join("");
    updateSovereignClocks();
  }

  function lockDataAnchor() {
    var el = document.getElementById("rhgi-data-anchor");
    if (!el) {
      return;
    }
    el.innerHTML =
      "<p><strong>" +
      RHGI_TACTICAL_WARDS.toLocaleString("en-NG") +
      "</strong> tactical wards · mandate target <strong>" +
      RHGI_MANDATE_VOTES.toLocaleString("en-NG") +
      "</strong> votes</p>" +
      "<p>Global operational fund <strong>₦" +
      RHGI_GLOBAL_FUND_NGN.toLocaleString("en-NG") +
      "</strong> · national vote target <strong>" +
      RHGI_MANDATE_VOTES.toLocaleString("en-NG") +
      "</strong></p>";
  }

  function buildTicker774() {
    var pool = [];
    var i;
    for (i = 1; i <= 774; i++) {
      pool.push("LGA " + String(i).padStart(3, "0") + " · node " + i);
    }
    var line = pool.join(" · ");
    var a = document.getElementById("rhgi-footer774A");
    var b = document.getElementById("rhgi-footer774B");
    if (a) {
      a.textContent = line;
    }
    if (b) {
      b.textContent = line;
    }
  }

  function renderCorridorMatrix() {
    var host = document.getElementById("rhgi-corridorGrid");
    if (!host) {
      return;
    }
    host.innerHTML = corridorMatrix
      .map(function (c) {
        var parties = ["APC", "ADC", "PDP", "LP"];
        var baseVotes = c.total2023;
        var targetVotes = c.total2027;
        var rows = parties
          .map(function (p) {
            var baseVal = Math.round((c.baseline[p] / 100) * baseVotes);
            var projVal = Math.round((c.projection[p] / 100) * targetVotes);
            return (
              '<div class="rhgi-corridor-row">' +
              '<p class="rhgi-corridor-party"><span class="rhgi-digital-glow">' +
              p +
              '</span><span>' +
              baseVal.toLocaleString("en-NG") +
              " (" +
              c.baseline[p] +
              "%) | " +
              projVal.toLocaleString("en-NG") +
              " (" +
              c.projection[p] +
              "%)</span></p>" +
              '<div class="rhgi-corridor-bars">' +
              '<div class="rhgi-corridor-rail"><div class="rhgi-corridor-fill rhgi-corridor-fill-base" data-w="' +
              c.baseline[p] +
              '"></div></div>' +
              '<div class="rhgi-corridor-rail"><div class="rhgi-corridor-fill rhgi-corridor-fill-proj" data-w="' +
              c.projection[p] +
              '"></div></div>' +
              "</div></div>"
            );
          })
          .join("");
        var baselineWinnerVotes = Math.max.apply(
          null,
          parties.map(function (p) {
            return Math.round((c.baseline[p] / 100) * baseVotes);
          })
        );
        var projectedWinnerVotes = Math.max.apply(
          null,
          parties.map(function (p) {
            return Math.round((c.projection[p] / 100) * targetVotes);
          })
        );
        var margin = targetVotes - baseVotes;
        var redZone = projectedWinnerVotes < baselineWinnerVotes;
        var wardGap = Math.max(0, Math.ceil((baselineWinnerVotes - projectedWinnerVotes) / 225));
        var redZoneBudget = wardGap * 40000;
        return (
          '<article class="rhgi-corridor-widget prism-frame rhgi-prism-frame' +
          (redZone ? " rhgi-combat-sentinel" : "") +
          '">' +
          '<p class="rhgi-corridor-title">' +
          c.label +
          " Corridor</p>" +
          '<div class="rhgi-corridor-pillars"><span>2023 Forensic</span><span>2027 Projection</span></div>' +
          '<p class="rhgi-corridor-margin rhgi-digital-glow" data-base="' +
          margin +
          '" id="rhgi-margin-' +
          c.key +
          '">WINNING MARGIN: +' +
          margin.toLocaleString("en-NG") +
          "</p>" +
          rows +
          '<p class="rhgi-corridor-note">Total Region Budget: <strong>' +
          c.budget +
          "</strong></p>" +
          '<p class="rhgi-corridor-note">2027 Projection Node: <strong>' +
          RHGI_PROJECTION_TARGET.toLocaleString("en-NG") +
          "</strong></p>" +
          (redZone
            ? '<p class="rhgi-corridor-note">Secondary Canvasser Budget (Red Zone @ ₦40,000/ward): <strong>₦' +
              redZoneBudget.toLocaleString("en-NG") +
              "</strong></p>"
            : "") +
          '<p class="rhgi-corridor-ratio">1 Unit Commander → 15 Canvassers → 225 Voters</p>' +
          "</article>"
        );
      })
      .join("");

    host.querySelectorAll(".rhgi-corridor-fill").forEach(function (el) {
      var w = el.getAttribute("data-w");
      requestAnimationFrame(function () {
        el.style.width = w + "%";
      });
    });
  }

  function updateWinningMarginsPulse() {
    document.querySelectorAll(".rhgi-corridor-margin").forEach(function (el) {
      var base = parseInt(el.getAttribute("data-base"), 10) || 0;
      var pulse = Math.round((Math.sin(Date.now() / 650) + 1) * 0.5 * 25000);
      el.textContent = "WINNING MARGIN: +" + (base + pulse).toLocaleString("en-NG");
    });
  }

  var pulseTimer = null;
  var countdownTimer = null;

  function startPulseInterval() {
    if (pulseTimer !== null) {
      return;
    }
    (function tickClock() {
      updateSovereignClocks();
      var delay = 1000 - (Date.now() % 1000);
      pulseTimer = setTimeout(tickClock, delay);
    })();
  }

  function startCountdownInterval() {
    if (countdownTimer !== null) {
      return;
    }
    (function tickCountdown() {
      updateCountdown();
      updateWinningMarginsPulse();
      var delay = 1000 - (Date.now() % 1000);
      countdownTimer = setTimeout(tickCountdown, delay);
    })();
  }

  function updateCountdown() {
    var now = new Date();
    var diffMs = RHGI_ELECTION_TARGET.getTime() - now.getTime();
    if (diffMs < 0) {
      diffMs = 0;
    }
    var totalSec = Math.floor(diffMs / 1000);
    var daysTotal = Math.floor(totalSec / 86400);
    var months = Math.floor(daysTotal / 30);
    var days = daysTotal % 30;
    var hours = Math.floor((totalSec % 86400) / 3600);
    var seconds = totalSec % 60;

    var monthsEl = document.getElementById("rhgi-cd-months");
    var daysEl = document.getElementById("rhgi-cd-days");
    var hoursEl = document.getElementById("rhgi-cd-hours");
    var secondsEl = document.getElementById("rhgi-cd-seconds");

    if (monthsEl) monthsEl.textContent = String(months).padStart(2, "0");
    if (daysEl) daysEl.textContent = String(days).padStart(2, "0");
    if (hoursEl) hoursEl.textContent = String(hours).padStart(2, "0");
    if (secondsEl) secondsEl.textContent = String(seconds).padStart(2, "0");
  }

  function initConstitutionalGauge() {
    var arc = document.getElementById("rhgi-gaugeArc");
    var diamond = document.getElementById("rhgi-abujaDiamond");
    var validator = document.getElementById("rhgi-validatorText");
    var projected = RHGI_STATE_NOW / RHGI_STATE_MAX >= 0.75;
    var arcDeg = Math.round((RHGI_STATE_NOW / RHGI_VICTORY_REQUIREMENT) * 300);
    if (arc) {
      arc.style.setProperty("--arc-degree", arcDeg + "deg");
    }
    if (diamond) {
      diamond.classList.toggle("is-solid", projected);
      diamond.style.opacity = projected ? "1" : "0.45";
    }
    var abujaFrame = document.querySelector(".rhgi-clock-abuja-frame");
    if (abujaFrame) {
      abujaFrame.classList.toggle("rhgi-clock-abuja-flicker", !projected);
      abujaFrame.classList.toggle("rhgi-clock-abuja-solid", projected);
    }
    if (validator) {
      validator.textContent =
        "Constitutional Status: [" +
        RHGI_STATE_NOW +
        "/" +
        RHGI_STATE_MAX +
        " States Secured] | FCT: " +
        (projected ? "VALIDATED" : "PENDING");
    }
  }

  function initBig4Matrix() {
    big4Matrix.forEach(function (m) {
      var b23 = document.getElementById("rhgi-" + m.key + "-2023");
      var b27 = document.getElementById("rhgi-" + m.key + "-2027");
      var meta = document.getElementById("rhgi-" + m.key + "-meta");
      var gap = document.getElementById("rhgi-" + m.key + "-gap");
      var growth = Math.round(((m.target2027 - m.base2023) / m.base2023) * 100);
      if (b23) {
        requestAnimationFrame(function () {
          b23.style.width = m.base2023 + "%";
        });
      }
      if (b27) {
        requestAnimationFrame(function () {
          b27.style.width = m.target2027 + "%";
        });
      }
      if (meta) {
        meta.textContent = "2023: " + m.base2023 + "% | 2027: " + m.target2027 + "%";
      }
      if (gap) {
        gap.textContent = "+" + growth + "% to Victory";
      }
    });

    var fctDiamond = document.getElementById("rhgi-matrixAbujaDiamond");
    var fctData = big4Matrix.find(function (m) {
      return m.key === "fct";
    });
    if (fctDiamond && fctData) {
      var thresholdProjected = fctData.target2027 >= 25;
      fctDiamond.classList.toggle("is-solid", thresholdProjected);
      fctDiamond.style.opacity = thresholdProjected ? "1" : "0.45";
    }
  }

  function onReady() {
    lockDataAnchor();
    initConstitutionalGauge();
    initBig4Matrix();
    renderCorridorMatrix();
    buildTicker774();
    renderClockFaces();
    startPulseInterval();
    startCountdownInterval();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
