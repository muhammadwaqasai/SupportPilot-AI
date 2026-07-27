from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_business_report(
    filename,
    stats,
    ai_report,
    root_cause,
    trend_report
):

    print("START PDF GENERATION")
    print("FILENAME:", filename)

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    # ---------------- TITLE ----------------

    content.append(
        Paragraph(
            "SupportPilot AI - Business Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ---------------- BASIC STATS ----------------

    content.append(
        Paragraph(
            f"Total Tickets: {stats['total']}",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Business Health Score: {ai_report['health_score']}/100",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            ai_report["business_health"],
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ---------------- SUMMARY ----------------

    content.append(
        Paragraph(
            "Executive Summary",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            ai_report["summary"],
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ---------------- RECOMMENDATIONS ----------------

    content.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    for item in ai_report["recommendations"]:

        content.append(
            Paragraph(
                "- " + item,
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # ---------------- ROOT CAUSE ----------------

    content.append(
        Paragraph(
            "Root Cause Analysis",
            styles["Heading2"]
        )
    )

    for item in root_cause["main_problems"]:

        content.append(
            Paragraph(
                "- " + item,
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # ---------------- TREND ----------------

    content.append(
        Paragraph(
            "Trend Analysis",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            trend_report["trend_summary"],
            styles["Normal"]
        )
    )

    print("CONTENT ITEMS:", len(content))

    doc.build(content)

    print("PDF BUILD COMPLETE")
    print("PDF CREATED:", filename)