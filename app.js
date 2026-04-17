(() => {
  const root = window;
  const defaults = {
    version: "INSTITUTIONAL_MATRIX_V34_EXPANSION",
    theme: {
      font: "Goldman",
      background: "#001a33",
    },
    senderWhitelist: ["GALADIMA_R"],
    institutionalTicker: ["CBN", "NNPCL", "RMAFC", "NSA", "NIMASA", "NAHCON"],
    institutionalTickerSecondary: ["AMCON", "NDIC", "NHIS", "Hajj Commission", "INEC"],
    opportunityNodes: ["Federal Ministry of Works", "SMEDAN", "ITF", "NEMA"],
    alertTriggerNodes: ["Police", "Immigration"],
    sovereignKeys: ["LW15954", "GCSLC2026", "SOVEREIGN_MANDATE"],
    kadunaPopulation: 2000000,
    kadunaLgaCount: 23,
  };

  root.GCSLC_APP_V34 = Object.assign({}, defaults, root.GCSLC_APP_V34 || {});
  root.GCSLC_APP_V33 = root.GCSLC_APP_V34;
  root.GCSLC_APP_V32 = root.GCSLC_APP_V34;
  root.GCSLC_APP_V30 = root.GCSLC_APP_V34;
})();
