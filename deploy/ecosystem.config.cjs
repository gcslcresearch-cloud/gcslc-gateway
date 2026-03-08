// PM2 config for NVFC Gradio Dashboard (Mac/Linux)
// Usage: from repo root run:
//   pm2 start deploy/ecosystem.config.cjs
//   pm2 save && pm2 startup   # persist across reboot
//   pm2 logs nvfc-gradio

module.exports = {
  apps: [
    {
      name: "nvfc-gradio",
      script: "nvfc_gradio.py",
      interpreter: "python3",
      cwd: "/Users/user/Desktop/GCSLC_Sovereign_Gateway",
      autorestart: true,
      watch: false,
      max_restarts: 10,
      min_uptime: "5s",
      env: {},
    },
  ],
};
