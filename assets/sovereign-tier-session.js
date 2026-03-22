/**
 * GCSLC / AWC · K-GEC Sovereign OS — cumulative 30m session (Tier 1 + Tier 2).
 * STRIKE 1968v24: ?mode=chairman — no session timer interval, no expiry lock (unlimited for that load).
 * Visitors: hard 30-minute cumulative limit from KEY_START; tick runs every 1s.
 */
(function (global) {
  'use strict';

  var KEY_START = 'gcslc_awc_kgec_sovereign_session_start_v1';
  var KEY_EXPIRED = 'gcslc_awc_kgec_sovereign_session_expired_v1';
  var STORAGE_PREFIX = 'gcslc_awc_kgec_sovereign';
  var TOTAL_MS = 30 * 60 * 1000;
  var TIER1_MS = 15 * 60 * 1000;

  function isChairmanMode() {
    try {
      return new URLSearchParams(global.location.search || '').get('mode') === 'chairman';
    } catch (e) {
      return false;
    }
  }

  global.GCSLC_CHAIRMAN_IMMUNITY = isChairmanMode();

  function ts() {
    return Date.now();
  }

  function chairmanGuard() {
    return global.GCSLC_CHAIRMAN_IMMUNITY === true;
  }

  /**
   * Master Reset Protocol — clears timer-related localStorage + sessionStorage.
   */
  function resetSovereignSession() {
    try {
      localStorage.removeItem(KEY_START);
      localStorage.removeItem(KEY_EXPIRED);
      var lk = [];
      var i;
      for (i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i);
        if (k && k.indexOf(STORAGE_PREFIX) === 0) lk.push(k);
      }
      for (i = 0; i < lk.length; i++) localStorage.removeItem(lk[i]);
    } catch (e) {}

    try {
      var sk = [];
      for (i = 0; i < sessionStorage.length; i++) {
        var key = sessionStorage.key(i);
        if (key && key.indexOf(STORAGE_PREFIX) === 0) sk.push(key);
      }
      for (i = 0; i < sk.length; i++) sessionStorage.removeItem(sk[i]);
    } catch (e2) {}
  }

  function isExpiredFlag() {
    if (chairmanGuard()) return false;
    try {
      return localStorage.getItem(KEY_EXPIRED) === '1';
    } catch (e) {
      return false;
    }
  }

  function setExpiredFlag() {
    if (chairmanGuard()) return;
    try {
      localStorage.setItem(KEY_EXPIRED, '1');
    } catch (e) {}
  }

  function ensureStart() {
    if (chairmanGuard()) return;
    try {
      var s = localStorage.getItem(KEY_START);
      if (!s) {
        localStorage.setItem(KEY_START, String(ts()));
      }
    } catch (e) {}
  }

  function remainingMs() {
    if (chairmanGuard()) return TOTAL_MS;
    if (isExpiredFlag()) return 0;
    ensureStart();
    var startT = 0;
    try {
      startT = parseInt(localStorage.getItem(KEY_START), 10) || ts();
    } catch (e) {
      startT = ts();
    }
    var elapsed = ts() - startT;
    return Math.max(0, TOTAL_MS - elapsed);
  }

  function formatMMSS(ms) {
    var s = Math.ceil(ms / 1000);
    var m = Math.floor(s / 60);
    s = s % 60;
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function lockUi() {
    if (chairmanGuard()) return;
    document.documentElement.classList.add('sovereign-access-expired');
    var modal = document.getElementById('sovereignTierExpiredModal');
    if (modal) {
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
    }
    try {
      sessionStorage.clear();
    } catch (e) {}
  }

  function unlockUi() {
    document.documentElement.classList.remove('sovereign-access-expired');
    var modal = document.getElementById('sovereignTierExpiredModal');
    if (modal) {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
    }
  }

  function sovereignLogout() {
    if (chairmanGuard()) return;
    setExpiredFlag();
    lockUi();
  }

  function tick() {
    if (chairmanGuard()) return;
    if (isExpiredFlag()) {
      lockUi();
      return;
    }
    var rem = remainingMs();
    if (rem <= 0) {
      sovereignLogout();
      return;
    }
    var txt = formatMMSS(rem);
    var els = document.querySelectorAll('.sovereign-tier-remaining');
    for (var i = 0; i < els.length; i++) els[i].textContent = txt;
    var tierLabel = rem > TIER1_MS ? 'Tier 1 active' : 'Tier 2 active';
    var tw = document.querySelectorAll('.sovereign-tier-which');
    for (var j = 0; j < tw.length; j++) tw[j].textContent = tierLabel;
  }

  function armFreshThirtyMinuteSession() {
    if (chairmanGuard()) return;
    unlockUi();
    try {
      localStorage.setItem(KEY_START, String(ts()));
      localStorage.removeItem(KEY_EXPIRED);
    } catch (e) {}
    tick();
  }

  /** Visitor: clear session storage and reload (logout parity). */
  function visitorSovereignLogout() {
    if (chairmanGuard()) {
      global.location.reload();
      return;
    }
    resetSovereignSession();
    unlockUi();
    global.location.reload();
  }

  function initChairmanImmunity() {
    document.documentElement.classList.add('gcslc-chairman-immunity');
    try {
      localStorage.removeItem(KEY_EXPIRED);
    } catch (e) {}
    unlockUi();
    var els = document.querySelectorAll('.sovereign-tier-remaining');
    var i;
    for (i = 0; i < els.length; i++) els[i].textContent = '—';
    var tw = document.querySelectorAll('.sovereign-tier-which');
    for (i = 0; i < tw.length; i++) tw[i].textContent = 'Chairman immunity';
  }

  function init() {
    if (chairmanGuard()) {
      initChairmanImmunity();
      return;
    }
    if (isExpiredFlag()) {
      lockUi();
      return;
    }
    ensureStart();
    if (remainingMs() <= 0) {
      sovereignLogout();
      return;
    }
    tick();
    setInterval(tick, 1000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.resetSovereignSession = resetSovereignSession;

  global.GCSLC_SOVEREIGN_SESSION = {
    remainingMs: remainingMs,
    formatRemaining: function () {
      return formatMMSS(remainingMs());
    },
    lock: sovereignLogout,
    armFreshThirtyMinuteSession: armFreshThirtyMinuteSession,
    visitorLogout: visitorSovereignLogout,
    unlockUi: unlockUi,
    isChairmanMode: function () {
      return chairmanGuard();
    }
  };
})(window);
