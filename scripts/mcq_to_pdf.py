import sys
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_mcq_pdf(input_file, output_file, title="MCQ Quiz"):
    # Read lines and remove empty ones
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Split into question blocks
    questions = []
    current_q = []
    for line in lines:
        if re.match(r'^\d+\.', line):  # detect question number like "1."
            if current_q:
                questions.append(current_q)
                current_q = []
        current_q.append(line)
    if current_q:
        questions.append(current_q)

    # PDF setup
    doc = SimpleDocTemplate(output_file, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    # Title style
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'],
                                 alignment=1, fontSize=20, textColor=colors.darkblue)
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))

    # Question & option styles
    q_style = ParagraphStyle('QuestionStyle', parent=styles['Normal'],
                             fontSize=12, spaceAfter=6, leading=16)
    opt_style = ParagraphStyle('OptionStyle', parent=styles['Normal'],
                               leftIndent=20, fontSize=11, leading=14)

    # Add content
    for q in questions:
        story.append(Paragraph(f"<b>{q[0]}</b>", q_style))
        for opt in q[1:]:
            story.append(Paragraph(opt, opt_style))
        story.append(Spacer(1, 10))

    # Build PDF
    doc.build(story)
    print(f"✅ PDF created successfully: {output_file}")

# -------- Main Program --------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mcq_to_pdf.py <input_file> [output_file] [title]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else "mcq_quiz.pdf"
    title = sys.argv[3] if len(sys.argv) >= 4 else "MCQ Quiz"

    create_mcq_pdf(input_file, output_file, title)

