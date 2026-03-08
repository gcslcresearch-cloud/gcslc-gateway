// PM2 config for NVFC Gradio Dashboard (Mac/Linux)
// Script path is resolved relative to this file so it works from any install path.
const path = require("path");

const repoRoot = path.resolve(__dirname, "..");
const scriptPath = path.join(repoRoot, "nvfc_gradio.py");

module.exports = {
  apps: [
    {
      name: "nvfc-gradio",
      script: scriptPath,
      interpreter: "python3",
      cwd: repoRoot,
      autorestart: true,
      watch: false,
      max_restarts: 10,
      min_uptime: "5s",
      env: {},
    },
  ],
};
