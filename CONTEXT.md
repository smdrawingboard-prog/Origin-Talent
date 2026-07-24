# ORIGIN TALENT — FULL CONTEXT HANDOFF FOR CLAUDE CODE

Prepared by: Fate Collab (Claude in claude.ai) — 24 July 2026
Purpose: Drop this file into the repo (e.g. as `CONTEXT.md` or paste into `CLAUDE.md`) so Claude Code has everything Claude.ai already knows. This closes the loop between the two tools.

---

## 1. CLIENT & BRAND

- **Client:** Origin Talent (Pty) Ltd — professional domestic & household staffing agency, South Africa
- **Tagline (client's own):** "Exceptional People for Exceptional Homes"
- **Contact:** Roger Donaldson, Director — roger@origintalent.co.za / +27 10 502 0105 (office) / +27 76 958 1501 (mobile)
- **Site-facing admin email:** admin@origintalent.co.za
- **Address:** First Floor, Dainfern Square, Cnr Winnie Mandela & Broadacres Drive, Dainfern, Johannesburg, 2191
- **Claimed domain:** [www.origintalent.co.za](https://www.origintalent.co.za)
- **Brand palette (from Phase 1 build + logo):** Navy (#-ish dark blue) and gold, logo mark is a stylised blue dancer/figure with three stars, wordmark "ORIGIN TALENT" with tracked-out "TALENT" subline
- **Production credit note:** Phase 1 files carry "Production by BTR Africa (Pty) Ltd" — confirm with Faye whether that's a partner or a prior vendor before anything ships under Fate Collab.

---

## 2. TWO DESIGN DIRECTIONS EXIST — NOT YET RECONCILED

**Direction A — "Phase 1" (already coded, in the original zip):**
Minimal/editorial, navy+gold, card-based, no photography. Fully built: home, client enquiry form, candidate application form, privacy page, downloads page. Forms are demo-capture only (not wired to a backend).

**Direction B — newer screenshot (homepage only, seen by Claude.ai, not yet by Claude Code):**
Warm, lifestyle-photography-led. Blue top bar with contact details, full-width hero photo (mother reading with two children), headline "Exceptional People. Trusted in Your Home. Peace of Mind, Every Day." Icon-based 6-category service grid (Nannies & Au Pairs, Tutors & Educators, House Managers, Private Chefs, Domestic Staff, Drivers & Assistants). Stats bar: 10,000+ Successful Placements, 98% Client Satisfaction, 24–72hrs Average Placement Time, 15+ Years Industry Experience. Full nav: Home / Employers / Job Seekers / Our Services / About Us / Resources / Contact, plus "Hire Staff" CTA button.

**Open decision:** which direction is canonical. Recommendation from Claude.ai: rebuild around Direction B's warmer homepage (better emotional fit for the audience) while keeping Direction A's already-built form/legal page infrastructure underneath it. **Not yet confirmed by Faye — check before treating either as final.**

**Claude Code: if you've built further on Direction B, please add a summary of what exists (pages, stack, repo structure, deployment URL if any) back into this file or the Project Brain doc so Claude.ai stays current too.**

---

## 3. SITE MAP (target — merge of both directions until told otherwise)

- `/` Home
- `/employers` or `/client` — Client Staffing Enquiry (form)
- `/job-seekers` or `/candidate` — Candidate Application (form)
- `/services` — Our Services (category breakdown, see Section 4)
- `/about` — About Us
- `/resources` — Resources / blog (not yet scoped)
- `/downloads` — Document centre (PDF downloads of the 3 forms/agreement)
- `/privacy` — POPIA privacy notice
- `/contact`

---

## 4. WEBSITE COPY — CLIENT-SUPPLIED (verbatim from Roger, 14 Jul 2026 email "Website Text and Picture Examples")

Use this as the base copy for the Services section / category pages. 20 category photos were attached to that email but have not yet been pulled into any build — request them from Faye/Gmail or ask Roger to resend as a shared folder.

**Intro:**
> Professional Domestic & Household Staffing Services — Exceptional People for Exceptional Homes
> At Origin Talent we specialize in sourcing, screening, and placing highly qualified household and personal support professionals to meet the unique needs of families, individuals, and estates. Our rigorous recruitment process ensures that every candidate is experienced, trustworthy, and committed to delivering exceptional service.
> Whether you require childcare support, household management, personal assistance, or specialist care services, we connect you with professionals who fit seamlessly into your lifestyle.

**Our Placement Services (category name → description):**

| Category | Description |
|---|---|
| Au Pair | We place experienced and caring Au Pairs who provide reliable childcare support while helping children learn, grow, and thrive in a nurturing environment. Our Au Pairs are carefully selected for their professionalism, responsibility, and genuine passion for working with children. |
| Caregivers | Our qualified Nurses and Caregivers provide compassionate care for seniors, individuals recovering from illness, and those requiring ongoing assistance. We match clients with professionals who deliver personalized care while maintaining dignity, comfort, and independence. |
| House Managers | A well-managed home requires exceptional organization. Our House Managers oversee household operations, coordinate staff, manage schedules, supervise maintenance, and ensure your home runs efficiently every day. |
| Night Nurses | Our experienced Night Nurses provide overnight care for new-borns and infants, allowing parents to rest with confidence. They assist with feeding routines, sleep training, monitoring, and overall infant care during night-time hours. |
| Chauffeurs | We recruit professional Chauffeurs who offer safe, reliable, and discreet transportation services. Our drivers maintain the highest standards of professionalism, punctuality, and customer service. |
| Babysitters | Our trusted Babysitters provide flexible childcare solutions for families requiring occasional, part-time, or emergency childcare support. Every candidate undergoes thorough screening and reference verification. |
| Personal Assistants (Home & Office) | Our Personal Assistants help busy professionals and families manage daily responsibilities, schedules, correspondence, appointments, travel arrangements, and administrative tasks both at home and in the workplace. |
| Pet Care Specialists | Your pets deserve the highest level of care. We place experienced Pet Care professionals who provide feeding, exercise, grooming support, companionship, and overall wellbeing management for your beloved animals. |
| Private Chefs | Enjoy exceptional dining experiences in the comfort of your home with our skilled Private Chefs. Whether for daily meal preparation, special dietary requirements, family gatherings, or private events, we match you with culinary professionals who meet your preferences. |
| Tutors & Governesses | Our Tutors and Governesses provide personalized educational support, academic guidance, and child development assistance. We carefully select professionals who can help children excel academically while fostering confidence and personal growth. |

**Why Choose Us:**
- Thorough candidate screening and background checks
- Reference verification and qualification assessment
- Personalized matching process
- Confidential and professional service
- Ongoing client support
- High-quality candidates with proven experience

**Closing CTA copy:**
> Let Us Find the Right Professional for You — Finding trustworthy and qualified household staff can be challenging. Our dedicated recruitment specialists make the process simple, efficient, and stress-free by connecting you with exceptional professionals who meet your exact requirements. Contact us today to discuss your staffing needs and discover how we can help you build the perfect support team for your home, family, or business.

**Available role categories (used as dropdown options across both forms):** Au Pair, Nanny, Caregiver, Registered Nurse, Night Nurse, House Manager, Cleaner, Chauffeur, Babysitter, Personal Assistant, Private Chef, Pet Sitter, Tutor / Governess.

---

## 5. FORM SPECIFICATIONS

### 5a. Client Staffing Enquiry Form (`/employers` or `/client`)

**Contact info:** Full name*, Company name (optional), Email*, Mobile*, Alternative contact number, Preferred contact method (Phone/Email/WhatsApp), Home/work address*

**Position requirement:** Position required* (dropdown, categories above), Employment type (Permanent/Temporary/Fixed-term/Part-time), Position arrangement (Live-in/Live-out/Flexible), Days required (Mon–Sun checkboxes), Working hours, Placement urgency (Immediate/Within 1 week/Within 1 month/Flexible), Expected salary range (R5,000–R8,000 / R9,000–R12,000 / R13,000–R15,000 / R16,000+ / Discuss), Driving required (Yes/No), Language requirements

**Free text:** Duties and responsibilities* (textarea), Additional requirements/notes (textarea)

**Consent checkbox (required):** "I authorise Origin Talent to process this information for recruitment and placement services in accordance with its privacy notice." Include the note: "Selection criteria must be linked to lawful, genuine role requirements" (POPIA/labour-law protection against discriminatory briefs).

### 5b. Candidate Application Form (`/job-seekers` or `/candidate`)

**Personal info:** Full name*, Date of birth*, ID/passport number*, Nationality, Residential address*, Province, Mobile*, Email*, Next of kin name, Next of kin number, Valid driver's licence (Y/N), Reliable transport (Y/N)

**Application details:** Position applying for* (dropdown), Availability (Full-time/Part-time/Temporary/Weekend/Night shifts/Emergency — checkboxes), Position type (Live-in/Live-out/Flexible), Legally permitted to work in SA (Y/N), Able to perform essential duties (Yes/No/Reasonable accommodation may be required)

**Free text:** Skills and experience* (textarea), Qualifications and training (textarea), Languages spoken

**Screening consent (checkboxes):** Identity verification, Reference checks, Qualification verification, Criminal-record check where lawful and relevant

**Supporting documents checklist (do NOT build as public upload fields yet — see Section 7 gate):** Professional photograph, CV, ID/passport + work authorisation, Reference letter/contactable references, Driver's licence if applicable, Qualifications/certificates, Police clearance if available, Proof of address (requested securely at the appropriate stage)

**Security note to display on this form:** "Do not email or upload bank statements through an unsecured public channel. Banking information should only be requested when necessary and through an approved secure process."

**Declaration + consent checkbox (required):** "I certify that the information supplied is true and complete... I authorise Origin Talent to verify information, contact references and conduct lawful background checks. I consent to the secure processing and storage of my personal information for recruitment and placement purposes in accordance with the privacy notice."

---

## 6. LEGAL / COMPLIANCE DOCUMENTS — DO NOT PUBLISH AS FINAL

### Client Service Agreement — 14 numbered clauses covering: Appointment, Services, Client responsibilities, Fees & payment (30-day terms), Permanent placement fees (due on offer acceptance/start, 12-month non-circumvention window), Temp/contract staffing, Replacement support, Verification limitations, Confidentiality & POPIA, Non-circumvention, Liability, Termination (30 days notice), Disputes/governing law (South African law, mediation/arbitration before court), Entire agreement. Has a Commercial Schedule (fee, VAT, deposit, replacement period, payment terms — all currently blank).
**GATE: South African legal counsel must review before this is published or signed. Company registration number and fee schedule are still blank placeholders.**

### Privacy / POPIA Notice — covers purpose, information collected, special personal information (criminal record/health), sharing, retention & security, data-subject rights, contact (admin@origintalent.co.za).
**GATE: needs the actual Information Officer's name, real retention periods, list of operators/processors, and PAIA manual reference before publication.**

---

## 7. RELEASE GATES (do not let these slip through to production)

1. Forms are currently front-end capture only — must be wired to a real destination (CRM, secure form endpoint, or monitored mailbox) before go-live. Faye/Roger have not yet chosen which.
2. Candidate ID/CV/photo/police-clearance uploads need secure, access-controlled storage — not an open public form field. Do not build this as a plain `<input type="file">` posting to an unsecured endpoint.
3. Client Service Agreement — legal review required (Section 6).
4. Privacy notice — Information Officer detail required (Section 6).
5. Company registration number, final fee schedule, and final domain/hosting are still outstanding.
6. Selection-criteria language on the client form must stay tied to lawful, non-discriminatory role requirements — don't let a client brief slip into unlawful preference language (age/race/gender etc. unless a genuine occupational requirement).

---

## 8. SEO REQUIREMENTS (Fate Collab standard — bake into every page)

- Location targeting: Dainfern, Fourways, Sandton, Bryanston, Johannesburg North — Google.co.za intent
- Every page needs: unique title tag (<60 chars), meta description (<160 chars), H1→H2→H3 structure, alt text on every image, internal links between service categories and the enquiry form
- Schema recommendation: `EmploymentAgency` or `LocalBusiness` structured data on the homepage; `Service` schema per category page if categories get their own URLs
- Current gap (Phase 1 build): only `index.html` has a meta description; `client.html`, `candidate.html`, `privacy.html`, `downloads.html` have title tags but no meta descriptions — fix this
- AI-search visibility (ChatGPT/Perplexity/Google AI Overviews): add FAQ-style content per category once design direction is confirmed (e.g. "How do I hire a night nurse in Johannesburg?") — Phase 2, not urgent

---

## 9. TECH NOTES FROM PHASE 1 BUILD (for reference/reuse)

- Plain HTML/CSS/JS, no framework — `styles.css` + `script.js` shared across pages
- `en-ZA` lang attribute already set correctly on all pages
- Forms use `data-demo` attribute and show/hide a `.form-status` div — currently just a front-end acknowledgment, no real submission handler
- File structure:

```
site/
 ├─ index.html
 ├─ client.html
 ├─ candidate.html
 ├─ privacy.html
 ├─ downloads.html
 ├─ styles.css
 └─ script.js
documents/
 ├─ Origin Talent - Client Staffing Enquiry Form.docx/.pdf
 ├─ Origin Talent - Candidate Application Form.docx/.pdf
 └─ Origin Talent - Client Service Agreement.docx/.pdf
```

---

## 10. OPEN QUESTIONS (ask Faye/Roger — don't guess and ship)

1. Which design direction is canonical — A, B, or a merge?
2. Where should form submissions go — which CRM/inbox?
3. Who is Origin Talent's Information Officer?
4. Has the Service Agreement gone to SA legal counsel?
5. Final registration number + fee schedule?
6. Is BTR Africa still involved as a vendor?
7. Domain/hosting — confirmed provider and timeline?

---

## 11. LOOP-CLOSING INSTRUCTION FOR CLAUDE CODE

This project is also tracked in a Claude.ai Project under the file **"Origin Talent Project Brain"** (workflow tracker + email log + document inventory). If you make material changes here — new pages, new copy, a chosen design direction, a deployment URL — please write a short changelog entry back into this file or flag it to Faye so she can paste it into the Claude.ai project. That's what keeps both tools in sync instead of drifting into two different builds, which is what happened this week.

---

## 12. CLAUDE CODE STATUS — appended 24 July 2026

What actually exists in `smdrawingboard-prog/Origin-Talent` right now, so Claude.ai stays current:

**This repo already *is* Direction B**, built as a single scrolling page rather than the full sitemap in Section 3. Confirmed matches to this doc, verbatim: the stats bar (10,000+ Successful Placements, 98% Client Satisfaction, 24–72hrs Average Placement Time, 15+ Years Industry Experience), the 6-category services grid (Nannies & Au Pairs, Tutors & Educators, House Managers, Private Chefs, Domestic Staff, Drivers & Assistants), the top info bar with office/WhatsApp/email, and both forms' role dropdowns (exact match to Section 4's 13-category list). It does **not** yet have the full-width lifestyle hero photo, or separate URLs for `/employers`, `/job-seekers`, `/services`, `/about`, `/resources`, `/privacy`, `/contact` — those are in-page anchors on one `index.html`.

**Two branches exist, not yet reconciled:**
- `claude/site-build-nvcfpm` — the branch this session has been working on. Single-page site above; both forms (Client Staffing Enquiry, Candidate Application) write live to a Supabase project (`kajwnrstdyfcwvyufket`, tables `client_enquiries` / `candidate_applications`), RLS locked to insert-only with server-side validation (required fields, POPIA/declaration checkboxes, length caps). Legacy Google Apps Script + Sheets backend kept in `apps-script/` for reference only, not called.
- `claude/site-build-origin-talent` (merged via PR #1 from `claude/skill-build-connect-sd0rk9`, a separate Claude Code session) — everything above, **plus** an internal staff dashboard (`dashboard.html`) gated by Supabase Auth against a `staff` table, with pipeline stage tracking, staff assignment, internal notes, and admin-only POPIA erasure (`supabase/003_staff_dashboard.sql`).

**Release gates (Section 7), checked against what's actually built:**
1. Forms wired to a real destination — **done** on `claude/site-build-nvcfpm` (Supabase, not just front-end capture). Still needs Roger/Faye's sign-off that Supabase is the chosen destination rather than a specific CRM.
2. Candidate document uploads — **not applicable yet**; no file-upload fields exist on the form at all, so no unsecured-upload risk.
3. Client Service Agreement — **not resolved**. The site links to a `documents/Origin-Talent-Client-Service-Agreement.pdf` download that doesn't exist in the repo; flagged as a known gap in `README.md` rather than fabricated.
4. Privacy/POPIA notice — **not built**. No dedicated `/privacy` page; only inline POPIA consent checkboxes on both forms.
5. Registration number / fee schedule / hosting — not displayed anywhere on the site (no gate triggered).
6. Lawful selection-criteria language — looks fine; the client form's role/employment fields don't include age/gender/race-adjacent options.

**Not yet done, deliberately left for a decision rather than guessed:** adopting Roger's longer 10-category service descriptions from Section 4 (site currently uses short one-line blurbs for 6 broader categories); splitting into the target sitemap's separate URLs; the full-width hero photo; reconciling the two branches above into one.
