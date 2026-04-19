/**
 * GCSLC Listening Post — Termii-compatible handshake receiver (Vercel serverless).
 * POST JSON increments pulseSeq (in-memory, warm-instance) so the dashboard can poll GET
 * and fire NAFC inbound pulse + cyan key flash (Directive #30).
 */
var handshakePulseSeq = 0;
var handshakeLastTs = null;

function parseBody(req) {
  var raw = req.body;
  if (raw == null || raw === "") return {};
  if (typeof raw === "string") {
    try {
      return JSON.parse(raw);
    } catch (_) {
      return null;
    }
  }
  if (typeof raw === "object") return raw;
  return {};
}

function setCors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept");
}

export default function handler(req, res) {
  setCors(res);

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      service: "gcslc-handshake-v30",
      listening: true,
      path: "/api/handshake",
      methods: ["POST"],
      pulseSeq: handshakePulseSeq,
      lastPingTs: handshakeLastTs,
      note:
        "POST application/json simulates Termii test ping; pulseSeq increments. Dashboard polls this endpoint to auto-pulse NAFC inbound.",
    });
  }

  if (req.method !== "POST") {
    res.setHeader("Allow", "GET, POST, OPTIONS");
    return res.status(405).json({ ok: false, error: "Method Not Allowed" });
  }

  var body = parseBody(req);
  if (body === null) {
    return res.status(400).json({ ok: false, error: "Invalid JSON body" });
  }

  handshakePulseSeq += 1;
  handshakeLastTs = new Date().toISOString();

  return res.status(200).json({
    ok: true,
    received: true,
    nafcInboundPulse: true,
    pulseSeq: handshakePulseSeq,
    lastPingTs: handshakeLastTs,
    snapshot: body,
    ts: handshakeLastTs,
  });
}
