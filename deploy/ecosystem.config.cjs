// PM2 config for NVFC Gradio Dashboard (Mac/Linux)
// Script path is resolved relative to this file so it works from any install path.
const path = require("path");

const repoRoot = path.resolve(__dirname, "..");
const scriptPath = path.join(repoRoot, "nvfc_gradio.py");
const venvPython = path.join(repoRoot, ".venv", "bin", "python");

module.exports = {
  apps: [
    {
      name: "NVFC-COMMAND",
      script: scriptPath,
      interpreter: venvPython,
      cwd: repoRoot,
      autorestart: true,
      watch: false,
      max_restarts: 10,
      min_uptime: "5s",
      restart_delay: 4000,
      env: {},
    },
  ],
};
