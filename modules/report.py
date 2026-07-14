"""
PDF Report Generator.
Builds a downloadable PDF summary of a password analysis result using reportlab.
"""

import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 ListFlowable, ListItem, HRFlowable)

DARK = colors.HexColor("#101820")
ACCENT = colors.HexColor("#00E5A0")
GREY = colors.HexColor("#555555")
LIGHTBG = colors.HexColor("#F2F6FB")


def _status_color(passed: bool):
    return colors.HexColor("#1B8A3E") if passed else colors.HexColor("#C62828")


def generate_pdf_report(analysis: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                             leftMargin=18 * mm, rightMargin=18 * mm, title="SecurePass Report")

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleX", parent=styles["Title"], fontSize=22, textColor=DARK)
    subtitle_style = ParagraphStyle("SubX", parent=styles["Normal"], fontSize=10, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, textColor=DARK, spaceBefore=12, spaceAfter=6)
    body = ParagraphStyle("BodyX", parent=styles["Normal"], fontSize=10, leading=14)
    bullet = ParagraphStyle("BulletX", parent=body, leftIndent=12, spaceAfter=3)

    story = []
    story.append(Paragraph("SecurePass -- Password Analysis Report", title_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))

    # Summary table
    summary_data = [
        ["Metric", "Value"],
        ["Password (masked)", analysis["password_masked"]],
        ["Overall Score", f"{analysis['score']} / 100"],
        ["Strength", analysis["strength"]],
        ["Entropy", f"{analysis['entropy']} bits ({analysis['entropy_label']})"],
        ["Estimated Crack Time", analysis["crack_time_estimate"]],
    ]
    t = Table(summary_data, colWidths=[60 * mm, 100 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHTBG]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)

    story.append(Paragraph("Policy Checks", h2))
    policy = analysis["policy"]
    policy_rows = [
        ["Check", "Result"],
        ["Minimum Length", "Passed" if policy["length"] else "Failed"],
        ["Uppercase Letter", "Passed" if policy["uppercase"] else "Failed"],
        ["Lowercase Letter", "Passed" if policy["lowercase"] else "Failed"],
        ["Number", "Passed" if policy["numbers"] else "Failed"],
        ["Special Character", "Passed" if policy["special"] else "Failed"],
    ]
    t2 = Table(policy_rows, colWidths=[80 * mm, 80 * mm])
    style2 = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i, key in enumerate(["length", "uppercase", "lowercase", "numbers", "special"], start=1):
        style2.append(("TEXTCOLOR", (1, i), (1, i), _status_color(policy[key])))
    t2.setStyle(TableStyle(style2))
    story.append(t2)

    story.append(Paragraph("Attack Simulation Checks", h2))
    checks = [
        ["Check", "Result"],
        ["Common Password", "Detected" if analysis["common_password"]["is_common"] else "Not Detected"],
        ["Dictionary Attack", "Vulnerable" if analysis["dictionary_attack"]["vulnerable"] else "Safe"],
        ["Keyboard Pattern", "Detected" if analysis["keyboard_pattern"]["detected"] else "Not Detected"],
        ["Repeated Characters", "Detected" if analysis["repeated_chars"]["detected"] else "Not Detected"],
        ["Sequential Characters", "Detected" if analysis["sequential_chars"]["detected"] else "Not Detected"],
    ]
    t3 = Table(checks, colWidths=[80 * mm, 80 * mm])
    bad_flags = [
        analysis["common_password"]["is_common"],
        analysis["dictionary_attack"]["vulnerable"],
        analysis["keyboard_pattern"]["detected"],
        analysis["repeated_chars"]["detected"],
        analysis["sequential_chars"]["detected"],
    ]
    style3 = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i, flag in enumerate(bad_flags, start=1):
        style3.append(("TEXTCOLOR", (1, i), (1, i), _status_color(not flag)))
    t3.setStyle(TableStyle(style3))
    story.append(t3)

    story.append(Paragraph("Suggestions to Improve", h2))
    items = [ListItem(Paragraph(s, bullet)) for s in analysis["suggestions"]]
    story.append(ListFlowable(items, bulletType="bullet", start="\u2022"))

    story.append(Spacer(1, 14))
    story.append(Paragraph("Generated by SecurePass -- AI Inspired Password Strength Analyzer", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
