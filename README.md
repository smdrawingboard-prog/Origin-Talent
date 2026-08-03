# Origin Talent — Website

Single-page marketing site for Origin Talent (domestic staffing recruitment,
Johannesburg). `index.html` is fully self-contained — all CSS and the logo
are inlined, no build step required.

## Structure

- `index.html` — the site (hero, services, how it works, about, testimonials,
  FAQ, client staffing enquiry form, candidate application form, document
  centre, contact, footer).
- `apps-script/client-enquiries.gs` / `apps-script/candidate-applications.gs`
  — legacy Google Apps Script + Sheets backend. Kept for reference/rollback
  only; the live site does **not** call these.
- `supabase/001_init.sql` — creates the two tables and their original
  insert-only RLS policies.
- `supabase/002_tighten_rls.sql` — replaces those policies with ones that
  enforce required fields, the POPIA/declaration checkboxes, and length
  caps, instead of a blanket `WITH CHECK (true)`. Run after `001_init.sql`.
- `supabase/003_staff_dashboard.sql` — adds pipeline tracking columns and
  a `staff` directory/auth layer so staff can read and manage submissions.
  Run after `002_tighten_rls.sql`.
- `dashboard.html` — internal staff dashboard for working the enquiry and
  application pipelines. Not linked from the public site.

## Form backend: Supabase

Both the Client Staffing Enquiry form and the Candidate Application form
write directly to a Supabase project (`kajwnrstdyfcwvyufket`) via
`supabase-js`, loaded from CDN in `index.html`:

- `client_enquiries` table — one row per client staffing enquiry.
- `candidate_applications` table — one row per candidate application.

Both tables have row-level security enabled with an **insert-only** policy
for anonymous visitors — the public key embedded in the page can add rows
but cannot read, edit or delete existing ones. The insert policy also
validates required fields, the POPIA/declaration checkboxes, and length
caps server-side (see `supabase/002_tighten_rls.sql`) — it doesn't just
trust the form's client-side JavaScript, since anyone can POST to the
REST API directly.

The SQL in `supabase/` was run manually in the Supabase SQL Editor for
that project (`001_init.sql` then `002_tighten_rls.sql`) — it's checked in
here for version history, but changing these files does **not** apply them;
re-run the SQL in the Supabase Dashboard to apply schema changes.

The project URL and anon/publishable key are set near the bottom of
`index.html`, in the final `<script>` block:

```js
var SUPABASE_URL = 'https://kajwnrstdyfcwvyufket.supabase.co';
var SUPABASE_ANON_KEY = 'sb_publishable_djBWndOqnzRsVzHtfhqAHQ_giqehaME';
```

The anon/publishable key is safe to expose client-side by design — it only
has the permissions granted by RLS policies above. To view submissions,
use the Supabase Dashboard's Table Editor for that project (service-role
access, not exposed to the site).

### Reverting to Google Sheets

If you ever want to go back to the Apps Script + Sheets flow, redeploy the
two `.gs` files as Web Apps (Extensions > Apps Script > Deploy > New
deployment > Web app, execute as Me, access Anyone) and swap the form
submit handler back to `fetch(endpoint, ...)` against those URLs instead of
`sb.from(table).insert(...)`.

## Staff dashboard

`dashboard.html` is an internal, self-contained page (same no-build-step
pattern as `index.html`, same brand fonts/colours) for staff to work the
two form pipelines: Client Enquiries and Candidate Applications. It is
**not** linked from the public site and has `<meta name="robots" content="noindex, nofollow">`,
but the file itself is not secret — access to data is enforced server-side
by Supabase Auth + RLS, not by hiding the URL.

What it does:

- Sign-in (Supabase Auth email/password) gated to rows in the `staff`
  table — the anon key alone gets you a login form, nothing else.
- Overview KPIs (new enquiries/applications in the last 7 days, active
  pipeline counts, placements this month) and a recent-activity feed.
- Client Enquiries and Candidate Applications tables: search, filter by
  stage, colour-coded "days in stage" ageing (amber at 10+ days, red at
  20+), and a detail view per record showing every field submitted on the
  form.
- From the detail view: change pipeline stage, assign a staff member, add
  internal notes (staff-only, separate from the applicant's own notes),
  and — admins only — permanently delete a record for a POPIA
  data-erasure request.
- A Staff panel showing the directory and each person's open workload.

What it deliberately does **not** do: there's no revenue/deal-value
tracking, currency figures, LinkedIn/HubSpot/Salesforce/Pipedrive/Bullhorn
integrations, or document upload panel. The website's forms don't capture
a monetary deal value, and Origin Talent is a single-office domestic
staffing agency rather than a multi-team sales org, so that machinery
would be dead weight — this stays scoped to the two pipelines the site
actually generates.

### Setting up staff access

1. Run `supabase/003_staff_dashboard.sql` in the Supabase SQL Editor
   (after `001_init.sql` and `002_tighten_rls.sql`).
2. In the Supabase Dashboard, go to **Authentication → Users → Add user**
   and create the first staff account (email + password, or send an
   invite).
3. Copy that user's UID, then in the SQL Editor:
   ```sql
   insert into public.staff (id, full_name, email, role)
   values ('<uid>', 'Full Name', 'person@origintalent.co.za', 'admin');
   ```
   Use `role = 'consultant'` for non-admin staff — admins can additionally
   delete records (POPIA erasure) and manage the `staff` table.
4. Repeat steps 2–3 for each additional staff member. There's no
   self-serve sign-up in `dashboard.html` by design.

## Quick contact form

The short "Get In Touch" form at the bottom of the page has no dedicated
spreadsheet backend. It opens WhatsApp with the enquiry pre-filled, since
WhatsApp is the site's primary contact channel — no extra deployment needed.

## Document Centre PDFs

`documents/` holds the three PDFs linked from the Document Centre section:

- `Origin-Talent-Client-Staffing-Enquiry-Form.pdf` — printable version of
  the online client enquiry form.
- `Origin-Talent-Candidate-Application-Form.pdf` — printable version of
  the online candidate application form.
- `Origin-Talent-Client-Service-Agreement.pdf` — a working-draft placement
  terms agreement (fee and guarantee-period fields left blank for a
  consultant to fill in per client; matches the "working draft" notice
  already on the site).

They're generated by `documents/generate_pdfs.py` (`pip install reportlab`,
then `python3 documents/generate_pdfs.py`) rather than hand-built, so if
the online forms' fields or options change, update the data in that script
and re-run it instead of editing the PDFs directly.

## Hosting

The site is static — deploy `index.html` as-is to any static host (GitHub
Pages, Netlify, Vercel, etc.) or upload directly to the production domain.
