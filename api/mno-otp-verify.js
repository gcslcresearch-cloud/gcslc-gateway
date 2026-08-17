/**
 * MNO Verification Sandbox — OTP verify → clearance token (stateless cookie).
 */
const crypto = require("crypto");

const STORE = globalThis.__mnoOtpStore || (globalThis.__mnoOtpStore = new Map());

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(body));
}

function hashOtp(otp, salt) {
  return crypto.createHmac("sha256", salt).update(String(otp)).digest("hex");
}

function mintClearance(secret) {
  const exp = Date.now() + 30 * 60 * 1000;
  const payload = Buffer.from(JSON.stringify({ v: 1, exp, lane: "mno_sandbox" })).toString("base64url");
  const sig = crypto.createHmac("sha256", secret).update(payload).digest("base64url");
  return `${payload}.${sig}`;
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return json(res, 405, { error: "method_not_allowed" });

  let body = {};
  try {
    const chunks = [];
    for await (const c of req) chunks.push(c);
    body = JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
  } catch {
    return json(res, 400, { error: "invalid_json" });
  }

  const sessionId = String(body.session_id || "").trim();
  const otp = String(body.otp || "").trim();
  const salt = (process.env.MNO_OTP_HMAC_SECRET || "SNI-VAI-SANDBOX-NOT-PRODUCTION").trim();
  const gateSecret = (process.env.MNO_GATE_SECRET || salt).trim();

  const row = STORE.get(sessionId);
  if (!row) return json(res, 401, { error: "session_expired_or_unknown" });
  if (row.expiresAt < Date.now()) {
    STORE.delete(sessionId);
    return json(res, 401, { error: "otp_expired" });
  }
  const expected = row.otpHash;
  const got = hashOtp(otp, salt);
  if (expected.length !== got.length || !crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(got))) {
    return json(res, 401, { error: "otp_invalid" });
  }

  STORE.delete(sessionId);
  const token = mintClearance(gateSecret);
  const secure = process.env.VERCEL ? "; Secure" : "";
  res.setHeader(
    "Set-Cookie",
    `mno_clearance=${token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=1800${secure}`
  );

  return json(res, 200, {
    ok: true,
    cleared: true,
    sender_id_used: row.senderId,
    message: "Clearance granted. Stateless airlock — no MSISDN stored.",
  });
};
