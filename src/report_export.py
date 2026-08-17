# ============================================================
# BRANDPULSE AI
# PROFESSIONAL REPORT EXPORT
# ============================================================

from io import BytesIO
from datetime import datetime

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches, Pt


# ============================================================
# HELPERS
# ============================================================

def add_title(
    document,
    text,
):
    paragraph = document.add_paragraph()

    paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    run = paragraph.add_run(
        text
    )

    run.bold = True
    run.font.size = Pt(22)


def add_subtitle(
    document,
    text,
):
    paragraph = document.add_paragraph()

    paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    run = paragraph.add_run(
        text
    )

    run.font.size = Pt(11)


def add_section_heading(
    document,
    text,
):
    heading = document.add_heading(
        text,
        level=1
    )

    return heading


def add_subheading(
    document,
    text,
):
    document.add_heading(
        text,
        level=2
    )


def add_paragraph_text(
    document,
    text,
):
    if text is None:
        return

    text = str(text).strip()

    if not text:
        return

    document.add_paragraph(
        text
    )


# ============================================================
# MARKDOWN-LIKE LLM REPORT PARSER
# ============================================================

def add_llm_report(
    document,
    report_text,
):
    """
    Convert the basic Markdown-style output
    produced by the LLM into Word headings
    and paragraphs.
    """

    if not report_text:
        return

    lines = str(
        report_text
    ).splitlines()

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        # Main heading
        if line.startswith(
            "# "
        ):

            document.add_heading(
                line[2:].strip(),
                level=1
            )

        # Level 2 heading
        elif line.startswith(
            "## "
        ):

            document.add_heading(
                line[3:].strip(),
                level=2
            )

        # Level 3 heading
        elif line.startswith(
            "### "
        ):

            document.add_heading(
                line[4:].strip(),
                level=3
            )

        # Bullet
        elif (
            line.startswith("- ")
            or line.startswith("• ")
        ):

            bullet_text = (
                line[2:].strip()
            )

            document.add_paragraph(
                bullet_text,
                style="List Bullet"
            )

        # Numbered item
        elif (
            len(line) > 2
            and line[0].isdigit()
            and ". " in line[:4]
        ):

            document.add_paragraph(
                line,
                style="List Number"
            )

        else:

            # Remove basic Markdown bold
            cleaned_line = (
                line.replace(
                    "**",
                    ""
                )
            )

            document.add_paragraph(
                cleaned_line
            )


# ============================================================
# CREATE DOCX
# ============================================================

def create_brandpulse_docx(
    analysis_summary,
    manager_reports,
    executive_report,
):
    """
    Create the complete BrandPulse AI
    management report as an in-memory DOCX.
    """

    document = Document()


    # ========================================================
    # DOCUMENT MARGINS
    # ========================================================

    for section in document.sections:

        section.top_margin = (
            Inches(0.65)
        )

        section.bottom_margin = (
            Inches(0.65)
        )

        section.left_margin = (
            Inches(0.75)
        )

        section.right_margin = (
            Inches(0.75)
        )


    # ========================================================
    # COVER PAGE
    # ========================================================

    add_title(
        document,
        "BrandPulse AI"
    )

    add_subtitle(
        document,
        (
            "AI-Assisted Brand Reputation "
            "Intelligence Report"
        )
    )

    document.add_paragraph()

    title = document.add_paragraph()

    title.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    run = title.add_run(
        (
            "Online Review-Based Brand "
            "Reputation Prediction Using "
            "NLP Techniques"
        )
    )

    run.bold = True
    run.font.size = Pt(14)


    generated = document.add_paragraph()

    generated.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    generated.add_run(
        "Generated: "
        + datetime.now().strftime(
            "%d %B %Y, %H:%M"
        )
    )


    document.add_page_break()


    # ========================================================
    # 1. ANALYSIS OVERVIEW
    # ========================================================

    add_section_heading(
        document,
        "1. Brand Reputation Overview"
    )


    overview_table = document.add_table(
        rows=1,
        cols=2
    )

    overview_table.alignment = (
        WD_TABLE_ALIGNMENT.CENTER
    )

    overview_table.style = (
        "Table Grid"
    )


    header_cells = (
        overview_table.rows[
            0
        ].cells
    )

    header_cells[0].text = (
        "Indicator"
    )

    header_cells[1].text = (
        "Result"
    )


    overview_values = [

        (
            "Reviews Analysed",
            analysis_summary.get(
                "total_reviews",
                0
            )
        ),

        (
            "Positive Reviews",
            analysis_summary.get(
                "positive_reviews",
                0
            )
        ),

        (
            "Negative Reviews",
            analysis_summary.get(
                "negative_reviews",
                0
            )
        ),

        (
            "Positive Percentage",
            (
                str(
                    analysis_summary.get(
                        "positive_percentage",
                        0
                    )
                )
                + "%"
            )
        ),

        (
            "Negative Percentage",
            (
                str(
                    analysis_summary.get(
                        "negative_percentage",
                        0
                    )
                )
                + "%"
            )
        ),

        (
            "Brand Reputation Score",
            (
                str(
                    analysis_summary.get(
                        "reputation_score",
                        0
                    )
                )
                + "%"
            )
        ),
    ]


    for (
        indicator,
        result
    ) in overview_values:

        cells = (
            overview_table
            .add_row()
            .cells
        )

        cells[0].text = str(
            indicator
        )

        cells[1].text = str(
            result
        )


    document.add_paragraph()


    note = document.add_paragraph()

    run = note.add_run(
        "Methodology Note: "
    )

    run.bold = True

    note.add_run(
        (
            "The Brand Reputation Score is "
            "a project-defined indicator based "
            "on the proportion of positive "
            "DistilBERT sentiment predictions."
        )
    )


    # ========================================================
    # 2. ISSUE ANALYSIS
    # ========================================================

    add_section_heading(
        document,
        "2. Negative Review Issue Analysis"
    )


    issue_counts = (
        analysis_summary.get(
            "issue_counts",
            {}
        )
    )


    if issue_counts:

        issue_table = (
            document.add_table(
                rows=1,
                cols=2
            )
        )

        issue_table.style = (
            "Table Grid"
        )

        issue_table.alignment = (
            WD_TABLE_ALIGNMENT.CENTER
        )


        header = (
            issue_table.rows[
                0
            ].cells
        )

        header[0].text = (
            "Issue Category"
        )

        header[1].text = (
            "Mentions"
        )


        for (
            issue,
            count
        ) in issue_counts.items():

            cells = (
                issue_table
                .add_row()
                .cells
            )

            cells[0].text = str(
                issue
            )

            cells[1].text = str(
                count
            )


    else:

        add_paragraph_text(
            document,
            (
                "No negative-review issue "
                "categories were detected."
            )
        )


    # ========================================================
    # 3. CUSTOMER VOICE
    # ========================================================

    add_section_heading(
        document,
        "3. Customer Voice Intelligence"
    )


    add_subheading(
        document,
        "3.1 Frequent Positive Terms"
    )


    positive_words = (
        analysis_summary.get(
            "top_positive_words",
            []
        )
    )


    if positive_words:

        positive_table = (
            document.add_table(
                rows=1,
                cols=2
            )
        )

        positive_table.style = (
            "Table Grid"
        )

        header = (
            positive_table.rows[
                0
            ].cells
        )

        header[0].text = "Word"
        header[1].text = "Frequency"


        for item in positive_words:

            cells = (
                positive_table
                .add_row()
                .cells
            )

            cells[0].text = str(
                item.get(
                    "word",
                    ""
                )
            )

            cells[1].text = str(
                item.get(
                    "count",
                    0
                )
            )


    add_subheading(
        document,
        "3.2 Frequent Negative Terms"
    )


    negative_words = (
        analysis_summary.get(
            "top_negative_words",
            []
        )
    )


    if negative_words:

        negative_table = (
            document.add_table(
                rows=1,
                cols=2
            )
        )

        negative_table.style = (
            "Table Grid"
        )

        header = (
            negative_table.rows[
                0
            ].cells
        )

        header[0].text = "Word"
        header[1].text = "Frequency"


        for item in negative_words:

            cells = (
                negative_table
                .add_row()
                .cells
            )

            cells[0].text = str(
                item.get(
                    "word",
                    ""
                )
            )

            cells[1].text = str(
                item.get(
                    "count",
                    0
                )
            )


    # ========================================================
    # 4. REPRESENTATIVE NEGATIVE REVIEWS
    # ========================================================

    add_section_heading(
        document,
        (
            "4. Representative Negative "
            "Customer Reviews"
        )
    )


    negative_reviews = (
        analysis_summary.get(
            "sample_negative_reviews",
            []
        )
    )


    if negative_reviews:

        for (
            index,
            review
        ) in enumerate(
            negative_reviews,
            start=1
        ):

            paragraph = (
                document.add_paragraph(
                    style="List Number"
                )
            )

            paragraph.add_run(
                str(review)
            )


    else:

        add_paragraph_text(
            document,
            "No negative reviews detected."
        )


    # ========================================================
    # PAGE BREAK BEFORE MANAGERS
    # ========================================================

    document.add_page_break()


    # ========================================================
    # 5. DEPARTMENT MANAGER REPORTS
    # ========================================================

    add_section_heading(
        document,
        "5. AI Department Manager Reports"
    )


    manager_order = [

        "Technical Manager",

        "Product Manager",

        "Customer Service Manager",

        "Marketing Manager",

        "Subscription Manager",
    ]


    for (
        manager_number,
        manager_name
    ) in enumerate(
        manager_order,
        start=1
    ):

        report = (
            manager_reports.get(
                manager_name
            )
        )


        if not report:
            continue


        document.add_heading(
            (
                f"5.{manager_number} "
                f"{manager_name}"
            ),
            level=2
        )


        provider = report.get(
            "provider",
            "Unknown"
        )

        model = report.get(
            "model",
            "Unknown"
        )


        source = document.add_paragraph()

        source_run = source.add_run(
            "LLM Provider: "
        )

        source_run.bold = True

        source.add_run(
            str(provider)
        )


        source.add_run(
            " | "
        )


        model_run = source.add_run(
            "Model: "
        )

        model_run.bold = True

        source.add_run(
            str(model)
        )


        document.add_paragraph()


        add_llm_report(
            document,
            report.get(
                "content",
                ""
            )
        )


        document.add_paragraph()


    # ========================================================
    # 6. EXECUTIVE REPORT
    # ========================================================

    document.add_page_break()


    add_section_heading(
        document,
        "6. Executive Brand Reputation Report"
    )


    if executive_report:

        provider = (
            executive_report.get(
                "provider",
                "Gemini"
            )
        )

        model = (
            executive_report.get(
                "model",
                "Unknown"
            )
        )


        source = document.add_paragraph()

        source_run = source.add_run(
            "Executive LLM Provider: "
        )

        source_run.bold = True

        source.add_run(
            str(provider)
        )


        source.add_run(
            " | "
        )


        model_run = source.add_run(
            "Model: "
        )

        model_run.bold = True

        source.add_run(
            str(model)
        )


        document.add_paragraph()


        add_llm_report(
            document,
            executive_report.get(
                "content",
                ""
            )
        )


    else:

        add_paragraph_text(
            document,
            (
                "Executive report has not "
                "been generated."
            )
        )


    # ========================================================
    # 7. LIMITATION NOTE
    # ========================================================

    document.add_page_break()


    add_section_heading(
        document,
        "7. System Interpretation Notes"
    )


    interpretation_notes = [

        (
            "Sentiment classifications are "
            "predictions produced by the trained "
            "DistilBERT model."
        ),

        (
            "Model confidence does not guarantee "
            "that an individual prediction is correct."
        ),

        (
            "Issue categories are derived from "
            "the system's predefined issue-analysis "
            "logic."
        ),

        (
            "LLM-generated management reports "
            "should be treated as decision-support "
            "recommendations rather than factual "
            "management decisions."
        ),

        (
            "OpenRouter reports may use different "
            "free models because the application "
            "requests the openrouter/free route."
        ),
    ]


    for note_text in (
        interpretation_notes
    ):

        document.add_paragraph(
            note_text,
            style="List Bullet"
        )


    # ========================================================
    # SAVE TO MEMORY
    # ========================================================

    output = BytesIO()

    document.save(
        output
    )

    output.seek(0)

    return output
