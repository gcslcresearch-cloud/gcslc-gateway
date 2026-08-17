/**
 * MNO Verification Sandbox — OTP request (stateless).
 * Only authorized operator emails may request OTP (AT / MNO audit gate).
 */
const crypto = require("crypto");

const STORE = globalThis.__mnoOtpStore || (globalThis.__mnoOtpStore = new Map());

const ALLOWED = new Set(
  String(process.env.MNO_ALLOWED_EMAILS || "gcslc.research@gmail.com,info@galadimanruwacenter.org")
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean)
);

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(body));
}

function pickSender(lane) {
  const L = String(lane || "domestic").toLowerCase();
  if (L === "intl" || L === "industrial" || L === "gcslcintel") return "GCSLCINTEL";
  return "GaladimaR";
}

function hashOtp(otp, salt) {
  return crypto.createHmac("sha256", salt).update(String(otp)).digest("hex");
}

function normEmail(s) {
  return String(s || "").trim().toLowerCase();
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

  const email = normEmail(body.email);
  if (!email || !email.includes("@")) {
    return json(res, 422, { error: "email_required" });
  }
  if (!ALLOWED.has(email)) {
    return json(res, 403, {
      error: "email_not_authorized",
      hint: "Only GCSLC operator emails listed on the MNO filing may clear this airlock.",
    });
  }

  const senderId = pickSender(body.lane);
  const otp = String(crypto.randomInt(100000, 999999));
  const salt = (process.env.MNO_OTP_HMAC_SECRET || "SNI-VAI-SANDBOX-NOT-PRODUCTION").trim();
  const ttlSec = Math.min(300, Math.max(60, Number(process.env.MNO_OTP_TTL_SEC || 180)));
  const sessionId = crypto.randomBytes(16).toString("hex");
  const expiresAt = Date.now() + ttlSec * 1000;

  STORE.set(sessionId, {
    emailFp: crypto.createHash("sha256").update(email + salt).digest("hex").slice(0, 32),
    otpHash: hashOtp(otp, salt),
    senderId,
    expiresAt,
  });

  for (const [k, v] of STORE) {
    if (v.expiresAt < Date.now()) STORE.delete(k);
  }

  const echo = String(process.env.MNO_SANDBOX_ECHO || "1") === "1";
  const provider = (process.env.MNO_OTP_PROVIDER || "sandbox_issue").trim();

  return json(res, 200, {
    ok: true,
    staging: true,
    initiative: "SNI-VAI",
    session_id: sessionId,
    sender_id: senderId,
    authorized_email: email,
    provider,
    ttl_sec: ttlSec,
    message:
      provider === "sandbox_issue"
        ? `Sandbox: OTP for ${email} would be delivered via Sender ID ${senderId} (transactional DND path).`
        : `OTP dispatch requested via ${senderId}.`,
    sandbox_otp: echo ? otp : undefined,
    law: "Email must be on the operator allow-list. Session expires with TTL. Not a citizen warehouse.",
  });
};
