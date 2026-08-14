export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ ok: false });
    return;
  }
  const pin = (process.env.AIDRI_VAULT_PIN || "").trim();
  if (!pin) {
    res.status(503).json({ ok: false, detail: "vault_pin_unset" });
    return;
  }
  let body = {};
  try {
    body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
  } catch {
    body = {};
  }
  const offered = String(body.pin || "").trim();
  if (!offered || offered !== pin) {
    res.status(401).json({ ok: false });
    return;
  }
  res.setHeader(
    "Set-Cookie",
    "aidri_vault=1; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=43200"
  );
  res.status(200).json({ ok: true, node0: "WAIT_TERMII" });
}
