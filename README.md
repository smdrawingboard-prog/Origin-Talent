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

## Quick contact form

The short "Get In Touch" form at the bottom of the page has no dedicated
spreadsheet backend. It opens WhatsApp with the enquiry pre-filled, since
WhatsApp is the site's primary contact channel — no extra deployment needed.

## Known gap: Document Centre PDFs

The Document Centre section links to three PDFs that don't exist yet:

- `documents/Origin-Talent-Client-Staffing-Enquiry-Form.pdf`
- `documents/Origin-Talent-Candidate-Application-Form.pdf`
- `documents/Origin-Talent-Client-Service-Agreement.pdf`

Add real files at those paths (a `documents/` folder) before launch, or
remove the download cards if printable versions aren't needed.

## Hosting

The site is static — deploy `index.html` as-is to any static host (GitHub
Pages, Netlify, Vercel, etc.) or upload directly to the production domain.
