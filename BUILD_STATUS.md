# BUILD STATUS — Origin Talent Website
Prepared by: Claude Code, 3 August 2026, in response to `CLAUDE_CODE_HANDOFF.md` from the claude.ai side (Fate Collab project).

This closes the loop the handoff asked for: what actually exists in the `Origin-Talent` GitHub repo, how it compares to Design A / Design B, and what's still open.

---

## Design direction: it's Design B, and it's gone further than either doc describes

The repo is **not** the multi-page Phase 1 build in the handoff zip's `site-build-origin-talent/` (Design A: separate `index.html` / `client.html` / `candidate.html` / `privacy.html` / `downloads.html`).

It's a **single self-contained `index.html`** built on the Design B direction — hero copy is verbatim "Exceptional People. Trusted in Your Home." / "Peace of Mind, Every Day." (`index.html:519-520`), matching `brand-assets/design-B-homepage-reference.png`. All sections (hero, services, client enquiry form, candidate application form, about, document centre/resources, contact, footer) live on one page as anchor-linked sections (`#employers`, `#job-seekers`, `#about`, `#resources`, `#contact`), not separate pages.

Beyond the homepage, this build also has working, submitting forms and a real backend — which neither Design A nor Design B (as described in the handoff) had yet.

## Stack

- **Frontend:** static HTML/CSS/JS, no build step, no framework. Single file (`index.html`, 1046 lines) with inlined CSS and the logo. Two `<script type="application/ld+json">` blocks (EmploymentAgency + LocalBusiness schema).
- **Forms backend:** Supabase (`supabase-js` via CDN) — `client_enquiries` and `candidate_applications` tables, insert-only RLS for anon visitors, with server-side validation of required fields/POPIA checkbox/length caps (`supabase/002_tighten_rls.sql`). Legacy Google Apps Script backend (`apps-script/*.gs`) is kept for reference/rollback but the live page does not call it.
- **Staff dashboard:** `dashboard.html`, self-contained, Supabase Auth–gated (`staff` table), pipeline stage tracking, ageing indicators, notes, admin-only POPIA erasure delete. Not linked from the public site; `noindex, nofollow`.
- **Quick contact form:** no backend — opens WhatsApp pre-filled (no spreadsheet/table).
- **Hosting:** none configured yet — no `vercel.json`/`netlify.toml` in the repo, no deploy history found. **There is no live/preview URL right now.**

## Pages that exist

| Page | Status |
|---|---|
| `index.html` | Live-ready static file. One `<title>` + one meta description — good, since it's a single page (no multi-page meta-description gap; that gap only applied to the old Design A multi-page structure). |
| `dashboard.html` | Internal only, not linked publicly, not for launch/SEO. |
| `/privacy-policy` | **Referenced in the footer (`index.html:913`) but does not exist as a file.** Design A's `privacy.html` was never ported over — this is a dead link right now. |
| Document Centre PDFs | `index.html`'s Document Centre section links to 3 PDFs under `documents/` that **don't exist in this repo**. The handoff zip's `documents/` folder *does* contain real branded PDF+DOCX versions of all three (Client Staffing Enquiry Form, Candidate Application Form, Client Service Agreement) — not yet copied in. |

## Release-gate check (from the handoff, Section on release gates)

1. ❌ Forms are still demo-labelled in markup (`data-demo="client"` / `data-demo="candidate"`, `index.html:596,678`) but **are** wired to a real Supabase backend, not just demo-capture — the `data-demo` attribute name is stale/misleading, worth a rename pass.
2. ❌ No candidate ID/CV/photo upload field exists yet on the form at all (checked — no `<input type="file">` present anywhere), so the "never a plain public file input" gate hasn't been tested either way. Still open.
3. ❌ Client Service Agreement — legal review status unknown from this repo; the branded PDF/DOCX exist in the handoff zip's `documents/`, not yet reviewed or linked.
4. ❌ Privacy notice — doesn't exist yet in this repo (see above); no Information Officer name/retention periods to check.
5. ❓ Company registration number / final fee schedule — not present anywhere in `index.html`; can't confirm placeholder vs. finalised without Roger's sign-off.

## What's NOT in this repo (so it doesn't look done when it isn't)

- No `/privacy-policy` page.
- No Document Centre PDFs.
- No hosting/deploy config — nothing is live.
- No file upload for candidate ID/CV/photo.

---

**For the claude.ai side:** treat this repo as the current source of truth for the coded build — it supersedes both the Design A multi-page files and the Design B screenshot in the handoff zip. Next real decision points are the four items in "What's NOT in this repo" above, plus Roger's sign-off on the legal/registration/fee gates.
