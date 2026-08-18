#!/usr/bin/env python3
"""
Generates the three Document Centre PDFs linked from index.html:
  - Origin-Talent-Client-Staffing-Enquiry-Form.pdf
  - Origin-Talent-Candidate-Application-Form.pdf
  - Origin-Talent-Client-Service-Agreement.pdf

Source of truth for field lists/options/legal text is Origin Talent's own
source documents (Client_Staffing_Enquiry_Form__ONLINE_FORM_OT.docx,
Candidate_Online_Application_Form_OT.docx, CLIENT_SERVICE_AGREEMENT__
ORIGIN_TALENT.docx), cross-checked against the live online forms in
index.html (data-demo="client" / data-demo="candidate"). Where the two
disagree, the .docx wins here, since it's the client's authoritative
content — see README.md for the known differences from the live site.

If the source content changes, update the data below and re-run:

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
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    KeepTogether, ListFlowable, ListItem
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
# The Service Agreement source doc gives a separate admin/accounts address —
# used only on that document, per the source.
AGREEMENT_EMAIL = "admin@origintalent.co.za"
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
styles.add(ParagraphStyle('BulletBody', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=9.4, textColor=INK, leading=13))
styles.add(ParagraphStyle('Notice', parent=styles['Normal'], fontName='Helvetica-Oblique',
                           fontSize=8.4, textColor=INK_SOFT, leading=11.5))
styles.add(ParagraphStyle('Footer', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=7.6, textColor=INK_SOFT, alignment=TA_CENTER))


def letterhead(title, email=EMAIL):
    story = [
        Paragraph("ORIGIN TALENT", styles['Brand']),
        Paragraph("Exceptional People, Trusted in Your Home", styles['Tagline']),
        HRFlowable(width="100%", thickness=1.4, color=GOLD, spaceAfter=8),
        Paragraph(title, styles['DocTitle']),
        Spacer(1, 4),
        Paragraph(
            f"{ADDRESS} &nbsp;|&nbsp; {PHONE} &nbsp;|&nbsp; WhatsApp {WHATSAPP} &nbsp;|&nbsp; {email}",
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


def checkbox_list(options, col_width=170*mm):
    """Single-column checkbox list — for options whose labels are too long
    for a grid (e.g. the document-upload checklist)."""
    rows = [[checkbox_item(opt, col_width)] for opt in options]
    t = Table(rows, colWidths=[col_width])
    t.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
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


def bullet_list(items):
    return ListFlowable(
        [ListItem(Paragraph(item, styles['BulletBody']), spaceAfter=3) for item in items],
        bulletType='bullet', start='•', leftIndent=14, bulletFontSize=8,
    )


ROLE_OPTIONS = [
    "Au Pair", "Nanny", "Caregiver", "Registered Nurse", "Night Nurse",
    "House Manager", "Cleaner", "Chauffeur", "Babysitter",
    "Personal Assistant (Home & Office)", "Private Chef", "Pet Sitter", "Tutor / Governess",
]

EMPLOYMENT_TYPE_OPTIONS = [
    "Permanent (Full-time)", "Temporary Contract (Fixed term)",
    "Part-time (Selective days per week or a weekender)",
]
ARRANGEMENT_OPTIONS_ENQUIRY = ["Live-in", "Live-out"]
URGENCY_OPTIONS = ["Immediately (in 2–4 days)", "Within 1 week", "Within 1 month", "Flexible"]
SALARY_OPTIONS = [
    "R5 000 – R8 000", "R9 000 – R12 000", "R13 000 – R15 000", "R16 000+", "Open to discussion",
]
NATIONALITY_OPTIONS_ENQUIRY = ["South African", "Zimbabwean", "Lesotho", "Other"]
LANGUAGE_OPTIONS = ["English", "Zulu", "Afrikaans", "Xhosa", "Sotho", "Tswana", "Other"]

AVAILABILITY_OPTIONS = [
    "Full-time", "Part-time", "Temporary", "Weekend work", "Night shifts", "Emergency placements",
]
POSITION_TYPE_OPTIONS = ["Live-in", "Live-out", "Flexible"]
SCREENING_OPTIONS = [
    "Criminal background checks", "Identity verification",
    "Qualification verification", "Reference checks",
]
UPLOAD_CHECKLIST = [
    "Recent photograph (must be professional and look neat)",
    "Curriculum Vitae (CV)",
    "Copy of ID or passport, with a valid work permit if applicable",
    "Contactable reference letter from your previous employer",
    "Bank statement in your name (serves as proof of residence and bank account confirmation)",
    "Driver's licence (if applicable)",
    "Certificates / qualifications (if available)",
    "Police clearance certificate (if available, must be less than 6 months old)",
]


# ------------------------------------------------------------ document 1 ---
def build_client_enquiry():
    story = letterhead("Client Staffing Enquiry Form")
    story.append(Paragraph(
        "Find the Perfect Household Professional — complete the form below and one of our "
        "recruitment consultants will contact you within 24 hours to discuss your requirements. "
        f"Fields marked * are required. For the fastest response, submit online at {SITE} or "
        f"WhatsApp {WHATSAPP}.",
        styles['Instructions']
    ))

    story.append(Paragraph("Contact Information", styles['SectionHead']))
    story.append(field_line("Full name", required=True))
    story.append(field_line("Company name (if applicable)"))
    story.append(two_col_fields([
        ("Email address", True), ("Mobile number", True),
    ]))
    story.append(two_col_fields([
        ("Alternative contact number", False), ("Home address", False),
    ]))

    story.append(Paragraph("Preferred method of contact", styles['FieldLabel']))
    story.append(checkbox_grid(["Phone", "Email", "WhatsApp"], columns=3))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Position required *", styles['FieldLabel']))
    story.append(checkbox_grid(ROLE_OPTIONS, columns=3))
    story.append(field_line("If other, please specify", blank_w=100*mm, label_w=60*mm))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Candidate nationality", styles['FieldLabel']))
    story.append(checkbox_grid(NATIONALITY_OPTIONS_ENQUIRY, columns=4))
    story.append(field_line("If other, please specify", blank_w=100*mm, label_w=60*mm))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Employment type", styles['FieldLabel']))
    story.append(checkbox_grid(EMPLOYMENT_TYPE_OPTIONS, columns=1))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Type", styles['FieldLabel']))
    story.append(checkbox_grid(ARRANGEMENT_OPTIONS_ENQUIRY, columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Days required", styles['FieldLabel']))
    story.append(checkbox_grid(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], columns=4
    ))
    story.append(Spacer(1, 6))

    story.append(field_line("Working hours"))

    story.append(Paragraph("How urgently do you require placement?", styles['FieldLabel']))
    story.append(checkbox_grid(URGENCY_OPTIONS, columns=2))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Please describe the duties and responsibilities *", styles['FieldLabel']))
    story.append(ruled_block(4))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Expected monthly salary range", styles['FieldLabel']))
    story.append(checkbox_grid(SALARY_OPTIONS, columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Driving required", styles['FieldLabel']))
    story.append(checkbox_grid(["Yes", "No"], columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Language requirements", styles['FieldLabel']))
    story.append(checkbox_grid(LANGUAGE_OPTIONS, columns=4))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Additional notes", styles['FieldLabel']))
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

    story.append(Paragraph("Personal Information", styles['SectionHead']))
    story.append(field_line("Full name", required=True))
    story.append(two_col_fields([
        ("Date of birth", True), ("ID / passport number", True),
    ]))
    story.append(two_col_fields([
        ("Gender", False), ("Nationality", False),
    ]))
    story.append(field_line("Residential address", required=True))
    story.append(two_col_fields([
        ("Province / state", False), ("Mobile number", True),
    ]))
    story.append(two_col_fields([
        ("Email address", True), ("Next of kin — name", False),
    ]))
    story.append(field_line("Next of kin — number"))

    story.append(Paragraph("Do you have a valid driver's licence?", styles['FieldLabel']))
    story.append(checkbox_grid(["Yes", "No"], columns=2))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Do you own reliable transportation?", styles['FieldLabel']))
    story.append(checkbox_grid(["Yes", "No"], columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Position applying for *", styles['FieldLabel']))
    story.append(checkbox_grid(ROLE_OPTIONS, columns=3))
    story.append(field_line("If other, please specify", blank_w=100*mm, label_w=60*mm))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Are you available for:", styles['FieldLabel']))
    story.append(checkbox_grid(AVAILABILITY_OPTIONS, columns=3))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Position type", styles['FieldLabel']))
    story.append(checkbox_grid(POSITION_TYPE_OPTIONS, columns=3))
    story.append(Spacer(1, 8))

    story.append(Paragraph("List your skills per your experience *", styles['FieldLabel']))
    story.append(Paragraph(
        "e.g. Driving, childcare, special-needs care, professional cooking, household "
        "administration, pet care, event preparation, report writing, etc.",
        styles['Notice']
    ))
    story.append(ruled_block(4))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Qualifications (list any tertiary, certificates or training)", styles['FieldLabel']))
    story.append(ruled_block(3))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Languages (list all languages that you can speak)", styles['FieldLabel']))
    story.append(ruled_block(2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Have you ever been convicted of a criminal offence?", styles['FieldLabel']))
    story.append(checkbox_grid(["Yes", "No"], columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Are you willing to undergo:", styles['FieldLabel']))
    story.append(checkbox_grid(SCREENING_OPTIONS, columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Are you medically fit to perform household duties?", styles['FieldLabel']))
    story.append(checkbox_grid(["Yes", "No"], columns=2))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Are you legally permitted to work in this country?", styles['FieldLabel']))
    story.append(checkbox_grid(["Yes", "No"], columns=2))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Documents to attach", styles['SectionHead']))
    story.append(Paragraph(
        "Please attach copies of the following when submitting this form:",
        styles['Body']
    ))
    story.append(checkbox_list(UPLOAD_CHECKLIST))
    story.append(Paragraph(
        "Do not send banking or identity documents through an unsecured public channel — hand "
        "these to your Origin Talent consultant directly or via an approved secure process.",
        styles['Notice']
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Declaration", styles['SectionHead']))
    story.append(Paragraph(
        "By submitting this form, you agree to the below:", styles['Body']
    ))
    story.append(bullet_list([
        "I certify that the information provided in this application is true, complete, and "
        "accurate to the best of my knowledge.",
        "I understand that providing false or misleading information may result in the rejection "
        "of my application or termination of employment if placed.",
        "I authorise the agency to verify the information provided, contact my references, and "
        "conduct background and identity checks where applicable.",
        "I consent to the processing and secure storage of my personal information for "
        "recruitment and placement purposes in accordance with applicable privacy and data "
        "protection laws.",
    ]))
    story.append(Spacer(1, 10))
    story.append(signature_block("Candidate signature"))

    story += footer_note(
        "Origin Talent — Candidate Application Form · Printable reference version of the online form."
    )
    return story


# ------------------------------------------------------------ document 3 ---
def party_table(rows):
    t = Table(rows, colWidths=[38*mm, 132*mm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.4),
        ('TEXTCOLOR', (0, 0), (0, -1), INK),
        ('LINEBELOW', (1, 0), (1, -1), 0.7, LINE),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ]))
    return t


def build_service_agreement():
    story = letterhead("Client Service Agreement", email=AGREEMENT_EMAIL)

    story.append(Paragraph(
        "This document is a template — complete the details below and review with your "
        "Origin Talent consultant before signature.",
        ParagraphStyle('DraftNote', parent=styles['Notice'], textColor=BLUE_DARK)
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        'This Client Service Agreement ("Agreement") is entered into by:',
        styles['Body']
    ))
    story.append(party_table([
        [Paragraph("Business Name:", styles['FieldLabel']), Paragraph("Origin Talent", styles['Body'])],
        [Paragraph("Registration Number:", styles['FieldLabel']), ''],
        [Paragraph("Address:", styles['FieldLabel']), Paragraph(ADDRESS, styles['Body'])],
        [Paragraph("Telephone:", styles['FieldLabel']), Paragraph(PHONE, styles['Body'])],
        [Paragraph("Email:", styles['FieldLabel']), Paragraph(AGREEMENT_EMAIL, styles['Body'])],
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("AND", ParagraphStyle('And', parent=styles['Body'], alignment=TA_CENTER, fontName='Helvetica-Bold')))
    story.append(Spacer(1, 6))
    story.append(party_table([
        [Paragraph("Full Name:", styles['FieldLabel']), ''],
        [Paragraph("ID Number:", styles['FieldLabel']), ''],
        [Paragraph("Address:", styles['FieldLabel']), ''],
        [Paragraph("Telephone:", styles['FieldLabel']), ''],
        [Paragraph("Email:", styles['FieldLabel']), ''],
    ]))
    story.append(Spacer(1, 4))

    def clause(number, title, body=None, bullets=None):
        story.append(Paragraph(f"{number}. {title}", styles['SectionHead']))
        if body:
            for p in (body if isinstance(body, list) else [body]):
                story.append(Paragraph(p, styles['Body']))
        if bullets:
            story.append(bullet_list(bullets))

    clause(1, "Appointment", [
        "1.1 The Client appoints the Staffing Agency to recruit, screen, and supply temporary, "
        "contract, fixed-term, or permanent employees according to the Client's staffing "
        "requirements.",
        "1.2 The Staffing Agency accepts the appointment subject to the terms and conditions "
        "contained in this Agreement.",
    ])

    clause(2, "Services Provided",
           "2.1 The Staffing Agency shall provide one or more of the following services:",
           bullets=[
               "Recruitment and selection of employees.",
               "Candidate interviews and screening.",
               "Qualification verification where applicable.",
               "Reference checking.",
               "Criminal and credit checks where legally permissible and authorised.",
               "Temporary Employment Services (TES).",
               "Contract staffing.",
               "Permanent placements.",
               "Payroll administration (where applicable).",
               "HR support services.",
           ])

    clause(3, "Client Responsibilities",
           "3.1 The Client undertakes to:",
           bullets=[
               "Provide accurate job descriptions.",
               "Inform the Staffing Agency of all required qualifications, skills, experience, "
               "and medical or legal requirements relevant to the role.",
               "Maintain a safe workplace in accordance with the Occupational Health and Safety Act.",
               "Ensure fair treatment of assigned employees.",
               "Supervise employees during assignments.",
               "Notify the Staffing Agency immediately of any workplace incidents, misconduct, "
               "absenteeism, disciplinary issues, or injuries.",
               "Allow the Staffing Agency reasonable access to employees where necessary.",
           ])

    clause(4, "Fees and Payment", [
        "4.1 The Client agrees to pay all invoices issued by the Staffing Agency.",
        "4.2 Unless otherwise agreed:",
    ], bullets=[
        "Payment terms are strictly 30 days from the date of invoice.",
        "Interest may be charged on overdue accounts at the maximum rate permitted by law.",
        "Collection costs and legal fees incurred in recovering unpaid accounts shall be for "
        "the Client's account.",
    ])

    clause(5, "Temporary Employment Services (TES)",
           "5.1 Where employees are supplied on a temporary basis:",
           bullets=[
               "The Staffing Agency remains the employer for payroll purposes unless otherwise agreed.",
               "The Client shall supervise the employees during working hours.",
               "The Client shall comply with all obligations imposed by the Labour Relations Act "
               "regarding Temporary Employment Services.",
               "The Client shall not require employees to perform unlawful or unsafe work.",
           ])

    clause(6, "Permanent Placements", [
        "6.1 Permanent placement fees become payable immediately once a candidate accepts employment.",
        "6.2 Should the Client employ a candidate introduced by the Staffing Agency within twelve "
        "(12) months of introduction, the agreed placement fee shall remain payable.",
    ])

    clause(7, "Replacement Guarantee",
           "7.1 Where a permanent employee resigns or is lawfully dismissed for poor performance "
           "within the first ninety (90) days of employment, the Staffing Agency shall make "
           "reasonable efforts to provide one replacement candidate at no additional recruitment "
           "fee, provided:",
           bullets=[
               "The original invoice has been paid in full.",
               "The Client followed a fair probation process.",
               "The employee was not dismissed due to redundancy or restructuring.",
           ])

    clause(8, "Confidentiality", [
        "8.1 Both Parties agree to keep confidential all information relating to:",
    ], bullets=[
        "Business operations.", "Clients.", "Candidates.", "Pricing.",
        "Trade secrets.", "Recruitment processes.",
    ])
    story.append(Paragraph(
        "8.2 Such information shall not be disclosed except where required by law.", styles['Body']
    ))

    clause(9, "Protection of Personal Information (POPIA)", [
        "9.1 Both Parties undertake to comply with the Protection of Personal Information Act, 2013.",
        "9.2 The Client agrees that:",
    ], bullets=[
        "Candidate information shall be used solely for recruitment purposes.",
        "Candidate information shall not be shared with third parties without lawful authority.",
        "Personal information shall be securely stored.",
        "Personal information shall be destroyed when no longer required.",
    ])

    clause(10, "Non-Solicitation",
           "10.1 The Client agrees not to employ, directly or indirectly, any employee or "
           "candidate introduced by the Staffing Agency without paying the applicable placement "
           "fee if such employment occurs within twelve (12) months of the introduction.")

    clause(11, "Liability", [
        "11.1 The Staffing Agency exercises reasonable care when recruiting employees.",
        "11.2 However:",
    ], bullets=[
        "The final hiring decision rests solely with the Client.",
        "The Staffing Agency does not guarantee employee performance.",
        "The Staffing Agency shall not be liable for any indirect or consequential losses "
        "arising from the actions of supplied employees except where required by law.",
    ])

    clause(12, "Health and Safety",
           "12.1 The Client shall:",
           bullets=[
               "Provide a safe working environment.",
               "Conduct workplace induction where required.",
               "Supply necessary protective clothing and equipment.",
               "Report workplace injuries immediately.",
               "Comply with the Occupational Health and Safety Act.",
           ])

    clause(13, "Dispute Resolution", [
        "13.1 Any dispute arising from this Agreement shall first be resolved through negotiation.",
        "13.2 If unresolved within fourteen (14) days, the Parties may refer the dispute to "
        "mediation or arbitration before approaching a court of competent jurisdiction.",
    ])

    clause(14, "Termination", [
        "14.1 Either Party may terminate this Agreement by giving thirty (30) days' written notice.",
        "14.2 Termination shall not affect:",
    ], bullets=[
        "Outstanding payments.", "Confidentiality obligations.", "Any rights accrued before termination.",
    ])

    clause(15, "Governing Law",
           "15.1 This Agreement shall be governed by the laws of the Republic of South Africa.")

    clause(16, "Entire Agreement", [
        "16.1 This document constitutes the entire agreement between the Parties.",
        "16.2 No amendment shall be valid unless reduced to writing and signed by both Parties.",
    ])

    story.append(Spacer(1, 12))
    story.append(field_line("Signed at", blank_w=100*mm, label_w=45*mm))
    story.append(Spacer(1, 10))

    sign_agency = Table(
        [
            [Paragraph("<b>For the Staffing Agency</b>", styles['Body']), ''],
            [Paragraph("Business Name:", styles['FieldLabel']), Paragraph("Origin Talent", styles['Body'])],
            [Paragraph("Representative:", styles['FieldLabel']), ''],
            [Paragraph("Position:", styles['FieldLabel']), ''],
            [Paragraph("Signature:", styles['FieldLabel']), ''],
            [Paragraph("Date:", styles['FieldLabel']), ''],
        ],
        colWidths=[38*mm, 132*mm]
    )
    sign_agency.setStyle(TableStyle([
        ('LINEBELOW', (1, 1), (1, -1), 0.7, LINE),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('SPAN', (0, 0), (1, 0)),
    ]))
    story.append(KeepTogether(sign_agency))
    story.append(Spacer(1, 10))

    sign_client = Table(
        [
            [Paragraph("<b>For the Client</b>", styles['Body']), ''],
            [Paragraph("Full Name:", styles['FieldLabel']), ''],
            [Paragraph("Position:", styles['FieldLabel']), ''],
            [Paragraph("Signature:", styles['FieldLabel']), ''],
            [Paragraph("Date:", styles['FieldLabel']), ''],
        ],
        colWidths=[38*mm, 132*mm]
    )
    sign_client.setStyle(TableStyle([
        ('LINEBELOW', (1, 1), (1, -1), 0.7, LINE),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('SPAN', (0, 0), (1, 0)),
    ]))
    story.append(KeepTogether(sign_client))

    story += footer_note(
        "Origin Talent — Client Service Agreement · Template document, not valid until "
        "completed and signed by both parties."
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
