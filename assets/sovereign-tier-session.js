/**
 * GCSLC / AWC · K-GEC — session gate disabled: dashboard loads unlocked (no expiry lock).
 * Tier timer / Access Expired overlay logic removed per Tier 3 override.
 * NRRFC 24h free pass: hides Access Expired / LW15954 modal for 24h from first page load (per browser).
 */
(function (global) {
  'use strict';

  var KEY_NRRFC_PASS_START = 'gcslc_nrrfc_free_pass_start_v1';
  var MS_24H = 86400000;

  var KEY_VISITOR_BRIDGE = 'gcslc_sovereign_bridge_v1';
  var KEY_CHAIRMAN_GATE = 'gcslc_gate_chairman_v1';

  function isChairmanMode() {
    try {
      if (new URLSearchParams(global.location.search || '').get('mode') === 'chairman') {
        return true;
      }
      return localStorage.getItem(KEY_CHAIRMAN_GATE) === '1';
    } catch (e) {
      return false;
    }
  }

  global.GCSLC_CHAIRMAN_IMMUNITY = isChairmanMode();

  var KEY_START = 'gcslc_awc_kgec_sovereign_session_start_v1';
  var KEY_EXPIRED = 'gcslc_awc_kgec_sovereign_session_expired_v1';

  function unlockUi() {
    document.documentElement.classList.remove('sovereign-access-expired');
    var modal = document.getElementById('sovereignTierExpiredModal');
    if (modal) {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
    }
  }

  function isNrrfc24hPassActive() {
    try {
      var raw = localStorage.getItem(KEY_NRRFC_PASS_START);
      var t0 = raw ? parseInt(raw, 10) : NaN;
      if (!raw || isNaN(t0)) {
        t0 = Date.now();
        localStorage.setItem(KEY_NRRFC_PASS_START, String(t0));
      }
      return Date.now() - t0 < MS_24H;
    } catch (e) {
      return false;
    }
  }

  function applyNrrfcFreePassIfActive() {
    try {
      if (!isNrrfc24hPassActive()) return;
      document.documentElement.classList.add('gcslc-nrrfc-free-pass');
      unlockUi();
      if (document.getElementById('gcslc-nrrfc-free-pass-style')) return;
      var st = document.createElement('style');
      st.id = 'gcslc-nrrfc-free-pass-style';
      st.textContent =
        '#sovereignTierExpiredModal{display:none!important;visibility:hidden!important;pointer-events:none!important;opacity:0!important;}';
      (document.head || document.documentElement).appendChild(st);
    } catch (e) {}
  }

  /** Clears legacy timer keys (logout / intake parity); does not lock UI. */
  function resetSovereignSession() {
    try {
      localStorage.removeItem(KEY_START);
      localStorage.removeItem(KEY_EXPIRED);
    } catch (e) {}
  }

  function armFreshThirtyMinuteSession() {
    resetSovereignSession();
    unlockUi();
  }

  function init() {
    try {
      if (new URLSearchParams(global.location.search || '').get('mode') === 'chairman') {
        localStorage.setItem(KEY_CHAIRMAN_GATE, '1');
      }
    } catch (e) {}
    applyNrrfcFreePassIfActive();
    unlockUi();
    global.GCSLC_CHAIRMAN_IMMUNITY = isChairmanMode();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.resetSovereignSession = resetSovereignSession;

  global.GCSLC_SOVEREIGN_SESSION = {
    remainingMs: function () {
      return Number.POSITIVE_INFINITY;
    },
    formatRemaining: function () {
      return '—';
    },
    lock: function () {},
    armFreshThirtyMinuteSession: armFreshThirtyMinuteSession,
    visitorLogout: function () {
      try {
        localStorage.removeItem(KEY_VISITOR_BRIDGE);
        localStorage.removeItem(KEY_CHAIRMAN_GATE);
      } catch (e) {}
      resetSovereignSession();
      unlockUi();
      global.location.href = 'sovereign-mirror.html';
    },
    unlockUi: unlockUi,
    isChairmanMode: function () {
      return global.GCSLC_CHAIRMAN_IMMUNITY === true;
    }
  };
})(window);
