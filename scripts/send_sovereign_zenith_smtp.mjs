/**
 * Sovereign Zenith Node — outbound handshake (SendGrid API or SMTP via Nodemailer).
 *
 * Required for SendGrid:
 *   SENDGRID_API_KEY
 *   MAIL_FROM   (verified sender in SendGrid), e.g. noreply@yourdomain.com
 *
 * Required for SMTP (e.g. Gmail app password, transactional provider):
 *   SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
 *   SMTP_SECURE=true|false  (optional; default true for 465)
 *   MAIL_FROM
 *
 * Always:
 *   MAIL_TO=gcslc.research@gmail.com  (default below)
 */

import sgMail from "@sendgrid/mail";
import nodemailer from "nodemailer";

const MAIL_TO = process.env.MAIL_TO || "gcslc.research@gmail.com";
const MAIL_FROM = process.env.MAIL_FROM || "";
const LINK = "https://gcslc-gateway.vercel.app/advisory.html";

const subject = "FINAL_HANDSHAKE_VERIFICATION — Sovereign Zenith Node (8R)";

const text = [
  "Sovereign Zenith Node — manual SMTP handshake",
  "",
  `Isolated node (live): ${LINK}`,
  "",
  "8R Strategic Confirmation:",
  "D1–D8 determinants acknowledged; advisory traffic locked to ZENITH_INFRA_STRIKE on port 8848.",
  "Institutional header (GCSLC LTD/GTE) and Goldman Shimmering Cyan styling verified on live advisory route.",
  "",
  `Sent at: ${new Date().toISOString()}`,
].join("\n");

const html = `
  <p><strong>Sovereign Zenith Node — manual SMTP handshake</strong></p>
  <p>Isolated node (live): <a href="${LINK}">${LINK}</a></p>
  <p><strong>8R Strategic Confirmation:</strong> D1–D8 determinants acknowledged; advisory traffic locked to ZENITH_INFRA_STRIKE on port 8848.</p>
  <p>Institutional header (GCSLC LTD/GTE) and Goldman Shimmering Cyan styling verified on live advisory route.</p>
  <p style="color:#666;font-size:12px">Sent at ${new Date().toISOString()}</p>
`;

function logExit(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

async function sendSendGrid() {
  const key = process.env.SENDGRID_API_KEY;
  if (!key) return null;
  if (!MAIL_FROM) logExit("MAIL_FROM is required when using SENDGRID_API_KEY.", 1);
  sgMail.setApiKey(key);
  const [response] = await sgMail.send({
    to: MAIL_TO,
    from: MAIL_FROM,
    subject,
    text,
    html,
  });
  const h = response.headers || {};
  const mid =
    h["x-message-id"] ||
    h["X-Message-Id"] ||
    h["X-Message-ID"] ||
    "(see headers below)";
  console.log("[SendGrid] HTTP", response.statusCode);
  console.log("[SendGrid] Message-ID:", mid);
  console.log("[SendGrid] Headers:", JSON.stringify(h, null, 2));
  console.log("[SendGrid] Response body (first 800 chars):", String(response.body || "").slice(0, 800));
  return true;
}

async function sendSmtp() {
  const host = process.env.SMTP_HOST;
  if (!host) return null;
  if (!MAIL_FROM) logExit("MAIL_FROM is required when using SMTP_*.", 1);
  const port = Number(process.env.SMTP_PORT || "465");
  const secure =
    String(process.env.SMTP_SECURE || "").toLowerCase() === "false"
      ? false
      : port === 465;
  const transporter = nodemailer.createTransport({
    host,
    port,
    secure,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });
  const info = await transporter.sendMail({
    from: MAIL_FROM,
    to: MAIL_TO,
    subject,
    text,
    html,
  });
  console.log("[SMTP] Message-ID:", info.messageId);
  console.log("[SMTP] Accepted:", info.accepted);
  console.log("[SMTP] Response:", info.response);
  return true;
}

async function main() {
  if (await sendSendGrid()) return;
  if (await sendSmtp()) return;
  logExit(
    [
      "No outbound mail credentials found.",
      "Set either:",
      "  SENDGRID_API_KEY + MAIL_FROM",
      "or:",
      "  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_FROM",
      "",
      "Example:",
      '  MAIL_FROM="verified-sender@yourdomain.com" SENDGRID_API_KEY="SG.xxx" npm run send:zenith-handshake',
    ].join("\n"),
    1
  );
}

main().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
