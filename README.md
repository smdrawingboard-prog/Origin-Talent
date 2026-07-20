# Origin Talent — Website

Single-page marketing site for Origin Talent (domestic staffing recruitment,
Johannesburg). `index.html` is fully self-contained — all CSS and the logo
are inlined, no build step required.

## Structure

- `index.html` — the site (hero, services, how it works, about, testimonials,
  FAQ, client staffing enquiry form, candidate application form, document
  centre, contact, footer).
- `apps-script/client-enquiries.gs` — Google Apps Script backend for the
  Client Staffing Enquiry form.
- `apps-script/candidate-applications.gs` — Google Apps Script backend for
  the Candidate Application form.

## Deploying the two form backends

Each form posts to a Google Sheet via an Apps Script Web App. For **each**
`.gs` file:

1. Create (or open) the Google Sheet that should receive submissions, with a
   sheet/tab named `Sheet1`.
2. **Extensions > Apps Script**, paste in the matching file's contents as
   `Code.gs`.
3. **Deploy > New deployment > type "Web app"**.
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**, authorize, and copy the resulting Web App URL.

Then open `index.html`, find the `SHEETS_ENDPOINTS` object near the bottom
(in the final `<script>` block), and fill in the two URLs:

```js
var SHEETS_ENDPOINTS = {
  client: 'PASTE_CLIENT_ENQUIRIES_WEB_APP_URL_HERE',
  candidate: 'PASTE_CANDIDATE_APPLICATIONS_WEB_APP_URL_HERE'
};
```

Until these are filled in, both forms still work from a visitor's
perspective (they show a "captured, not yet connected" confirmation) but
nothing is saved anywhere — fill these in before going live.

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
