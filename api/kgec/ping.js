/**
 * V203 — K-GEC / AWC-C&D private core ping (server-side gate).
 * Requires HttpOnly session cookie minted by POST /api/sovereign/mint-session
 */
export default function handler(req, res) {
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.setHeader("Allow", "GET, HEAD");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }
  const has = typeof req.headers.cookie === "string" && req.headers.cookie.includes("gcslc_http_sovereign=1");
  if (!has) {
    res.setHeader("Cache-Control", "no-store");
    return res.status(401).json({ ok: false, layer: "k-gec", state: "dormant" });
  }
  res.setHeader("Cache-Control", "no-store");
  return res.status(200).json({
    ok: true,
    engine: "K-GEC/AWC-C&D",
    layer: "private",
    pulse: "live",
    note: "Komi Generative Eagle Cloud — server-gated envelope (no secrets in HTML).",
  });
}
