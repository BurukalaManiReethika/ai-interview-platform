from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_report(
        filename,
        ats_score,
        skills,
        questions):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"ATS Score: {ats_score}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            f"Skills: {', '.join(skills)}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            questions.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    pdf.build(content)

    return filename
