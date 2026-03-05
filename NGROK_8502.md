# ngrok tunnel for port 8502 (dashboard on S24 Ultra)

## 1. Get ngrok in the project folder

- **If you see "Command Not Found"** — ngrok is not in your project or PATH.
  - Download: [ngrok.com/download](https://ngrok.com/download) (choose **macOS**, then ARM64 if you're on M1/M2/M3).
  - Unzip the archive and **move the `ngrok` file** into:
    ```
    ~/Desktop/GCSLC_Sovereign_Gateway/
    ```
  - So the path is: `~/Desktop/GCSLC_Sovereign_Gateway/ngrok`

- **If you see "Permission Denied"** — the file is there but not executable. The script below will fix that.

## 2. Make ngrok executable (if it’s in the project folder)

From the project root, either run the helper script (it does `chmod +x` for you) or run by hand:

```bash
cd ~/Desktop/GCSLC_Sovereign_Gateway
chmod +x ngrok
```

## 3. Add your authtoken (one-time)

Get your token from [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken), then:

```bash
cd ~/Desktop/GCSLC_Sovereign_Gateway
./ngrok config add-authtoken YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with your actual ngrok authtoken.

## 4. Start the tunnel on port 8502

**Option A — Use the script (recommended):**

```bash
cd ~/Desktop/GCSLC_Sovereign_Gateway
./run_ngrok_8502.sh
```

**Option B — Run ngrok directly:**

```bash
cd ~/Desktop/GCSLC_Sovereign_Gateway
./ngrok http 8502
```

## 5. Open on your S24 Ultra

- Start your Streamlit app on **port 8502** (e.g. `streamlit run app.py --server.port 8502`).
- After ngrok starts, copy the **HTTPS** URL ngrok shows (e.g. `https://abc123.ngrok-free.app`) and open it on your S24 Ultra to view the dashboard.
