/**
 * V203 — Mint HttpOnly sovereign session after passphrase verification (server-side).
 * Set GCSLC_SOVEREIGN_KEY in Vercel env (do not commit secrets).
 */
import crypto from "crypto";

function timingSafeEqualStr(a, b) {
  const ab = Buffer.from(String(a || ""), "utf8");
  const bb = Buffer.from(String(b || ""), "utf8");
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
}

export default function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }
  const expected = process.env.GCSLC_SOVEREIGN_KEY || "";
  if (!expected) {
    return res.status(503).json({ ok: false, error: "sovereign_key_not_configured" });
  }
  let body = req.body;
  if (typeof body === "string") {
    try {
      body = JSON.parse(body || "{}");
    } catch {
      body = {};
    }
  }
  if (!body || typeof body !== "object") body = {};
  const key = body.key || body.passphrase || body.sovereignKey || body.sovereign_key || "";
  if (!timingSafeEqualStr(key, expected)) {
    res.setHeader("Cache-Control", "no-store");
    return res.status(401).json({ ok: false, error: "sovereign_key_invalid" });
  }
  const maxAge = 365 * 24 * 60 * 60;
  const secure = process.env.VERCEL === "1" ? "; Secure" : "";
  res.setHeader(
    "Set-Cookie",
    `gcslc_http_sovereign=1; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAge}${secure}`
  );
  res.setHeader("Cache-Control", "no-store");
  return res.status(200).json({ ok: true, minted: "http_only_session" });
}
