from pathlib import Path
import shutil
import subprocess
import sys
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
ASSETS = ROOT / "tmp" / "pdfs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

if not (ASSETS / "vellitas-logo-on-dark.png").exists():
    converter = shutil.which("rsvg-convert")
    if not converter:
        raise RuntimeError("rsvg-convert is required to build the report assets")
    conversions = [
        (ROOT / "assets" / "vellitas-logo-on-dark.svg", ASSETS / "vellitas-logo-on-dark.png", 906, 225),
        (ROOT / "assets" / "vellitas-shield-blue.svg", ASSETS / "shield-blue.png", 184, 216),
        (ROOT / "assets" / "vellitas-shield-green.svg", ASSETS / "shield-green.png", 184, 216),
        (ROOT / "assets" / "vellitas-shield-yellow.svg", ASSETS / "shield-yellow.png", 184, 216),
        (ROOT / "assets" / "vellitas-shield-red.svg", ASSETS / "shield-red.png", 184, 216),
    ]
    for source, target, width, height in conversions:
        subprocess.run(
            [converter, "-w", str(width), "-h", str(height), str(source), "-o", str(target)],
            check=True,
        )

PAGE_W, PAGE_H = letter
M = 48

BG = HexColor("#020B14")
BG_DEEP = HexColor("#01070D")
SURFACE = HexColor("#071827")
SURFACE_2 = HexColor("#0A1E2F")
TEXT = HexColor("#F5F8FB")
MUTED = HexColor("#A7B4C5")
MUTED_2 = HexColor("#C7D1DC")
CYAN = HexColor("#25D8F5")
CYAN_SOFT = HexColor("#8DEAFA")
BLUE = HexColor("#0F75BC")
GREEN = HexColor("#34D399")
YELLOW = HexColor("#F5C451")
RED = HexColor("#FF6A2A")
LINE = HexColor("#174158")
WHITE_06 = Color(1, 1, 1, alpha=0.06)

LOGO = ImageReader(str(ASSETS / "vellitas-logo-on-dark.png"))
SHIELDS = {
    "blue": ImageReader(str(ASSETS / "shield-blue.png")),
    "green": ImageReader(str(ASSETS / "shield-green.png")),
    "yellow": ImageReader(str(ASSETS / "shield-yellow.png")),
    "red": ImageReader(str(ASSETS / "shield-red.png")),
}


def pstyle(size=10, leading=None, color=MUTED, font="Helvetica", align=TA_LEFT, space_after=0):
    return ParagraphStyle(
        "custom",
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.42,
        textColor=color,
        alignment=align,
        spaceAfter=space_after,
        allowWidows=0,
        allowOrphans=0,
    )


def para(c, text, x, y, w, size=10, leading=None, color=MUTED, font="Helvetica", align=TA_LEFT):
    story = Paragraph(text, pstyle(size, leading, color, font, align))
    _, h = story.wrap(w, PAGE_H)
    story.drawOn(c, x, y - h)
    return y - h


def fill_page(c, color=BG):
    c.setFillColor(color)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def line(c, x1, y1, x2, y2, color=LINE, width=0.7):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def rounded(c, x, y, w, h, fill=SURFACE, stroke=LINE, radius=8, width=0.8):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def tag(c, text, x, y, color=CYAN, fill=SURFACE_2):
    tw = stringWidth(text.upper(), "Helvetica-Bold", 7.5) + 18
    c.setFillColor(fill)
    c.setStrokeColor(color)
    c.setLineWidth(0.6)
    c.roundRect(x, y - 14, tw, 18, 9, fill=1, stroke=1)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 9, y - 8.5, text.upper())
    return tw


def header(c, page_num, section, prototype="CURRENT CAPABILITY"):
    c.drawImage(LOGO, M, PAGE_H - 55, width=145, height=36, mask="auto", preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(CYAN)
    c.drawRightString(PAGE_W - M, PAGE_H - 31, prototype)
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - M, PAGE_H - 43, section.upper())
    line(c, M, PAGE_H - 66, PAGE_W - M, PAGE_H - 66)
    footer(c, page_num, prototype)


def footer(c, page_num, prototype):
    line(c, M, 35, PAGE_W - M, 35, color=LINE, width=0.45)
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawString(M, 22, "VELLITAS, LLC | CONFIDENTIAL DESIGN PROTOTYPE")
    c.drawCentredString(PAGE_W / 2, 22, prototype)
    c.drawRightString(PAGE_W - M, 22, f"{page_num:02d}")


def title(c, eyebrow, heading, deck=None, y=PAGE_H - 104):
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(CYAN)
    c.drawString(M, y, eyebrow.upper())
    y -= 24
    y = para(c, heading, M, y, PAGE_W - 2 * M, size=25, leading=29, color=TEXT, font="Helvetica-Bold")
    if deck:
        y -= 13
        y = para(c, deck, M, y, PAGE_W - 2 * M, size=10.5, leading=15, color=MUTED_2)
    return y


def metric(c, x, y, w, h, label, value, note="", accent=CYAN):
    rounded(c, x, y, w, h)
    c.setFillColor(accent)
    c.rect(x, y + h - 3, w, 3, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(MUTED)
    c.drawString(x + 15, y + h - 23, label.upper())
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(TEXT)
    c.drawString(x + 15, y + h - 55, str(value))
    if note:
        para(c, note, x + 15, y + 24, w - 30, size=7.5, leading=9.5, color=MUTED)


def section_card(c, x, y, w, h, heading, body, accent=CYAN, label=None):
    rounded(c, x, y, w, h)
    c.setFillColor(accent)
    c.rect(x, y, 3, h, fill=1, stroke=0)
    top = y + h - 20
    if label:
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(accent)
        c.drawString(x + 18, top, label.upper())
        top -= 18
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(TEXT)
    c.drawString(x + 18, top, heading)
    para(c, body, x + 18, top - 13, w - 36, size=8.5, leading=12, color=MUTED)


def status_row(c, y, label, count, severity, color, total):
    c.setFillColor(MUTED_2)
    c.setFont("Helvetica", 9)
    c.drawString(M, y, label)
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(356, y, f"{count:,}")
    x_bar = 375
    w_bar = 150
    c.setFillColor(SURFACE_2)
    c.roundRect(x_bar, y - 2, w_bar, 7, 3.5, fill=1, stroke=0)
    ratio = min(count / total, 1)
    c.setFillColor(color)
    c.roundRect(x_bar, y - 2, max(4, w_bar * ratio), 7, 3.5, fill=1, stroke=0)
    tag(c, severity, 535, y + 4, color=color, fill=BG)


def cover(c, subtitle, title_text, deck, version, shield="blue", roadmap=False):
    fill_page(c, BG_DEEP)
    c.drawImage(LOGO, M, PAGE_H - 74, width=184, height=46, mask="auto", preserveAspectRatio=True)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.circle(PAGE_W - 60, 80, 230, fill=0, stroke=1)
    c.circle(PAGE_W - 60, 80, 175, fill=0, stroke=1)
    c.circle(PAGE_W - 60, 80, 120, fill=0, stroke=1)
    c.setFillColor(Color(0.145, 0.847, 0.961, alpha=0.04))
    c.circle(PAGE_W - 60, 80, 240, fill=1, stroke=0)
    c.drawImage(SHIELDS[shield], PAGE_W - 168, 72, width=92, height=108, mask="auto", preserveAspectRatio=True)
    tag(c, subtitle, M, PAGE_H - 145, color=CYAN)
    y = PAGE_H - 196
    y = para(c, title_text, M, y, 470, size=34, leading=38, color=TEXT, font="Helvetica-Bold")
    y -= 22
    y = para(c, deck, M, y, 430, size=12, leading=18, color=MUTED_2)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(CYAN)
    c.drawString(M, 96, version.upper())
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(M, 80, "Prepared by Vellitas, LLC")
    c.drawString(M, 65, "September 2026")
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(RED if not roadmap else YELLOW)
    c.drawString(M, 42, "CONFIDENTIAL - DESIGN PROTOTYPE - NOT A FRESH SECURITY ASSESSMENT")
    c.showPage()


def current_report(path):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Vellitas Current Capability Assessment - Syntheticized Report Redesign")
    c.setAuthor("Vellitas, LLC")
    cover(
        c,
        "Current capability report",
        "Outside-In Certificate Risk Assessment",
        "A real-world-informed assessment redesigned as a synthetic enterprise dataset. Names, domains, IP addresses, dates, geography, counts, and evidence rows have been altered while realistic security relationships and analytical meaning are retained.",
        "Real-world-informed synthetic dataset | Illustrative enterprise",
        shield="blue",
    )

    # Page 2
    fill_page(c); header(c, 2, "Executive assessment")
    y = title(c, "Executive view", "The exposed certificate estate contains material, externally observable risk.",
              "This syntheticized portfolio demonstrates discovery, enrichment, policy comparison, prioritization, and corrective guidance at global scale. Metrics were altered to prevent attribution while preserving plausible cross-category relationships.")
    card_w = (PAGE_W - 2 * M - 18) / 2
    metric(c, M, y - 103, card_w, 86, "Certificates discovered", "38,640", "Internet-visible certificates associated with approved markers.", CYAN)
    metric(c, M + card_w + 18, y - 103, card_w, 86, "Weak protocols", "8,912", "Hosts presenting legacy encryption protocols.", RED)
    metric(c, M, y - 207, card_w, 86, "Self-signed", "6,284", "Certificates without third-party trust validation.", YELLOW)
    metric(c, M + card_w + 18, y - 207, card_w, 86, "Weak signing", "9,476", "24.5% used SHA-1 or weaker algorithms.", RED)
    y2 = y - 242
    section_card(c, M, y2 - 112, PAGE_W - 2 * M, 112, "Executive conclusion",
                 "The portfolio requires a coordinated remediation program, not isolated certificate replacement. First establish ownership and business need, then correct cryptographic defects, retire forgotten endpoints, and verify each change from the outside. Geographic and name anomalies require customer validation before they are treated as compromise.", RED, "Action required")
    c.showPage()

    # Page 3
    fill_page(c); header(c, 3, "Scope and method")
    y = title(c, "Observed from the outside", "What the real-world-informed model demonstrates.",
              "The report documents a repeatable process that starts with approved customer markers and ends with prioritized evidence and recommended corrective work.")
    items = [
        ("Discover", "Search internet-visible certificate deployments associated with domains, names, IP ranges, and other approved identifiers."),
        ("Enrich", "Attach IP, country, certificate authority, serial number, signature algorithm, validity, key strength, and presented protocol."),
        ("Compare", "Evaluate observed issuance, location, lifetime, environment markers, protocol, cipher, and certificate properties against expectations."),
        ("Prioritize", "Surface anomalous geography, name encroachment, self-signed, expired, near-expiry, weak-key, weak-signature, wildcard, and non-production exposure."),
        ("Recommend", "Provide corrective actions, ownership questions, revocation or renewal guidance, and a focused evidence appendix."),
    ]
    yy = y - 24
    for i, (h, b) in enumerate(items, 1):
        c.setFillColor(CYAN)
        c.circle(M + 14, yy - 9, 13, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(M + 14, yy - 12, f"{i:02d}")
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(TEXT)
        c.drawString(M + 42, yy - 4, h)
        para(c, b, M + 42, yy - 15, PAGE_W - 2 * M - 42, size=8.5, leading=12, color=MUTED)
        yy -= 82
    rounded(c, M, 60, PAGE_W - 2 * M, 82, fill=SURFACE_2)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(CYAN); c.drawString(M + 16, 121, "OBSERVATION BOUNDARY")
    para(c, "The report is based on public-facing certificate and TLS evidence. It does not prove ownership, internal configuration, compromise, or business legitimacy without customer confirmation and separately authorized investigation.", M + 16, 108, PAGE_W - 2 * M - 32, size=8.5, leading=12, color=MUTED_2)
    c.showPage()

    # Page 4
    fill_page(c); header(c, 4, "Portfolio status")
    y = title(c, "Prioritized portfolio", "Observed conditions, ranked for investigation.",
              "Counts may overlap because one certificate can present multiple conditions. Severity should be calibrated using asset criticality, customer policy, and corroborating evidence.")
    total = 38640
    rows = [
        ("Weak signing algorithm", 9476, "Immediate", RED),
        ("Weak encryption protocol", 8912, "Immediate", RED),
        ("Weak key (<2048-bit)", 7305, "Immediate", RED),
        ("Self-signed certificate", 6284, "Investigate", RED),
        ("Wildcard certificate", 5842, "Review", YELLOW),
        ("Non-production marker", 4116, "Investigate", YELLOW),
        ("Expiring within 90 days", 2893, "Plan", YELLOW),
        ("Expired certificate", 683, "Immediate", RED),
    ]
    yy = y - 42
    for row in rows:
        status_row(c, yy, *row, total=total)
        yy -= 48
    section_card(c, M, 62, PAGE_W - 2 * M, 74, "Interpretation",
                 "The syntheticized portfolio models 6.8% weak cipher-suite use and a multi-authority issuance profile. The report separates observed facts from investigative hypotheses and assigns validation before remediation.", CYAN)
    c.showPage()

    # Page 5
    fill_page(c); header(c, 5, "Geospatial distribution")
    y = title(c, "Location is context, not proof.", "This illustrative distribution demonstrates country-level geospatial enrichment and flags locations outside the expected operating pattern for customer review.")
    countries = [("United States", 9620), ("Germany", 5180), ("Netherlands", 3740), ("United Kingdom", 3260), ("Singapore", 2950), ("Canada", 2380), ("Brazil", 2060), ("Australia", 1820), ("Japan", 1540), ("South Africa", 1180)]
    maxv = countries[0][1]
    yy = y - 30
    for idx, (name, val) in enumerate(countries):
        c.setFont("Helvetica", 8.5); c.setFillColor(MUTED_2); c.drawString(M, yy, name)
        c.setFont("Helvetica-Bold", 8.5); c.setFillColor(TEXT); c.drawRightString(M + 188, yy, f"{val:,}")
        bx = M + 205; bw = 275
        c.setFillColor(SURFACE_2); c.roundRect(bx, yy - 1, bw, 7, 3.5, fill=1, stroke=0)
        c.setFillColor(CYAN if idx < 2 else BLUE); c.roundRect(bx, yy - 1, bw * val / maxv, 7, 3.5, fill=1, stroke=0)
        yy -= 32
    section_card(c, M, 78, PAGE_W - 2 * M, 112, "Investigation rule",
                 "A new or unusual country raises priority only when it conflicts with customer expectations or is corroborated by certificate, DNS, ASN, provider, issuer, naming, or historical evidence. Cloud delivery, CDNs, outsourcing, disaster recovery, and acquisitions can all create legitimate geographic changes.", YELLOW, "Customer validation required")
    c.showPage()

    # Page 6
    fill_page(c); header(c, 6, "Name and domain encroachment")
    y = title(c, "Names that resemble the organization deserve review.", "This syntheticized assessment demonstrates organization-name, domain, and proximal-name discovery across internet-visible certificates.")
    examples = [
        ("typo-brand.example", "Certificate text used a one-character variation of the enterprise name", "Possible character substitution or unrelated naming."),
        ("weather-provider.example", "mobile-brand.weather-provider.example", "Possible authorized third-party service."),
        ("managed-service.example", "DDN_GlobalEnterprise_IBW.managed-service.example", "Possible outsourcing or technology partner."),
    ]
    yy = y - 24
    for i, (domain, evidence, interpretation) in enumerate(examples, 1):
        rounded(c, M, yy - 94, PAGE_W - 2 * M, 82)
        c.setFillColor(CYAN); c.setFont("Helvetica-Bold", 8); c.drawString(M + 16, yy - 18, f"CANDIDATE {i:02d}")
        c.setFillColor(TEXT); c.setFont("Helvetica-Bold", 12); c.drawString(M + 112, yy - 18, domain)
        para(c, f"<b>Observed naming:</b> {evidence}<br/><b>Working interpretation:</b> {interpretation}", M + 112, yy - 31, PAGE_W - 2 * M - 128, size=8.5, leading=12, color=MUTED)
        yy -= 106
    section_card(c, M, 83, PAGE_W - 2 * M, 120, "Required decision path",
                 "Confirm whether the domain and certificate belong to the customer, an approved vendor, an unrelated organization, or a deceptive actor. Approved dependencies should be added to the governed inventory. Suspicious issuance should be investigated with the issuer and, when justified, revoked or reported through the appropriate process.", RED, "Do not infer compromise from similarity alone")
    c.showPage()

    # Page 7
    fill_page(c); header(c, 7, "Trust and issuance")
    y = title(c, "Certificate authority and self-signed exposure.", "The syntheticized dataset inventories issuer families and distinguishes public trust from self-signed certificate deployments.")
    metric(c, M, y - 100, 155, 82, "Issuer families", "14", "Public, private, and self-signed trust patterns.", CYAN)
    metric(c, M + 170, y - 100, 155, 82, "Public CA families", "10", "Illustrative portfolio count.", GREEN)
    metric(c, M + 340, y - 100, 155, 82, "Self-signed", "6,284", "Requires ownership and purpose review.", RED)
    yy = y - 138
    section_card(c, M, yy - 126, 244, 126, "Current analytical value",
                 "Unexpected issuers, inconsistent trust patterns, and large self-signed populations can identify policy drift, default appliance certificates, unmanaged services, or incorrect ownership assumptions.", CYAN)
    section_card(c, M + 262, yy - 126, 244, 126, "Required customer context",
                 "Self-signed does not automatically mean malicious. Private appliances, lab systems, and controlled service-to-service uses may be legitimate, but public exposure still requires validation and policy alignment.", YELLOW)
    section_card(c, M, 82, PAGE_W - 2 * M, 124, "Modern reporting treatment",
                 "Record issuer, serial number, subject and SANs, validity, fingerprint, public-key hash, chain status, endpoint, observation time, and policy result. Tie each finding to an approved issuer list and a specific remediation or documented exception.", GREEN, "Evidence before conclusion")
    c.showPage()

    # Page 8
    fill_page(c); header(c, 8, "Certificate lifecycle")
    y = title(c, "Expiration and validity require ownership decisions.", "The report demonstrates expired, near-expiry, and long-validity analysis using internally consistent syntheticized lifecycle buckets.")
    metric(c, M, y - 102, 155, 84, "Already expired", "683", "Immediate ownership and service-need decision.", RED)
    metric(c, M + 170, y - 102, 155, 84, "Expire in 90 days", "2,893", "Renew, replace, or decommission.", YELLOW)
    metric(c, M + 340, y - 102, 155, 84, "Over 2 years", "1,942", "Illustrative long-validity count.", YELLOW)
    yy = y - 142
    section_card(c, M, yy - 130, PAGE_W - 2 * M, 130, "Validity distribution",
                 "The syntheticized portfolio contains 1,942 certificates with validity beyond two years, including 312 beyond five years and 46 beyond ten years. Production reports recalculate nested buckets from raw observations and prevent contradictory totals from entering executive decisioning.", RED, "Validation built in")
    section_card(c, M, 77, 244, 124, "If the service is required",
                 "Assign an owner, replace the certificate with an approved profile, confirm complete chain presentation, and establish renewal monitoring.", GREEN)
    section_card(c, M + 262, 77, 244, 124, "If the service is not required",
                 "Remove DNS, revoke the certificate where appropriate, decommission the service, and verify that the endpoint is no longer reachable.", CYAN)
    c.showPage()

    # Page 9
    fill_page(c); header(c, 9, "Cryptographic posture")
    y = title(c, "Weak cryptography is known exploitable exposure.", "The assessment demonstrates key-strength, signature-algorithm, protocol, and cipher-suite evaluation. A finding is mapped to current policy; it is not presented as proof that exploitation occurred.")
    metric(c, M, y - 100, 155, 82, "Weak key", "7,305", "Certificates below the 2048-bit threshold.", RED)
    metric(c, M + 170, y - 100, 155, 82, "Weak signature", "9,476", "SHA-1 or weaker in the illustrative portfolio.", RED)
    metric(c, M + 340, y - 100, 155, 82, "Weak ciphers", "6.8%", "Illustrative portfolio percentage.", YELLOW)
    yy = y - 140
    status_row(c, yy, "Legacy protocols observed", 8912, "Immediate", RED, 38640); yy -= 58
    section_card(c, M, yy - 112, PAGE_W - 2 * M, 112, "Modern interpretation",
                 "TLS 1.0 and TLS 1.1 are deprecated by IETF RFC 8996. NIST SP 800-52 Rev. 2 provides modern TLS configuration expectations for federal systems. Customer reports should map the exact observed protocol, cipher, key, signature, and chain evidence to the policy that applies to that environment.", CYAN)
    section_card(c, M, 73, PAGE_W - 2 * M, 108, "Corrective work",
                 "Disable obsolete protocols and disallowed cipher suites, replace weak keys and signatures, deploy the complete approved chain, test compatibility, and reobserve the public endpoint after change. Where replacement creates operational risk, document an exception with compensating controls and a retirement date.", GREEN)
    c.showPage()

    # Page 10
    fill_page(c); header(c, 10, "Exposure patterns")
    y = title(c, "Wildcard and non-production certificates expand operational risk.", "These conditions are not automatically vulnerabilities. They become higher priority when combined with unmanaged ownership, public exposure, weak configuration, expiry, excessive reuse, or policy drift.")
    metric(c, M, y - 100, 240, 84, "Wildcard certificates", "5,842", "518 showed additional lifecycle risk.", YELLOW)
    metric(c, M + 258, y - 100, 240, 84, "Non-production markers", "4,116", "Test, development, QA, staging, or similar names.", RED)
    yy = y - 142
    section_card(c, M, yy - 122, 244, 122, "Wildcard review",
                 "Identify reuse across endpoints, confirm private-key custody, reduce blast radius, document legitimate coverage, and replace broad certificates where narrower SANs are practical.", YELLOW)
    section_card(c, M + 262, yy - 122, 244, 122, "Non-production review",
                 "Confirm whether the endpoint is intentionally public, hardened, patched, monitored, owned, and separated from production data and credentials.", RED)
    section_card(c, M, 78, PAGE_W - 2 * M, 120, "Current feature confirmed",
                 "Historical assessment evidence confirms that Vellitas generated a special flag when certificate nomenclature indicated a non-production service. That places certificate-creep detection based on naming signals in the demonstrated current-capability baseline.", CYAN, "Roadmap status updated")
    c.showPage()

    # Page 11
    fill_page(c); header(c, 11, "Remediation plan")
    y = title(c, "Turn findings into owned, testable work.", "The modern report organizes findings and recommendations into a phased remediation program with explicit verification.")
    phases = [
        ("01", "Validate scope and ownership", "Reconcile domains, vendors, business owners, approved locations, issuers, and exception policy."),
        ("02", "Contain immediate exposure", "Address expired certificates, obsolete protocols, weak keys or signatures, and suspicious public non-production services."),
        ("03", "Reduce structural risk", "Rationalize certificate authorities, self-signed use, wildcard reuse, long validity, and unmanaged dependencies."),
        ("04", "Verify from the outside", "Reobserve each endpoint, record the corrected evidence, and preserve closure or exception rationale."),
        ("05", "Continue monitoring", "Repeat discovery and notify on material changes to the external security profile."),
    ]
    yy = y - 22
    for num, heading, body in phases:
        rounded(c, M, yy - 70, PAGE_W - 2 * M, 62, fill=SURFACE)
        c.setFillColor(CYAN); c.setFont("Helvetica-Bold", 17); c.drawString(M + 16, yy - 35, num)
        c.setFillColor(TEXT); c.setFont("Helvetica-Bold", 10); c.drawString(M + 62, yy - 24, heading)
        para(c, body, M + 62, yy - 34, PAGE_W - 2 * M - 78, size=8.2, leading=11.5, color=MUTED)
        yy -= 80
    c.showPage()

    # Page 12
    fill_page(c); header(c, 12, "Evidence appendix")
    y = title(c, "Representative synthetic evidence.", "Rows below preserve the structure and analytical usefulness of certificate evidence without reproducing a source customer's records. IP addresses use documentation-only ranges reserved for examples.")
    data = [
        ["IP", "Country", "Signature", "Authority", "Expires", "Years", "Key", "Protocol"],
        ["192.0.2.34", "USA", "SHA-1", "Self-signed", "03/15/27", "3.0", "1024", "TLS 1.0"],
        ["198.51.100.72", "Netherlands", "MD5", "Self-signed", "11/30/26", "10.0", "1024", "SSLv3"],
        ["203.0.113.141", "Singapore", "SHA-1", "Self-signed", "06/30/26", "5.0", "1024", "TLS 1.1"],
    ]
    table = Table(data, colWidths=[83, 54, 50, 74, 58, 42, 44, 55], rowHeights=[26, 34, 34, 34])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SURFACE_2),
        ("TEXTCOLOR", (0, 0), (-1, 0), CYAN_SOFT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 6.6),
        ("TEXTCOLOR", (0, 1), (-1, -1), MUTED_2),
        ("BACKGROUND", (0, 1), (-1, -1), SURFACE),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    _, th = table.wrap(PAGE_W - 2 * M, 200)
    table.drawOn(c, M, y - th - 26)
    yy = y - th - 66
    section_card(c, M, yy - 145, PAGE_W - 2 * M, 145, "Capabilities confirmed by historical work",
                 "Internet-visible discovery; approved marker expansion; geospatial analysis; certificate authority inventory; name and domain encroachment; protocol and cipher analysis; self-signed, expiration, near-expiry, long-validity, weak-key, weak-signature, wildcard, and non-production detection; certificate-level evidence; portfolio summary; and consultant-authored remediation recommendations.", GREEN)
    rounded(c, M, 72, PAGE_W - 2 * M, 94, fill=SURFACE_2, stroke=YELLOW)
    c.setFillColor(YELLOW); c.setFont("Helvetica-Bold", 8); c.drawString(M + 16, 145, "SOURCE CONTROL")
    para(c, "This prototype is informed by patterns from a historical enterprise assessment. All names, domains, IP addresses, dates, geographic distributions, counts, and evidence rows have been altered or synthesized. Findings and proportions remain plausible demonstrations of Vellitas capabilities, but no row or metric describes the original customer or any current environment.", M + 16, 132, PAGE_W - 2 * M - 32, size=8.5, leading=12, color=MUTED_2)
    c.showPage()
    c.save()


def roadmap_report(path):
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setTitle("Vellitas Roadmap Report - Future-State Product Preview")
    c.setAuthor("Vellitas, LLC")
    cover(
        c,
        "Roadmap report",
        "Continuous External Trust Intelligence",
        "A future-state report concept that extends proven certificate assessment into continuous Certificate Transparency, DNS and infrastructure change monitoring, vendor assurance, confidence scoring, tenant-scoped exploration, and governed remediation automation.",
        "Illustrative future-state product preview",
        shield="yellow",
        roadmap=True,
    )

    # Page 2
    fill_page(c); header(c, 2, "Future-state executive view", "ROADMAP PREVIEW")
    y = title(c, "Illustrative only", "From periodic assessment to continuous trust monitoring.", "The events and counts on this page are synthetic design examples. They show how the future report should communicate change without claiming that an anomaly proves compromise.")
    card_w = (PAGE_W - 2 * M - 18) / 2
    metric(c, M, y - 102, card_w, 84, "New CT issuances", "04", "Illustrative events requiring policy comparison.", CYAN)
    metric(c, M + card_w + 18, y - 102, card_w, 84, "DNS changes", "07", "A, AAAA, CNAME, MX, or NS drift.", YELLOW)
    metric(c, M, y - 204, card_w, 84, "Vendor exceptions", "02", "Baseline deviations awaiting validation.", RED)
    metric(c, M + card_w + 18, y - 204, card_w, 84, "Verified closures", "11", "Remediations confirmed from the outside.", GREEN)
    section_card(c, M, y - 352, PAGE_W - 2 * M, 116, "Executive question",
                 "What changed in the public trust surface, does it conflict with approved policy, how confident is the conclusion, who owns the next action, and has the corrective work been independently verified?", CYAN, "Future-state reporting principle")
    c.showPage()

    # Page 3
    fill_page(c); header(c, 3, "Certificate Transparency", "ROADMAP PREVIEW")
    y = title(c, "Early warning from public certificate issuance.", "Continuous CT monitoring should identify related issuance before or independently of endpoint discovery, then correlate it with customer scope and approved infrastructure.")
    events = [
        ("08:14 UTC", "NEW ISSUANCE", "api.example-corp.com", "Unexpected issuer", RED),
        ("08:18 UTC", "SAN EXPANSION", "*.payments.example-corp.com", "New wildcard", YELLOW),
        ("09:02 UTC", "RENEWAL", "www.example-corp.com", "Approved pattern", GREEN),
        ("11:46 UTC", "LOOKALIKE", "examplecorp-support.net", "Ownership unknown", RED),
    ]
    yy = y - 22
    for time, kind, name, status, accent in events:
        rounded(c, M, yy - 70, PAGE_W - 2 * M, 60)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(MUTED); c.drawString(M + 14, yy - 26, time)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(accent); c.drawString(M + 86, yy - 26, kind)
        c.setFont("Helvetica-Bold", 10); c.setFillColor(TEXT); c.drawString(M + 175, yy - 26, name)
        c.setFont("Helvetica", 8); c.setFillColor(MUTED_2); c.drawRightString(PAGE_W - M - 14, yy - 26, status)
        yy -= 78
    section_card(c, M, 76, PAGE_W - 2 * M, 120, "Production acceptance criteria",
                 "Deduplicate redundant CT sources; match exact, wildcard, SAN, subsidiary, brand, and reviewed similarity candidates; retain issuer, serial, validity, fingerprint, SPKI hash, log timestamp, source log, and first-seen evidence; suppress known renewals; assign confidence; and preserve reproducible evidence.", CYAN)
    c.showPage()

    # Page 4
    fill_page(c); header(c, 4, "DNS and infrastructure drift", "ROADMAP PREVIEW")
    y = title(c, "Show what moved, when, and why it matters.", "Correlate CT with DNS, IP, ASN, cloud provider, geography, and endpoint observations. The example below is synthetic.")
    x0 = M + 34; x1 = PAGE_W - M - 34; yy = y - 68
    line(c, x0, yy, x1, yy, color=LINE, width=2)
    timeline = [
        (0.00, "First seen", "Certificate observed", GREEN),
        (0.31, "DNS change", "CNAME moved", YELLOW),
        (0.58, "Network drift", "New ASN/provider", RED),
        (0.82, "Geo change", "New country", RED),
        (1.00, "Validated", "Approved migration", GREEN),
    ]
    for pos, label, note, accent in timeline:
        xx = x0 + (x1 - x0) * pos
        c.setFillColor(BG); c.setStrokeColor(accent); c.setLineWidth(2); c.circle(xx, yy, 8, fill=1, stroke=1)
        c.setFillColor(accent); c.circle(xx, yy, 3, fill=1, stroke=0)
        para(c, f"<b>{label}</b><br/>{note}", xx - 42, yy - 18, 84, size=7.2, leading=9.5, color=MUTED_2, align=TA_CENTER)
    section_card(c, M, yy - 210, 244, 112, "Signals to preserve",
                 "A, AAAA, CNAME, MX, and NS; resolver and observation time; IP; ASN; network owner; provider; country; endpoint; certificate and key identity; first seen; last seen.", CYAN)
    section_card(c, M + 262, yy - 210, 244, 112, "Context before escalation",
                 "Approved CDN, cloud migration, disaster recovery, acquisition, vendor, and maintenance patterns. Geography remains a risk signal, not a verdict.", YELLOW)
    section_card(c, M, 76, PAGE_W - 2 * M, 112, "Outcome",
                 "The report should explain the observed transition, compare it with customer policy, list corroborating evidence, record alternate legitimate explanations, assign confidence, and identify the validation step.", GREEN)
    c.showPage()

    # Page 5
    fill_page(c); header(c, 5, "Certificate and key graph", "ROADMAP PREVIEW")
    y = title(c, "One certificate can reveal a wider deployment pattern.", "A future graph links certificate fingerprints and public keys to domains, endpoints, networks, locations, issuers, vendors, and historical observations.")
    cx, cy = PAGE_W / 2, y - 176
    nodes = [
        (cx, cy, 54, "Fingerprint\n9F:2A:...", CYAN),
        (cx - 170, cy + 95, 42, "api.example", GREEN),
        (cx + 170, cy + 95, 42, "vpn.vendor", YELLOW),
        (cx - 175, cy - 95, 42, "ASN 64510", BLUE),
        (cx + 175, cy - 95, 42, "New country", RED),
        (cx, cy - 145, 42, "SPKI hash", CYAN_SOFT),
    ]
    for x, y2, _, _, accent in nodes[1:]: line(c, cx, cy, x, y2, color=accent, width=1.1)
    for x, y2, r, label, accent in nodes:
        c.setFillColor(SURFACE); c.setStrokeColor(accent); c.setLineWidth(1.2); c.circle(x, y2, r, fill=1, stroke=1)
        para(c, label, x - r + 5, y2 + 9, 2 * r - 10, size=7.5, leading=9, color=TEXT, font="Helvetica-Bold", align=TA_CENTER)
    section_card(c, M, 74, PAGE_W - 2 * M, 118, "Investigation value",
                 "Detect the same certificate or public key appearing on unfamiliar IP addresses, providers, vendor systems, or countries; identify blast radius after issuer or key incidents; and distinguish planned shared deployment from suspicious reuse.", RED)
    c.showPage()

    # Page 6
    fill_page(c); header(c, 6, "Vendor assurance", "ROADMAP PREVIEW")
    y = title(c, "A vendor's public edge becomes part of your trust model.", "Continuous vendor assurance should apply a customer-approved baseline proportionate to the access, software, identity, data, or operational dependency involved.")
    rounded(c, M, y - 210, PAGE_W - 2 * M, 190)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(CYAN); c.drawString(M + 18, y - 44, "ILLUSTRATIVE VENDOR PROFILE")
    c.setFont("Helvetica-Bold", 17); c.setFillColor(TEXT); c.drawString(M + 18, y - 72, "Northstar Managed Services")
    c.setFont("Helvetica", 8); c.setFillColor(MUTED); c.drawString(M + 18, y - 91, "Relationship: privileged remote administration | Criticality: high")
    checks = [("Certificate baseline", "Pass", GREEN), ("TLS policy", "Caution", YELLOW), ("DNS drift", "Investigate", RED), ("Approved geography", "Pass", GREEN)]
    yy = y - 122
    for i, (label, result, accent) in enumerate(checks):
        xx = M + 18 + (i % 2) * 240
        yrow = yy - (i // 2) * 38
        c.setFillColor(accent); c.circle(xx + 4, yrow + 3, 4, fill=1, stroke=0)
        c.setFillColor(MUTED_2); c.setFont("Helvetica", 8); c.drawString(xx + 15, yrow, label)
        c.setFillColor(accent); c.setFont("Helvetica-Bold", 8); c.drawRightString(xx + 215, yrow, result)
    section_card(c, M, y - 352, 244, 116, "Minimum data model",
                 "Vendor, business service, access level, authorized scope, owner, criticality, required baseline, exceptions, last verification, findings, remediation owner, and retest status.", CYAN)
    section_card(c, M + 262, y - 352, 244, 116, "Assessment boundary",
                 "Passive public sources may identify exposure. Active scanning must remain within written authorization. Outside-in evidence does not replace the vendor's internal security program.", YELLOW)
    section_card(c, M, 66, PAGE_W - 2 * M, 105, "Standards alignment",
                 "Map the program to NIST CSF 2.0 GV.SC, NIST SP 800-161 Rev. 1, applicable contractual requirements, and sector-specific obligations. Referencing a standard does not itself establish compliance.", GREEN)
    c.showPage()

    # Page 7
    fill_page(c); header(c, 7, "Confidence and explainability", "ROADMAP PREVIEW")
    y = title(c, "Make every score explainable.", "A future finding should expose the evidence, policy, corroboration, legitimate alternatives, and validation step behind its confidence and severity.")
    rounded(c, M, y - 178, PAGE_W - 2 * M, 158)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(RED); c.drawString(M + 18, y - 48, "SYNTHETIC EXAMPLE - HIGH PRIORITY")
    c.setFont("Helvetica-Bold", 16); c.setFillColor(TEXT); c.drawString(M + 18, y - 77, "Certificate and DNS moved to an unapproved provider")
    para(c, "New IP and ASN + new country + certificate fingerprint reused + DNS changed within 18 minutes + no approved maintenance record.", M + 18, y - 92, PAGE_W - 2 * M - 36, size=8.5, leading=12, color=MUTED_2)
    c.setFillColor(SURFACE_2); c.roundRect(M + 18, y - 145, 380, 10, 5, fill=1, stroke=0)
    c.setFillColor(RED); c.roundRect(M + 18, y - 145, 319, 10, 5, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(TEXT); c.drawRightString(PAGE_W - M - 18, y - 146, "84 / 100")
    yy = y - 208
    factors = [
        ("Evidence quality", "Repeated direct observation", GREEN),
        ("Policy conflict", "Provider and country unapproved", RED),
        ("Corroboration", "Four independent changes", RED),
        ("False-positive context", "CDN / migration not yet ruled out", YELLOW),
        ("Required validation", "Confirm change with owner", CYAN),
    ]
    for label, value, accent in factors:
        c.setFont("Helvetica", 8); c.setFillColor(MUTED); c.drawString(M, yy, label)
        c.setFont("Helvetica-Bold", 8); c.setFillColor(accent); c.drawRightString(PAGE_W - M, yy, value)
        line(c, M, yy - 10, PAGE_W - M, yy - 10, color=LINE, width=0.4)
        yy -= 40
    section_card(c, M, 70, PAGE_W - 2 * M, 90, "Severity is not confidence",
                 "Severity describes potential business impact. Confidence describes how strongly the evidence supports the working interpretation. A high-impact anomaly can still require customer validation before action.", CYAN)
    c.showPage()

    # Page 8
    fill_page(c); header(c, 8, "Governed remediation automation", "ROADMAP PREVIEW")
    y = title(c, "Generate scripts, but keep humans in control.", "Future remediation artifacts should be versioned, target-specific, reviewable, reversible, and verified from the outside. Automatic execution remains off by default.")
    steps = [
        ("01", "Generate", "Create a change artifact tied to a specific finding and target."),
        ("02", "Preview", "Show exact commands, expected effect, dependencies, and risk."),
        ("03", "Dry run", "Use a safe validation mode where the platform permits it."),
        ("04", "Approve", "Require authorized Vellitas and customer review."),
        ("05", "Execute", "Run through the customer's controlled change process."),
        ("06", "Verify", "Reobserve the endpoint and preserve result and rollback evidence."),
    ]
    yy = y - 24
    for idx, (num, heading, body) in enumerate(steps):
        col = idx % 2; row = idx // 2
        x = M + col * 262; ycard = yy - row * 132 - 110
        rounded(c, x, ycard, 244, 104)
        c.setFillColor(CYAN); c.setFont("Helvetica-Bold", 16); c.drawString(x + 15, ycard + 71, num)
        c.setFillColor(TEXT); c.setFont("Helvetica-Bold", 11); c.drawString(x + 55, ycard + 73, heading)
        para(c, body, x + 15, ycard + 56, 214, size=8.2, leading=11.5, color=MUTED)
    section_card(c, M, 67, PAGE_W - 2 * M, 90, "Mandatory safeguards",
                 "Least privilege, tenant and target binding, immutable audit history, secrets isolation, output capture, rollback guidance, time-bounded approvals, customer change windows, and post-change external verification.", RED)
    c.showPage()

    # Page 9
    fill_page(c); header(c, 9, "Tenant-scoped customer portal", "ROADMAP PREVIEW")
    y = title(c, "Let customers explore only their approved portfolio.", "The portal must deny access by default and bind every asset, observation, finding, report, script, and query to a tenant and confirmed scope.")
    rounded(c, M, y - 235, PAGE_W - 2 * M, 215)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(CYAN); c.drawString(M + 16, y - 46, "ILLUSTRATIVE FILTERED SEARCH")
    filters = ["Portfolio: Example Corp", "Status: self-signed", "Environment: public", "Region: all", "Owner: unassigned"]
    xx = M + 16; yy = y - 72
    for f in filters:
        w = stringWidth(f, "Helvetica", 7) + 18
        c.setFillColor(SURFACE_2); c.setStrokeColor(LINE); c.roundRect(xx, yy - 12, w, 20, 10, fill=1, stroke=1)
        c.setFillColor(MUTED_2); c.setFont("Helvetica", 7); c.drawString(xx + 9, yy - 5, f)
        xx += w + 8
        if xx > PAGE_W - M - 120: xx = M + 16; yy -= 28
    table_data = [
        ["Host", "Finding", "Confidence", "Owner", "State"],
        ["vpn.example.com", "Self-signed", "Confirmed", "Network", "Open"],
        ["admin.example.com", "Default appliance cert", "High", "Unassigned", "Triage"],
        ["lab.example.com", "Non-production exposed", "Medium", "Engineering", "Exception"],
    ]
    t = Table(table_data, colWidths=[127, 139, 76, 80, 62], rowHeights=[25, 31, 31, 31])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BG), ("TEXTCOLOR", (0, 0), (-1, 0), CYAN_SOFT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7), ("TEXTCOLOR", (0, 1), (-1, -1), MUTED_2),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ]))
    t.wrap(PAGE_W - 2 * M - 32, 200)
    t.drawOn(c, M + 16, y - 219)
    section_card(c, M, y - 374, 244, 116, "Scope onboarding",
                 "Start with customer-provided domains, brands, subsidiaries, acquisitions, networks, and cloud accounts. Propose related assets from public evidence for review; do not auto-authorize active assessment.", YELLOW)
    section_card(c, M + 262, y - 374, 244, 116, "Access controls",
                 "Tenant-bound data model, RBAC, SSO/MFA, audit logging, export controls, reviewed support access, and authorization enforced below the interface at every query and object boundary.", RED)
    c.showPage()

    # Page 10
    fill_page(c); header(c, 10, "Delivery roadmap", "ROADMAP PREVIEW")
    y = title(c, "Build on the proven assessment foundation.", "The supplied report moves discovery and core certificate analysis into the current baseline. The remaining roadmap centers on continuous change, productized workflows, and safe customer access.")
    phases = [
        ("CURRENT", GREEN, "Established assessment", "Discovery, geospatial, name encroachment, CA inventory, certificate lifecycle, key/signature, protocol/cipher, wildcard, non-production, reporting, and consultant remediation."),
        ("NEXT", CYAN, "Normalize and monitor", "Evidence model; first/last seen; fingerprint/key reuse; expected-vs-observed policy; continuous CT; DNS/IP/ASN/provider correlation; confidence and alert suppression."),
        ("THEN", YELLOW, "Workflow and portal", "Tenant-scoped search; candidate-scope review; SSO/MFA; ownership; tickets; retest; audit trail; vendor portfolios; SIEM/API/webhooks."),
        ("LATER", RED, "Controlled automation", "Reviewed remediation scripts; dry-run; approvals; rollback; customer change execution; limited automated revocation or removal requests with strong authorization."),
    ]
    yy = y - 30
    for label, accent, heading, body in phases:
        rounded(c, M, yy - 108, PAGE_W - 2 * M, 94)
        c.setFillColor(accent); c.rect(M, yy - 108, 4, 94, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(accent); c.drawString(M + 18, yy - 37, label)
        c.setFont("Helvetica-Bold", 12); c.setFillColor(TEXT); c.drawString(M + 104, yy - 37, heading)
        para(c, body, M + 104, yy - 50, PAGE_W - 2 * M - 122, size=8.2, leading=11.5, color=MUTED)
        yy -= 116
    rounded(c, M, 58, PAGE_W - 2 * M, 78, fill=SURFACE_2, stroke=CYAN)
    c.setFillColor(CYAN); c.setFont("Helvetica-Bold", 8); c.drawString(M + 16, 116, "REPORTING STANDARD")
    para(c, "Every future report must distinguish observed evidence, inferred interpretation, customer-confirmed context, current product capability, roadmap capability, severity, confidence, required work, responsible owner, and outside-in verification status.", M + 16, 103, PAGE_W - 2 * M - 32, size=8.5, leading=12, color=MUTED_2)
    c.showPage()
    c.save()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"
    if mode not in {"--all", "--current-only", "--roadmap-only"}:
        raise SystemExit("usage: build-vellitas-reports.py [--all|--current-only|--roadmap-only]")
    if mode in {"--all", "--current-only"}:
        current_path = OUT / "Vellitas-Current-Capability-Report-Redesign.pdf"
        current_report(current_path)
        print(current_path)
    if mode in {"--all", "--roadmap-only"}:
        roadmap_path = OUT / "Vellitas-Roadmap-Report-Future-State.pdf"
        roadmap_report(roadmap_path)
        print(roadmap_path)
