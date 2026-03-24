/**
 * RHGI-14314-MIGRATION-53 — Global Pulse clocks (Abuja · London · Dubai UTC+4 · New York)
 * Data anchor: 144,000 wards · 39,790,350 votes · ₦60,840,000,000
 */

(function () {
  "use strict";

  var RHGI_TACTICAL_WARDS = 144000;
  var RHGI_MANDATE_VOTES = 39790350;
  var RHGI_GLOBAL_FUND_NGN = 60840000000;
  var RHGI_STATE_NOW = 24;
  var RHGI_STATE_MAX = 36;
  var RHGI_ELECTION_TARGET = new Date("2027-01-16T00:00:00+01:00");

  var zones = [
    { city: "Abuja", tz: "Africa/Lagos" },
    { city: "London", tz: "Europe/London" },
    { city: "Dubai", tz: "Asia/Dubai" },
    { city: "New York", tz: "America/New_York" }
  ];
  var regionalWidgets = [
    { key: "nw", label: "Northwest", progress: 82, lgas: 186 },
    { key: "ne", label: "Northeast", progress: 77, lgas: 112 },
    { key: "nc", label: "Northcentral", progress: 80, lgas: 120 },
    { key: "sw", label: "Southwest", progress: 86, lgas: 137 },
    { key: "se", label: "Southeast", progress: 79, lgas: 95 },
    { key: "ss", label: "Southsouth", progress: 81, lgas: 124 }
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
      zones[idx].tz === "Asia/Dubai"
        ? '<span class="rhgi-clock-tz">UTC+4</span>'
        : "";
    return (
      '<div class="rhgi-clock-wrap" data-tz="' +
      zones[idx].tz +
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

  function clockPartsForTZ(tz, now) {
    var fmt = new Intl.DateTimeFormat("en-GB", {
      timeZone: tz,
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      hour12: false
    });
    var parts = fmt.formatToParts(now);
    var h24 = 0;
    var Mi = 0;
    var Se = 0;
    parts.forEach(function (p) {
      if (p.type === "hour") {
        h24 = parseInt(p.value, 10);
      }
      if (p.type === "minute") {
        Mi = parseInt(p.value, 10);
      }
      if (p.type === "second") {
        Se = parseInt(p.value, 10);
      }
    });
    return { h24: h24, Mi: Mi, Se: Se };
  }

  function updateSovereignClocks() {
    var row = document.getElementById("rhgi-clocksRow");
    if (!row) {
      return;
    }
    var now = new Date();
    row.querySelectorAll(".rhgi-clock-wrap").forEach(function (wrap) {
      var tz = wrap.getAttribute("data-tz");
      var t = clockPartsForTZ(tz, now);
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

  function buildRegionalWidgets() {
    regionalWidgets.forEach(function (w) {
      var bar = document.getElementById("rhgi-bar-" + w.key);
      var a = document.getElementById("rhgi-lineA-" + w.key);
      var b = document.getElementById("rhgi-lineB-" + w.key);
      var line =
        w.label +
        " · " +
        w.lgas +
        " LGAs · progress " +
        w.progress +
        "% · ward relay synced";
      if (bar) {
        requestAnimationFrame(function () {
          bar.style.width = w.progress + "%";
        });
      }
      if (a) {
        a.textContent = line;
      }
      if (b) {
        b.textContent = line;
      }
    });
  }

  var pulseTimer = null;

  function startPulseInterval() {
    if (pulseTimer !== null) {
      return;
    }
    pulseTimer = setInterval(updateSovereignClocks, 1000);
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
    var fill = document.getElementById("rhgi-gaugeFill");
    var diamond = document.getElementById("rhgi-abujaDiamond");
    var ratio = (RHGI_STATE_NOW / RHGI_STATE_MAX) * 100;
    if (fill) {
      requestAnimationFrame(function () {
        fill.style.width = ratio + "%";
      });
    }
    if (diamond) {
      diamond.style.opacity = RHGI_STATE_NOW / RHGI_STATE_MAX >= 0.25 ? "1" : "0.45";
    }
  }

  function onReady() {
    lockDataAnchor();
    initConstitutionalGauge();
    updateCountdown();
    buildRegionalWidgets();
    buildTicker774();
    renderClockFaces();
    updateSovereignClocks();
    startPulseInterval();
    setInterval(updateCountdown, 1000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
