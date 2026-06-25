from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
import os


def create_report(filename: str, ats_score: int, skills: list, questions: str) -> str:
    """
    Generate a PDF interview report and return the file path.
    The file is saved in the 'reports' folder.
    """
    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Heading1"],
                                  fontSize=20, textColor=colors.HexColor("#2c3e50"),
                                  spaceAfter=12)
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"],
                                    fontSize=14, textColor=colors.HexColor("#2980b9"),
                                    spaceAfter=8)
    body_style = styles["BodyText"]

    story = []

    # Title
    story.append(Paragraph("AI Interview Platform — Resume Report", title_style))
    story.append(Spacer(1, 0.5*cm))

    # ATS Score
    story.append(Paragraph("ATS Score", heading_style))
    score_color = "#27ae60" if ats_score >= 70 else "#e67e22" if ats_score >= 40 else "#e74c3c"
    story.append(Paragraph(
        f'<font color="{score_color}"><b>{ats_score} / 100</b></font>',
        body_style
    ))
    story.append(Spacer(1, 0.5*cm))

    # Skills
    story.append(Paragraph("Extracted Skills", heading_style))
    if skills:
        skills_text = ", ".join(skills)
        story.append(Paragraph(skills_text, body_style))
    else:
        story.append(Paragraph("No skills detected.", body_style))
    story.append(Spacer(1, 0.5*cm))

    # Interview Questions
    story.append(Paragraph("Suggested Interview Questions", heading_style))
    if questions:
        for line in questions.strip().split("\n"):
            line = line.strip()
            if line:
                story.append(Paragraph(line, body_style))
                story.append(Spacer(1, 0.2*cm))
    else:
        story.append(Paragraph("No questions generated.", body_style))

    doc.build(story)
    return filepath
