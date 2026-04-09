module.exports = {
  apps: [
    {
      name: "presidential_8505",
      script: "python3",
      args: "-m streamlit run 14314/app.py --server.port 8505 --server.address 0.0.0.0",
      cwd: "/Users/user/Desktop/GCSLC_Sovereign_Gateway",
      autorestart: true,
      watch: false,
      max_restarts: 50,
      restart_delay: 3000,
    },
    {
      name: "operational_8506",
      script: "python3",
      args: "-m streamlit run 14314/ops_app.py --server.port 8506 --server.address 0.0.0.0",
      cwd: "/Users/user/Desktop/GCSLC_Sovereign_Gateway",
      autorestart: true,
      watch: false,
      max_restarts: 50,
      restart_delay: 3000,
    },
    {
      name: "convener_tunnel_8505",
      script: "npx",
      args: "--yes localtunnel --port 8505 --subdomain sovereign-exec-8505",
      cwd: "/Users/user/Desktop/GCSLC_Sovereign_Gateway",
      autorestart: true,
      watch: false,
      max_restarts: 200,
      restart_delay: 5000,
    },
  ],
};
