# NVFC Gradio Dashboard — Persistent Deploy

## Gradio configuration (in app)

- `share=True` — public URL (bypasses local browser/connection issues)
- `server_port=7860`
- `show_error=True` — surface errors in UI

## Option A: PM2 (Mac or Linux)

1. Install PM2: `npm install -g pm2`
2. From repo root, edit `deploy/ecosystem.config.cjs` and set `cwd` to your repo path.
3. Start:
   ```bash
   cd /Users/user/Desktop/GCSLC_Sovereign_Gateway
   pm2 start deploy/ecosystem.config.cjs
   ```
4. Persist across reboot:
   ```bash
   pm2 save
   pm2 startup
   ```
5. Commands: `pm2 status` | `pm2 logs nvfc-gradio` | `pm2 restart nvfc-gradio`

## Option B: systemd (Linux only)

1. Copy and edit the service file:
   ```bash
   sudo cp deploy/nvfc-gradio.service /etc/systemd/system/
   sudo nano /etc/systemd/system/nvfc-gradio.service
   ```
   Set `User`, `WorkingDirectory`, `Environment=PATH`, and `ExecStart` to your user and repo path (and venv if used).

2. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable nvfc-gradio
   sudo systemctl start nvfc-gradio
   ```

3. Status / logs: `sudo systemctl status nvfc-gradio` | `journalctl -u nvfc-gradio -f`
