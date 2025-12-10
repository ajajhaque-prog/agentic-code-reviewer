
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from typing import Dict, Any

def build_pdf_report(review_data: Dict[str, Any], output_path: str, filename: str):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles["Title"]
    story.append(Paragraph(f"Code Review Report: {filename}", title_style))
    story.append(Spacer(1, 12))

    # Ratings Table
    rating = review_data.get("rating", {})
    rating_data = [
        ["Metric", "Score"],
        ["Quality", str(rating.get("quality", "N/A"))],
        ["Security", str(rating.get("security", "N/A"))],
        ["Maintainability", str(rating.get("maintainability", "N/A"))],
        ["Overall", str(rating.get("overall", "N/A"))]
    ]
    t = Table(rating_data, colWidths=[200, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 24))

    # Summary
    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    summary_text = review_data.get("summary_markdown", "").replace("\n", "<br/>")
    story.append(Paragraph(summary_text, styles["BodyText"]))
    story.append(Spacer(1, 24))

    # Findings
    story.append(Paragraph("Detailed Findings", styles["Heading2"]))
    findings = review_data.get("findings", [])

    if not findings:
        story.append(Paragraph("No issues found.", styles["BodyText"]))

    for f in findings:
        # Finding Header
        severity = f.get("severity", "info").upper()
        color = colors.black
        if severity == "CRITICAL": color = colors.red
        elif severity == "HIGH": color = colors.orange
        elif severity == "MEDIUM": color = colors.brown

        header_text = f"<b>[{severity}] {f.get('title', 'Issue')} (Line {f.get('line', '?')})</b>"
        story.append(Paragraph(header_text, styles["Heading3"]))
        
        # Details
        story.append(Paragraph(f"<b>Category:</b> {f.get('category', 'General')}", styles["Normal"]))
        story.append(Paragraph(f"<b>Description:</b> {f.get('description', '')}", styles["Normal"]))
        story.append(Paragraph(f"<b>Recommendation:</b> {f.get('recommendation', '')}", styles["Normal"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph("-" * 60, styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)
