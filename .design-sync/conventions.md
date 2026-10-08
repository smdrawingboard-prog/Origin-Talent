# Origin Talent - brand kit conventions

Origin Talent is a Johannesburg domestic-staffing agency (nannies, tutors, house managers, chefs, drivers). Tone: warm, trustworthy, premium-but-friendly. This kit has **no JS components** - it is a token + CSS-class vocabulary extracted from the live site. Build with plain HTML and these classes. Do not invent colours, fonts or class names.

## Setup
Link `styles.css` (it imports `tokens/tokens.css` and the Google Fonts: Fraunces, Inter, Dancing Script). Without it nothing is styled. Page background is white; `body` is Inter, colour `--ink`.

```html
<link rel="stylesheet" href="styles.css">
```

## Tokens (use `var(--name)`, never raw hex)
`--blue` #0349A9 primary / links / CTAs; `--blue-dark` #062F73 hover, topbar, stats, footer; `--blue-tint` #EFF4FC soft section and icon backgrounds; `--gold` #C9A227 accent (stars, highlight button, warnings only); `--cream` #FBF8F1 warm hover surface; `--ink` #1B2233 text; `--ink-soft` #525B72 body copy; `--line` #E3E8F2 borders; `--radius` 14px cards. Fonts: `--font-display` Fraunces (h1-h3, big numbers, wordmark), `--font-body` Inter, `--font-script` Dancing Script (`.script` taglines only).

## Class vocabulary
- Layout: `.wrap` (1180px centred), `.section` (84px vertical), `.section.tint`, `.section-head` (centred h2 + p), `.eyebrow` (small blue caps label above a heading).
- Buttons (pill): `.btn` + `.btn-primary` | `.btn-outline` | `.btn-gold`.
- Cards (white, 1px `--line` border, radius `--radius`): `.svc-card` (+ `.svc-icon`, `.lnk`), `.step` (+ `.n`), `.testi` (+ `.stars`, `.who`), `.download-card`, `.contact-card`, `.form-panel`.
- Grids: `.grid-6` (3 col), `.steps` (4 col), `.testi-grid` (3 col), `.stats .wrap` (4 col on `--blue-dark`).
- Bands: `.stats` (dark blue strip with `.num`/`.lbl`), `.jobseek` (blue gradient call-to-action panel).
- Forms: `.field` (label + input/select/textarea), `.form-2col`, `.checkrow`, `.notice-box` (+ `.warn` for gold).
- FAQ: `<details class="faq-item"><summary>Q</summary><div class="a">A</div></details>` inside `.faq`.
- Header/footer: `header.site`, `.topbar`, `footer` with `.foot-grid`.

## Rules of thumb
Headings are Fraunces 600; everything else Inter. One primary button per view; secondary is `.btn-outline`. Gold is an accent, never a large fill. Mobile breakpoints are 980/760/560px; tap targets are at least 44px. Copy is South African English, WhatsApp is the preferred contact channel, and POPIA consent sits next to any form.

## Source of truth
Read `styles.css` and `tokens/tokens.css` before styling. Logo: `assets/logo.png` (portrait mark; invert to white on dark backgrounds with `filter:brightness(0) invert(1)`).

## Example
```html
<section class="section tint"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Our services</span>
    <h2>Trusted people for your home</h2><p>Vetted, screened and reliable.</p></div>
  <div class="grid-6">
    <div class="svc-card"><div class="svc-icon">👶</div><h3>Nannies</h3>
      <p>Experienced, background-checked childcare.</p><a class="lnk" href="#">Learn more →</a></div>
  </div>
  <a class="btn btn-primary" href="#">Request staff</a>
</div></section>
```
