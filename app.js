(() => {
  const root = window;
  const defaults = {
    version: "SOVEREIGN_TOTAL_SYNC_V33",
    theme: {
      font: "Goldman",
      background: "#001a33",
    },
    senderWhitelist: ["GALADIMA_R"],
    institutionalTicker: ["CBN", "NNPCL", "RMAFC", "NSA", "NIMASA", "NAHCON"],
    institutionalTickerSecondary: ["AMCON", "NDIC", "NHIS", "Hajj Commission", "INEC"],
    alertTriggerNodes: ["Police", "Immigration"],
    sovereignKeys: ["LW15954", "GCSLC2026", "SOVEREIGN_MANDATE"],
    kadunaPopulation: 2000000,
    kadunaLgaCount: 23,
  };

  root.GCSLC_APP_V33 = Object.assign({}, defaults, root.GCSLC_APP_V33 || {});
  root.GCSLC_APP_V32 = root.GCSLC_APP_V33;
  root.GCSLC_APP_V30 = root.GCSLC_APP_V33;
})();
