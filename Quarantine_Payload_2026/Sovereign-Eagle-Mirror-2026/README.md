# Sovereign Protocol - Sovereign Eagle Mirror 2026

This document is the operational constitution for the merged workspace `Sovereign-Eagle-Mirror-2026`.
It defines merger intent, 8R Stealth Paradigm logic, and data contracts for contact intelligence and polling-unit mapping.

## 1) Merger Protocol (Total Sovereign Merger)

### Mission
- Consolidate intelligence and institutional layers into one durable operating workspace.
- Preserve `Zaria (11.0855 N, 7.7200 E)` as the primary sovereign anchor.
- Maintain a hardened 4-pillar architecture for modular continuity and auditability.

### Source and Destination
- Source folder: `Sovereign-Eagle-Corridor-Alpha` (intelligence layer)
- Master folder: `Sovereign-Eagle-Mirror-2026` (institutional foundation)

### Graft Operations Completed
- `buildQuadPillarReality` logic migrated into:
  - `Part_03_Security/build_quad_pillar_reality.py`
- Northern Pulse market coordinates ingested into:
  - `Part_03_Security/data/northern_pulse_markets.json`
  - `Part_04_Social/data/northern_pulse_markets.json`
- Distance-to-Service analytics deployed in:
  - `Part_04_Social/distance_to_service.py`
- Human Residence nodes initialized in:
  - `Part_04_Social/data/human_residence_nodes.json`
  - Nodes: `Binji/Danchadi`, `Goronyo`, `Dekina`
- Unified UI rebuilt in:
  - `app.py` (Deep Navy Blue + Quad-Pillar HUD + Zaria-first map logic)

### Integrity Layout (4-Pillar)
- `Part_01_Institutional`
- `Part_02_Finance`
- `Part_03_Security`
- `Part_04_Social`

---

## 2) 8R Stealth Paradigm Logic

The 8R Stealth Paradigm is the campaign-to-infrastructure execution doctrine used to move from raw field signals to controlled action.

- `R1 Rebuild` - recover trust and baseline signal integrity.
- `R2 Reactivate` - re-engage dormant supporters and inactive wards.
- `R3 Retarget` - re-score persuasion clusters using observed behavior.
- `R4 Reinforce` - harden ballot and incident response channels.
- `R5 Remessage` - adapt narratives per demographic and corridor economics.
- `R6 Reconcile` - align internal structures to one turnout covenant.
- `R7 Rehearse` - simulate election-day logistics and escalation drills.
- `R8 Reward` - amplify high-performing cells with resources and visibility.

### In-Mirror Application
- COMM pillar: signal clarity, communication velocity, and outage resilience.
- FIN pillar: liquidity/service gravity and inclusion coverage.
- SEC pillar: corridor stability, incident pressure, and hardening posture.
- SOC pillar: well-being links between services, mobility, and communities.

---

## 3) Data Contracts

Data contracts define required fields, types, quality checks, and interoperability across ingestion pipelines.

### 3.1 Kaduna Contacts Contract (2.0M Capacity Schema)

Purpose: support up to 2,000,000 contact records for outreach, stratification, and compliance-safe activation.

#### Entity: `kaduna_contacts_v2`
- `contact_id` (string, required, unique) - deterministic UUID or hash key.
- `full_name` (string, required)
- `phone_e164` (string, required) - normalized phone format (`+234...`).
- `ward_code` (string, required) - joins to polling-ward map.
- `lga_code` (string, required)
- `state_code` (string, required, default `KD`)
- `gender` (string, optional, enum constrained)
- `age_band` (string, optional, enum constrained)
- `language_pref` (string, optional)
- `engagement_score` (number, optional, range `0..100`)
- `support_score` (number, optional, range `0..100`)
- `last_contacted_at` (datetime, optional)
- `channel_opt_in_sms` (boolean, required)
- `channel_opt_in_voice` (boolean, required)
- `consent_status` (string, required, enum: `granted|revoked|pending`)
- `source_system` (string, required)
- `created_at` (datetime, required)
- `updated_at` (datetime, required)

#### Required Quality Rules
- No duplicate `phone_e164`.
- Referential integrity on `ward_code`, `lga_code`.
- Reject records missing consent flags.
- Preserve full append-only audit trail on score changes.

### 3.2 Polling Unit Mapping Contract

Purpose: geospatial intelligence layer for coverage analysis, turnout strategy, and routing.

#### Entity: `polling_units_v1`
- `pu_id` (string, required, unique)
- `pu_name` (string, required)
- `registration_area_code` (string, required)
- `ward_code` (string, required)
- `lga_code` (string, required)
- `latitude` (number, required)
- `longitude` (number, required)
- `status` (string, required, enum: `active|inactive|relocated`)
- `voter_count_est` (integer, optional)
- `risk_tier` (string, optional, enum: `low|medium|high|critical`)
- `nearest_service_id` (string, optional, foreign key to service infrastructure)
- `distance_to_service_km` (number, optional)
- `updated_at` (datetime, required)

#### Geospatial/Logic Rules
- Coordinate CRS: WGS84 decimal degrees.
- Zaria anchor remains immutable reference for corridor calculations.
- Distance calculations use haversine method.
- Mapping feed must preserve one-to-one consistency between `pu_id` and location pair.

### 3.3 Distance-to-Service Contract (Villages)

#### Input
- `name` (string)
- `lat` (number)
- `lon` (number)

#### Output
- `village` (string)
- `nearest_service` (string)
- `service_kind` (string; `bank|tower`)
- `distance_km` (number, rounded to 2 decimals)

---

## 4) Runtime and Startup

From inside `Sovereign-Eagle-Mirror-2026`:

```bash
streamlit run app.py
```

Default local URL (if port is free): `http://localhost:8501`

---

## 5) Operational Notes

- The interface is designed around a Deep Navy Blue institutional visual.
- Quad-Pillar HUD (`COMM`, `FIN`, `SEC`, `SOC`) is continuously animated.
- Zaria anchor is always rendered as the sovereign map heart.
- Human Residence forensic lines expose village-to-service gaps in real time.
