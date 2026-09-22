# URL Shortener — System Design Study Notes

> A learning build, not a project. The point is to understand the *mechanisms* a
> scalable system uses. Rate limiting, auth, and analytics are their own topics
> for other days — this doc deliberately leaves them out so the core ideas stay
> in focus:
>
> - short-code generation strategies
> - the read path: cache-aside, TTL choices, negative caching
> - cache stampede / thundering herd
> - schema + indexing for an exact-key lookup
> - where the database scaling levers are and when you'd pull them
> - reliability basics: timeouts, fallback, graceful shutdown

---

## 1. Reality check on the numbers

Your instincts are right; a few arithmetic slips to fix.

| Thing | Your number | Corrected | Notes |
|---|---|---|---|
| Total traffic | 100K/day | ✅ | 1 day = 86,400 s (not 100k) |
| Avg read RPS | 1 RPS | ~1.2 RPS | 100K / 86,400 |
| Burst (5x) | 5 RPS | ✅ ~6 RPS | fine as a planning ceiling |
| Read:write | 100:1 | ✅ | so writes ≈ 1K/day, ≈ 0.012/s |
| Writes/day | "10K/day" | **1K/day** | 10K contradicts the 100:1 ratio |
| Storage/month | "30 MB" | ~30 MB *(at 1K/day)*, ~300 MB *(at 10K/day)* | 1 KB/row × writes/day × 30 |

**Takeaway:** one modest server + one Postgres + one Redis handles this workload
thousands of times over. Even at 100x growth (~115 RPS) it's still one box. So the
value here isn't the load — it's learning *where each scaling lever lives and when
it would matter*. Every section below marks that.

---

## 2. What this build covers

**Endpoints:**
- `POST /api/urls` — `{ "url": "https://..." }` → `201 { shortCode, shortUrl, longUrl }`
- `GET /:code` — `302` redirect to the long URL (or `404`)
- `GET /healthz` — process is alive (no I/O)
- `GET /readyz` — can reach Postgres; used by a load balancer to decide routing

**Explicitly out of scope (separate study topics):**
- Rate limiting / load shedding — its own deep topic; here just a `pg` pool cap
  as a natural concurrency bound (§8).
- Authentication — the redirect path is public by nature; the create path would
  just get an API key or JWT, which teaches nothing new about shorteners.
- Click analytics — noted as an aside in §7 so you know why it's *not* a column.

---

## 3. Stack

| Component | Choice | Why |
|---|---|---|
| Language | TypeScript (Node 20+) | types catch wiring mistakes across the moving parts |
| HTTP framework | **Fastify** | ~2–3x Express on JSON; built-in JSON-Schema validation + fast serialization; clean async lifecycle. On-theme for "scalable." |
| Cache / counter | **Redis 7** | `GET/SET` with TTL, `INCRBY`, `SET NX` — all we need |
| Database | **PostgreSQL 16** | reliable, great indexes, replicas are easy later |
| DB driver | `pg` with a small query layer (or Kysely/Drizzle) | no heavy ORM on the hot path |
| Local infra | `docker-compose` (postgres + redis) | |
| Load test | `autocannon` (quick) or `k6` (scenarios) | to actually observe cache hit rate, p99, pool saturation |

Express instead of Fastify is fine if it's more familiar — you'd add `zod` for
validation and accept lower throughput. Nothing else in the design changes.

---

## 4. Architecture

```
                 ┌───────────────────────────────────────────┐
   client ──────▶│  Load balancer (nginx / HAProxy)          │
                 │  - TLS termination                        │
                 │  - routes on /readyz                      │
                 └──────────────┬───────────────────────────┘
                                │  (app nodes are stateless — no sticky sessions)
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        ┌──────────┐      ┌──────────┐      ┌──────────┐
        │ app 1    │      │ app 2    │ ...  │ app N    │   Fastify
        └────┬─────┘      └────┬─────┘      └────┬─────┘
             │                 │                 │
      ┌──────┴─────────────────┴─────────────────┴──────┐
      ▼                                                 ▼
 ┌──────────────┐                          ┌──────────────────────┐
 │ Redis        │                          │ Postgres primary     │
 │ - code cache │                          │  └─ read replica(s)   │
 │ - neg cache  │                          │     [only if needed]  │
 │ - INCRBY ctr │                          └──────────────────────┘
 └──────────────┘
```

- **App nodes hold no state.** Horizontal scaling = add a node to the LB. Any
  coordination state (the counter) lives in Redis, never in one process's memory.
- **Why "add a node behind an LB" scales linearly here:** every request is
  independent, there's no shared in-process state, so throughput grows with node
  count until a downstream (Redis or Postgres) becomes the bottleneck.

---

## 5. Short-code generation

Goal: unique, short (~7 chars base62 → 62⁷ ≈ 3.5 trillion), O(1) on write, no
collision round-trip to the DB, correct with N app nodes running at once.

### Option A — random + `ON CONFLICT` (simplest; start here)

```sql
INSERT INTO urls (short_code, long_url)
VALUES ($1, $2)
ON CONFLICT (short_code) DO NOTHING
RETURNING short_code;
```

Generate 7 random base62 chars. No row returned ⇒ collision ⇒ regenerate, retry.
In a 3.5-trillion space with millions of rows, expected retries ≈ 0. Collisions
only get real near *billions* of rows (birthday bound). Zero infrastructure.

### Option B — counter + base62 with per-node ranges (the "proper" scalable one)

1. Global counter in Redis.
2. Each app node claims a block: `INCRBY shortener:counter 1000` → say it returns
   `45000`; the node now owns IDs `44001–45000` in local memory and hands them
   out with **zero network calls**. Exhausts the block ⇒ grab the next one.
3. `short_code = base62(id)`.
4. Insert. Uniqueness is guaranteed by the counter — **no collision check at all**.

- **Crash behavior:** a dying node wastes ≤ ~1000 unused IDs. Nothing to monitor,
  no pool to refill, no generator service.
- **Downside:** codes are sequential ⇒ enumerable (`/aaaab` follows `/aaaaa`). If
  that matters, run the integer through a keyed bijective scramble (a small
  **Feistel network** / `skip32`) before base62 — still 1:1, still collision-free,
  output looks random.

### Option C — your pre-generation pool (KGS)

A separate service fills a store of random codes; app nodes claim one per write.
Valid and a common interview answer. To be safe:
- The pool is in **Redis or Postgres, never app memory.** `SPOP pool` (atomic
  across N nodes) or `DELETE ... WHERE code = (SELECT ... FOR UPDATE SKIP LOCKED) RETURNING code`.
- A top-up worker refills when `SCARD pool` drops below a threshold.
- A crash loses only the code a single in-flight request had claimed — not the
  whole pool — because claiming is per-request, not batched into process memory.
- The pool's one real advantage over Option B: codes are random (not
  enumerable). Its cost: an extra service + pool-size monitoring.

**Recommendation:** build **A** first (it's ~10 lines), then swap in **B** to feel
the difference — B is the version that removes the DB from the write's
uniqueness concern entirely. C is worth understanding but is the most moving
parts for the least gain here.

---

## 6. Data model

```sql
CREATE TABLE urls (
    id          BIGINT      PRIMARY KEY,        -- from the counter (Option B); omit for Option A
    short_code  TEXT        NOT NULL UNIQUE,    -- the lookup key
    long_url    TEXT        NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

- The lookup is always `WHERE short_code = $1`. The `UNIQUE` constraint **already
  builds the B-tree index** that lookup uses — you don't add a separate index.
  (This is the "index on shortcode" from your plan; it comes free with the
  constraint.)
- **No `click_count` column.** Incrementing a row on every redirect turns your
  read-heavy hot path into a write on every request and creates lock contention
  on popular links. If you ever want counts: `INCR clicks:{code}` in Redis and a
  worker flushes them to a separate table. That's the analytics aside — it stays
  *out* of this table.
- Partition by `created_at` only at hundreds of millions of rows, and that's a
  VACUUM/maintenance fix, not a throughput one.

---

## 7. Read path (redirect) — the hot path

```
GET /:code
  ├─ cheap shape check on {code} (charset, length) — reject junk before any I/O
  ├─ Redis GET url:{code}
  │     ├─ value is a URL   → 302 Location: <url>
  │     ├─ value is "\0"    → 404  (negative cache hit)
  │     └─ miss → single-flight (see §8):
  │              ├─ SELECT long_url FROM urls WHERE short_code = $1
  │              │     ├─ found     → SET url:{code} <url> EX 86400 ; 302
  │              │     └─ not found → SET url:{code} "\0"  EX 60    ; 404
  │              └─ the SET is fire-and-forget — don't block the response on it
  └─ Redis unreachable → skip cache, read Postgres directly, still serve
```

### Corrections to your caching plan

1. **TTL is not 300 s.** `short_code → long_url` is **immutable** once created.
   Cache it long (24 h, or no TTL with `maxmemory` + `allkeys-lru` eviction). A
   5-minute TTL just forces pointless DB reads. You'd only `DEL url:{code}` if you
   later add link deletion/editing.
2. **Negative caching.** Cache "not found" as a sentinel for 30–60 s. Bots *will*
   scan random codes; without this, each bogus code is a DB query on every hit.
3. **Redis eviction:** `maxmemory` + `allkeys-lru` so it behaves as a cache, not a
   store that OOMs.
4. **Redis is an optimization, not a dependency.** Short timeout (~50 ms) +
   try/catch on every call. Redis down ⇒ serve from Postgres, don't 500.
   Optionally a tiny circuit breaker so you stop hammering a dead Redis.
5. **The whole dataset fits in RAM.** 100K codes × ~250 B ≈ 25 MB, so steady-state
   hit rate ≈ 100%. Even 100M codes ≈ 25 GB fits one large Redis. **Caching — not
   read replicas — is the primary read-scaling mechanism for this system.**

### 301 vs 302

`301` lets browsers/proxies/CDNs cache the redirect, so many clicks never reach
your server — but you then lose all analytics and can never disable or change a
link. `302` (or `307`) sends every click through your server: full control, more
load (still trivial at ~6 RPS). **Use 302.** Revisit `301 + CDN` only if redirect
load ever genuinely becomes a problem.

---

## 8. Thundering herd / cache stampede

A link goes viral while its cache entry is cold (or a bot fires 1,000 concurrent
requests for the same missing code) → 1,000 identical DB queries at once.

Apply the first two; understand the rest:

1. **In-process single-flight (first line).** Per process, keep
   `Map<code, Promise<Result>>`. The first request for a cold code creates the
   promise and does the DB read; the other requests on that node `await` the
   *same* promise. Delete the entry when it settles. ~20 lines, and it kills most
   of a herd because a herd usually lands on one node.
2. **Cross-node lock (next level).** Before the DB read: `SET lock:{code} 1 NX PX 3000`.
   Winner reads DB + fills cache; losers sleep ~20–50 ms and re-check the cache
   (now warm). Bounds concurrent DB hits for one key to ~1 across the whole fleet.
3. **Negative caching** (§7.2) — handles the "everyone requests a *nonexistent*
   key" variant.
4. **Long TTL on immutable data** — entries almost never expire, so cold misses
   are rare by construction. (Probabilistic early expiration / stale-while-
   revalidate matter when values *change* — mostly moot here.)
5. **The `pg` pool size is a concurrency bound.** A pool of 20 per node means at
   most 20 concurrent DB ops no matter the inbound rate; the rest queue or time
   out (→ 503). This is the "queue / shed load rather than fall over" idea in its
   simplest form — set the number deliberately.

---

## 9. Reliability basics

- **Timeouts on everything:** Redis ~50 ms, Postgres query ~1–2 s. No unbounded
  waits.
- **Graceful degradation:** Redis down → direct Postgres reads. Postgres down →
  cached codes still redirect; uncached reads and all writes return `503` with
  `Retry-After`.
- **Graceful shutdown (SIGTERM):** stop accepting new connections, finish
  in-flight requests, close the `pg` pool and Redis client, exit. The LB stops
  routing once `/readyz` fails.
- **Liveness vs readiness:** `/healthz` = process up, touches nothing. `/readyz` =
  can reach Postgres. The LB routes on readiness.
- **Input check on create:** URL parses, scheme is `http`/`https`, length ≤ 2048,
  host isn't `localhost` / a private IP / your own shortener domain (stops
  redirect loops).

---

## 10. Database scaling — the levers, in order

Your original list had the right endpoints; the middle needs fixing. Postgres
doesn't scale horizontally by just adding nodes, and vertical *partitioning*
(splitting columns) does nothing for a 4-column table.

**App tier:** add nodes behind the LB — linear until a downstream is the
bottleneck.

**Database tier, pulled in this order:**
1. **Vertical scaling** — a bigger Postgres box. Cheapest thing that works;
   carries this workload absurdly far.
2. **Connection pooling (PgBouncer, transaction mode)** — needed once several app
   nodes exist, or N × pool-size connections exhaust Postgres. Big win, low
   effort.
3. **Caching** — already in the design (§7). This is what actually absorbs the
   reads. Push hit rate toward ~100%.
4. **Read replicas** — route cache-miss reads (and any analytics queries) to
   replicas. Accept replication lag: a just-created code might 404 on a replica
   for a few ms — read the primary for very fresh codes, or tolerate it.
5. **Range partitioning by `created_at`** — only at hundreds of millions of rows,
   when VACUUM / index maintenance hurts. An ops fix, not a throughput fix.
6. **Sharding by `hash(short_code)`** — only when one primary can't take the write
   rate or the data won't fit one box. At 1K writes/day you never get here. Worth
   knowing the shape: consistent hashing on the shard key, a routing layer, and
   no cross-shard queries because every lookup is by exact code.

**Redis:** one node → add a replica for HA → Redis Cluster (hash-slot sharding)
only past tens of GB or when one node's throughput saturates.

---

## 11. Suggested build order

Not phases of a product — just a sensible sequence to build and poke at:

1. `docker-compose` with postgres + redis. Fastify app with `/healthz` +
   `/readyz`. Config from env vars.
2. Migration for the `urls` table.
3. `POST /api/urls` using **Option A** (random code + `ON CONFLICT` retry) and
   JSON-Schema validation on the body.
4. `GET /:code` with cache-aside: Redis lookup → miss → Postgres → warm cache →
   302. Add negative caching. Long TTL.
5. Swap code generation to **Option B** (Redis counter + per-node range). Feel
   how the write no longer depends on the DB for uniqueness. Optionally add the
   Feistel scramble.
6. Add **in-process single-flight** on cache miss. Then the cross-node
   `SET NX` lock as a second layer.
7. Add Redis-down fallback, timeouts, graceful shutdown.
8. Load-test with `autocannon` / `k6`. Watch: cache hit ratio, p50/p95/p99,
   `pg` pool saturation under 6 RPS and under a 50x burst. Run two app nodes
   behind local nginx. Add a read replica in compose and route cache-miss reads
   to it. Write down the sharding design without building it.

---

## 12. What changed from your original plan

1. Fixed the traffic/storage math; made explicit the load is tiny and this is a
   mechanisms study.
2. Recommend **counter + per-node range** over the random pre-gen pool (fewer
   moving parts, nothing to monitor). Random + `ON CONFLICT` to start. Pool (KGS)
   documented as a third option, with the fix that it must live in Redis/PG and be
   claimed per-request.
3. Cache TTL: **long / immutable**, not 300 s. Added **negative caching** and
   `allkeys-lru`. Redis failure is **non-fatal** — fall back to Postgres.
4. Thundering herd: **in-process single-flight first**, then cross-node `SET NX`
   lock, plus negative cache. The `pg` pool cap is your queueing/load-shedding
   bound. Concrete recipes in §8.
5. Redirects use **302**, not 301 — otherwise clients cache the redirect and you
   lose all control over the link.
6. **No per-redirect `UPDATE`** for click counts — that's what would break the
   read-heavy advantage. Analytics, if ever, go through Redis `INCR` + a flush
   worker into a separate table.
7. DB scaling order corrected: vertical → PgBouncer → cache → read replicas →
   time-range partitioning → (theoretical) sharding. Dropped "vertical
   partitioning" — meaningless for this table.
8. Stack: **Fastify + TypeScript**, using its schema validation + fast
   serialization.
9. Left auth and rate limiting out entirely — they're separate topics and add no
   shortener-specific insight.

**Verdict:** the plan is sound and the instincts are right (KGS, cache-aside,
stampede awareness, staged DB scaling). The above are refinements. Good design to
build and experiment on.
