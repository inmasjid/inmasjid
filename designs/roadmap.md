#### InMasjid
- **User Onboarding and RBAC**
  - Super Admin
  - Admin
  - Super Musallee
  - Musallee
  - Guest
- **Masjid Onboarding**
  - Adding Masjid with relevant information
  - Masjid CRUD Operations
  - Salah Time Integration (Hanafi and other Madhabs)
  - Iqaamah Time Integration
- **Advanced Search Functions**
  - Masjid By `Info`
  - Zuhr After 1:30PM near me
  - Last Fajr near me
  - First Isha near me
  - First Isha Near Cubbon Park
  - First Asr 5:30 PM from near the pinned location
  - Masjid Near Me with Active Iqaamah
  - Distance × Time × User Time
  - Closest and reachable time
- **Tasks**
  - Designs: Documented
  - Development: Containerized
  - Deployed: Home Server
  - Tested: Production Ready

<details>
<summary> InMasjid Discussions </summary>
# 🕌 Masjid & Iqaamah Search — Full Architecture & Design Log

**Purpose:**
This document logs the complete design discussion and decisions for implementing a high-scale, mobile-first prayer time search service using Postgres + PostGIS.
Intended to be attached to the PRD as a persistent design memory.
No information omitted.

---

## **1. Problem Context**

### **Entities**

* **Masjid**

  * 5 daily prayers.
  * At least 1 Jumu’ah (max 3).
  * Can have Eid ul Fitr & Eid ul Adha prayers (max 3 each).
* **Musallah**

  * 1 to 5 daily prayers.
  * Max 1 Jumu’ah.
  * No Eid prayers.
* **Eidgah**

  * No daily prayers, no Jumu’ah.
  * Only Eid ul Fitr & Eid ul Adha prayers (at least 1, max 3).
* **Madrasa**

  * No prayers.
  * Only Islamic classes.

---

### **Core Data**

* Current schema:

  * `masjid` table → masjid meta info, lat/lon.
  * `iqaamah` table → time-only columns for fajr, zuhr, asr, maghrib, isha.
* Times are **time-only**.
  Default date = **today** in server timezone (IST initially, later global).
* **Geocoding** is done in frontend; backend receives `(lat, lon)`.

---

### **Query Use Cases**

1. **Zuhr After 1:30PM near me**

   * `zuhr >= 13:30` for N nearest masjids.
2. **Last Fajr near me**

   * Latest fajr among N nearest masjids.
3. **First Isha near me**

   * Earliest isha among N nearest masjids.
4. **First Isha near Cubbon Park**

   * Same as (3) with different location.
5. **First Asr ≥ 17:30 near pinned location**

   * Earliest asr ≥ 17:30 among N nearest masjids.
6. **Masjid near me with active iqaamahs**

   * Next prayer time today > current time.
7. **Earliest upcoming Maghrib after now**

   * Earliest maghrib among N nearest masjids > current time.

---

## **2. Clarifications Agreed**

* **Radius not required** — only limit N results (default 10, user-defined).
* **Inclusive filtering** (`>=`).
* No date column in iqaamah table.
* No iqaamah today → exclude + return “no schedule”.
* Always return a list (even if single result).
* Masjid data is permanent — no expiry logic.
* Default timezone = IST for now.
* Notifications only on **iqaamah changes**.

---

## **3. Read vs. Write Load**

* **Reads:** \~100B QPS.
* **Writes:** \~10M QPS.
* Optimized for read-heavy workload.
* Extreme read optimization required.

---

## **4. Schema Decision**

**Chosen Approach:**

* Fully **denormalized hot-path table** (`masjid_iqaamah`) for masjid + musallah daily prayers.
* Separate tables for occasional prayers and non-prayer entities.

**Reason:**

* Avoid joins in hot path for extreme scale.
* Keep hot table as small as possible for fast KNN PostGIS lookups.

---

### **Hot Table: `masjid_iqaamah`**

Contains:

```
masjid_id, name, lat, lon, geom,
fajr, zuhr, asr, maghrib, isha,
jummah_times JSONB,
address, contact, timezone, last_updated
```

**Indexes:**

* GiST index on `geom` for nearest search.
* Partial indexes for each prayer column (`fajr`, `zuhr`, etc.).

---

### **Supporting Tables**

* **`eid_salah`** — Jumuah, Eid ul Fitr & Eid ul Adha only.

* **`eidgah_meta`** — Metadata & classes.

* **`madarsa_meta`** — Metadata & classes.

* **`general_audit`**

  * Logs important changes (3-day retention, then delete/archive).
  * Columns:

    ```
    id, entity_type, entity_id, field_changed,
    old_value, new_value, change_type, is_notifiable, changed_at
    ```
* **`notification_queue`**

  * Stores queued notifications for push, in-app, WhatsApp.

---

## **5. Audit & Notification Flow**

1. **Change detected** in iqaamah times.
2. Insert row in `general_audit` with `is_notifiable = true`.
3. If notifiable:

   * Fan-out to `notification_queue`.
   * Queue jobs for push notifications, WhatsApp and in-app banner.
4. If non-important change:

   * Log only, no notification.
5. Retain `general_audit` for 3 days; move to cold storage if needed.

---

## **6. NULL Bloat Solution**

* Madrasa and Eidgah **moved out of hot table** to avoid nulls in daily prayer columns.
* Occasional prayers stored in separate tables to keep hot table lean.

---

## **7. Extra Architectural Considerations**

1. **Index Bloat**

   * Partial indexes will grow large at global scale.
   * Schedule `REINDEX CONCURRENTLY` + tune autovacuum.
2. **KNN Cost**

   * PostGIS KNN is fast but only if index is selective; keep hot table minimal.
3. **Time vs. JSONB**

   * TIME columns for fixed daily prayers → faster than JSONB.
4. **Clock Drift**

   * Store `timezone` per masjid for future global support.
5. **Notification Scale**

   * At 100B DAU, multi-channel fan-out must be idempotent.
6. **Cold Storage**

   * Archive `general_audit` to S3 or columnar DB for analytics.
7. **UI-to-SQL Mapping**

   * Structured UI → prepared SQL queries with pre-analyzed plans.
8. **Geo Sharding**

   * Consider geographic sharding (`masjid_iqaamah_asia`, etc.) at extreme scale.

---

## **8. Final Design Summary**

* **`masjid_iqaamah`**

  * Denormalized table for Masjid + Musallah daily prayers.
* **`eid_salah`**

  * Occasional Eid prayers only.
* **`eidgah_meta`**

  * Metadata for eidgahs.
* **`madarsa_meta`**

  * Metadata for madrasas.
* **`general_audit`**

  * Logs important changes; triggers notifications on prayer time changes.
* **`notification_queue`**

  * Decouples notification fan-out from main DB writes.

---

## **10. SQL DDL — Final Schema**

```sql
-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- ========================================
-- HOT TABLE: Masjid & Musallah
-- ========================================
CREATE TABLE masjid_iqaamah (
    masjid_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    geom GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography) STORED,

    fajr TIME WITHOUT TIME ZONE,
    zuhr TIME WITHOUT TIME ZONE,
    asr TIME WITHOUT TIME ZONE,
    maghrib TIME WITHOUT TIME ZONE,
    isha TIME WITHOUT TIME ZONE,
    address TEXT,
    contact TEXT,
    timezone TEXT DEFAULT 'Asia/Kolkata',
    last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- Spatial index for nearest search
CREATE INDEX idx_masjid_geom ON masjid_iqaamah USING gist (geom);

-- Partial indexes for each prayer time
CREATE INDEX idx_fajr_time ON masjid_iqaamah (fajr) WHERE fajr IS NOT NULL;
CREATE INDEX idx_zuhr_time ON masjid_iqaamah (zuhr) WHERE zuhr IS NOT NULL;
CREATE INDEX idx_asr_time ON masjid_iqaamah (asr) WHERE asr IS NOT NULL;
CREATE INDEX idx_maghrib_time ON masjid_iqaamah (maghrib) WHERE maghrib IS NOT NULL;
CREATE INDEX idx_isha_time ON masjid_iqaamah (isha) WHERE isha IS NOT NULL;

-- ========================================
-- Eidgah Prayers
-- ========================================
CREATE TABLE eid_salah (
    place_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    geom GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography) STORED,
    eid_times JSONB, -- {"eid_ul_fitr": ["07:00"], "eid_ul_adha": ["07:15", "08:00"]}
    address TEXT,
    contact TEXT,
    timezone TEXT DEFAULT 'Asia/Kolkata',
    last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE INDEX idx_eidgah_geom ON eid_salah USING gist (geom);

-- ========================================
-- Eidgah
-- ========================================
CREATE TABLE eidgah_meta (
    eidgah_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    geom GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography) STORED,
    address TEXT,
    contact TEXT,
    timezone TEXT DEFAULT 'Asia/Kolkata',
    last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ========================================
-- Madrasa
-- ========================================
CREATE TABLE madarsa_meta (
    madarsa_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    geom GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography) STORED,
    classes JSONB,
    address TEXT,
    contact TEXT,
    timezone TEXT DEFAULT 'Asia/Kolkata',
    last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE INDEX idx_madarsa_geom ON madarsa_meta USING gist (geom);

-- ========================================
-- General Audit Table
-- ========================================
CREATE TABLE general_audit (
    id BIGSERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL, -- 'masjid', 'eidgah', 'madarsa'
    entity_id BIGINT NOT NULL,
    field_changed TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type TEXT,
    is_notifiable BOOLEAN DEFAULT false,
    changed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ========================================
-- Notification Queue
-- ========================================
CREATE TABLE notification_queue (
    id BIGSERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id BIGINT NOT NULL,
    change_type TEXT NOT NULL,
    payload JSONB,
    channel TEXT NOT NULL, -- 'push', 'in_app', 'whatsapp'
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    sent_at TIMESTAMP WITHOUT TIME ZONE
);
```

---

---

## **9. Why This Works**

* **Read-optimized**: Hot table contains only prayer-heavy entities.
* **Scalable**: No joins in hot path; PostGIS KNN + partial indexes. Supports high-scale read operations.
* **Clean separation**: Occasional and non-prayer data moved out.
* **Future-proof**: Supports global timezone expansion.
* **Resilient notifications**: Audit + queue separation ensures delivery without blocking writes. Decoupled notification handling.
---
</details>