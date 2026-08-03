#!/usr/bin/env python3
"""
Generates the three Document Centre PDFs linked from index.html:
  - Origin-Talent-Client-Staffing-Enquiry-Form.pdf
  - Origin-Talent-Candidate-Application-Form.pdf
  - Origin-Talent-Client-Service-Agreement.pdf

Source of truth for field lists/options is the live online forms in
index.html (search for data-demo="client" / data-demo="candidate"). If
those forms change, update the FORM data below to match and re-run:

    python3 documents/generate_pdfs.py

Requires: reportlab (pip install reportlab)
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- brand ----
BLUE = colors.HexColor('#0349A9')
BLUE_DARK = colors.HexColor('#062F73')
GOLD = colors.HexColor('#C9A227')
INK = colors.HexColor('#1B2233')
INK_SOFT = colors.HexColor('#525B72')
LINE = colors.HexColor('#B9C4DC')
TINT = colors.HexColor('#EFF4FC')

ADDRESS = "First Floor, Dainfern Square, Cnr Winnie Mandela & Broadacres Drive, Dainfern, Johannesburg, 2191"
PHONE = "+27 10 502 0105"
WHATSAPP = "+27 76 958 1501"
EMAIL = "roger@origintalent.co.za"
SITE = "www.origintalent.co.za"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('DocTitle', parent=styles['Title'], fontName='Helvetica-Bold',
                           fontSize=16, textColor=BLUE_DARK, spaceAfter=2, alignment=TA_CENTER))
styles.add(ParagraphStyle('Brand', parent=styles['Normal'], fontName='Helvetica-Bold',
                           fontSize=18, textColor=BLUE_DARK, alignment=TA_CENTER, leading=20))
styles.add(ParagraphStyle('Tagline', parent=styles['Normal'], fontName='Helvetica-Oblique',
                           fontSize=9.5, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle('ContactLine', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=8.3, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle('Instructions', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=9, textColor=INK_SOFT, spaceAfter=10, leading=12))
styles.add(ParagraphStyle('FieldLabel', parent=styles['Normal'], fontName='Helvetica-Bold',
                           fontSize=9.3, textColor=INK, spaceAfter=1))
styles.add(ParagraphStyle('SectionHead', parent=styles['Normal'], fontName='Helvetica-Bold',
                           fontSize=11.5, textColor=BLUE_DARK, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=9.4, textColor=INK, leading=13.5, spaceAfter=6))
styles.add(ParagraphStyle('Notice', parent=styles['Normal'], fontName='Helvetica-Oblique',
                           fontSize=8.4, textColor=INK_SOFT, leading=11.5))
styles.add(ParagraphStyle('Footer', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=7.6, textColor=INK_SOFT, alignment=TA_CENTER))


def letterhead(title):
    story = [
        Paragraph("ORIGIN TALENT", styles['Brand']),
        Paragraph("Exceptional People, Trusted in Your Home", styles['Tagline']),
        HRFlowable(width="100%", thickness=1.4, color=GOLD, spaceAfter=8),
        Paragraph(title, styles['DocTitle']),
        Spacer(1, 4),
        Paragraph(
            f"{ADDRESS} &nbsp;|&nbsp; {PHONE} &nbsp;|&nbsp; WhatsApp {WHATSAPP} &nbsp;|&nbsp; {EMAIL}",
            styles['ContactLine']
        ),
        Spacer(1, 10),
    ]
    return story


def footer_note(text):
    return [
        Spacer(1, 14),
        HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=6),
        Paragraph(text, styles['Footer']),
    ]


def field_line(label, required=False, blank_w=None, label_w=48*mm):
    """A single-line field: bold label + an underline box to write in."""
    lbl = label + (" *" if required else "")
    t = Table(
        [[Paragraph(lbl, styles['FieldLabel']), '']],
        colWidths=[label_w, blank_w or (170*mm - label_w)]
    )
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LINEBELOW', (1, 0), (1, 0), 0.8, LINE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


def two_col_fields(pairs):
    """pairs: list of (label, required) tuples, rendered two per row."""
    rows = []
    for i in range(0, len(pairs), 2):
        left = pairs[i]
        right = pairs[i+1] if i+1 < len(pairs) else None
        left_cell = field_line(left[0], left[1], blank_w=38*mm, label_w=45*mm)
        if right:
            right_cell = field_line(right[0], right[1], blank_w=38*mm, label_w=45*mm)
        else:
            right_cell = ''
        rows.append([left_cell, right_cell])
    t = Table(rows, colWidths=[85*mm, 85*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (1, 0), (1, -1), 8),
    ]))
    return t


def checkbox_item(text, item_width):
    """A hand-drawn empty checkbox (base-14 fonts have no reliable ballot-box
    glyph — Unicode U+2610 renders as a solid tofu box in Helvetica) followed
    by its label, as a single flowable."""
    box = Table([['']], colWidths=[3.6*mm], rowHeights=[3.6*mm])
    box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.9, INK_SOFT),
    ]))
    t = Table([[box, Paragraph(text, styles['Body'])]], colWidths=[5.5*mm, item_width - 5.5*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('LEFTPADDING', (1, 0), (1, 0), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    return t


def checkbox_grid(options, columns=3, col_width=None):
    cw = col_width or (170*mm / columns)
    rows = []
    for i in range(0, len(options), columns):
        row = options[i:i+columns]
        row_cells = [checkbox_item(opt, cw) for opt in row]
        while len(row_cells) < columns:
            row_cells.append('')
        rows.append(row_cells)
    t = Table(rows, colWidths=[cw]*columns)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return t


def ruled_block(n_lines=4):
    rows = [[''] for _ in range(n_lines)]
    t = Table(rows, colWidths=[170*mm], rowHeights=[7*mm]*n_lines)
    t.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.7, LINE),
    ]))
    return t


def signature_block(party_label="Signature"):
    t = Table(
        [[
            Paragraph(f"{party_label}: ______________________________", styles['Body']),
            Paragraph("Date: ______________________", styles['Body']),
        ]],
        colWidths=[110*mm, 60*mm]
    )
    return t


ROLE_OPTIONS = [
    "Au Pair", "Nanny", "Caregiver", "Registered Nurse", "Night Nurse",
    "House Manager", "Cleaner", "Chauffeur", "Babysitter",
    "Personal Assistant", "Private Chef", "Pet Sitter", "Tutor / Governess",
]

# ------------------------------------------------------------ document 1 ---
def build_client_enquiry():
    story = letterhead("Client Staffing Enquiry Form")
    story.append(Paragraph(
        "Please complete in full and return via WhatsApp, email or in person to your Origin Talent "
        "consultant. Fields marked * are required. For the fastest response, submit online at "
        f"{SITE} or WhatsApp {WHATSAPP}.",
        styles['Instructions']
    ))

    story.append(field_line("Full name", required=True))
    story.append(field_line("Company name (if applicable)"))
    story.append(two_col_fields([
        ("Email address", True), ("Mobile number", True),
    ]))
    story.append(two_col_fields([
        ("Alternative contact number", False), ("Home / work address", False),
    ]))

    story.append(Paragraph("Preferred contact method", styles['FieldLabel']))
    story.append(checkbox_grid(["Phone", "Email", "WhatsApp"], columns=3))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Position required *", styles['FieldLabel']))
    story.append(checkbox_grid(ROLE_OPTIONS, columns=3))
    story.append(field_line("If other, please specify", blank_w=100*mm, label_w=60*mm))

    story.append(two_col_fields([
        ("Employment type", False), ("Position arrangement", False),
    ]))
    story.append(checkbox_grid(["Permanent", "Temporary", "Fixed-term", "Part-time"], columns=4))
    story.append(Spacer(1, 4))
    story.append(checkbox_grid(["Live-in", "Live-out", "Flexible"], columns=3))
    story.append(Spacer(1, 6))

    story.append(two_col_fields([
        ("Working hours", False), ("Driving required", False),
    ]))
    story.append(checkbox_grid(["No", "Yes"], columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Placement urgency", styles['FieldLabel']))
    story.append(checkbox_grid(["Immediate", "Within 1 week", "Within 1 month", "Flexible"], columns=4))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Expected salary range", styles['FieldLabel']))
    story.append(checkbox_grid(
        ["R5 000–R8 000", "R9 000–R12 000", "R13 000–R15 000", "R16 000+", "Discuss"],
        columns=3
    ))
    story.append(Spacer(1, 6))

    story.append(field_line("Language requirements"))

    story.append(Paragraph("Days required", styles['FieldLabel']))
    story.append(checkbox_grid(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], columns=4
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Duties and responsibilities *", styles['FieldLabel']))
    story.append(ruled_block(4))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Additional requirements or notes", styles['FieldLabel']))
    story.append(ruled_block(3))
    story.append(Spacer(1, 10))

    story.append(checkbox_item(
        "I consent to Origin Talent processing this information for recruitment and "
        "placement services in accordance with its privacy notice. *",
        170*mm
    ))
    story.append(Paragraph(
        "Selection criteria must be linked to lawful, genuine role requirements. Nationality or "
        "demographic preferences may not be used unlawfully or discriminatorily.",
        styles['Notice']
    ))
    story.append(Spacer(1, 14))
    story.append(signature_block("Client signature"))

    story += footer_note(
        "Origin Talent — Client Staffing Enquiry Form · Printable reference version of the online form."
    )
    return story


# ------------------------------------------------------------ document 2 ---
def build_candidate_application():
    story = letterhead("Candidate Application Form")
    story.append(Paragraph(
        "Please provide complete and accurate information for consideration in suitable household "
        f"roles. Fields marked * are required. Prefer WhatsApp? Message us on {WHATSAPP} instead.",
        styles['Instructions']
    ))

    story.append(field_line("Full name", required=True))
    story.append(two_col_fields([
        ("Date of birth", True), ("ID / passport number", True),
    ]))
    story.append(two_col_fields([
        ("Nationality", False), ("Province", False),
    ]))
    story.append(field_line("Residential address", required=True))
    story.append(two_col_fields([
        ("Mobile number", True), ("Email address", True),
    ]))
    story.append(two_col_fields([
        ("Next of kin — name", False), ("Next of kin — number", False),
    ]))

    story.append(Paragraph("Position applying for *", styles['FieldLabel']))
    story.append(checkbox_grid(ROLE_OPTIONS, columns=3))
    story.append(field_line("If other, please specify", blank_w=100*mm, label_w=60*mm))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Position type", styles['FieldLabel']))
    story.append(checkbox_grid(["Live-in", "Live-out", "Flexible"], columns=3))
    story.append(Spacer(1, 6))

    story.append(two_col_fields([
        ("Valid driver's licence?", False), ("Reliable transport?", False),
    ]))
    story.append(checkbox_grid(["No", "Yes"], columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Availability", styles['FieldLabel']))
    story.append(checkbox_grid(
        ["Full-time", "Part-time", "Temporary", "Weekend", "Night shifts", "Emergency"], columns=3
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Skills and experience *", styles['FieldLabel']))
    story.append(Paragraph(
        "Childcare, driving, special-needs care, cooking, household administration, pet care, etc.",
        styles['Notice']
    ))
    story.append(ruled_block(4))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Qualifications and training", styles['FieldLabel']))
    story.append(ruled_block(3))
    story.append(Spacer(1, 6))

    story.append(field_line("Languages spoken"))

    story.append(two_col_fields([
        ("Legally permitted to work in South Africa? *", False),
        ("Medically able to perform essential duties?", False),
    ]))
    story.append(checkbox_grid(["Yes", "No"], columns=2))
    story.append(Paragraph(
        "(For medical ability: Yes / No / Reasonable accommodation may be required)",
        styles['Notice']
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Screening consent", styles['FieldLabel']))
    story.append(checkbox_grid([
        "Identity verification", "Reference checks",
        "Qualification verification", "Criminal-record check where lawful and relevant",
    ], columns=2))
    story.append(Spacer(1, 10))

    story.append(checkbox_item(
        "I certify that the information supplied is true and complete, and authorise "
        "Origin Talent to verify information, contact references and conduct lawful background checks. *",
        170*mm
    ))
    story.append(Spacer(1, 3))
    story.append(checkbox_item(
        "I consent to the secure processing and storage of my personal information for "
        "recruitment and placement purposes, in accordance with the privacy notice. *",
        170*mm
    ))
    story.append(Paragraph(
        "Do not email or upload bank statements through an unsecured public channel. Banking "
        "information will only be requested when necessary, through an approved secure process.",
        styles['Notice']
    ))
    story.append(Spacer(1, 14))
    story.append(signature_block("Candidate signature"))

    story += footer_note(
        "Origin Talent — Candidate Application Form · Printable reference version of the online form."
    )
    return story


# ------------------------------------------------------------ document 3 ---
def build_service_agreement():
    story = letterhead("Client Service Agreement")

    draft_box = Table(
        [[Paragraph(
            "WORKING DRAFT — for discussion with your Origin Talent consultant. Final fees, terms "
            "and legal wording are confirmed with your consultant before signature.",
            ParagraphStyle('DraftNote', parent=styles['Body'], textColor=BLUE_DARK, fontName='Helvetica-Bold')
        )]],
        colWidths=[170*mm]
    )
    draft_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TINT),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(draft_box)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "This Service Agreement (“Agreement”) is made between <b>Origin Talent</b> "
        f"({ADDRESS}) (“Origin Talent”, “we”, “us”) and the client named "
        "below (“Client”), and sets out the terms on which Origin Talent sources and places "
        "domestic staff on the Client's behalf.",
        styles['Body']
    ))

    story.append(two_col_fields([("Client name", True), ("Company (if applicable)", False)]))
    story.append(two_col_fields([("Address", False), ("Contact number", True)]))
    story.append(field_line("Position(s) being filled", required=True))

    story.append(Paragraph("1. Services Provided", styles['SectionHead']))
    story.append(Paragraph(
        "Origin Talent will source, screen and present suitably qualified candidates for the "
        "position(s) specified above. Screening may include identity verification, reference checks, "
        "qualification verification, and criminal-record checks where lawful and relevant to the role. "
        "Screening is conducted on a best-efforts basis using information reasonably available to "
        "Origin Talent; it does not constitute a guarantee of a candidate's conduct, and the Client "
        "remains responsible for its own final due diligence before appointment.",
        styles['Body']
    ))

    story.append(Paragraph("2. Placement Fee", styles['SectionHead']))
    story.append(field_line("Placement fee", blank_w=100*mm, label_w=45*mm))
    story.append(field_line("Payment terms", blank_w=100*mm, label_w=45*mm))
    story.append(Paragraph(
        "Placement fees depend on the role and seniority required and are confirmed with the Client "
        "in writing (quotation or invoice) before a placement is confirmed. Fees are payable as set "
        "out in that written quotation; nothing in this Agreement fixes a fee amount.",
        styles['Body']
    ))

    story.append(Paragraph("3. Replacement Guarantee", styles['SectionHead']))
    story.append(Paragraph(
        "Should a placed candidate leave the role within ", styles['Body']
    ))
    story.append(field_line("Guarantee period (days)", blank_w=30*mm, label_w=55*mm))
    story.append(Paragraph(
        "of the placement start date, through no fault of the Client, Origin Talent will source a "
        "suitable replacement candidate at no additional placement fee, subject to the Client having "
        "met its obligations under this Agreement and the Sectoral Determination referred to below.",
        styles['Body']
    ))

    story.append(Paragraph("4. Client Obligations", styles['SectionHead']))
    story.append(Paragraph(
        "The Client will: (a) provide accurate and complete information about the role and its "
        "requirements; (b) ensure that any selection criteria are lawful, genuine and non-discriminatory; "
        "(c) enter into a compliant written contract of employment directly with any candidate appointed, "
        "in line with the Basic Conditions of Employment Act and Sectoral Determination 7 (Domestic "
        "Worker Sector); (d) register for and meet UIF and, where applicable, COIDA obligations as the "
        "candidate's employer; and (e) notify Origin Talent promptly if a placement ends.",
        styles['Body']
    ))

    story.append(Paragraph("5. Data Protection (POPIA)", styles['SectionHead']))
    story.append(Paragraph(
        "Both parties will process personal information shared under this Agreement — including "
        "candidate and Client contact details — in accordance with the Protection of Personal "
        "Information Act, 2013, and Origin Talent's privacy notice. Personal information will be used "
        "only for recruitment, placement and related administration, and retained only as long as "
        "reasonably necessary for those purposes.",
        styles['Body']
    ))

    story.append(Paragraph("6. Term and Termination", styles['SectionHead']))
    story.append(Paragraph(
        "This Agreement applies to the placement(s) described above and remains in effect until the "
        "engagement is concluded or either party terminates it in writing. Termination does not affect "
        "fees already due for placements made before the termination date.",
        styles['Body']
    ))

    story.append(Paragraph("7. Limitation of Liability", styles['SectionHead']))
    story.append(Paragraph(
        "Origin Talent's total liability under this Agreement is limited to the placement fee paid by "
        "the Client for the relevant placement. Origin Talent is not liable for any indirect or "
        "consequential loss arising from a placement.",
        styles['Body']
    ))

    story.append(Paragraph("8. Governing Law", styles['SectionHead']))
    story.append(Paragraph(
        "This Agreement is governed by the laws of the Republic of South Africa.",
        styles['Body']
    ))

    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "Agreed and accepted by the parties below.", styles['Body']
    ))
    story.append(Spacer(1, 6))

    sign_table = Table(
        [
            [Paragraph("<b>For the Client</b>", styles['Body']), Paragraph("<b>For Origin Talent</b>", styles['Body'])],
            [Paragraph("Signature: ____________________________", styles['Body']),
             Paragraph("Signature: ____________________________", styles['Body'])],
            [Paragraph("Name: ____________________________", styles['Body']),
             Paragraph("Name: ____________________________", styles['Body'])],
            [Paragraph("Date: ____________________________", styles['Body']),
             Paragraph("Date: ____________________________", styles['Body'])],
        ],
        colWidths=[85*mm, 85*mm]
    )
    sign_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(KeepTogether(sign_table))

    story += footer_note(
        "Origin Talent — Client Service Agreement (working draft) · Not valid until confirmed and "
        "signed with your Origin Talent consultant."
    )
    return story


def render(filename, story_fn):
    path = os.path.join(OUT_DIR, filename)
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        topMargin=16*mm, bottomMargin=14*mm, leftMargin=20*mm, rightMargin=20*mm,
        title=filename.replace('.pdf', '').replace('-', ' '),
        author="Origin Talent",
    )
    doc.build(story_fn())
    print("Wrote", path)


if __name__ == '__main__':
    render("Origin-Talent-Client-Staffing-Enquiry-Form.pdf", build_client_enquiry)
    render("Origin-Talent-Candidate-Application-Form.pdf", build_candidate_application)
    render("Origin-Talent-Client-Service-Agreement.pdf", build_service_agreement)
