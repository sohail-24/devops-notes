# THE FRAGRANCE STORE — MASTER PROJECT HANDOVER
## Cloudflare Migration & R2 Image Storage
**Last updated:** November 4, 2026  
**Project:** The Fragrance Store — House of Brands  
**Current tenant:** INHALE FRAGRANCES (Website-A)  
**Tenant slug:** `the-fragrance-store`  
**Status:** R2 image migration successfully completed; production image-serving integration is the next major task.

---

# 1. Project overview

The Fragrance Store is a multi-tenant SaaS e-commerce platform designed to support multiple fragrance brands and their independent storefronts.

The current focus is Website A:

- Brand: INHALE FRAGRANCES
- Tenant slug: `the-fragrance-store`
- Production application: `https://fragrance.sohaildevops.site`
- Storefront: `/store/the-fragrance-store`
- Admin and Super Master functionality are part of the existing application.

The long-term infrastructure goal is to migrate away from Netlify and use Cloudflare infrastructure.

**Important:** The migration is staged. Netlify must remain available as a rollback option until the Cloudflare application is deployed, tested, and verified in production.

## Existing technology stack

| Layer | Technology |
|---|---|
| Frontend | React 19 |
| Build tool | Vite 7 |
| Language | TypeScript |
| Styling | Tailwind CSS 3.4 |
| UI | Shadcn / Radix UI |
| Backend | Hono v4 |
| API | tRPC v11 |
| Routing | React Router v7 |
| ORM | Drizzle ORM |
| Database | Neon PostgreSQL |
| Existing hosting | Netlify |
| Target hosting | Cloudflare Workers |
| Object storage | Cloudflare R2 |
| DNS / CDN | Cloudflare |
| Deployment repository | GitHub |

---

# 2. Important infrastructure architecture decisions

Our target architecture is:

| Component | Responsibility |
|---|---|
| Cloudflare Workers | Application and API runtime |
| Cloudflare R2 | Product images and user-uploaded media |
| Cloudflare DNS | Domain management |
| Cloudflare CDN / WAF | Delivery and protection |
| Neon PostgreSQL | Relational application data |
| GitHub | Source code and version control |

### Important decisions

1. Neon PostgreSQL remains our relational database.
2. R2 is object storage, not a replacement database.
3. We will not replace Neon with Cloudflare D1.
4. Each tenant's database isolation must remain intact.
5. Uploaded product images should eventually be served from R2.
6. Static Git repository assets can remain static.
7. Netlify must not be removed until Cloudflare production is verified.
8. Existing Neon image data must not be deleted during the initial R2 rollout.

### Multi-tenant database isolation

The platform has a central control-plane database and separate tenant databases.

Website A's authoritative database is its own Neon database.

Do not accidentally use the central database as Website A's catalog or image database.

Canonical tenant information:

```text
Tenant slug:
the-fragrance-store

Tenant UUID:
00000000-0000-4000-8000-000000000001
```

---

# 3. Cloudflare R2 setup

We created two R2 buckets.

| Bucket | Purpose | Current status |
|---|---|---|
| `fragrance-saas-media` | Production media | Active |
| `fragrance-saas-media-preview` | Preview/testing | Created |

Both buckets were configured as private buckets with automatic location selection in Asia Pacific and Standard storage class.

### R2 usage and billing

The Cloudflare dashboard initially displayed the included monthly allowance:

- 10 GB storage
- 1 million Class A operations
- 10 million Class B operations

Usage beyond the included allowance can be charged.

We activated the R2 subscription. The dashboard initially showed $0 monthly base cost.

Do not assume that all future usage is unlimited or free. Monitor billing and usage.

### Production R2 connectivity test

We created:

```text
scripts/test-r2-connectivity.ts
```

Package command:

```bash
npm run test:r2-connectivity
```

The test performs:

1. Connect to R2 using the S3-compatible API.
2. Upload a temporary validation file.
3. Read the file back.
4. Verify SHA-256 and content length.
5. Delete the exact temporary test object.

The test passed twice.

Most recent result:

```text
[r2:test] SUCCESS:
R2 connectivity round-trip verified successfully.

Bucket: fragrance-saas-media

Verified Key:
validation/the-fragrance-store/r2-connectivity-test.txt

Bytes: 118

Test object cleaned up.
```

This confirms that the Mac terminal successfully connected to the production R2 bucket.

---

# 4. R2 credentials and environment variables

The migration tools use these environment variables:

```bash
R2_ACCOUNT_ID
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET_NAME
```

Production bucket:

```bash
R2_BUCKET_NAME="fragrance-saas-media"
```

Website A database connection:

```bash
WEBSITE_A_DATABASE_URL
```

Credentials were entered securely through the Mac terminal.

Example secure input:

```bash
read -s "R2_ACCESS_KEY_ID?Enter R2 Access Key ID: "
echo
export R2_ACCESS_KEY_ID

read -s "R2_SECRET_ACCESS_KEY?Enter R2 Secret Access Key: "
echo
export R2_SECRET_ACCESS_KEY

read -s "WEBSITE_A_DATABASE_URL?Enter Website A database URL: "
echo
export WEBSITE_A_DATABASE_URL
```

The actual secret values must never be pasted into ChatGPT, GitHub, source code, or ordinary prompts.

If the terminal session is reset, enter the credentials again securely.

---

# 5. R2 database schema foundation

We extended the existing `product_images` table.

Original columns included:

```text
id
productId
filename
mimeType
data
size
createdAt
updatedAt
```

We added these R2 metadata columns:

```text
storageProvider varchar(20)
r2Key varchar(500)
r2Etag varchar(100)
checksumSha256 varchar(64)
migratedAt timestamp
```

We also created:

```text
product_images_r2_key_idx
```

Migration file:

```text
db/migrations/0008_r2_storage_foundation.sql
```

Migration journal:

```text
db/migrations/meta/_journal.json
```

The migration was recorded in:

```text
drizzle.__drizzle_migrations
```

### Important migration history

The Website A Neon database already had migration history 0000–0007.

We compared the existing migration hashes and confirmed they matched the local migration files.

Migration 0008 was then applied manually through the Neon SQL Editor and recorded in the migration history.

The migration did not remove or modify existing image data.

### Database verification

After migration 0008:

```text
total_images: 29
postgres_images: 29
images_with_data: 29

total_image_bytes: 42492019
```

All 29 original image records remained intact.

---

# 6. R2 image storage service

Created:

```text
api/services/r2StorageService.ts
```

The service provides:

- Image upload
- Image retrieval
- Object existence checks
- Object metadata retrieval
- SHA-256 calculation
- Controlled object deletion
- In-memory R2 implementation for automated tests

Deletion requires an explicit authorization option:

```text
{ authorized: true }
```

This protects against accidental object deletion.

### Error handling improvements

We added:

```text
isR2ObjectNotFoundError(err)
mapR2ClientError(operation, key, err)
```

Important behavior:

- A confirmed missing R2 object can return `null`.
- Authentication failures must throw.
- Permission errors must throw.
- Network failures must throw.
- Rate-limit errors must throw.
- NoSuchBucket must throw.
- Server errors must throw.

This prevents the application from treating a real R2 outage as if an image simply does not exist.

---

# 7. Image migration script

Created:

```text
scripts/migrate-images-to-r2.ts
```

Package commands:

```bash
npm run image:migrate:dry-run
```

Dry-run command:

```bash
npm run image:migrate
```

Actual execution requires an explicit approval flag:

```bash
npm run image:migrate -- --confirm-execution
```

### Migration safety mechanisms

The script includes:

1. Canonical tenant validation.
2. Website A database URL verification.
3. Control-plane database URL comparison.
4. SHA-256 verification.
5. Content-length verification.
6. Existing-object detection.
7. Idempotent behavior.
8. Controlled batch processing.
9. Error reporting.
10. Preservation of PostgreSQL image data.

The migration processes images in batches, with a default batch size of 10.

### Important storage status values

| Value | Meaning |
|---|---|
| `postgres` | Image exists in PostgreSQL; not yet migrated |
| `dual` | Verified R2 copy exists; PostgreSQL copy remains |
| `r2` | Reserved for a later cutover stage |

We intentionally chose `dual` for this first migration.

We must not switch records to `r2` until production image serving has been integrated and tested.

---

# 8. Work completed November 3–4, 2026

## November 3 — R2 infrastructure and preparation

Completed:

- Activated Cloudflare R2.
- Created production and preview buckets.
- Inspected the existing application architecture.
- Reviewed existing PostgreSQL image storage.
- Designed tenant-specific R2 object keys.
- Implemented R2 storage service.
- Created migration script.
- Created dry-run mode.
- Added SHA-256 verification.
- Added R2 connectivity test.
- Added migration safeguards.
- Verified the Website A database target.
- Preserved the existing Neon image records.

## November 4 — Database, tests and actual migration

### A. Neon schema correction

The first image dry-run failed because the production Neon database did not yet contain the new R2 metadata columns.

We inspected the database and found:

- Migration history 0000–0007 already matched.
- Migration 0008 was missing from the actual table schema.
- Existing image data was present and healthy.

We safely applied migration 0008.

### B. Database verification

After applying migration 0008:

```text
Total images: 29
Images with data: 29
Original image bytes: 42,492,019
```

### C. Dry-run verification

Executed:

```bash
npm run image:migrate:dry-run
```

Result:

```text
Mode: DRY-RUN (Zero writes)

Total records evaluated: 29
Missing / pending migration: 29
Existing already verified in R2: 0
Newly migrated: 0
Checksum mismatches: 0
Failed records: 0
Total bytes uploaded: 0

Finished. Status: SUCCESS
```

This proved that the script could read and evaluate all 29 images without modifying anything.

### D. R2 connectivity verification

Executed:

```bash
npm run test:r2-connectivity
```

Result:

```text
SUCCESS

Bucket: fragrance-saas-media
Bytes: 118
SHA-256 verified
Test object cleaned up
```

### E. Actual migration

Initially, the normal command:

```bash
npm run image:migrate
```

still ran in dry-run mode.

We inspected the script and found that it requires explicit execution approval.

Relevant script behavior:

```text
--confirm-execution
--approve
-y
```

The correct execution command was:

```bash
npm run image:migrate -- --confirm-execution
```

We executed it successfully.

Final output:

```text
[image:migrate] Target:
Website A Neon database
Tenant: the-fragrance-store

[image:migrate] Mode: CONFIRMED EXECUTION

[image:migrate] Total records evaluated:
29 (42,492,019 bytes)

[image:migrate] Missing / pending migration:
0 (0 bytes)

[image:migrate] Existing already verified in R2:
0 (0 bytes)

[image:migrate] Newly migrated: 29

[image:migrate] Checksum mismatches: 0

[image:migrate] Failed records: 0

[image:migrate] Total bytes uploaded:
42,492,019 bytes

[image:migrate] Finished. Status: SUCCESS
```

**This was the first successful actual migration of all 29 Website A images to production R2.**

---

# 9. Independent verification after migration

We checked both Cloudflare and Neon.

## Cloudflare R2 dashboard

The production bucket displayed:

```text
Bucket: fragrance-saas-media

Objects: 29

Size: 42.5 MB
```

The preview bucket displayed:

```text
Objects: 0
Size: 0 B
```

Cloudflare usage panel displayed:

```text
Class A Operations: 264
Class B Operations: 165
Total storage: 42.5 MB
Billable usage: $0.00
```

These figures are from the November 4 dashboard screenshot and can change as usage continues.

## Neon SQL verification

We executed this read-only query:

```sql
SELECT
    "storageProvider",
    COUNT(*) AS image_count,
    COUNT(*) FILTER (
        WHERE data IS NOT NULL
    ) AS images_with_original_data,
    COUNT(*) FILTER (
        WHERE "r2Key" IS NOT NULL
    ) AS images_with_r2_key,
    COUNT(*) FILTER (
        WHERE "checksumSha256" IS NOT NULL
    ) AS images_with_checksum,
    SUM(octet_length(data)) AS original_bytes_preserved
FROM public.product_images
GROUP BY "storageProvider";
```

The screenshot showed:

| storageProvider | image_count | original data | R2 key | checksum |
|---|---:|---:|---:|---:|
| dual | 29 | 29 | 29 | 29 |

This confirms:

- All 29 records are marked `dual`.
- All 29 original PostgreSQL image data fields are still populated.
- All 29 records have an R2 object key.
- All 29 records have a SHA-256 checksum.

The screenshot did not expose the final `original_bytes_preserved` result column, so that exact aggregate was not independently visible in the screenshot.

### Final migration conclusion

**R2 image migration: SUCCESSFUL.**

All 29 image objects are present in the production R2 bucket, and all 29 Neon image records retain their original data.

Do not delete PostgreSQL image data.

---

# 10. GitHub and local development status

Repository:

```text
sohail-24/saas-fragrance-store
```

Local Mac project directory:

```text
/Users/sohal/Downloads/saas-fragrance-store
```

Current branch:

```text
main
```

### Package-lock issue solved

During earlier work, Google AI Studio accidentally removed `package-lock.json`.

We restored it and committed it to GitHub.

Commit:

```text
5ae9a52
chore: restore npm package lockfile
```

The user pushed it successfully.

We verified:

```bash
git status
```

Output:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Then:

```bash
npm ci
```

Result:

```text
added 535 packages
```

### Dependency audit

The installation reported:

```text
18 vulnerabilities
16 moderate
2 high
```

Do not blindly execute:

```bash
npm audit fix
npm audit fix --force
```

Review vulnerabilities separately and avoid breaking dependency upgrades during infrastructure migration.

### Important Google AI Studio instruction

Whenever requesting code changes, explicitly instruct AI Studio:

- Preserve `package-lock.json`.
- Do not delete or regenerate lockfiles unnecessarily.
- Use npm as the package manager.
- Preserve existing tenant isolation.
- Do not modify unrelated features.
- Do not remove Netlify yet.
- Do not delete PostgreSQL image data.
- Do not switch storage status from `dual` to `r2` prematurely.

---

# 11. Important outstanding technical issues

The R2 image migration is complete, but the application has not yet been fully switched to serve images from R2.

Earlier architecture inspection identified these issues:

### A. Production image-serving route

File:

```text
api/app.ts
```

Existing route:

```text
/api/uploads/:filename
```

At the time of inspection, this route still used PostgreSQL image lookup.

A helper was added:

```text
resolveProductImageWithR2Fallback
```

in:

```text
api/queries/productImages.ts
```

However, this helper was not yet integrated into the production route because the Netlify runtime did not have a Cloudflare R2 environment binding.

This must be reviewed before integration.

### B. Cloudflare Worker entrypoint

The earlier Wrangler configuration referenced:

```text
api/worker.ts
```

But this entrypoint did not exist at the time of the architecture audit.

It must be implemented and tested as part of the Cloudflare Workers migration.

### C. Vite asset output mismatch

Vite production build output:

```text
dist/public
```

Earlier Wrangler assets configuration:

```text
./dist
```

This mismatch must be corrected during Worker deployment.

We must ensure that internal build files such as `dist/boot.js` are not unintentionally exposed as public assets.

### D. Node.js compatibility

The current application uses Node-oriented APIs and database connections.

Areas requiring review:

- `node:fs`
- `pg.Pool`
- Netlify serverless adapters
- Cloudflare Workers runtime
- Neon serverless database connectivity
- SMTP/email integration

Do not assume Node APIs will work identically inside Cloudflare Workers.

### E. Dynamic tenant database connections

This platform uses physically separate tenant databases.

A single static Hyperdrive binding should not be assumed to support dynamically selected arbitrary tenant database URLs.

The implementation must preserve tenant isolation and securely resolve each tenant's own database connection.

Neon serverless connectivity may be needed depending on the final Worker architecture.

---

# 12. Next development phases

## Phase 4 — R2 production image-serving integration

**This should be our next task.**

Objective: Make the application retrieve images from R2 while keeping Neon as a fallback.

Required work:

1. Inspect the existing R2 service.
2. Inspect the production `/api/uploads/:filename` route.
3. Inspect the existing `resolveProductImageWithR2Fallback` helper.
4. Integrate R2 access using the correct runtime environment binding.
5. Preserve tenant-specific object key validation.
6. Verify that R2 errors are not mistaken for missing objects.
7. Keep PostgreSQL fallback working.
8. Ensure the image-serving route returns the correct MIME type.
9. Test actual product images from the storefront.
10. Verify Inventory image uploads and image retrieval.

Initial behavior should be:

```text
Request image
      |
      v
Resolve correct tenant image record
      |
      v
Check storageProvider
      |
      v
Try R2 for verified dual records
      |
      +---- R2 success ----> Return image
      |
      +---- Confirmed missing object
      |             |
      |             v
      |       PostgreSQL fallback
      |
      +---- Authentication/network error
                    |
                    v
              Report real error
```

Important: Do not silently treat authentication or network failures as missing images.

### Phase 4 testing requirements

Test:

- Existing product images.
- Product images from Inventory.
- Brand images.
- Unlinked images.
- Missing R2 object.
- R2 access failure.
- Database lookup failure.
- Wrong tenant access.
- Correct MIME types.
- Mobile storefront images.
- Admin product image previews.

Keep all image records marked `dual` during the initial rollout.

## Phase 5 — Cloudflare Workers migration

Objective: Move the application from Netlify to Cloudflare Workers.

Tasks:

1. Create the Worker entrypoint.
2. Integrate Hono with the Worker environment.
3. Configure R2 binding.
4. Configure Neon connectivity.
5. Fix Vite asset output configuration.
6. Replace Netlify-specific runtime dependencies.
7. Configure secure environment variables and secrets.
8. Test API routes.
9. Test authentication.
10. Test tenant isolation.
11. Test storefront routes.
12. Test image serving.
13. Deploy to a Cloudflare preview environment.
14. Perform production validation.

Do not remove the Netlify deployment.

## Phase 6 — Custom domain and production cutover

Target:

- Cloudflare Workers production deployment.
- Cloudflare DNS.
- Custom tenant domains.
- HTTPS.
- CDN and security.
- R2 image delivery.

Only switch production traffic after successful end-to-end testing.

## Phase 7 — Long-term image storage cleanup

Not approved yet.

Only after a stable production period, verified backups, and an explicit review should we consider changing records from `dual` to `r2` or deleting PostgreSQL image bytes.

Do not perform this cleanup automatically.

---

# 13. Rules for future AI Studio prompts

Use these rules whenever asking Google AI Studio to modify the project.

1. First inspect only the files relevant to the current task.
2. Diagnose the root cause before implementation.
3. Make narrowly scoped changes.
4. Preserve working functionality.
5. Do not modify unrelated UI or backend modules.
6. Preserve the physical tenant database isolation.
7. Never add a fallback to the central database for Website A.
8. Preserve `package-lock.json`.
9. Avoid unnecessary dependency installations.
10. Avoid broad automated refactors.
11. Do not run repeated expensive commands unnecessarily.
12. Report every changed file.
13. Report tests executed and actual results.
14. Clearly state whether live Neon or R2 was accessed.
15. Never claim a live test passed if only mocks were used.
16. Do not delete PostgreSQL image data.
17. Do not change `dual` to `r2` before explicit approval.
18. Keep Netlify available until Cloudflare is fully validated.

---

# 14. Useful commands

### Git

```bash
git status
git pull origin main
git log -5 --oneline
```

### Dependencies

```bash
npm ci
```

### TypeScript check

```bash
npm run check
```

### R2 connectivity

```bash
npm run test:r2-connectivity
```

### Image migration dry-run

```bash
npm run image:migrate:dry-run
```

### Actual migration

```bash
npm run image:migrate -- --confirm-execution
```

**Do not run the actual migration again unless a new migration is deliberately planned. All 29 existing images have already been migrated.**

---

# 15. Current project status — November 4, 2026

| Component | Current status |
|---|---|
| Website A Neon DB | Working |
| Migration 0008 | Applied |
| Original image records | 29 preserved |
| Original image data | 29 records populated |
| Cloudflare production bucket | Created |
| Cloudflare preview bucket | Created |
| R2 connectivity | Passed |
| Image migration dry-run | Passed |
| Actual R2 migration | Completed |
| R2 objects | 29 |
| R2 storage | 42.5 MB |
| Neon storage metadata | All 29 marked `dual` |
| R2 keys | 29 |
| SHA-256 metadata | 29 |
| Migration failures | 0 |
| Checksum mismatches | 0 |
| Git package-lock | Restored and committed |
| Local npm installation | Successful |
| Netlify | Retained |
| Cloudflare Workers production migration | Not completed |
| Production R2 image-serving integration | Not completed |

---

# 16. How to continue in the next ChatGPT conversation

Paste this message together with the handover:

"Mentor, continue The Fragrance Store Cloudflare migration using this project handover.

We have successfully migrated all 29 Website A images to Cloudflare R2. The production bucket contains 29 objects (42.5 MB), and Neon confirms all 29 image records are marked `dual`, with original PostgreSQL image data preserved.

Do not repeat the completed migration. Do not delete Neon image data. Do not remove Netlify.

Our next task is Phase 4: integrate production R2 image serving into the existing application, with PostgreSQL fallback and tenant isolation.

Guide me step by step. First inspect the relevant existing code and identify the exact root cause and implementation plan. Then give me a carefully scoped Google AI Studio Task prompt."

---

**Final mentor note:**

We have completed a major infrastructure milestone.

We moved 29 existing Website A images from PostgreSQL storage into Cloudflare R2 without removing the original database copies.

The next challenge is not uploading images anymore. It is making the application reliably serve those R2 images in production while preserving tenant isolation and PostgreSQL fallback.

One phase at a time. No unnecessary refactoring, no risky deletions, and no premature production cutover.
